#!/usr/bin/env python3
"""Build the defense PDFs with temporary TeX files outside this repository.

The rehearsal script uses defense-script.md as its sole prose source. Its
headings must match the live deck, including every backup's deck page number.
Requires Python 3, latexmk, and a standard pdfLaTeX installation; no pip packages.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from datetime import datetime, timezone
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
sys.dont_write_bytecode = True
from update_metadata import ROOT, read_frames, figure_paths
from reference_support import CITE, cite_keys, load_snapshot, validate_references, without_comments, write_external_aux

def normal_title(value: str) -> str:
    value = value.replace('$H^1$', 'H¹').replace(r'\_', '_')
    value = value.replace('---', '—').replace('--', '–').replace('’', "'")
    return ' '.join(value.split())

def parse_script() -> tuple[str, list[dict]]:
    text = (ROOT / 'defense-script.md').read_text(encoding='utf-8')
    headings = list(re.finditer(r'^## (Slide|Backup) (\d+)\s+[—–-]\s+(.+)$', text, re.MULTILINE))
    if not headings: raise ValueError('No slide or backup headings found in defense-script.md')
    frames = read_frames()
    if len(headings) != len(frames):
        raise ValueError(f'Script has {len(headings)} sections but deck has {len(frames)} frames')
    sections = []
    for index, (heading, frame) in enumerate(zip(headings, frames)):
        role = 'core' if heading[1] == 'Slide' else 'discussion'
        if role != frame['role'] or int(heading[2]) != frame['number']:
            raise ValueError(f'Script numbering mismatch at {heading[0]}')
        if normal_title(heading[3]) != normal_title(frame['title']):
            raise ValueError(f'Title mismatch: script {heading[3]!r}; deck {frame["title"]!r}')
        end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        body = text[heading.end():end].strip()
        # The next major section heading and its introduction are front matter.
        body = re.split(r'^# ', body, maxsplit=1, flags=re.MULTILINE)[0].strip()
        if role == 'discussion':
            page = re.search(r'^Deck page:\s*(\d+)\.', body, re.MULTILINE)
            if not page or int(page[1]) != frame['page']:
                raise ValueError(f'Wrong or missing deck page for Backup {frame["number"]}')
            body = body[:page.start()] + body[page.end():]
        sections.append(dict(frame, title=heading[3], body=body.strip()))
    intro = text[:headings[0].start()]
    intro = '\n'.join(line for line in intro.splitlines() if not line.startswith('# ')).strip()
    return intro, sections

def tex_escape(text: str) -> str:
    replacements = {'\\':r'\textbackslash{}', '&':r'\&', '%':r'\%', '$':r'\$', '#':r'\#', '_':r'\_',
                    '{':r'\{', '}':r'\}', '~':r'\textasciitilde{}', '^':r'\textasciicircum{}',
                    '—':'---', '–':'--', '•':r'\textbullet{}', '’':"'", '‘':"'", '“':'``', '”':"''",
                    '→':r'$\rightarrow$', '¹':r'$^1$', '²':r'$^2$', 'κ':r'$\kappa$', 'λ':r'$\lambda$',
                    'τ':r'$\tau$', '∇':r'$\nabla$', '≤':r'$\leq$', '≥':r'$\geq$', '≠':r'$\neq$',
                    '∞':r'$\infty$', 'α':r'$\alpha$', 'ε':r'$\varepsilon$', 'δ':r'$\delta$',
                    'ρ':r'$\rho$', 'σ':r'$\sigma$', 'ℓ':r'$\ell$', '−':'-', '\u00a0':' '}
    return ''.join(replacements.get(char, char) for char in text)

def inline(text: str) -> str:
    # Links are printed as their readable labels; emphasis and code stay legible.
    text = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', text)
    parts = re.split(r'(\*\*[^*]+\*\*|`[^`]+`)', text)
    return ''.join(r'\textbf{' + tex_escape(p[2:-2]) + '}' if p.startswith('**') else
                   r'\texttt{' + tex_escape(p[1:-1]) + '}' if p.startswith('`') else tex_escape(p)
                   for p in parts)

REFERENCE = re.compile(r'Backup (\d+)(?:, page (\d+))?|\b[Ss]lide (\d+)\b|\bpage (\d+)\b')

def link_refs(tex: str, pages: dict | None) -> str:
    """Link Backup N, Backup N, page P, slide N, and page P to that deck page's script page."""
    if not pages:
        return tex
    def replace(match: re.Match) -> str:
        backup, stated, slide, page = match.groups()
        if backup:
            target = pages['backup'].get(int(backup))
            if target is None:
                raise ValueError(f'Script refers to missing Backup {backup}')
            if stated and int(stated) != target:
                raise ValueError(f'Script says Backup {backup} is on page {stated}; it is on page {target}')
        elif slide:
            target = int(slide) if 1 <= int(slide) <= pages['main'] else None
        else:
            target = int(page) if 1 <= int(page) <= pages['total'] else None
        if target is None:
            return match[0]
        return f'\\hyperlink{{deck{target}}}{{{match[0]}}}'
    return REFERENCE.sub(replace, tex)

