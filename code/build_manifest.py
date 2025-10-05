#!/usr/bin/env python3
"""
build_manifest.py  —  Merge-safe file manifest builder

- Reads metadata/file_manifest.csv (canonical header below)
- PRESERVES human fields: title, description, keywords, author, license_override
- REFRESHES computed fields: size_bytes, sha256, rows, cols
- Writes the updated CSV back (UTF-8, \n newlines)
- Generates docs/FILE_MANIFEST.md with a readable summary table

Canonical CSV header (order matters):
path,kind,size_bytes,sha256,rows,cols,title,description,keywords,author,license_override
"""

from __future__ import annotations
import argparse
import csv
import hashlib
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Any

# ---------- Paths ----------
# Script lives in .../code/build_manifest.py; repo root is its parent directory
REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = REPO_ROOT / "metadata" / "file_manifest.csv"
DEFAULT_MD = REPO_ROOT / "docs" / "FILE_MANIFEST.md"

# ---------- Constants ----------
HEADER = [
    "path",
    "kind",
    "size_bytes",
    "sha256",
    "rows",
    "cols",
    "title",
    "description",
    "keywords",
    "author",
    "license_override",
]

HUMAN_FIELDS = {"title", "description", "keywords", "author", "license_override"}
COMPUTED_FIELDS = {"size_bytes", "sha256", "rows", "cols"}


# ---------- Helpers ----------
def sha256_file(p: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()


def count_csv_rows_cols(p: Path) -> Tuple[int, int]:
    """
    Count rows and columns for a CSV file.
    - Rows include header row.
    - Cols = number of columns in header (or max seen if header missing).
    """
    import csv

    rows = 0
    cols = 0
    # Handle optional BOM cleanly
    with p.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader, start=1):
            rows += 1
            cols = max(cols, len(row))
    return rows, cols


def human_bytes(n: int) -> str:
    """Human-friendly size."""
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(n)
    for u in units:
        if size < 1024 or u == units[-1]:
            return f"{size:.0f} {u}" if u == "B" else f"{size:.1f} {u}"
        size /= 1024.0
    return f"{n} B"


def read_manifest(manifest_csv: Path) -> List[Dict[str, Any]]:
    if not manifest_csv.exists():
        sys.exit(f"[ERROR] Manifest not found: {manifest_csv}")

    with manifest_csv.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        cols = [c.strip() for c in reader.fieldnames or []]
        # Soft-validate header presence
        missing = [c for c in HEADER if c not in cols]
        if missing:
            sys.exit(
                "[ERROR] Manifest header mismatch.\n"
                f"Missing in CSV: {missing}\n"
                f"Expected header exactly:\n{','.join(HEADER)}"
            )
        rows = []
        for r in reader:
            # Normalize keys; ensure all HEADER keys present
            norm = {k: (r.get(k, "") or "").strip() for k in HEADER}
            rows.append(norm)
        return rows


def write_manifest(manifest_csv: Path, rows: List[Dict[str, Any]]) -> None:
    manifest_csv.parent.mkdir(parents=True, exist_ok=True)
    with manifest_csv.open("w", encoding="utf-8", newline="\n") as f:
        writer = csv.DictWriter(f, fieldnames=HEADER)
        writer.writeheader()
        for r in rows:
            writer.writerow({k: r.get(k, "") for k in HEADER})


