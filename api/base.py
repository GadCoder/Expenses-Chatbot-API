from fastapi import APIRouter
from .routers.whatsapp import router as whatsapp_router

api_router = APIRouter()

api_router.include_router(whatsapp_router, prefix=("/webhook"), tags=["whatsapp"])
