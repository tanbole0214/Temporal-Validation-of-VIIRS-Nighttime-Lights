"""Hash and numerical checks; no external data access."""
from __future__ import annotations

import csv
import hashlib
from pathlib import Path

import numpy as np
import pandas as pd


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def check_integrity(root: Path) -> None:
    rows = list(csv.DictReader((root / "PACKAGE_SHA256.csv").open(encoding="utf-8-sig", newline="")))
    failures = []
    checked = 0
    for row in rows:
        if row["mutable_on_full_run"] == "yes":
            continue
        path = root / row["relative_path"]
        if not path.is_file() or sha(path) != row["sha256"]:
            failures.append(row["relative_path"])
        checked += 1
    if failures:
        raise SystemExit(f"Input integrity failed: {failures[:8]}; total={len(failures)}")
    print(f"Immutable file hashes: PASS ({checked} files)")


def check_results(root: Path) -> None:
    refs = sorted((root / "reference_results").rglob("*.csv"))
    failures = []
    compared = 0
    largest = 0.0
    for ref in refs:
        if ref.name == "ROUND4_00_INPUT_AND_PROVENANCE_AUDIT.csv":
            # Portable archive deliberately omits private prompt/old Word inputs.
            continue
        current = root / ref.relative_to(root / "reference_results")
        if not current.is_file():
            failures.append(f"missing {current.relative_to(root)}")
            continue
        a = pd.read_csv(ref, low_memory=False)
        b = pd.read_csv(current, low_memory=False)
        if list(a.columns) != list(b.columns) or len(a) != len(b):
            failures.append(f"schema/rows {current.relative_to(root)}")
            continue
        num = list(a.select_dtypes(include="number").columns)
        if num:
            av = a[num].to_numpy(dtype=float)
            bv = b[num].to_numpy(dtype=float)
            diff = np.abs(av - bv)
            maxdiff = float(np.nanmax(diff)) if np.any(np.isfinite(diff)) else 0.0
            largest = max(largest, maxdiff)
            if not np.allclose(av, bv, atol=1e-8, rtol=1e-8, equal_nan=True):
                failures.append(f"numeric {current.relative_to(root)} max_diff={maxdiff:g}")
        # Categorical identifiers, products, domains, and statuses must agree;
        # machine-local paths and creation timestamps are deliberately excluded.
        for col in ("product", "benchmark", "target_year", "year", "test_year", "domain", "status", "city_code", "prefecture_id", "moderator"):
            if col in a and col not in num:
                if not a[col].fillna("<NA>").astype(str).equals(b[col].fillna("<NA>").astype(str)):
                    failures.append(f"label {current.relative_to(root)}:{col}")
        compared += 1
    gate = pd.read_csv(root / "round4_ijde_identification_closure/ROUND4_01_REPRODUCTION_GATE.csv")
    nested = pd.read_csv(root / "round4_ijde_identification_closure/ROUND4_02_NESTED_BENCHMARK_LEAKAGE_AUDIT.csv")
    if not gate.status.eq("PASS").all(): failures.append("reproduction gate")
    if "status" in nested and not nested.status.eq("PASS").all(): failures.append("nested leakage gate")
    panel = pd.read_csv(root / "temporal_extension_2013_2021/07_panel/prefecture_panel_2014_2021_extended.csv")
    if len(panel) != 2368 or panel.city_code.nunique() != 296: failures.append("panel universe")
    if failures:
        raise SystemExit("Output comparison failed:\n" + "\n".join(failures[:20]))
    print(f"Frozen output numerical comparison: PASS ({compared} CSV files; max absolute difference {largest:g})")
    print(f"Reproduction and leakage gates: PASS ({len(gate)} gate rows; {len(nested)} nested audit rows)")
