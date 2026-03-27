# Phase 99 — Full Target Profile: ChEMBL + UniProt

## Version: 1.0 (Plan)

## Goal
Fetch KRAS target data from ChEMBL (CHEMBL2189121) and UniProt (P01116), merge into a unified target_profile.json. Demonstrates programmatic access to public drug discovery databases.

## CLI
```bash
PYTHONUTF8=1 python main.py
PYTHONUTF8=1 python main.py --chembl-id CHEMBL2189121 --uniprot-id P01116
```

## Outputs
- `output/target_profile.json` — unified target profile combining ChEMBL + UniProt data
- Console summary of fetched data

## Logic
1. Fetch target info from ChEMBL REST API (target name, type, organism, cross-references)
2. Fetch bioactivity summary from ChEMBL (count of assays, active compounds)
3. Fetch protein info from UniProt REST API (gene name, function, sequence length, subcellular location)
4. Merge into unified JSON profile
5. Save to output/

## Key Concepts
- ChEMBL REST API for target and bioactivity data
- UniProt REST API for protein annotations
- Data integration from multiple public sources
- No API key required

## Verification Checklist
- [ ] `--help` works
- [ ] ChEMBL fetch succeeds
- [ ] UniProt fetch succeeds
- [ ] Output JSON is well-formed and contains both sources
- [ ] Console prints summary

## Risks
- External API availability — both are stable public APIs
- Rate limiting unlikely for single requests
