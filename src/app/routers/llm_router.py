# src/app/routers/llm_router.py
from fastapi import APIRouter, Body
from pydantic import BaseModel
from typing import Optional, Any, Dict

router = APIRouter()

class LLMChatRequest(BaseModel):
    userId: str
    message: str
    context: Optional[Any] = None

class LLMChatResponse(BaseModel):
    reply_text: str
    action: Optional[Dict[str, Any]] = None

@router.post("/", response_model=LLMChatResponse)
async def llm_chat(payload: LLMChatRequest = Body(...)):
    return LLMChatResponse(reply_text="Demo", action=None)
