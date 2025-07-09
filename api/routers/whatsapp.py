from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import APIRouter, Response, Depends

from database.database import get_db
from services.messages.message_handler import process_message
from services.gemini.gemini_service import GeminiService, get_gemini_service


router = APIRouter()


class RequestPayload(BaseModel):
    chat_id: str
    message: str | None


@router.post("/process-message")
async def whatsapp_webhook(
    request_payload: RequestPayload,
    db: Session = Depends(get_db),
    gemini: GeminiService = Depends(get_gemini_service),
):
    chat_id = request_payload.chat_id
    message = request_payload.message
    if not message:
        return Response(content="No message received", status_code=400)
    answer = process_message(chat_id=chat_id, message=message, db=db, gemini=gemini)
    if not answer:
        return Response(content="Couldn't process message", status_code=400)
    return {"reply": answer}
