# Dissertation defense

This is the single active defense, on `main`.

The [spoken-recall Anki deck](anki/README.txt) has a 54-card core package and a 119-card complete package, focused on explaining the talk's results, proof mechanisms, assumptions, and consequences aloud. [Preview the cards](anki/preview.html) or import [the core deck](anki/defense-core.apkg) to begin.

- [Committee handout](defense-committee.pdf): the copy to send the committee. It has the 33 main slides, the backups listed in [committee-backups.txt](committee-backups.txt) (currently 7), and reference pages for the works those slides cite. Rebuild with `make committee`.
- [Audience deck](defense.pdf): the full presenting deck, with 33 main slides and 73 backups (70 discussion slides and 3 reference pages).
- [Speaker edition](defense-notes.pdf): slide-level notes.
- [Rehearsal script](defense-script.pdf): full main-talk scripts and self-contained backup answers; editable source is [defense-script.md](defense-script.md).
- [Synchronized presenter edition](defense-presenter.pdf): slides and full script paired for Pympress; rebuild with `make presenter`.
- [Strategy](strategy.md), [delivery guide](delivery-guide.txt), and [related-work rationale and citations](related-work.md).
- [Current state and next-session instructions](STATE.md).

Run `make check` to check script/deck alignment and figure availability. Run `make all` to rebuild all four PDFs (audience, notes, script, committee) and refresh build validation, the source map, and source hashes. Builds use disposable directories under `/tmp`; only final deliverables are published here. Requirements: Python 3 and a TeX installation with Beamer, animate, and the packages used by the sources.

Edit slide content and embedded speaker notes in `core.tex` and `backup.tex`; edit the full spoken script in `defense-script.md`. Keep their titles and numbering synchronized. `defense.tex` controls the presentation and theme. The script builder checks every section against the live deck.

Slide 20 contains the credited aperture animations. Playback depends on PDF-viewer support; `aperture-demo.html` provides a self-contained browser alternative. Static posters remain visible in print and the speaker edition.

Earlier proposal folders are preserved under `../misc_ideas_feedback/_archive/`. The old candidate branch is historical; continue work here on `main`. The five reviewed backup additions are integrated at pages 39, 40, 77, 82, and 90, with matching script answers and notes. Two theory backups (complementarity lemma, adaptive-weight stability) are integrated at pages 97 and 98. Two more, on weak-regularization limits and on harmonic fill-in of event-free flow regions, are at pages 102 and 103. A third, on fractional regularization, is kept in `held/` and stays out of every build until it is ready; `held/fractional-backup.tex` lists the steps to add it. Continue editing the active files here; the separate draft package is a review record.

Dated committee review evidence is under `history/committee-review-2026-10-03/`. Current `validation.json` reports build and synchronization checks, not a new mathematical review.

## Dissertation references

Footers use actual LaTeX cross-references imported from a complete dissertation build. Write `\dref{Theorem}{thm:uniqueness}` for a numbered result and `\drefpage{subsubsec:ode}` for a page reference. Unnumbered topics use their name and page, since their labels inherit an enclosing section counter. `thesis-references.json` bundles the compiled labels and hashes of the thesis inputs; keep it with the defense source. The build creates the auxiliary file for `xr` under `/tmp` and renders `\ref*` / `\pageref*`.

Citations use the dissertation's own numbers. Write `\cite{piatkowska2017}` with any key the dissertation cites; it prints the dissertation number, for example [78], and links to the reference pages at the end of the deck (pages 104–106). The snapshot also stores each cited work's number and `.bbl` entry, so the build writes those pages from it. A key the dissertation does not cite stops the build. The three `\thesisreferences{n}` frames at the end of `backup.tex` hold the list; the build splits the cited works across however many such frames exist, so add a frame (and its script section) if a page overflows. Sources outside the dissertation bibliography (Adelson–Movshon, Wolfe et al., Antil–Di–Khatri, Willert–Klinner) stay as typed text.

After changing dissertation sources:

1. Run `../dissertation_format_rules/recheck.sh` and use the completed build directory it reports.
2. Run `make refs THESIS_BUILD=/tmp/udts_recheck.XXXXXX/build`, substituting that directory.
3. Run `make all`.

Normal builds check the snapshot against the sibling thesis and report stale or missing labels before compiling. A standalone copy of the defense can use the bundled snapshot. `source-map.csv` contains both readable numbered footers and the underlying keys/source locations. The snapshot was refreshed from the October 19 dissertation build in `/tmp/udts_recheck.GDYNkk` (207 pages; its formatting check passed all 35 rules); `make refs` needs that build's `.aux` and `.bbl`.

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

Rebuild with `make presenter` whenever slides or script change. This target compiles both from current sources and checks their pairing before publishing. Its PDF contains all slides followed by all script pages; open it with Pympress's `--notes=after` option so the script appears only in the private presenter view. The presenter PDF includes private script text, so send `defense-committee.pdf` to the committee; it carries no script or notes.

Before the defense, rehearse a Zoom screen share and check its audience view, script readability, next/previous navigation, and both videos. Build and file checks can verify the pairings and media paths; playback and screen capture depend on the presentation computer. Pympress setup and media support: https://pympress.github.io/README.html. Zoom window sharing: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0060596.

The grouped presenter PDF labels its script pages `script:1`, `script:2`, etc. Keep this prefix when changing the builder: Pympress reserves `notes:` for a different layout with each script page immediately following its slide. Using `notes:` for the grouped PDF makes startup select that incompatible layout and leaves the script pane empty, even when launched with `--notes=after`. After replacing an older presenter PDF, close both Pympress windows and reopen the rebuilt file with the command above.
