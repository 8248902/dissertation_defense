"""Regenerate defense source navigation and the current input hash manifest.

Run from any working directory with Python 3. The dated October 2 manifest is
kept as a historical record; this script updates only the current manifest.
"""

from __future__ import annotations

import csv
import hashlib
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DEFENSE = ROOT / "defense"


def read_dissertation_labels() -> dict[str, tuple[str, str]]:
    """Read compiled label numbers/pages when optional aux files are present."""
    labels: dict[str, tuple[str, str]] = {}
    aux_files = list(ROOT.glob("chapter*.aux")) + [ROOT / "appendixA.aux"]
    pattern = re.compile(r"\\newlabel\{([^}]+)\}\{\{([^{}]*)\}\{([^{}]*)\}")
    for path in aux_files:
        if not path.is_file():
            continue
        for match in pattern.finditer(path.read_text(encoding="utf-8")):
            labels[match.group(1)] = (match.group(2), match.group(3))
    return labels


def source_label_locations(source_paths: list[Path]) -> dict[str, list[str]]:
    locations: dict[str, list[str]] = {}
    for path in source_paths:
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT).as_posix()
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for label in re.findall(r"\\label\{([^}]+)\}", line):
                locations.setdefault(label, []).append(f"{relative}:{line_number}")
    return locations


def main() -> None:
    labels = read_dissertation_labels()
    source_paths = [
        ROOT / name
        for name in (
            "chapterOne.tex",
            "chapterTwo.tex",
            "chapterThree.tex",
            "chapterFour.tex",
            "chapterFive.tex",
            "appendixA.tex",
        )
    ]
    source_paths += sorted((ROOT / "shared_bodies").glob("*.tex"))
    source_paths += sorted((ROOT / "appendix_bodies").glob("*.tex"))
    locations = source_label_locations(source_paths)

    rows: list[list[object]] = []
    slide_number = 0
    section = "The inverse problems"
    role_counts = {"core": 0, "discussion": 0}
    for filename, role in (("core.tex", "core"), ("backup.tex", "discussion")):
        path = DEFENSE / filename
        content = path.read_text(encoding="utf-8")
        matches = list(
            re.finditer(
                r"\\begin\{frame\}(?:\[[^\]]*\])?(?:\{([^\n]*)\})?",
                content,
            )
        )
        for index, match in enumerate(matches):
            slide_number += 1
            role_counts[role] += 1
            block_end = matches[index + 1].start() if index + 1 < len(matches) else len(content)
            block = content[match.start() : block_end]
            before = content[: match.start()]
            sections = re.findall(r"\\section\{([^}]+)\}", before)
            if sections:
                section = sections[-1]
            if role == "discussion":
                section = "Discussion and additional proofs"

            title = (match.group(1) or "Title / opening").strip()
            statements = re.findall(r"\\src\{([^\n]+)\}", block)
            statement = "; ".join(statements).replace(r"\_", "_")
            selected_labels: list[str] = []
            for label in re.findall(r"\b[a-z]+:[A-Za-z0-9_]+", statement):
                if label not in selected_labels:
                    selected_labels.append(label)

            references: list[str] = []
            source_locations: list[str] = []
            for label in selected_labels:
                if label in labels:
                    number, page = labels[label]
                    references.append(f"{label} = {number}, dissertation p. {page}")
                source_locations.extend(locations.get(label, []))

            numerical_sources = re.findall(r"^% source:\s*(.*)$", block, re.MULTILINE)
            source_line = content.count("\n", 0, match.start()) + 1
            rows.append(
                [
                    slide_number,
                    role,
                    section,
                    title,
                    f"defense/{filename}:{source_line}",
                    statement,
                    "; ".join(dict.fromkeys(source_locations)),
                    "; ".join(references),
                    " | ".join(source.strip() for source in numerical_sources),
                ]
            )

    source_map = DEFENSE / "source-map.csv"
    with source_map.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(
            [
                "pdf_slide",
                "role",
                "section",
                "slide_title",
                "editable_source",
                "dissertation_source_footer",
                "source_label_locations",
                "compiled_dissertation_references",
                "immediate_numerical_provenance",
            ]
        )
        writer.writerows(rows)

    figures: set[Path] = set()
    figure_pattern = re.compile(r"\{((?:\.\./)?figures/[^}]+)\}")
    for filename in ("core.tex", "backup.tex"):
        content = (DEFENSE / filename).read_text(encoding="utf-8")
        for figure in figure_pattern.findall(content):
            relative = figure.removeprefix("../")
            figures.add(ROOT / relative)

    fixed_inputs = [ROOT / "gmuETD.bib", ROOT / "GMU-Diss_template.tex"]
    inputs = set(source_paths + fixed_inputs) | figures
    current_manifest = DEFENSE / "source-snapshot.sha256"
    manifest_entries: list[tuple[str, str]] = []
    for path in sorted(inputs):
        if path.is_file():
            manifest_entries.append(
                (hashlib.sha256(path.read_bytes()).hexdigest(), path.relative_to(ROOT).as_posix())
            )
    with current_manifest.open("w", encoding="utf-8", newline="\n") as stream:
        for digest, relative in manifest_entries:
            stream.write(f"{digest}  {relative}\n")

    print(
        f"Updated {source_map.relative_to(ROOT)}: {len(rows)} slides "
        f"({role_counts['core']} core, {role_counts['discussion']} discussion); "
        f"updated {current_manifest.relative_to(ROOT)}: {len(manifest_entries)} inputs "
        f"including {len(figures)} referenced figures."
    )


if __name__ == "__main__":
    main()
