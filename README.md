# Dissertation defense

This is the single active defense, on `main`.

- [Audience deck](defense.pdf): 35 main slides and 53 backups.
- [Speaker edition](defense-notes.pdf): slide-level notes.
- [Rehearsal script](defense-script.pdf): full main-talk scripts and self-contained backup answers; editable source is [defense-script.md](defense-script.md).
- [Synchronized presenter edition](defense-presenter.pdf): slides and full script paired for Pympress; rebuild with `make presenter`.
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

## Presenting on Zoom with a private synchronized script

For Linux with two monitors, use the optional Pympress edition. It pairs every audience slide with its complete script page, including backups. A single next/previous slide action advances both views. The three script introduction/index pages are excluded from this pairing.

On Ubuntu, install the viewer, PDF build dependency, and video backend:

```bash
sudo apt install pympress python3-pypdf gstreamer1.0-gtk3 gstreamer1.0-libav
make presenter PYTHON=/usr/bin/python3
pympress --notes=after defense-presenter.pdf
```

Use an extended desktop. Keep Pympress's presenter window on your private monitor and the audience window on the other monitor. In Zoom, share only the audience window. Advance slides from the presenter window with the arrow keys or a clicker; the full script changes with the slide. This synchronizes pages, rather than continuously scrolling two independent PDF viewers. Resize the notes pane to make the script comfortable to read. Pympress's `S` shortcut swaps the screens. The large presenter pane should show the full script for the current slide. If notes mode has been toggled off, press `N` in the presenter window to enable it.

Slide 20 in this edition uses linked, looping MP4s. Click each animation panel to play it. Keep `figures/aperture/app5-hide.mp4` and `app6-show.mp4` at their relative paths beside the PDF's directory when copying the presentation. Both videos can also be opened directly in a media player. The normal audience PDF continues to use its original animation build.

Rebuild with `make presenter` whenever slides or script change. This target compiles both from current sources and checks their pairing before publishing. Its PDF contains all slides followed by all script pages; open it with Pympress's `--notes=after` option so the script appears only in the private presenter view. The presenter PDF includes private script text, so send `defense.pdf` when distributing audience slides.

Before the defense, rehearse a Zoom screen share and check its audience view, script readability, next/previous navigation, and both videos. Build and file checks can verify the pairings and media paths; playback and screen capture depend on the presentation computer. Pympress setup and media support: https://pympress.github.io/README.html. Zoom window sharing: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0060596.

The grouped presenter PDF labels its script pages `script:1`, `script:2`, etc. Keep this prefix when changing the builder: Pympress reserves `notes:` for a different layout with each script page immediately following its slide. Using `notes:` for the grouped PDF makes startup select that incompatible layout and leaves the script pane empty, even when launched with `--notes=after`. After replacing an older presenter PDF, close both Pympress windows and reopen the rebuilt file with the command above.
