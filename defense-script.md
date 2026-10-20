# Defense rehearsal script

Daniel Blauvelt • Canonical defense • Updated October 20, 2026

This rehearsal script covers all 33 main slides and all 68 backup slides. The main talk is a continuous spoken script. Each substantive backup slide has a likely committee question, a self-contained spoken answer, and a deeper follow-up. The three navigation slides and the three reference pages have silent navigation cues. Read ordinary paragraphs aloud; headings, questions, and bracketed italic directions organize rehearsal and are silent.

The main talk contains approximately 5,870 spoken words: about 47–53 minutes at 110–125 words per minute, before pauses and questions. Backup responses are outside that timing. Rehearse the main talk aloud to establish its actual length.

Slide 3 gives the five-stage outline. The footer highlights the current stage; backup footers show their deck page number. This script identifies each backup by its backup number and deck page. The clickable slide index and PDF bookmarks let you jump directly to a main slide or a backup response.

Slide 20 contains embedded animations with play controls. Playback has been checked in Firefox; desktop Acrobat Reader is also supported. Viewers without animation support show first-frame posters. The local aperture-demo.html remains an offline browser alternative.

# Main talk

## Slide 1 — Title

Thank you all for being here. My dissertation develops variational and optimization methods for event cameras, sensors that report only changes in brightness.

One question runs through the whole talk: if all we observe are changes, what can we recover? I'll answer it for three targets: an image, the motion in that image, and depth. Most of the time goes to reconstructing images over time. Then I'll present the main optical-flow result, give a short summary of stereo depth, and close with future directions.

*[Advance.]*

## Slide 2 — What can changes tell us about a scene?

*[Point to the reference image, the accumulated events, and the reconstruction.]*

On the left is an ordinary camera image of an outdoor scene; we keep it there to help recognize the scene. In the middle is a fifty-millisecond sample of the events from the same recording. Blue marks pixels that got brighter, orange pixels that got darker, and purple pixels that did both. On the right is our reconstruction, computed from a longer stretch of those events, a little under a second.

Each event says only that the brightness at one pixel changed at one moment. So the events record change and nothing else: they have no record of how bright anything is. To get from events to the image on the right, the model has to fill in what the events leave out, starting with a reference brightness level. Regularization makes that choice and balances it against fitting the data.

That is the theme of the talk. At each step, I'll separate what the observations determine from what the model chooses. Regularization can pick out a single answer. To know what that answer means, we need to know which parts came from the data and which came from the model.

Here's how the talk is organized.

## Slide 3 — The route through the talk

*[Follow the five stages from top to bottom.]*

We'll start with the sensor, and how its events become data that an estimator can use. Then comes the largest part of the talk: reconstructing an image over time, starting from a single pixel.

Next is optical flow, where spatial information helps pin down motion. I'll walk through the central theorem and its proof. After a brief summary of stereo depth, I'll finish with the contributions and the questions they open.

One question ties these stages together: what do the observations determine, and what does the model supply?

Before the sensor, let me place this work among the approaches it builds on.

## Slide 4 — Where this work fits

*[Compare the prior approaches with the dissertation contribution in each column.]*

For image reconstruction, Rebecq and colleagues train a recurrent neural network on simulated events. Zhang, Yezzi, and Gallego use optical flow to pose reconstruction as a linear inverse problem, with classical or learned regularization. Antil and Sayre combine events with conventional frames in a bilevel problem that estimates a parameter of the event-based blur kernel.

Our published temporal work reconstructs each pixel on its own from event increments. I develop the temporal kernel representation and the activity-based penalties, and then analyze the resulting quadratic solve: what the observations determine, how regularization picks the baseline, and how perturbations move the solution. That analysis shows where the reconstructed temporal structure comes from.

For flow, Horn and Schunck gave us the data-plus-smoothness formulation, and Benosman and colleagues developed the local geometry of event timestamps. Classical quadratic flow already has a well-posedness theory, for example from Weickert and Schnörr. What I add is one quadratic family that covers three ways of building coefficients from events, with explicit assumptions for when the motion is identified and how sensitive the estimate is to those coefficients.

Now to the sensor, and the observations these models use.

## Slide 5 — Why an event camera? Each pixel reports its own changes

*[Trace the moving bar through the two diagrams.]*

A conventional camera samples the whole image at fixed frame times. In the left diagram, each vertical column is one frame across all the pixels.

In an event camera, each pixel works on its own. When the leading edge of this bright bar reaches a pixel, the pixel gets brighter and fires a positive event. When the trailing edge passes, it gets darker and fires a negative event.

The output is a stream of locations, timestamps, and signs. That's why event displays tend to look like moving outlines. Under steady lighting, a pixel's brightness changes when a boundary crosses it. The inside of a uniform region produces little activity even while it moves, and so does a straight edge sliding along itself, because the local pattern stays the same. Changes in lighting trigger events too, since the sensor responds to any change in brightness over time.

Event sensors also have microsecond timing and high dynamic range, so they suit fast motion and difficult lighting.

For the mathematics, the key feature is that each pixel measures change relative to its own reference. Let me make that rule precise.

## Slide 6 — An event camera: each pixel reports threshold crossings

*[Follow the solid curve and point to one positive and one negative event.]*

The solid curve is the log intensity at one pixel. The dashed curve is the reference the pixel compares against.

When the log intensity rises one threshold above that reference, the pixel reports a positive event and resets its reference. A drop of one threshold gives a negative event. Every pixel resets on its own schedule, which is why event times are asynchronous.

The equation on the right states this ideal rule. An event carries a pixel location, a time, and a polarity, and the change since the last reset is the polarity times the threshold.

Now shift the whole log-intensity curve up by a constant. Every change stays the same, so the events stay the same. That's the first ambiguity in the talk: the events leave the baseline level free.

Real sensors add threshold variation and other errors. I use the ideal rule to motivate the observation model, and then pose reconstruction as a regularized fit to the data.

## Slide 7 — From events to images, motion, and depth

*[Indicate the three panels from left to right.]*

These three estimates come from the same indoor flight, at nearly the same moment. Each method uses its own observation window, and the depth estimate uses two cameras.

On the left is an image reconstructed by the temporal model. In the middle is optical flow, the apparent motion in the image plane. Color shows the direction and size of the motion wherever events occurred. On the right is depth from the two event cameras, with the color scale running from half a meter to eight meters.

Each problem has its own difficulty. For reconstruction, the brightness baseline is unknown. For flow, a local edge reveals the motion across it and leaves the motion along it free. For stereo, we have to decide which points in the two views are the same point in the scene.

Most of the talk goes to the temporal model and the main flow theorem. The stereo summary will show that an estimate can be well defined and still pick the wrong match.

*[If asked which methods produced these panels: a B-spline temporal kernel, contrast maximization, and weighted least squares. Contrast maximization has a nonconvex objective outside the quadratic flow family analyzed later; its existence result is in the backup.]*

## Slide 8 — A point measure needs a representation before optimization

We can write the raw event stream as a signed point measure: a point mass at each event's location and time, weighted by its polarity.

*[Follow the three boxes.]*

The quadratic models in this talk need quantities that can go into a residual, so first I convert the stream. Binning, smoothing, and interpolation do that.

For temporal reconstruction, kernels spread each event's contribution across reconstruction intervals. For flow, time surfaces and voxel grids supply the coefficients of the motion constraints. For stereo, accumulated events give paired temporal features.

This conversion is part of the model. It decides what information we keep, and how measurement errors reach the coefficients.

I'll also keep track of what each variable means. Physical intensity, log intensity, represented event activity, and a fitted latent profile all play different roles. For example, the stereo preprocessing produces event-feature profiles whose scale is set by that preprocessing.

With the observations defined, let's start with a single pixel.

## Slide 9 — Start with one pixel: integrated changes on a temporal chain

Here's the temporal model in scene terms. The unknown is each pixel's log-brightness history over the recording. The events tell us how much that brightness rose or fell in each interval. Each pixel is reconstructed on its own, and the model picks the reference level that the events leave open. A pixel with no events stays at that reference level, however bright it really is.

Now the details. Fix a pixel and take its events over a time window. At each event time, place a kernel and multiply it by the polarity. Adding these up gives the represented temporal signal on the left.

Then I integrate over the reconstruction intervals. Each entry of y is the signed event contribution in one interval. The algorithm chooses the reconstruction times.

*[Point to the first row of A.]*

The matrix A takes differences of consecutive samples of the unknown profile. Its first row subtracts the first sample from the second, and each later row does the same one step further on. So A f should approximately equal y. These are plain increments; dividing by the time step would turn them into difference quotients.

If A f is zero, every consecutive pair is equal, so f is constant. And every constant vector gives zero differences. So the null space is exactly the constants.

In short, the data constrain the increments, and we need one more rule to choose the level.

## Slide 10 — Temporal kernels: how far each event's influence spreads

*[Point to the kernel curves, then to the bin-integral formula.]*

The kernel controls how an event's contribution spreads over time. Delta binning puts the whole event into its own bin. The rectangular, spline, and truncated Gaussian kernels spread it over a short interval.

Each kernel has unit mass, so an event contributes its full signed amount whenever its whole support lies inside the observation window. The sum on the right expresses that conservation across the bins. Events whose support crosses the edge of the window need special handling at the boundary.

A wider kernel spreads the contribution further. That can reduce sensitivity to timing jitter, and it also blurs fast changes. The curves here share one width for illustration; the experiments use different widths for different kernels.

The difference matrix A stays the same. The kernel changes y, and through y it can also change the weights. That will matter when we get to conditioning.

Next: when does this integrated observation match a physical brightness change?

## Slide 11 — From threshold crossings to an approximate observation

So far, y is something we compute from the events. When does it measure something physical?

*[Point to the diagram.]*

In the ideal sensor, each event marks a change in log brightness of one contrast threshold. So if we add up the signed events between two reconstruction times, we get, approximately, the change in log brightness divided by the threshold. That's the approximation at the top right.

*[Point to the exact identity.]*

Below it is the exact version, from Chapter 2. Three terms separate the two sides. B is kernel mass that spills across a bin boundary. Epsilon is the overshoot or threshold mismatch at each event; a missed or spurious event makes it as large as the threshold itself. And r is change since the pixel's last event that stayed below threshold, so the sensor never reported it. In the diagram, that's the gap at the right end.

When those terms are small, A f approximately equal to y is a model of brightness changes. The events measure change; the absolute level has to come from the model. Next is how the model chooses it.

*[If asked about the continuous-time limit: Backup 03, the jump primitive. If asked whether sub-threshold signals can disappear entirely: Backup 34.]*

## Slide 12 — A regularized estimate is uniquely selected

The objective has two terms. The first fits the reconstructed increments to y. The second penalizes the size of the profile, weighted by a positive diagonal matrix, Lambda. For this theorem, those weights are fixed and strictly positive.

*[Follow the objective down to the normal equations and the computation steps.]*

Setting the gradient of this quadratic to zero gives a linear system. Its matrix is A transpose A plus Lambda transpose Lambda, and its right-hand side is A transpose y. That matrix is positive definite, so there is a unique global minimizer.

In practice, we build this matrix and right-hand side for each pixel, solve the system, and keep the resulting profile. The pixels are independent, so we solve them in parallel. To get the image at a given time, we read off every pixel's value at that time.

*[Point to the baseline identity.]*

The system also tells us how the level is chosen. Take the inner product of the normal equations with the constant vector. A sends constants to zero, so the data term drops out, and we're left with the weighted zero-mean identity shown here.

In scene terms, the weighted average of each pixel's history is zero, so the intervals with the largest weights set the reference level. (Replaces: The penalty therefore chooses a baseline.) The penalty also changes the fitted increments, because the solution balances both terms. Next, why this construction gives uniqueness and a quantitative stability bound.


## Slide 13 — Why uniqueness and stability hold

*[Walk through the first inequality slowly.]*

Take any nonzero direction z. The quadratic form of the normal matrix is the squared norm of A z plus the squared norm of Lambda z.

The first term is nonnegative. The second is at least the smallest weight squared times the squared norm of z. Since that weight is positive, the curvature is positive in every direction.

That gives coercivity and strict convexity, so a minimizer exists and is unique.

For stability, compare two data vectors with the same weights. Subtracting their normal equations gives the exact difference between the two solutions, shown here. Bounding the inverse matrix gives the estimate. In scene terms, one spurious or missed event changes the data by at most one in norm, because each kernel splits a single unit of polarity across the bins. So the bound limits how far one noise event can move a pixel's history, and the smallest weight sets that limit. (Replaces: Bounding the inverse matrix gives the displayed estimate in terms of the data difference and the smallest weight.)

The last expression bounds the condition number in terms of the largest and smallest weights. Lowering the smallest weight weakens these worst-case guarantees.

All of this holds for fixed weights. If the data change and we also recompute the weights, the comparison picks up an extra term for the change in the weights.

Next, what the penalty does to the temporal information itself.

## Slide 14 — What the penalty does to temporal information

To interpret the penalty, take a single scalar weight, so Lambda is lambda times the identity. And suppose the observations are exact differences of a latent signal.

The eigenvectors of A transpose A are temporal modes. In that basis, reconstruction multiplies each mode of the latent signal by g over g plus lambda squared, where g is the mode's eigenvalue.

*[Point first to zero frequency, then along the two curves.]*

The constant mode has eigenvalue zero, so reconstruction removes it entirely. Among the remaining modes, the slowest are damped the most. In the images, slow brightness drift fades and passing edges remain, which is why the reconstructions look edge-enhanced. (Replaces: The low nonconstant modes are attenuated most.) A larger lambda damps more.

That's what the penalty does to the latent signal. Kernel averaging is a separate step, and it can blur fast changes before the solve.

The curves connect the finite-grid gains so the trend is visible. This mode-by-mode formula holds for a scalar weight. A general positive diagonal still gives the uniqueness theorem, but its effect on the modes needs a fuller matrix analysis.

So how are the diagonal weights chosen in the experiments?

## Slide 15 — How are the temporal weights chosen?

The rule we selected uses the size of the signed event total in each bin. Positive and negative events can cancel in that total, so it measures net signed activity.

*[Point to the sigmoid expression.]*

As activity increases, the sigmoid rule lowers the penalty. A positive floor keeps every weight above zero. So quiet intervals get the largest weights, and through the weighted-average identity they set each pixel's reference level. Busy intervals get the smallest weights: they're free to change, and they set the worst-case noise bound from the stability result. (Replaces: The practical intention is to allow stronger changes in active intervals while applying stronger magnitude control in quieter intervals.)

We chose this rule empirically, as a compromise between reconstruction quality and conditioning. Outdoors, the sigmoid gives the lowest condition number of the three choices. Indoors, inverse-proportional weighting gives a lower condition number, so the choice trades conditioning against reconstruction quality.

The point to remember is that the weights are computed from the data and then held fixed during the solve. The theorem covers that frozen problem. Stability of the full adaptive procedure also requires controlling how the weights change.

Here's what these choices give on real data.

