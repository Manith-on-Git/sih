# Computer Vision Module (Image Preprocessing)

## Purpose
This module handles all image enhancement, noise filtering, glare removal, orientation correction, and label region cropping before passing package images to the OCR engine.

## Planned Responsibilities
- **Glare & Reflection Removal**: Packaging materials often have glossy surfaces that create bright glare spots.
- **Orientation & Deskewing**: Automatically detect label orientation and straighten skewed text.
- **Perspective Correction**: Rectify angled or curved surfaces (e.g., cylindrical bottles, bent pouches).
- **Contrast & Binarization**: Adaptive thresholding to enhance legibility of fine-print mandatory declarations.
- **Region of Interest (ROI) Detection**: Detect where declaration panels (Principal Display Panel / Information Panel) reside.

## Technologies
- OpenCV (`opencv-python`)
- NumPy

## Status
- **Phase 1**: Placeholder created.
- **Phase 2 Implementation**: Preprocessing functions will be implemented and integrated with the pipeline.
