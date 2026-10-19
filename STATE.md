# Defense presentation — current state

Updated October 19, 2026. **Canonical location: `../dissertation_defense`, branch `main`.** The Opus route is now the actual defense. Continue all deck, notes, script, and strategy work here.

## Current deliverables

- `defense.pdf`: 88 pages, consisting of 35 main slides and 53 backups.
- `defense-notes.pdf`: matching 88-page speaker edition.
- `defense-script.md` and `defense-script.pdf`: the editable rehearsal script and its 91-page rendering (cover, two indexes, one page per deck frame). Main talk is about 6,000 spoken words (roughly 6,100 after the slide 2 and 7 updates), approximately 48–55 minutes at 110–125 words per minute, plus pauses and questions. Backups are outside this timing.
- `strategy.md`: selected route, time priorities, and backup navigation.
- `delivery-guide.txt`: practical delivery and build instructions.
- `related-work.md`: precise comparisons, primary references, and contribution boundaries.

The main talk opens with the outline on slide 3 and concise relevant-work positioning on slide 4. Event-camera behavior follows on slides 5–8, temporal reconstruction on 9–19, optical flow on 20–29, stereo on 30–31, and conclusions on 32–35. Literature backup is deck page 62; the formal aperture explanation is page 88. The matched indoor reconstruction example is now slide 16. Slide 20 embeds the credited Sinauer aperture sequences; `aperture-demo.html` is the offline browser alternative. Breadcrumbs identify the current topic, and the author appears on the title slide.

The new relevant-work slide distinguishes learned event-only reconstruction, flow-based image reconstruction, and frame-assisted bilevel reconstruction. It credits classical optical-flow regularization and well-posedness theory. The contribution is the particular event-derived models and their common analysis, with explicit author contribution for the published temporal work. Speaker notes, script, and expanded literature backup agree on these distinctions.

## Optimization explanation — October 18

Slides 12 and 28 now connect the optimization problems to their computation. Slide 12 follows the objective through normal equations, independent numerical pixel solves, and parallel assembly of temporal profiles into frames. The solver organization was checked against `monocular_reconstruction/src/core/lat_image_af_with_lambda.m` and `lat_image_af.m`; the presentation makes no specialized-factorization claim. Slide 28 shows the simultaneous block-Jacobi update, explains its local two-component solve and use of the previous neighbor field, and retains all graph and sampled-information hypotheses. Spectral proof details remain in speaker notes and backup. The corresponding full script sections match. Slide titles and counts are unchanged.

## Readable dissertation references — October 18

Main and backup footers now use actual `\ref*` / `\pageref*` values imported through `xr`, rendered via `\dref` and `\drefpage`. They show named, numbered results (for example, Theorem 2.2.5 and Theorem 3.6.1); unnumbered topics use their names and page numbers. The old `sec:irls_scope` key was replaced by the existing specific results and sections relevant to those slides. Internal keys remain in source and metadata for maintenance.

The reference snapshot comes from the complete current 208-page dissertation build in `/tmp/udts_recheck.NFS9fQ/build`, which passed 35 formatting rules with zero warnings/failures. A stray prose paste inside the `pan2019bringing` BibTeX entry was removed to restore compilation; the author's other thesis edits were preserved. The snapshot records 297 labels and 147 thesis input hashes. Missing labels and stale source hashes stop the defense build with refresh instructions. README documents the reference-update workflow.

## Scene-terms framing — October 19

Each approach now has a plain-language summary of what it models, folded into existing slides (no new frames): temporal on slide 9, flow on slide 20's script and slide 24's table (new "Edge measurement from" column), stereo on slide 30. Proof and result slides 12, 13, 14, 15, 21, 25, 26, 27, 28, and 31 carry short "In scene terms" glosses (e.g., mean = common drift/camera pan, m = how well edges cover every direction, |∇T| = edge slowness, one noise event gives ‖δy‖ ≤ 1). Speaker notes carry matching cues. In the script, each gloss that replaced a sentence keeps the original as "(Replaces: …)" for the presenter's reference; that text is not spoken. Main talk rose from 5,490 to 6,019 spoken words (counting excludes stage directions and Replaces text), over the 45–50 minute target; the trims already named in strategy.md (slides 28, 19, 22) are the user's call.

## Three estimated outputs — October 19

Slide 7 now uses the transferred HPC estimates from MVSEC indoor_flying2 near 47.6 s: B-spline temporal reconstruction, CMAX flow displayed at event-active pixels, and WLS stereo depth. Its title is “From events to images, motion, and depth.” All panels are estimates. The panels are labeled by chapter only, so the slide presents the three estimation targets. The method names (B-spline kernel, contrast maximization, WLS) appear only in the speaker notes and as a script stage direction for questions; the stage direction notes that contrast maximization lies outside the quadratic family covered by the central flow theorem. The slide has display keys, and notes explain the different task windows, stereo rectification, and white-pixel masks. Original image bytes and HPC metadata are preserved under figures/indoor_flying2_t47p6. The script section matches.

Slide 2 uses the corrected, timestamped outdoor_day1 release triptych from the full defense_mvsec_20261019 bundle, preserved under figures/mvsec_outdoor_day1/defense_matched with metadata.json. The event display is a 50 ms sample ending at the reconstruction target; blue denotes positive-only pixels, orange negative-only, and purple both polarities. The reference is 4.672 ms later. The reconstruction uses the full saved 500,000-event interval, while the display shows a short sample. Full-bundle provenance revealed that the old frame_012 reference and reconstruction used different temporal grids, so both were replaced. The pending-metadata limitation from the partial transfer is resolved; no estimator rerun was needed.

