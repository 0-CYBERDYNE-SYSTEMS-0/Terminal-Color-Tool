"""Color extraction API endpoint."""

import tempfile
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException

from app.image_processor import ImageProcessor

router = APIRouter()
image_processor = ImageProcessor()


@router.post("/extract-colors")
async def extract_colors(image: UploadFile = File(...)):
    """Extract colors from an uploaded image."""
    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(image.filename or "img").suffix) as tmp:
        content = await image.read()
        tmp.write(content)
        tmp_path = tmp.name
    
    try:
        colors = image_processor.extract_colors(tmp_path, num_colors=16)
        if not colors:
            raise HTTPException(status_code=400, detail="Could not extract colors from image")
        return {"colors": colors}
    finally:
        Path(tmp_path).unlink(missing_ok=True)
