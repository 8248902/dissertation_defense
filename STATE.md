# Defense presentation — state

Status: delivered. Slides and speaker notes as presented to the committee on
2026-10-03, plus the verification records built alongside them.

## What is here

| File | Role |
|---|---|
| `defense.tex`, `core.tex`, `notes.tex` | Beamer deck; `core.tex` holds the slide content, `notes.tex` the speaker notes. |
| `backup.tex` | Backup slides held in reserve for questions. |
| `gmu-theme-trial.tex`, `mybeamertheme_light.sty`, `beamercolorthemeCMAI.sty` | Theme sources and the GMU/CMAI colors. |
| `Makefile` | `make` builds `defense.pdf` and `defense-notes.pdf` into `build/`. |
| `defense.pdf`, `defense-notes.pdf` | The delivered deck and the notes version; tracked deliberately. |
| `source-map.csv` | Every slide claim mapped to its dissertation source. |
| `source-snapshot.sha256`, `source-snapshot-2026-10-02.sha256` | Hashes of the dissertation sources the slides were checked against. |
| `validation.json`, `review-validation-2026-10-03.txt`, `math-review.txt`, `slide-audit.txt` | Verification records for the claims and the mathematics on the slides. |
| `delivery-guide.txt` | Timing and delivery notes. |
| `figures/` | The 18 images the slides include, copied from the dissertation at the move so the deck builds from this repository alone. |
| `update_metadata.py` | Refreshes `validation.json` and the source snapshot. |

## Provenance

This directory lived at `dissertation_thesis/defense/` until 2026-10-15, when it
became a sibling submodule of the `drafts` umbrella so that the dissertation
repository holds only what builds the dissertation. Its history before that date
is in the `dissertation_thesis` repository (the move point is commit `6cb17bd`,
and the state delivered to the committee is tag `committee-draft-2026-10-03`).

The remote `git@github.com:8248902/dissertation_defense.git` is recorded but does
not exist yet — create it before the first push.

The slides used to reach the dissertation's figures through `\graphicspath{{../}}`
and `../figures/...`, which only worked from inside the dissertation repository.
Both now resolve inside this one: `\graphicspath{{./}}` and `figures/...`, with
the images copied in. Refresh a copy from `../dissertation_thesis/figures/` if the
dissertation regenerates one.

## Keeping the slides and the dissertation consistent

The dissertation has changed since the defense: `dissertation_thesis` branch
`post-committee-minimal` reverts the post-defense restructuring back to what the
committee received, so slide claims recorded in `source-map.csv` still refer to
committee-era section and proposition numbers. Re-run `update_metadata.py` and
re-check `source-map.csv` against the dissertation before reusing these slides.
