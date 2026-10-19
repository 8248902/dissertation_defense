# Defense rehearsal script

Daniel Blauvelt • Canonical defense • Updated October 19, 2026

This rehearsal script covers all 36 main slides and all 54 backup slides. The main talk is a continuous spoken script. Each substantive backup slide has a likely committee question, a self-contained spoken answer, and a deeper follow-up. The three navigation slides have silent navigation cues. Read ordinary paragraphs aloud; headings, questions, and bracketed italic directions organize rehearsal and are silent.

The main talk contains approximately 6,450 spoken words: about 52–59 minutes at 110–125 words per minute, before pauses and questions. Backup responses are outside that timing. Rehearse the main talk aloud to establish its actual length.

Slide 3 gives the five-stage outline. The footer highlights the current stage; backup footers show their deck page number. This script identifies each backup by its backup number and deck page. The clickable slide index and PDF bookmarks let you jump directly to a main slide or a backup response.

Slide 20 contains embedded animations with play controls. Playback has been checked in Firefox; desktop Acrobat Reader is also supported. Viewers without animation support show first-frame posters. The local aperture-demo.html remains an offline browser alternative.

# Main talk

## Slide 1 — Title

Thank you all for being here. My dissertation develops variational and optimization methods for event cameras, sensors that report only changes in brightness.

One question runs through the whole talk: if all we observe are changes, what can we recover? I'll answer it for three targets: an image, the motion in that image, and depth. Most of the time goes to reconstructing images over time. Then I'll present the main optical-flow result, give a short summary of stereo depth, and close with future directions.

*[Advance.]*

## Slide 2 — What can changes tell us about a scene?

*[Point to the reference image, the accumulated events, and the reconstruction.]*

On the left is an ordinary camera image of an outdoor scene; we keep it there to help recognize the scene. In the middle are the events from fifty milliseconds of the same recording. Blue marks pixels that got brighter, orange pixels that got darker, and purple pixels that did both. On the right is our reconstruction from the events.

Each event says only that the brightness at one pixel changed at one moment. So the middle panel records change and nothing else: it has no record of how bright anything is. To get from the middle panel to the right one, the model has to fill in what the events leave out, starting with a reference brightness level. Regularization makes that choice and balances it against fitting the data.

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

For image reconstruction, Rebecq and colleagues train a recurrent neural network on simulated events. Zhang, Yezzi, and Gallego use optical flow to pose reconstruction as a linear inverse problem, with classical or learned regularization. Antil and Sayre combine events with conventional frames in a bilevel problem that estimates the event thresholds.

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

The same construction also has a continuous-time reading.

## Slide 11 — Continuous time: a distributional initial-value problem

Start with the signed event measure at one pixel. Integrating it gives a staircase, which I'll call the jump primitive: each event is a signed jump, and an initial value sets the overall level.

If we first replace each point mass with a narrow kernel, we get smoothed versions of that staircase. Under the stated assumptions, they converge in L one to the jump primitive as the kernel width goes to zero.

*[Point to the distributional derivative equation.]*

In the sense of distributions, the derivative of the jump primitive is the event measure. The primitive has bounded variation. But any interior jump makes its derivative singular, and that places it outside H one.

Integrating over a bin gives the signed event mass in that bin. The slide assumes no event lands exactly on a bin boundary, so the endpoint convention shown gives the same increments.

This is why the discrete model works with integrated changes. It also shows the baseline ambiguity again: the events fix the jumps, and the initial value is still free.

This staircase is the raw event integral, with no regularization. Next is the regularized estimate that I actually compute.

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

The pictures are a representative example from MVSEC indoor flying four: a reference image, and an event-only reconstruction with sigmoid weights. The table summarizes the kernel comparison over the indoor flying sequences.

The reconstruction makes the scene structure visible. The table reports two things: PSNR, which measures similarity to the reference image, and the condition number of the linear system.

Indoors, the spline and Gaussian kernels give similar PSNR, both above delta binning, with much smaller condition numbers. Outdoors, the ordering changes. So kernel and weight choices affect both reconstruction quality and conditioning, and the best choice depends on the scene.

The kernel changes the observations, and the adaptive weights can then change the matrix we solve. That's how representation choices reach the linear system.

## Slide 17 — Relation to Antil--Sayre bilevel reconstruction

Here's how the temporal method compares with the Antil--Sayre bilevel approach.

*[Indicate the two workflows at the top.]*

In this chapter, the events set activity-based regularization weights, and then we do one fixed convex solve over time.

The bilevel approach uses events together with intensity frames. Its outer optimization adjusts the event-threshold parameters. That's the key difference: their outer variables are thresholds, while my empirical rule chooses the magnitude weights of the temporal profile.

The table compares complete methods that use different inputs and different optimization structures. Indoors, the bilevel approach has higher PSNR; outdoors, the event-only approach is slightly higher. The event-only approach has lower condition numbers in both. So the two formulations trade off reconstruction and conditioning differently.

Their guarantees also answer different questions. The bilevel analysis proves existence, and local uniqueness under additional conditions. The result I've presented gives a unique global minimizer for every fixed positive diagonal.

The main point for this talk is the event-only construction and the explicit role of its regularizer. Now let's see it on several real event streams.

## Slide 18 — Real event data: indoor, high-speed, and orbital scenes

*[Pause so the audience can look at all three columns.]*

These examples apply the same per-pixel reconstruction, with sigmoid weights and events as input, in three very different settings.

On the left is a handheld office sequence. As the camera moves, objects and scene boundaries become recognizable.

In the middle, a bullet strikes a cup. The scene changes very fast, and the reconstruction shows structure from the impact and the breakup.

On the right is orbital imagery from the Falcon Neuro instrument on the International Space Station, showing structure in the Earth scene below.

The lower cup and orbital panels use false color. Color and grayscale are only display choices; the reference brightness level is still the one the model selected.

These are qualitative demonstrations across very different time scales. They show what the event-derived profiles can reveal.

So far, every pixel has been treated on its own. Next, a way to connect the pixels through a shared scene and known motion.

## Slide 19 — Shared motion couples temporal profiles to one scene

Suppose a static scene is described by a vector theta, and we know how the camera moves. Each projection P maps the scene to what the camera sees at one time.

Stack those projections and take temporal differences. The resulting operator, B sub SAR, maps one scene to its predicted changes across the sequence. SAR stands for synthetic aperture radar, which combines a moving sensor's observations into one image of a fixed scene. This model carries that idea over to events.

*[Point to the null-space expression.]*

A scene direction is in the null space when its projections look the same at every time. Constants qualify, because the projections are row-normalized. Which other directions are invisible depends on the projections and the trajectory.

Adding a positive ridge coefficient makes the normal system invertible and gives a stability bound for this fixed-motion linear model. One note on notation: here lambda is the coefficient itself, whereas the earlier temporal matrix contained squared weights.

The reasoning is the same as before, now for a shared scene: find what the observation operator controls, then regularize the directions it leaves free.

Now a different problem, where the unknown is the motion in the image itself.

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

For this slide, assume V obeys a transport equation with constant velocity over the window. Integrate V over a sliding time window to get a.

Integrating the transport equation gives another transport equation, now for a. Its time derivative is the activity entering at the end of the window minus the activity leaving at the start.

The residual is then the spatial gradient of a, dotted with the velocity, plus that time derivative.

The physical assumption here is about transported event activity, which is a different quantity from scene brightness: a steadily bright region can produce very little activity.

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

## Slide 27 — Proof: control the mean and the fluctuation separately

*[Slow down. Point to each line as its role is explained.]*

Write the velocity as its spatial mean plus a zero-mean fluctuation, w. The gradient of w is the same as the gradient of the full field. Physically, the mean is the common drift of the whole field, like a camera pan, and the fluctuation is how motion varies across the image: rotation, zoom, or objects moving separately.

Poincaré's inequality bounds the L two norm of w by its gradient norm. So the smoothness term controls the fluctuation.

That leaves the mean. Smoothness charges nothing for a uniform pan, so the data have to determine it, and one edge orientation fixes only one of its components. Let m be the smallest eigenvalue of the integrated matrix B; it measures how well the scene's edges, taken together, cover every direction of motion. (Replaces: The remaining task is to control the constant mean. Let m be the smallest eigenvalue of the integrated matrix B.) By hypothesis, m is positive. Applying the integrated quadratic form to the mean gives a lower bound of m times the mean's squared size.

To connect this to the energy of the full field, write the mean as v minus w. Apply the square root of B and use the squared triangle inequality. That bounds the mean term by twice the data energy of v, plus twice a B-weighted fluctuation term.

We bound that last term with the upper bound on B and Poincaré's inequality again. That gives the second line.

*[Pause at the coercivity inequality.]*

Now the quadratic energy controls the mean, the fluctuation, and the gradient. Together, they give a positive lower bound in the full H one norm.

The bilinear form is bounded and coercive, so Lax--Milgram gives a unique weak solution. The weak equation is the first-order condition of this strictly convex energy, so its solution is the unique minimizer.

The mechanism is what matters: smoothness controls how motion varies across the image, and edges in different orientations fix the common drift. (Replaces: smoothness controls fluctuations, and integrated data control constants.)

## Slide 28 — Stability follows by subtracting weak equations

The same coercivity estimate also gives stability with respect to the coefficients.

Take two sets of coefficients with common bounds on B and b, and a common positive lower bound on integrated identifiability. Those shared bounds give one coercivity constant that works for both problems.

Subtract the two weak equations, and test with the difference of the solutions. The left side controls the squared H one norm of that difference.

The right side has two parts. One comes from the change in b. The other comes from the change in B, acting on the second solution. Cauchy--Schwarz and the bound on that solution give the final estimate.

*[Point to the two terms in the bound.]*

So small changes in the coefficients produce controlled changes in the flow, as long as identifiability stays uniformly positive. In scene terms, the coefficients change because of timestamp jitter, binning choices, and noise events, and the flow changes in proportion. The constants grow as m shrinks; the stripe scene two slides ahead, dominated by one edge orientation, comes close to that case. (Replaces: As the lower identifiability bound approaches zero, this guarantee deteriorates.)

This is stability with respect to the represented coefficients. Linking it to raw sensor errors, or to the true motion, needs an additional model of the representation error.

## Slide 29 — Discrete flow: connectivity and sampled directions matter

To compute the flow, we discretize on a pixel graph. Each node stores two velocity components. Its data matrix B describes the measured directions, and b carries the corresponding observations. A positive node factor, q, weights that local contribution.

*[Point to the local two-by-two matrix, then to the two terms on the right.]*

At node i, the matrix combines the local data with alpha squared times the weighted degree: the total weight linking the node to its neighbors. Solving this two-by-two system blends the pixel's own edge measurement with its neighbors' previous velocities. (Replaces: The degree is the sum of the neighboring edge weights. On the right, we combine the local observation term with a weighted sum of the previous neighbor velocities. Solving this two-by-two system gives the new velocity at that node.)

Every node uses the same old field. Once all the new velocities are computed, we replace the field and repeat. That simultaneous update is block Jacobi. Each sweep carries information from image edges one more pixel into textureless regions.

For convergence, we assume the graph is connected, its edge weights are symmetric and nonnegative, its degrees and node factors are positive, and each data block is positive semidefinite. If the weighted sum of the data blocks is positive definite, the sweeps converge to the unique discrete minimizer from any starting field.

The reason mirrors the continuous argument: the graph controls variation, and the sampled data control the remaining constant direction. The graph structure also gives the spectral condition this particular iteration needs. The theorem applies when the stencil and update schedule match these hypotheses. The next slide shows velocity estimates on known-motion examples.


## Slide 30 — Known-motion examples make the aperture problem visible

*[Give the audience a moment to compare the two rows.]*

These examples use a known diagonal motion. The top row has a stripe texture, and the bottom row a checkerboard. The true-motion arrows and the estimates share a common scale.

Inside a vertical stripe region, the strong gradients are horizontal, so they mainly constrain the normal motion. In the theorem's terms, this texture gives the integrated matrix little energy along the stripes. In the velocity diagram from earlier, the stripe interior gives only one line. The checkerboard has edges along both axes, so its lines cross. Object boundaries can add directional information as well.