## Slide 16 — Temporal evidence: structure without an absolute baseline

*[Point to the images, then to the table.]*

The pictures are a representative example from MVSEC indoor flying two: a reference image, and an event-only reconstruction with sigmoid weights. The table summarizes the kernel comparison over the indoor flying sequences.

The reconstruction makes the scene structure visible. The table reports two things: PSNR, which measures similarity to the reference image, and the condition number of the linear system. PSNR also scores the absolute brightness level, which the model selects, so it measures something different from agreement with the recorded changes.

Indoors, the spline and Gaussian kernels give similar PSNR, both above delta binning, with much smaller condition numbers. Outdoors, the ordering changes. So kernel and weight choices affect both reconstruction quality and conditioning, and the best choice depends on the scene.

The kernel changes the observations, and the adaptive weights can then change the matrix we solve. That's how representation choices reach the linear system.

## Slide 17 — Relation to Antil--Sayre bilevel reconstruction

Here's how the temporal method compares with the Antil--Sayre bilevel approach.

*[Indicate the two workflows at the top.]*

In this chapter, the events set activity-based regularization weights, and then we do one fixed convex solve over time.

The bilevel approach uses events together with intensity frames. Its outer optimization adjusts z, a parameter of the event-based blur kernel that links each blurry frame to the sharp latent image, with one value per pixel and frame. That's the key difference: their outer variable shapes how events explain the frames, while my empirical rule chooses the magnitude weights of the temporal profile.

The table compares complete methods that use different inputs and different optimization structures. Indoors, the bilevel approach has higher PSNR; outdoors, the event-only approach is slightly higher. The event-only approach has lower condition numbers in both. So the two formulations trade off reconstruction and conditioning differently.

Their guarantees also answer different questions. The bilevel analysis proves existence, and local uniqueness under additional conditions. The result I've presented gives a unique global minimizer for every fixed positive diagonal.

The main point for this talk is the event-only construction and the explicit role of its regularizer. Now let's see it on several real event streams.

## Slide 18 — Real event data: indoor, high-speed, and orbital scenes

*[Pause so the audience can look at all three columns.]*

These examples apply the same per-pixel reconstruction, with sigmoid weights and events as input, in three very different settings.

On the left is one frame from a handheld office sequence. The desk, the chair, and the person are all recognizable.

In the middle, a bullet strikes a cup. The scene changes very fast, and the reconstruction shows structure from the impact and the breakup.

On the right is orbital imagery from the Falcon Neuro instrument on the International Space Station, showing structure in the Earth scene below.

The lower cup and orbital panels use false color. Color and grayscale are only display choices; the reference brightness level is still the one the model selected.

These are qualitative demonstrations across very different time scales. They show what the event-derived profiles can reveal.

So far, every pixel has been treated on its own. Next, a way to connect the pixels through a shared scene and known motion.

## Slide 19 — Shared motion couples temporal profiles to one scene

So far, each pixel's history has been rebuilt on its own. In joint work with Professor Antil and David Sayre, called ESAR, the same event constraints describe one static scene seen by a moving camera.

*[Point to the operator equation.]*

Theta is the scene. P holds the known motion: it maps the scene into each view. A takes differences between consecutive views, as before. So B sub SAR maps one scene to the event changes predicted across the whole sequence. SAR stands for synthetic aperture radar, which combines a moving sensor's views into one image of a fixed scene.

*[Point to the figure.]*

Here's a simulated example: disks seen through a window that shifts one pixel per view. Left is the scene, center the estimate, right the error. The error concentrates along rows through the disks. Those are the directions the motion leaves weakly constrained: a pattern that is constant along the motion looks the same in every view. It's the same lesson as the baseline: find what the observations control, and let regularization supply the rest.

Here the motion was known. In optical flow, the motion is the unknown.

## Slide 20 — The aperture problem: what a local view reveals

Optical flow is the apparent velocity in the image plane. A local view can leave part of that velocity free. This is the aperture problem; an aperture here just means a limited window.

*[Play the embedded animation in the left panel.]*

Look at the stripes through these three circular windows. They all seem to move the same way. Each window shows only the inside of a straight striped pattern, so all we can see is how fast the stripes move across their own edges.

*[Play the embedded animation in the right panel. Pause.]*

With the full patterns, we see three different motions: diagonal, upward, and leftward. All three share the same motion perpendicular to the stripes. They differ in the motion along the stripes, and the window hides that part.

The animations show the geometry, and the same ambiguity holds for an event camera. Under steady lighting, these ideal patterns produce the same brightness changes inside each window, and so the same events, given the same thresholds and starting references.

Next, I'll draw this ambiguity for a single edge and state what the flow model assumes.

## Slide 21 — Motion introduces a new invisible direction

*[Point to the left diagram: the edge, the teal arrow, then the amber arrow.]*

Here is one straight edge. The teal arrow is its motion perpendicular to the edge; the dashed line shows where the edge will be a moment later. The amber arrow is motion along the edge. Sliding an edge along itself changes nothing a pixel can see. So the events determine the teal component and leave the amber one free.

*[Point to the right diagram.]*

The right panel shows the same fact in velocity space. Every velocity on the amber line moves edge one across itself at the same speed, so every one of them fits its events. That line runs parallel to the edge. A second edge, at a different angle, gives a different line, and the two lines cross at exactly one velocity.

Here's the flow model in scene terms. The unknown is the image velocity at every pixel. At each edge, the events give the speed perpendicular to that edge. The model assumes that neighboring pixels move alike. That fills in the motion along edges, and the motion where there are no events. It's also why the two edges in the picture can be in different places: smoothness carries each edge's information across the image. The three representations differ in how they get the edge measurement: from crossing times, from transported event activity, or from gradients pooled over a small window. The main theorem makes the requirement precise: somewhere in the scene, there must be edges in at least two orientations.

As with the temporal baseline, the data leave one quantity free, and the model supplies it. Next, I'll derive the local constraint behind this picture, from the time at which an edge crosses each pixel.

## Slide 22 — Derive the time-surface constraint by following the edge

Define psi as the current time minus the crossing-time map. Follow a point moving with the edge: along that path, psi stays zero, because the current time equals the crossing time there.

Differentiate along the path. The time derivative gives one. The spatial part gives minus the gradient of the crossing-time map, dotted with the velocity. Setting the sum to zero gives the time-surface constraint: the gradient of the crossing-time map, dotted with the velocity, equals one.

In scene terms, the size of that gradient is the edge's slowness. If an edge takes ten milliseconds to cross one pixel, it's moving at one hundred pixels per second perpendicular to itself. Motion along the edge leaves the crossing times unchanged, so this single equation already contains the aperture problem.

*[Pause at the hypotheses box.]*

The derivation assumes each location is crossed once, the normal speed is nonzero, and the crossing-time map is differentiable. In real data, a stored timestamp can be stale, or a location can be crossed more than once. Fitting and interpolation also affect the coefficients.

So I treat this relation as a model for the represented data. The analysis then shows what follows once the coefficient fields meet the stated assumptions.

The second representation starts from events binned in both space and time.

## Slide 23 — Voxel projection: transport a represented event-activity field

A voxel grid adds a time axis to the image grid. After smoothing and binning, it gives an event-activity field, V.

Integrate V over a sliding time window to get a.

*[Point to the assumption box.]*

This step adds a modeling assumption, shown in the box: the activity field moves with the scene, at constant velocity over the window. That goes beyond the threshold model. A pixel can start or stop producing events as brightness, motion, and threshold conditions change, and activity is a different quantity from brightness: a steadily bright region can produce very little of it.

Integrating the transport equation gives another transport equation, now for a. Its time derivative is the activity entering at the end of the window minus the activity leaving at the start.

The residual is then the spatial gradient of a, dotted with the velocity, plus that time derivative.

The continuous identity holds under the transport assumption with consistent derivatives. Binning and the choice of numerical derivatives can introduce mismatch. The common theorem applies to the fixed coefficients that enter the energy; how accurate the result is physically also depends on how well this representation describes the motion.

The third representation pools gradients over a small neighborhood.

## Slide 24 — The structure tensor pools directional information

The structure tensor pools several nearby gradients of the represented event field.

Each space-time gradient contributes an outer product. With nonnegative pooling weights, the result is positive semidefinite, because its quadratic form is an integral of squares.

*[Point to the spatial block and the temporal cross term.]*

The spatial block gives the quadratic dependence on the two velocity components. The temporal cross terms give the linear term. The last temporal entry adds a constant to the energy, because the third component of the augmented velocity is fixed at one.

A single spatial gradient constrains one direction. Pooling gradients that point in different directions can constrain both components at one location.

That's one way to get more directional information. The theorem I'll present needs less: enough information across the whole domain, together with spatial smoothness.

So we have three representations. Their coefficients differ, but they all lead to the same kind of variational problem.

## Slide 25 — Three representations, one quadratic variational problem

*[Point to the energy, then briefly indicate the three table rows.]*

This keeps the classical data-plus-smoothness structure, with the event representation supplying the coefficients.

The first integral measures agreement with the motion constraints. B is the data-curvature matrix: it records which motion directions the local edges measure, and how strongly. The forcing vector b carries the measured values. (Replaces: B is the data-curvature matrix and b is the forcing vector.) The second integral penalizes spatial variation of the velocity, with positive strength alpha squared.

For the time surface, B is the outer product of the time-surface gradient. For voxel projection, it's the outer product of the activity gradient. For the structure tensor, it's the pooled spatial block.

The natural space is H one on the image domain, for both velocity components: square-integrable velocities with square-integrable weak derivatives.

The advantage is that we prove one result for fixed B and b, and then apply it to each representation once we've checked its hypotheses.

The question now is whether the data and the smoothness term, together, control every direction in that space.

## Slide 26 — The main flow theorem: global information controls constants

This result specializes the classical well-posedness framework to the event-derived coefficients, under these hypotheses.

*[Read the hypotheses by explaining their roles, rather than reciting the symbols.]*

The domain is bounded, connected, and Lipschitz, and the smoothness weight is positive. The matrix field B is bounded, symmetric, and positive semidefinite, and b is square-integrable.

The key assumption is that the integral of B over the domain is positive definite. Under these hypotheses, the energy has a unique minimizer in H one.

What does that integrated condition mean? Take any nonzero constant velocity. Summed over the domain, the observations must give positive energy in that direction. In scene terms, the recording has edges in at least two orientations, possibly at different pixels: the two crossing lines from the velocity diagram.

Individual locations may give only one direction. Regions with no texture or no events give zero data curvature, and their neighbors supply the motion there. (Replaces: Individual locations may supply only one direction, and some open regions may supply zero data curvature. Spatial coupling allows the estimator to combine information from different locations.)

Connectedness matters because it makes any field with zero gradient a single constant vector over the whole domain. The integrated matrix controls that remaining freedom.

The proof follows this picture directly: split the field into its mean and its fluctuation, and control each part.

## Slide 27 — Proof idea: smoothness fixes variation, edges fix the drift

*[Point to the decomposition, then move across the three columns.]*

Write the velocity as its spatial mean plus a zero-mean fluctuation, w. Physically, the mean is the common drift of the whole field, like a camera pan, and the fluctuation is how motion varies across the image: rotation, zoom, or objects moving separately.

Poincaré's inequality bounds the fluctuation by the gradient, so the smoothness term controls it.

Smoothness charges nothing for a uniform pan, so the data have to fix the mean. That's the role of m, the smallest eigenvalue of the integrated matrix B. It measures how well the scene's edges, taken together, cover every direction of motion. Because m is positive, the data energy controls the mean.

Together, the energy controls the full H one norm, with a constant c zero that depends on the domain, alpha, the bound on B, and m. Lax--Milgram then gives the unique minimizer.

So the gradient penalty controls everything except the constants, and the integrated edge information controls the constants. The constant c zero shrinks as m shrinks: nearly parallel edges weaken control of the drift. The stripe scene on the next slide comes close to that case.

*[If asked for the derivations: the full proof is Backup 09, page 42. If asked about stability: the same c zero gives a Lipschitz bound in B and b, Backup 10, page 43. If asked what happens when the integrated matrix is singular: a constant velocity direction is uncontrolled, Backup 35.]*

## Slide 28 — Known-motion examples make the aperture problem visible

*[Give the audience a moment to compare the two rows.]*

These examples use a known diagonal motion. The top row has a stripe texture, and the bottom row a checkerboard. The true-motion arrows and the estimates share a common scale.

Inside a vertical stripe region, the strong gradients are horizontal, so they mainly constrain the normal motion. In the theorem's terms, this texture gives the integrated matrix little energy along the stripes. In the velocity diagram from earlier, the stripe interior gives only one line. The checkerboard has edges along both axes, so its lines cross, which reduces the aperture ambiguity. Object boundaries can add directional information as well. How accurate the estimate is also depends on the representation and the regularization.

The voxel and structure-tensor columns illustrate the quadratic representations from the talk.

*[If asked about other methods: the contrast-maximization comparison on these scenes is Backup 43; "why analyze the quadratic family" is Backup 45.]*

These are selected simulation windows that illustrate the directional-information argument. A quantitative assessment across real scenes would need a broader evaluation. The purpose here is to connect the geometry of the observations with the conditions in the theorem.

## Slide 29 — Two viewpoints turn correspondence into depth

I'll close the technical part with a short summary of stereo depth.

*[Point to the two cameras and the scene point.]*

Two cameras see the same scene from different positions. After rectification, matching points lie on the same image row. Their horizontal offset is the disparity.

By similar triangles, depth is the focal length times the camera baseline, divided by the disparity. Small disparities mean distant points, so a disparity error matters most at large depths.

For each left pixel, we compare candidate right pixels along the same row. Each candidate gives a right-view temporal signal to pair with the left one.

Here's the stereo model in scene terms. If a left pixel and a right pixel see the same scene point, they see the same changes over time, so their event profiles should agree over the window. For each candidate disparity, the model reconstructs a profile in each view, ties the two together softly, and scores how well one shared explanation fits both streams. The weights treat busy intervals as noisier, as Poisson counts would be, so they give more weight to intervals with less predicted activity. The best-scoring candidate gives the disparity, and from that the depth. So there are two levels: solving for the profiles at a fixed candidate, and then comparing candidates. (Replaces: This creates two levels of estimation. At a fixed candidate, we solve for the latent temporal profiles. We then compare candidates to choose a disparity.)

The model assumes the candidate match holds approximately over the window, with the scene point visible in both views. The key distinction is between solving for the profiles and choosing the match.

## Slide 30 — Stereo on MVSEC: competitive accuracy, more scored points

*[Point to the energy first, then to the WLS row and the Piatkowska row.]*

At each candidate disparity, the model solves for one temporal profile per view. Each profile fits its own events, as in the temporal chapter, and a soft penalty ties the two profiles together.

*[Point to the two labels.]*

The mathematical result is for a fixed disparity with the weights frozen. The coupling term is nonnegative, so the temporal coercivity proof carries over, and the inner problem has a unique solution. The benchmark runs the full method: the weights are updated, the costs are aggregated over neighboring pixels, and the lowest-cost candidate gives the disparity.

