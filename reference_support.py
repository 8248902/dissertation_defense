#!/usr/bin/env python3
"""Refresh and validate the bundled dissertation-reference snapshot.

Refresh explicitly after a successful thesis build:
    python3 reference_support.py --thesis-build /tmp/udts_recheck.XXXX/build
The adjacent src/ copy must match the sibling dissertation_thesis sources.
Normal defense builds use the snapshot, validate its source hashes when the
sibling thesis exists, and generate only a small auxiliary file in /tmp.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
THESIS = ROOT.parent / 'dissertation_thesis'
SNAPSHOT = ROOT / 'thesis-references.json'
MAIN = 'GMU-Diss_template'
REFRESH = 'Rebuild the thesis, then run make refs THESIS_BUILD=/path/to/fresh/build.'

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def argument(text: str, start: int) -> tuple[str, int]:
    while start < len(text) and text[start].isspace(): start += 1
    if start >= len(text) or text[start] != '{': raise ValueError('Malformed braced reference argument')
    depth, end = 1, start + 1
    while end < len(text):
        if text[end] == '\\': end += 2; continue
        if text[end] == '{': depth += 1
        if text[end] == '}': depth -= 1
        if depth == 0: return text[start + 1:end], end + 1
        end += 1
    raise ValueError('Unclosed reference argument')

def without_comments(text: str) -> str:
    return re.sub(r'(?<!\\)%[^\n]*', '', text)

def read_aux(build: Path) -> tuple[dict, dict]:
    labels, hashes, seen = {}, {}, set()
    def visit(path: Path) -> None:
        path = path.resolve()
        if path in seen: return
        if not path.is_file(): raise FileNotFoundError(f'Missing thesis auxiliary file: {path}')
        if build.resolve() not in path.parents:
            raise ValueError(f'Thesis auxiliary input is outside the specified build: {path}')
        seen.add(path)
        hashes[path.relative_to(build.resolve()).as_posix()] = digest(path)
        text = path.read_text(encoding='utf-8')
        for match in re.finditer(r'^\\newlabel(?=\{)', text, re.MULTILINE):
            key, pos = argument(text, match.end())
            body, _ = argument(text, pos)
            fields, pos = [], 0
            while body[pos:].strip():
                field, pos = argument(body, pos)
                fields.append(field)
            if len(fields) < 2: raise ValueError(f'Malformed thesis label: {key}')
            # cleveref metadata has nested non-display values; ordinary labels
            # remain the source of all \ref and \pageref values.
            if key.endswith('@cref'): continue
            value = dict(number=fields[0], page=fields[1], title=fields[2] if len(fields)>2 else '', anchor=fields[3] if len(fields)>3 else '')
            if key in labels and labels[key] != value: raise ValueError(f'Conflicting thesis label: {key}')
            labels[key] = value
        for match in re.finditer(r'\\@input\b', text):
            child, _ = argument(text, match.end())
            visit(path.parent / child)
    visit(build / (MAIN + '.aux'))
    if not labels: raise ValueError('The thesis build contains no extracted labels')
    return labels, hashes

def source_inputs(thesis: Path, copied: Path, build: Path) -> dict[str, str]:
    """Hash source text/style/bibliography and local recorder inputs (figures)."""
    if not thesis.is_dir() or not copied.is_dir():
        raise ValueError('Refresh requires both the sibling thesis and the fresh build source copy')
    sources = {path for path in thesis.rglob('*') if path.is_file() and path.suffix in {'.tex','.sty','.cls','.bib'} and '.git' not in path.parts}
    fls = build / (MAIN + '.fls')
    if not fls.is_file(): raise FileNotFoundError(f'Missing thesis recorder file: {fls}')
    text = fls.read_text(encoding='utf-8')
    pwd = next((Path(line[4:]) for line in text.splitlines() if line.startswith('PWD ')), copied)
    for line in text.splitlines():
        if not line.startswith('INPUT '): continue
        candidate = Path(line[6:])
        if not candidate.is_absolute(): candidate = pwd / candidate
        candidate = candidate.resolve()
        try: relative = candidate.relative_to(copied.resolve())
        except ValueError: continue
        original = thesis / relative
        if original.is_file(): sources.add(original)
        elif candidate.name.endswith('-eps-converted-to.pdf'):
            original = thesis / relative.with_name(candidate.name.removesuffix('-eps-converted-to.pdf') + '.eps')
            if not original.is_file(): raise FileNotFoundError(f'Original EPS source is missing: {original}')
            sources.add(original)
        elif candidate.suffix not in {'.aux','.bbl','.out','.toc','.lof','.lot','.log'}:
            raise ValueError(f'Build input has no matching thesis source: {relative}')
    result = {}
    for source in sorted(sources):
        relative = source.relative_to(thesis).as_posix()
        counterpart = copied / relative
        if not counterpart.is_file() or digest(source) != digest(counterpart):
            raise ValueError(f'Thesis changed since this build: {relative}. {REFRESH}')
        result[relative] = digest(source)
    return result

def refresh(build: Path, thesis: Path = THESIS, snapshot: Path = SNAPSHOT, copied: Path | None = None) -> dict:
    build, thesis = build.resolve(), thesis.resolve()
    copied = copied.resolve() if copied else build.parent / 'src'
    log = build / (MAIN + '.log')
    if not (build / (MAIN + '.pdf')).is_file() or not log.is_file():
        raise ValueError('Reference refresh requires a completed thesis PDF and log')
    text = log.read_text(encoding='utf-8')
    if re.search(r'^!|There were undefined references|Label\(s\) may have changed', text, re.MULTILINE):
        raise ValueError('Thesis build has errors or unresolved references; complete a clean build before refreshing')
    labels, auxiliary = read_aux(build)
    sources = source_inputs(thesis, copied, build)
    result = dict(schema_version=1, generated_at_utc=datetime.now(timezone.utc).isoformat(timespec='seconds'),
                  thesis_main=MAIN, thesis_pdf_sha256=digest(build / (MAIN + '.pdf')),
                  source_sha256=sources, auxiliary_sha256=auxiliary, labels=dict(sorted(labels.items())))
    snapshot.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(f'Refreshed {snapshot.name}: {len(labels)} labels, {len(sources)} thesis input hashes.')
    return result

def load_snapshot(snapshot: Path = SNAPSHOT, thesis: Path = THESIS) -> dict:
    if not snapshot.is_file(): raise ValueError(f'Missing {snapshot.name}. {REFRESH}')
    try: data = json.loads(snapshot.read_text(encoding='utf-8'))
    except (ValueError, OSError) as error: raise ValueError(f'Malformed reference snapshot: {error}') from error
    if not isinstance(data, dict) or data.get('schema_version') != 1 or not isinstance(data.get('labels'), dict) or not data['labels'] or not isinstance(data.get('source_sha256'),dict) or not data['source_sha256']:
        raise ValueError(f'Malformed {snapshot.name}: expected labels and source hashes. {REFRESH}')
    for key, value in data['labels'].items():
        if not isinstance(value,dict) or not all(isinstance(value.get(field),str) for field in ['number','page']):
            raise ValueError(f'Malformed reference label {key!r} in {snapshot.name}')
    for name, expected in data['source_sha256'].items():
        if not isinstance(expected,str) or not re.fullmatch('[0-9a-f]{64}', expected) or Path(name).is_absolute() or '..' in Path(name).parts:
            raise ValueError(f'Malformed source hash entry in {snapshot.name}: {name!r}')
        if thesis.is_dir():
            path = thesis / name
            if not path.is_file() or digest(path) != expected:
                raise ValueError(f'Stale dissertation references: {name} changed or is missing. {REFRESH}')
    return data

def used_references(text: str) -> list[tuple[str,str,str]]:
    refs = []
    clean = without_comments(text)
    for match in re.finditer(r'\\(drefpage|dref)\b', clean):
        first, pos = argument(clean, match.end())
        if match[1] == 'dref':
            key, _ = argument(clean, pos)
            refs.append(('number', first, key))
        else: refs.append(('page', 'p.', first))
    return refs

def validate_references(snapshot: dict, root: Path = ROOT) -> set[str]:
    used = set()
    for filename in ['core.tex', 'backup.tex']:
        for kind, _, key in used_references((root / filename).read_text(encoding='utf-8')):
            field = 'page' if kind == 'page' else 'number'
            if key not in snapshot['labels'] or not snapshot['labels'][key][field]:
                raise ValueError(f'Unresolved dissertation reference {key!r} in {filename}. {REFRESH}')
            used.add(key)
    return used

def write_external_aux(directory: Path, snapshot: dict, used: set[str]) -> None:
    lines = ['\\relax']
    for key in sorted(used):
        value = snapshot['labels'][key]
        lines.append(r'\newlabel{' + key + '}{{' + value['number'] + '}{' + value['page'] + '}{}{}{}}')
    (directory / 'thesis-labels.aux').write_text('\n'.join(lines) + '\n', encoding='utf-8')

def resolved_footer(text: str, snapshot: dict) -> str:
    result, cursor = [], 0
    for match in re.finditer(r'\\(drefpage|dref)\b', text):
        result.append(text[cursor:match.start()])
        first, end = argument(text, match.end())
        if match[1] == 'dref':
            key, end = argument(text, end)
            result.append(first + ' ' + snapshot['labels'][key]['number'])
        else: result.append('p. ' + snapshot['labels'][first]['page'])
        cursor = end
    result.append(text[cursor:])
    return ''.join(result).replace(r'\_', '_').replace('~',' ')

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--thesis-build', type=Path)
    parser.add_argument('--thesis-root', type=Path, default=THESIS)
    parser.add_argument('--build-source', type=Path, help='Source copy used by the build; default ../src relative to build')
    args = parser.parse_args()
    if args.thesis_build: refresh(args.thesis_build,args.thesis_root,copied=args.build_source)
    data = load_snapshot(thesis=args.thesis_root)
    used = validate_references(data)
    print(f'Validated {len(used)} dissertation labels used by the defense.')

if __name__ == '__main__':
    try: main()
    except (ValueError, FileNotFoundError) as error: raise SystemExit(str(error))
