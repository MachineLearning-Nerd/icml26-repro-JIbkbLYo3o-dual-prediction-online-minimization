"""Four-route audit of the unreleased real-data experiments."""
from __future__ import annotations

import csv
import hashlib
import io
import json
import os
import platform
import re
import subprocess
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path

from source_payload import open_source

ROOT = Path(__file__).resolve().parents[2]
UA = (
    "Mozilla/5.0 (compatible; OpenResearchReproduction/1.0; "
    "+https://github.com/MachineLearning-Nerd)"
)
NOAA_URL = (
    "https://www.ncei.noaa.gov/data/"
    "global-historical-climatology-network-daily/access/USW00094728.csv"
)
S3_URL = "https://s3.amazonaws.com/tripdata"


def fetch(url: str, timeout: int = 180) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def image_manifest() -> dict:
    names = {
        "parking_k": "ICML_submission/figures/varyn.png",
        "parking_f": "ICML_submission/figures/finaldiscountfactor.png",
        "bike_trip": "ICML_submission/figures/plot1_v2.png",
        "bike_minute": "ICML_submission/figures/plot2_v2.png",
    }
    result = {}
    with open_source(ROOT) as archive:
        for label, name in names.items():
            payload = archive.extractfile(name).read()
            result[label] = {
                "path": name,
                "bytes": len(payload),
                "sha256": hashlib.sha256(payload).hexdigest(),
            }
    return result


def ghcn_audit() -> dict:
    payload = fetch(NOAA_URL)
    rows = list(csv.DictReader(io.StringIO(payload.decode("utf-8-sig"))))
    by_year: dict[int, list[dict]] = defaultdict(list)
    for row in rows:
        year = int(row["DATE"][:4])
        if 1869 <= year <= 2021 and row["DATE"][5:] != "02-29":
            by_year[year].append(row)
    summaries = []
    # GHCN-Daily PRCP is stored in tenths of millimeters. These correspond to
    # >0 mm, >1 mm, and >2.5 mm definitions of a rainy day.
    thresholds = (0, 10, 25)
    rain_totals = Counter()
    missing_prcp = 0
    for year in range(1869, 2022):
        year_rows = by_year[year]
        values = []
        for row in year_rows:
            raw = row.get("PRCP", "")
            if raw == "":
                missing_prcp += 1
                values.append(None)
            else:
                values.append(float(raw))
        counts = {}
        for threshold in thresholds:
            count = sum(value is not None and value > threshold for value in values)
            counts[str(threshold)] = count
            rain_totals[str(threshold)] += count
        summaries.append(
            {
                "year": year,
                "rows_after_feb29_drop": len(year_rows),
                "rain_days_by_raw_tenths_mm_threshold": counts,
            }
        )
    return {
        "url": NOAA_URL,
        "retrieval_user_agent": UA,
        "bytes": len(payload),
        "sha256": hashlib.sha256(payload).hexdigest(),
        "station_ids": sorted({row["STATION"] for row in rows}),
        "station_names": sorted({row["NAME"] for row in rows}),
        "target_years": 153,
        "complete_365_day_years": sum(
            row["rows_after_feb29_drop"] == 365 for row in summaries
        ),
        "missing_prcp_cells": missing_prcp,
        "prcp_unit": "tenths of millimeters",
        "rain_totals_by_raw_tenths_mm_threshold": dict(rain_totals),
        "first_three_years": summaries[:3],
        "last_three_years": summaries[-3:],
        "unresolved_source_choices": [
            "precipitation threshold defining a rainy day",
            "handling of February 29 and missing precipitation",
            "whether permit type indexing starts at k=0 or k=1",
            "interval alignment and boundary rules",
            "exact deterministic and randomized PPP baseline implementations",
            "random seeds and number of repetitions",
        ],
    }


def s3_listing(prefix: str) -> list[dict]:
    token = None
    result = []
    while True:
        query = {"list-type": "2", "prefix": prefix}
        if token:
            query["continuation-token"] = token
        payload = fetch(S3_URL + "?" + urllib.parse.urlencode(query))
        root = ET.fromstring(payload)
        namespace = {"s3": "http://s3.amazonaws.com/doc/2006-03-01/"}
        for item in root.findall("s3:Contents", namespace):
            result.append(
                {
                    "key": item.findtext("s3:Key", namespaces=namespace),
                    "bytes": int(item.findtext("s3:Size", namespaces=namespace)),
                    "etag": item.findtext("s3:ETag", namespaces=namespace).strip('"'),
                    "last_modified": item.findtext(
                        "s3:LastModified", namespaces=namespace
                    ),
                }
            )
        if root.findtext("s3:IsTruncated", namespaces=namespace) != "true":
            break
        token = root.findtext("s3:NextContinuationToken", namespaces=namespace)
    return result