The voxel and structure-tensor columns illustrate the quadratic representations from the talk.

The last column is contrast maximization, an event-alignment method. It warps the events toward a common time and rewards a sharp result. Its nonconvex objective is analyzed separately in Chapter Three.

These are selected simulation windows that illustrate the directional-information argument. A quantitative assessment across real scenes would need a broader evaluation. The purpose here is to connect the geometry of the observations with the conditions in the theorem.

## Slide 31 — Two viewpoints turn correspondence into depth

I'll close the technical part with a short summary of stereo depth.

*[Point to the two cameras and the scene point.]*

Two cameras see the same scene from different positions. After rectification, matching points lie on the same image row. Their horizontal offset is the disparity.

By similar triangles, depth is the focal length times the camera baseline, divided by the disparity. Small disparities mean distant points, so a disparity error matters most at large depths.

For each left pixel, we compare candidate right pixels along the same row. Each candidate gives a right-view temporal signal to pair with the left one.

Here's the stereo model in scene terms. If a left pixel and a right pixel see the same scene point, they see the same changes over time, so their event profiles should agree over the window. For each candidate disparity, the model reconstructs a profile in each view, ties the two together softly, and scores how well one shared explanation fits both streams. Busy intervals have noisier event counts, so the weights trust quiet intervals more. The best-scoring candidate gives the disparity, and from that the depth. So there are two levels: solving for the profiles at a fixed candidate, and then comparing candidates. (Replaces: This creates two levels of estimation. At a fixed candidate, we solve for the latent temporal profiles. We then compare candidates to choose a disparity.)

The model assumes the candidate match holds approximately over the window, with the scene point visible in both views. The key distinction is between solving for the profiles and choosing the match.

## Slide 32 — Stereo depth in one slide: what Chapter 4 adds

*[Move through the numbered results deliberately.]*

The model takes one temporal profile per view and adds a soft penalty on their difference. For fixed nonnegative observation weights, positive magnitude weights, and nonnegative coupling, the temporal coercivity proof carries over directly. The coupling adds a nonnegative term, so every frozen inner problem has a unique solution.

The correspondence analysis then looks at the unweighted cost for a single candidate, before spatial aggregation. After minimizing over the profiles, that cost has a monocular term for each view plus a coupling discrepancy. The right-view term changes with the candidate.

In the exact example, the perfect match costs one third, while an attenuated candidate costs nine fortieths. The attenuated candidate wins because its smaller monocular penalty outweighs the discrepancy. In other words, a right view that's a weaker copy of the left can beat the true match, so the cost favors quieter candidates. (Replaces: The attenuated candidate wins because the reduction in its monocular penalty outweighs the discrepancy cost.)

A separation condition guarantees that this model picks the correct candidate. And once the winner has a positive margin, cost errors each smaller than half that margin, say from noise events or mismatched thresholds between the two sensors, leave the winner unchanged. (Replaces: Once a winner has a positive margin, uniformly perturbing all costs by less than half that margin preserves the winner.)

For the reciprocal reweighting map, a fixed point exists. Under a sufficient contraction condition, it's unique and the iteration converges. Each frozen inner solve keeps its own uniqueness guarantee from the positive-definite quadratic model.

Finally, on the MVSEC benchmark, our weighted least-squares method, WLS, leads on indoor flying two, and narrowly on the aggregate log-RMSE, while scoring more pixels than the local adaptation of Piatkowska and colleagues’ stereo method. Each method is scored on its own valid pixels, so the comparison reflects both accuracy and coverage.

That completes the three estimation problems. I'll finish by bringing their guarantees together.

## Slide 33 — What is proved, and what remains a modeling question

*[Use the table as a recap; avoid reading every cell.]*

For temporal reconstruction, once the positive weights are fixed, we have a unique solution and perturbation bounds. We also know how the penalty selects the baseline.

For flow, spatial smoothness and integrated directional information combine to give a unique, stable field. The discrete theorem gives the matching result for the graph model.

For stereo, solving the inner problem and selecting the correspondence are separate steps, with separate results. Reweighting brings its own assumptions and guarantees.

The dissertation also proves that the regularized contrast-maximization objective has a global minimizer.

The proof tools are classical. The contribution is the analysis of these event-derived models under explicit hypotheses, and what that analysis says about null spaces, conditioning, coupling, and candidate selection.

Those conclusions also point to concrete next questions.

## Slide 34 — Next questions follow directly from the proved bounds

The first is how sensor errors propagate through the representation. The flow theorem starts from perturbations in B and b. The next step is to connect timestamp uncertainty, binning, and smoothing to those perturbations.

Second, the adaptive procedures need an analysis of the full update. Recomputing the weights changes the estimator, so a complete sensitivity or convergence argument has to include those changes and the stopping rules.

Third, stereo margins should be studied for the weighted, aggregated costs that the full method uses. That would connect the ideal single-candidate result to the implemented estimator.

Finally, controlled comparisons can separate modeling effects. Scoring every method on the same pixels and holding other settings fixed would make changes in weighting or coupling easier to interpret.

Each of these has a specific mathematical or experimental target. The next slide connects those targets to research settings.

## Slide 35 — Research opportunities

*[Move through the four boxes, with most time on the first two.]*

One direction is learned temporal regularization. When all the weights are positive, the fixed-weight solution is a smooth function of those weights. That gives a well-defined lower-level solution map for an outer learning problem. Choosing the outer objective, and the data used to fit the weights, would be part of that extension.

A second direction is event-based flow measurement in fluids. A controlled velocimetry setup would let us test how representation choices affect the estimated motion. The coefficient-stability result suggests measuring the representation error and the strength of directional information, alongside the flow error.

For shared-scene and orbital sensing, a concrete question is to characterize the invariant scene modes for a given trajectory. The null-space expression is a starting point for understanding which trajectories constrain which scene directions.

Finally, the stereo work suggests extending the margin analysis to weighting and aggregation, to find when a winning match stays stable under the operations that the full estimator uses.

Each direction builds on a quantity already in the dissertation: a solution map, a stability constant, a null space, and a cost margin.

## Slide 36 — From event changes to well-posed estimators

*[Look up from the screen.]*

I began by asking what we can recover from changes alone.

Temporal reconstruction shows how a penalty selects the baseline. Flow shows how directional observations and spatial coupling together determine a motion field. Stereo shows that a unique inner solution and a reliable match need separate arguments.

Across all three, the common question is which directions the observations control, and which the model chooses.

Thank you. I'm happy to take your questions.

*[Stop. Leave the closing slide visible.]*

# Backup responses

Use these responses when a question calls for the corresponding slide. Start with the answer and expand into the follow-up when useful. Each response defines its own context, so you can enter at any slide. There are no scripted transitions between backup slides.

## Backup 01 — Discussion guide

Deck page: 37.

*[Navigation only. Private navigation only. Choose the relevant technical question from this index; no spoken introduction or audience direction is needed.]*

## Backup 02 — Must every temporal penalty entry be positive?

Deck page: 38.

**Likely question:** Do you really need a positive penalty at every temporal sample?

*[Point first to the kernel intersection, then to the connected-chain null space.]*

### Answer

The exact requirement is that the observation operator and the penalty have no common nonzero null vector. Here, A is the first-difference operator, and Lambda is the penalty operator. The quadratic form of the reconstruction matrix is the squared norm of A applied to a vector plus the squared norm of Lambda applied to that vector. It is strictly positive precisely when those two quantities cannot vanish together for a nonzero vector.

For a connected temporal chain, the null space of A consists of constant profiles. A single nonzero diagonal penalty entry therefore removes the ambiguity. Fixing one reference value or imposing zero mean also selects a unique representative. I use a fully positive diagonal in the theorem because it gives a simple quantitative lower bound as well as uniqueness. A measured reference would additionally supply physical information about the brightness baseline.

### If asked for more

There is a distinction between selecting the constant and regularizing the entire profile. A zero-mean constraint fixes the unobserved offset. A magnitude penalty also attenuates the nonconstant modes and changes their response to noise. With one anchoring penalty, the matrix is positive definite, but the lower bound based on the smallest positive diagonal entry across all samples must be replaced by a bound for that anchored matrix. The kernel-intersection criterion remains the exact algebraic statement.

## Backup 03 — The event measure has a jump primitive

Deck page: 39.

**Likely question:** What is the precise continuous-time interpretation of accumulating events?

*[Indicate the right-closed interval convention, then the two primitives.]*

### Answer

At one pixel, I represent the events as a signed measure: each event contributes an atom at its timestamp, weighted by its polarity. Its cumulative primitive is a step function. Starting from a chosen initial value, I add the signed mass of events between the initial time and the current time. Using intervals that include the right endpoint makes that primitive right-continuous and makes its increments agree exactly with the event measure.

For finitely many events, this primitive has bounded variation. Smoothing the measure with a standard smooth kernel gives a regular temporal driver, and integrating that driver gives a smooth approximation to the cumulative profile. As the kernel width decreases, these primitives converge in L-one for finitely many interior events. This describes the cumulative-event surrogate. The regularized reconstruction then makes a separate choice about fitting those increments and controlling the profile magnitude.

### If asked for more

A nonzero jump has a singular distributional derivative, so the unsmoothed primitive belongs naturally to bounded variation rather than H-one. At positive kernel width, the standard kernels here give an L-two driver and an H-one primitive. The discrete first-difference matrix computes increments. Dividing those increments by the time step would instead approximate a derivative. Keeping that scaling and the interval endpoints consistent is essential when comparing the continuous and discrete descriptions; convergence of these primitives alone establishes no joint grid-and-regularization limit.

## Backup 04 — Latent-signal gain and observation-noise gain are different

Deck page: 40.

**Likely question:** What does regularization do to the signal and to measurement noise?

*[Contrast the first and second table rows before discussing the variance row.]*

### Answer

Those are two related but different transfer functions. In this slide, the penalty is a single positive scalar, lambda, and the observations are unweighted. Let g denote an eigenvalue of A transpose A. If I start with an underlying temporal profile, apply A to form ideal differences, and then reconstruct, that profile mode is multiplied by g divided by the sum of g and lambda squared. Low modes are attenuated most, and the constant mode is set to zero.

If I instead perturb the difference observations, their amplitude gain is the square root of g, divided by the sum of g and lambda squared. For independent white observation noise with variance sigma squared, squaring that gain gives the reconstructed modal variance. This distinction matters because a statement about suppressing low latent modes is different from a statement about how observation noise passes through the inverse.

### If asked for more

The singular-value decomposition makes the calculation explicit: A maps right singular modes of the profile to left singular modes of the observations. The inverse maps back with the observation gain shown here. The variance factor reaches its continuous maximum at g equal to lambda squared, with maximum one over four lambda squared. The finite chain may have a smaller maximum because it has a discrete set of eigenvalues. These exact modal formulas apply to the scalar unweighted model; general diagonal or adaptive weights require the corresponding matrix analysis.

## Backup 05 — Kernel performance depends on the scene and adaptive weights

Deck page: 41.

**Likely question:** Why does changing the temporal kernel change both accuracy and conditioning?

*[Point across the indoor and outdoor columns to show the change in ranking.]*

### Answer

The first-difference operator stays the same, but the represented observations change with the temporal kernel. The adaptive penalty is computed from those observations, so its entries can change as well. That changes the reconstruction matrix and therefore its condition number. The conditioning difference is a property of the resulting adaptive system.

The table also shows a scene-dependent accuracy ranking. Indoors, the B-spline gives PSNR 8.86 and condition number 22.16; the Gaussian gives a very similar PSNR of 8.84 and condition number 20.22. Outdoors, the delta representation has the highest PSNR among these four, at 7.97, with condition number 53.34. Those comparisons support choosing the representation with the scene and weighting rule in mind. Conditioning measures sensitivity of the linear solve; reconstruction accuracy also depends on the represented data and the bias introduced by regularization.

### If asked for more

