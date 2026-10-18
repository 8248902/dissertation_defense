# Defense presentation — current state

Updated October 18, 2026. **Canonical location: `../dissertation_defense`, branch `main`.** The Opus route is now the actual defense. Continue all deck, notes, script, and strategy work here.

## Current deliverables

- `defense.pdf`: 88 pages, consisting of 35 main slides and 53 backups.
- `defense-notes.pdf`: matching 88-page speaker edition.
- `defense-script.md` and `defense-script.pdf`: the editable rehearsal script and its 91-page rendering (cover, two indexes, one page per deck frame). Main talk is about 5,400 spoken words, approximately 43–49 minutes at 110–125 words per minute, plus pauses and questions. Backups are outside this timing.
- `strategy.md`: selected route, time priorities, and backup navigation.
- `delivery-guide.txt`: practical delivery and build instructions.
- `related-work.md`: precise comparisons, primary references, and contribution boundaries.

The main talk opens with the outline on slide 3 and concise relevant-work positioning on slide 4. Event-camera behavior follows on slides 5–8, temporal reconstruction on 9–19, optical flow on 20–29, stereo on 30–31, and conclusions on 32–35. Literature backup is deck page 62; the formal aperture explanation is page 88. The matched indoor reconstruction example is now slide 16. Slide 20 embeds the credited Sinauer aperture sequences; `aperture-demo.html` is the offline browser alternative. Breadcrumbs identify the current topic, and the author appears on the title slide.

The new relevant-work slide distinguishes learned event-only reconstruction, flow-based image reconstruction, and frame-assisted bilevel reconstruction. It credits classical optical-flow regularization and well-posedness theory. The contribution is the particular event-derived models and their common analysis, with explicit author contribution for the published temporal work. Speaker notes, script, and expanded literature backup agree on these distinctions.

## User decisions to preserve

Treat existing numerical and analytical results as established. Keep precise hypotheses, empirical scope, and conditional convergence assumptions; keep internal audit history and pending-verification language out of the audience deck and spoken script. Refer listeners to the dissertation for supporting detail when appropriate. Backup answers are self-contained responses for questions, rather than planned main-talk transitions.

The advisor permits a selective defense, with confidence in the material taking priority over covering every dissertation chapter. The selected route emphasizes published temporal reconstruction and the central flow theorem; stereo remains brief. Avoid broad novelty claims and do not describe event-only prior methods as frame-assisted.

## Build and verification

Run `make check`, then `make all` after content changes. The latter rebuilds all three PDFs, writes a dated `validation.json`, and refreshes `source-map.csv` and `source-snapshot.sha256`. Scratch files remain under `/tmp`. The script uses Markdown as its only prose source and checks all titles, deck pages, and one-page-per-frame sections. The source map uses current source lines; compiled dissertation label numbers are populated only when an explicit current thesis build is supplied to `update_metadata.py --thesis-build`.

October 18 final build: audience 88 pages, notes 88 pages, script 91 pages; no build/layout/reference warnings. All 88 script sections match the deck. Metadata covers 88 frames and all 42 referenced figure assets, including 14 animation frames. Primary-source attribution and new slide layouts were reviewed. `validation.json` records build checks; historical committee mathematical reviews are kept separately.

The defense-scoped numerical-source and figure-reference CI checks pass. The umbrella check still reports four source-comment issues in `dissertation_proof_reference_2026-10-10` and figure paths in historical proposal/snapshot documents and `optical-flow-manuscript`; these pre-existing portfolio issues are outside the active defense.

## Consolidation and history

The selected candidate was preserved at commit `1746292` on historical branch `candidate/advisor-split-opus` before promotion. Its separate worktree has been retired. Earlier main corrections were already present in the selected source and were retained.

These folders are frozen history, not active editing destinations:

- `../misc_ideas_feedback/_archive/defense_candidate_opus_2026-10-16/`
- `../misc_ideas_feedback/_archive/defense_strategy_2026-10-16/`
- `history/committee-review-2026-10-03/`

Earlier defense history, before the October 15 split into a sibling submodule, is in `dissertation_thesis` through commit `6cb17bd`. The selected route, notes, figures, animations, script, and supporting strategy now live together here. Local commits preserve this consolidation; no remote push was requested. The umbrella repository has unrelated existing changes; its canonical defense gitlink update remains uncommitted until the submodule is pushed under the portfolio workflow.
