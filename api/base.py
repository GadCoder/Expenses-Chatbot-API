from fastapi import APIRouter
from .routers.users import router as users_router
from .routers.whatsapp import router as whatsapp_router

api_router = APIRouter()

api_router.include_router(users_router, prefix=("/users"), tags=["users"])
api_router.include_router(whatsapp_router, prefix=("/webhook"), tags=["whatsapp"])