def paragraphs(body: str, pages: dict | None = None) -> list[str]:
    output = []
    for paragraph in re.split(r'\n\s*\n', body.strip()):
        paragraph = paragraph.strip()
        if not paragraph: continue
        if paragraph.startswith('*[') and paragraph.endswith(']*'):
            output.append(r'{\small\itshape\color{muted}' + link_refs(tex_escape(paragraph[1:-1]), pages) + '}\n')
        elif paragraph.startswith('### '):
            output.append(r'{\small\bfseries\color{teal}' + tex_escape(paragraph[4:]) + '}\\par\n')
        elif paragraph.startswith('**Likely question:**'):
            output.append(r'{\small\color{muted}' + link_refs(inline(paragraph), pages) + '}\\par\n')
        elif paragraph.startswith('#'):
            raise ValueError(f'Unsupported heading in script body: {paragraph}')
        else:
            output.append(link_refs(inline(paragraph.replace('\n', ' ')), pages) + '\n')
    return output

PREAMBLE = r'''\documentclass[12pt,letterpaper]{article}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{lmodern,microtype,xcolor,geometry,fancyhdr,hyperref,multicol}
\geometry{margin=0.85in,headheight=16pt}
\definecolor{ink}{HTML}{172F46}
\definecolor{teal}{HTML}{007F83}
\definecolor{muted}{HTML}{506576}
\hypersetup{pdftitle={Defense rehearsal script},pdfauthor={Daniel Blauvelt},colorlinks=true,linkcolor=teal}
\pagestyle{fancy}\fancyhf{}
\fancyhead[L]{\small\color{muted}Defense rehearsal script}
\fancyhead[R]{\small\color{muted}\nouppercase{\rightmark}}
\fancyfoot[C]{\small\color{muted}\thepage}
\renewcommand{\headrulewidth}{0.3pt}
\setlength{\parindent}{0pt}\setlength{\parskip}{0.65em}
\linespread{1.08}
\begin{document}\color{ink}
'''

def render(intro: str, sections: list[dict]) -> str:
    out = [PREAMBLE, r'\thispagestyle{empty}\pdfbookmark[0]{Using this script}{intro}',
           r'{\LARGE\bfseries Defense rehearsal script\par}\vspace{1em}']
    out += paragraphs(intro)
    pages = {'backup': {s['number']: s['page'] for s in sections if s['role'] == 'discussion'},
             'main': sum(s['role'] == 'core' for s in sections), 'total': len(sections)}
    for role, label in [('core', 'Main talk index'), ('discussion', 'Backup responses index')]:
        out += [r'\clearpage\markright{' + label + '}',
                r'\pdfbookmark[0]{' + label + '}{index' + role + '}',
                r'{\LARGE\bfseries ' + label + r'\par}',
                r'{\small Each entry links to its script page. Numbers identify audience-deck pages.}\par',
                r'\begin{multicols}{2}\fontsize{8}{9.5}\selectfont\setlength{\parskip}{3pt}\raggedright']
        for section in sections:
            if section['role'] == role:
                out += [f"\\hyperlink{{deck{section['page']}}}{{\\textbf{{{section['page']}}} {tex_escape(section['title'])}}}\\par"]
        out += [r'\end{multicols}']
    for section in sections:
        main = section['role'] == 'core'
        label = f"Slide {section['number']}" if main else f"Backup {section['number']:02d} / deck {section['page']}"
        out += [r'\clearpage\markright{' + label + '}', f"\\hypertarget{{deck{section['page']}}}{{}}"]
        if section['number'] == 1:
            out += [r'\pdfbookmark[0]{' + ('Main talk' if main else 'Backup responses') + '}{' + section['role'] + '}']
        # ASCII bookmark title avoids math/superscript warnings in PDF strings.
        bookmark = section['title'].replace('¹','1').replace('²','2')
        out += [f"\\pdfbookmark[1]{{{label} --- {tex_escape(bookmark)}}}{{bookmark{section['page']}}}",
                r'{\small\bfseries\color{teal}' + label.upper() + r'}\par',
                r'{\Large\bfseries\raggedright ' + tex_escape(section['title']) + r'\par}\vspace{0.4em}',
                f"\\label{{scriptpage{section['page']}}}",
                f"% source: defense-script.md; {section['filename']}:{section['line']}."]
        out += paragraphs(section['body'], pages)
        out += [f"\\label{{scriptend{section['page']}}}"]
    out += [r'\end{document}']
    return '\n'.join(out)

