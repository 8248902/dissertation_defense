#!/usr/bin/env python3
"""Rebuild current source navigation and hashes; preserve dated historical records.

Compiled thesis numbers are included only with --thesis-build PATH. Manifest
paths are relative to this defense directory and work with sha256sum --check.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FRAME = re.compile(r"\\begin\{frame\}(?:\[[^\]]*\])?")

def braced(text: str, start: int) -> tuple[str, int]:
    """Read a balanced TeX argument, respecting escaped braces."""
    while start < len(text) and text[start].isspace():
        start += 1
    if start >= len(text) or text[start] != '{':
        raise ValueError(f'Expected braced argument at character {start}')
    depth, end = 1, start + 1
    while end < len(text):
        if text[end] == '\\':
            end += 2
            continue
        if text[end] == '{': depth += 1
        if text[end] == '}': depth -= 1
        if depth == 0: return text[start + 1:end], end + 1
        end += 1
    raise ValueError('Unclosed TeX argument')

def commands(text: str, name: str) -> list[str]:
    return [braced(text, m.end())[0] for m in re.finditer(r'\\' + name + r'\b', text)]

def read_frames(root: Path = ROOT) -> list[dict]:
    frames = []
    for filename, role in [('core.tex', 'core'), ('backup.tex', 'discussion')]:
        text = (root / filename).read_text(encoding='utf-8')
        for index, match in enumerate(FRAME.finditer(text), 1):
            end = text.find(r'\end{frame}', match.end())
            if end < 0: raise ValueError(f'Unclosed frame in {filename}')
            rest = text[match.end():end].lstrip()
            title = braced(rest, 0)[0] if rest.startswith('{') else 'Title'
            sections = commands(text[:match.start()], 'section')
            section = sections[-1] if sections else 'The inverse problems'
            if role == 'discussion': section = 'Discussion and additional proofs'
            frames.append(dict(page=len(frames) + 1, number=index, role=role,
                               title=title, section=section, filename=filename,
                               line=text.count('\n', 0, match.start()) + 1,
                               block=text[match.start():end]))
    return frames

def figure_paths(root: Path = ROOT) -> set[Path]:
    """Collect literal figure arguments and expand every animation frame."""
    figures = set()
    def resolve(name: str) -> Path:
        path = root / name
        if path.is_file(): return path
        for suffix in ('.pdf', '.png', '.jpg', '.jpeg'):
            if path.with_name(path.name + suffix).is_file():
                return path.with_name(path.name + suffix)
        raise FileNotFoundError(f'Referenced figure is missing: {name}')
    for filename in ('core.tex', 'backup.tex'):
        text = (root / filename).read_text(encoding='utf-8')
        prefixes = set()
        for match in re.finditer(r'\\animategraphics(?:\[[^\]]*\])?', text):
            args, pos = [], match.end()
            for _ in range(4):
                value, pos = braced(text, pos)
                args.append(value)
            _, prefix, first, last = args
            prefixes.add(prefix)
            width = len(first) if first.startswith('0') else 0
            for number in range(int(first), int(last) + 1):
                figures.add(resolve(prefix + str(number).zfill(width)))
        for name in re.findall(r'\{(figures/[^{}]+)\}', text):
            if name not in prefixes: figures.add(resolve(name))
    return figures

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--thesis-root', type=Path, default=ROOT.parent / 'dissertation_thesis')
    parser.add_argument('--thesis-build', type=Path, help='Explicit build directory containing current thesis .aux files')
    parser.add_argument('--output-dir', type=Path, default=ROOT)
    args = parser.parse_args()
    thesis = args.thesis_root.resolve()
    sources = sorted(thesis.glob('*.tex')) + sorted(thesis.glob('shared_bodies/*.tex')) + sorted(thesis.glob('appendix_bodies/*.tex'))
    locations = {}
    for path in sources:
        for number, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
            for label in re.findall(r'\\label\{([^}]+)\}', line):
                locations.setdefault(label, []).append(f'{os.path.relpath(path, ROOT)}:{number}')
    labels = {}
    if args.thesis_build:
        if not args.thesis_build.is_dir(): raise ValueError('--thesis-build must be an existing directory')
        for path in sorted(args.thesis_build.rglob('*.aux')):
            for match in re.finditer(r'\\newlabel\{([^}]+)\}\{\{([^{}]*)\}\{([^{}]*)\}', path.read_text(encoding='utf-8')):
                labels[match[1]] = (match[2], match[3])
    rows = []
    frames = read_frames()
    for frame in frames:
        footer = '; '.join(commands(frame['block'], 'src'))
        if not footer:
            custom = re.search(r'Dissertation:\s*(.*?)(?:\\par|$)', frame['block'])
            if custom:
                footer = custom.group(1).strip()
        footer = footer.replace(r'\_', '_')
        selected = list(dict.fromkeys(re.findall(r'\b[a-z]+:[A-Za-z0-9_]+', footer)))
        references = [f'{label} = {labels[label][0]}, dissertation p. {labels[label][1]}' for label in selected if label in labels]
        provenance = re.findall(r'^\s*% source:\s*(.*)$', frame['block'], re.MULTILINE)
        rows.append([frame['page'], frame['role'], frame['section'], frame['title'],
                     f"{frame['filename']}:{frame['line']}", footer,
                     '; '.join(dict.fromkeys(loc for label in selected for loc in locations.get(label, []))),
                     '; '.join(references), ' | '.join(provenance)])
    figures = figure_paths()
    inputs = set(sources) | figures
    for name in ['defense.tex', 'notes.tex', 'core.tex', 'backup.tex', 'defense-script.md',
                 'build_script.py', 'update_metadata.py', 'Makefile', 'aperture-demo.html']:
        path = ROOT / name
        if path.is_file(): inputs.add(path)
    inputs.update(path for path in thesis.glob('*.bib'))
    inputs.update(path for path in thesis.glob('*.sty'))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    with (args.output_dir / 'source-map.csv').open('w', encoding='utf-8', newline='') as stream:
        writer = csv.writer(stream, lineterminator='\n')
        writer.writerow(['pdf_slide', 'role', 'section', 'slide_title', 'editable_source',
                         'dissertation_source_footer', 'source_label_locations',
                         'compiled_dissertation_references', 'immediate_numerical_provenance'])
        writer.writerows(rows)
    entries = sorted((os.path.relpath(path, ROOT), hashlib.sha256(path.read_bytes()).hexdigest()) for path in inputs)
    (args.output_dir / 'source-snapshot.sha256').write_text(''.join(f'{digest}  {name}\n' for name, digest in entries), encoding='utf-8')
    print(f'Updated {len(rows)} source-map rows and {len(entries)} hashes, including {len(figures)} figures.')
    if not args.thesis_build: print('Compiled thesis references left blank; supply --thesis-build to include current labels.')

if __name__ == '__main__':
    main()
