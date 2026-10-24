# Defense presentation — current state

**Schedule: pre-defense October 22, 2026 (held); defense November 23, 2026.**

## Start here — handoff, October 24 (pare-down after the pre-defense)

**Pre-defense feedback (Oct 22):** the motivation was thin, the talk turned technical immediately, and the slides were packed. Löhner and Griva also asked about the computational cost and whether the method could run on low-power edge hardware.

**Deck:** 22 main slides + 85 backups (82 discussion, 3 references); defense.pdf has 107 pages. `make all` is clean apart from the 4 pt overfull on the discussion guide, which was already there. The plan and approved choices are in `../misc_ideas_feedback/defense_pare_down_2026-10-24/plan.md`. Everything is uncommitted.

- **New main order:**
  - title;
  - **hook** (old 18: office / cup / ISS, plus why event cameras and on-board use);
  - why an event camera, threshold crossings, three problems;
  - **"Three estimators, each well posed"** (replaces the route);
  - one pixel, kernels, observation identity;
  - **unique + stable** (old 12 + 13);
  - **"One tridiagonal solve per pixel"** (new: cost, streaming identity, laptop timings);
  - penalty spectrum;
  - **MVSEC comparison with Antil–Sayre bilevel** (old 16 images + 17 table);
  - ESAR;
  - aperture, invisible direction (bottom text halved), three representations, theorem (proof idea spoken in one sentence), known-motion examples;
  - **stereo** (old 29 + two-row 30 table);
  - research opportunities (four blocks, adding edge hardware);
  - **closing** (old 31 table + common question + thank you).
- **Moved to Backups 71–82 (pages 93–104):** old 2, 4, 8, 13, 15, 16, 22, 23, 24, 27, 30, 33. Their script sections are now backup answers. Backups 1–70 keep their numbers; references are now Backups 83–85.
- **Density:**
  - Takeaway boxes are removed from main slides except the closing one.
  - Main-slide source footers are hidden in the audience/notes/presenter decks; `\src` prints on backups and when `\DefenseCommittee` is defined, which the committee build sets.
  - Slide 16's hand-written source line follows the same rule.
- **Script:**
  - main talk about 4,600 spoken words (was about 6,570 by the same count), about 37–42 min at 110–125 wpm before pauses;
  - Backup 07 (real time) rewritten with measured numbers;
  - all "Backup N, page P" cues remapped (page = N + 22).
- **Anki:**
  - slide_titles.json retitled;
  - new key `tridiag`;
  - new cards T30 (core: cost) and T31 (follow-up: streaming); 125 cards (55 core).
- **Timings source:** `monocular_reconstruction/python/edge/README.md` (branch `feature/edge-tridiag`, uncommitted). Raspberry Pi 5 numbers are pending hardware.
- **Not changed:** strategy.md (historical slide numbers), committee-backups.txt (titles unchanged).

## Start here — handoff, October 20 (Anki gap pass)

Anki now has 119 cards (54 core, 65 follow-up); every content slide has at least one card (uncovered: title, route, overview, dividers, references). New: V41 (FE reading of the stencils), V42 (Jacobi rate, CG, multigrid), V43 core (why analyze the quadratic family; CMax AEE numbers), V44 (known-motion protocol), V45 (stripe normal flow 2.12 px off), V46 (particle velocimetry), V47 (pooled kurtosis), V48 (correlated timestamp errors), S21 core (stereo benchmark numbers), S22 (coverage numbers), S23 (weighting comparison), S24 (observation-perturbation margin), S25 (IRLS constant derivation), S26 (Gaussian evidence), S27 (global optimality by layer), X12 core (observation model / theorem / benchmark). Numbers added to the More fields of T23, V02, S01, S18, S19, X06; X07's bilevel sentence narrowed to the lower level; anchors `proofidea` (slide 27) and `stereomvsec` (slide 30). The HPC identifiability prompt is at `../misc_ideas_feedback/hpc_integrated_identifiability_prompt_2026-10-20.md` (handed off). Fixed the Q&A file's Q26 constant: q_inv has √ℓ in the denominator (Prop. 4.6.13).

## Start here — handoff, October 20 (probing Q&A pass)

**Deck:** 33 main slides + 73 backups. defense.pdf 106 pages. `make check`, `make all`, `make presenter PYTHON=/usr/bin/python3`, and the Anki rebuild (103 cards: 51 core, 52 follow-up) are clean, with zero overfull boxes. Uncommitted.

