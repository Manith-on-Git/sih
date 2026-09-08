# AI-Based Packaged Commodity Compliance Scanner (SIH26034)

An AI-assisted compliance verification system for Smart India Hackathon 2026. This system analyzes packaged commodity labels and checks whether they contain the mandatory declarations required under the **Legal Metrology (Packaged Commodities) Rules, 2011**.

---

## 1. Project Purpose

Packaged commodities sold in India must display statutory declarations (such as Maximum Retail Price inclusive of all taxes, Net Quantity, Manufacturer/Packer/Importer details, Month and Year of manufacture, Country of Origin, and Consumer Care contacts) to safeguard consumer rights and maintain trade transparency.

This project provides an automated, AI-assisted verification pipeline that:
1. Receives an image of a packaged commodity label.
2. Enhances the image via computer vision (glare reduction, deskewing).
3. Transcribes text and spatial bounding boxes via OCR (PaddleOCR).
4. Extracts structured declaration fields.
5. Verifies findings against official Legal Metrology (Packaged Commodities) Rules, 2011.
6. Detects violations, computes a compliance score, and produces an inspection audit report (PDF).

> **Important Legal Standard:**
> All rules and citations in this project are strictly mapped to official Government of India gazette notifications. Unverified rules are explicitly marked as `TODO: TO_BE_VERIFIED` to eliminate hallucinated statutory claims.

---

## 2. System Architecture

```
Package Image 
      │
      ▼
Frontend UI (HTML / CSS / JavaScript)
      │  (HTTP POST /api/upload)
      ▼
Flask Backend Server (backend/app.py)
      │  (Stores uploaded image in backend/uploads/)
      ├─────────────────────────────────────────────────────────────┐
      ▼ (Subsequent Phases)                                         ▼ (Subsequent Phases)
computer_vision/ (OpenCV Preprocessing)                       database/ (SQLite Audit Logs)
      │
      ▼
ocr/ (PaddleOCR Text Detection & Recognition)
      │
      ▼
field_extraction/ (Structured Mandatory Field Extraction)
      │
      ▼
rule_engine/ (Legal Metrology Rules, 2011 Verification Engine)
      │
      ▼
reports/ (Inspection Report & PDF Generator)
```

---

## 3. Project Folder Structure

```
SIH_Compliance_scanner/
│
├── frontend/                     # Web User Interface
│   ├── index.html                # Main UI with title, upload dropzone, preview, scan button
│   ├── style.css                 # Clean, responsive styling (no heavy UI frameworks)
│   └── app.js                    # Client-side file preview and async upload logic
│
├── backend/                      # Python Flask Backend
│   ├── app.py                    # Server entry point, static file serving, and REST API
│   ├── config.py                 # Server, file size, and upload configurations
│   ├── uploads/                  # Safe local storage for uploaded package images
│   └── utils/
│       ├── __init__.py
│       └── file_handler.py       # File extension validation and secure name generator
│
├── computer_vision/              # Image enhancement, glare removal, deskewing (OpenCV)
│   ├── __init__.py
│   └── README.md
│
├── ocr/                          # Optical Character Recognition (PaddleOCR)
│   ├── __init__.py
│   └── README.md
│
├── field_extraction/             # Regex & heuristic parsing of mandatory fields
│   ├── __init__.py
│   └── README.md
│
├── rule_engine/                  # Legal Metrology statutory compliance evaluation
│   ├── __init__.py
│   └── README.md
│
├── reports/                      # Inspection scorecard & PDF report generation
│   ├── __init__.py
│   └── README.md
│
├── database/                     # SQLite audit logging and scan history
│   ├── __init__.py
│   └── README.md
│
├── test_data/                    # Sample packaged commodity images for testing
│   ├── README.md
│   └── .gitkeep
│
├── docs/                         # Architecture details and statutory reference trackers
│   ├── architecture.md           # Pipeline architecture and data flow
│   └── legal_metrology_notes.md  # Official Legal Metrology clause mapping
│
├── requirements.txt              # Project dependencies
├── .gitignore                    # Git ignore file for Python and upload artifacts
└── README.md                     # Project documentation (this file)
```

---

## 4. Getting Started (Windows Setup Guide)

### Prerequisites
- **Python 3.10+** (Tested on Python 3.11)
- Modern web browser (Chrome, Edge, Firefox)

### Step 1: Clone or Navigate to the Project Folder
Open PowerShell or Command Prompt:
```powershell
cd C:\Users\Priya\Documents\SIH_Compliance_scanner
```

### Step 2: (Optional but Recommended) Create a Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\activate
```

### Step 3: Install Dependencies
```powershell
python -m pip install -r requirements.txt
```

---

## 5. Running the Application

### Start the Flask Server
Run the following command from the project root:
```powershell
python backend/app.py
```

You will see output similar to:
```
==================================================
 SIH26034 - Packaged Commodity Compliance Scanner 
 Server running at: http://127.0.0.1:5000
 Upload directory:  ...\backend\uploads
==================================================
 * Serving Flask app 'backend.app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### Access the Web Interface
Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 6. Testing the Upload & OCR Endpoints

### Via Web Interface:
1. Open `http://127.0.0.1:5000` in your browser.
2. Click the upload area or drag and drop a packaged commodity image (e.g. `test_data/sample_package.png`).
3. An instant preview will be displayed.
4. Click **Run OCR Scan** (or **Upload Only** for Phase 1 behavior).
5. The interface will process the image through OpenCV and PaddleOCR, displaying:
   - Total lines detected and average confidence percentage.
   - Extracted text elements with color-coded confidence badges.
   - Bounding box coordinates `(X, Y, W, H)` for spatial localization.
   - Collapsible formatted raw JSON viewer.

### Via PowerShell / curl:

#### Test Image Upload:
```powershell
curl -X POST -F "image=@test_data/sample_package.png" http://127.0.0.1:5000/api/upload
```

#### Test OCR Pipeline:
```powershell
curl -X POST -F "image=@test_data/sample_package.png" http://127.0.0.1:5000/api/ocr
```

Expected JSON Response:
```json
{
  "status": "success",
  "image": "pkg_20260909_003329_9b53467b.png",
  "total_lines": 3,
  "results": [
    {
      "text": "SIH26034 Test Commodity Label",
      "confidence": 0.9995,
      "box": {
        "x": 0,
        "y": 6,
        "width": 161,
        "height": 15
      }
    },
    {
      "text": "MRP Rs. 50.00 (incl. of all taxes)",
      "confidence": 0.9763,
      "box": {
        "x": 0,
        "y": 47,
        "width": 150,
        "height": 13
      }
    },
    {
      "text": "NetQty: 500 g",
      "confidence": 0.9859,
      "box": {
        "x": 0,
        "y": 86,
        "width": 73,
        "height": 18
      }
    }
  ]
}
```

---

## 7. Current Project Status
- **Phase 1 (Complete)**: Clean modular architecture, Flask REST backend, safe upload API, client interface, and documentation.
- **Phase 2 (Complete)**: OpenCV image preprocessing (CLAHE glare reduction, bilateral noise smoothing), PaddleOCR text detection & recognition, structured OCR output, and interactive frontend results viewer.
- **Phase 3 (Upcoming)**: Structured field extraction (MRP, Net Qty, Dates, Manufacturer, Country of Origin, Consumer Care) and Legal Metrology Rule Engine.
- **Phase 4 (Upcoming)**: Evidence highlighting, scoring, SQLite persistence, and PDF report export.

