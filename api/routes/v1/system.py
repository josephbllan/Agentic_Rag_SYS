"""
System Routes (V1)
Health checks and system information
"""
from fastapi import APIRouter, Depends, HTTPException

from api.controllers.health_controller import HealthController
from api.security.jwt_handler import get_current_active_user, User
from api.dependencies import get_search_engine
from config.settings import APP_VERSION
from core.search_engine import SearchEngine

router = APIRouter()


def get_health_controller() -> HealthController:
    """Creates and returns a new HealthController instance
    to serve as a FastAPI dependency for health-check endpoints.
    """
    return HealthController()


@router.get("/health")
async def health_check(
    controller: HealthController = Depends(get_health_controller),
):
    """Liveness probe (public)"""
    return await controller.check_health()


@router.get("/ready")
async def readiness_check(
    controller: HealthController = Depends(get_health_controller),
):
    """Readiness probe (public) -- checks DB and critical deps"""
    result = await controller.check_ready()
    if result["status"] != "ready":
        raise HTTPException(status_code=503, detail=result)
    return result


@router.get("/health/detailed")
async def detailed_health_check(
    controller: HealthController = Depends(get_health_controller),
    current_user: User = Depends(get_current_active_user),
):
    """Detailed health check with system metrics (requires authentication)"""
    return await controller.check_detailed_health()


@router.get("/system/status")
async def system_status(
    search_engine: SearchEngine = Depends(get_search_engine),
    current_user: User = Depends(get_current_active_user),
):
    """Get system status (requires authentication)"""
    try:
        vector_stats = search_engine.vector_db.get_stats()
        return {
            "status": "healthy",
            "vector_database": vector_stats,
            "search_engine": "active",
            "api_version": APP_VERSION,
        }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


@router.post("/system/rebuild-index")
async def rebuild_index(
    search_engine: SearchEngine = Depends(get_search_engine),
    current_user: User = Depends(get_current_active_user),
):
    """Rebuild vector index (requires admin role)"""
    if "admin" not in current_user.roles:
        raise HTTPException(status_code=403, detail="Admin role required")
    try:
        search_engine.vector_db.rebuild_index()
        return {"status": "success", "message": "Vector index rebuilt"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analytics/stats")
async def analytics_stats(
    search_engine: SearchEngine = Depends(get_search_engine),
    current_user: User = Depends(get_current_active_user),
):
    """Get search analytics (requires authentication)"""
    try:
        return search_engine.get_search_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
