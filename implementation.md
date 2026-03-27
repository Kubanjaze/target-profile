# Phase 99 — Full Target Profile: ChEMBL + UniProt

## Version: 1.1 (Final as-built)

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
- [x] `--help` works
- [x] ChEMBL fetch succeeds
- [x] UniProt fetch succeeds
- [x] Output JSON is well-formed and contains both sources
- [x] Console prints summary

## Results
- Target: **GTPase KRas** (SINGLE PROTEIN, Homo sapiens)
- ChEMBL: 16,720 total bioactivities for CHEMBL2189121
- UniProt: KRAS gene, 189 aa, function annotation retrieved
- Unified target_profile.json saved with both ChEMBL and UniProt data

## Key Findings
- KRAS is a heavily studied target with ~17K bioactivities in ChEMBL
- Both APIs return rich structured data — ChEMBL for pharmacology, UniProt for biology
- No API keys needed — fully open access

## Deviations
- None

## Risks
- External API availability — both are stable public APIs (saw one transient 500 from ChEMBL, retry succeeded)
- Rate limiting unlikely for single requests