Here's how that performs on the MVSEC indoor flying sequences, against the dataset's lidar-based ground-truth depth. The first four columns are mean depth error in centimeters, one per sequence. Then log RMSE, and the number of scored points.

Our weighted least-squares method, WLS, has the lowest error on indoor flying two and the lowest log RMSE. On the other three sequences, the local adaptation of Piatkowska and colleagues' method is lower, by between one and a half and six centimeters. WLS scores two point six six million points, more than twice the one point two million for that method. It also leads the three other prior event-based methods on every sequence.

Each method is scored on its own valid pixels, so the comparison reflects both accuracy and coverage.

That completes the three estimation problems. I'll finish by bringing their guarantees together.

## Slide 31 — What the data constrain and what the models prove

*[Read across each row: what the events constrain, then what the model proves.]*

For temporal reconstruction, the events constrain brightness increments. For each fixed positive weight matrix, the regularized history is unique, with perturbation bounds, and the penalty selects the baseline.

*[If asked about recomputed weights: Backup 65, page 98, gives a local Lipschitz bound beyond the dissertation.]*

For flow, the events give directional constraints on the motion. Smoothness and integrated directional information together give a unique H one minimizer.

For stereo, the two cameras give paired event-feature profiles. At a fixed candidate disparity, with the weights frozen, the inner solve is unique. Choosing the disparity is a separate comparison across candidates.

The proof tools are classical. The contribution is the analysis of these event-derived models under explicit hypotheses: what the observations control, and what the model selects.

Those results point to a few research directions.

## Slide 32 — Research opportunities

*[Move through the three boxes, left to right.]*

First, event-sensor modeling. Slide eleven separated the measured increments from brightness changes by three error terms. Measuring those terms on a real sensor, together with timestamp and binning error, would let the stability bounds translate sensor error into estimate error. The new GMU Neuromorphic Imaging and Digital Twins Lab makes those controlled acquisitions possible.

Second, learned temporal regularization, as a possible extension. When all the weights are positive, the fixed-weight solution is a smooth function of those weights. That gives a well-defined lower-level map for an outer learning problem, in the spirit of Antil, Di, and Khatri.

Third, shared-scene and orbital sensing. For a given trajectory, which scene patterns does the motion leave invisible? The null space of B sub SAR answers that question, and sparse orbital streams like the ISS data are a natural application.

Each direction starts from a quantity the dissertation already controls: an observation error, a solution map, or a null space.

## Slide 33 — From event changes to well-posed estimators

*[Look up from the screen.]*

I began by asking what we can recover from changes alone.

Temporal reconstruction shows how a penalty selects the baseline. Flow shows how directional observations and spatial coupling together determine a motion field. Stereo shows that a unique inner solution and a reliable match need separate arguments.

Across all three, the common question is which directions the observations control, and which the model chooses.

Thank you. I'm happy to take your questions.

*[Stop. Leave the closing slide visible.]*

# Backup responses

Use these responses when a question calls for the corresponding slide. Start with the answer and expand into the follow-up when useful. Each response defines its own context, so you can enter at any slide. There are no scripted transitions between backup slides.

## Backup 01 — Discussion guide

Deck page: 34.

*[Navigation only. Choose the relevant technical question from this index; no spoken introduction is needed.]*

## Backup 02 — Must every temporal penalty entry be positive?

Deck page: 35.

**Likely question:** Do you really need a positive penalty at every temporal sample?

*[Point first to the kernel intersection, then to the connected-chain null space.]*

### Answer

No. The requirement is weaker: the observation operator and the penalty must not share a nonzero null vector. On the slide, that's the kernel intersection. Here A is the first-difference operator and Lambda is the penalty. The quadratic form of the reconstruction matrix is the squared norm of A times a vector, plus the squared norm of Lambda times that vector. It's strictly positive exactly when those two can't both vanish for the same nonzero vector.

On a connected temporal chain, the null space of A is the constant profiles. So a single nonzero penalty entry is enough to remove the ambiguity. Fixing one reference value, or requiring zero mean, also picks out a unique answer. I use a fully positive diagonal in the theorem because it gives a simple quantitative lower bound along with uniqueness. A measured reference would go further: it would supply actual physical information about the brightness baseline.

### If asked for more

Selecting the constant is different from regularizing the whole profile. A zero-mean constraint fixes only the unobserved offset. A magnitude penalty also damps the nonconstant modes and changes how they respond to noise. With a single anchoring entry, the matrix is still positive definite, but the lower bound based on the smallest diagonal entry has to be replaced by a bound for that anchored matrix. The kernel-intersection test remains the exact algebraic criterion.

## Backup 03 — The event measure has a jump primitive

Deck page: 36.

**Likely question:** What is the precise continuous-time interpretation of accumulating events?

*[Indicate the right-closed interval convention, then the two primitives.]*

### Answer

At one pixel, I write the events as a signed measure: a point mass at each timestamp, weighted by its polarity. Its cumulative primitive is a step function. Start from a chosen initial value, and add the signed mass of the events up to the current time. Counting the right endpoint of each interval makes the primitive right-continuous, and its increments then match the event measure exactly.

With finitely many events, this primitive has bounded variation. Smoothing the measure with a standard kernel gives a regular temporal driver, and integrating that driver gives a smooth approximation of the staircase. As the kernel width shrinks, these smooth primitives converge in L one, for finitely many interior events. That describes the cumulative-event surrogate. The regularized reconstruction then makes its own, separate choice about fitting those increments and controlling the size of the profile.

### If asked for more

A nonzero jump has a singular distributional derivative, so the unsmoothed primitive naturally lives in bounded variation, outside H one. At any positive kernel width, the kernels here give an L two driver and an H one primitive. On the discrete side, the first-difference matrix computes increments; dividing by the time step would instead approximate a derivative. Keeping that scaling and the interval endpoints consistent is essential when comparing the continuous and discrete descriptions. A joint limit in the grid and the regularization would need its own argument, beyond convergence of these primitives.

## Backup 04 — Latent-signal gain and observation-noise gain are different

Deck page: 37.

**Likely question:** What does regularization do to the signal and to measurement noise?

*[Contrast the first and second table rows before discussing the variance row.]*

### Answer

They're two related but different transfer functions. On this slide, the penalty is a single positive scalar, lambda, and the observations are unweighted. Let g be an eigenvalue of A transpose A.

First, the signal. Take an underlying temporal profile, apply A to get ideal differences, and reconstruct. Each profile mode comes back multiplied by g over g plus lambda squared. The low modes are damped most, and the constant mode is removed.

Second, the noise. If instead I perturb the difference observations, the amplitude gain is the square root of g, over g plus lambda squared. For independent white noise with variance sigma squared, squaring that gain gives the reconstructed variance in each mode. So damping slow modes of the signal and passing observation noise through the inverse are two separate statements.

### If asked for more

The singular value decomposition makes this explicit. A maps the right singular modes of the profile to the left singular modes of the observations, and the inverse maps back with the gain shown here. Treating g as continuous, the variance factor peaks at g equal to lambda squared, where it equals one over four lambda squared. On a finite chain the maximum can be smaller, because the eigenvalues are discrete. These exact formulas hold for the scalar, unweighted model; general diagonal or adaptive weights need the corresponding matrix analysis.

## Backup 05 — Kernel performance depends on the scene and adaptive weights

Deck page: 38.

**Likely question:** Why does changing the temporal kernel change both accuracy and conditioning?

*[Point across the indoor and outdoor columns to show the change in ranking.]*

### Answer

Because the kernel changes the data, and the adaptive penalty is computed from the data. The first-difference operator stays the same. But the represented observations change with the kernel, so the penalty entries can change too. That changes the reconstruction matrix, and with it the condition number. So the conditioning difference belongs to the resulting adaptive system.

The table also shows that the accuracy ranking depends on the scene. Indoors, the B-spline gives a PSNR of 8.86 with condition number 22.16; the Gaussian is very close, at 8.84, with condition number 20.22. Outdoors, delta binning has the highest PSNR of these four, 7.97, with condition number 53.34. So the representation should be chosen with the scene and the weighting rule in mind. Conditioning measures how sensitive the linear solve is; accuracy also depends on the data, and on the bias that regularization introduces.

### If asked for more

If A and Lambda were both held fixed, changing only the right-hand side would leave the condition number unchanged. Here, the adaptive penalty is what links the representation to the conditioning. The positive-definiteness theorem applies to every fixed positive penalty this produces. It guarantees the solve, while the table compares actual reconstructions. Those are scored against reference images, and the events still leave the absolute temporal offset to the regularization or the reference convention.

## Backup 06 — What the reconstruction scores measure

Deck page: 39.

**Likely question:** How is each reconstruction metric computed, and what do the scores establish?

### Answer

Briefly, metric by metric.

**PSNR** starts from the mean squared pixel error against a reference image. It's ten times the base-ten log of the peak value squared over that error. **SSIM** compares local means, variances, and covariance, which captures luminance, contrast, and structure. Both are averaged over frames.

**EPI** correlates the gradient magnitude of the mean reconstruction with the normalized event-count map. **ERC** correlates the absolute change between consecutive reconstructed frames with the absolute bump-integrated event data.

**TC** takes the root-mean-square change between consecutive frames, divides it by the reconstruction's intensity range, and exponentiates the negative. **TG** averages the absolute frame-to-frame changes over pixels and frame pairs. **TV** averages the sum of absolute horizontal and vertical gradients over pixels and frames.

**SC** is the fraction of each frame's Fourier power inside a central low-frequency disk, averaged over frames. **CN** is the ratio of the evaluated matrix's largest singular value to its smallest.

These measure different things. Under these conventions, a constant sequence gets the best possible TC, one, and an ERC of zero. Smoothness scores reward a static output, so I read reference fidelity, event consistency, and conditioning together.

### If asked for more

For ERC, both sequences are truncated to the same number of slices, flattened, and compared by Pearson correlation. EPI also uses Pearson correlation. Inputs with zero variance get zero correlation. TC is one for a reconstruction with zero range. In SC, an all-zero frame contributes zero power fraction, and the disk radius is one eighth of the smaller image dimension.

PSNR and SSIM depend on the normalization used for scoring, and CN describes the specified diagnostic matrix. The baseline choice and the regularization affect image agreement as well as smoothness.

## Backup 07 — Can the reconstruction run in real time?

Deck page: 40.

**Likely question:** Can the reconstruction run in real time, and what governs its responsiveness?

### Answer

Yes. I developed a native C++ and CUDA version inside iniVation's DV software and used it for live reconstruction, so I have practical experience running this approach in near real time.

The model suits repeated windowed processing: each pixel has its own temporal problem, and the first-difference operator makes the systems sparse. The implementation takes incoming batches of events and produces updated images.

How fast it runs depends on the number of active pixels, the event load, the number of temporal samples, the window length, and the output rate. More temporal detail or more event context means more work, and possibly more delay; the settings can instead favor quicker updates.

So the practical answer is live, windowed reconstruction with an adjustable processing budget. Four quantities are worth keeping apart: the fine event timestamps, the spacing of the reconstructed times, the rate of completed outputs, and the camera-to-display latency.

### If asked for more

The DV module receives events, sets up the active pixels' temporal systems in C++, calls CUDA and cuSOLVER's sparse QR, and returns the latest image through the DV frame output. Each selected batch is solved independently.

It supports accumulation by event count or by time window. That choice affects how much data goes into each reconstruction and how old the selected events are. The update interval sets the minimum spacing between triggers; the rate of completed outputs also depends on processing time and on event availability.

The module times batch selection, reconstruction, and frame emission. Camera-to-display latency also includes acquisition, buffering, and display. If asked for a specific rate or delay, give the figure together with the module's settings and workload.

## Backup 08 — The weak equation supplies the natural boundary condition

Deck page: 41.

**Likely question:** Which boundary condition does the flow model use?

*[Move from the variational equation to the interior equation and then the weak boundary trace.]*

### Answer

The natural one: homogeneous Neumann. I minimize over all of H one, so the boundary values are free. Taking the first variation gives the weak equation shown here, for every H one test field. B is the data coefficient matrix, b is the data forcing, and alpha sets the spatial smoothing.

The argument has two steps. First, test fields supported inside the domain give the differential equation in the distributional sense. Under the coefficient hypotheses, B times the solution and b are both in L two, so the solution's distributional Laplacian is in L two as well. That's enough regularity to define a weak normal trace of the gradient. Second, going back to general test fields shows that this normal derivative is zero on the boundary, in that weak trace sense. That's the right boundary statement on the Lipschitz domains the theorem uses.

### If asked for more

The last step is the generalized Green's identity. Its boundary pairing must vanish against the trace of every H one test field. The trace map reaches the whole boundary trace space, so the normal trace is zero. For a fixed anisotropic diffusion tensor, the same argument applies to the flux: the normal component of D times the gradient is zero. That's a conormal boundary condition. The weak formulation uses the bounded tensor directly, so D never needs a classical derivative.

## Backup 09 — Proof: control the mean and the fluctuation separately

Deck page: 42.

**Likely question:** How exactly does the proof control the mean?

*[Point to each line as its role is explained.]*

### Answer

Through m, the smallest eigenvalue of the integrated matrix B. Write the velocity as its spatial mean plus a zero-mean fluctuation, w. The gradient of w is the same as the gradient of the full field, so Poincaré's inequality bounds the L two norm of w by the gradient norm. Smoothness controls the fluctuation.

Smoothness charges nothing for a uniform pan, so the data have to fix the mean. Applying the integrated quadratic form to the mean gives a lower bound of m times the mean's squared size. To connect this to the energy of the full field, write the mean as v minus w. Apply the square root of B and use the squared triangle inequality. That bounds the mean term by twice the data energy of v, plus twice a B-weighted fluctuation term. The upper bound on B and Poincaré's inequality control that last term, which gives the displayed inequality.

Now the energy controls the mean, the fluctuation, and the gradient, so it bounds the full H one norm from below. The bilinear form is bounded and coercive, so Lax--Milgram gives a unique weak solution. The weak equation is the first-order condition of this strictly convex energy, so its solution is the unique minimizer.

### If asked for more

An admissible constant, not an optimal one, is c zero equals the smaller of two numbers: m over twice the domain's area, and alpha squared over one plus C P squared plus twice the area times beta B times C P squared over m. It comes from writing the squared H one norm as the area times the mean's squared size, plus the squared L two norm of the fluctuation, plus the squared gradient norm. For fixed alpha and beta B, this bound decreases linearly as m decreases.

## Backup 10 — Stability follows by subtracting weak equations

Deck page: 43.

**Likely question:** How do you get the stability bound?

*[Point to the two terms in the bound.]*

### Answer

By subtracting the two weak equations and reusing one coercivity constant. Take two sets of coefficients with common bounds on B and b, and a common positive lower bound m on integrated identifiability. Those shared bounds give one coercivity constant, c zero, that works for both problems.

