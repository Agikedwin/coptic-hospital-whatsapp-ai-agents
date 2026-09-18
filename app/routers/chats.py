from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from requests import session
from sqlalchemy.orm import Session

from app import schemas
from app.crud import clients as crud
from app.database import get_db
from app.exceptions import CRUDConflictError
from  agent.agent import  run_chat

router = APIRouter(prefix="/chats", tags=["Chats"])


@router.post("/chat", response_model=schemas.ChatResponse)
async def chat(request: schemas.ChatRequest) -> schemas.ChatResponse:
    response = await  run_chat(
        messages = request.message,
        session_id = request.session_id,
        client_id = request.client_id,
    )
    return schemas.ChatResponse(message = response, session_id=request.session_id)