If I held both A and Lambda fixed, changing the right-hand side alone would leave the matrix condition number unchanged. Here the adaptive penalty provides the link between representation and matrix conditioning. The positive-definiteness theorem applies to every resulting positive fixed penalty. It supplies a guarantee for the solve, while the table compares actual reconstruction outcomes. Reference-image scores evaluate those outcomes against the images; the event observations still leave the absolute temporal offset to the chosen regularization or reference convention.

## Backup 06 — What the reconstruction scores measure

Deck page: 42.

**Likely question:** How is each reconstruction metric computed, and what do the scores establish?

### Answer

**PSNR** starts with mean squared pixel error against a reference image, then takes ten times the base-ten logarithm of the peak-squared to error ratio. **SSIM** combines local means, variances and covariance to compare luminance, contrast and structure. Frame scores are then averaged.

**EPI** correlates the spatial-gradient magnitudes of the mean reconstruction with the normalized event-count map. **ERC** correlates absolute differences between consecutive reconstructed frames with absolute values of the bump-integrated event data.

**TC** takes the root-mean-square consecutive-frame change, divides it by the reconstruction's intensity range, and exponentiates its negative. **TG** averages the absolute consecutive-frame changes over pixels and frame pairs. **TV** averages the sum of absolute horizontal and vertical spatial gradients over pixels and frames.

**SC** takes each frame's Fourier power inside the central low-frequency disk, divides by total Fourier power, then averages across frames. **CN** divides the evaluated matrix's largest singular value by its smallest.

These computations measure different outcomes. A constant sequence has TC equal to one and ERC equal to zero under the stated conventions. Smoothness rewards a static output, so I consider reference fidelity, event consistency and conditioning together.

### If asked for more

For ERC, truncate the reconstructed-change and event-cube sequences to the same number of slices, flatten them, and compute Pearson correlation. EPI also uses Pearson correlation. Zero-variance inputs receive zero correlation. TC is one for a zero-range reconstruction. In SC, an all-zero frame contributes zero power fraction; the disk radius is one eighth of the smaller image dimension.

PSNR and SSIM depend on the scoring normalization; CN describes the specified diagnostic matrix. The event-only baseline choice and regularization affect image agreement as well as smoothness.

## Backup 07 — Can the reconstruction run in real time?

Deck page: 43.

**Likely question:** Can the reconstruction run in real time, and what governs its responsiveness?

### Answer

I developed and used a native C++ and CUDA version in iniVation's DV software for live reconstruction. That gives practical experience with a near-real-time implementation of this approach.

The model is well suited to repeated windowed processing because each pixel has its own temporal problem, and the first-difference operator gives sparse systems. The implementation processes incoming event batches and produces updated reconstructed images.

The operating point depends on the active pixels, event workload, number of temporal samples, event-window length and output cadence. Increasing temporal detail or event context increases the work and can increase delay; settings can instead favor more responsive updates.

The practical answer is therefore live, windowed reconstruction with a controllable processing budget. Fine event timestamps, the spacing of reconstructed times, completed output cadence and camera-to-display latency are separate quantities.

### If asked for more

If asked about the implementation, the native DV module receives events, prepares the active pixels' temporal systems in C++, invokes CUDA and cuSOLVER sparse QR, and returns the latest reconstructed image through the DV frame output. Each selected batch is solved independently.

The module supports both event-count and time-window accumulation. Those choices affect how much data enters each reconstruction and how old the selected events are. Its update interval sets minimum trigger spacing; completed output cadence also depends on processing time and event availability.

The module records processing time around batch selection, reconstruction and frame emission. Camera-to-display latency also includes acquisition, buffering and downstream display. If asked for a specific rate or delay, attach the figure to the native module's settings and workload.

## Backup 08 — The weak equation supplies the natural boundary condition

Deck page: 44.

**Likely question:** Which boundary condition does the flow model use?

*[Move from the variational equation to the interior equation and then the weak boundary trace.]*

### Answer

It uses the natural homogeneous Neumann condition. I minimize over the full H-one space of velocity fields, so the field values on the boundary remain free. Taking the first variation gives the weak equation displayed here for every H-one test field. B is the data coefficient matrix, b is the data forcing, and alpha controls spatial smoothing.

First, choosing test fields supported inside the domain gives the differential equation in the distributional sense. Under the coefficient hypotheses, B times the solution and b are both in L-two, so the solution's distributional Laplacian is in L-two as well. That regularity allows a weak normal trace of its gradient. Returning to general test fields gives zero normal derivative on the boundary in that weak trace sense. This is the appropriate boundary statement on the Lipschitz domains used by the theorem.

### If asked for more

The final step is generalized Green's identity. Its boundary pairing must vanish against the trace of every H-one test field. Since the trace map reaches the boundary trace space, the normal trace is zero. For a fixed anisotropic diffusion tensor, the same argument applies to the flux: the normal component of D times the gradient is zero. That is a conormal boundary condition. The weak formulation uses the bounded tensor directly and requires no classical derivative of D.

## Backup 09 — Why block-Jacobi converges for this graph model

Deck page: 45.

**Likely question:** Why does block-Jacobi converge for your discrete flow system?

*[Explain the two signs in the energy identity before pointing to the spectral interval.]*

### Answer

The proof uses the graph structure of this particular system. The graph is connected, its edge weights are symmetric and nonnegative, and the sampled data blocks are positive semidefinite with a positive-definite sum. D contains each node's weighted degree and data block; R contains the couplings between neighboring nodes. Positive alpha and positive degrees make D positive definite.

The key is to prove that both D minus R and D plus R are positive definite. Their quadratic forms are sums of nonnegative data terms and squared differences or squared sums across edges. Connectedness reduces their possible zero modes to constant or alternating constant fields, and the data blocks eliminate those modes. After scaling by D to the minus one-half, these two inequalities place every eigenvalue of the symmetric coupling matrix strictly between minus one and one. That gives convergence of simultaneous Jacobi sweeps.

### If asked for more

For D minus R, a zero edge contribution forces neighboring vectors to agree, hence a single constant vector on the connected graph. For D plus R, neighbors must be opposites. A bipartite graph allows an alternating copy of one vector; an odd cycle forces that vector to zero. In either case, the positive-definite sum of data blocks removes a surviving nonzero vector. The Jacobi matrix is similar to the scaled symmetric matrix, so it has the same spectrum. This proof concerns the simultaneous update schedule.

## Backup 10 — Anisotropy needs a uniform ellipticity floor

Deck page: 46.

**Likely question:** How can directional smoothing preserve the well-posedness theorem?

*[Use the two eigenvalues to distinguish tangent smoothing from normal smoothing.]*

### Answer

The diffusion tensor needs a uniform positive lower eigenvalue bound. Here I use the normalized Nagel–Enkelmann form built from the spatial gradient of event density. The gradient points across a density edge; its perpendicular points along the edge. The tensor has eigenvalue one along the tangent and a smaller positive eigenvalue along the normal.

That reduces the penalty on changes in the flow across a density edge while retaining smoothing along it. The positive parameter gamma supplies a floor. When the density gradient is bounded, the formula gives one common positive lower bound, theta, throughout the domain. The coercivity proof then works with alpha squared times theta in place of alpha squared. The directional model therefore retains the same type of existence and uniqueness argument under the integrated data-identifiability condition, with a quantitative dependence on that ellipticity floor.

### If asked for more

A pointwise positive eigenvalue can approach zero across the domain, so the proof specifically uses a uniform floor. Bounded density gradient and positive gamma give that floor explicitly here. If the tensor is recomputed when the data change, the stability estimate must also account for the change in D in the essential-supremum norm. The directional interpretation is tied to event-density edges. Their relationship to actual motion boundaries is a modeling choice, and the theorem guarantees solvability for the specified tensor.

## Backup 11 — A variable diffusion tensor must stay inside the divergence

Deck page: 47.

**Likely question:** Can the anisotropic operator be implemented by weighting the second derivatives?

*[Point to the coefficient-derivative terms, then to the affine example.]*

### Answer

For a spatially varying tensor, the divergence form includes both second derivatives of the field and first derivatives of the tensor coefficients. Applying the product rule gives all the terms on this slide. Keeping only the tensor-weighted Hessian would describe the correct operator when the tensor is constant, or when the additional coefficient terms vanish.

The example makes the distinction concrete. Take event density equal to x squared over two, gamma equal to one, and the test field u equal to x. The tensor becomes diagonal, with first entry one over one plus x squared. The field has zero second derivatives, but its flux changes with x because that tensor entry changes. Differentiating the flux gives minus two x divided by the square of one plus x squared. A discretization must capture that spatially changing flux to approximate the stated variational model.

### If asked for more

The weak formulation is useful when D is merely bounded and measurable. It uses the integral of the test-field gradient paired with D times the solution gradient. Classical coefficient derivatives then need not be introduced at all. A flux-based discretization can approximate this divergence structure directly. The affine test field here is a simple consistency check: its constant gradient still produces a varying flux, so the computed operator should reflect that variation.

## Backup 12 — The regression radius formula is a heuristic

Deck page: 48.

**Likely question:** Is the regression-radius formula an optimal choice of neighborhood?

*[Identify the increasing bias term and decreasing variance term before discussing the radius.]*

### Answer

It optimizes a leading approximation to the finite-design error bound. The assumptions are a complete disk on a square lattice, a radius large relative to the lattice spacing, and a smooth time surface throughout that disk. L-H measures how rapidly the Hessian can change, sigma is the timestamp-noise standard deviation, and h is the lattice spacing.

The leading squared-bias term grows as radius to the fourth power, while the variance term decreases as its reciprocal. Balancing them gives the displayed radius: noisier data favor more averaging, whereas faster curvature variation favors a smaller neighborhood. I use that scaling as a principled guide. For an actual finite neighborhood, the exact lattice sums provide the appropriate bound. The admissible radius must also keep the whole fitting disk within the region where the smoothness assumptions apply.

### If asked for more

Differentiating a positive expression of the form A times r to the fourth plus B times r to the minus fourth gives r to the eighth equal to B over A. Substituting these coefficients yields the factor shown. The asymptotic remainder has no prescribed sign, so the leading expression alone is not an upper bound for every finite design. For an affine time surface, the curvature bias is zero and adding samples reduces variance; this model then supplies no finite bias–variance balancing radius.

## Backup 13 — Uniform projection and OLS slope need not be transport partners

Deck page: 49.

**Likely question:** Why must the temporal slope and spatial projection use compatible weights?

*[Point to the common temporal weight and then the cubic residual.]*

### Answer

They enter the same transport equation, so their averaging rules must match if that equation is to remain exact. The ordinary least-squares temporal slope can be written as a weighted average of the temporal derivative. Its weight is the parabola shown here: it is zero at the endpoints and largest near the center of the time interval.

If I integrate the transport equation with that weight, the spatial term must use the same weighted projection. Pairing the OLS slope with a uniform temporal projection instead introduces the displayed residual. The transported cubic example gives a residual of one-tenth even though the underlying field satisfies exact transport. This distinguishes two questions: whether the chosen coefficient fields define a well-posed reconstruction problem, and whether those coefficients exactly represent the physical transport relation. The abstract flow theorem answers the first question for coefficients satisfying its hypotheses.

### If asked for more

Integration by parts in the OLS formula produces the parabolic derivative weight. Uniform averaging and that weight agree on their zeroth and first temporal moments, which makes lower-degree tests less revealing. For transported polynomials through degree two, the transport residual mismatch vanishes. The cubic is therefore a useful explicit example of the derivative inconsistency. If the resulting coefficient error is controlled in the norms used by the stability theorem and the identifiability bound remains positive, that theorem bounds its effect on the reconstructed flow.

## Backup 14 — Mean-zero conditioning removes the unobserved mode

Deck page: 50.

**Likely question:** Can a mean-zero formulation avoid poor conditioning as lambda becomes small?

*[Point to the excluded k equals zero mode and the new smallest eigenvalue.]*

### Answer

Yes, in the scalar unweighted model, removing the constant temporal modes gives a conditioning bound that remains finite as lambda approaches zero. The first-difference operator annihilates constants, and the right-hand side has zero mean in each view. The scalar system preserves that mean-zero subspace, so for positive lambda the solution already lies in it.

