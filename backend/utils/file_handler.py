import os
import uuid
from datetime import datetime
from pathlib import Path
from werkzeug.utils import secure_filename
from backend.config import ALLOWED_EXTENSIONS, UPLOAD_DIR


def is_allowed_file(filename: str) -> bool:
    """Check whether the uploaded file has an allowed image extension."""
    if not filename or "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in ALLOWED_EXTENSIONS


def save_upload_file(file_storage) -> dict:
    """
    Safely save an uploaded FileStorage object to the upload folder.
    Returns metadata about the saved file.
    """
    if not file_storage or file_storage.filename == "":
        raise ValueError("No file provided for upload.")

    original_filename = file_storage.filename
    if not is_allowed_file(original_filename):
        allowed_list = ", ".join(sorted(ALLOWED_EXTENSIONS))
        raise ValueError(f"Invalid file type. Allowed formats: {allowed_list}")

    # Ensure uploads directory exists
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    # Sanitize and create unique filename
    safe_base = secure_filename(original_filename)
    # Extract extension safely
    ext = safe_base.rsplit(".", 1)[1].lower() if "." in safe_base else "jpg"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_token = uuid.uuid4().hex[:8]
    safe_filename = f"pkg_{timestamp}_{unique_token}.{ext}"

    destination_path = UPLOAD_DIR / safe_filename
    file_storage.save(str(destination_path))

    file_size = destination_path.stat().st_size

    return {
        "filename": safe_filename,
        "original_filename": original_filename,
        "file_path": str(destination_path),
        "size_bytes": file_size,
    }
