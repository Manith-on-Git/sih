# Database Module (SQLite)

## Purpose
This module provides lightweight, zero-configuration local database persistence using SQLite. It stores inspection history, compliance verdicts, extracted declaration data, and audit records.

## Planned Schema Tables
1. `scans`:
   - `id` (INTEGER PRIMARY KEY)
   - `timestamp` (DATETIME)
   - `original_filename` (TEXT)
   - `stored_filename` (TEXT)
   - `overall_score` (REAL)
   - `compliance_status` (TEXT - COMPLIANT, NON_COMPLIANT, REVIEW)
   - `report_path` (TEXT)
2. `extracted_fields`:
   - `id` (INTEGER PRIMARY KEY)
   - `scan_id` (FOREIGN KEY)
   - `field_name` (TEXT)
   - `extracted_value` (TEXT)
   - `confidence` (REAL)
   - `bbox_json` (TEXT)
3. `violations`:
   - `id` (INTEGER PRIMARY KEY)
   - `scan_id` (FOREIGN KEY)
   - `field_name` (TEXT)
   - `rule_reference` (TEXT)
   - `violation_description` (TEXT)
   - `severity` (TEXT)

## Status
- **Phase 1**: Placeholder created.
- **Phase 4 Implementation**: SQLite connection manager and repository layer.
