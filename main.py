from fastapi import FastAPI
from api.routers import whatsapp

app = FastAPI()

app.include_router(whatsapp.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Expenses Chatbot API!"}