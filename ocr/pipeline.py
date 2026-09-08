"""
OCR Pipeline for Packaged Commodity Compliance Scanner.
Combines OpenCV image preprocessing with PaddleOCR text recognition
to produce structured JSON output (text, confidence, bounding boxes).
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Union
import numpy as np

# On Windows, preload torch if present to resolve MKL/OpenMP DLL conflict with paddle
try:
    import torch
except Exception:
    pass

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from computer_vision.preprocessing import preprocess_for_ocr

# Global singleton OCR engine instance to avoid reloading heavy weights on every request
_OCR_ENGINE = None


def get_ocr_engine():
    """
    Lazy-load and cache the PaddleOCR engine instance.
    Uses CPU with enable_mkldnn=False for cross-platform stability on Windows.
    """
    global _OCR_ENGINE
    if _OCR_ENGINE is None:
        import paddle
        # Disable MKLDNN to ensure stable execution on Windows CPU
        paddle.set_flags({"FLAGS_use_mkldnn": 0})

        from paddleocr import PaddleOCR
        # Initialize PaddleOCR with textline orientation and CPU stability flags
        try:
            _OCR_ENGINE = PaddleOCR(
                use_textline_orientation=True,
                lang="en",
                enable_mkldnn=False
            )
        except TypeError:
            _OCR_ENGINE = PaddleOCR(
                use_angle_cls=True,
                lang="en"
            )
    return _OCR_ENGINE


def _coords_to_box(coords: Union[List, np.ndarray]) -> Dict[str, int]:
    """
    Convert coordinates to {x, y, width, height}.
    Handles both [xmin, ymin, xmax, ymax] and 4-point polygon [[x1,y1], ...].
    """
    coords_list = list(coords)
    if len(coords_list) == 4 and not isinstance(coords_list[0], (list, tuple, np.ndarray)):
        # Format: [xmin, ymin, xmax, ymax]
        min_x = max(0, int(round(float(coords_list[0]))))
        min_y = max(0, int(round(float(coords_list[1]))))
        max_x = int(round(float(coords_list[2])))
        max_y = int(round(float(coords_list[3])))
    else:
        # Format: 4-point polygon [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
        x_pts = [float(p[0]) for p in coords_list]
        y_pts = [float(p[1]) for p in coords_list]
        min_x = max(0, int(round(min(x_pts))))
        min_y = max(0, int(round(min(y_pts))))
        max_x = int(round(max(x_pts)))
        max_y = int(round(max(y_pts)))

    width = max(0, max_x - min_x)
    height = max(0, max_y - min_y)

    return {
        "x": min_x,
        "y": min_y,
        "width": width,
        "height": height
    }


def run_ocr_pipeline(image_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Execute the end-to-end OCR pipeline on a packaged commodity image:
    1. Preprocesses image with OpenCV (CLAHE, denoising).
    2. Runs PaddleOCR detection and recognition.
    3. Formats the output into structured JSON containing detected text,
       confidence score, and bounding-box coordinates.
       
    Returns dictionary with schema:
    {
      "image": "filename.jpg",
      "results": [
        {
          "text": "MRP Rs. 50.00",
          "confidence": 0.96,
          "box": {
            "x": 100,
            "y": 200,
            "width": 150,
            "height": 40
          }
        }
      ]
    }
    """
    img_path = Path(image_path).resolve()
    if not img_path.exists():
        raise FileNotFoundError(f"Image not found at path: {img_path}")

    filename = img_path.name

    # Step 1: Preprocess image with OpenCV
    preprocessed_img = preprocess_for_ocr(img_path)

    # Step 2: Run PaddleOCR
    ocr_engine = get_ocr_engine()
    raw_predictions = list(ocr_engine.predict(preprocessed_img))

    structured_results: List[Dict[str, Any]] = []

    if raw_predictions:
        for pred in raw_predictions:
            # Handle PaddleOCR 3.x dict format
            if isinstance(pred, dict):
                rec_texts = pred.get("rec_texts", [])
                rec_scores = pred.get("rec_scores", [])
                rec_boxes = pred.get("rec_boxes", [])
                rec_polys = pred.get("rec_polys", [])

                for idx, text in enumerate(rec_texts):
                    text_str = str(text).strip()
                    if not text_str:
                        continue

                    conf = float(rec_scores[idx]) if idx < len(rec_scores) else 0.0

                    if idx < len(rec_boxes):
                        box_dict = _coords_to_box(rec_boxes[idx])
                    elif idx < len(rec_polys):
                        box_dict = _coords_to_box(rec_polys[idx])
                    else:
                        box_dict = {"x": 0, "y": 0, "width": 0, "height": 0}

                    structured_results.append({
                        "text": text_str,
                        "confidence": round(conf, 4),
                        "box": box_dict
                    })

            # Handle PaddleOCR 2.x list-of-lines format
            elif isinstance(pred, list):
                for line in pred:
                    try:
                        poly_points = line[0]
                        text_info = line[1]
                        text_str = str(text_info[0]).strip()
                        conf = float(text_info[1])
                        if text_str:
                            structured_results.append({
                                "text": text_str,
                                "confidence": round(conf, 4),
                                "box": _coords_to_box(poly_points)
                            })
                    except Exception:
                        continue

    return {
        "image": filename,
        "results": structured_results
    }