On that subspace, the smallest temporal eigenvalue is g-one rather than zero. The sum and difference blocks therefore have eigenvalues g-k plus lambda squared, and g-k plus lambda squared plus twice gamma, with the constant mode excluded. The ratio shown gives the exact restricted condition number. Its denominator stays positive at lambda zero. This makes a mean-zero parameterization useful for the algebraic solve while keeping the convention about the unobserved brightness baseline explicit.

### If asked for more

The bound is uniform in lambda for a fixed temporal grid and fixed coupling. Its grid dependence remains important: g-one is asymptotic to pi squared divided by n squared for the unscaled chain. Thus the lambda-uniform bound grows quadratically with the number of samples. The full-space matrix at lambda zero retains a constant null mode, so a numerical implementation must actually preserve the mean-zero restriction to use the restricted guarantee. General diagonal penalties or unequal weights require their own matrix bounds.

## Backup 15 — The selection theorem has an exact ellipsoid interpretation

Deck page: 51.

**Likely question:** Can you characterize exactly which competing stereo profiles beat the ideal match?

*[Explain inside, boundary, and outside using the completed-square expression.]*

### Answer

For the candidate-local unweighted model, the answer is an ellipsoid in observation space. I hold the positive regularizer and coupling fixed across candidates, and assume the ideal candidate has the same right profile as the left observation. S is the monocular cost matrix, T is the coupling-discrepancy matrix, and P is their sum.

Completing the square writes the cost gap as the squared P-distance from the candidate profile to a center c, minus rho squared. P defines the metric, so the equal-cost surface is an ellipsoid. The ideal match lies on its boundary. A competitor inside that ellipsoid has lower cost; a competitor outside has higher cost. This gives an exact geometric description of the attenuation effect, and it also yields a useful sufficient selection rule: every mismatch larger than twice rho in the P-norm loses to the ideal match.

### If asked for more

Let the mismatch be the left observation minus the competing right observation. The cost gap is its squared P-norm minus a linear term involving S. Cauchy–Schwarz in the P inner product bounds that linear term by twice rho times the mismatch norm. The resulting lower bound is positive whenever the mismatch norm exceeds twice rho. The exact ellipsoid test is sharper because it retains direction as well as distance. Both statements concern the fixed unweighted candidate cost before spatial aggregation.

## Backup 16 — An observation perturbation bound can protect a disparity winner

Deck page: 52.

**Likely question:** How much observation noise can the stereo decision tolerate?

*[Indicate that the maximum includes the winner, then the half-margin condition.]*

### Answer

A positive winning margin gives a quantitative answer for a fixed candidate list and fixed model parameters. Here I hold the left observation, A, Lambda, and gamma fixed, and perturb each right candidate profile. The cost is quadratic in that right observation. Its gradient is twice P times the displacement from c, and its Hessian is twice P.

The operator norm of P is at most one-half. Expanding the quadratic therefore bounds each cost change by the candidate's distance from c times the perturbation size, plus one-half the perturbation size squared. Eta is the largest such bound across all candidates, including the original winner. If eta is smaller than half the original winning margin, every competitor remains more expensive. This protects the discrete selection even though the formerly ideal right profile may also be perturbed.

### If asked for more

The factor of two in the margin condition comes from two possible changes: the winner's cost can rise by eta while a competitor's falls by eta. Subtracting the perturbed scores leaves at least the original margin minus twice eta. For this observation bound, the quadratic expansion is exact. If preprocessing, left data, or adaptive parameters change as well, their contributions must be included in the score-perturbation estimate. The same elementary margin argument then applies to whatever uniform score bound has been established.

## Backup 17 — How the reciprocal IRLS contraction bound is obtained

Deck page: 53.

**Likely question:** Where does the sufficient IRLS contraction constant come from?

*[Follow the difference identity through the operator, residual, and weight estimates.]*

### Answer

I compare two frozen-weight solves generated by two input states. B-time is the block-diagonal temporal difference operator for the two views. Subtracting the normal equations isolates the difference in the solutions as an inverse-system operator applied to a weight difference times a residual.

Three estimates control that expression. First, the positive regularizer gives an inverse-operator bound involving ell, the square of the smallest penalty entry. Second, comparing the frozen optimum with zero bounds its weighted residual by the weighted data norm. Third, reciprocal weights have a controlled increment because the change in an absolute value is bounded by the change in its argument, and every weight is at most one over epsilon. Combining these estimates gives q on the slide. When q is below one, the frozen-solve map is a contraction and its iterates converge geometrically to a unique fixed point.

### If asked for more

The reciprocal-weight estimate uses a weighted residual rather than a separate unweighted residual bound. That is what produces the epsilon to the minus three-halves dependence. The change in predicted temporal differences is bounded by the norm of A times the change in the state, supplying the remaining operator factor. This is a sufficient global bound for the unclipped reciprocal map. If it reaches or exceeds one, it provides no contraction conclusion; an actual convergence claim then requires another argument or an additional sufficient condition on the map.

## Backup 18 — A converged frozen-weight iteration need not be maximum likelihood

Deck page: 54.

**Likely question:** Does convergence of the reweighted iteration imply a maximum-likelihood estimate?

*[At the fixed point, show that the residual term vanishes while the log-variance derivative remains.]*

### Answer

A frozen-weight fixed point and a likelihood optimum solve different derivative equations when the variance depends on the unknown state. The scalar example shows this directly. Take a positive observation y and variance equal to the absolute prediction plus a positive epsilon. With the variance frozen, every least-squares problem has its minimum at the prediction y, so the iteration reaches that fixed point immediately.

For the full Gaussian negative log-likelihood, the variance changes with the prediction and contributes a log-variance term. At the prediction y, the residual is zero, but the derivative of that log-variance term is positive: one divided by twice the quantity y plus epsilon. A small decrease in the prediction therefore decreases the likelihood objective locally. This example explains precisely why the fixed-point theorem supports a statement about the iterative map, while likelihood optimality requires differentiation of the full state-dependent objective.

### If asked for more

This scalar illustration deliberately has no regularizer, which keeps the mechanism transparent. It establishes the distinction between two claims rather than serving as an instance of the positive-penalty temporal theorem. The dissertation also gives a two-sample temporal example with positive regularization where a fixed point differs from a stationary point of the final-state-weighted score, even before adding the Gaussian log term. The empirical estimator is evaluated as the specified surrogate procedure, with its own objective and stopping rules.

## Backup 19 — What the implemented IRLS procedure returns

Deck page: 55.

**Likely question:** What does one candidate-level IRLS call actually return?

*[Walk through the five steps, emphasizing the different solve and scoring weights.]*

### Answer

It returns the last accepted latent iterate and its computed score. The procedure starts from the exact unweighted solve. At each iteration it forms predicted-rate weights, clips them for the linear solve, and freezes them. The resulting system is positive definite. The algorithm solves it and takes a damped step toward that frozen minimizer.

For scoring, it recomputes the weights at the proposed state using the unclipped rule, then applies the acceptance and stopping criteria. The score uses the weighted residual and regularization terms, with no Gaussian log-variance contribution. This description matters because clipping, damping, and stopping are part of the evaluated estimator. After these candidate-level computations, masking, averaging, margin normalization, and semi-global matching modify the candidate comparisons. The fixed-map existence and contraction results explain their specified reweighting map; the experimental results assess the complete implemented procedure.

### If asked for more

The solve and score weights play different roles. Clipping controls the matrix used for the update; recomputing unclipped weights defines the score used to assess the proposal. A stopping rule can return an accepted iterate before it reaches a fixed point. Later, finite penalty values used for guidance or rejection participate in averaging, so they produce a soft preference rather than a hard feasibility constraint. Final winner selection exactly minimizes its computed score list, while path aggregation supplies the spatial context for that list.

## Backup 20 — Depth evaluation distinguishes returned coverage and scored coverage

Deck page: 56.

**Likely question:** Does WLS achieve its better scores by returning estimates at many more pixels?

*[Contrast the first two numeric columns before discussing the scored-point totals.]*

### Answer

The table distinguishes returned coverage from the population used for accuracy scoring. First, ground truth must be finite and within the reporting band. Returned coverage then counts finite estimates at those locations. Scoring additionally requires the estimate itself to fall between 0.5 and 8 meters.

The control returns finite estimates at 50.17 percent of the eligible locations, and WLS at 49.48 percent. Those returned coverages are similar. The larger difference is in estimate-side retention within the reporting band: 51.54 percent for the control and 96.40 percent for WLS. That yields 1.43 million scored points for the control and 2.66 million for WLS. The result is a substantially larger scored population with WLS, alongside comparable returned coverage. These are complete configurations, so the comparison includes their preprocessing, weighting, and final masking choices.

### If asked for more

A finite depth outside the band is excluded by the evaluation convention; it may still correspond to a physically possible depth. That is why returned coverage, in-band retention, and accuracy answer different questions. The benchmark's raw outputs include interpolation of the finest-level score minimum and exclude the separate posterior refinement operator. Reading the error values together with these population counts keeps the interpretation precise. A common-population accuracy comparison would use the same eligible pixels for both methods.

## Backup 21 — Pooled kurtosis does not establish heavy-tailed active errors

Deck page: 57.

**Likely question:** Does the large pooled residual kurtosis justify a heavy-tailed noise model?

*[Point to the single active-probability factor in both moments and its effect in their ratio.]*

### Answer

It motivates looking more closely at the residual population. This simple mixture explains why. Suppose a fraction of pixels has exactly zero residual, while the remaining residuals are zero-mean Gaussian with variance sigma squared. The Gaussian component itself has ordinary Gaussian tails. Nevertheless, pooling it with the point mass at zero produces excess kurtosis equal to three divided by the active fraction, minus three.

As the zero fraction grows, that pooled kurtosis grows. Event-free pixels can contribute exactly zero fitted transport residuals, so sparsity alone can create this effect. Regularized fitting, unequal variances, and temporal dependence also influence the residual distribution. I would therefore interpret the pooled diagnostic alongside the event-active residuals and their variance scaling. That distinguishes concentration at zero from the tail behavior of the active errors and gives a better basis for choosing an observation model.

### If asked for more

The moment calculation is direct. Only the active Gaussian component contributes to the second and fourth moments, so both receive one factor of the active probability. Dividing the fourth moment by the square of the second leaves the reciprocal of that probability. A useful follow-up analysis would report the zero fraction, standardize active residuals by their variance, and compare with synthetic residuals passed through the same fitting procedure. Robust penalties remain possible choices, but their benefit needs evidence beyond this pooled moment alone.

## Backup 22 — Adaptive temporal weights are fixed in the theorem

Deck page: 58.

**Likely question:** How do the adaptive temporal penalties relate to the fixed-weight theorem?

*[Contrast the activity-decreasing Chapter 2 rules with the energy-increasing Chapter 4 rule.]*

### Answer

The theorem applies after the adaptive rule has supplied a positive penalty matrix. In Chapter 2, the sigmoid, inverse-proportional, and exponential rules reduce the magnitude penalty as the chosen event-activity measure grows. This allows more temporal variation where the representation indicates activity, while maintaining a positive floor.

Chapter 4 uses a different empirical rule based on pre-normalization energy. Its weight increases with that energy and is also bounded below by a positive floor. The two chapters therefore make distinct design choices. For each resulting fixed positive matrix, the relevant quadratic solve has the stated uniqueness guarantee. When the input data change and the rule recomputes Lambda, both the data term and the penalty can change. Describing the sensitivity of that complete adaptive reconstruction requires including both contributions, rather than using only the fixed-penalty data bound.

### If asked for more

On a differentiable part of the adaptive rule, differentiating the normal equations gives two forcing terms: A transpose times the observation change, and minus the change in Lambda squared applied to the current solution. Multiplication by the inverse reconstruction matrix converts those into the first-order solution change. Absolute values and clipping introduce kinks, so a full global sensitivity analysis must handle those pieces explicitly. The positive-floor theorem remains useful because it controls each individual solve produced by the rule.

## Backup 23 — A real MVSEC flow example is qualitative

Deck page: 59.

**Likely question:** What does the real-data flow comparison establish?

*[Identify the reference and ground truth first; compare methods only through visible features.]*

### Answer

