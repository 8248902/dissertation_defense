# Aperture demonstration assets

Source: Wolfe et al., *Sensation and Perception*, fourth edition, Activity 8.2, The Aperture Problem, Movies 5 and 6. Sinauer Associates, copyright 2015.

- `app5-hide.gif`: https://cdn.sinauer.com/wolfe4e/ch/08/act0802/app5-hide.gif
- `app6-show.gif`: https://cdn.sinauer.com/wolfe4e/ch/08/act0802/app6-show.gif
- Publisher explanation: https://cdn.sinauer.com/wolfe4e/wa08.02.html#Aperture

The original GIFs were downloaded October 18, 2026. Both contain seven 500 by 218 pixel frames, each lasting 200 milliseconds: five frames per second and a 1.4-second cycle. The source images are perceptual stimuli, distinct from event-camera measurements.

`app5-hide/frame-0.png` through `frame-6.png` and the corresponding `app6-show` sequence are lossless RGB PNG exports of every composited GIF frame. Conversion uses Pillow: open the GIF, seek each frame in order, convert the composited frame to RGB, and save as PNG. Full pixel dimensions, frame order, colors, and timing are retained. `masked.png` and `revealed.png` are the same first frames, retained for static use.

The audience PDF embeds both complete sequences with LaTeX `animate` at five frames per second. Playback starts with the panel's forward-play button; each sequence loops. Controls also allow reverse play and stopping at the first/last frame. Both use first-frame posters, so the comparison remains visible when printed or viewed statically. The notes edition uses the stills and omits the animation package. Playback needs no network connection; source links provide attribution rather than the playback mechanism.

PDF animation requires a compatible viewer with JavaScript enabled. The installed `animate` manual (2024-10-14, sections 1, 2, and 6.1) lists desktop Acrobat Reader, KDE Okular, PDF-XChange, Foxit Reader, Firefox version 130 or newer, and PDF.js version 4.4.168 or newer. Its `widget` method is used for broader viewer support. Chrome's PDF.js extension additionally requires active PDF content and local-file access to be enabled. Other viewers may show only the poster. Consult the [official package manual](https://mirrors.ibiblio.org/CTAN/macros/latex/contrib/animate/animate.pdf) for viewer-specific support.