def build_markdown(md_path: Path, rows: List[Dict[str, Any]]) -> None:
    md_path.parent.mkdir(parents=True, exist_ok=True)

    total_size = 0
    present_rows = []
    for r in rows:
        try:
            b = int(r.get("size_bytes") or 0)
        except ValueError:
            b = 0
        total_size += b
        present_rows.append(r)

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    lines = []
    lines.append("# File manifest")
    lines.append("")
    lines.append(f"_Generated: {timestamp}_")
    lines.append("")
    lines.append("| Path | Kind | Size | Rows | Cols | Title | SHA256 (8) |")
    lines.append("|------|------|------:|-----:|-----:|-------|------------|")

    for r in present_rows:
        size = r.get("size_bytes") or ""
        size_h = human_bytes(int(size)) if size.isdigit() else ""
        sha = (r.get("sha256") or "")[:8]
        rows_c = r.get("rows") or ""
        cols_c = r.get("cols") or ""
        title = r.get("title") or ""
        lines.append(
            f"| {r.get('path','')} | {r.get('kind','')} | {size_h} | {rows_c} | {cols_c} | {title} | `{sha}` |"
        )

    lines.append("")
    lines.append(f"**Files:** {len(present_rows)} &nbsp;&nbsp; **Total size:** {human_bytes(total_size)}")
    lines.append("")
    lines.append(
        "> Notes: Sizes/rows/cols are derived automatically. Human fields (title/description/keywords/author/license_override) "
        "are preserved from the CSV and can be edited there."
    )
    lines.append("")

    md_path.write_text("\n".join(lines), encoding="utf-8")


def refresh_rows(rows: List[Dict[str, Any]], base: Path) -> List[Dict[str, Any]]:
    """
    For each existing row:
    - Recalculate computed fields
    - Preserve human fields
    """
    updated: List[Dict[str, Any]] = []

    for r in rows:
        rel = r.get("path", "").strip()
        if not rel:
            continue

        # Ensure all keys exist
        for k in HEADER:
            r.setdefault(k, "")

        p = (base / rel).resolve()
        exists = p.exists()

        # Start with original row data (so human fields remain)
        out = {k: r.get(k, "") for k in HEADER}

        # Compute numbers if file exists
        if exists and p.is_file():
            try:
                size = p.stat().st_size
                out["size_bytes"] = str(size)
                out["sha256"] = sha256_file(p)

                if p.suffix.lower() == ".csv":
                    nrows, ncols = count_csv_rows_cols(p)
                    out["rows"] = str(nrows)
                    out["cols"] = str(ncols)
                else:
                    out["rows"] = ""
                    out["cols"] = ""
            except Exception as e:
                print(f"[WARN] Could not compute for {rel}: {e}", file=sys.stderr)
        else:
            # Missing file: clear computed fields (preserve human)
            out["size_bytes"] = ""
            out["sha256"] = ""
            out["rows"] = ""
            out["cols"] = ""
            print(f"[WARN] Missing file listed in manifest: {rel}", file=sys.stderr)

        updated.append(out)

    return updated


# ---------- CLI ----------
def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Rebuild file manifest (merge-safe).")
    ap.add_argument(
        "--manifest",
        default=str(DEFAULT_MANIFEST),
        help=f"Path to manifest CSV (default: {DEFAULT_MANIFEST})",
    )
    ap.add_argument(
        "--out-md",
        default=str(DEFAULT_MD),
        help=f"Path to FILE_MANIFEST.md (default: {DEFAULT_MD})",
    )
    ap.add_argument(
        "--no-md",
        action="store_true",
        help="Do not write docs/FILE_MANIFEST.md",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not write files; just print a summary",
    )
    return ap.parse_args()


def main() -> int:
    args = parse_args()
    manifest_csv = Path(args.manifest)
    out_md = Path(args.out_md)

    if not manifest_csv.is_absolute():
        manifest_csv = (REPO_ROOT / manifest_csv).resolve()
    if not out_md.is_absolute():
        out_md = (REPO_ROOT / out_md).resolve()

    rows = read_manifest(manifest_csv)
    updated = refresh_rows(rows, REPO_ROOT)

    # Print brief summary
    ok = sum(1 for r in updated if r.get("size_bytes"))
    missing = len(updated) - ok
    print(f"[INFO] Files in manifest: {len(updated)}  |  present: {ok}  |  missing: {missing}")

    if args.dry_run:
        print("[INFO] Dry run: not writing CSV/MD.")
        return 0

    write_manifest(manifest_csv, updated)
    print(f"[INFO] Wrote {manifest_csv}")

    if not args.no_md:
        build_markdown(out_md, updated)
        print(f"[INFO] Wrote {out_md}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
