import os
import sys
from pathlib import Path

# Add project root to sys.path so modules can be imported reliably
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from flask import Flask, request, jsonify, send_from_directory
from backend.config import FRONTEND_DIR, UPLOAD_DIR, MAX_CONTENT_LENGTH, HOST, PORT, DEBUG
from backend.utils.file_handler import save_upload_file
from ocr.pipeline import run_ocr_pipeline

app = Flask(__name__, static_folder=str(FRONTEND_DIR), static_url_path="")
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH


@app.route("/")
def index():
    """Serve frontend index.html."""
    return send_from_directory(str(FRONTEND_DIR), "index.html")


@app.route("/<path:path>")
def static_proxy(path):
    """Serve static frontend files (CSS, JS, assets)."""
    file_path = FRONTEND_DIR / path
    if file_path.exists() and file_path.is_file():
        return send_from_directory(str(FRONTEND_DIR), path)
    return jsonify({"error": "File not found"}), 404


@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint to verify backend operational status."""
    return jsonify({
        "status": "healthy",
        "service": "SIH26034 Compliance Scanner Backend",
        "stage": "Phase 2 - OCR & Computer Vision Pipeline"
    }), 200


@app.route("/api/upload", methods=["POST"])
def upload_image():
    """
    Receive packaged commodity image and save it securely.
    Accepts multipart/form-data with key 'image' (or fallback 'file').
    """
    file = request.files.get("image") or request.files.get("file")
    if not file or file.filename == "":
        return jsonify({
            "status": "error",
            "message": "No image file provided in request. Please select an image file under the 'image' field."
        }), 400

    try:
        saved_file_info = save_upload_file(file)
        return jsonify({
            "status": "success",
            "message": "Image uploaded successfully. Ready for OCR and compliance pipeline.",
            "file": {
                "filename": saved_file_info["filename"],
                "original_filename": saved_file_info["original_filename"],
                "size_bytes": saved_file_info["size_bytes"]
            }
        }), 200
    except ValueError as val_err:
        return jsonify({
            "status": "error",
            "message": str(val_err)
        }), 400
    except Exception as err:
        return jsonify({
            "status": "error",
            "message": f"Server error processing upload: {str(err)}"
        }), 500


@app.route("/api/ocr", methods=["POST"])
def extract_ocr():
    """
    OCR endpoint: Accepts an uploaded image (or reference to existing uploaded file),
    runs OpenCV preprocessing + PaddleOCR, and returns structured OCR JSON.
    """
    saved_path = None
    original_name = None

    # Option 1: File uploaded directly via multipart/form-data
    file = request.files.get("image") or request.files.get("file")
    if file and file.filename != "":
        try:
            saved_file_info = save_upload_file(file)
            saved_path = Path(saved_file_info["file_path"])
            original_name = saved_file_info["original_filename"]
        except ValueError as val_err:
            return jsonify({
                "status": "error",
                "message": str(val_err)
            }), 400

    # Option 2: Filename passed in JSON or form data (for image already in uploads/)
    if not saved_path:
        req_json = request.get_json(silent=True) or {}
        filename = req_json.get("filename") or request.form.get("filename")
        if filename:
            target_path = (UPLOAD_DIR / filename).resolve()
            if target_path.exists() and target_path.is_file() and target_path.parent == UPLOAD_DIR.resolve():
                saved_path = target_path
                original_name = filename
            else:
                return jsonify({
                    "status": "error",
                    "message": f"Specified file '{filename}' was not found in uploads directory."
                }), 404

    if not saved_path:
        return jsonify({
            "status": "error",
            "message": "No image provided. Please upload an image file under key 'image' or specify a valid 'filename'."
        }), 400

    # Run OpenCV Preprocessing + PaddleOCR pipeline
    try:
        ocr_data = run_ocr_pipeline(saved_path)
        return jsonify({
            "status": "success",
            "image": ocr_data["image"],
            "original_filename": original_name,
            "results": ocr_data["results"],
            "total_lines": len(ocr_data["results"])
        }), 200
    except Exception as ocr_err:
        return jsonify({
            "status": "error",
            "message": f"OCR extraction failed: {str(ocr_err)}"
        }), 500


@app.route("/uploads/<filename>", methods=["GET"])
def get_uploaded_file(filename):
    """Serve uploaded images for verification or frontend preview."""
    return send_from_directory(str(UPLOAD_DIR), filename)


@app.errorhandler(413)
def file_too_large(e):
    return jsonify({
        "status": "error",
        "message": f"File size exceeds maximum allowed limit ({MAX_CONTENT_LENGTH // (1024 * 1024)} MB)."
    }), 413


if __name__ == "__main__":
    print(f"==================================================")
    print(f" SIH26034 - Packaged Commodity Compliance Scanner ")
    print(f" Server running at: http://{HOST}:{PORT}")
    print(f" Upload directory:  {UPLOAD_DIR}")
    print(f" OCR Endpoint:      http://{HOST}:{PORT}/api/ocr")
    print(f"==================================================")
    app.run(host=HOST, port=PORT, debug=DEBUG)
