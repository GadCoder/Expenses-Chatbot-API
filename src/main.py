import time
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from database import models
from api.base import api_router
from database.database import engine, Base
from src.core.logging_config import setup_logging

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup
    Base.metadata.create_all(bind=engine)
    yield
    # On shutdown (if needed)


app = FastAPI(lifespan=lifespan)

logger = logging.getLogger(__name__)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    logger.info(f"Request: {request.method} {request.url.path}")
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"Response: {response.status_code} in {process_time:.2f}s")
    return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "Internal server error"},
    )


app.include_router(api_router)


@app.get("/")
async def root():
    return {"message": "Welcome to the Expenses Chatbot API!"}
