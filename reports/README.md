# Reports Generation Module

## Purpose
This module generates standardized, downloadable inspection reports (PDF format) documenting the compliance status of analyzed packaged commodities.

## Planned Contents of Inspection Report
1. **Header & Metadata**:
   - Inspection ID, timestamp, and packaging commodity identifier.
   - Overall Compliance Verdict (Compliant / Non-Compliant / Flagged for Manual Review).
   - Overall Compliance Score (0-100%).
2. **Visual Evidence**:
   - Annotated commodity label image showing detected bounding boxes with color-coded status (Green = Compliant declaration, Red = Violation / Missing).
3. **Findings Table**:
   - Mandatory field name.
   - Observed value on packaging.
   - Legal Metrology statutory rule reference.
   - Compliance status and remediation note for non-compliance.
4. **Official Disclaimer**:
   - Clear disclaimer regarding automated AI-assisted scanning.

## Technologies
- ReportLab (`reportlab`) or WeasyPrint for PDF generation.

## Status
- **Phase 1**: Placeholder created.
- **Phase 4 Implementation**: PDF template and report generation service.
