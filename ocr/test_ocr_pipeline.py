"""
Test script for the OCR and Computer Vision pipeline.
Tests preprocessing and text recognition on sample package images.
"""

import sys
import json
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ocr.pipeline import run_ocr_pipeline


def test_sample_image():
    sample_img = PROJECT_ROOT / "test_data" / "sample_package.png"
    if not sample_img.exists():
        raise FileNotFoundError(f"Sample test image not found at {sample_img}")

    print(f"Running OCR pipeline on: {sample_img}")
    ocr_result = run_ocr_pipeline(sample_img)

    print("\n--- OCR JSON RESULT ---")
    print(json.dumps(ocr_result, indent=2))

    # Assertions
    assert ocr_result["image"] == "sample_package.png"
    results = ocr_result["results"]
    assert len(results) > 0, "No text detected by OCR"

    all_text = " ".join([r["text"] for r in results]).lower()
    print(f"\nTotal lines detected: {len(results)}")
    print(f"Aggregated detected text: {all_text}")

    # Check for expected tokens from sample_package.png
    assert "mrp" in all_text, "Expected 'MRP' in detected text"
    assert "50" in all_text, "Expected '50' in detected text"

    for r in results:
        assert "text" in r
        assert "confidence" in r
        assert "box" in r
        box = r["box"]
        assert all(k in box for k in ("x", "y", "width", "height"))
        assert box["width"] > 0
        assert box["height"] > 0
        print(f"  [CONF {r['confidence']:.2f}] (x={box['x']}, y={box['y']}, w={box['width']}, h={box['height']}): {r['text']}")

    print("\n>>> ALL OCR PIPELINE TESTS PASSED! <<<")


if __name__ == "__main__":
    test_sample_image()
