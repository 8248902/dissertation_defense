# Dissertation defense

This is the single active defense, on `main`. The selected Opus presentation and its supporting material were consolidated here on October 18, 2026.

- [Audience deck](defense.pdf): 35 main slides and 53 backups.
- [Speaker edition](defense-notes.pdf): slide-level notes.
- [Rehearsal script](defense-script.pdf): full main-talk scripts and self-contained backup answers; editable source is [defense-script.md](defense-script.md).
- [Strategy](strategy.md), [delivery guide](delivery-guide.txt), and [related-work rationale and citations](related-work.md).
- [Current state and next-session instructions](STATE.md).

Run `make check` to check script/deck alignment and figure availability. Run `make all` to rebuild all three PDFs and refresh build validation, the source map, and source hashes. Builds use disposable directories under `/tmp`; only final deliverables are published here. Requirements: Python 3 and a TeX installation with Beamer, animate, and the packages used by the sources.

Edit slide content and embedded speaker notes in `core.tex` and `backup.tex`; edit the full spoken script in `defense-script.md`. Keep their titles and numbering synchronized. `defense.tex` controls the presentation and theme. The script builder checks every section against the live deck.

Slide 20 contains the credited aperture animations. Playback depends on PDF-viewer support; `aperture-demo.html` provides a self-contained browser alternative. Static posters remain visible in print and the speaker edition.

Earlier proposal folders are preserved under `../misc_ideas_feedback/_archive/`. The old candidate branch is historical; continue work here on `main`. Dated committee review evidence is under `history/committee-review-2026-10-03/`. Current `validation.json` reports build and synchronization checks, not a new mathematical review.

## Dissertation references

Footers use actual LaTeX cross-references imported from a complete dissertation build. Write `\dref{Theorem}{thm:uniqueness}` for a numbered result and `\drefpage{subsubsec:ode}` for a page reference. Unnumbered topics use their name and page, since their labels inherit an enclosing section counter. `thesis-references.json` bundles the compiled labels and hashes of the thesis inputs; keep it with the defense source. The build creates the auxiliary file for `xr` under `/tmp` and renders `\ref*` / `\pageref*`.

After changing dissertation sources:

1. Run `../dissertation_format_rules/recheck.sh` and use the completed build directory it reports.
2. Run `make refs THESIS_BUILD=/tmp/udts_recheck.XXXXXX/build`, substituting that directory.
3. Run `make all`.

Normal builds check the snapshot against the sibling thesis and report stale or missing labels before compiling. A standalone copy of the defense can use the bundled snapshot. `source-map.csv` contains both readable numbered footers and the underlying keys/source locations. The snapshot was refreshed from the October 18, 208-page dissertation build; its formatting check passed all 35 rules.