Reviewed `../misc_ideas_feedback/defense_probing_q&a.md` (37 questions) against the deck. All but two already had a backup; those two are new:
- Backup 69 (p. 102) "Weak regularization: a limit in time, the aperture line in space": the λ-independent baseline rule, the λ→0 minimum-weighted-norm limit (Ch. 2 states it), noise gain ≤ min{1/(2λ), 1/√g₁} with 1/√g₁ ≈ N_t/π (checked numerically, N_t = 10, 50, 200); flow coercivity constant ≤ α² when an event-free open set exists, and at α = 0 the time-surface minimizers are the aperture line. Flow statements are a short argument beyond the chapter.
- Backup 70 (p. 103) "Where there are no events, smoothness fills in harmonically": Laplace equation where B = b = 0, least-gradient fill-in, weak maximum principle sup_U|v| ≤ sup_Γ|v|. Short argument beyond the chapter.
- References moved to pp. 104–106 (Backups 71–73). Discussion guide links both under Flow analysis ("Anisotropy; λ,α→0; event-free regions").
- Script "if asked" cues: slide 13 (→ Backups 69, 65), slide 19 (figure uses smoothed TV; Prop. 2.4.1 covers the ridge), slide 26 (event-free regions, checking m on data, disconnected domains), Backup 35 (disconnected domain), Backup 64 (extending to fractional/TV regularizers), Backup 67 (bilevel well-posedness: compact weight box gives existence). Backup 67's "that outer problem is well defined" now says the outer problem has a well-defined, smooth lower level (script and note).
- Anki: T25 (Backup 65), T26, V37–V40, X09 (Backup 64), X10, X11. T25 and V39 (Jacobi theorem versus the solvers run) are core.
- Delivery guide: counts and pages refreshed, slide 23/26 order fixed, new QUESTION HANDLING section from the Q&A's Part VI.

## Start here — handoff, October 20 (FEM/spline coverage for Löhner)

**Deck:** 33 main slides + 71 backups. defense.pdf 104 pages. `make check`, `make all`, `make presenter PYTHON=/usr/bin/python3`, and the Anki rebuild (94 cards) are clean, with zero overfull boxes. Uncommitted.

- Backup 68 (p. 101) "The spline regularizer is uniformly coercive under refinement": partition of unity plus Jensen gives ‖u_h‖² ≤ h²‖c‖², so the 2ε/M ridge is a uniform L² penalty (Mh²/|Ω| = 1.20 at h = 8 px) and the regularizer is uniformly H¹-coercive; κ = O(h⁻²). This is a short argument beyond the chapter, checked numerically (largest 1D Gram eigenvalue / h = 0.981, 0.994, 1.000 for h = 8, 4, 2). The Backup 46 talk note and script now point to it. Guide link: "splines" under Flow analysis.
- References moved to pp. 102–104 (Backups 69–71).
- Script "If asked" answers: Backup 11 (pixel stencils are P1/Q1 FE stencils with nodal quadrature), Backup 12 (Jacobi rate 1 − O(N⁻²); why Jacobi; CG, SOR, multigrid), Backup 39 (event-based particle velocimetry), Backup 46 (uniform versus adaptive knots).
- Dissertation Ch. 1 line 52: "quadratic B-spline" corrected to "cubic B-spline" to match Prop. 3.5.1 and the code (order 3). Recheck 35/0/0.

## Start here — handoff, October 20 (parameter-choice and learned-estimator backups)

**Deck (superseded above):** 33 main slides + 70 backups. defense.pdf 103 pages; script 106; presenter 206; committee 43 (unchanged content). `make check`, `make all`, `make presenter PYTHON=/usr/bin/python3`, and the Anki rebuild are clean (zero overfull boxes). Uncommitted; the user commits and pushes.

