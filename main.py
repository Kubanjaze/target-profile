"""Phase 99 — Full Target Profile: ChEMBL + UniProt.

Fetches KRAS target data from ChEMBL and UniProt, merges into a unified
target_profile.json.
"""
import sys
import os

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

import argparse
import json
from pathlib import Path

import requests
import pandas as pd


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Fetch target profile from ChEMBL + UniProt",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("--chembl-id", default="CHEMBL2189121", help="ChEMBL target ID")
    p.add_argument("--uniprot-id", default="P01116", help="UniProt accession")
    p.add_argument("--output", default="output", help="Output directory")
    return p.parse_args()


def fetch_chembl_target(chembl_id: str) -> dict:
    """Fetch target info from ChEMBL REST API."""
    url = f"https://www.ebi.ac.uk/chembl/api/data/target/{chembl_id}.json"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    return {
        "chembl_id": data.get("target_chembl_id"),
        "pref_name": data.get("pref_name"),
        "target_type": data.get("target_type"),
        "organism": data.get("organism"),
        "tax_id": data.get("tax_id"),
        "species_group_flag": data.get("species_group_flag"),
        "cross_references": data.get("cross_references", []),
        "target_components": [
            {
                "component_id": c.get("component_id"),
                "component_type": c.get("component_type"),
                "accession": c.get("accession"),
                "description": c.get("component_description"),
            }
            for c in data.get("target_components", [])
        ],
    }


def fetch_chembl_activities(chembl_id: str) -> dict:
    """Fetch activity summary for a target from ChEMBL."""
    url = (
        f"https://www.ebi.ac.uk/chembl/api/data/activity.json"
        f"?target_chembl_id={chembl_id}&limit=0"
    )
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    total = data.get("page_meta", {}).get("total_count", 0)
    return {"total_activities": total}


def fetch_uniprot(uniprot_id: str) -> dict:
    """Fetch protein info from UniProt REST API."""
    url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.json"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    # Extract key fields
    gene_names = []
    for g in data.get("genes", []):
        if "geneName" in g:
            gene_names.append(g["geneName"].get("value", ""))

    function_text = ""
    subcellular = []
    for comment in data.get("comments", []):
        if comment.get("commentType") == "FUNCTION":
            texts = comment.get("texts", [])
            if texts:
                function_text = texts[0].get("value", "")
        if comment.get("commentType") == "SUBCELLULAR LOCATION":
            for sl in comment.get("subcellularLocations", []):
                loc = sl.get("location", {})
                if "value" in loc:
                    subcellular.append(loc["value"])

    seq = data.get("sequence", {})

    return {
        "uniprot_id": data.get("primaryAccession"),
        "entry_name": data.get("uniProtkbId"),
        "gene_names": gene_names,
        "protein_name": data.get("proteinDescription", {}).get(
            "recommendedName", {}
        ).get("fullName", {}).get("value", ""),
        "organism": data.get("organism", {}).get("scientificName", ""),
        "function": function_text,
        "subcellular_location": subcellular,
        "sequence_length": seq.get("length"),
        "sequence_mass": seq.get("molWeight"),
    }


def main() -> None:
    args = parse_args()
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Phase 99 — Full Target Profile")
    print(f"ChEMBL: {args.chembl_id} | UniProt: {args.uniprot_id}\n")

    # 1. ChEMBL target
    print("[1] Fetching ChEMBL target info...")
    chembl_target = fetch_chembl_target(args.chembl_id)
    print(f"  Name: {chembl_target['pref_name']}")
    print(f"  Type: {chembl_target['target_type']}")
    print(f"  Organism: {chembl_target['organism']}")

    # 2. ChEMBL activities
    print("\n[2] Fetching ChEMBL activity summary...")
    activities = fetch_chembl_activities(args.chembl_id)
    print(f"  Total activities: {activities['total_activities']}")

    # 3. UniProt
    print("\n[3] Fetching UniProt protein info...")
    uniprot = fetch_uniprot(args.uniprot_id)
    print(f"  Protein: {uniprot['protein_name']}")
    print(f"  Gene: {', '.join(uniprot['gene_names'])}")
    print(f"  Sequence length: {uniprot['sequence_length']} aa")
    print(f"  Function: {uniprot['function'][:120]}...")

    # 4. Merge
    profile = {
        "phase": 99,
        "description": "Unified target profile from ChEMBL + UniProt",
        "chembl": {**chembl_target, **activities},
        "uniprot": uniprot,
    }

    profile_path = out_dir / "target_profile.json"
    with open(profile_path, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2, ensure_ascii=False)

    print(f"\n[4] Saved to {profile_path}")
    print("Done.")


if __name__ == "__main__":
    main()