This slide gives a qualitative comparison on MVSEC indoor flying 2, frame 0340. The reference image shows the scene, and the ground-truth flow provides the visual target. The remaining panels show the event-accumulation baseline and the time-surface, voxel, and structure-tensor voxel estimates.

The three latter representations are the ones connected by the common quadratic flow analysis. They construct different coefficient fields from the same kind of event input, so the panels let us inspect how those choices affect the spatial flow pattern in a concrete scene. The event-accumulation baseline is a separate comparison method. This example supports that visual assessment; Chapter 3 does not report an aggregate real-data average endpoint error for this comparison. I would therefore describe what is visible in the selected frame and keep a dataset-level numerical ranking separate from this figure.

### If asked for more

Average endpoint error would require measuring the Euclidean difference between estimated and ground-truth velocity at a specified set of valid locations and then aggregating over a stated population. This figure supplies a single frame, not that aggregate experiment. The mathematical theorem answers another question: for coefficient fields satisfying its assumptions, the regularized estimate exists, is unique, and depends continuously on those coefficients. Physical accuracy against ground-truth motion is established through evaluation, so it should be reported with its own valid set and aggregation rule.

## Backup 24 — Quadratic H¹ regularization and TV answer different questions

Deck page: 60.

**Likely question:** Why choose a quadratic H-one flow model rather than total variation?

*[Point to the quadratic gradient term, then state its smoothing consequence before discussing TV.]*

### Answer

The quadratic model gives a common, explicit well-posedness analysis for the event-derived representations. Its gradient penalty defines a bilinear form, and the integrated directional-information condition controls the constant velocity component. Together with the gradient term and Poincare's inequality, that produces H-one coercivity. Lax–Milgram then gives a unique solution, and subtracting the weak equations yields coefficient-stability estimates.

That choice has a practical consequence: quadratic smoothing spreads sharp motion transitions. Total variation is attractive when preserving jumps is a priority, and its natural setting is the space of functions of bounded variation. It would need its own existence, uniqueness, and stability analysis. The normalized directional tensor offers another option within the quadratic framework: it reduces smoothing across selected density edges while retaining a positive ellipticity floor and the corresponding coercivity proof.

### If asked for more

The integrated full-rank condition is sufficient for the specific quadratic H-one argument. Replacing the gradient penalty with total variation changes the functional's growth and the available compactness and coercivity arguments. A residual-square fidelity can be studied with TV, but the resulting theorem must address that functional directly. For the abstract signed-linear energy written here, simply substituting TV can even allow the energy to be unbounded below. Stronger fidelity assumptions can support strict convexity and uniqueness in a TV model.

## Backup 25 — Frozen prediction weights are not generally an MM majorizer

Deck page: 61.

**Likely question:** Is the reciprocal-weight iteration a majorization–minimization algorithm?

*[Point to the omitted denominator derivative and explain the derivative-contact requirement.]*

### Answer

A general majorization–minimization claim would require the frozen objective to lie above the state-dependent score and touch it at the current state. For differentiable functions, that contact also requires matching derivatives. Here the variance proxy depends on the predicted signal, so differentiating the full score produces an extra term from the changing denominator.

The frozen quadratic matches the score value at the current state, but its derivative holds that denominator constant. The displayed term therefore remains in the full derivative and is generally nonzero. This explains why I analyze the method through its frozen-solve map: I prove fixed-point existence and convergence under a sufficient contraction condition. Those are precise properties of the map. Any monotonic-descent statement for a state-dependent score would require a separate surrogate inequality or an acceptance rule that actually enforces that descent.

### If asked for more

If a differentiable surrogate majorizes the score and touches it at an interior point, their difference has a local minimum of zero there. Its derivative must therefore vanish, forcing equal derivatives. The missing variance derivative violates that necessary condition in general. It vanishes in special cases, such as a zero residual, but that does not establish a global majorizer. The implemented acceptance rule is another mechanism and can allow small cost increases, so its behavior should be described using its actual thresholds.

## Backup 26 — A Gaussian model gives an evidence interpretation of attenuation

Deck page: 62.

**Likely question:** Is there a probabilistic interpretation of the attenuation in the stereo cost?

*[Connect the conditional mean c to the ellipsoid center, then discuss the evidence ratio.]*

### Answer

Yes, for the fixed common-parameter Gaussian model. Interpret the magnitude and coupling penalties as a Gaussian prior on the two latent profiles, and use independent unit-variance Gaussian observation noise. After integrating out the profiles, the conditional right observation given the left is Gaussian. Its mean is c, the same shifted center that appears in the cost ellipsoid, and its covariance is the inverse of twice P.

This means the model's conditional prediction is centered on an attenuated profile rather than necessarily on the left observation itself. For a scalar regularizer, that attenuation is diagonal in the temporal observation modes. Comparing the coupled model's evidence with the independent model's evidence leaves the discrepancy term plus a candidate-independent constant. That gives a probabilistic interpretation of both the shifted prediction and a possible discrepancy-based comparison, within the stated Gaussian assumptions.

### If asked for more

Integrating a quadratic Gaussian model produces determinant terms as well as the minimized quadratic cost. With common fixed parameters, those determinants are constant across candidates, which permits this comparison. The prediction operator has eigenvalues between zero and one and is contractive in the P metric; a Euclidean-norm contraction requires additional structure. The discrepancy alone would favor an ideal equal-profile candidate over distinct competitors when coupling is positive and A has full row rank. That is a mathematical alternative score, separate from the evaluated stereo pipeline.

## Backup 27 — The implemented estimator has several distinct layers

Deck page: 63.

**Likely question:** How do the individual theorems relate to the complete stereo estimator?

*[Follow the diagram in order; attach each guarantee to its specific box.]*

### Answer

The estimator has several layers, and the guarantees apply to the corresponding mathematical objects. It first rectifies and motion-compensates events, then bins and normalizes them. For each candidate disparity, it runs the frozen-weight solve and damping procedure and computes a score at the returned iterate. Spatial masking, averaging, normalization, and semi-global matching then modify the candidate costs.

The final selection chooses a disparity from that computed score list, with interpolation around the finest-level minimum, and converts positive valid disparity to depth. Semi-global matching encourages spatial coherence by penalizing disparity changes along multiple image paths. The inner uniqueness theorem establishes a unique frozen quadratic solve. Selection and margin theorems address candidate decisions under their hypotheses. The benchmark evaluates all these stages together, so its results describe the complete estimator and its scoring population.

### If asked for more

There are several useful distinctions within those layers. Solve weights are clipped, while scoring weights are recomputed without clipping. Finite guidance penalties participate in averaging, making the resulting preference soft. Choosing a minimum of the final finite list is exact relative to that list; physical correspondence accuracy is a separate property. Likewise, path aggregation is its specified spatial algorithm rather than an exact solution of a general two-dimensional labeling problem. The reported benchmark includes score-minimum interpolation and excludes the separate hole-filling and refinement stage.

## Backup 28 — What does the dissertation contribute mathematically?

Deck page: 64.

**Likely question:** What is the mathematical contribution if the proof tools are classical?

*[Use one specific consequence, such as attenuation or integrated directional information, after listing the contributions.]*

### Answer

The contribution is the construction and analysis of event-based inverse models with precise assumptions and consequences. For temporal reconstruction, I identify the observation null space, formulate a transparent regularized inverse, and derive quantitative guarantees for the fixed-weight solution. For flow, I put several event-derived coefficient constructions into one quadratic framework and prove well-posedness and stability under explicit directional-information conditions.

For contrast maximization, I separate the coercivity supplied by the spline regularizer from the nonconvex focus term and establish existence for the full finite-dimensional objective. For stereo, the block structure leads to a profiled-cost decomposition, an explicit attenuation mechanism, selection and robustness conditions, and a separate adaptive-weight analysis. Classical tools make those arguments possible. The research content lies in the event-specific formulations, the hypotheses that each representation requires, and the conclusions those hypotheses actually support.

### If asked for more

The stereo analysis is a concrete example of why that work matters. A unique latent reconstruction at each candidate says how the inner solve behaves. The cost decomposition then shows how the candidate comparison also includes monocular regularization bias. The attenuation example exposes its effect, while the separation and margin conditions provide sufficient conditions for selecting and retaining the desired candidate. Similarly, the common flow theorem makes clear exactly which directional information each event representation must supply for the same global regularizer to determine both velocity components.

## Backup 29 — Literature anchors and where to find the claims

Deck page: 65.

**Likely question:** Which prior work underlies these models and where are your detailed arguments?

*[Use the relevant literature item for the question; refer to the dissertation chapter for proof or protocol details.]*

### Answer

There are several main literature connections. For image reconstruction, Rebecq and colleagues learn an event-to-video map, Zhang, Yezzi, and Gallego formulate a flow-based image inverse problem, and Antil and Sayre combine events with frames in a bilevel model. Gallego and colleagues' event-vision survey provides the sensor and field overview. Horn and Schunck supply the classical variational flow framework, where a data constraint is coupled to spatial smoothness. Benosman and colleagues develop the timestamp geometry used in event-based visual flow. Weickert and Schnörr establish well-posedness theory for classical quadratic optical flow. Gallego, Rebecq, and Scaramuzza introduce the contrast-maximization framework that motivates the separate nonconvex formulation. The MVSEC paper describes the multivehicle stereo event-camera data used for evaluation.

The dissertation develops the particular inverse models, assumptions, and results presented here. Chapter 2 contains temporal reconstruction; Chapter 3 contains the event-derived flow models and contrast-maximization analysis; Chapter 4 contains the stereo formulation and selection analysis. The appendix specifies the evaluation protocol. The chapters contain the full proofs and experimental definitions.

### If asked for more

The important distinction is between a framework I build on and a result established for the model in this dissertation. For example, the Horn–Schunck structure supplies the data-plus-smoothness organization, while the event-derived coefficients and their integrated identifiability assumptions determine how the present theorem applies. The time-surface literature motivates timestamp geometry, and the crossing assumptions specify the exact constraint used here. For numerical comparisons, the dissertation's protocol defines the evaluated configurations, metrics, and valid scoring populations.

## Backup 30 — Stable estimates can still have regularization bias

Deck page: 66.

**Likely question:** If the reconstruction is unique and stable, how close is it to the true signal?

*[Point to the two error terms in order: bias, then propagated observation noise.]*

### Answer

Stability controls how much the estimate moves when its observations change. Accuracy also depends on the bias introduced by regularization. Here I assume a fixed temporal grid, a positive scalar regularization parameter, and observations equal to the exact temporal differences of a reference signal plus additive error.

Substituting that observation model into the reconstruction formula gives the displayed error identity. The first term is the regularization bias: the penalty shrinks components of the reference signal. The second term is the observation error passed through the reconstruction operator. Increasing regularization changes both terms, typically exchanging more shrinkage for stronger noise control. The constant component is especially important because temporal differences remove it completely. The penalty selects that baseline, while the observations determine the measured changes. So the theorem establishes a controlled reconstruction map; physical accuracy additionally depends on the signal, noise, and modeling assumptions.

### If asked for more

For a mean-zero reference signal on a fixed grid, exact noiseless difference data recover that signal as the regularization parameter tends to zero. Every nonconstant temporal mode then has a gain approaching one. With persistent observation noise, weakening the penalty also exposes the inverse problem's sensitivity. A refinement statement therefore needs joint control of the noise level, grid spacing, and regularization. Any mismatch between physical events and the increment model contributes an additional observation-error term.

## Backup 31 — The physical event stream loses more than one baseline

Deck page: 67.

**Likely question:** Does the constant nullspace describe all the information lost by an event camera?

*[Point to the amplitude inequality, then compare the constant and oscillating profiles.]*

### Answer

The constant nullspace describes exactly the ambiguity of the discrete first-difference model. The physical threshold sensor has additional ambiguity because it reports threshold crossings rather than every temporal change. This slide gives an explicit example with the same initial reference for both signals.