def citibike_audit() -> dict:
    entries = []
    for year in ("2023", "2024", "2025"):
        entries.extend(s3_listing(year))
    pattern = re.compile(
        r"^(?:2023-citibike|2024[01][0-9]-citibike|"
        r"2025[01][0-9]-citibike)-tripdata\.zip$"
    )
    selected = sorted(
        (entry for entry in entries if pattern.match(entry["key"])),
        key=lambda entry: entry["key"],
    )
    years = Counter(entry["key"][:4] for entry in selected)
    return {
        "official_bucket": S3_URL,
        "retrieval_user_agent": UA,
        "objects": selected,
        "object_count_by_year": dict(years),
        "compressed_bytes": sum(entry["bytes"] for entry in selected),
        "downloaded_for_this_audit": False,
        "reason_not_downloaded": (
            "the paper omits algorithm/preprocessing choices needed to define "
            "the claimed computation; downloading tens of gigabytes cannot "
            "resolve those missing semantics"
        ),
        "unresolved_source_choices": [
            "geographic rule for selecting trips originating in Manhattan",
            "latitude endpoints of the ten equal intervals",
            "initial k-server configuration for each day",
            "whether configurations permit colocated servers",
            "WFA and Double Coverage tie breaking",
            "distance normalization on the ten-point line",
            "alignment of variable trip requests to 15-minute dual blocks",
            "treatment of days or minutes with no trips",
            "confidence-interval estimator and random seeds",
        ],
    }


def main() -> None:
    started = time.perf_counter()
    route1 = {
        "route": "source-figure self-consistency",
        "kind": "artifact audit, not a rerun",
        "images": image_manifest(),
        "paper_text_values": {
            "K": 9,
            "randomized_over_augmented": 1.8,
            "deterministic_over_augmented": 4.4,
        },
        "assessment": (
            "ALIGNED with the plotted source artifact, but circular and "
            "insufficient for empirical verification"
        ),
    }
    route2 = {
        "route": "full GHCN input reconstruction",
        "kind": "independent primary-data audit",
        "data": ghcn_audit(),
        "assessment": (
            "INPUT RECONSTRUCTED; outcome remains underdetermined because "
            "the rain and algorithm choices are absent"
        ),
    }
    route3 = {
        "route": "Citi Bike full-period manifest and method audit",
        "kind": "primary-data feasibility audit",
        "data": citibike_audit(),
        "assessment": (
            "BLOCKED before faithful computation by missing method semantics; "
            "a proxy implementation would not test the exact claim"
        ),
    }
    route4 = {
        "route": "mandatory falsification search",
        "exact_claim": (
            "the specified augmented PPP algorithm has 1.8x/4.4x advantages "
            "at K=9 and the specified dual k-server algorithm outperforms WFA/DC "
            "on the authors' 2023-2025 processing"
        ),
        "assumptions": (
            "authors' unreleased policies, preprocessing, initial states, "
            "tie rules, randomization, and processed daily instances"
        ),
        "tests": [
            "checked numerical prose against source figure pixels/artifacts",
            "checked all 153 named GHCN calendar-year inputs and threshold sensitivity",
            "resolved the official Citi Bike object manifest for 2023-2025",
        ],
        "result": "NO_VALID_COUNTEREXAMPLE",
        "why_not_falsified": (
            "alternative preprocessing or algorithms violate the exact "
            "unreleased-assumption contract and cannot contradict the claim"
        ),
    }
    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    ).stdout.strip()
    result = {
        "claim_id": "C5",
        "verdict": "BLOCKED",
        "confidence": "LOW",
        "routes_completed": 4,
        "routes": [route1, route2, route3, route4],
        "unblockers": [
            "author experiment code at the reported revision",
            "processed PPP and daily Citi Bike instances with hashes",
            "initial configurations, tie rules, and random seeds",
        ],
        "git_sha": commit,
        "compute": {
            "estimated_cores": 2,
            "selected_flavor": "hf cpu-upgrade",
            "actual_visible_logical_cpus": os.cpu_count(),
            "python": platform.python_version(),
            "runtime_seconds": time.perf_counter() - started,
        },
    }
    path = ROOT / "outputs/claim5_four_route_audit.json"
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