Subtract the two weak equations, and test with the difference of the solutions, z. The left side controls c zero times the squared H one norm of z. The right side has two parts. One comes from the change in b. The other comes from the change in B, acting on the second solution. Cauchy--Schwarz, together with the bound R b over c zero on that solution, gives the final estimate.

So small changes in the coefficients produce controlled changes in the flow, as long as identifiability stays uniformly positive. The coefficients change because of timestamp jitter, binning choices, and noise events. The constants grow as m shrinks; the stripe scene on slide 28 comes close to that case.

### If asked whether a stable estimate is close to the true motion

The theorem is about the minimizer of the chosen energy. How close that minimizer is to the true motion depends on two things: how accurately the represented coefficients describe the motion, and how much the H one penalty smooths across motion boundaries. The known-motion experiments measure that distance directly. In the stripe interior, the estimate is unique but mostly horizontal, and the normal-flow reference there is 2.12 pixels from the true diagonal motion.

### If asked for more

Linking the bound to raw sensor errors needs an additional model of the representation error. If a density-dependent diffusion tensor is recomputed, the regularizer changes too, and its L infinity perturbation must enter the bound as well.

## Backup 11 — Discrete flow: connectivity and sampled directions matter

Deck page: 44.

**Likely question:** How is the flow computed, and when does the iteration converge?

*[Point to the local two-by-two matrix, then to the two terms on the right.]*

### Answer

By simultaneous block-Jacobi sweeps on a pixel graph. They converge to the unique discrete minimizer from any starting field when the weighted sum of the sampled data blocks is positive definite.

Each node stores two velocity components. Its data matrix B describes the measured directions, and b carries the corresponding observations. A positive node factor, q, weights that local contribution. At node i, the matrix combines the local data with alpha squared times the weighted degree: the total weight linking the node to its neighbors. Solving this two-by-two system blends the pixel's own edge measurement with its neighbors' previous velocities.

Every node uses the same old field. Once all the new velocities are computed, we replace the field and repeat. Each sweep carries information from image edges one more pixel into textureless regions.

The theorem assumes the graph is connected, its edge weights are symmetric and nonnegative, its degrees and node factors are positive, and each data block is positive semidefinite.

### If asked for more

The reason mirrors the continuous argument: the graph controls variation, and the sampled data control the remaining constant direction. The graph structure also gives the spectral condition this particular iteration needs; the next backup has that argument. The theorem applies when a representation's stencil and update schedule match these hypotheses.

## Backup 12 — Why block-Jacobi converges for this graph model

Deck page: 45.

**Likely question:** Why does block-Jacobi converge for your discrete flow system?

*[Explain the two signs in the energy identity before pointing to the spectral interval.]*

### Answer

The proof uses the graph structure of this particular system. The graph is connected, its edge weights are symmetric and nonnegative, and the sampled data blocks are positive semidefinite with a positive-definite sum. D holds each node's weighted degree and data block; R holds the couplings between neighbors. Positive alpha and positive degrees make D positive definite.

The key step is showing that both D minus R and D plus R are positive definite. Their quadratic forms are sums of nonnegative data terms plus squared differences, or squared sums, across edges. Connectedness narrows their possible zero modes to constant fields or alternating constant fields, and the data blocks rule those out. After scaling by D to the minus one-half, these two inequalities put every eigenvalue of the symmetric coupling matrix strictly between minus one and one. That's exactly what simultaneous Jacobi sweeps need in order to converge.

### If asked for more

For D minus R, a zero contribution on every edge forces neighbors to agree, so on a connected graph the field is one constant vector. For D plus R, neighbors must be opposites. A bipartite graph allows an alternating copy of one vector; an odd cycle forces that vector to zero. Either way, the positive-definite sum of data blocks rules out any surviving nonzero vector. The Jacobi matrix is similar to the scaled symmetric matrix, so the two share a spectrum. This proof covers the simultaneous update schedule.

## Backup 13 — Anisotropy needs a uniform ellipticity floor

Deck page: 46.

**Likely question:** How can directional smoothing preserve the well-posedness theorem?

*[Use the two eigenvalues to distinguish tangent smoothing from normal smoothing.]*

### Answer

The diffusion tensor needs a uniform positive lower bound on its eigenvalues. I use the normalized Nagel–Enkelmann form, built from the spatial gradient of event density. That gradient points across a density edge, and its perpendicular points along the edge. The tensor has eigenvalue one along the edge and a smaller positive eigenvalue across it.

So it penalizes flow changes across a density edge less, while still smoothing fully along it. The positive parameter gamma provides the floor. When the density gradient is bounded, the formula gives one positive lower bound, theta, over the whole domain. The coercivity proof then goes through with alpha squared times theta in place of alpha squared. So the directional model keeps the same existence and uniqueness argument under the integrated identifiability condition, with constants that depend explicitly on that floor.

### If asked for more

A pointwise positive eigenvalue could still approach zero somewhere in the domain, which is why the proof needs a uniform floor. Here, a bounded density gradient and positive gamma give that floor explicitly. If the tensor is recomputed when the data change, the stability estimate must also account for the change in D, measured in the essential-supremum norm. The tensor follows event-density edges; treating those as motion boundaries is a modeling choice. The theorem guarantees solvability for the specified tensor.

## Backup 14 — A variable diffusion tensor must stay inside the divergence

Deck page: 47.

**Likely question:** Can the anisotropic operator be implemented by weighting the second derivatives?

*[Point to the coefficient-derivative terms, then to the affine example.]*

### Answer

Only when the extra coefficient terms vanish, for example when the tensor is constant. For a spatially varying tensor, the divergence form contains both second derivatives of the field and first derivatives of the tensor coefficients; the product rule gives all the terms on this slide. Keeping only the tensor-weighted Hessian drops the coefficient terms.

The example makes this concrete. Take event density x squared over two, gamma equal to one, and the test field u equal to x. The tensor is diagonal, with first entry one over one plus x squared. The field has zero second derivatives, yet its flux changes with x, because that tensor entry changes. Differentiating the flux gives minus two x over the square of one plus x squared. A discretization has to capture that changing flux to approximate the stated model.

### If asked for more

The weak formulation is useful when D is only bounded and measurable. It integrates the test-field gradient against D times the solution gradient, so coefficient derivatives never appear. A flux-based discretization can approximate this divergence structure directly. The affine test field is a simple consistency check: its gradient is constant, but its flux varies, and the computed operator should show that variation.

## Backup 15 — The regression radius formula is a heuristic

Deck page: 48.

**Likely question:** Is the regression-radius formula an optimal choice of neighborhood?

*[Identify the increasing bias term and decreasing variance term before discussing the radius.]*

### Answer

Only in a leading-order sense. It optimizes the leading approximation to the exact error bound for the actual lattice disk of sample points. The assumptions are a complete disk on a square lattice, a radius large compared with the lattice spacing, and a time surface that's smooth throughout the disk. L sub H measures how fast the Hessian can change, sigma is the timestamp-noise standard deviation, and h is the lattice spacing.

The leading squared-bias term grows like the radius to the fourth, and the variance term shrinks like its reciprocal. Balancing them gives the radius shown. Noisier data favor more averaging; faster-changing curvature favors a smaller neighborhood. I use that scaling as a principled guide. For an actual finite neighborhood, the exact lattice sums give the appropriate bound. And the whole fitting disk has to stay inside the region where the smoothness assumptions hold.

### If asked for more

Minimizing one constant times r to the fourth plus another constant times r to the minus fourth makes r to the eighth equal to the ratio of the second constant to the first. Substituting the coefficients gives the factor shown. The asymptotic remainder can have either sign, so the leading expression alone isn't an upper bound for every finite design. And for an affine time surface the curvature bias is zero, so more samples only reduce variance, and this model has no finite balancing radius.

## Backup 16 — Uniform projection and OLS slope need not be transport partners

Deck page: 49.

**Likely question:** Why must the temporal slope and spatial projection use compatible weights?

*[Point to the common temporal weight and then the cubic residual.]*

### Answer

Because they enter the same transport equation, and that equation stays exact only if both use the same averaging. The ordinary least-squares temporal slope can be written as a weighted average of the time derivative. Its weight is the parabola shown here: zero at the endpoints and largest in the middle of the interval.

If I integrate the transport equation against that weight, the spatial term must use the same weighted projection. Pairing the OLS slope with a uniform temporal projection instead leaves the residual shown. For the transported cubic, that residual is one tenth, even though the underlying field satisfies transport exactly. So there are two separate questions: whether the coefficient fields give a well-posed problem, and whether they represent the physical transport relation exactly. The flow theorem answers the first, for any coefficients that meet its hypotheses.

### If asked for more

Integrating by parts in the OLS formula produces the parabolic weight. Uniform averaging and that weight agree on the zeroth and first temporal moments, so low-degree tests reveal little. For transported polynomials up to degree two, the mismatch is zero, which makes the cubic the natural explicit example. If the resulting coefficient error is controlled in the norms of the stability theorem, and identifiability stays positive, that theorem bounds its effect on the flow.

## Backup 17 — Mean-zero conditioning removes the unobserved mode

Deck page: 50.

**Likely question:** Can a mean-zero formulation avoid poor conditioning as lambda becomes small?

*[Point to the excluded k equals zero mode and the new smallest eigenvalue.]*

### Answer

Yes, in the scalar, unweighted model. Removing the constant temporal modes gives a condition-number bound that stays finite as lambda goes to zero. The first-difference operator sends constants to zero, so the right-hand side has zero mean in each view. The scalar system preserves the mean-zero subspace, so for positive lambda the solution already lies in it.

On that subspace, the smallest temporal eigenvalue is g one instead of zero. The sum and difference blocks have eigenvalues g k plus lambda squared, and g k plus lambda squared plus two gamma, with the constant mode left out. Their ratio gives the exact restricted condition number, and its denominator stays positive even at lambda equal to zero. So a mean-zero parameterization helps the algebraic solve, provided we state the convention for the unobserved brightness baseline.

### If asked for more

The bound is uniform in lambda for a fixed temporal grid and fixed coupling. It still depends on the grid: g one behaves like pi squared over n squared for the unscaled chain, so the lambda-uniform bound grows quadratically with the number of samples. At lambda equal to zero the full-space matrix still has a constant null mode, so to use the restricted guarantee, a numerical implementation has to actually enforce the mean-zero restriction. General diagonal penalties or unequal weights need their own matrix bounds.

## Backup 18 — The selection theorem has an exact ellipsoid interpretation

Deck page: 51.

**Likely question:** Can you characterize exactly which competing stereo profiles beat the ideal match?

*[Explain inside, boundary, and outside using the completed-square expression.]*

### Answer

Yes. For the candidate-local unweighted model, the competitors that beat the ideal match fill an ellipsoid in observation space. I hold the positive regularizer and the coupling fixed across candidates, and assume the ideal candidate's right profile equals the left observation. S is the monocular cost matrix, T is the coupling-discrepancy matrix, and P is their sum.

Completing the square writes the cost gap as the squared P-distance from the candidate profile to a center c, minus rho squared. P defines the metric, so the surface of equal cost is an ellipsoid, and the ideal match lies on its boundary. A competitor inside the ellipsoid costs less than the ideal match; one outside costs more. That's an exact geometric picture of the attenuation effect. It also gives a simple sufficient rule: any mismatch larger than two rho in the P-norm loses to the ideal match.

### If asked for more

Let the mismatch be the left observation minus the competing right observation. The cost gap is its squared P-norm minus a linear term involving S. Cauchy–Schwarz in the P inner product bounds that linear term by two rho times the mismatch norm, so the gap is positive whenever the mismatch norm exceeds two rho. The exact ellipsoid test is sharper, because it uses direction as well as distance. Both statements concern the fixed, unweighted candidate cost before spatial aggregation.

## Backup 19 — An observation perturbation bound can protect a disparity winner

Deck page: 52.

**Likely question:** How much observation noise can the stereo decision tolerate?

*[Indicate that the maximum includes the winner, then the half-margin condition.]*

### Answer

With a positive winning margin, we can put a number on it, for a fixed candidate list and fixed model parameters. I hold the left observation, A, Lambda, and gamma fixed, and perturb each right candidate profile. The cost is quadratic in that right observation: its gradient is two P times the displacement from c, and its Hessian is two P.

The operator norm of P is at most one half. Expanding the quadratic, each cost changes by at most the candidate's distance from c times the size of the perturbation, plus one half the perturbation size squared. Eta is the largest such bound over all candidates, including the original winner. If eta is less than half the original winning margin, every competitor stays more expensive. That protects the decision even though the formerly ideal right profile may be perturbed too.

### If asked for more

The factor of two in the margin condition covers two changes at once: the winner's cost can rise by eta while a competitor's falls by eta. So the perturbed gap is at least the original margin minus two eta. For this observation bound, the quadratic expansion is exact. If the preprocessing, the left data, or adaptive parameters also change, their contributions must go into the score-perturbation estimate. The same margin argument then applies to whatever uniform score bound results.

## Backup 20 — How the reciprocal IRLS contraction bound is obtained

Deck page: 53.

**Likely question:** Where does the sufficient IRLS contraction constant come from?

*[Follow the difference identity through the operator, residual, and weight estimates.]*

### Answer

I compare two frozen-weight solves generated by two input states. B time is the block-diagonal temporal difference operator for the two views. Subtracting the normal equations expresses the difference of the solutions as an inverse-system operator applied to a weight difference times a residual.

Three estimates control that expression. First, the positive regularizer bounds the inverse operator in terms of ell, the square of the smallest penalty entry. Second, comparing the frozen optimum with zero bounds its weighted residual by the weighted data norm. Third, reciprocal weights change in a controlled way: the change in an absolute value is at most the change in its argument, and every weight is at most one over epsilon. Combining the three gives q on the slide. When q is below one, the frozen-solve map is a contraction, and its iterates converge geometrically to a unique fixed point.

### If asked for more

The weight estimate pairs with the weighted residual, instead of a separate unweighted residual bound, and that's what produces the epsilon to the minus three-halves. The change in predicted temporal differences is at most the norm of A times the change in the state, which supplies the remaining factor. This is a sufficient global bound for the unclipped reciprocal map. When it's one or larger, it gives no conclusion about contraction; a convergence claim then needs another argument or a further sufficient condition.

## Backup 21 — A converged frozen-weight iteration need not be maximum likelihood

Deck page: 54.

**Likely question:** Does convergence of the reweighted iteration imply a maximum-likelihood estimate?

*[At the fixed point, show that the residual term vanishes while the log-variance derivative remains.]*

### Answer

No. When the variance depends on the unknown state, a frozen-weight fixed point and a likelihood optimum solve different derivative equations. A scalar example shows this directly. Take a positive observation y, with variance equal to the absolute prediction plus a positive epsilon. With the variance frozen, every least-squares step is minimized at the prediction y, so the iteration reaches that fixed point immediately.