## User decisions to preserve

Treat existing numerical and analytical results as established. Keep precise hypotheses, empirical scope, and conditional convergence assumptions; keep internal audit history and pending-verification language out of the audience deck and spoken script. Refer listeners to the dissertation for supporting detail when appropriate. Backup answers are self-contained responses for questions, rather than planned main-talk transitions.

The advisor permits a selective defense, with confidence in the material taking priority over covering every dissertation chapter. The selected route emphasizes published temporal reconstruction and the central flow theorem; stereo remains brief. Avoid broad novelty claims and do not describe event-only prior methods as frame-assisted.

## Build and verification

Run `make check`, then `make all` after content changes. The latter rebuilds all three PDFs, writes a dated `validation.json`, and refreshes `source-map.csv` and `source-snapshot.sha256`. Scratch files remain under `/tmp`. The script uses Markdown as its only prose source and checks all titles, deck pages, and one-page-per-frame sections. The source map uses current source lines and readable references from `thesis-references.json`. Normal builds validate that snapshot against the sibling thesis. After thesis edits, run the formatting build, `make refs THESIS_BUILD=/path/to/fresh/build`, and `make all`; see README. A standalone defense uses its bundled snapshot.

October 18 final build: audience 88 pages, notes 88 pages, script 91 pages; no build/layout/reference warnings. All 88 script sections match the deck. Metadata covers 88 frames and all 42 referenced figure assets, including 14 animation frames. The current source manifest contains 67 hashes. Primary-source attribution and new slide layouts were reviewed. `validation.json` records build checks; historical committee mathematical reviews are kept separately.

The defense-scoped numerical-source and figure-reference CI checks pass. The umbrella check still reports four source-comment issues in `dissertation_proof_reference_2026-10-10` and figure paths in historical proposal/snapshot documents and `optical-flow-manuscript`; these pre-existing portfolio issues are outside the active defense.

## Consolidation and history

The selected candidate was preserved at commit `1746292` on historical branch `candidate/advisor-split-opus` before promotion. Its separate worktree has been retired. Earlier main corrections were already present in the selected source and were retained.

These folders are frozen history, not active editing destinations:

- `../misc_ideas_feedback/_archive/defense_candidate_opus_2026-10-16/`
- `../misc_ideas_feedback/_archive/defense_strategy_2026-10-16/`
- `history/committee-review-2026-10-03/`

Earlier defense history, before the October 15 split into a sibling submodule, is in `dissertation_thesis` through commit `6cb17bd`. The selected route, notes, figures, animations, script, and supporting strategy now live together here. Local commits preserve this consolidation; no remote push was requested. The umbrella repository has unrelated existing changes; its canonical defense gitlink update remains uncommitted until the submodule is pushed under the portfolio workflow.

## MP4 playback and synchronized Zoom presenter — October 19

Created H.264/yuv420p `figures/aperture/app5-hide.mp4` and `app6-show.mp4`, preserving 500 by 218 dimensions, the original 1.4-second cycle, and 200 ms holds per source image. Original GIFs remain intact. The MP4s also open directly in media players.

For the user's Linux/two-monitor Zoom setup, `make presenter` now builds `defense-presenter.pdf`: all 88 audience slides followed by 88 complete script pages, paired for `pympress --notes=after defense-presenter.pdf`. The script's introduction/index pages are excluded using compiled page labels, and all retained script text is verified. Advance slides from Pympress's private presenter window; Zoom shares only its audience window. Slide 20 in this optional edition uses two linked looping MP4 panels. Keep their relative paths when moving the PDF. The normal audience/notes/script builds retain their existing presentation behavior.

README.md and delivery-guide.txt include Ubuntu installation, rebuild, launch, screen sharing, and video instructions. The presenter builder requires pypdf in its selected Python environment; Ubuntu's system Python can use python3-pypdf (`make presenter PYTHON=/usr/bin/python3`). Normal make check/make all passed; normal PDFs remain 88/88/91 pages with zero compile warnings, and the presenter has 176 pages. All 88 script pairings, two looping media annotations, paths, and panel rectangles passed structural checks. Parent visually checked the aperture slide and script page. Pympress/Zoom GUI playback remains a rehearsal check on the presentation computer; no GUI packages were installed during this session. Broader portfolio CI reports existing unrelated proof/archive/other-manuscript issues.

## Presenter script visibility correction — October 19

The user's Pympress 1.8.4 run exposed a startup-mode conflict in the initial presenter PDF: its grouped script pages used the reserved `notes:` label prefix, which makes Pympress select an adjacent-slide/notes mapping during startup, overriding the earlier command-line setting. Reproduced the failure with the installed Pympress parser: 176 detected slides and zero valid script pairings.

Changed the grouped pages to `script:` labels and rebuilt defense-presenter.pdf. Validated through the installed Pympress Document API that auto-detection selects AFTER, reports exactly 88 audience slides, and maps all 88 to their matching full-script pages. Every parsed script page has nonempty text identical to the fresh script build; both MP4s resolve with repeat enabled. Updated README/delivery guide and source metadata. Close both existing Pympress windows, then reopen with `pympress --notes=after defense-presenter.pdf`; this clears the old instance's cached mode. N toggles notes mode in the presenter window. The runtime check used the real installed parser without opening GUI windows or changing user configuration. Scratch build and evidence: /tmp/defense-presenter-notes-fix.