The first log-intensity stays constant. The second oscillates sinusoidally around that value, with amplitude strictly smaller than the contrast threshold. Its change from the reset reference stays inside the threshold throughout the interval, so both signals generate the same empty event stream. Exponentiating either log-intensity gives a positive physical intensity. Thus even time-varying signals can share an event stream. The distinction matters when interpreting the reconstruction theorem: it establishes uniqueness for the regularized increment surrogate. Connecting that surrogate to the physical signal also requires assumptions about the threshold measurement and the information retained in the representation.

### If asked for more

The initial reset reference and the strict amplitude inequality are essential. They ensure that the oscillation stays below threshold at every time. This example uses an empty stream, which makes the ambiguity transparent. For a nonempty stream, perturbations can alter event times by moving threshold crossings. A perturbation supported away from crossings can preserve the schedule when a positive threshold margin remains throughout its support. That requires checking the specific signal and event reference.

## Backup 32 — Integrated directional information is necessary for uniqueness

Deck page: 68.

**Likely question:** Why is positive integrated directional information necessary for unique optical flow?

*[Use the displayed energy identity to distinguish a nonzero linear slope from a flat direction.]*

### Answer

Consider the stated quadratic energy on all vector fields in the Sobolev space H one, with a positive gradient penalty and a bounded positive semidefinite data matrix field. If the integrated matrix is singular, it has a nonzero null vector, which I call c. Positivity then implies that the data matrix annihilates c almost everywhere.

Adding any constant multiple of c to a velocity field leaves both quadratic terms unchanged. The spatial gradient is unchanged because c is constant, and the data quadratic sees zero curvature in that direction. Only the linear forcing term can change the energy. If its coefficient along c is nonzero, choosing the sign of the multiple drives the energy downward without bound. If that coefficient is zero, the energy is constant along the entire family. Consequently, a unique minimizer requires the integrated matrix to be positive definite for this unrestricted model.

### If asked for more

The key step uses positive semidefiniteness pointwise. The nonnegative function c transpose B c has zero integral, so it equals zero almost everywhere. Its square-root representation then gives B c equal to zero. In the flat case, every existing minimizer has a family of equally good constant shifts; existence is a separate issue. Boundary constraints or a magnitude penalty can control that constant direction, so they change the uniqueness criterion.

## Backup 33 — Coefficient stability is one stage of event-to-flow stability

Deck page: 69.

**Likely question:** How does your stability theorem translate into stability with respect to the raw events?

*[Point first to the coefficient-to-flow arrow, then to the preprocessing arrow.]*

### Answer

The theorem controls the second arrow in this diagram: how the estimated velocity changes when the fitted coefficient fields change. The first arrow includes event representation, neighborhood selection, and any fitting used to construct those coefficients. An event-to-flow theorem would connect the two stages quantitatively.

The first requirement is a metric on event streams. For example, moving one event by a very small time changes its timestamp slightly, but its distance depends strongly on the chosen metric. The second requirement is a bound showing how that event perturbation changes the coefficient fields in the norms used by the variational theorem. With a Lipschitz preprocessing bound and a shared positive coercivity bound, the two estimates compose. This identifies a concrete extension of the analysis: establish representation stability in a suitable event metric, then carry it through the already controlled quadratic solve.

### If asked for more

For one positive unit event, shifting its time by any nonzero amount gives a total variation norm of two for the difference of the corresponding atomic measures. Their mass-one Wasserstein distance is the magnitude of the time shift. Hard temporal bins can change discontinuously when an event crosses a bin boundary. Fixed-bandwidth smoothing can support a different continuity analysis. These examples explain why the metric and representation must be specified before asserting stability of the complete pipeline.

## Backup 34 — Refinement requires a choice of continuum scaling

Deck page: 70.

**Likely question:** How should the temporal regularization parameter change when you refine the time grid?

*[Point to the factors one over h and h before identifying lambda at spacing h.]*

### Answer

The scaling follows from the continuum energy we choose to approximate. This slide uses a smooth illustrative model with uniform spacing h. The observations are increments, so each observed increment is h times a sampled derivative-like quantity. The difference residual therefore also carries a factor of h.

Approximating the integral of the squared derivative residual gives a discrete squared-increment residual divided by h. Approximating the integral of the squared signal gives h times the sum of its squared samples. Multiplying the complete discrete objective by h preserves its minimizer and puts it in the form used for the temporal reconstruction. Matching coefficients then gives lambda at grid spacing h equal to beta time multiplied by h. Beta time is the fixed continuum penalty strength. This provides a concrete scaling law for this particular target energy and observation convention.

### If asked for more

This calculation matches coefficients; a convergence proof would additionally control the quadrature, approximation spaces, and data errors. Endpoint quadrature may introduce endpoint weights. Physical event data also raise separate choices about smoothing bandwidth and how noise changes under refinement. Those choices can lead to a different scaling problem. The useful principle is to specify the continuum functional and the units of the observations first, then derive the discrete penalty from that model.

## Backup 35 — Strong smoothness selects one constant flow

Deck page: 71.

**Likely question:** What does the optical-flow estimator approach when spatial regularization becomes very strong?

*[Point to the limiting constant and identify the integrated matrix as the quantity controlling the mean.]*

### Answer

With the domain and coefficient fields fixed under the unified theorem's assumptions, increasing alpha drives the velocity toward one constant vector. Alpha squared multiplies the gradient energy, so spatial variation becomes increasingly expensive. The remaining constant is selected by the integrated data: it is the inverse of the integrated matrix B applied to the integral of the forcing b.

That formula has a direct interpretation. The data term combines all the available directional constraints across the domain, and the constant vector balances those constraints in aggregate. Positive definiteness of the integrated matrix makes that balance unique. The convergence is in the H one norm, so it controls both the velocity field and its gradient. Strong regularization therefore produces a spatially uniform compromise determined by the data, with local velocity differences progressively suppressed.

### If asked for more

For the proof, subtract the limiting constant and test the weak equation with that difference. The residual forcing has zero integral. Poincare's inequality bounds its pairing by the gradient norm, giving a gradient bound proportional to alpha to the power minus two. Testing with constant vectors also gives an integrated data balance. Positive definiteness of the integrated matrix then controls the mean of the difference, completing convergence in H one.

## Backup 36 — Transporting a scalar differs from conserving a density

Deck page: 72.

**Likely question:** Why use scalar transport rather than a continuity equation for the event representation?

*[Point to the product-rule term containing the divergence of velocity.]*

### Answer

The equations encode different assumptions about the represented quantity. Scalar transport says that a pattern value stays constant along a moving trajectory. A continuity equation treats the quantity as a conserved density, whose value also changes when the flow compresses or expands space.

Expanding the divergence in the continuity equation produces the scalar transport terms plus the represented value multiplied by the divergence of velocity. That extra term accounts for compression. The equations agree when this product is zero, including divergence-free flow. Event representations arise from threshold-triggered observations and preprocessing, so treating them as a conserved physical density requires an additional model. In the dissertation, the scalar transport relation provides the constraint being analyzed. A conservation formulation would require a justification for the density interpretation and, potentially, a source term describing the creation or loss of events.

### If asked for more

A simple one-dimensional example separates the assumptions. Let velocity equal position and let the represented value be constantly one. The scalar's temporal and spatial derivatives are zero, so scalar transport is satisfied. The divergence of value times velocity is one, so source-free density conservation has a residual of one. A source term of one would balance that example. This shows exactly where the compression contribution enters the model.

## Backup 37 — Correlation changes uncertainty without removing coercivity

Deck page: 73.

**Likely question:** What changes if the timestamp errors are correlated?

*[Point to the covariance matrix in the sandwich formula, then to the positive regularizer in the temporal matrix.]*

### Answer

Correlation changes the uncertainty calculation through the full error covariance matrix. For the centered symmetric regression design on this slide, the slope estimate is a linear map of the timestamps. Applying that linear map to the covariance gives the sandwich formula displayed here: inverse Q, then design transpose, covariance, design, and inverse Q. Independent errors with common variance reduce it to variance times inverse Q.

The deterministic reconstruction question is separate. If we use a positive definite covariance matrix Gamma in a weighted temporal fidelity term, its inverse supplies the precision weights. Adding the positive magnitude penalty makes the temporal system matrix positive definite. Therefore the regularized solve remains unique, with stability constants reflecting the chosen weights. Correlation affects uncertainty and the weighting model; the coercivity argument follows from the positive quadratic terms.

### If asked for more

A common error mean cancels from the slope when the design is centered, even if the errors are correlated. Smoothing changes the covariance to the smoothing operator times the original covariance times its transpose. That matrix can be singular, so an inverse-covariance formulation requires a positive definite covariance or an appropriate treatment of its nullspace. A Gaussian likelihood interpretation additionally requires a Gaussian modeling assumption; the covariance identity itself only needs finite second moments.

## Backup 38 — Optical flow: further analysis

Deck page: 74.

*[Navigation only. Silent navigation cue: select the regression or contrast-maximization slide matching the question.]*

## Backup 39 — Time-surface gradient estimation: bias versus variance

Deck page: 75.

**Likely question:** What determines the accuracy of your time-surface gradient estimate?

*[Point to Q for sample geometry, then to the two contributions in the mean squared error.]*

### Answer

The estimator fits a plane to timestamps at nearby spatial offsets. Q summarizes the geometry of those offsets. Positive definiteness of Q means the samples span both spatial directions, so the fitted slope is determined. Under a centrally symmetric design and independent timestamp errors with a common mean and variance, the slope covariance is the noise variance multiplied by inverse Q.

The bias comes from fitting a plane to a curved time surface. Central symmetry cancels the quadratic Taylor contribution to the slope. A Lipschitz bound on the Hessian controls the remaining cubic Taylor error and gives the displayed finite-design bias bound. The mean squared error is then the squared bias plus the trace of the covariance. Increasing the neighborhood can improve the geometric information and reduce variance, while also including more curvature. That is the bias-variance tradeoff captured here.

### If asked for more

The design matrix depends on sample positions. A well-conditioned fit can accurately estimate the time-surface gradient even around a moving straight edge. That still leaves tangential velocity free, because one reliable normal-direction constraint is only one component of motion. Regression rank and velocity identifiability therefore answer different questions. The stated uncertainty formula also assumes the timestamp-error model explicitly; it does not follow automatically from a model for event counts.

## Backup 40 — Contrast maximization finds the motion that sharpens the events

Deck page: 76.

**Likely question:** What does contrast maximization model, and why is it worth pursuing?

*[Describe the warp on the left, then point to the CMAX column of the table.]*

### Answer

An edge moving across the sensor produces events all along its path during the time window, so a plain accumulation of those events looks like a smeared trail. Contrast maximization slides each event back along a candidate flow to one reference time. When the candidate matches the true motion, the trail stacks into a sharp edge. Image variance measures that sharpness, so the method searches for the flow that makes the warped event image sharpest.

The method works directly on individual events and their own timestamps. The quadratic models first summarize events as a time surface or in temporal bins, and an edge that moves during a bin blurs that summary. On the known-motion scenes in Chapter Three, contrast maximization has the lowest endpoint error in all three: 0.49 pixels against 2.15 for the structure tensor on idealized stripes, 1.19 against 1.92 on simulated stripes, and 0.32 against 0.98 on the simulated checkerboard. A zero flow field scores 3.00. On the stripes it recovers the diagonal motion, because warping events over the whole window brings in evidence from the object's boundary.

### If asked for more

These numbers come from one representative window, chosen by the rule that minimizes deviation from each method's median error, on simulated scenes with known motion. On the idealized stripes, contrast maximization also assigns flow to the background around the object. The dissertation reports no aggregate real-data endpoint error for any of the flow methods. The guarantee for contrast maximization is that a global minimizer exists; the solver is a local quasi-Newton method. The contrast-maximization objective and existence backups give those details.

## Backup 41 — How the known-motion comparison was evaluated

Deck page: 77.

**Likely question:** How were the flow examples selected, and how fair is the comparison?

### Answer

These are controlled tests of the geometry behind the models. A sixty-by-forty-pixel object translates diagonally by three pixels per evaluation window. The chapter uses directly generated idealized events and events generated by the v2e simulator. Stripes emphasize the normal-motion constraint; checker texture supplies spatial directions along both axes.