- Backup 66 (p. 99) "How the parameters were chosen": grid sweeps in all three chapters, Antil–Sayre scalar weight versus adaptive diagonal Λ, theorems hold for every positive value, classical rules (discrepancy principle with Skellam noise level, L-curve, GCV; typed external citations) and bilevel learning as next steps.
- Backup 67 (p. 100) "Learned estimators face the same free directions": per-problem table of what the events leave free, the model-based choice, and the learned choice; bilevel combination; ISS/ballistics without training data. Talk note holds the spoken "why not a neural network?" answer; benchmark-accuracy concession is in "if asked for more" only (user: event vision has no agreed reconstruction standard, so do not volunteer it).
- References moved to pp. 101–103 (Backups 68–70). Existing "page 97/98" references unchanged. Discussion guide: "Contribution; parameters; learning" links.
- Slide 15 now says "Selected by grid sweeps, balancing image fidelity and conditioning"; its talk note and script match and point to Backup 66. Slide 4 talk note points to Backup 67.
- Anki: X06 (parameter choice) and X07 (learned estimators) follow-ups; 93 cards.
- Dissertation: three sourced sentences (Ch. 2 per-rule scale sweep; Ch. A.1.3 flow grid sweeps on MVSEC; Ch. 4 grid sweep of γ and latent count plus paired weighting comparison). Recheck 35/0/0 from `/tmp/udts_recheck.lr3fff`; `make refs` refreshed from it. "Optuna" appears only in source comments, at the user's request.

## Start here — handoff, October 20 (pre-defense revisions)

**Deck (superseded above):** 33 main slides + 68 backups. defense.pdf 101 pages; script 104; presenter 202. `make check`, `make all`, `make presenter PYTHON=/usr/bin/python3`, and the Anki rebuild are clean (zero overfull boxes). Uncommitted; the user commits and pushes.

Applied `../misc_ideas_feedback/pre-defense_review_recommendations_2026-10-20.md` (user-approved; choices: slide 23 keeps the derivation with a labeled assumption; future work keeps sensor modeling, learned regularization, ESAR):
- Slide 11 is now "From threshold crossings to an approximate observation": ideal-threshold approximation plus the Ch. 2 arbitrary-endpoint identity, with the B / overshoot / sub-threshold terms as underbraces. The distributional IVP is Backup 03 only.
- Slide 16: one line and one script sentence saying PSNR also scores the model-selected baseline. Script now says indoor flying three.
- Slide 2 script: the reconstruction uses a longer stretch than the 50 ms display.
- Slide 19: dissertation Fig. 2.10 (copied to figures/sar_synthetic/), caption names the smoothed-TV penalty, one operator equation; nullspace/ridge algebra moved to the talknote.
- Slide 23: transport equation in a "Modeling assumption" block.
- Slide 27: three displayed results (Poincaré, m, coercivity); stability bound moved to notes/script (Backup 10, p. 43).
- Slide 28 takeaway: checker reduces the aperture ambiguity; accuracy depends on representation and regularization.
- Slide 30: "Mathematical result" (fixed d, frozen weights) vs "Benchmark" (full WLS method) labels.
- Slide 31: "What the data constrain and what the models prove", a three-row table (CMax row and scoped results now backup-only; the p. 98 adaptive-weight link kept).
- Slides 32–33 merged into "Research opportunities" (three blocks, CFD and stereo-margin/adaptive-gap items removed; the fractional nonlocal penalty was dropped from the notes).
- All backup page references shifted by −1. Anki: slide_titles keys 11/33 retitled, key 34 removed, T07/T08 point to Backup 03, X03 rewritten, new core card T24 (slide 11). Main talk ≈5,750 spoken words (≈45 min at 126 wpm).

**Committee copy, October 20 (user-approved):** `make committee` (also part of `make all`) builds defense-committee.pdf: 33 main slides, the 7 backups named in committee-backups.txt (02 penalty positivity, 05 kernel results, 06 metrics, 33 bias–noise, 34 sub-threshold, 51 frozen stereo solve, 63 aperture model), and reference pages for only the works those slides cite (43 pages). The build fails if a kept slide links to an omitted one. defense.pdf stays the full presenting deck. Slide 31's adaptive-weight link was removed in both versions (temporal cell now "each fixed positive weight matrix, with perturbation bounds"); Backup 65 is a stage direction in the script. Slide 18 shows the office scene once, larger; cup/ISS keep gray + false-color pairs with a caption line.

## Start here — handoff, October 19 late evening

**Deck:** 34 main slides + 68 backups (65 discussion + 3 reference pages). defense.pdf 102 pages, notes 102, script 105 (cover, two indexes, one page per frame), presenter 204. Last full build clean (zero overfull boxes): `make check`, `make all`, `make presenter PYTHON=/usr/bin/python3` (default python lacks pypdf). Anki rebuilt with `/home/q/g/r/.venv/bin/python anki/build_deck.py`. The thesis reference snapshot (schema 2: labels plus citation numbers and `.bbl` entries) comes from `/tmp/udts_recheck.GDYNkk` (35 pass / 0 warn / 0 fail); `make refs` needs a build with its `.aux` and `.bbl`.

