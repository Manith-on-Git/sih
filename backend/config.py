import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"
UPLOAD_DIR = BASE_DIR / "uploads"

# Upload configurations
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "bmp", "tiff"}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload size

# Server configurations
HOST = "127.0.0.1"
PORT = 5000
DEBUG = True
