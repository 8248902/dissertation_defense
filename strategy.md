# Defense strategy

The active presentation develops temporal reconstruction in depth, then the central optical-flow theorem and proof, followed by a brief stereo summary and research directions.

The advisor's guidance is to select material the presenter feels confident discussing; the defense can cover a subset of the dissertation. The published temporal work anchors the talk. The common question is what the observations determine and what the model supplies.

## Main route

| Deck pages | Topic | Purpose |
|---|---|---|
| 1–4 | Motivation, outline, relevant work | State the question and distinguish prior approaches from the dissertation's contribution. |
| 5–8 | Sensor and data representations | Explain event generation, outputs, and the modeling step before equations. |
| 9–19 | Temporal reconstruction | Develop the model, proof, spectral interpretation, weighting, comparisons, and real-data examples. |
| 20–28 | Optical flow | Explain aperture ambiguity, the flow model in scene terms with the two-orientation requirement, and the three representations, then the unified theorem, a one-slide proof idea with the stability bound, and known-motion examples. |
| 29–30 | Stereo depth | Explain the geometry, the coupled model with its unique inner solve, and the MVSEC benchmark. Correspondence selection and IRLS stay in backup. |
| 31–34 | Contributions and next questions | State the established results and research directions. |

The outline and footer use the same five stages: Sensor and data, Reconstruction, Optical flow, Stereo depth, Conclusions. The author's name appears on the title slide. Backup pages carry their actual deck page number.

## Timing and rehearsal

The main script has about 5,870 spoken words, approximately 47–53 minutes at 110–125 words per minute before pauses and questions. The October 19 rehearsal of the earlier 6,450-word version took 51 minutes (about 126 wpm), which puts the current version near 46 minutes. Rehearsal determines the actual duration. The advisor's approximate 30-minute expectation for the introduction, data modeling, and monocular reconstruction concerns that part of the talk, not a requirement to cover every chapter.

Protect the temporal formulation and proof, the integrated-information interpretation, and the mean/fluctuation proof idea (slide 27). The discrete-flow slide and the full proof and stability derivations moved to backup on October 19. If rehearsal still runs long, the next candidates are the shared-scene extension on page 19 and the voxel derivation on page 23; slide 25 cites the voxel derivation and slide 33 cites slide 19. Retain the brief prior-work positioning so the audience can distinguish established ingredients from the dissertation's contribution.

## Relevant work

The early comparison covers learned event-only reconstruction (Rebecq et al.), flow-based linear inverse reconstruction (Zhang, Yezzi, and Gallego), and frame-assisted bilevel reconstruction (Antil–Sayre). The flow discussion credits Horn–Schunck, Benosman's timestamp geometry, and Weickert–Schnörr's classical well-posedness theory. Full references and comparison boundaries are in [related-work.md](related-work.md).

The intended claims concern the specified models and analyses. They distinguish the event-derived formulations and their consequences while crediting established regularization, flow models, and proof tools. The temporal comparison uses different input information across methods. The stereo benchmark reports each method's own scored population alongside accuracy.

## Questions and deeper explanations

Pages 35–99 contain the backup slides. Their independent script responses begin with a likely question, give a complete spoken answer, and then develop a deeper follow-up. The three navigation slides have private cues. Follow the question rather than presenting the backup as another planned section.

Moved from the main talk on October 19: full flow proof page 43; stability derivation page 44; discrete flow page 45 (next to Jacobi convergence, page 46); Chapter 4 results summary page 82. Other recent backups: metric computations page 40; real-time reconstruction page 41; controlled-flow protocol page 78; stereo alignment page 83; disparity-to-depth sensitivity page 91.

Useful anchors: temporal uniqueness page 36; natural boundary condition page 42; Jacobi convergence page 46; stereo cost geometry page 52; reciprocal IRLS proof page 54; evaluation populations page 57; mathematical contribution page 65; literature page 66; contrast maximization (what it models, evidence) page 77; full stereo arc pages 81–96; formal aperture model page 97; complementarity lemma page 98; adaptive-weight stability page 99.

Keep the hypotheses with the corresponding claim: fixed positive penalties for the temporal solve; integrated directional information for unrestricted quadratic flow; a finite candidate set and margin for selection stability; the sufficient contraction condition for IRLS convergence. The reported empirical results are established results, and the spoken material contains no audit or pending-verification commentary.