The full Gaussian negative log-likelihood is different: the variance moves with the prediction, which adds a log-variance term. At the prediction y the residual is zero, but the derivative of the log-variance term is positive: one over two times the quantity y plus epsilon. So lowering the prediction slightly lowers the negative log-likelihood, and the fixed point is not its minimizer. The fixed-point theorem is a statement about the iterative map; likelihood optimality requires differentiating the full state-dependent objective.

### If asked for more

This scalar example deliberately has no regularizer, to keep the mechanism visible. It separates two claims; it isn't an instance of the positive-penalty temporal theorem. The dissertation also gives a two-sample temporal example with positive regularization, where a fixed point differs from a stationary point of the final-state-weighted score, even before the Gaussian log term is added. The empirical estimator is evaluated as the specified surrogate procedure, with its own objective and stopping rules.

## Backup 22 — What the implemented IRLS procedure returns

Deck page: 55.

**Likely question:** What does one candidate-level IRLS call actually return?

*[Walk through the five steps, emphasizing the different solve and scoring weights.]*

### Answer

It returns the last accepted latent iterate and its computed score. The procedure starts from the exact unweighted solve. At each iteration it forms predicted-rate weights, clips them for the linear solve, and freezes them. That system is positive definite. The algorithm solves it and takes a damped step toward the frozen minimizer.

For scoring, it recomputes the weights at the proposed state with the unclipped rule, then applies the acceptance and stopping tests. The score uses the weighted residual and the regularization terms, without a Gaussian log-variance term. So clipping, damping, and stopping are all part of the estimator being evaluated. After these candidate-level steps, masking, averaging, margin normalization, and semi-global matching adjust the candidate comparisons. The existence and contraction results describe the specified reweighting map; the experiments assess the complete implemented procedure.

### If asked for more

The solve weights and the score weights do different jobs. Clipping controls the matrix used for the update; the unclipped weights define the score used to judge the proposal. A stopping rule can return an accepted iterate before it reaches a fixed point. Later, finite penalty values used for guidance or rejection go into averaging, so they act as soft preferences rather than hard constraints. The final winner is the exact minimizer of its computed score list, and path aggregation supplies the spatial context for that list.

## Backup 23 — Depth evaluation distinguishes returned coverage and scored coverage

Deck page: 56.

**Likely question:** Does WLS achieve its better scores by returning estimates at many more pixels?

*[Contrast the first two numeric columns before discussing the scored-point totals.]*

### Answer

No. Both methods return estimates at about half the eligible pixels; the difference is in how many of those estimates fall inside the reporting band. The table keeps returned coverage separate from the population used to score accuracy. First, the ground truth must be finite and inside the band. Returned coverage counts finite estimates at those locations. Scoring also requires the estimate itself to fall between 0.5 and 8 meters.

The control returns finite estimates at 50.17 percent of eligible locations, and WLS at 49.48 percent. The in-band share of those estimates is where they differ: 51.54 percent for the control, and 96.40 percent for WLS. That gives 1.43 million scored points for the control, and 2.66 million for WLS. So WLS has a much larger scored population with comparable returned coverage. These are complete configurations, so the comparison includes their preprocessing, weighting, and final masking.

### If asked for more

A finite depth outside the band is excluded by the evaluation convention, though it may still be physically possible. That's why returned coverage, in-band retention, and accuracy answer different questions. The benchmark's raw outputs include interpolation around the finest-level score minimum, and leave out the separate posterior refinement step. Reading the errors alongside these counts keeps the interpretation precise. A common-population comparison would score both methods on the same eligible pixels.

## Backup 24 — Pooled kurtosis does not establish heavy-tailed active errors

Deck page: 57.

**Likely question:** Does the large pooled residual kurtosis justify a heavy-tailed noise model?

*[Point to the single active-probability factor in both moments and its effect in their ratio.]*

### Answer

Not by itself; it's a reason to look more closely at the residuals. This simple mixture shows why. Suppose a fraction of pixels have exactly zero residual, and the rest are zero-mean Gaussian with variance sigma squared. The Gaussian part has ordinary Gaussian tails. But pooling it with the point mass at zero gives an excess kurtosis of three over the active fraction, minus three.

So the more zeros, the larger the pooled kurtosis. Event-free pixels can have exactly zero fitted transport residuals, so sparsity alone can create the effect. Regularized fitting, unequal variances, and temporal dependence also shape the residual distribution. So I'd read the pooled diagnostic alongside the event-active residuals and how their variance scales. That separates concentration at zero from the tails of the active errors, and gives a better basis for choosing the observation model.

### If asked for more

The moment calculation is direct. Only the active Gaussian part contributes to the second and fourth moments, so each picks up one factor of the active probability. Dividing the fourth moment by the square of the second leaves the reciprocal of that probability. A useful follow-up would report the zero fraction, standardize the active residuals by their variance, and compare with synthetic residuals passed through the same fitting procedure. Robust penalties remain an option, but choosing one needs evidence beyond this pooled moment.

## Backup 25 — Adaptive temporal weights are fixed in the theorem

Deck page: 58.

**Likely question:** How do the adaptive temporal penalties relate to the fixed-weight theorem?

*[Contrast the activity-decreasing Chapter 2 rules with the energy-increasing Chapter 4 rule.]*

### Answer

The theorem applies once the adaptive rule has produced a positive penalty matrix. In Chapter 2, the sigmoid, inverse-proportional, and exponential rules all lower the magnitude penalty as event activity grows. That allows more temporal variation where there's activity, while a positive floor keeps every weight above zero.

Chapter 4 uses a different empirical rule, based on energy before normalization. Its weight increases with that energy, and it also has a positive floor. So the two chapters make different design choices. For every fixed positive matrix either rule produces, the quadratic solve is unique. But when the data change and the rule recomputes Lambda, both the data term and the penalty change. The sensitivity of the full adaptive reconstruction has to include both contributions, beyond the fixed-penalty data bound.

### If asked for more

Where the adaptive rule is differentiable, differentiating the normal equations gives two forcing terms: A transpose times the change in the observations, and minus the change in Lambda squared applied to the current solution. Multiplying by the inverse reconstruction matrix turns those into the first-order change in the solution. Absolute values and clipping introduce kinks, but every rule is still Lipschitz, so the local bound on page 98 needs no derivatives. The positive-floor theorem is still useful, because it controls every individual solve the rule produces.

## Backup 26 — A real MVSEC flow example is qualitative

Deck page: 59.

**Likely question:** What does the real-data flow comparison establish?

*[Identify the reference and ground truth first; compare methods only through visible features.]*

### Answer

It's a qualitative comparison on one frame: MVSEC indoor flying 2, frame 0340. The reference image shows the scene, and the ground-truth flow is the visual target. The other panels show the event-accumulation baseline and the time-surface, voxel, and structure-tensor voxel estimates.

Those last three are the representations covered by the common quadratic analysis. They build different coefficient fields from the same kind of event input, so the panels show how those choices change the flow pattern in a real scene. The accumulation baseline is a separate comparison method. Chapter 3 reports no aggregate real-data endpoint error for this comparison, so I describe what's visible in this frame and keep any dataset-level ranking separate.

### If asked for more

Average endpoint error would measure the Euclidean distance between estimated and true velocity at a specified set of valid locations, then aggregate over a stated population. This figure is a single frame, not that experiment. The theorem answers a different question: for coefficient fields meeting its assumptions, the regularized estimate exists, is unique, and depends continuously on the coefficients. Accuracy against true motion comes from evaluation, reported with its own valid set and aggregation rule.

## Backup 27 — Quadratic H¹ regularization and TV answer different questions

Deck page: 60.

**Likely question:** Why choose a quadratic H-one flow model rather than total variation?

*[Point to the quadratic gradient term, then state its smoothing consequence before discussing TV.]*

### Answer

The quadratic model gives one explicit well-posedness analysis that covers all the event-derived representations. Its gradient penalty defines a bilinear form, and the integrated directional-information condition controls the constant velocity component. Together with the gradient term and Poincaré's inequality, that gives H one coercivity. Lax–Milgram then gives a unique solution, and subtracting weak equations gives the coefficient-stability estimates.

The tradeoff is that quadratic smoothing spreads out sharp motion boundaries. Total variation is attractive when preserving jumps matters most, and its natural setting is the space of functions of bounded variation. It would need its own existence, uniqueness, and stability analysis. Within the quadratic framework, the normalized directional tensor is another option: it reduces smoothing across selected density edges, while keeping a positive ellipticity floor and the same coercivity proof.

### If asked for more

The integrated full-rank condition is sufficient for this particular quadratic H one argument. Replacing the gradient penalty with total variation changes how the functional grows, and which compactness and coercivity arguments are available. A squared-residual fidelity can be studied with TV, but the theorem has to address that functional directly. For the signed-linear energy written here, simply substituting TV can even make the energy unbounded below. Stronger fidelity assumptions can give strict convexity and uniqueness in a TV model.

## Backup 28 — Frozen prediction weights are not generally an MM majorizer

Deck page: 61.

**Likely question:** Is the reciprocal-weight iteration a majorization–minimization algorithm?

*[Point to the omitted denominator derivative and explain the derivative-contact requirement.]*

### Answer

Not in general. For majorization–minimization, the frozen objective would have to lie above the state-dependent score and touch it at the current state. For differentiable functions, touching also means matching derivatives. Here the variance proxy depends on the predicted signal, so the derivative of the full score has an extra term from the changing denominator.

The frozen quadratic matches the score's value at the current state, but its derivative treats that denominator as constant. So the term shown remains in the full derivative, and it's generally nonzero. That's why I analyze the method through its frozen-solve map: I prove that a fixed point exists, and that the iteration converges under a sufficient contraction condition. Those are precise properties of the map. A monotone-descent claim for a state-dependent score would need a separate surrogate inequality, or an acceptance rule that actually enforces descent.

### If asked for more

If a differentiable surrogate majorizes the score and touches it at an interior point, their difference has a local minimum of zero there. So the derivative of the difference vanishes, and the derivatives must match. The missing variance derivative violates that necessary condition in general. It does vanish in special cases, such as a zero residual, but that alone gives no global majorizer. The implemented acceptance rule is a different mechanism and can allow small cost increases, so describe its behavior through its actual thresholds.

## Backup 29 — A Gaussian model gives an evidence interpretation of attenuation

Deck page: 62.

**Likely question:** Is there a probabilistic interpretation of the attenuation in the stereo cost?

*[Connect the conditional mean c to the ellipsoid center, then discuss the evidence ratio.]*

### Answer

Yes, for the Gaussian model with fixed common parameters. Read the magnitude and coupling penalties as a Gaussian prior on the two latent profiles, and assume independent unit-variance Gaussian observation noise. After integrating out the profiles, the right observation given the left is Gaussian. Its mean is c, the same shifted center as in the cost ellipsoid, and its covariance is the inverse of two P.

So the model predicts an attenuated profile, rather than necessarily the left observation itself. For a scalar regularizer, that attenuation is diagonal in the temporal observation modes. Comparing the coupled model's evidence with the independent model's leaves the discrepancy term plus a constant that is the same for every candidate. Under these Gaussian assumptions, that explains both the shifted prediction and a possible discrepancy-based comparison.

### If asked for more

Integrating a quadratic Gaussian model produces determinant terms as well as the minimized quadratic cost. With fixed common parameters, the determinants are the same for every candidate, which is what allows this comparison. The prediction operator has eigenvalues between zero and one and is a contraction in the P metric; a Euclidean contraction would need extra structure. The discrepancy alone would favor an ideal equal-profile candidate over distinct competitors, when the coupling is positive and A has full row rank. That's an alternative score, separate from the evaluated stereo method.

## Backup 30 — The implemented estimator has several distinct layers

Deck page: 63.

**Likely question:** How do the individual theorems relate to the complete stereo estimator?

*[Follow the diagram in order; attach each guarantee to its specific box.]*

### Answer

Each guarantee attaches to one layer of the estimator. The estimator first rectifies and motion-compensates the events, then bins and normalizes them. For each candidate disparity, it runs the frozen-weight solve with damping and computes a score at the returned iterate. Spatial masking, averaging, normalization, and semi-global matching then adjust the candidate costs.

The final step picks a disparity from that score list, interpolating around the finest-level minimum, and converts a positive valid disparity to depth. Semi-global matching encourages spatial coherence by penalizing disparity changes along several image paths. The inner uniqueness theorem covers the frozen quadratic solve. The selection and margin theorems cover candidate decisions under their hypotheses. The benchmark tests all the stages together, so its results describe the complete estimator and its scored population.

### If asked for more

A few distinctions inside those layers. Solve weights are clipped; scoring weights are recomputed without clipping. Finite guidance penalties go into averaging, so the preference they create is soft. Picking the minimum of the final finite list is exact relative to that list; whether it's the physically correct match is a separate question. Likewise, path aggregation is its own specified spatial algorithm, rather than an exact solver for a general two-dimensional labeling problem. The reported benchmark includes score-minimum interpolation and leaves out the separate hole-filling and refinement stage.

## Backup 31 — What does the dissertation contribute mathematically?

Deck page: 64.

**Likely question:** What is the mathematical contribution if the proof tools are classical?

*[Use one specific consequence, such as attenuation or integrated directional information, after listing the contributions.]*

### Answer

The contribution is building event-based inverse models and analyzing them with precise assumptions and consequences. For temporal reconstruction, I identify the observation null space, set up a transparent regularized inverse, and derive quantitative guarantees for the fixed-weight solution. For flow, I put several event-derived coefficient constructions into one quadratic framework, and prove well-posedness and stability under explicit directional-information conditions.

For contrast maximization, I separate the coercivity that the spline regularizer supplies from the nonconvex focus term, and prove existence for the full finite-dimensional objective. For stereo, the block structure leads to a profiled-cost decomposition, an explicit attenuation mechanism, selection and robustness conditions, and a separate analysis of the adaptive weights. Classical tools make those arguments possible. The research content is in the event-specific formulations, the hypotheses each representation needs, and the conclusions those hypotheses support.

### If asked for more

Stereo is a good example of why this matters. A unique latent reconstruction at each candidate tells us how the inner solve behaves. The cost decomposition then shows that the candidate comparison also carries monocular regularization bias. The attenuation example exposes that effect, and the separation and margin conditions are sufficient for picking and keeping the right candidate. Similarly, the common flow theorem makes explicit which directional information each event representation must supply, so that one global regularizer determines both velocity components.

## Backup 32 — Literature anchors and where to find the claims

Deck page: 65.

**Likely question:** Which prior work underlies these models and where are your detailed arguments?

*[Use the relevant literature item for the question; refer to the dissertation chapter for proof or protocol details.]*

### Answer

Here are the main connections. For image reconstruction, Rebecq and colleagues learn an event-to-video map; Zhang, Yezzi, and Gallego pose a flow-based image inverse problem; and Antil and Sayre combine events with frames in a bilevel model. Gallego and colleagues' survey covers the sensor and the field. Horn and Schunck give the classical variational flow framework, where a data constraint is coupled to spatial smoothness. Benosman and colleagues develop the timestamp geometry behind event-based visual flow. Weickert and Schnörr establish well-posedness for classical quadratic flow. Gallego, Rebecq, and Scaramuzza introduce contrast maximization, which motivates the separate nonconvex formulation. And the MVSEC paper describes the multivehicle stereo event dataset used for evaluation.

