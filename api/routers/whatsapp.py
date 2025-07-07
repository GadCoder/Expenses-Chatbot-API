from fastapi import APIRouter, Request, Response, Depends
from sqlalchemy.orm import Session
from services.nlp_service import process_message
from database.database import SessionLocal, engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

router = APIRouter()


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/webhook")
async def whatsapp_webhook(request: Request, db: Session = Depends(get_db)):
    # In a real WhatsApp integration, you would parse the incoming message
    # from the request body. For now, we'll assume a simple text message.
    # This part needs to be adapted based on the actual WhatsApp API payload.

    # For demonstration, let's assume the message is in the request body as plain text
    # or a simple JSON with a 'message' key.
    try:
        body = await request.json()
        message = body.get("message", "")
    except Exception:
        message = await request.body()
        message = message.decode("utf-8")
    if not message:
        return Response(content="No message received", status_code=200)

    response_text = process_message(message, db)
    return {"reply": response_text}