The panels share one arrow scale and one selected window. Window twenty-two minimizes the summed deviation of each variant's endpoint error from that variant's median over windows one through thirty-one. AEE averages the Euclidean displacement error over scored locations, in pixels per evaluation window. A zero estimate scores three pixels here.

The quadratic variants use alpha equal to twenty without a pyramid, while contrast maximization uses one hundred L-BFGS iterations. These are specified solver settings. The implementations use different spatial stencils, so equal numerical alpha values give different effective smoothing strengths. Their computational budgets also differ.

The comparison supports an illustration of directional information and the behavior of these implementations at those settings. A dataset-level accuracy ranking needs its own evaluation and parameter-calibration protocol.

### If asked for more

VOX uses an eight-neighbor interior stencil, while the structure-tensor implementation uses a conductance-weighted four-neighbor stencil. In the isotropic interior their continuum smoothing coefficients are alpha squared times h squared divided by three and by four, respectively. This describes their stencil contributions; their full models differ in other ways as well.

The separate MVSEC contrast-maximization configuration uses a ten-iteration cap. The controlled figures here use one hundred. The chapter denotes the AEE evaluation mask by M; its construction needs the experiment's evaluator to answer an exact population question. The convergence theorem uses simultaneous block-Jacobi updates with fixed coefficients. The evaluated time-surface implementation uses in-place updates and event-dependent reference times; the convergence backup explains the proved schedule.

## Backup 42 — Contrast maximization changes the optimization problem

Deck page: 78.

**Likely question:** How does contrast maximization differ from your quadratic optical-flow model?

*[Point to the warped locations, then identify the ridge lower bound in the regularizer.]*

### Answer

Contrast maximization changes the represented event image as the motion estimate changes. Each event is warped to a common reference time, and aligned events tend to produce a concentrated image. The objective rewards that concentration through image variance and adds a quadratic regularizer on the motion coefficients.

The motion variable q is displacement measured over the normalized time window. It equals the physical velocity multiplied by the window duration. I represent that field with continuous B-splines so its value is well-defined at every event location. Because the warp depends on those coefficients, the complete objective is generally nonconvex. The regularizer has two distinct roles: spatial diffusion controls variation across the field, while a positive coefficient ridge controls the overall coefficient magnitude, including constant motion. The existence argument for this formulation therefore uses finite-dimensional continuity and coercivity.

### If asked for more

Concentration alone can also reward an incorrect warp that collapses events, which is why the regularization and model restrictions matter. Continuous splines provide valid point evaluations; a general two-dimensional H one field is an equivalence class and needs more regularity for prescribed-point evaluation. A diffusion penalty controls spatial variation but leaves constant fields free. The coefficient ridge supplies the missing control needed for the coercivity proof of this complete objective.

## Backup 43 — A global minimizer exists, even though the solver is local

Deck page: 79.

**Likely question:** What guarantees that contrast maximization has a global minimizer?

*[Follow the lower bound from bounded focus gain to the positive quadratic ridge.]*

### Answer

There are finitely many events with fixed weights. Their total absolute weight bounds the amount of mass that bilinear accumulation can place on the image canvas. In particular, both the image's sum of absolute pixel values and its largest absolute pixel value are bounded by that total weight. Bounding variance by the second moment gives the focus bound shown here.

The negative variance term therefore has a finite lower bound. Meanwhile, the positive coefficient ridge grows quadratically with the coefficient norm. The full objective tends to infinity as the coefficients become arbitrarily large. Bilinear accumulation is continuous in the warped locations, so the finite-dimensional objective is continuous as well. Its relevant sublevel sets are compact, and the extreme-value theorem supplies a global minimizer. This proves existence for the model; the evaluated local optimization procedure returns the solution reached by its numerical search.

### If asked for more

The continuity statement includes pixel-boundary crossings because the bilinear tent weights join continuously. Differentiability is piecewise, which matters for numerical optimization but is stronger than what the existence proof needs. Coercivity relies on a strictly positive ridge for the fixed discretization. A refinement theorem would need uniform control of that lower bound. The proof establishes existence; global uniqueness or global convergence of a local solver would require additional structure.

## Backup 44 — Stereo depth: full Chapter 4 arc

Deck page: 80.

*[Navigation only. Silent navigation cue: choose the matching model, selection, IRLS, or benchmark page.]*

## Backup 45 — Stereo alignment after motion compensation

Deck page: 81.

**Likely question:** Why should two pixel histories agree when the rig and scene are moving?

### Answer

The stereo model compares temporal profiles for a proposed correspondence. That comparison assumes synchronized streams, calibrated rectification, and a scene point visible in both cameras.

The preprocessing also compensates motion within each slice. It fits one global translation separately in each camera and warps events to the slice end. Subtracting the two warped horizontal coordinates gives the displayed equation: the original disparity acquires a correction equal to the time to the reference multiplied by the difference of the horizontal warp velocities.

Compatible warps preserve the intended comparison. A horizontal mismatch alters the disparity presented to the matcher; a vertical mismatch moves the correspondence away from its row. The reported slices are twelve and a half milliseconds wide within a quarter-second evaluation window.

The inner positive-definite system gives a unique fit to the profiles it receives. Physical correspondence also depends on the timing, calibration, and motion approximation used to build those profiles.

### If asked for more

For simultaneous points originally on the same row, subtracting the warped vertical coordinates gives the time to the reference multiplied by the difference of the vertical warp velocities. Global translation approximates each slice; depth-dependent parallax, changing disparity, and independently moving objects can introduce mismatch.

These translations come from Chapter 4's own preprocessing fit. Chapter 3's dense-flow estimator is a separate study. Soft coupling permits profile disagreement, but its penalty continues to favor agreement. Occlusion removes the visible mate and requires a rejection or visibility treatment beyond the unique inner fit.

## Backup 46 — At each candidate, couple two temporal profiles

Deck page: 82.

**Likely question:** What are the unknowns in the stereo reconstruction model?

*[Point to the two data terms, two magnitude terms, and coupling term in that order.]*

### Answer

At a fixed left pixel and candidate disparity, the unknowns are two temporal feature profiles, one for each view. The left observation is fixed, while the right observation is sampled according to the candidate disparity. Each profile has its own weighted data-fidelity term using the same temporal first-difference operator.

There are also two magnitude penalties and a soft coupling term. The magnitude penalties control the temporal baselines. The coupling penalizes disagreement between the two profiles, with gamma setting its strength. During a frozen solve, the weights and positive diagonal regularizer are fixed, and gamma is nonnegative. The right profile is an auxiliary variable for this particular left pixel and candidate. A different candidate gets its own right-profile solve. Spatial context enters later through aggregation of candidate costs. Because preprocessing transforms the observations, I interpret these unknowns as event-feature profiles.

### If asked for more

Setting both weight matrices to identity gives the unweighted model used for the explicit selection analysis. Finite coupling allows the profiles to differ while charging for that difference. The data terms therefore retain information from each view. Absolute calibrated log-intensity would require a calibrated observation model linking the processed features to physical units; the candidate-local optimization and its positive-definiteness proof concern the stated feature model.

## Backup 47 — Frozen weights give a unique, stable inner solve

Deck page: 83.

**Likely question:** Why is the stereo solve unique when the weights are frozen?

*[Point to the magnitude terms as the source of the uniform positive lower bound.]*

### Answer

For a fixed disparity, fixed positive weights, a positive diagonal regularizer, and nonnegative coupling strength, the objective is a quadratic in the two latent profiles. Its Hessian is the block matrix shown here. To establish positive definiteness, evaluate its quadratic form on an arbitrary pair of perturbation profiles.

The result is the sum of two weighted difference energies, two magnitude-penalty energies, and the coupling energy of their difference. Every term is nonnegative. More strongly, the magnitude terms are at least the smallest regularizer entry squared times the squared norm of the stacked perturbation. Every nonzero direction therefore has strictly positive curvature. This gives exactly one global minimizer of the frozen quadratic and an invertible linear system. Subtracting two such systems also gives stable dependence on the observations when the matrix and weights stay fixed.

### If asked for more

The inverse matrix norm is at most the reciprocal of the smallest regularizer entry squared. To turn that into an observation-to-solution bound, one also includes the norm of the weighted observation map on the right-hand side. This theorem concerns each inner solve. Candidate selection adds a discrete comparison, and changing the weights changes the quadratic itself. Those stages have their own separation and fixed-point analyses.

## Backup 48 — Sum and difference modes expose the coupling

Deck page: 84.

**Likely question:** What does increasing the stereo coupling strength actually do?

*[Point to K in the mean block and K plus twice gamma in the difference block.]*

### Answer

When the two temporal blocks are equal, an orthogonal change of coordinates separates the common profile from the disagreement profile. Adding the normal equations removes the coupling term. Subtracting them adds twice gamma to the temporal precision. Thus coupling suppresses left-right disagreement while leaving the equation for their mean unchanged.

The same decomposition gives an exact conditioning formula in the unweighted case with a scalar magnitude penalty. The smallest full-space eigenvalue is lambda squared, coming from the shared constant temporal mode. The largest is the largest temporal difference eigenvalue plus lambda squared plus twice gamma. Their ratio is the condition number displayed here. Increasing gamma therefore raises the full-space condition number at fixed lambda, even as it enforces closer agreement between views. The mean profile still needs the magnitude penalty to control its baseline.

### If asked for more

The orthogonal transform preserves Euclidean eigenvalue and condition-number calculations. Its simple block diagonalization requires equal temporal blocks; unequal adaptive weights generally mix the mean and difference coordinates. A mean-zero restriction removes the shared constant mode for appropriately structured perturbations and can yield a sharper bound. Full-space conditioning still matters for numerical errors that can enter arbitrary directions, so it is useful to keep those two settings explicit.

## Backup 49 — Profile out the latent variables to see what disparity compares

Deck page: 85.

**Likely question:** What quantity is actually compared when you choose a disparity?

*[Point to the candidate-dependent right monocular term before the discrepancy term.]*

### Answer

For the unweighted model, I can solve out the two latent profiles exactly. The minimized cost separates into a left monocular cost, a right monocular cost, and a discrepancy term between their observations. Here m is the minimum regularized temporal reconstruction cost for a single observation vector.

The left monocular term is common to all candidates. The right monocular term changes as the candidate changes, and so does the discrepancy. The discrepancy is a nonnegative quadratic formed from the difference of observations passed through the transpose of the temporal operator. Its matrix is the difference between the inverse temporal precision and the inverse precision with twice gamma added. This formula exposes the selection mechanism: a candidate is rewarded both for matching the left observation and for having a lower individual reconstruction cost. Those competing contributions explain why correspondence selection needs its own analysis.

### If asked for more

The derivation completes the square in the stacked latent variables, then uses the sum-and-difference transform to separate the terms. The inverse difference equals twice gamma times the product of the two positive inverse matrices, so it is positive semidefinite. An exact winner of these unaggregated profiled costs minimizes the corresponding joint objective over the candidate set and latent variables. Establishing physical correspondence additionally requires assumptions that connect that objective to the true match.

## Backup 50 — A perfect correspondence need not have the lowest cost

Deck page: 86.

**Likely question:** Can the stereo objective favor a wrong correspondence even when the true profiles match exactly?

*[Point to the exact-match point, the one-half point, and their displayed costs. Read the follow-up scalar factors slowly.]*

### Answer

Yes. This two-sample example shows the mechanism exactly. The temporal operator takes one difference, both magnitude penalties use the identity, and gamma equals one. The left observation is one, while the right candidate observation is the scalar b. Solving the latent problem gives the displayed quadratic cost in b.

At the perfect observation match, b equals one and the minimized cost is one third. At the attenuated candidate b equal to one half, the cost is nine fortieths, which is smaller. The minimum over continuously varying b occurs at two sevenths. Attenuation reduces the right monocular reconstruction cost enough to compensate for the added discrepancy. Every inner solve in this example remains strictly convex and uniquely solved. The example therefore isolates the candidate-selection issue: inner uniqueness establishes a profile for each candidate, while physical correctness depends on how their minimized costs compare.

### If asked for more