The particular models, assumptions, and results are developed in the dissertation. Chapter 2 covers temporal reconstruction; Chapter 3, the event-derived flow models and the contrast-maximization analysis; Chapter 4, the stereo formulation and selection analysis. The appendix specifies the evaluation protocol. The full proofs and experimental definitions are in the chapters.

### If asked for more

The key distinction is between a framework I build on and a result proved for the models in this dissertation. For example, Horn–Schunck supplies the data-plus-smoothness structure, while the event-derived coefficients and their integrated identifiability assumptions determine how the present theorem applies. The time-surface literature motivates the timestamp geometry, and the crossing assumptions pin down the exact constraint used here. For numerical comparisons, the dissertation's protocol defines the configurations, metrics, and valid scoring populations.

## Backup 33 — Stable estimates can still have regularization bias

Deck page: 66.

**Likely question:** If the reconstruction is unique and stable, how close is it to the true signal?

*[Point to the two error terms in order: bias, then propagated observation noise.]*

### Answer

Stability says how much the estimate moves when the observations change. Accuracy also depends on the bias that regularization introduces. Here I assume a fixed temporal grid, a positive scalar regularization parameter, and observations equal to the exact temporal differences of a reference signal plus additive error.

Substituting that model into the reconstruction formula gives the error identity shown. The first term is regularization bias: the penalty shrinks parts of the reference signal. The second is the observation error passed through the reconstruction operator. Increasing regularization affects both, typically trading more shrinkage for better noise control. The constant component deserves special mention, because temporal differences remove it completely: the penalty selects that baseline, while the observations determine the changes. So the theorem gives a controlled reconstruction map; physical accuracy also depends on the signal, the noise, and the modeling assumptions.

### If asked for more

For a mean-zero reference signal on a fixed grid, exact noiseless difference data recover the signal as the regularization parameter goes to zero, because every nonconstant mode's gain approaches one. With persistent observation noise, weakening the penalty also exposes the problem's sensitivity to that noise. A refinement statement therefore needs joint control of the noise level, the grid spacing, and the regularization. Any mismatch between physical events and the increment model adds another observation-error term.

## Backup 34 — The physical event stream loses more than one baseline

Deck page: 67.

**Likely question:** Does the constant nullspace describe all the information lost by an event camera?

*[Point to the amplitude inequality, then compare the constant and oscillating profiles.]*

### Answer

No. The constant null space is exactly the ambiguity of the discrete first-difference model. The physical threshold sensor loses more, because it reports only threshold crossings rather than every change. This slide gives an explicit example, with the same initial reference for both signals.

The first log intensity is constant. The second oscillates sinusoidally around that value, with amplitude strictly smaller than the contrast threshold. Its change from the reset reference stays inside the threshold the whole time, so both signals produce the same empty event stream. Exponentiating either one gives a positive physical intensity. So even time-varying signals can share an event stream. This matters for reading the reconstruction theorem: it proves uniqueness for the regularized increment surrogate. Connecting that surrogate to the physical signal also takes assumptions about the threshold measurement and about what the representation retains.

### If asked for more

The shared initial reference and the strict amplitude inequality are essential: together they keep the oscillation below threshold at every time. An empty stream makes the ambiguity easy to see. In a nonempty stream, a perturbation can shift event times by moving threshold crossings. A perturbation supported away from the crossings preserves the schedule, provided a positive threshold margin remains throughout its support. That has to be checked for the specific signal and event reference.

## Backup 35 — Integrated directional information is necessary for uniqueness

Deck page: 68.

**Likely question:** Why is positive integrated directional information necessary for unique optical flow?

*[Use the displayed energy identity to distinguish a nonzero linear slope from a flat direction.]*

### Answer

Take the quadratic energy on all H one vector fields, with a positive gradient penalty and a bounded positive semidefinite data matrix field. Suppose the integrated matrix is singular. Then it has a nonzero null vector, c, and positivity forces the data matrix to annihilate c almost everywhere.

Now add any multiple of c to a velocity field. Both quadratic terms stay the same: the gradient is unchanged because c is constant, and the data quadratic has zero curvature in that direction. Only the linear forcing term can change. If its coefficient along c is nonzero, choosing the sign of the multiple sends the energy down without bound. If that coefficient is zero, the energy is constant along the whole family. Either way there's no unique minimizer. So for this unrestricted model, uniqueness requires the integrated matrix to be positive definite.

### If asked for more

The key step uses positive semidefiniteness pointwise. The nonnegative function c transpose B c has zero integral, so it's zero almost everywhere, and the square-root factorization then gives B c equal to zero. In the flat case, any minimizer comes with a whole family of equally good constant shifts; whether a minimizer exists at all is a separate question. Boundary constraints or a magnitude penalty can control the constant direction, and they change the uniqueness criterion accordingly.

## Backup 36 — Coefficient stability is one stage of event-to-flow stability

Deck page: 69.

**Likely question:** How does your stability theorem translate into stability with respect to the raw events?

*[Point first to the coefficient-to-flow arrow, then to the preprocessing arrow.]*

### Answer

The theorem controls the second arrow in this diagram: how the velocity changes when the fitted coefficient fields change. The first arrow covers the event representation, neighborhood selection, and any fitting used to build those coefficients. An event-to-flow theorem would connect the two arrows quantitatively.

That needs two things. First, a metric on event streams. For example, moving one event by a tiny amount of time changes its timestamp only slightly, but how far apart the two streams are depends heavily on the metric. Second, a bound on how that event perturbation changes the coefficient fields, in the norms the variational theorem uses. With a Lipschitz bound for the preprocessing and a shared positive coercivity bound, the two estimates compose. That's a concrete extension: prove representation stability in a suitable event metric, then carry it through the quadratic solve, which is already controlled.

### If asked for more

Take one positive unit event and shift its time by any nonzero amount. The difference of the two point masses has total variation norm two, while their Wasserstein-one distance is just the size of the shift. Hard temporal bins can jump when an event crosses a bin boundary; smoothing with a fixed bandwidth supports a different continuity analysis. That's why the metric and the representation have to be specified before claiming stability for the whole chain from events to flow.

## Backup 37 — Refinement requires a choice of continuum scaling

Deck page: 70.

**Likely question:** How should the temporal regularization parameter change when you refine the time grid?

*[Point to the factors one over h and h before identifying lambda at spacing h.]*

### Answer

That depends on which continuum energy we want to approximate. This slide uses a smooth illustrative model with uniform spacing h. The observations are increments, so each one is h times a sampled derivative-like value, g, and the difference residual also carries a factor of h.

The target energy is one half the integral of the squared derivative residual, plus beta-time squared over two times the integral of the squared signal. The first integral becomes the squared increment residual over two h. The second becomes beta-time squared times h over two, times the sum of squared samples. Multiplying the whole discrete objective by h leaves its minimizer unchanged and puts it in the Chapter 2 form. Matching coefficients then gives lambda at spacing h equal to beta-time times h, where beta-time is the fixed continuum penalty strength. So for this target energy and this observation convention, the penalty scales linearly with the grid spacing.

### If asked for more

This calculation matches coefficients; a convergence proof would also have to control the quadrature, the approximation spaces, and the data errors. Endpoint quadrature may add endpoint weights. Physical event data also raise separate choices: the smoothing bandwidth, and how the noise changes under refinement. Those can lead to a different scaling. The principle is to specify the continuum functional and the units of the observations first, then derive the discrete penalty from them.

## Backup 38 — Strong smoothness selects one constant flow

Deck page: 71.

**Likely question:** What does the optical-flow estimator approach when spatial regularization becomes very strong?

*[Point to the limiting constant and identify the integrated matrix as the quantity controlling the mean.]*

### Answer

It approaches one constant vector. With the domain and coefficients fixed under the unified theorem's assumptions, increasing alpha makes spatial variation more and more expensive, because alpha squared multiplies the gradient energy. The integrated data select the constant: it's the inverse of the integrated matrix B applied to the integral of the forcing b.

That formula has a direct meaning. The data term pools all the directional constraints across the domain, and the constant balances them in aggregate. Positive definiteness of the integrated matrix makes that balance unique. The convergence is in H one, so it controls both the velocity field and its gradient. Very strong regularization therefore gives a spatially uniform compromise set by the data, with local velocity differences progressively suppressed.

### If asked for more

For the proof, subtract the limiting constant and test the weak equation with the difference. The remaining forcing has zero integral, so Poincaré's inequality bounds its pairing by the gradient norm, which gives a gradient bound of order alpha to the minus two. Testing with constant vectors gives an integrated data balance. Positive definiteness of the integrated matrix then controls the mean of the difference, which completes convergence in H one.

## Backup 39 — Transporting a scalar differs from conserving a density

Deck page: 72.

**Likely question:** Why use scalar transport rather than a continuity equation for the event representation?

*[Point to the product-rule term containing the divergence of velocity.]*

### Answer

The two equations make different assumptions about the represented quantity. Scalar transport says a pattern value stays constant along each moving trajectory. A continuity equation treats the quantity as a conserved density, so its value also changes when the flow compresses or expands space.

Expanding the divergence in the continuity equation gives the scalar transport terms plus the represented value times the divergence of the velocity. That extra term is the compression effect. The two equations agree when it's zero, for example in divergence-free flow. Event representations come from threshold-triggered observations and preprocessing, so treating them as a conserved physical density needs an extra model. In the dissertation, scalar transport is the constraint being analyzed. A conservation formulation would need a justification for the density interpretation, and possibly a source term for the creation or loss of events.

### If asked for more

A one-dimensional example separates the two. Let the velocity equal the position, and let the represented value be the constant one. Its time and space derivatives are zero, so scalar transport holds. But the divergence of value times velocity is one, so source-free conservation has a residual of one. A source term of one would balance it. This shows exactly where the compression term enters.

## Backup 40 — Correlation changes uncertainty without removing coercivity

Deck page: 73.

**Likely question:** What changes if the timestamp errors are correlated?

*[Point to the covariance matrix in the sandwich formula, then to the positive regularizer in the temporal matrix.]*

### Answer

Correlation changes the uncertainty, through the full error covariance matrix. For the centered symmetric regression design on this slide, the slope estimate is a linear map of the timestamps. Applying that map to the covariance gives the sandwich formula shown: inverse Q, then the design transpose, the covariance, the design, and inverse Q again. With independent errors of common variance, it reduces to the variance times inverse Q.

The reconstruction question is separate. If a positive definite covariance matrix Gamma is used in a weighted temporal fidelity term, its inverse supplies the precision weights. Adding the positive magnitude penalty keeps the temporal system matrix positive definite. So the regularized solve is still unique, with stability constants that reflect the chosen weights. Correlation affects the uncertainty and the weighting model; coercivity comes from the positive quadratic terms.

### If asked for more

A common error mean cancels from the slope when the design is centered, even with correlated errors. Smoothing changes the covariance to the smoothing operator times the covariance times its transpose. That matrix can be singular, so an inverse-covariance formulation needs either a positive definite covariance or a treatment of its null space. A Gaussian likelihood reading needs a Gaussian assumption on top of that; the covariance identity itself only needs finite second moments.

## Backup 41 — Optical flow: further analysis

Deck page: 74.

*[Navigation only. Silent navigation cue: select the regression or contrast-maximization slide matching the question.]*

## Backup 42 — Time-surface gradient estimation: bias versus variance

Deck page: 75.

**Likely question:** What determines the accuracy of your time-surface gradient estimate?

*[Point to Q for sample geometry, then to the two contributions in the mean squared error.]*

### Answer

Two things: the geometry of the samples, and the curvature of the time surface. The estimator fits a plane to timestamps at nearby spatial offsets, and Q summarizes the geometry of those offsets. If Q is positive definite, the samples span both spatial directions and the fitted slope is determined. With a centrally symmetric design and independent timestamp errors of common mean and variance, the slope covariance is the noise variance times inverse Q.

The bias comes from fitting a plane to a curved surface. Central symmetry cancels the quadratic Taylor term in the slope. A Lipschitz bound on the Hessian controls the remaining cubic error and gives the bias bound shown, which holds for the actual finite set of samples. The mean squared error is then the squared bias plus the trace of the covariance. A larger neighborhood can improve the geometry and reduce the variance, but it also takes in more curvature. That's the bias–variance tradeoff here.

### If asked for more

The design matrix depends on the sample positions. A well-conditioned fit can estimate the time-surface gradient accurately even at a moving straight edge, and the tangential velocity is still free, because one reliable normal constraint fixes only one component of motion. So regression rank and velocity identifiability answer different questions. The uncertainty formula also assumes an explicit timestamp-error model; a model for event counts would need its own derivation.

## Backup 43 — Contrast maximization finds the motion that sharpens the events

Deck page: 76.

**Likely question:** What does contrast maximization model, and why is it worth pursuing?

*[Describe the warp on the left, then point to the CMAX column of the table.]*

### Answer

An edge moving across the sensor produces events all along its path during the time window, so a plain accumulation of those events looks like a smeared trail. Contrast maximization slides each event back along a candidate flow to one reference time. When the candidate matches the true motion, the trail stacks into a sharp edge. Image variance measures that sharpness, so the method searches for the flow that makes the warped event image sharpest.

The method works directly on individual events and their own timestamps. The quadratic models first summarize events as a time surface or in temporal bins, and an edge that moves during a bin blurs that summary. On the known-motion scenes in Chapter Three, contrast maximization has the lowest endpoint error in all three: 0.49 pixels against 2.15 for the structure tensor on idealized stripes, 1.19 against 1.92 on simulated stripes, and 0.32 against 0.98 on the simulated checkerboard. A zero flow field scores 3.00. On the stripes it recovers the diagonal motion, because warping events over the whole window brings in evidence from the object's boundary.

### If asked for more

These numbers come from one representative window, chosen by the rule that minimizes deviation from each method's median error, on simulated scenes with known motion. On the idealized stripes, contrast maximization also assigns flow to the background around the object. The dissertation reports no aggregate real-data endpoint error for any of the flow methods. The guarantee for contrast maximization is that a global minimizer exists; the solver is a local quasi-Newton method. The contrast-maximization objective and existence backups give those details.

## Backup 44 — How the known-motion comparison was evaluated

Deck page: 77.

**Likely question:** How were the flow examples selected, and how fair is the comparison?

### Answer

These are controlled tests of the geometry behind the models. A sixty-by-forty-pixel object translates diagonally by three pixels per evaluation window. The chapter uses idealized events generated directly, and events from the v2e simulator. Stripes emphasize the normal-motion constraint; the checkerboard supplies edge directions along both axes.

