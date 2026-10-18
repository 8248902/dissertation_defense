# Defense strategy

The active presentation develops temporal reconstruction in depth, then the central optical-flow theorem and proof, followed by a brief stereo summary and research directions. This is the selected route formerly developed as the Opus candidate. Its sources and supporting documents now live only in this repository.

The advisor's guidance is to select material the presenter feels confident discussing; the defense can cover a subset of the dissertation. The published temporal work anchors the talk. The common question is what the observations determine and what the model supplies.

## Main route

| Deck pages | Topic | Purpose |
|---|---|---|
| 1–4 | Motivation, outline, relevant work | State the question and distinguish prior approaches from the dissertation's contribution. |
| 5–8 | Sensor and data representations | Explain event generation, outputs, and the modeling step before equations. |
| 9–19 | Temporal reconstruction | Develop the model, proof, spectral interpretation, weighting, comparisons, and real-data examples. |
| 20–29 | Optical flow | Explain aperture ambiguity and the three representations, then the unified theorem, proof, stability, and examples. |
| 30–31 | Stereo depth | Explain the geometry and distinguish a unique inner reconstruction from a correct correspondence. |
| 32–35 | Contributions and next questions | State the established results and research directions. |

The outline and footer use the same five stages: Sensor and data, Reconstruction, Optical flow, Stereo depth, Conclusions. The author's name appears on the title slide. Backup pages carry their actual deck page number.

## Timing and rehearsal

The main script has about 5,400 spoken words, approximately 43–49 minutes at 110–125 words per minute before pauses and questions. This is an estimate from the text; rehearsal determines the actual duration. The advisor's approximate 30-minute expectation for the introduction, data modeling, and monocular reconstruction concerns that part of the talk, not a requirement to cover every chapter.

Protect the temporal formulation and proof, the integrated-information interpretation, and the mean/fluctuation proof. If rehearsal runs long, first shorten the discrete-flow discussion on page 28, the shared-scene extension on page 19, and the voxel derivation on page 22. Retain the brief prior-work positioning so the audience can distinguish established ingredients from the dissertation's contribution.

## Relevant work

The early comparison covers learned event-only reconstruction (Rebecq et al.), flow-based linear inverse reconstruction (Zhang, Yezzi, and Gallego), and frame-assisted bilevel reconstruction (Antil–Sayre). The flow discussion credits Horn–Schunck, Benosman's timestamp geometry, and Weickert–Schnörr's classical well-posedness theory. Full references and comparison boundaries are in [related-work.md](related-work.md).

The intended claims concern the specified models and analyses. They distinguish the event-derived formulations and their consequences while crediting established regularization, flow models, and proof tools. The temporal comparison uses different input information across methods. The stereo benchmark reports each method's own scored population alongside accuracy.

## Questions and deeper explanations

Pages 36–88 contain the backup slides. Their independent script responses begin with a likely question, give a complete spoken answer, and then develop a deeper follow-up. The three navigation slides have private cues. Follow the question rather than presenting the backup as another planned section.

Useful anchors: temporal uniqueness page 37; natural boundary condition page 41; Jacobi convergence page 42; stereo cost geometry page 48; reciprocal IRLS proof page 50; evaluation populations page 53; mathematical contribution page 61; literature page 62; full stereo arc pages 75–87; formal aperture model page 88.

Keep the hypotheses with the corresponding claim: fixed positive penalties for the temporal solve; integrated directional information for unrestricted quadratic flow; a finite candidate set and margin for selection stability; the sufficient contraction condition for IRLS convergence. The reported empirical results are established results, and the spoken material contains no audit or pending-verification commentary.
