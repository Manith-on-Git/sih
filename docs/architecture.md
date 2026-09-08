# SIH26034 System Architecture & Data Pipeline

## 1. System Overview
The **AI-Based Packaged Commodity Compliance Scanner** is designed to audit consumer packaged goods against the statutory requirements of the **Legal Metrology (Packaged Commodities) Rules, 2011**.

```
+--------------------------------------------------------------------------------+
|                                 USER CLIENT                                    |
|   - Web Browser (Vanilla HTML5 / CSS3 / JavaScript)                            |
|   - File selection & live client-side preview                                  |
|   - Asynchronous multipart/form-data upload to Flask REST API                  |
+---------------------------------------+----------------------------------------+
                                        | HTTP POST /api/upload
                                        v
+--------------------------------------------------------------------------------+
|                              FLASK BACKEND                                     |
|   - Validates file type and size constraints                                   |
|   - Safely saves image to backend/uploads/                                     |
|   - Serves static assets and provides REST endpoints                           |
+---------------------------------------+----------------------------------------+
                                        | (Pipeline Execution)
                                        v
+--------------------------------------------------------------------------------+
|                        STAGE 1: COMPUTER VISION PREPROCESSING                  |
|   - Glare suppression & ambient reflection normalization                       |
|   - Deskewing and perspective distortion rectification                         |
|   - Contrast optimization & ROI extraction (Principal Display Panel)           |
+---------------------------------------+----------------------------------------+
                                        | Preprocessed Image + ROI
                                        v
+--------------------------------------------------------------------------------+
|                        STAGE 2: OPTICAL CHARACTER RECOGNITION                  |
|   - Text detection: spatial bounding boxes [xmin, ymin, xmax, ymax]            |
|   - Text recognition: text transcription + confidence scores                   |
|   - Estimated font height calculation                                          |
+---------------------------------------+----------------------------------------+
                                        | Bounding Boxes + Text Tokens
                                        v
+--------------------------------------------------------------------------------+
|                        STAGE 3: STRUCTURED FIELD EXTRACTION                    |
|   - Parsing key packaging declarations using pattern matching & heuristics:    |
|       * Maximum Retail Price (MRP)                                             |
|       * Net Quantity & standard measurement units                              |
|       * Manufacturer / Packer / Importer name & postal address                 |
|       * Month and Year of manufacture / packing / import                       |
|       * Country of Origin                                                      |
|       * Consumer Care details (name, address, telephone, email)                |
+---------------------------------------+----------------------------------------+
                                        | Normalized Declaration Object
                                        v
+--------------------------------------------------------------------------------+
|                   STAGE 4: LEGAL METROLOGY RULE ENGINE                         |
|   - Evaluates mandatory requirements against strictly verified official rules  |
|   - Evaluates unit compliance, font height compliance, completeness            |
|   - Generates violation list with statutory citations                          |
|   - Computes weighted compliance score (0 - 100%)                              |
+-------------------+------------------------------------+-----------------------+
                    |                                    |
                    v                                    v
+-----------------------------------+    +---------------------------------------+
|    STAGE 5: AUDIT PERSISTENCE     |    |    STAGE 6: INSPECTION REPORT (PDF)   |
|    - SQLite local database        |    |    - Summary scorecard                |
|    - Scan session history         |    |    - Annotated visual evidence        |
|    - Violation logging            |    |    - Statutory violation findings      |
+-----------------------------------+    +---------------------------------------+
```

## 2. Technology Stack
- **Frontend**: HTML5, CSS3, Modern Vanilla JavaScript (ES6+ `fetch`, `FileReader`, `FormData`).
- **Backend API**: Python 3.11+, Flask.
- **Computer Vision**: OpenCV (`opencv-python`), NumPy.
- **OCR Engine**: PaddleOCR (`paddleocr`).
- **Database**: SQLite3.
- **Reporting**: Python PDF Generation (`reportlab`).
