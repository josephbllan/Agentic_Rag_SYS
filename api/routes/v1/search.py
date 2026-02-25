"""
Search Routes (V1)
Text, image, and hybrid search endpoints. Requires authentication.
Rate-limited to 30 req/min per IP.
"""
from fastapi import APIRouter, HTTPException, Depends, Request

from api.controllers.search_controller import SearchController
from api.dependencies import get_search_engine
from api.schemas.text_search_request import TextSearchRequest
from api.schemas.image_search_request import ImageSearchRequest
from api.schemas.hybrid_search_request import HybridSearchRequest
from api.security.jwt_handler import get_current_active_user
from api.schemas.user import User
from api.middleware.rate_limiter import limiter

router = APIRouter()


def get_search_controller(
    search_engine=Depends(get_search_engine),
) -> SearchController:
    return SearchController(search_engine)


@router.post("/text")
@limiter.limit("30/minute")
async def text_search(
    request: Request,
    body: TextSearchRequest,
    controller: SearchController = Depends(get_search_controller),
    current_user: User = Depends(get_current_active_user),
):
    try:
        result = await controller.text_search(
            query=body.query,
            filters=body.filters,
            limit=body.limit,
            similarity_threshold=body.similarity_threshold,
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/image")
@limiter.limit("30/minute")
async def image_search(
    request: Request,
    body: ImageSearchRequest,
    controller: SearchController = Depends(get_search_controller),
    current_user: User = Depends(get_current_active_user),
):
    try:
        result = await controller.image_search(
            image_path=body.image_path,
            filters=body.filters,
            limit=body.limit,
            similarity_threshold=body.similarity_threshold,
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/hybrid")
@limiter.limit("30/minute")
async def hybrid_search(
    request: Request,
    body: HybridSearchRequest,
    controller: SearchController = Depends(get_search_controller),
    current_user: User = Depends(get_current_active_user),
):
    try:
        result = await controller.hybrid_search(
            query=body.query,
            image_path=body.image_path,
            filters=body.filters,
            limit=body.limit,
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