All the panels share one arrow scale and one selected window. Window twenty-two minimizes the summed deviation of each variant's endpoint error from that variant's median over windows one through thirty-one. AEE averages the Euclidean displacement error over the scored locations, in pixels per evaluation window. A zero estimate scores three pixels here.

The quadratic variants use alpha equal to twenty, without a pyramid; contrast maximization uses one hundred L-BFGS iterations. The implementations use different spatial stencils, so the same numerical alpha gives different effective smoothing. Their computational budgets also differ.

So the comparison illustrates directional information, and how these implementations behave at these settings. A dataset-level accuracy ranking needs its own evaluation and parameter-calibration protocol.

### If asked for more

VOX uses an eight-neighbor interior stencil, and the structure-tensor implementation uses a conductance-weighted four-neighbor stencil. In the isotropic interior, their continuum smoothing coefficients are alpha squared times h squared over three, and over four, respectively. That describes the stencils only; the full models differ in other ways too.

The separate MVSEC contrast-maximization configuration caps iterations at ten; the controlled figures here use one hundred. The chapter calls the AEE evaluation mask M; the experiment's evaluator defines its exact population. The convergence theorem uses simultaneous block-Jacobi updates with fixed coefficients. The evaluated time-surface implementation uses in-place updates and event-dependent reference times; the convergence backup explains the schedule that's proved.

## Backup 45 — Contrast maximization changes the optimization problem

Deck page: 78.

**Likely question:** How does contrast maximization differ from your quadratic optical-flow model?

*[Point to the warped locations, then identify the ridge lower bound in the regularizer.]*

### Answer

In contrast maximization, the event image itself changes as the motion estimate changes. Each event is warped to a common reference time, and well-aligned events produce a concentrated image. The objective rewards that concentration through image variance, and adds a quadratic regularizer on the motion coefficients.

The motion variable q is displacement over the normalized time window: physical velocity times the window duration. I represent that field with continuous B-splines, so it has a well-defined value at every event location. Because the warp depends on the coefficients, the full objective is generally nonconvex. The regularizer does two separate jobs. Spatial diffusion controls variation across the field, and a positive coefficient ridge controls the overall size of the coefficients, including constant motion. So the existence argument uses finite-dimensional continuity and coercivity.

### If asked for more

Concentration alone can also reward a wrong warp that collapses events together, which is why the regularization and the model restrictions matter. Continuous splines can be evaluated at points; a general two-dimensional H one field is an equivalence class, and needs more regularity before point values make sense. A diffusion penalty controls spatial variation but leaves constant fields free. The coefficient ridge supplies the missing control that the coercivity proof needs.

### If asked why analyze the quadratic family at all

Because the two answer different questions. The quadratic models are where I can prove what the events determine: a unique flow, stable in its coefficients, computed by an iteration that converges, under a condition you can check in the scene — edges in two orientations. That condition is what explains the stripe result. Contrast maximization is more accurate on these tests, but its objective is nonconvex: I can prove a global minimizer exists, and the solver is local. So one tells us when the data identify the motion; the other is a stronger estimator with weaker guarantees.

## Backup 46 — A global minimizer exists, even though the solver is local

Deck page: 79.

**Likely question:** What guarantees that contrast maximization has a global minimizer?

*[Follow the lower bound from bounded focus gain to the positive quadratic ridge.]*

### Answer

Two facts: the focus term is bounded, and the ridge grows. There are finitely many events with fixed weights. Their total absolute weight bounds how much mass bilinear accumulation can put on the image. In particular, both the sum of absolute pixel values and the largest absolute pixel value are bounded by that total weight. Bounding the variance by the second moment gives the focus bound shown.

So the negative variance term is bounded below. Meanwhile, the positive coefficient ridge grows quadratically with the coefficient norm, so the full objective goes to infinity as the coefficients grow without bound. Bilinear accumulation is continuous in the warped locations, so the finite-dimensional objective is continuous too. Its relevant sublevel sets are compact, and the extreme value theorem gives a global minimizer. That proves existence for the model; the local optimizer used in the experiments returns whatever solution its numerical search reaches.

### If asked for more

The continuity holds even when events cross pixel boundaries, because the bilinear tent weights join continuously. Differentiability is only piecewise; that matters for the numerical optimizer, while the existence proof needs only continuity. Coercivity relies on a strictly positive ridge for the fixed discretization; a refinement theorem would need uniform control of that lower bound. The proof gives existence; global uniqueness, or global convergence of a local solver, would need additional structure.

## Backup 47 — Stereo depth: full Chapter 4 arc

Deck page: 80.

*[Navigation only. Silent navigation cue: choose the matching model, selection, IRLS, or benchmark page.]*

## Backup 48 — Stereo depth in one slide: what Chapter 4 adds

Deck page: 81.

**Likely question:** What does Chapter 4 prove beyond the inner solve?

*[Move through the numbered results deliberately.]*

### Answer

Three things: what the candidate cost actually compares, when the correct candidate wins, and when the reweighting converges.

The model takes one temporal profile per view and adds a soft penalty on their difference. For fixed nonnegative observation weights, positive magnitude weights, and nonnegative coupling, the temporal coercivity proof carries over directly, so every frozen inner problem has a unique solution.

The correspondence analysis looks at the unweighted cost for a single candidate, before spatial aggregation. After minimizing over the profiles, that cost has a monocular term for each view plus a coupling discrepancy. The right-view term changes with the candidate. In the exact example, the perfect match costs one third, while an attenuated candidate costs nine fortieths: a right view that's a weaker copy of the left can beat the true match, so the cost favors quieter candidates.

A separation condition guarantees that this model picks the correct candidate. Once the winner has a positive margin, cost errors each smaller than half that margin, say from noise events or mismatched thresholds between the two sensors, leave the winner unchanged.

For the reciprocal reweighting map, a fixed point exists. Under a sufficient contraction condition, it's unique and the iteration converges.

### If asked for more

On the MVSEC benchmark, WLS leads on indoor flying two and narrowly on the aggregate log RMSE, while scoring more pixels than the local adaptation of Piatkowska and colleagues' method. Each method is scored on its own valid pixels. The separation results concern unweighted candidate-local costs before aggregation.

## Backup 49 — Stereo alignment after motion compensation

Deck page: 82.

**Likely question:** Why should two pixel histories agree when the rig and scene are moving?

### Answer

Because, for a proposed correspondence, both pixels watch the same scene point once we account for the motion. The comparison assumes synchronized streams, calibrated rectification, and a scene point visible in both cameras.

The preprocessing also compensates motion within each slice. It fits one global translation separately in each camera and warps the events to the end of the slice. Subtracting the two warped horizontal coordinates gives the equation shown: the original disparity picks up a correction equal to the time to the reference, times the difference of the two horizontal warp velocities.

When the warps agree, the comparison is preserved. A horizontal mismatch changes the disparity the matcher sees; a vertical mismatch moves the correspondence off its row. The reported slices are twelve and a half milliseconds wide, within a quarter-second evaluation window.

The inner positive-definite system gives a unique fit to whatever profiles it receives. Whether that fit reflects the physical correspondence also depends on the timing, calibration, and motion approximation used to build the profiles.

### If asked for more

For simultaneous points that start on the same row, subtracting the warped vertical coordinates gives the time to the reference, times the difference of the vertical warp velocities. A global translation approximates each slice; depth-dependent parallax, changing disparity, and independently moving objects can introduce mismatch.

These translations come from Chapter 4's own preprocessing fit; Chapter 3's dense-flow estimator is a separate study. Soft coupling allows the profiles to disagree, but its penalty still favors agreement. Occlusion removes the visible match, which needs a rejection or visibility treatment beyond the unique inner fit.

## Backup 50 — At each candidate, couple two temporal profiles

Deck page: 83.

**Likely question:** What are the unknowns in the stereo reconstruction model?

*[Point to the two data terms, two magnitude terms, and coupling term in that order.]*

### Answer

For a fixed left pixel and candidate disparity, the unknowns are two temporal feature profiles, one per view. The left observation is fixed, and the right observation is sampled at the candidate disparity. Each profile has its own weighted data-fidelity term, with the same temporal first-difference operator.

There are also two magnitude penalties and a soft coupling term. The magnitude penalties control the temporal baselines, and the coupling penalizes disagreement between the profiles, with gamma setting its strength. During a frozen solve, the weights and the positive diagonal regularizer are fixed, and gamma is nonnegative. The right profile is an auxiliary variable for this left pixel and candidate; each candidate gets its own right-profile solve. Spatial context comes in later, when the candidate costs are aggregated. Because preprocessing transforms the observations, I interpret these unknowns as event-feature profiles.

### If asked for more

Setting both weight matrices to the identity gives the unweighted model used in the explicit selection analysis. With finite coupling, the profiles can differ, at a cost, so the data terms keep information from each view. Absolute calibrated log intensity would need a calibrated observation model linking the processed features to physical units; the candidate-local optimization and its positive-definiteness proof concern the stated feature model.

## Backup 51 — Frozen weights give a unique, stable inner solve

Deck page: 84.

**Likely question:** Why is the stereo solve unique when the weights are frozen?

*[Point to the magnitude terms as the source of the uniform positive lower bound.]*

### Answer

Because with the weights frozen, every direction has positive curvature. For a fixed disparity, fixed positive weights, a positive diagonal regularizer, and nonnegative coupling, the objective is quadratic in the two latent profiles. Its Hessian is the block matrix shown. To show it's positive definite, evaluate its quadratic form on an arbitrary pair of perturbation profiles.

The result is a sum of two weighted difference energies, two magnitude-penalty energies, and the coupling energy of their difference. Every term is nonnegative. More than that, the magnitude terms alone are at least the smallest regularizer entry squared times the squared norm of the stacked perturbation. So every nonzero direction has strictly positive curvature. That gives exactly one global minimizer of the frozen quadratic, and an invertible linear system. Subtracting two such systems also gives stable dependence on the observations, as long as the matrix and weights stay fixed.

### If asked for more

The inverse matrix has norm at most one over the smallest regularizer entry squared. To turn that into an observation-to-solution bound, also include the norm of the weighted observation map on the right-hand side. This theorem is about each inner solve. Candidate selection adds a discrete comparison, and changing the weights changes the quadratic itself; those stages have their own separation and fixed-point analyses.

## Backup 52 — Sum and difference modes expose the coupling

Deck page: 85.

**Likely question:** What does increasing the stereo coupling strength actually do?

*[Point to K in the mean block and K plus twice gamma in the difference block.]*

### Answer

Coupling acts only on the disagreement between the views. When the two temporal blocks are equal, an orthogonal change of coordinates separates the common profile from the difference profile. Adding the normal equations cancels the coupling term; subtracting them adds two gamma to the temporal precision. So coupling suppresses left-right disagreement and leaves the equation for the mean unchanged.

The same decomposition gives an exact condition number in the unweighted case with a scalar magnitude penalty. The smallest full-space eigenvalue is lambda squared, from the shared constant temporal mode. The largest is the largest temporal difference eigenvalue plus lambda squared plus two gamma. Their ratio is the condition number shown. So at fixed lambda, increasing gamma raises the full-space condition number, even as it pulls the views into closer agreement. The mean profile still needs the magnitude penalty to control its baseline.

### If asked for more

The orthogonal transform preserves Euclidean eigenvalues and condition numbers. The simple block diagonalization needs equal temporal blocks; unequal adaptive weights generally mix the mean and difference coordinates. A mean-zero restriction removes the shared constant mode for suitably structured perturbations, and can give a sharper bound. Full-space conditioning still matters, because numerical errors can enter in any direction, so it's useful to keep the two settings separate.

## Backup 53 — Profile out the latent variables to see what disparity compares

Deck page: 86.

**Likely question:** What quantity is actually compared when you choose a disparity?

*[Point to the candidate-dependent right monocular term before the discrepancy term.]*

### Answer

In the unweighted model, I can solve out the two latent profiles exactly. The minimized cost splits into a left monocular cost, a right monocular cost, and a discrepancy term between the two observations. Here m is the minimum regularized temporal reconstruction cost for a single observation vector.

The left monocular term is the same for every candidate. The right monocular term changes with the candidate, and so does the discrepancy. The discrepancy is a nonnegative quadratic in the difference of the observations, passed through the transpose of the temporal operator. Its matrix is the inverse temporal precision minus the inverse precision with two gamma added. This exposes the selection mechanism: a candidate is rewarded both for matching the left observation and for having a low reconstruction cost of its own. Those two pulls can compete, which is why correspondence selection needs its own analysis.

### If asked for more

The derivation completes the square in the stacked latent variables, then uses the sum-and-difference transform to separate the terms. The inverse difference equals two gamma times the product of the two positive inverse matrices, so it's positive semidefinite. An exact winner of these unaggregated profiled costs minimizes the corresponding joint objective over the candidates and the latent variables. Showing that it's the physical match takes assumptions that connect that objective to the true correspondence.

## Backup 54 — A perfect correspondence need not have the lowest cost

Deck page: 87.

**Likely question:** Can the stereo objective favor a wrong correspondence even when the true profiles match exactly?

*[Point to the exact-match point, the one-half point, and their displayed costs. Read the follow-up scalar factors slowly.]*

### Answer

Yes. This two-sample example shows exactly how. The temporal operator takes one difference, both magnitude penalties are the identity, and gamma equals one. The left observation is one, and the right candidate observation is a scalar, b. Solving the latent problem gives the quadratic cost in b shown here.

At the perfect match, b equals one and the cost is one third. At the attenuated candidate, b equals one half and the cost is nine fortieths, which is smaller. Over all b, the minimum is at two sevenths. Attenuation lowers the right monocular cost by more than it adds in discrepancy. Every inner solve here is still strictly convex with a unique solution. So the example isolates the selection problem: inner uniqueness gives a profile for each candidate, and whether the correct candidate wins depends on how their minimized costs compare.

### If asked for more

For an observation scaled by b, the monocular part is one plus b squared, times the left monocular cost. The discrepancy part is one minus b, squared, times the discrepancy coefficient. The derivative at b equal to one is twice the positive monocular cost, so decreasing b slightly lowers the score. This concerns the unweighted local cost before aggregation; the evaluated weighted method has additional steps.

## Backup 55 — Correct disparity needs a separation condition

Deck page: 88.

**Likely question:** What assumptions ensure that the correct disparity wins?

*[Subtract twice the left monocular cost and point to the nonnegative monocular-cost difference and the strictly positive discrepancy.]*

### Answer

A sufficient condition is that every competitor costs at least as much to reconstruct on its own as the left view does. The result concerns a finite candidate set and the unweighted local cost. The positive regularizer is shared by both views and all candidates, and the coupling strength is fixed and strictly positive. At the true candidate, the right observation equals the left observation exactly.

For every competitor, assume its right observation differs from the left, and its own monocular reconstruction cost is at least the left monocular cost. Subtracting the true candidate's cost leaves two parts. The monocular-cost difference is nonnegative by assumption. The discrepancy is strictly positive for a distinct observation, because the temporal difference matrix has full row rank and gamma is positive. Their sum is positive, so every competitor costs more, and the correct candidate wins uniquely. The condition works by ruling out the cost advantage that attenuation provides in the counterexample.

