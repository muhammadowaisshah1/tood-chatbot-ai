'use client';

import React, { useState, useRef, useEffect } from 'react';
import { sendChatMessage } from '@/lib/api';
import { X, MessageCircle, Send, Minimize2, Maximize2, Trash2 } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

interface Message {
    role: 'user' | 'assistant';
    content: string;
}

export default function ChatInterface() {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState<Message[]>([]);
    const [inputValue, setInputValue] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [conversationId, setConversationId] = useState<string | undefined>(undefined);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    // Check if user is logged in (crude check via token presence)
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    useEffect(() => {
        // Client-side only check
        const token = localStorage.getItem('auth_token');
        setIsAuthenticated(!!token);
    }, [isOpen]);

    useEffect(() => {
        scrollToBottom();
    }, [messages, isOpen]);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    const handleSendMessage = async (e?: React.FormEvent) => {
        e?.preventDefault();
        if (!inputValue.trim() || isLoading) return;

        const userMsg = inputValue.trim();
        setInputValue('');

        // Optimistic UI update
        setMessages((prev) => [...prev, { role: 'user', content: userMsg }]);
        setIsLoading(true);

        try {
            const response = await sendChatMessage(userMsg, conversationId);

            setConversationId(response.conversation_id);
            setMessages((prev) => [
                ...prev,
                { role: 'assistant', content: response.message }
            ]);
        } catch (error) {
            console.error(error);
            setMessages((prev) => [
                ...prev,
                { role: 'assistant', content: '⚠️ Sorry, I encountered an error. Please try again.' }
            ]);
        } finally {
            setIsLoading(false);
        }
    };

    const startNewChat = () => {
        setMessages([]);
        setConversationId(undefined);
    };

    if (!isAuthenticated) return null; // Don't show if not logged in

    return (
        <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end">
            {/* Chat Window */}
            {isOpen && (
                <div className="mb-4 w-[350px] sm:w-[400px] h-[500px] bg-white dark:bg-gray-800 rounded-lg shadow-2xl border border-gray-200 dark:border-gray-700 flex flex-col overflow-hidden transition-all duration-300 ease-in-out">
                    {/* Header */}
                    <div className="p-3 bg-violet-600 text-white flex justify-between items-center shadow-md">
                        <div className="flex items-center gap-2">
                            <MessageCircle size={20} />
                            <h3 className="font-semibold text-sm">AI Assistant</h3>
                        </div>
                        <div className="flex gap-2">
                            <button
                                onClick={startNewChat}
                                title="New Chat"
                                className="hover:bg-violet-700 p-1 rounded transition-colors"
                            >
                                <Trash2 size={16} />
                            </button>
                            <button
                                onClick={() => setIsOpen(false)}
                                className="hover:bg-violet-700 p-1 rounded transition-colors"
                            >
                                <Minimize2 size={18} />
                            </button>
                        </div>
                    </div>

                    {/* Messages Area */}
                    <div className="flex-1 overflow-y-auto p-4 bg-gray-50 dark:bg-gray-900 space-y-4">
                        {messages.length === 0 && (
                            <div className="flex flex-col items-center justify-center h-full text-gray-400 text-center text-sm p-4">
                                <MessageCircle size={48} className="mb-2 opacity-20" />
                                <p>Hello! I can help you manage your tasks.</p>
                                <p className="text-xs mt-2">Try saying "Add a task to buy milk"</p>
                            </div>
                        )}

                        {messages.map((msg, idx) => (
                            <div
                                key={idx}
                                className={`flex w-full ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                            >
                                <div
                                    className={`max-w-[85%] rounded-2xl px-4 py-2 text-sm shadow-sm ${msg.role === 'user'
                                        ? 'bg-violet-600 text-white rounded-br-none'
                                        : 'bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-100 rounded-bl-none border border-gray-100 dark:border-gray-600'
                                        }`}
                                >
                                    {msg.role === 'assistant' ? (
                                        <div className="prose prose-sm dark:prose-invert max-w-none">
                                            <ReactMarkdown>{msg.content}</ReactMarkdown>
                                        </div>
                                    ) : (
                                        msg.content
                                    )}
                                </div>
                            </div>
                        ))}

                        {isLoading && (
                            <div className="flex justify-start w-full">
                                <div className="bg-white dark:bg-gray-700 rounded-2xl rounded-bl-none px-4 py-3 shadow-sm border border-gray-100 dark:border-gray-600 flex items-center gap-2">
                                    <div className="w-2 h-2 bg-violet-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                                    <div className="w-2 h-2 bg-violet-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                                    <div className="w-2 h-2 bg-violet-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                                </div>
                            </div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>

                    {/* Input Area */}
                    <form onSubmit={handleSendMessage} className="p-3 bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 flex gap-2">
                        <input
                            type="text"
                            value={inputValue}
                            onChange={(e) => setInputValue(e.target.value)}
                            placeholder="Type a message..."
                            className="flex-1 bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white rounded-full px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-violet-500"
                            disabled={isLoading}
                        />
                        <button
                            type="submit"
                            disabled={!inputValue.trim() || isLoading}
                            className="bg-violet-600 hover:bg-violet-700 disabled:opacity-50 text-white p-2 rounded-full transition-all shadow-sm"
                        >
                            <Send size={18} />
                        </button>
                    </form>
                </div>
            )}

            {/* Toggle Button */}
            {!isOpen && (
                <button
                    onClick={() => setIsOpen(true)}
                    className="group flex items-center justify-center p-4 bg-violet-600 hover:bg-violet-700 text-white rounded-full shadow-xl transition-all hover:scale-105 active:scale-95"
                >
                    <MessageCircle size={28} className="group-hover:animate-pulse" />
                    <span className="sr-only">Open Chat</span>
                </button>
            )}
        </div>
    );
}
