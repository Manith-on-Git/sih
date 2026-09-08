"""
Image preprocessing module for the Compliance Scanner.
Enhances packaging label images to improve OCR accuracy using OpenCV.
"""

from pathlib import Path
from typing import Union
import cv2
import numpy as np


def load_image(image_path: Union[str, Path]) -> np.ndarray:
    """
    Safely load an image from disk in a Windows-compatible manner,
    handling spaces, unicode characters, and long paths.
    """
    path = Path(image_path).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Image not found at path: {path}")

    # Use numpy.fromfile + cv2.imdecode to avoid Windows path encoding bugs with cv2.imread
    img_array = np.fromfile(str(path), dtype=np.uint8)
    image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    if image is None:
        raise ValueError(f"Failed to decode image from path: {path}")

    return image


def enhance_contrast_clahe(image: np.ndarray, clip_limit: float = 2.0, tile_grid_size: tuple = (8, 8)) -> np.ndarray:
    """
    Apply Contrast Limited Adaptive Histogram Equalization (CLAHE) on the L-channel (LAB space)
    to suppress glare on glossy packaging and boost text readability without washing out colors.
    """
    if len(image.shape) == 2:  # Grayscale
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
        return clahe.apply(image)

    # Convert to LAB color space
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l_channel, a_channel, b_channel = cv2.split(lab)

    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    cl = clahe.apply(l_channel)

    # Merge channels and convert back to BGR
    merged = cv2.merge((cl, a_channel, b_channel))
    return cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)


def denoise_image(image: np.ndarray) -> np.ndarray:
    """
    Apply a fast bilateral filter to smooth packaging surface noise/halftone print patterns
    while strictly preserving sharp text edges.
    """
    return cv2.bilateralFilter(image, d=5, sigmaColor=50, sigmaSpace=50)


def preprocess_for_ocr(image_source: Union[str, Path, np.ndarray]) -> np.ndarray:
    """
    Full preprocessing pipeline for packaging commodity images before OCR:
    1. Safe loading (if path provided)
    2. Subtle noise smoothing (preserving edge boundaries)
    3. Adaptive contrast enhancement via CLAHE (mitigates glare on plastic/foil wrappers)
    
    Returns preprocessed BGR image array ready for PaddleOCR inference.
    """
    if isinstance(image_source, (str, Path)):
        img = load_image(image_source)
    elif isinstance(image_source, np.ndarray):
        img = image_source.copy()
    else:
        raise TypeError("image_source must be a file path or numpy.ndarray")

    # Step 1: Denoise packaging surface texture
    denoised = denoise_image(img)

    # Step 2: Enhance contrast with CLAHE
    enhanced = enhance_contrast_clahe(denoised)

    return enhanced
