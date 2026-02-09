from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.dependencies import get_current_user, get_db
from app.models import User
from app.agents.orchestrator import run_agent

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

@router.post("", status_code=status.HTTP_200_OK)
def chat_endpoint(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    """
    Chat with the AI Assistant.
    
    Returns:
        JSON object with 'conversation_id' and 'message' (assistant response).
    """
    if not request.message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    try:
        response = run_agent(
            user=current_user,
            session=session,
            message_content=request.message,
            conversation_id=request.conversation_id
        )
        return response
    except Exception as e:
        import traceback
        # Log the error with traceback
        print(f"Chat Error: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error processing chat request: {str(e)}")
