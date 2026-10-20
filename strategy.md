# Defense strategy

The active presentation develops temporal reconstruction in depth, then the central optical-flow theorem and proof, followed by a brief stereo summary and research directions.

The advisor's guidance is to select material the presenter feels confident discussing; the defense can cover a subset of the dissertation. The published temporal work anchors the talk. The common question is what the observations determine and what the model supplies.

## Main route

| Deck pages | Topic | Purpose |
|---|---|---|
| 1–4 | Motivation, outline, relevant work | State the question and distinguish prior approaches from the dissertation's contribution. |
| 5–8 | Sensor and data representations | Explain event generation, outputs, and the modeling step before equations. |
| 9–19 | Temporal reconstruction | Develop the model, the sensor-to-observation identity (slide 11), proof, spectral interpretation, weighting, comparisons, real-data examples, and the shared-scene (ESAR) bridge. |
| 20–28 | Optical flow | Explain aperture ambiguity, the flow model in scene terms with the two-orientation requirement, and the three representations, then the unified theorem, a one-slide proof idea (stability in backup), and known-motion examples. |
| 29–30 | Stereo depth | Explain the geometry, the coupled model with its frozen-weight unique inner solve, and the MVSEC benchmark of the full method. Correspondence selection and IRLS stay in backup. |
| 31–33 | Contributions and next questions | Three-row synthesis (what the data constrain, what the models prove), three research directions, close. |

The outline and footer use the same five stages: Sensor and data, Reconstruction, Optical flow, Stereo depth, Conclusions. The author's name appears on the title slide. Backup pages carry their actual deck page number.

## Timing and rehearsal

The main script has about 5,750 spoken words, approximately 46–52 minutes at 110–125 words per minute before pauses and questions. The October 19 rehearsal of the earlier 6,450-word version took 51 minutes (about 126 wpm), which puts the current version near 45 minutes. Rehearsal determines the actual duration. The advisor's approximate 30-minute expectation for the introduction, data modeling, and monocular reconstruction concerns that part of the talk, not a requirement to cover every chapter.

Protect the temporal formulation and proof, the integrated-information interpretation, and the mean/fluctuation proof idea (slide 27). The discrete-flow slide and the full proof and stability derivations moved to backup on October 19. On October 20 the distributional IVP (now Backup 03 only) gave way to the sensor-to-observation slide 11, the stability bound left slide 27, and the two future-work slides merged without CFD. If rehearsal still runs long, the next candidate is the voxel derivation on page 23; slide 25 cites it, and slide 32 cites slides 11 and 19. Retain the brief prior-work positioning so the audience can distinguish established ingredients from the dissertation's contribution.

## Relevant work

The early comparison covers learned event-only reconstruction (Rebecq et al.), flow-based linear inverse reconstruction (Zhang, Yezzi, and Gallego), and frame-assisted bilevel reconstruction (Antil–Sayre). The flow discussion credits Horn–Schunck, Benosman's timestamp geometry, and Weickert–Schnörr's classical well-posedness theory. Full references and comparison boundaries are in [related-work.md](related-work.md).

The intended claims concern the specified models and analyses. They distinguish the event-derived formulations and their consequences while crediting established regularization, flow models, and proof tools. The temporal comparison uses different input information across methods. The stereo benchmark reports each method's own scored population alongside accuracy.

## Questions and deeper explanations

Pages 34–101 contain the backup slides; pages 102–104 are the reference list, numbered as in the dissertation. Their independent script responses begin with a likely question, give a complete spoken answer, and then develop a deeper follow-up. The three navigation slides and three reference pages have private cues. Follow the question rather than presenting the backup as another planned section.

Moved from the main talk on October 19: full flow proof page 42; stability derivation page 43; discrete flow page 44 (next to Jacobi convergence, page 45); Chapter 4 results summary page 81. Other recent backups: metric computations page 39; real-time reconstruction page 40; controlled-flow protocol page 77; stereo alignment page 82; disparity-to-depth sensitivity page 90.

Useful anchors: temporal uniqueness page 35; natural boundary condition page 41; Jacobi convergence page 45; stereo cost geometry page 51; reciprocal IRLS proof page 53; evaluation populations page 56; mathematical contribution page 64; literature page 65; contrast maximization (what it models, evidence) page 76; full stereo arc pages 80–95; formal aperture model page 96; complementarity lemma page 97; adaptive-weight stability page 98; parameter choice page 99; learned estimators page 100; spline coercivity page 101; references pages 102–104.

Keep the hypotheses with the corresponding claim: fixed positive penalties for the temporal solve; integrated directional information for unrestricted quadratic flow; a finite candidate set and margin for selection stability; the sufficient contraction condition for IRLS convergence. The reported empirical results are established results, and the spoken material contains no audit or pending-verification commentary.
