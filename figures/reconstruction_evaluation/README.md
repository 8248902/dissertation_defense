# Slide 16: indoor event-only reconstruction

Use `reference.png` and `event_only_reconstruction.png` as separate native
346 × 260 panels in LaTeX. `preview.png` is for inspection. The selected
MVSEC indoor_flying2 frame shows the patterned panel, barrel rings, and floor
markers more clearly than the previously suggested indoor_flying3 B-spline
example. This is a qualitative display choice, not a claim that the method is
more accurate across a dataset.

The reconstruction comes from saved release run `indoor_flying2_bump_05`,
zero-based solved frame 80: event-only Gaussian temporal kernel with sigma
50 ms and sigmoid regularization. The nearest actual left-camera reference
frame is 2.577 ms later. The reference was not an estimator input. Neither
estimator nor display normalization was changed for this export. See
`metadata.json` for exact times, normalization, source paths, and hashes.

Reexport with Python 3, NumPy, h5py, and Pillow:

```sh
python artifacts/defense_mvsec_20261019/slide16_indoor_gaussian50/export.py
```

This requires the saved release under `/scratch/dblauvel/ch2_mvsec_release_20261018`.
The PNGs and metadata are self-contained for transfer. The existing indoor
aggregate table on slide 16 is a separate historical summary and should not
be described as a score for this frame. On slide integration, update the
scene and method label to `MVSEC indoor_flying2; event-only Gaussian 50 ms`.
