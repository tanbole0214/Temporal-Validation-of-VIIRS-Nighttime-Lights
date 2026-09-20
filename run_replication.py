"""Offline statistical replay of the frozen IJDE analysis."""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STAGES = [
    "temporal_extension_2013_2021/code/run_extended_forward_validation.py",
    "temporal_extension_2013_2021/code/run_extended_geography_hotspots.py",
    *[f"round4_ijde_identification_closure/code/{s}" for s in (
        "01_reproduction.py", "02_conditional_incremental.py", "03_raw_error_geography.py",
        "04_spatial_hac.py", "05_hotspot_reference.py", "06_model_form.py",
        "07_AR_benchmark.py", "08_stress_domain.py", "09_finalize.py",
    )],
    "round10b_ijde/branch_b/analysis.py",
    "round10b_ijde/branch_b/make_figures.py",
    "round14_ijde/code/run_round14_analysis.py",
]


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true", help="verify immutable archive inputs and existing outputs")
    g.add_argument("--full", action="store_true", help="run all offline statistical stages, then compare outputs")
    args = p.parse_args()
    from verify_package import check_integrity, check_results
    check_integrity(ROOT)
    if args.full:
        env = os.environ.copy()
        env["MPLBACKEND"] = "Agg"
        for rel in STAGES:
            print(f"RUN {rel}", flush=True)
            run = subprocess.run([sys.executable, str(ROOT / rel)], cwd=ROOT, env=env, check=False)
            if run.returncode:
                raise SystemExit(f"STOP: {rel} exited {run.returncode}; later stages were not run")
    check_results(ROOT)


if __name__ == "__main__":
    main()
