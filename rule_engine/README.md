# Legal Metrology Rule Engine

## Purpose
The Rule Engine evaluates structured fields extracted from packaging labels against the statutory requirements of the **Legal Metrology (Packaged Commodities) Rules, 2011** (and applicable official amendments).

## CRITICAL LEGAL REQUIREMENT
> **DO NOT INVENT RULES OR RULE NUMBERS.**
> All compliance checks in this engine MUST reference verified, official statutory clauses published by the Ministry of Consumer Affairs, Food and Public Distribution (Department of Consumer Affairs), Government of India.
> Any rule or clause whose specific statutory citation is pending verification must be explicitly flagged with `TODO: TO_BE_VERIFIED`.

## Core Verification Areas (To Be Implemented)
1. **Mandatory Declarations Completeness**:
   - Check presence of all mandatory items under Rule 6(1) of the Legal Metrology (Packaged Commodities) Rules, 2011:
     - Name and address of manufacturer/packer/importer
     - Common or generic name of commodity
     - Net quantity (standard units of weight, measure, or number)
     - Month and year of manufacture/packing/import
     - Maximum Retail Price (inclusive of all taxes)
     - Consumer care contact details
     - Country of origin (for imported goods)
2. **Declaration Format & Font Sizing**:
   - Verification of standard units of measurement (e.g., standard symbols: `g`, `kg`, `ml`, `l`, `m`).
   - Font height checks relative to Principal Display Panel (PDP) area as prescribed in the schedules.
3. **Violation Reporting & Evidence**:
   - Output structured violations with statutory clause reference, observed text, expected requirement, and violation severity.
4. **Compliance Scoring**:
   - Objective calculation of label compliance score based on verified requirements.

## Status
- **Phase 1**: Placeholder created. No rules or rule numbers are mocked or hallucinated.
- **Phase 3 Implementation**: Verified statutory rule set implementation.
