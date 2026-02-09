
import os
import json
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime
from openai import OpenAI, OpenAIError
from sqlmodel import Session, select

from app.models import User, Conversation, Message, MessageRole
from app.mcp.tools import TOOL_SCHEMAS, AVAILABLE_TOOLS, current_user_cv, db_session_cv
from app.agents.prompts import ORCHESTRATOR_PROMPT

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OpenAI Client
# Ensure OPENAI_API_KEY is set in environment or .env
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

model_name = "gpt-4o-mini" # Using mini for better compatibility and cost

def get_or_create_conversation(session: Session, user_id: str, conversation_id: Optional[str] = None) -> Conversation:
    try:
        if conversation_id:
            conv = session.exec(select(Conversation).where(Conversation.id == conversation_id, Conversation.user_id == user_id)).one_or_none()
            if conv:
                return conv
    except Exception as e:
        print(f"Error fetching conversation: {e}")
    
    # Create new
    try:
        new_conv = Conversation(user_id=user_id)
        session.add(new_conv)
        session.commit()
        session.refresh(new_conv)
        return new_conv
    except Exception as e:
        print(f"Error creating conversation: {e}")
        raise e

def format_history(messages: List[Message]) -> List[Dict[str, Any]]:
    """
    Convert DB messages to OpenAI API format.
    Handles special storage of tool calls in 'content'.
    """
    api_messages = []
    for msg in messages:
        if msg.role == MessageRole.SYSTEM:
            api_messages.append({"role": "system", "content": msg.content})
        elif msg.role == MessageRole.USER:
            api_messages.append({"role": "user", "content": msg.content})
        elif msg.role == MessageRole.ASSISTANT:
            # Check if content implies tool calls
            # We store tool calls as JSON string in content if present
            try:
                # heuristic: if starts with { and contains tool_calls, parse it
                if msg.content.startswith("{") and '"tool_calls":' in msg.content:
                    data = json.loads(msg.content)
                    api_messages.append(data) # Inject the whole object (content + tool_calls)
                else:
                    api_messages.append({"role": "assistant", "content": msg.content})
            except:
                 api_messages.append({"role": "assistant", "content": msg.content})
        elif msg.role == MessageRole.TOOL:
            # Content should be JSON with tool_call_id and content
            try:
                data = json.loads(msg.content)
                api_messages.append({
                    "role": "tool",
                    "tool_call_id": data.get("tool_call_id"),
                    "content": data.get("content")
                })
            except:
                # If parsing fails, skip or treat as crude text
                pass
    return api_messages

def run_agent(user: User, session: Session, message_content: str, conversation_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Main entry point for Chat.
    1. Sets context.
    2. Loads history.
    3. Calls LLM (loop for tools).
    4. Persists results.
    """
    # 1. Set Context
    current_user_cv.set(user)
    db_session_cv.set(session)

    # 2. Manage Conversation
    conversation = get_or_create_conversation(session, user.id, conversation_id)
    
    # 3. Append User Message
    user_msg = Message(
        conversation_id=conversation.id,
        role=MessageRole.USER,
        content=message_content
    )
    session.add(user_msg)
    session.commit()
    
    # 4. Load History
    # Fetch last 20 messages to keep context window manageable
    # Subquery or fetch all and slice might be easier, but let's query efficiently
    # We want top 20 newest, then sorted by time asc
    stmt = (
        select(Message)
        .where(Message.conversation_id == conversation.id)
        .order_by(Message.created_at.desc())
        .limit(20)
    )
    history_msgs = list(reversed(session.exec(stmt).all()))
    
    messages_payload = [{"role": "system", "content": ORCHESTRATOR_PROMPT.replace("{{current_date}}", str(datetime.now().date())).replace("{{user_name}}", user.name)}]
    messages_payload.extend(format_history(history_msgs))
    
    # 5. LLM Loop
    final_response_text = ""
    
    try:
        # First call
        response = client.chat.completions.create(
            model=model_name,
            messages=messages_payload,
            tools=TOOL_SCHEMAS,
            tool_choice="auto"
        )
        
        response_msg = response.choices[0].message
        
        # Check for tool calls
        if response_msg.tool_calls:
            # Append Assistant Message with Tool Calls to DB and Payload
            # We serialize the message object to store it
            msg_data = {
                "role": "assistant",
                "content": response_msg.content,
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": tc.type,
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    } for tc in response_msg.tool_calls
                ]
            }
            
            # Save to DB
            db_asst_msg = Message(
                conversation_id=conversation.id,
                role=MessageRole.ASSISTANT,
                content=json.dumps(msg_data)
            )
            session.add(db_asst_msg)
            session.commit()
            
            # Update payload for next turn
            messages_payload.append(msg_data)
            
            # Execute Tools
            for tool_call in response_msg.tool_calls:
                func_name = tool_call.function.name
                func_args = json.loads(tool_call.function.arguments)
                tool_call_id = tool_call.id
                
                if func_name in AVAILABLE_TOOLS:
                    # Execute
                    try:
                        result = AVAILABLE_TOOLS[func_name](**func_args)
                    except Exception as e:
                        result = f"Error executing tool {func_name}: {str(e)}"
                else:
                    result = f"Error: Tool {func_name} not found."
                
                # Append Tool Output to DB and Payload
                tool_msg_data = {
                    "tool_call_id": tool_call_id,
                    "content": str(result)
                }
                
                db_tool_msg = Message(
                    conversation_id=conversation.id,
                    role=MessageRole.TOOL,
                    content=json.dumps(tool_msg_data)
                )
                session.add(db_tool_msg)
                session.commit()
                
                messages_payload.append({
                    "role": "tool",
                    "tool_call_id": tool_call_id,
                    "content": str(result)
                })
            
            # Second call to get final response
            final_response = client.chat.completions.create(
                model=model_name,
                messages=messages_payload
            )
            final_response_text = final_response.choices[0].message.content
            
        else:
            final_response_text = response_msg.content
            
        # Save Final Assistant Response
        if final_response_text:
            final_msg = Message(
                conversation_id=conversation.id,
                role=MessageRole.ASSISTANT,
                content=final_response_text
            )
            session.add(final_msg)
            session.commit()
            
        return {
            "conversation_id": conversation.id,
            "message": final_response_text
        }

    except Exception as e:
        logger.error(f"Error in agent run: {e}")
        return {
            "conversation_id": conversation.id,
            "message": "I encountered an error processing your request. Please try again."
        }