**Git:** last commit is `a3a0981`. Uncommitted: the October 20 citation work below. The user commits and pushes; do not commit unless asked.

**Citations, October 20 (user-approved approach):** slides cite with `\cite{key}` and print the dissertation's own bibliography numbers, linked to reference pages 100–102 (Backups 66–68), which are generated from the thesis `.bbl`. 38 works cited. Uncited named methods, datasets and theorems now carry citations (mostly in `\src` footers where inline tags caused wraps). External hrefs on slide 4 and the literature page became `\cite`; the URLs stay as `% link:` comments. Adelson–Movshon, Wolfe, Antil–Di–Khatri and Willert–Klinner are not in the thesis bibliography and remain typed text. Slide 16 footer/notes corrected from indoor flying 4 to indoor flying 3 (matches its images and metadata.json). The held fractional backup now goes before the reference frames.

**Restructure, October 19 late (user-approved; details in LOG/2026-10-19.md):**
- Goal: steer the defense toward results that are easy to defend. Rehearsal of the 36-slide version took 51 min.
- Slides 27 (mean/fluctuation proof) and 28 (stability) merged into new slide 27, "Proof idea: smoothness fixes variation, edges fix the drift": decomposition, Poincaré, m, coercivity + Lax–Milgram, and the stability bound. The originals are Backups 09–10 (pages 43–44).
- Slide 29 (discrete flow / block-Jacobi) moved to Backup 11 (page 45), next to the Jacobi proof (Backup 12, page 46).
- Old slide 32 (four Chapter 4 results) moved to Backup 48 (page 82), after the stereo arc divider. New slide 30, "Stereo on MVSEC: competitive accuracy, more scored points": the coupled energy, unique inner solve, and the MVSEC table (WLS + Piatkowska, Xie, Kogler, Rogister; ablation rows stay in Backup 60).
- Decided against putting preliminary MVSEC *flow* numbers in the main talk: they are absent from Chapter 3 (AEE ≈2–2.5 px, angular error 40–65° in optical-flow-manuscript/ev_hs_of.tex) and would invite benchmark probes.
- Main talk now ≈5,870 spoken words; at the rehearsal pace (~126 wpm) about 46 min.

**Theory backups, October 20 (user-approved):** Backup 64 (page 98, complementarity lemma) and Backup 65 (page 99, adaptive-weight local Lipschitz bound) are integrated, with discussion-guide links. The fractional H^s backup is held in `held/` (frame + script) and is excluded from every build until the user is ready; it is not in the copy sent to the committee. Slide 31's "adaptive-weight stability" cell and Backup 25's takeaway named Chapter 2 adaptive stability as open. Both now point to page 99 (user-approved October 20).

**Open items:**
1. Rehearse the new slides 27 and 30 and re-time the talk.
2. Done: the contrast-maximization column is off slide 28; Backup 45 has the "why the quadratic family" answer.
3. Offered, not taken: "one orientation / two orientations" tags on slide 28's rows, linking to slide 21's velocity diagram.
4. Slide 31's table still lists "scoped graph convergence" and the stereo selection results; both are now backup-only in the talk, which is consistent with a recap of what the dissertation proves.
5. The "finite-design bound" wording on the slide of the regression-radius backup (now Backup 15, page 49) stays (user decision); only the script was reworded.

**Conventions the user has set:**
- Mathematical correctness and clarity come first. Verify formulas against backup.tex/core.tex and the dissertation before rewording.
- Propose wording before editing prose; the user approves or adjusts. Use positive consequence framing, and avoid "pipeline".
- In the script, "(Replaces: …)" notes are unspoken presenter references. Keep them.
- Script headings must match deck frames exactly (`## Slide N — Title`, `## Backup N — Title`, `Deck page: N.`), and each frame's script must fit one page. `make check` enforces both.
- Every numerical claim in .tex needs a `% source:` comment within two lines. `../check-ci.sh` failures under `misc_ideas_feedback/…/before/` and `optical-flow-manuscript` are pre-existing archive issues.
- SAR = synthetic aperture radar (idea transferred to events, slide 19).

Updated October 19, 2026. **Canonical location: `../dissertation_defense`, branch `main`.** The Opus route is now the actual defense. Continue all deck, notes, script, and strategy work here.

## Current deliverables

