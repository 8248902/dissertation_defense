# Relevant work and contribution boundaries

The main talk positions the dissertation against the following directly related methods. Slide 4 gives the overview; the temporal comparison and flow theorem develop the distinctions. The literature backup provides references for questions.

## Henri Rebecq, René Ranftl, Vladlen Koltun, and Davide Scaramuzza (2019)

[Events-to-Video: Bringing Modern Computer Vision to Event Cameras](https://openaccess.thecvf.com/content_CVPR_2019/papers/Rebecq_Events-To-Video_Bringing_Modern_Computer_Vision_to_Event_Cameras_CVPR_2019_paper.pdf).

Reconstructs video from an event stream with a recurrent neural network trained on simulated event data.

Learned event-only inference. Do not classify it as requiring synchronous frames at inference, or claim a benchmark advantage over it from the dissertation tables.

Dissertation bibliography key: `rebecq2019events`.

## Zelin Zhang, Anthony Yezzi, and Guillermo Gallego (2023)

[Formulating Event-Based Image Reconstruction as a Linear Inverse Problem With Deep Regularization Using Optical Flow](https://arxiv.org/abs/2112.06242).

Uses optical flow and warped events to form a linear brightness inverse problem, solved with classical or learning-based regularization.

This is an event-based inverse reconstruction approach, not a frame-assisted category. Use journal year 2023; the local key retains the 2021 preprint year. Our comparison concerns per-pixel temporal modeling versus flow-based spatial reconstruction, not who first posed a linear inverse problem.

Dissertation bibliography key: `zhang2021formulating`.

## Harbir Antil and David Sayre (2023)

[Bilevel inverse problems in neuromorphic imaging](https://arxiv.org/pdf/2302.02052).

Combines conventional frames with events in a bilevel reconstruction; the outer variable contains event-threshold parameters and the lower problem is a regularized temporal least-squares solve.

Their paper already proves existence and develops second-order sufficient conditions. Our fixed positive diagonal theorem analyzes a different event-only quadratic model. Do not describe their outer variable as a learned regularization weight. Do not call their per-pixel temporal model spatially coupled merely because it uses frames.

Dissertation bibliography key: `HAntil_DSayre_2023a`.

## Berthold K. P. Horn and Brian G. Schunck (1981)

[Determining Optical Flow](https://people.csail.mit.edu/bkph/papers/Optical_Flow_OPT.pdf).

Combines a brightness-constancy data residual with quadratic spatial smoothness of the velocity field.

Credit the data-plus-smoothness variational structure to this work. The dissertation supplies event-derived coefficient models and the specified common analysis.

Dissertation bibliography key: `horn1981determining`.

## Ryad Benosman, Charles Clercq, Xavier Lagorce, Sio-Hoi Ieng, and Chiara Bartolozzi (2014)

[Event-Based Visual Flow](https://doi.org/10.1109/TNNLS.2013.2273537).

Estimates visual flow from the local differential geometry of the spatiotemporal surface formed by event timestamps.

Use timestamp geometry as the attribution. Keep the ideal single-crossing assumptions and normal/tangential ambiguity explicit when presenting the dissertation time-surface constraint.

Dissertation bibliography key: `benosman2014event`.

## Joachim Weickert and Christoph Schnörr (2001)

[A Theoretical Framework for Convex Regularizers in PDE-Based Computation of Image Motion](https://link.springer.com/article/10.1023/A:1013614317973).

Classical variational flow already has well-posedness theory. This dissertation organizes the event-derived coefficient constructions and supplies explicit identifiability and perturbation hypotheses for its family.

Dissertation bibliography key: `weickert2001theoretical`.

## Edward H. Adelson and J. Anthony Movshon (1982)

[Phenomenal Coherence of Moving Visual Patterns](https://doi.org/10.1038/300523a0). *Nature* 300, 523–525.

Introduced the velocity-space intersection-of-constraints construction: each oriented component allows a line of velocities, and two orientations intersect at one. Slide 21 uses this picture to illustrate the integrated-identifiability requirement of the main flow theorem; the theorem itself is the dissertation's.

Not in the dissertation bibliography; credited on slide 21 only.

## Published temporal work

Harbir Antil, Daniel Blauvelt, and David Sayre (2026). [Dynamic reconstruction from neuromorphic data](https://doi.org/10.3934/fods.2026017).

The chapter footnote attributes bump-function and adaptive-regularization development/analysis, the continuous-time ODE connection, existence/uniqueness/stability derivations, and experimental validation to Daniel Blauvelt.

## Positioning in the talk

The temporal contribution is a per-pixel event-increment model with kernel representations, activity-based penalties, and explicit fixed-weight analysis. Prior event-only and inverse reconstruction methods remain credited. The flow contribution organizes three event-derived coefficient constructions under a common quadratic analysis with explicit integrated identifiability and perturbation hypotheses. Classical quadratic flow already has well-posedness theory. Stereo extends the temporal model through soft coupling and separates inner solvability from correspondence selection.
