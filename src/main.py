from fastapi import FastAPI

from database import models
from api.base import api_router
from database.database import engine, Base


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(api_router)


@app.get("/")
async def root():
    return {"message": "Welcome to the Expenses Chatbot API!"}