### If asked for more

The condition is sufficient, and it can be stronger than necessary. A competitor with a smaller monocular cost can still lose if its discrepancy is large enough. The more general metric-separation criterion covers that case. Both versions concern ideal matched profiles and candidate-local, unweighted costs. Applying the conclusion after masking, adaptive weighting, or spatial aggregation requires checking that scoring procedure and its assumptions.

## Backup 56 — A winning margin turns cost stability into selection stability

Deck page: 89.

**Likely question:** How much can candidate costs change before the selected disparity changes?

*[Point to the two eta contributions and the strict half-margin condition.]*

### Answer

By just under half the winning margin. Start with a fixed finite candidate set and a unique winner. Delta is the smallest gap between the winner and any competitor. If every candidate cost changes by at most eta, the worst case lowers a competitor by eta and raises the winner by eta, so the gap shrinks by at most two eta.

So whenever eta is strictly less than half of delta, every perturbed gap stays positive and the same candidate wins. That turns a bound on continuous cost perturbations into a statement about a discrete decision. It also shows why a small margin is fragile. If two right candidates have exactly the same temporal observations, and use the same local procedure and parameters, their local costs are equal. That tie can happen even with rich temporal activity; selection stability requires a positive gap between the candidate scores.

### If asked for more

The cost bound must cover the original winner as well as every competitor. At exactly half the margin, the bound allows a tie, so the strict inequality matters. An observation-based estimate can supply eta when the score parameters are fixed and the observation perturbations are controlled. Spatial aggregation can separate candidates using neighboring evidence, so the identical-profile example applies to the local score, rather than to every stereo algorithm that uses spatial context.

## Backup 57 — Depth sensitivity grows with distance

Deck page: 90.

**Likely question:** What does a pixel of disparity error mean for depth accuracy?

### Answer

It depends on distance: the same pixel matters much more far away. Depth is focal length times baseline divided by disparity. With fixed calibration, the exact change under a disparity perturbation is the difference formula on the slide. For a small relative disparity error, the absolute depth sensitivity is depth squared over focal length times baseline. So farther points turn the same disparity error into a larger depth error.

The examples hold calibration fixed and add one pixel of disparity. Going from four to five pixels underestimates depth by twenty percent. Going from twenty to twenty-one underestimates it by about four point seven six percent. These are illustrative calculations.

That's why I read depth error together with the depth range, the disparity precision, and the scored population. A stable winning label is one stage; interpolating it and converting it to depth each add their own sensitivity.

### If asked for more

The approximation needs the disparity error to be small relative to the disparity; the exact identity holds for any positive original and perturbed disparities. If the calibration also changes, the first-order relative depth change is the relative focal-length change plus the relative baseline change, minus the relative disparity change.

On the benchmark, finite in-band estimates and ground truth define each method's scored population; the coverage slides explain that selection. This calculation explains how disparity errors propagate within those populations. Attributing a method's error tails would take a separate analysis of its returned disparities.

## Backup 58 — Heteroscedastic weights: statistical motivation and scope

Deck page: 91.

**Likely question:** Why do you use reciprocal activity weights in stereo?

*[Point to the rate sum in the variance, then to the predicted-activity proxy in the weight.]*

### Answer

Because the noise model treats busy intervals as noisier. A useful starting point is a raw-count model where the positive and negative event counts are independent Poisson variables. Their difference has mean equal to the difference of the two rates, and variance equal to their sum. In a high-count approximation, inverse-variance weighting then motivates a weighted least-squares fidelity term.

The implemented rule uses reciprocal predicted activity plus a positive noise floor. It's a practical variance proxy: high predicted activity gets less weight, and the floor keeps the weight finite near zero. Total and net activity differ here: opposite polarity rates can cancel in the mean, while both still add to the variance. Also, the actual observations have been warped, downsampled, and normalized. So I treat each frozen weighted solve as a Gaussian surrogate for the processed features, with the reciprocal rule supported by the reported weighting comparison.

### If asked for more

The absolute difference of the two polarity rates is at most their sum, with equality exactly when at least one rate is zero. So a variance based only on the net rate adds an approximation. In the iteration, the weights are evaluated at the previous profile and held fixed during the quadratic solve. That keeps the positive-definiteness argument for each solve, and makes the statistical approximation explicit.

## Backup 59 — IRLS: fixed-point existence and conditional convergence

Deck page: 92.

**Likely question:** Does the iteratively reweighted stereo solver converge?

*[Point to the invariant-ball bound for existence, then separately to q less than one for convergence.]*

### Answer

Under an explicit condition, yes. The analysis gives two levels of guarantee for the unclipped reciprocal map, with the disparity, regularizer, and coupling fixed. First, a fixed point exists. Compare each frozen minimizer's objective with its value at zero. The positive magnitude penalty controls the solution's squared norm, and every reciprocal weight is at most one over the noise floor. Together, those put every update inside a sufficiently large closed ball.

The weight map is continuous, and the frozen system stays positive definite, so the update map is continuous. Brouwer's theorem then gives a fixed point. Second, the bound q shown is a sufficient contraction constant. If q is less than one, the fixed point is unique and the updates converge geometrically. That's the explicit parameter condition. All of this describes the analyzed update map; the implementation's stopping and acceptance rules decide when the numerical iteration ends.

### If asked for more

With a fixed damping parameter greater than zero and at most one, the update is a convex combination of the old state and the undamped update. The fixed points stay the same, and the Lipschitz bound becomes one minus omega, plus omega times q. When q is below one, that's still a contraction. When q is one or larger, this bound gives no contraction certificate. A fixed point means consistency with the frozen weights; reading it as a likelihood optimum needs a separate analysis of the objective.

## Backup 60 — Stereo benchmark: read accuracy alongside scored coverage

Deck page: 93.

**Likely question:** How competitive is the stereo method, and how should I interpret the coverage numbers?

*[Identify the centimeter columns, the scaled log metric, and the scored-point column separately.]*

### Answer

It's competitive. Its mean errors are within six centimeters of the Piatkowska adaptation's on every sequence; it leads on Flying 2 and narrowly on the averaged log error; and it's scored on more than twice as many points. The table reports mean absolute depth error in centimeters on four MVSEC indoor sequences, plus an averaged log error and the total number of scored points. Soft-coupled weighted least squares has mean errors of 73.83, 58.35, 70.33, and 59.24 centimeters. Its displayed log RMSE is 44.54, on 2.66 million scored points.

The Piatkowska adaptation has the smaller mean error on the other three sequences. The other three prior methods, Xie, Kogler, and Rogister, trail weighted least squares on every sequence and on the log error. The population sizes matter: the adaptation is scored on 1.20 million points. For each method, a pixel is scored only when both its estimate and the ground truth fall inside the reporting band. So the table compares accuracy together with scored coverage. A direct accuracy comparison would score both methods on the same pixels.

### If asked for more

The reporting band is 0.5 to 8 meters. Point counts are summed across sequences. The displayed log RMSE is one hundred times the base metric, averaged equally over the sequence-level values. A method can produce finite estimates outside the band; those count toward neither the reported error nor the scored total. These are complete implementations, including normalization, regularization, guidance, and activity masking, and the external methods are local adaptations.

## Backup 61 — A weighting comparison supports the selected rule

Deck page: 94.

**Likely question:** What empirical evidence supports the reciprocal weighting rule?

*[Point to the subtraction direction before reading the four positive differences.]*

### Answer

A controlled swap of the weighting rule, with everything else in the configuration held fixed. Each number is the rate-proportional method's reported mean depth error minus the reciprocal-weight method's. The differences are 4.44, 8.28, 2.73, and 5.17 centimeters on Flying 1 through Flying 4. All four are positive, so the reciprocal rule has the smaller reported mean error on every sequence.

That supports the selected rule for these configurations and their scored populations. Each method's evaluation population is defined separately, so the comparison combines its errors with the set of in-band points it returns. These sequences were also used to choose the rule. So I'd call this empirical support for the design choice; a common-pixel evaluation and additional sequences would test how far the advantage extends.

### If asked for more

These are differences of reported mean errors, not paired per-pixel improvements. A shared-population comparison would rescore both outputs on the same valid pixels. Because these sequences also selected the rule, the distinction between selection data and held-out validation matters here. The empirical improvement motivates the implementation choice; a maximum-likelihood interpretation would also need a justified probabilistic model for the processed observations.

## Backup 62 — Hard fusion changes both the constraint and the regularization

Deck page: 95.

**Likely question:** Why does hard fusion perform differently from soft coupling?

*[Compare the magnitude-penalty coefficients after dividing the hard-fusion equation by two.]*

### Answer

Hard fusion changes two things at once. It forces the two profiles to be equal and solves for one shared profile, and the implemented system also uses a different effective magnitude penalty. Dividing its normal equation by two shows half of lambda squared next to the temporal data matrix. By contrast, sending the soft model's coupling strength to infinity, with equal fixed weights and the same regularization, keeps the full lambda squared in the common-profile equation.

Averaged over the four sequences, the reported mean depth error is 102.10 centimeters for hard fusion and 65.44 for soft weighted least squares. That's the observed difference between the two evaluated configurations. But the comparison changes hard equality, effective regularization, weights, iteration budgets, and scored populations together. So it motivates controlled comparisons to find how much each choice contributes to the gap.

### If asked for more

The penalty accounting is the key algebraic point. Substituting one shared profile into the soft energy combines its two half-weighted magnitude penalties into one full squared penalty. The implemented hard-fusion objective uses half that amount. The soft model's mean equation already combines both views, so averaging alone gives no demonstrated explanation for the performance difference. Isolating the effect of hard equality would require matching the other settings and the evaluation population.

## Backup 63 — Motion-induced events and the aperture problem

Deck page: 96.

**Likely question:** Can you derive the aperture problem directly from the event-generating image model?

*[Point to the normal-component equation, then to the arbitrary tangential coefficient in the boxed velocity family.]*

### Answer

Yes. Take a straight edge under steady illumination. Its log intensity is a one-dimensional profile evaluated at the normal position minus the normal speed times time. The spatial gradient points along the edge normal, and the time derivative is minus the normal speed times the profile's derivative.

Substituting those into brightness constancy gives the normal vector dotted with the velocity equal to the edge's normal speed, wherever the profile's derivative is nonzero. Every velocity with that normal component satisfies the same equation, whatever its tangential component. These velocities produce the same local log-intensity histories, and so the same ideal threshold events when their reset references agree. That's the aperture ambiguity in this model: the edge fixes its normal motion and leaves the tangential motion free. This assumes the edge's endpoints and any other distinguishing features lie outside the observation window.

### If asked for more

If the normal speed is zero, the motion is purely tangential, and the pixel values stay constant in the ideal edge interior. With nonzero normal speed, the crossing-time surface has gradient equal to the normal divided by that speed, which recovers the time-surface transport constraint. Steady illumination is assumed to isolate motion. The sensor's threshold rule also responds to changes in illumination, so treating every event as motion needs additional scene assumptions.

## Backup 64 — One complementarity lemma behind the uniqueness results

Deck page: 97.

**Likely question:** The three chapters come from separate papers. Is there one mathematical mechanism behind their uniqueness results?

*[Point to the three hypotheses of the lemma, then read the table one row at a time.]*

### Answer

Yes. Each problem has two quadratic terms. One controls every direction except a small, finite-dimensional set of modes, and the other has to see those modes. If both happen, the sum is coercive, and the coercivity constant falls linearly with how well the second term sees the leftover modes.

In the temporal problem the data see every temporal variation, but they miss the constant baseline; the penalty fixes it. One nonzero weight is enough. Flow reverses the roles. Smoothness controls every variation, but it charges nothing for a uniform pan, so the data have to see the pan; that's the integrated matrix condition. The discrete flow theorem is the same statement on a connected graph. In the stereo inner solve, the two data terms and the coupling leave only a common constant, and the penalty fixes it.

The condition is also necessary. If a leftover mode is invisible to the second term, the quadratic form vanishes there. Backup 02 and Backup 35 are exactly those two cases.

### If asked for more

The proof is one line. Split u into its part in the leftover modes, n, and the rest, w. The square root of a is a seminorm, so a of n is at most twice a of u plus twice beta times the norm of w squared, and r controls the norm of w. Adding the two bounds gives the constant.

The constant explains the scene statements: for flow it falls as m shrinks, which is why the stripe scene is nearly degenerate. Two parts of the dissertation sit outside this lemma. Correspondence selection compares finitely many candidate costs, so it needs a separation margin. Contrast maximization is nonconvex, so compactness gives existence only. Total variation isn't a quadratic form, so neither this lemma nor Lax--Milgram applies to it.

## Backup 65 — Adaptive weights keep the temporal estimate locally Lipschitz

Deck page: 98.

**Likely question:** The temporal theorem fixes the weights, but you compute them from the data. Is the estimator you actually run stable?

*[Point to the subtracted normal equations, then to the two terms of the bound.]*

### Answer

Yes, it's locally Lipschitz, by a short argument. Each Chapter 2 rule maps event activity to a weight between a positive floor and a finite ceiling, and each rule is Lipschitz in the activity. The absolute value, the minimum and the maximum are all Lipschitz, so their kinks need no differentiability.

Subtract the two normal equations. The difference in the solutions equals the fixed-weight term from the change in the data, plus the change in the squared weights acting on the second solution. Three standard bounds finish it. The solution operator has norm at most one over twice the floor. The inverse system matrix has norm at most one over the floor squared. The squared weights change by at most twice the ceiling times L times the change in activity.

The second term grows with the size of the data, so the bound is Lipschitz on bounded sets of data. The table gives the floor, ceiling and Lipschitz constant for the sigmoid, inverse-proportional and exponential rules.

### If asked for more

The constants are pessimistic, because the floor of ten to the minus three enters cubed. The rules decrease with activity, so for data bounded by R the sigmoid floor improves to ten to the minus three plus ten over one plus e to the R. Pixels are independent, so the bound holds pixel by pixel.

Chapter 4 is different. Its observation weights are recomputed from the current profiles, so its estimator is a fixed point and needs the contraction condition in the stereo backups. Chapter 5 lists this as a future direction. The bound covers the step from the represented data to the estimate; connecting it to raw event perturbations is the representation question on slide 32.

## Backup 66 — References (1 of 3)

Deck page: 99.

*[Navigation only. Silent navigation cue: the reference numbers match the dissertation bibliography; each bracketed number in the deck links here. Return with the viewer's back command.]*

## Backup 67 — References (2 of 3)

Deck page: 100.

*[Navigation only. Silent navigation cue: the reference numbers match the dissertation bibliography; each bracketed number in the deck links here. Return with the viewer's back command.]*

## Backup 68 — References (3 of 3)

Deck page: 101.

*[Navigation only. Silent navigation cue: the reference numbers match the dissertation bibliography; each bracketed number in the deck links here. Return with the viewer's back command.]*