For an observation scaled by b, the monocular contribution is the product of one plus b squared and the left monocular cost. The discrepancy contribution is the square of one minus b, multiplied by the discrepancy coefficient. Differentiating at b equal to one gives twice the positive monocular cost, so a small decrease in b lowers the score. The example concerns the unweighted local cost before aggregation; the evaluated weighted pipeline has additional steps.

## Backup 51 — Correct disparity needs a separation condition

Deck page: 87.

**Likely question:** What assumptions ensure that the correct disparity wins?

*[Subtract twice the left monocular cost and point to the nonnegative monocular-cost difference and the strictly positive discrepancy.]*

### Answer

This sufficient result concerns a finite candidate set and the unweighted local cost. The positive regularizer is common to both views and all candidates, and the coupling strength is fixed and strictly positive. At the true candidate, the right observation equals the left observation exactly.

For every competitor, assume the right observation differs from the left and its individual monocular reconstruction cost is at least as large as the left monocular cost. Subtracting the true candidate's cost leaves two contributions. The monocular-cost difference is nonnegative by assumption. The discrepancy term is strictly positive for a distinct observation because the temporal difference matrix has full row rank and gamma is positive. Their sum is positive, so every competitor has a larger cost. This gives a unique correct winner under explicit conditions that prevent attenuation from supplying a competing cost advantage.

### If asked for more

The condition is sufficient and can be stronger than necessary. A competitor with a smaller monocular cost can still lose if its discrepancy is large enough to overcome that advantage. The more general metric-separation criterion captures that case. Both versions concern ideal matched profiles and candidate-local unweighted costs. Applying the conclusion after masking, adaptive weighting, or spatial aggregation requires examining the corresponding scoring procedure and its assumptions.

## Backup 52 — A winning margin turns cost stability into selection stability

Deck page: 88.

**Likely question:** How much can candidate costs change before the selected disparity changes?

*[Point to the two eta contributions and the strict half-margin condition.]*

### Answer

Start with a fixed finite candidate set and a unique winner. Delta is the smallest gap between that winner and any competitor. If every candidate cost changes by at most eta, the worst case lowers a competitor by eta and raises the winner by eta. The gap can therefore shrink by at most twice eta.

Whenever eta is strictly smaller than half of delta, every perturbed gap remains positive and the same candidate wins. This turns a continuous cost-perturbation bound into a statement about a discrete decision. It also identifies why a small winning margin is sensitive. If two right candidates have exactly the same temporal observations and use the same local procedure and parameters, their local costs coincide. Rich temporal activity can coexist with that tie; selection stability requires a positive gap between the candidate scores.

### If asked for more

The cost bound must include the original winner as well as every competitor. At the half-margin threshold, the elementary bound allows a tie, so the strict inequality matters. An observation-based estimate can supply eta when the score parameters are fixed and the observation perturbations are controlled. Spatial aggregation can distinguish candidates through neighboring evidence, so the identical-profile example is scoped to the local scoring procedure rather than every contextual stereo algorithm.

## Backup 53 — Depth sensitivity grows with distance

Deck page: 89.

**Likely question:** What does a pixel of disparity error mean for depth accuracy?

### Answer

Depth is focal length times baseline divided by disparity. For fixed calibration, the exact change under a disparity perturbation is given by the difference formula on the slide. For a small relative disparity error, absolute depth sensitivity is depth squared divided by focal length times baseline. Farther points therefore turn the same disparity error into larger absolute depth errors.

The examples hold calibration fixed and add one pixel to disparity. Moving from four to five pixels underestimates depth by twenty percent. Moving from twenty to twenty-one pixels underestimates depth by about four point seven six percent. These are illustrative calculations.

This explains why I interpret depth error together with the depth range, disparity precision, and scored population. A stable winning label is one stage; interpolating that label and converting it to depth add their own sensitivity.

### If asked for more

The approximation requires disparity error to be small relative to disparity. The exact identity applies to any positive original and perturbed disparities. If the camera calibration also changes, the first-order relative depth change is the relative focal-length change plus the relative baseline change minus the relative disparity change.

The benchmark's finite, in-band estimates and ground truth define method-specific scored populations. Existing coverage slides explain that selection. This sensitivity calculation explains how disparity errors propagate within those populations. Attributing a method's observed error tails requires a separate analysis of its returned disparities.

## Backup 54 — Heteroscedastic weights: statistical motivation and scope

Deck page: 90.

**Likely question:** Why do you use reciprocal activity weights in stereo?

*[Point to the rate sum in the variance, then to the predicted-activity proxy in the weight.]*

### Answer

A useful starting point is a raw-count model in which positive and negative event counts are independent Poisson variables. Their difference has mean equal to the difference of the two rates and variance equal to their sum. In a high-count approximation, inverse-variance weighting motivates a weighted least-squares fidelity term.

The implemented rule uses reciprocal predicted activity plus a positive noise floor. It is a practical variance proxy: high predicted activity receives less weight, and the noise floor keeps the weight finite near zero. The distinction between total and net activity matters. Opposing polarity rates can cancel in the mean while both contribute to variance. Also, the actual observations have undergone warping, downsampling, and normalization. I therefore interpret each frozen weighted solve as a Gaussian surrogate for the processed features, with the reciprocal rule supported by the reported weighting comparison.

### If asked for more

The absolute difference of the two polarity rates is at most their sum, with equality exactly when at least one rate is zero. Thus a variance determined solely by net rate introduces an additional approximation. In the iteration, weights are evaluated at the preceding profile and then held fixed during the quadratic solve. That separation preserves the positive-definiteness argument for each solve and makes the statistical approximation explicit.

## Backup 55 — IRLS: fixed-point existence and conditional convergence

Deck page: 91.

**Likely question:** Does the iteratively reweighted stereo solver converge?

*[Point to the invariant-ball bound for existence, then separately to q less than one for convergence.]*

### Answer

The analysis gives two levels of guarantee for the unclipped reciprocal map with disparity, regularizer, and coupling fixed. First, a fixed point exists. Compare each frozen minimizer's objective with its value at zero. The positive magnitude penalty controls the squared norm of the solution, while every reciprocal weight is bounded above by the reciprocal noise floor. This places every update inside a sufficiently large closed ball.

The weight map is continuous, and the frozen system remains positive definite, so the update map is continuous. Brouwer's theorem then supplies a fixed point. Second, the displayed bound q is a sufficient contraction constant. If q is smaller than one, the fixed point is unique and repeated updates converge geometrically. The convergence statement therefore has an explicit parameter condition. It describes the analyzed update map, while implementation stopping and acceptance rules specify how numerical iteration is terminated.

### If asked for more

For a fixed damping parameter strictly greater than zero and at most one, the update becomes a convex combination of the old state and the undamped update. Its fixed points are preserved, and the displayed Lipschitz bound becomes one minus omega plus omega times q. When q is below one this remains a contraction. When q is at least one, this bound supplies no contraction certificate. A fixed point expresses consistency with frozen weights; interpreting it as a likelihood optimum requires a separate objective analysis.

## Backup 56 — Stereo benchmark: read accuracy alongside scored coverage

Deck page: 92.

**Likely question:** How competitive is the stereo method, and how should I interpret the coverage numbers?

*[Identify the centimeter columns, the scaled log metric, and the scored-point column separately.]*

### Answer

The table reports mean absolute depth error in centimeters for four MVSEC indoor sequences, together with an averaged log error and the total number of scored points. Soft-coupled weighted least squares has mean errors of 73.83, 58.35, 70.33, and 59.24 centimeters. Its displayed log RMSE is 44.54, and its scored population is 2.66 million points.

The Piatkowska adaptation has smaller mean depth error on three sequences; weighted least squares leads on Flying 2 and has a slightly smaller averaged log RMSE. The population sizes matter: the adaptation is scored on 1.20 million points. Each method's valid population requires both an estimate and ground truth within the reporting band. This supports a comparison of the reported accuracy together with scored coverage. A direct accuracy comparison on identical pixels would use a shared evaluation population.

### If asked for more

The reporting band runs from 0.5 to 8 meters. Point counts are summed across sequences, while the displayed log RMSE is one hundred times the base metric and is averaged equally over sequence-level values. A method can produce finite estimates outside the band that contribute to neither the reported error nor the scored count. These are complete implementations, including their normalization, regularization, guidance, and activity masking, and the external methods are local adaptations.

## Backup 57 — A weighting comparison supports the selected rule

Deck page: 93.

**Likely question:** What empirical evidence supports the reciprocal weighting rule?

*[Point to the subtraction direction before reading the four positive differences.]*

### Answer

This comparison changes the weighting rule while holding the remaining configuration fixed. The displayed numbers subtract the reciprocal-weight method's reported mean depth error from the rate-proportional method's error. The differences are 4.44, 8.28, 2.73, and 5.17 centimeters across Flying 1 through Flying 4. All four are positive, so the reciprocal rule has a smaller reported mean error on each sequence.

That result supports the selected rule for these evaluated configurations and their scored populations. The evaluation population is defined separately for each method, so the comparison combines each method's errors with the set of points it returns within the reporting band. These sequences were also used to select the rule. I would describe the result as empirical support for this design choice, with a common-pixel evaluation and additional sequences providing natural ways to test how broadly the advantage extends.

### If asked for more

The numerical differences are differences of the reported mean errors; they are not per-pixel paired improvements. A shared-population comparison would rescore both outputs on the same valid pixels. Using these sequences to choose the rule also makes the distinction between selection data and held-out validation important. Empirical improvement motivates the implementation choice, while a maximum-likelihood interpretation would additionally require a justified probabilistic model for the processed observations.

## Backup 58 — Hard fusion changes both the constraint and the regularization

Deck page: 94.

**Likely question:** Why does hard fusion perform differently from soft coupling?

*[Compare the magnitude-penalty coefficients after dividing the hard-fusion equation by two.]*

### Answer

Hard fusion forces the two profiles to be equal and solves for one shared profile. The implemented hard-fusion system also uses a different effective magnitude penalty. Dividing its normal equation by two shows half of lambda squared alongside the temporal data matrix. By comparison, sending the soft model's coupling strength to infinity, with equal fixed weights and unchanged regularization, retains the full lambda-squared term in the common-profile equation.

The reported mean depth errors, averaged over the four sequences, are 102.10 centimeters for hard fusion and 65.44 centimeters for soft weighted least squares. This establishes the observed difference between the evaluated configurations. The comparison changes hard equality, effective regularization, weights, iteration budgets, and scored populations. It therefore motivates further controlled comparisons to identify how much each design choice contributes to the measured gap.

### If asked for more

The penalty accounting is the key algebraic point. Substituting one shared profile into the soft energy adds its two half-weighted magnitude penalties into one full squared penalty. The implemented hard-fusion objective uses half that amount. The mean equation of the soft model already combines both views, so averaging alone supplies no demonstrated explanation for the performance difference. Isolating hard equality would require matching the other settings and the evaluation population.

## Backup 59 — Motion-induced events and the aperture problem

Deck page: 95.

**Likely question:** Can you derive the aperture problem directly from the event-generating image model?

*[Point to the normal-component equation, then to the arbitrary tangential coefficient in the boxed velocity family.]*

### Answer

Take a straight edge with steady illumination. Its log-intensity is a one-dimensional profile evaluated at normal position minus normal speed times time. The spatial gradient points along the edge normal, and the temporal derivative is minus the normal speed times the profile derivative.

Substituting those expressions into brightness constancy gives normal vector dotted with velocity equal to the edge's normal speed, wherever the profile derivative is nonzero. Every velocity with that normal component satisfies the same equation; its tangential component can take any value. These velocities generate the same local log-intensity histories, and therefore the same ideal threshold events when their reset references agree. That is the aperture ambiguity in this model: the edge determines its normal motion, while tangential motion remains free. Endpoints and other distinguishing features are assumed to lie outside the observation window.

### If asked for more

If the normal speed is zero, motion is entirely tangential and pixel values remain constant in the ideal edge interior. With nonzero normal speed, the crossing-time surface has gradient equal to the normal divided by that speed, which recovers the time-surface transport constraint. The model assumes steady illumination to isolate motion. The sensor's original threshold rule also responds to temporal changes caused by illumination, so interpreting every event as motion requires additional scene assumptions.
