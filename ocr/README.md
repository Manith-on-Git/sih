# Optical Character Recognition (OCR) Module

## Purpose
This module ingests preprocessed packaging images and performs text detection, bounding box extraction, and text recognition across English and multi-lingual text printed on commodity labels.

## Planned Responsibilities
- **Text Detection**: Identify spatial bounding boxes for all printed words, numbers, and symbols.
- **Text Recognition**: Transcribe text within bounding boxes into unicode strings with confidence scores.
- **Spatial Metadata Extraction**: Keep track of bounding box coordinates `[x_min, y_min, x_max, y_max]` and font height estimates (critical for Legal Metrology minimum font height verification).
- **Multi-language Support**: Support for English and Indian regional languages where required.

## Technologies
- PaddleOCR (`paddleocr`, `paddlepaddle`)
- Fallback/Secondary: Tesseract (`pytesseract`) if needed

## Status
- **Phase 1**: Placeholder created.
- **Phase 2 Implementation**: OCR pipeline wrapper returning structured tokens and spatial bounding boxes.
