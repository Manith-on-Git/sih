# Field Extraction Module

## Purpose
This module transforms unstructured OCR tokens and spatial bounding boxes into standardized, structured fields matching the mandatory declarations under the Legal Metrology (Packaged Commodities) Rules, 2011.

## Mandatory Declarations to Extract
1. **MRP (Maximum Retail Price)**
   - Amount in INR
   - Requirement of "inclusive of all taxes"
   - Unit Sale Price (USP) where applicable
2. **Net Quantity**
   - Numeric quantity and unit of measurement (e.g., g, kg, ml, l, m, number)
   - Font height and prominence measurements
3. **Name & Complete Address**
   - Manufacturer, Packer, or Importer identification
4. **Date / Month / Year**
   - Month and Year of manufacture, packing, or import (and expiry / best before where applicable)
5. **Country of Origin**
   - Mandatory declaration of origin country (especially for imported goods)
6. **Consumer Care Details**
   - Contact person / office name, complete postal address, telephone/toll-free number, and email address

## Extraction Strategy
- Regular Expression (regex) patterns tailored to packaging norms.
- Spatial-aware keyword-value heuristic association (pairing key headers like "Mfg Date" with proximate dates).
- Entity recognition and validation using Pydantic schemas.

## Status
- **Phase 1**: Placeholder created.
- **Phase 2 Implementation**: Field parsers and schema definitions.
