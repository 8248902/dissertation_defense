## Backup 66 — Fractional regularization keeps the proof and allows jumps

Deck page: 100.

**Likely question:** Why the H one seminorm? What changes with a fractional-order regularizer?

*[Point to the seminorm, then move down the four items.]*

### Answer

The proof carries over, and the model gains the ability to represent motion boundaries. Replace the gradient penalty by alpha squared times the Gagliardo seminorm of order s. It vanishes only on constant fields, and it has an elementary Poincaré inequality: distances in the domain are at most its diameter, so the seminorm of a mean-zero field bounds its L two norm with an explicit constant. No boundary regularity is needed. The complementarity lemma then gives coercivity on H s, with the same integrated condition m. Lax--Milgram gives the unique minimizer, and the stability bound holds in the H s norm.

The gain is at motion boundaries. On the image rectangle the H one minimizer is in H two, which in two dimensions means it's continuous, so it can't jump where two objects move differently. A field that is constant on each of two regions belongs to H s exactly when s is below one half. The discrete version is an all-pairs graph, which is connected, so the block-Jacobi theorem still applies; the price is that every sweep is dense.

### If asked for more

For a jump between two velocities across a region boundary, the seminorm equals twice the squared jump times a fractional perimeter of the region. That's finite for s below one half. Since the cost is quadratic in the jump while total variation is linear, jumps are allowed but still shrunk, so this sits between H one and total variation and keeps the Hilbert-space structure.

The H two statement uses Neumann regularity on a convex polygon. The Euler--Lagrange operator is the regional fractional Laplacian, and Professor Warma's 2015 paper treats its Neumann-type boundary conditions. A spectral variant, built from the Neumann eigenvalues raised to the power s, also vanishes only on constants; Antil and Bartels use spectral fractional operators in imaging. None of this is in the dissertation; it's a direct extension of Theorem 3.6.1.
