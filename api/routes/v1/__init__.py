from fastapi import APIRouter
from .search import router as search_router
from .system import router as system_router
from .auth import router as auth_router
from .upload import router as upload_router
from .export import router as export_router

router = APIRouter()
router.include_router(auth_router, prefix="/auth", tags=["authentication"])
router.include_router(search_router, prefix="/search", tags=["search"])
router.include_router(upload_router, prefix="/files", tags=["files"])
router.include_router(export_router, prefix="/export", tags=["export"])
router.include_router(system_router, tags=["system"])
