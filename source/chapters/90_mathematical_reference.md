# Mathematical reference and practice

## Read a formula as a calculation

A scalar is one number. A vector is an ordered list of numbers; its order and units matter. A matrix is a rectangular array. In this book, a data matrix usually has observations in rows and features in columns, but every important use states the convention.

The symbol n often means a count of observations or workers. A subscript selects an entry: x_i means the ith value of x. A summation asks you to add terms over specified indices. A bar over a quantity commonly means its sample mean. A hat commonly marks an estimate or prediction. These are conventions, not substitutes for definitions.

A transpose, written T as a superscript or .T in NumPy, swaps rows and columns. A dot product multiplies matching entries and adds the products. The squared Euclidean norm adds squared entries of a vector. A matrix inverse reverses a square transformation when that inverse exists; many useful problems should be solved without explicitly forming it.

An eigenvector retains its direction when a matrix acts on it. Its eigenvalue is the corresponding scale factor. Singular values describe the strengths of orthogonal input and output directions of a matrix. PCA uses directions that retain variation after specified centering and scaling. A rank-k approximation keeps k such directions and discards the rest.

A derivative describes local change in output per change in input. A partial derivative varies one input while holding the others fixed. A gradient collects partial derivatives. Its entries can have different units, so an unscaled comparison of their magnitudes may be misleading.

A standard deviation describes spread and has the same units as the quantity. A variance is its square and has squared units. Covariance records paired variation and carries the product of two units. Correlation normalizes covariance into a unitless quantity. Standard uncertainty expresses uncertainty as an estimated standard deviation under a stated measurement model; it is not automatically the standard error of a sample mean.

A confidence interval describes a procedure's long-run coverage of a fixed target under repeated sampling and its assumptions. An input-uncertainty interval in a simulation summarizes outcomes induced by a chosen distribution over inputs. A sensitivity range reports what happened when selected inputs or settings changed. Label the kind of interval before interpreting its endpoints.

## Spatial and financial terms

A coordinate reference system, or CRS, defines how coordinates relate to locations. Declaring a CRS assigns meaning to existing numbers; transforming coordinates computes numbers in another CRS. A spatial join associates records through a geometric relationship and can produce several matches per input. A raster stores values on cells whose size, origin, orientation, and interpretation matter. NoData identifies unknown or unavailable values rather than physical zero.

Spatial autocorrelation describes association between values at locations considered neighbors under a stated weight matrix. Moran's I is one such summary. Its randomization test requires an exchangeability assumption and a defined tail. Inverse distance weighting, or IDW, estimates a value from distance-weighted observations; its surface is not automatically an uncertainty map.

Net present value, or NPV, sums dated cash flows after discounting them to a common date. A discount rate must match the cash-flow time unit and nominal or real convention. A simple return measures fractional gain over a period after the specified handling of external flows. A log return is the logarithm of one plus simple return and adds across periods on a compatible wealth path.

Drawdown measures a wealth path's decline from its running peak. Volatility is a standard deviation of returns under a stated period and model; it does not describe every form of risk. Value at risk, or VaR, is a specified loss quantile. Expected shortfall, or ES, averages the upper quantile tail with fractional probability mass at a discrete cutoff when necessary. A backtest evaluates a decision rule using historical or simulated records while respecting when information and execution were available.

## Four worked checks to keep nearby

For projection, [3, 1] projected onto the line through [1, 1] becomes [2, 2]. Its residual [1, −1] has zero dot product with that direction. If your result fails this perpendicularity check, inspect the calculation or the intended error metric.

For the Chapter 14 PCA example, the first component keeps 80 percent of total sample variance. The four reconstructed points are [1.5, 1.5], [1.5, 1.5], [3.5, 3.5], and [3.5, 3.5]. Their total squared reconstruction error is 2. Flipping the signs of a component and all its scores changes neither reconstruction nor error.

For image area, 576 square pixels with 0.2-mm sides cover 23.04 mm². If a scale standard uncertainty of 0.002 mm is the only uncertain input, the first-order area uncertainty is 0.4608 mm². Repeated pixels share that scale uncertainty.

For the synthetic worker model, the nominal best integer count from 1 through 32 is 22. Constraining the count to at most 12 makes 12 best. Reducing uncertainty about a coefficient can narrow the output distribution without changing its nominal optimum. Changing the coefficient's mean can move the optimum.

## A lab that joins the chapters

Choose one measurable engineering outcome, such as accepted tasks per hour, image-based area error, or research coverage of a region. Write the unit of observation, the outcome's denominator, and the action you are considering. Then list the inputs that could change your conclusion.

Build the smallest table or array that represents those inputs faithfully. Retain identifiers, units, provenance, and missing-value meaning. Make one plot that exposes a mechanism or comparison. If you compress the data, check what disappears. If you fit a model, keep an independent evaluation split that matches the way the model will be used.

Calculate one answer by hand or by a second method. For a matrix operation, check dimensions and a reconstruction identity. For a spatial result, check the coordinate system and a known distance or area. For a financial series, reconcile beginning value, flows, gains, costs, and ending value. For a simulation, compare a simplified case with an analytic answer.

Finally, alter an assumption that could reverse the decision. Report what stays true, what changes, and what new observation would resolve the important uncertainty. This is a more useful capstone than reproducing a chart without understanding its limits.