def compile_tex(work: Path, source: str, job: str) -> Path:
    command = ['latexmk', '-pdf', '-interaction=nonstopmode', '-halt-on-error', f'-jobname={job}', source]
    result = subprocess.run(command, cwd=work, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    (work / f'{job}-build.txt').write_text(result.stdout, encoding='utf-8')
    if result.returncode:
        raise RuntimeError(f'{job} build failed in {work}\n' + '\n'.join(result.stdout.splitlines()[-35:]))
    log = (work / f'{job}.log').read_text(encoding='utf-8')
    warnings = [line for line in log.splitlines() if re.search(r'Warning|Overfull|Underfull|^!', line)]
    if warnings: print(f'{job} build diagnostics:\n' + '\n'.join(warnings), file=sys.stderr)
    return work / f'{job}.pdf'

def check_script_pages(work: Path, sections: list[dict]) -> None:
    aux = (work / 'defense-script.aux').read_text(encoding='utf-8')
    labels = dict(re.findall(r'\\newlabel\{(script(?:page|end)\d+)\}\{\{[^{}]*\}\{(\d+)\}', aux))
    pages = []
    for section in sections:
        number = section['page']
        start, end = labels.get(f'scriptpage{number}'), labels.get(f'scriptend{number}')
        if start is None or start != end:
            raise ValueError(f'Deck page {number} script spills beyond one page: {start} to {end}')
        pages.append(int(start))
    if any(right != left + 1 for left, right in zip(pages, pages[1:])):
        raise ValueError('Script contains unexpected blank or overflowing slide pages')
    print(f'Validated one script page per deck frame ({len(sections)} frames); {pages[0]-1} front/index pages.')

COMMITTEE_LIST = ROOT / 'committee-backups.txt'
REFS_PER_PAGE = 13  # the full deck fits 38 works on 3 pages

def committee_backup(snapshot: dict) -> str:
    """backup.tex reduced to the listed frames, then right-sized reference pages."""
    wanted = [line.strip() for line in COMMITTEE_LIST.read_text(encoding='utf-8').splitlines()
              if line.strip() and not line.startswith('#')]
    frames = [frame for frame in read_frames() if frame['role'] == 'discussion']
    by_title = {normal_title(frame['title']): frame for frame in frames}
    missing = [title for title in wanted if normal_title(title) not in by_title]
    if missing: raise ValueError(f'committee-backups.txt names unknown backups: {missing}')
    keep = {normal_title(title) for title in wanted}
    blocks = [frame['block'] + '\\end{frame}\n' for frame in frames if normal_title(frame['title']) in keep]
    selected = '\n'.join(blocks)
    cited = set()
    for text in [(ROOT / 'core.tex').read_text(encoding='utf-8'), selected]:
        for match in CITE.finditer(without_comments(text)):
            cited.update(cite_keys(match[1]))
    parts = max(1, -(-len(cited) // REFS_PER_PAGE))
    references = [frame for frame in frames if '\\thesisreferences{' in frame['block']]
    if len(references) < parts: raise ValueError('Not enough reference frames in backup.tex for the committee copy')
    for index, frame in enumerate(references[:parts], 1):
        block = re.sub(r'\{References \(\d+ of \d+\)\}', '{References (' + str(index) + ' of ' + str(parts) + ')}', frame['block'], count=1)
        blocks.append(block + '\\end{frame}\n')
    return '% Generated committee selection; edit committee-backups.txt, not this file.\n' + '\n'.join(blocks)

def check_links(work: Path) -> None:
    """Every \\hyperlink in the built source must have a target that was kept."""
    text = ''.join(without_comments((work / name).read_text(encoding='utf-8')) for name in ['core.tex', 'backup.tex'])
    targets = set(re.findall(r'label=(\w+)', text)) | set(re.findall(r'\\hypertarget\{(\w+)\}', text))
    dead = sorted(set(re.findall(r'\\hyperlink\{(\w+)\}', text)) - targets)
    if dead: raise ValueError(f'Committee copy links to slides it leaves out: {dead}')

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', choices=['all','slides','notes','script','committee'], default='script')
    parser.add_argument('--check-only', action='store_true', help='Validate all Markdown headings, numbers, and figures without building')
    parser.add_argument('--output-dir', type=Path, default=ROOT)
    parser.add_argument('--build-dir', type=Path, help='Retain scratch files in an external directory (normally /tmp)')
    args = parser.parse_args()
    references = load_snapshot()
    used_labels = validate_references(references)
    intro, sections = parse_script()
    figures = figure_paths()
    print(f'Validated {sum(s["role"]=="core" for s in sections)} main and {sum(s["role"]=="discussion" for s in sections)} backup script sections.')
    if args.check_only: return
    # A supplied directory retains build logs. Automatic scratch is removed on success.
    automatic = args.build_dir is None
    scratch = Path(tempfile.mkdtemp(prefix='defense-build-', dir='/tmp')) if automatic else args.build_dir.resolve()
    if scratch == ROOT or ROOT in scratch.parents: raise ValueError('Build directory must be outside the defense repository')
    scratch.mkdir(parents=True, exist_ok=True)
    print(f'Scratch build directory: {scratch}')
    outputs = []
    targets = ['slides','notes','script','committee'] if args.target == 'all' else [args.target]
    for target in targets:
        work = scratch / target
        work.mkdir(exist_ok=True)
        if target == 'script':
            (work / 'defense-script.tex').write_text(render(intro, sections), encoding='utf-8')
            pdf = compile_tex(work, 'defense-script.tex', 'defense-script')
            check_script_pages(work, sections)
        else:
            for name in ['defense.tex','notes.tex','core.tex','backup.tex']:
                shutil.copy2(ROOT / name, work / name)
            if target == 'committee':
                (work / 'backup.tex').write_text(committee_backup(references), encoding='utf-8')
                (work / 'defense-committee.tex').write_text('% Committee handout: main slides (with source footers) and selected backups.\n\\def\\DefenseCommittee{}\n\\input{defense.tex}\n', encoding='utf-8')
                check_links(work)
            write_external_aux(work, references, used_labels, work)
            for source in figures:
                destination = work / source.relative_to(ROOT)
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, destination)
            job, tex = {'slides': ('defense','defense.tex'), 'notes': ('defense-notes','notes.tex'),
                        'committee': ('defense-committee','defense-committee.tex')}[target]
            pdf = compile_tex(work, tex, job)
        outputs.append(pdf)
    # Publish only after every requested target has succeeded.
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for pdf in outputs:
        destination = args.output_dir / pdf.name
        shutil.copy2(pdf, destination)
        print(f'Wrote {destination}')
    if args.target == 'all':
        pdf_reports = {}
        for pdf in outputs:
            log = (pdf.parent / (pdf.stem + '.log')).read_text(encoding='utf-8')
            page_match = re.search(r'Output written on .*?\((\d+) pages?[,)]', log, re.DOTALL)
            if not page_match:
                raise ValueError(f'Could not read PDF page count from {pdf.stem}.log')
            pdf_reports[pdf.name] = {
                'pages': int(page_match[1]),
                'compile_warnings': [line for line in log.splitlines()
                                     if re.search(r'Warning|Overfull|Underfull|^!', line)],
            }
        input_names = ['core.tex', 'backup.tex', 'defense.tex', 'notes.tex', 'committee-backups.txt',
                       'defense-script.md', 'build_script.py', 'update_metadata.py', 'Makefile',
                       'reference_support.py', 'thesis-references.json']
        hashes = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in input_names}
        hashes.update({pdf.name: hashlib.sha256((args.output_dir / pdf.name).read_bytes()).hexdigest()
                       for pdf in outputs})
        report = {
            'generated_at_utc': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'scope': 'Build validation only: compilation, script/deck correspondence, layout, and input/output hashes.',
            'main_frames': sum(section['role'] == 'core' for section in sections),
            'backup_frames': sum(section['role'] == 'discussion' for section in sections),
            'referenced_figure_count': len(figures),
            'checks': {'script_titles_and_numbers_match_deck': True,
                       'backup_deck_pages_match': True,
                       'one_script_page_per_deck_frame': True,
                       'dissertation_reference_snapshot_valid': True,
                       'all_used_dissertation_labels_resolved': True},
            'pdfs': pdf_reports,
            'sha256': hashes,
        }
        (args.output_dir / 'validation.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
        print(f'Wrote build-only validation: {args.output_dir / "validation.json"}')
    else:
        print('Individual target: any existing validation.json retains its original date and hashes; use --target all to refresh it.')
    if automatic: shutil.rmtree(scratch)

if __name__ == '__main__':
    try:
        main()
    except (ValueError, FileNotFoundError, RuntimeError) as error:
        raise SystemExit(str(error))
