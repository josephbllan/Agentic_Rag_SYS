"""
Upload Routes (V1)
File upload endpoints. Requires authentication.
"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from pathlib import Path
import uuid
import shutil

from api.security.jwt_handler import get_current_active_user, User
from config.settings import API_CONFIG

router = APIRouter()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/upload")
async def upload_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user)
):
    """Upload an image for search (requires authentication)"""
    try:
        if not file.content_type or not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")

        contents = await file.read()
        if len(contents) > API_CONFIG["max_file_size"]:
            raise HTTPException(status_code=400, detail="File too large (max 10MB)")

        file_extension = Path(file.filename).suffix if file.filename else ".jpg"
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        upload_path = UPLOAD_DIR / unique_filename

        with open(upload_path, "wb") as buffer:
            buffer.write(contents)

        return {
            "filename": unique_filename,
            "path": str(upload_path),
            "size": len(contents),
            "content_type": file.content_type
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
