# Cup movie (slide 2)

`cup_tripanel.mp4`, `poster_*.png`, `metadata.json`, and `causal_validation.json` come from
`monocular_reconstruction/artifacts/defense_cup_movie_20261121/make_tripanel.py`; `metadata.json`
records the sources, clock alignment, causal reconstruction configuration, and hashes.

`frames/frame-0.jpg` … `frame-89.jpg` are every second movie frame (odd frames 1, 3, …, 179),
used by the audience PDF's `animate` build at 12 frames/s, so the loop keeps the movie's 7.5 s
duration. `frames/frame-12.jpg` is movie frame 25, the same image as `poster_impact.png`
(+4.1 ms from impact), and is the PDF poster. The presenter edition links the MP4 directly.

```bash
ffmpeg -nostdin -i cup_tripanel.mp4 -vf "select='mod(n\,2)'" -vsync vfr -q:v 3 -start_number 0 frames/frame-%d.jpg
```
