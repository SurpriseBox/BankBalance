from fastapi import APIRouter

from .operations.router import router as operations_router
from .users.router import router as users_router

router = APIRouter()
router.include_router(operations_router)
router.include_router(users_router)