- `anki/defense-core.apkg`: 48 essential spoken-recall cards; `anki/defense-oral.apkg`: the same core plus 42 deeper follow-ups. Prompts practice accessible explanations of results, proof mechanisms, assumptions, and consequences for this talk. Source-linked answers, editable card source, a browser preview, and import/rebuild instructions are under `anki/`; start with `anki/README.txt`.
The five reviewed backups are now integrated with their scripts and notes: metrics page 42, real-time reconstruction page 43, controlled-flow protocol page 77, stereo alignment page 81, and depth sensitivity page 89. Continue editing the active files here; the sibling draft package is a review record. The timed core and its current main-talk script were preserved.

- `defense.pdf`: 95 pages, consisting of 36 main slides and 59 backups.
- `defense-notes.pdf`: matching 95-page speaker edition.
- `defense-presenter.pdf`: 190 pages, pairing the 95 audience slides with their 95 full-script pages.
- `defense-script.md` and `defense-script.pdf`: the editable rehearsal script and its 98-page rendering (cover, two indexes, one page per deck frame). Main talk is about 6,450 spoken words after the October 19 spoken-delivery rewrite, approximately 52–59 minutes at 110–125 words per minute, plus pauses and questions. Backups are outside this timing.
- `strategy.md`: selected route, time priorities, and backup navigation.
- `delivery-guide.txt`: practical delivery and build instructions.
- `related-work.md`: precise comparisons, primary references, and contribution boundaries.

The main talk opens with the outline on slide 3 and concise relevant-work positioning on slide 4. Event-camera behavior follows on slides 5–8, temporal reconstruction on 9–19, optical flow on 20–30, stereo on 31–32, and conclusions on 33–36. Slide 21 states the flow model in scene terms with the edge diagram and a velocity-space intersection-of-constraints panel for the two-orientation requirement. Literature backup is deck page 65; the formal aperture explanation is page 95. Contrast maximization and its evaluation protocol occupy pages 76–79: the model and known-motion evidence, the controlled protocol, then the objective and existence proof. The matched indoor reconstruction example is now slide 16. Slide 20 embeds the credited Sinauer aperture sequences; `aperture-demo.html` is the offline browser alternative. Breadcrumbs identify the current topic, and the author appears on the title slide.

The new relevant-work slide distinguishes learned event-only reconstruction, flow-based image reconstruction, and frame-assisted bilevel reconstruction. It credits classical optical-flow regularization and well-posedness theory. The contribution is the particular event-derived models and their common analysis, with explicit author contribution for the published temporal work. Speaker notes, script, and expanded literature backup agree on these distinctions.

## Optimization explanation — October 18

Slides 12 and 28 now connect the optimization problems to their computation. Slide 12 follows the objective through normal equations, independent numerical pixel solves, and parallel assembly of temporal profiles into frames. The solver organization was checked against `monocular_reconstruction/src/core/lat_image_af_with_lambda.m` and `lat_image_af.m`; the presentation makes no specialized-factorization claim. Slide 28 shows the simultaneous block-Jacobi update, explains its local two-component solve and use of the previous neighbor field, and retains all graph and sampled-information hypotheses. Spectral proof details remain in speaker notes and backup. The corresponding full script sections match. Slide titles and counts are unchanged.

## Readable dissertation references — October 18

Main and backup footers now use actual `\ref*` / `\pageref*` values imported through `xr`, rendered via `\dref` and `\drefpage`. They show named, numbered results (for example, Theorem 2.2.5 and Theorem 3.6.1); unnumbered topics use their names and page numbers. The old `sec:irls_scope` key was replaced by the existing specific results and sections relevant to those slides. Internal keys remain in source and metadata for maintenance.

The reference snapshot comes from the complete current 208-page dissertation build in `/tmp/udts_recheck.NFS9fQ/build`, which passed 35 formatting rules with zero warnings/failures. A stray prose paste inside the `pan2019bringing` BibTeX entry was removed to restore compilation; the author's other thesis edits were preserved. The snapshot records 297 labels and 147 thesis input hashes. Missing labels and stale source hashes stop the defense build with refresh instructions. README documents the reference-update workflow.

## Scene-terms framing — October 19

