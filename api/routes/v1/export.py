"""
Export Routes (V1)
Export search results. Requires authentication.
"""
from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import JSONResponse, FileResponse
from pathlib import Path
import uuid

from api.security.jwt_handler import get_current_active_user, User
from api.dependencies import get_search_engine

router = APIRouter()


@router.get("/results")
async def export_results(
    query: str = Query(..., description="Search query"),
    format: str = Query("json", description="Export format (json, csv)"),
    limit: int = Query(100, gt=0, le=1000, description="Maximum results"),
    current_user: User = Depends(get_current_active_user)
):
    """Export search results (requires authentication)"""
    try:
        search_engine = get_search_engine()
        results = search_engine.text_to_image_search(query, limit=limit)

        if format == "csv":
            import pandas as pd
            df = pd.DataFrame(results)
            export_dir = Path("exports")
            export_dir.mkdir(exist_ok=True)
            csv_path = export_dir / f"results_{uuid.uuid4()}.csv"
            df.to_csv(csv_path, index=False)
            return FileResponse(str(csv_path), media_type="text/csv", filename="results.csv")
        else:
            return JSONResponse(content=results)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
