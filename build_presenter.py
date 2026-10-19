#!/usr/bin/env python3
"""Build a Pympress PDF: all slides, then matching full-script notes.

Requires the normal TeX build tools and pypdf in the selected Python environment.
Run the result with: pympress --notes=after defense-presenter.pdf
"""
from __future__ import annotations

import argparse
from pathlib import Path
import re
import shutil
import sys
import tempfile

sys.dont_write_bytecode = True
from build_script import (check_script_pages, compile_tex, parse_script, render)
from reference_support import load_snapshot, validate_references, write_external_aux
from update_metadata import ROOT, figure_paths


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, default=ROOT)
    parser.add_argument('--build-dir', type=Path, help='Retain scratch files outside the repository')
    args = parser.parse_args()
    try:
        from pypdf import PdfReader, PdfWriter
    except ImportError as error:
        raise RuntimeError('Presenter build requires pypdf in the selected Python environment. '
                           'On Ubuntu: sudo apt install python3-pypdf; then make presenter PYTHON=/usr/bin/python3. '
                           'Alternatively install pypdf in a virtual environment and set PYTHON to its interpreter.') from error

    references = load_snapshot()
    used_labels = validate_references(references)
    intro, sections = parse_script()
    figures = figure_paths()
    media = [Path('figures/aperture') / name for name in ('app5-hide.mp4', 'app6-show.mp4')]
    for path in media:
        if not (ROOT / path).is_file():
            raise FileNotFoundError(f'Presenter movie is missing: {path}')
    automatic = args.build_dir is None
    scratch = Path(tempfile.mkdtemp(prefix='defense-presenter-', dir='/tmp')) if automatic else args.build_dir.resolve()
    if scratch == ROOT or ROOT in scratch.parents:
        raise ValueError('Build directory must be outside the defense repository')
    scratch.mkdir(parents=True, exist_ok=True)
    print(f'Scratch build directory: {scratch}')

    slides = scratch / 'slides'
    slides.mkdir(exist_ok=True)
    write_external_aux(slides, references, used_labels)
    for name in ('defense.tex', 'core.tex', 'backup.tex'):
        shutil.copy2(ROOT / name, slides / name)
    for source in figures:
        destination = slides / source.relative_to(ROOT)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    (slides / 'presenter-slides.tex').write_text(
        '\\def\\DefensePresenter{1}\n\\input{defense.tex}\n', encoding='utf-8')
    slide_pdf = compile_tex(slides, 'presenter-slides.tex', 'presenter-slides')
    script = scratch / 'script'
    script.mkdir(exist_ok=True)
    (script / 'defense-script.tex').write_text(render(intro, sections), encoding='utf-8')
    script_pdf = compile_tex(script, 'defense-script.tex', 'defense-script')
    check_script_pages(script, sections)
    # Read the validated labels, so front/index length is never hard-coded.
    aux = (script / 'defense-script.aux').read_text(encoding='utf-8')
    labels = dict(re.findall(r'\\newlabel\{scriptpage(\d+)\}\{\{[^{}]*\}\{(\d+)\}', aux))
    script_indices = [int(labels[str(section['page'])]) - 1 for section in sections]
    audience = PdfReader(slide_pdf)
    narration = PdfReader(script_pdf)
    count = len(sections)
    if len(audience.pages) != count:
        raise ValueError(f'Slide PDF has {len(audience.pages)} pages for {count} script sections')

    writer = PdfWriter()
    writer.append(audience)
    writer.append(narration, pages=script_indices)
    writer.set_page_label(0, count - 1, style='/D', start=1)
    # Pympress reserves notes: for adjacent slide/notes pairs; this file uses halves.
    writer.set_page_label(count, 2 * count - 1, style='/D', prefix='script:', start=1)
    writer.add_metadata({'/Title': 'Dissertation defense — slides and full-script presenter notes',
                         '/Author': 'Daniel Blauvelt'})
    candidate = scratch / 'defense-presenter.pdf'
    writer.write(candidate)

    # Reopen the written file to verify its notes mapping and retained media.
    result = PdfReader(candidate)
    if len(result.pages) != 2 * count:
        raise ValueError('Presenter PDF page count does not match paired slides and notes')
    expected_labels = [str(n) for n in range(1, count + 1)] + [f'script:{n}' for n in range(1, count + 1)]
    if result.page_labels != expected_labels:
        raise ValueError('Presenter slide/notes labels do not match')
    for index, source_page in enumerate(script_indices):
        if result.pages[count + index].extract_text() != narration.pages[source_page].extract_text():
            raise ValueError(f'Full script text changed for deck page {index + 1}')
    movies = []
    for number, page in enumerate(result.pages[:count], 1):
        for reference in page.get('/Annots', []):
            annotation = reference.get_object()
            if annotation.get('/Subtype') == '/Movie':
                filename = str(annotation['/Movie']['/F'])
                if annotation['/A'].get('/Mode') != '/Repeat':
                    raise ValueError(f'Movie loop setting missing: {filename}')
                rect = annotation['/Rect']
                if len(rect) != 4 or rect[2] <= rect[0] or rect[3] <= rect[1]:
                    raise ValueError(f'Movie rectangle has no visible area: {filename}')
                movies.append((number, filename))
    expected_movies = [(section['page'], str(path)) for section in sections
                       if 'The aperture problem:' in section['title'] for path in media]
    if movies != expected_movies:
        raise ValueError(f'Presenter movies differ from expected aperture panels: {movies}')
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for path in media:
        destination = args.output_dir / path
        if destination.resolve() != (ROOT / path).resolve():
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / path, destination)
    destination = args.output_dir / candidate.name
    shutil.copy2(candidate, destination)
    print(f'Validated {count} slides + {count} complete script pages; two looping MP4 panels on slide {movies[0][0]}.')
    print(f'Wrote {destination}')
    print('Launch from its directory: pympress --notes=after defense-presenter.pdf')
    if automatic:
        shutil.rmtree(scratch)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, FileNotFoundError, RuntimeError) as error:
        raise SystemExit(str(error))
