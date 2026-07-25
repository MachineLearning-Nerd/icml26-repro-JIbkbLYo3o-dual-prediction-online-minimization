"""Fail-closed evaluator-visible and historical-preservation release audit."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[2]
CANDIDATE = ROOT / "candidate" if (ROOT / "candidate").is_dir() else ROOT
STARTUP = ROOT / ".openresearch" / "artifacts" / "startup"
if not STARTUP.is_dir():
    STARTUP = CANDIDATE / "evidence" / "startup"
JUDGED_MANIFEST = STARTUP / "judged_space_manifest.json"
OUTPUT = ROOT / "outputs" / "release_candidate_verification.json"

EDITABLE_HISTORICAL_PATHS = {"README.md", "logbook.json", "pages/index.md"}
RELEASE_ALLOWLIST = CANDIDATE / "release" / "upload-allowlist.txt"
RELEASE_MANIFEST = CANDIDATE / "release" / "sha256-manifest.json"
SELF_EXCLUDED = "release/sha256-manifest.json"
TEXT_SUFFIXES = {
    ".b64",
    ".css",
    ".gitattributes",
    ".html",
    ".js",
    ".json",
    ".lock",
    ".md",
    ".py",
    ".python-version",
    ".svg",
    ".toml",
    ".txt",
}
MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
SECRET_PATTERNS = {
    "Hugging Face token": re.compile(rb"\bhf_[A-Za-z0-9]{20,}\b"),
    "GitHub token": re.compile(rb"\bgh[opsu]_[A-Za-z0-9]{20,}\b"),
    "AWS access key": re.compile(rb"\bAKIA[0-9A-Z]{16}\b"),
    "private key": re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_text_path(path: Path) -> bool:
    return path.suffix.lower() in TEXT_SUFFIXES or path.name in {
        ".gitattributes",
        ".python-version",
    }


def relative_files() -> dict[str, Path]:
    return {
        path.relative_to(CANDIDATE).as_posix(): path
        for path in CANDIDATE.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    }


def logbook_files(node: dict) -> list[str]:
    found = [node["file"]]
    for child in node.get("children", []):
        found.extend(logbook_files(child))
    return found


def local_target(source: Path, raw_target: str) -> Path | None:
    target = raw_target.strip().split()[0].strip("<>")
    if (
        target.startswith(("http://", "https://", "mailto:", "data:"))
        or target.startswith("#")
    ):
        return None
    target = unquote(target.split("#", 1)[0].split("?", 1)[0])
    if not target:
        return None
    resolved = (
        CANDIDATE / target.lstrip("/")
        if target.startswith("/")
        else source.parent / target
    ).resolve()
    resolved.relative_to(CANDIDATE.resolve())
    return resolved


def traverse_readme() -> tuple[set[str], list[str]]:
    queue = [CANDIDATE / "README.md"]
    visited: set[Path] = set()
    broken: list[str] = []
    while queue:
        source = queue.pop(0)
        if source in visited:
            continue
        visited.add(source)
        if not is_text_path(source):
            continue
        text = source.read_text(errors="strict")
        for match in MARKDOWN_LINK.finditer(text):
            target = local_target(source, match.group(1))
            if target is None:
                continue
            if not target.is_file():
                broken.append(
                    f"{source.relative_to(CANDIDATE)} -> "
                    f"{target.relative_to(CANDIDATE)}"
                )
                continue
            if target not in visited:
                queue.append(target)
    return {
        path.relative_to(CANDIDATE).as_posix() for path in visited
    }, broken


def expected_upload_paths(
    files: dict[str, Path], judged_files: dict[str, str]
) -> list[str]:
    changed = []
    for relative, path in files.items():
        if relative == SELF_EXCLUDED:
            changed.append(relative)
        elif relative not in judged_files or sha256(path) != judged_files[relative]:
            changed.append(relative)
    for release_path in ("release/upload-allowlist.txt", SELF_EXCLUDED):
        if release_path not in changed:
            changed.append(release_path)
    return sorted(changed)


def write_release_files(judged_files: dict[str, str]) -> None:
    RELEASE_ALLOWLIST.parent.mkdir(parents=True, exist_ok=True)
    RELEASE_ALLOWLIST.touch()
    RELEASE_MANIFEST.touch()
    files = relative_files()
    allowlist = expected_upload_paths(files, judged_files)
    RELEASE_ALLOWLIST.write_text("\n".join(allowlist) + "\n")
    files = relative_files()
    hashes = {
        relative: sha256(files[relative])
        for relative in allowlist
        if relative != SELF_EXCLUDED
    }
    tree_digest = hashlib.sha256(
        "".join(f"{path}\0{digest}\n" for path, digest in sorted(hashes.items())).encode()
    ).hexdigest()
    payload = {
        "space_id": "DineshAI/JIbkbLYo3o",
        "judged_revision": "ca024e6adeaf755dd21a0b28b642d5a85d6df733",
        "upload_mode": "text-only Hugging Face API",
        "self_excluded_path": SELF_EXCLUDED,
        "payload_tree_sha256": tree_digest,
        "files": hashes,
    }
    RELEASE_MANIFEST.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def audit() -> dict:
    judged = json.loads(JUDGED_MANIFEST.read_text())
    assert judged["space_id"] == "DineshAI/JIbkbLYo3o"
    assert judged["revision"] == "ca024e6adeaf755dd21a0b28b642d5a85d6df733"
    judged_files = judged["files"]
    files = relative_files()

    missing_historical = sorted(set(judged_files) - set(files))
    assert not missing_historical, missing_historical
    changed_protected = sorted(
        relative
        for relative, expected_hash in judged_files.items()
        if relative not in EDITABLE_HISTORICAL_PATHS
        and sha256(files[relative]) != expected_hash
    )
    assert not changed_protected, changed_protected

    logbook = json.loads(files["logbook.json"].read_text())
    assert logbook["space_id"] == "DineshAI/JIbkbLYo3o"
    root = logbook["root"]
    children = root["children"]
    assert [child["slug"] for child in children[:7]] == [
        "current-summary",
        "current-claim-c1",
        "current-claim-c2",
        "current-claim-c3",
        "current-claim-c4",
        "current-claim-c5",
        "current-claim-c6",
    ]
    historical = next(
        child for child in children if child["slug"] == "historical-rejected-baseline"
    )
    assert historical["title"] == "Historical rejected baseline"
    referenced_pages = logbook_files(root)
    assert all((CANDIDATE / page).is_file() for page in referenced_pages)

    reachable, broken_links = traverse_readme()
    assert not broken_links, broken_links
    required_pages = {
        f"pages/current-claim-c{claim}/page.md" for claim in range(1, 7)
    }
    required_pages.update(
        {
            "pages/current-summary/page.md",
            "pages/release-audit/page.md",
            "pages/overview/page.md",
            "report.md",
            "notebooks/dual_prediction_reproduction.py",
            "pyproject.toml",
            "uv.lock",
            "repro/src/run_publication_gate.py",
        }
    )
    assert required_pages <= reachable, sorted(required_pages - reachable)

    run_links = {
        1: "evidence/runs/C1-C3-C6-theory.json",
        2: "evidence/runs/C2-MTS-proof.json",
        3: "evidence/runs/C1-C3-C6-theory.json",
        4: "evidence/runs/C4-caching.json",
        5: "evidence/runs/C5-real-data-audit.json",
        6: "evidence/runs/C1-C3-C6-theory.json",
    }
    code_links = {
        1: (
            "verify_remaining_theory.py",
            "check_remaining_theory_independent.py",
            "run_remaining_theory_negative_controls.py",
        ),
        2: (
            "verify_claim2_proof.py",
            "check_claim2_independent.py",
            "run_claim2_negative_control.py",
        ),
        3: (
            "verify_remaining_theory.py",
            "check_remaining_theory_independent.py",
            "run_remaining_theory_negative_controls.py",
        ),
        4: (
            "verify_claim4_caching.py",
            "check_claim4_independent.py",
            "run_claim4_negative_controls.py",
        ),
        5: (
            "audit_claim5_real_data.py",
            "check_claim5_independent.py",
            "run_claim5_negative_control.py",
        ),
        6: (
            "verify_remaining_theory.py",
            "check_remaining_theory_independent.py",
            "run_remaining_theory_negative_controls.py",
        ),
    }
    for claim in range(1, 7):
        page_path = CANDIDATE / f"pages/current-claim-c{claim}/page.md"
        text = page_path.read_text()
        lower = text.lower()
        for token in (
            "verdict",
            "source",
            "command",
            "seed",
            "runtime",
            "limitation",
            "control",
        ):
            assert token in lower, (claim, token)
        linked = {
            local_target(page_path, match.group(1))
            for match in MARKDOWN_LINK.finditer(text)
        }
        linked.discard(None)
        required = {
            CANDIDATE / f"evidence/C{claim}/claim_contract.json",
            CANDIDATE / f"evidence/C{claim}/source_audit.md",
            CANDIDATE / f"evidence/C{claim}/method.md",
            CANDIDATE / f"evidence/C{claim}/EVAL.md",
            CANDIDATE / run_links[claim],
        }
        required.update(CANDIDATE / "repro/src" / name for name in code_links[claim])
        assert required <= linked, (
            claim,
            sorted(path.relative_to(CANDIDATE).as_posix() for path in required - linked),
        )
        assert {
            path.relative_to(CANDIDATE).as_posix() for path in required
        } <= reachable

    c2 = json.loads(files["evidence/runs/C2-MTS-proof.json"].read_text())
    theory = json.loads(files["evidence/runs/C1-C3-C6-theory.json"].read_text())
    c4 = json.loads(files["evidence/runs/C4-caching.json"].read_text())
    c5 = json.loads(files["evidence/runs/C5-real-data-audit.json"].read_text())
    assert c2["verdict"] == "VERIFIED"
    assert all(theory["claims"][claim]["verdict"] == "VERIFIED" for claim in ("C1", "C3", "C6"))
    assert theory["independent_checker"] == "PASS"
    assert theory["negative_controls"] == "REJECTED_AS_INTENDED"
    assert c4["verdict"] == "VERIFIED"
    assert c4["independent_checker"] == "PASS"
    assert c4["minimum_ratio_over_k_last_three"] > 0.9
    assert c5["verdict"] == "BLOCKED"
    assert c5["confidence"] == "LOW"
    assert c5["routes_completed"] == 4
    assert c5["falsification_result"] == "NO_VALID_COUNTEREXAMPLE"

    source_payload = "".join(
        files["source/arxiv-2606.05380.tar.b64"].read_text(encoding="ascii").split()
    )
    import base64

    source_hash = hashlib.sha256(
        base64.b64decode(source_payload, validate=True)
    ).hexdigest()
    assert source_hash == "364d1b1dabc7c09bce0839e214580e1beb08d78c2de7bdf2edd61fada706077c"

    secret_hits: list[tuple[str, str]] = []
    for relative, path in files.items():
        if not is_text_path(path) or path.suffix.lower() == ".b64":
            continue
        payload = path.read_bytes()
        for name, pattern in SECRET_PATTERNS.items():
            if pattern.search(payload):
                secret_hits.append((relative, name))
    assert not secret_hits, secret_hits

    allowlist = RELEASE_ALLOWLIST.read_text().splitlines()
    assert allowlist == sorted(set(allowlist))
    expected_allowlist = expected_upload_paths(files, judged_files)
    assert allowlist == expected_allowlist, {
        "missing": sorted(set(expected_allowlist) - set(allowlist)),
        "extra": sorted(set(allowlist) - set(expected_allowlist)),
    }
    assert all(is_text_path(Path(relative)) for relative in allowlist)
    assert not any(relative.endswith(".png") for relative in allowlist)
    manifest = json.loads(RELEASE_MANIFEST.read_text())
    assert manifest["space_id"] == "DineshAI/JIbkbLYo3o"
    assert manifest["self_excluded_path"] == SELF_EXCLUDED
    expected_hashes = {
        relative: sha256(files[relative])
        for relative in allowlist
        if relative != SELF_EXCLUDED
    }
    assert manifest["files"] == expected_hashes
    tree_digest = hashlib.sha256(
        "".join(
            f"{path}\0{digest}\n" for path, digest in sorted(expected_hashes.items())
        ).encode()
    ).hexdigest()
    assert manifest["payload_tree_sha256"] == tree_digest

    first_pass = files["evidence/red-team/pass-1.md"].read_text()
    second_pass = files["evidence/red-team/pass-2.md"].read_text()
    assert "README.md" in first_pass and "Files opened" in first_pass
    assert "Missing conclusions:" in first_pass and "Fixes applied" in first_pass
    assert "README.md" in second_pass and "Files opened" in second_pass
    assert "Missing conclusions: none" in second_pass

    return {
        "status": "PASS",
        "space_id": "DineshAI/JIbkbLYo3o",
        "judged_revision": judged["revision"],
        "historical_paths_preserved": len(judged_files),
        "historical_protected_hashes_unchanged": len(judged_files)
        - len(EDITABLE_HISTORICAL_PATHS),
        "canonical_entrypoint": "README.md",
        "reachable_files": len(reachable),
        "broken_links": 0,
        "claim_pages_complete": 6,
        "red_team_passes": 2,
        "secret_hits": 0,
        "upload_files": len(allowlist),
        "payload_tree_sha256": tree_digest,
        "source_sha256": source_hash,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-release-files", action="store_true")
    args = parser.parse_args()
    judged = json.loads(JUDGED_MANIFEST.read_text())
    if args.write_release_files:
        write_release_files(judged["files"])
        print(
            json.dumps(
                {
                    "status": "WROTE_RELEASE_FILES",
                    "allowlist": RELEASE_ALLOWLIST.relative_to(CANDIDATE).as_posix(),
                    "manifest": RELEASE_MANIFEST.relative_to(CANDIDATE).as_posix(),
                },
                indent=2,
            )
        )
        return
    result = audit()
    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