Each approach now has a plain-language summary of what it models, folded into existing slides (no new frames): temporal on slide 9, flow on slide 20's script and slide 24's table (new "Edge measurement from" column), stereo on slide 30. Proof and result slides 12, 13, 14, 15, 21, 25, 26, 27, 28, and 31 carry short "In scene terms" glosses (e.g., mean = common drift/camera pan, m = how well edges cover every direction, |∇T| = edge slowness, one noise event gives ‖δy‖ ≤ 1). Speaker notes carry matching cues. In the script, each gloss that replaced a sentence keeps the original as "(Replaces: …)" for the presenter's reference; that text is not spoken. Main talk rose from 5,490 to 6,019 spoken words (counting excludes stage directions and Replaces text), over the 45–50 minute target; the trims already named in strategy.md (then slides 28, 19, 22; now 29, 19, 23 after the slide 21 split) are the user's call.

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

## Separate backup drafts from committee-question review — October 19

A review of the current main/backup deck against Chapters 2–4 produced five proposed backups: reconstruction metric interpretation; sensor timing versus batch output delay; controlled-flow evaluation protocol; stereo alignment after motion compensation; and disparity-to-depth sensitivity. Draft slides, notes, full responses, presenter followups, source map, and insertion rationale are preserved in `../misc_ideas_feedback/defense_backup_drafts_2026-10-19/README.md`. They are separate from the active presentation. The active deck and script were not edited by this review task; another agent was concurrently editing the script. Draft PDFs validate at 5 slides / 5 notes / 6 script pages with zero layout/reference warnings.

## Backup draft metric and live prototype revision — October 19

Updated the separate package at `../misc_ideas_feedback/defense_backup_drafts_2026-10-19/`: D1 script/notes now explain all nine metric computations without adding a slide. D2 now presents the author's September 2025 DAVIS346 live reconstruction prototype and historically reported 0.4–0.7 s MATLAB reconstructions / approximately one-second updates. Read-only inspection of `~/g/r/reconstruction_live_demo` confirmed windowed background processing and compiled CPU/CUDA DV modules. Historical timings, current settings, GPU projections, and camera-to-display delay remain distinguished. Revised draft PDFs: 5/5/6 pages, zero layout/reference warnings. Active deck/script and thesis source untouched; D3–D5 bodies/scripts and earlier user edits preserved.

## Correction to backup D2 native GPU inference account — October 19

Author clarified that live inference used the native GPU modules in iniVation DV, not MATLAB. This supersedes the preceding draft revision's MATLAB-centered account. Corrected D2 slide/script/notes in the separate package to show DV events → native C++ preparation → CUDA/cuSOLVER sparse solution → DV frame output, with CPU backend selection when CUDA is unavailable. Removed the separate MATLAB prototype's timing figures from the slide and spoken answer. Source tracing confirms the native module/dispatcher/CUDA engine/build target; the author's clarification establishes the implementation used. D1 and D3–D5 preserved, active deck/script untouched. Corrected PDFs5/5/6 pages, zero final layout/reference warnings; build `/tmp/defense-backup-draft-build-zqhamb1g`.

## Restore the real-time question for draft D2 — October 19

At the author's correction, D2 is again “Can the reconstruction run in real time?” Its purpose is real-time feasibility, supported by the author's established native GPU DV implementation, rather than questioning whether GPU implementation exists. The slide/script now explain live processing and the workload/temporal-detail/event-context/output-cadence tradeoff. GPU mechanics sit in followups. Revised separate drafts build5/5/6pages, zero final layout/reference warnings; `/tmp/defense-backup-draft-build-v_pilhxl`. Other drafts and active presentation/software sources unchanged.

## Five reviewed backups integrated — October 19

Merged the current user-edited draft slides, notes and responses into the active appendix at pages 42 (metrics), 43 (real-time reconstruction), 77 (controlled-flow protocol), 81 (stereo alignment), and 89 (depth sensitivity). Core source and current main-talk script are byte-for-byte preserved. Original backup titles are preserved; existing answers changed only for numbering and one CMAX navigation sentence. New sources use actual imported thesis numbers where applicable and a software-source footer for the live implementation. The discussion guide links directly to all five new pages. Standalone draft package is now a review record; continue edits here.

Final verification: make check passed; audience/notes/script95/95/98pages with zero compile warnings. Presenter190pages with95exact script pairings and two looping movies on main slide20. All95script sections fit one page,98used thesis labels resolve, all13validation input hashes and72source/figure hashes match. New slides, metric notes, and discussion guide visually reviewed; all five new PDF destinations checked. Scratch: `/tmp/defense-integrate-backups-2026-10-19/`. No thesis edits, commits, or pushes.
