# Sources and evidence

These references support the definitions, methods, and further reading in the book. All worked datasets and figures are original or drawn from the pinned scheduler simulation. Generated teaching examples are labeled synthetic. Source pages were checked on 2 October 2026; official documentation may evolve independently of the companion runtime.

S01. [OpenTelemetry traces](https://opentelemetry.io/docs/concepts/signals/traces/)

Used in chapter 2. Trace, span, and attribute concepts for instrumentation.

S02. [Prometheus histograms and summaries](https://prometheus.io/docs/practices/histograms/)

Used in chapter 2. Aggregation limits of precomputed quantiles and histograms.

S03. [Wickham, Tidy Data](https://www.jstatsoft.org/article/view/v059i10)

Used in chapter 3. One variable per column, one observation per row, and one table per observational unit.

S04. [pandas merge documentation](https://pandas.pydata.org/docs/reference/api/pandas.merge.html)

Used in chapter 3. Join cardinality validation and pandas null-key behavior.

S05. [pandas scaling guidance](https://pandas.pydata.org/docs/user_guide/scale.html)

Used in chapter 3. In-memory scaling, reducing loaded data, and chunking.

S06. [NIST exploratory data analysis](https://www.itl.nist.gov/div898/handbook/eda/eda.htm)

Used in chapter 4. Exploratory graphics and assumption checking.

S07. [NIST intervals for paired differences](https://itl.nist.gov/div898/handbook/prc/section3/prc312.htm)

Used in chapter 5. Paired mean-difference confidence intervals.

S08. [SciPy bootstrap](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html)

Used in chapter 5. Bootstrap methods and paired resampling.

S09. [ASA statement on p values](https://www.amstat.org/asa/files/pdfs/P-ValueStatement.pdf)

Used in chapter 5. Interpretation limits of p values and threshold-only decisions.

S10. [NIST multiple comparisons](https://www.itl.nist.gov/div898/handbook/prc/section4/prc463.htm)

Used in chapter 5. Bonferroni control for preselected multiple comparisons.

S11. [Causal Inference What If](https://miguelhernan.org/whatifbook)

Used in chapter 7, 13. Counterfactual causal framework and further reading.

S12. [NIST design selection](https://www.itl.nist.gov/div898/handbook/pri/section3/pri33.htm)

Used in chapter 7. Comparative, screening, and response-surface experiment objectives.

S13. [Columbia notes on Little's law](https://www.columbia.edu/~ks20/stochastic-I/stochastic-I-LL.pdf)

Used in chapter 8. Little’s law, consistent system boundaries, and time averages.

S14. [NIST process monitoring](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm)

Used in chapter 8. Control limits versus specification limits.

S15. [Forecasting Principles and Practice on time-series cross-validation](https://otexts.com/fpp3/tscv.html)

Used in chapter 8. Time-ordered rolling-origin evaluation.

S16. [Google SRE monitoring](https://sre.google/sre-book/monitoring-distributed-systems/)

Used in chapter 8. Latency, traffic, errors, saturation, and symptoms versus causes.

S17. [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)

Used in chapter 9. Agent task, trial, grader, transcript, and outcome distinctions.

S18. [Zheng and colleagues on LLM judges](https://arxiv.org/abs/2306.05685)

Used in chapter 9. Documented judge position, verbosity, and self-enhancement biases; no universal accuracy claim.

S19. [scikit-learn probability calibration](https://scikit-learn.org/stable/modules/calibration.html)

Used in chapter 9. Calibration versus discrimination and reliability diagrams.

S20. [scikit-learn common pitfalls](https://scikit-learn.org/stable/common_pitfalls.html)

Used in chapter 10. Training-only preprocessing and leakage prevention.

S21. [scikit-learn cross-validation](https://scikit-learn.org/stable/modules/cross_validation.html)

Used in chapter 10. Grouped and time-aware cross-validation.

S22. [Kapoor and Narayanan on leakage](https://arxiv.org/abs/2207.07048)

Used in chapter 10. Leakage risks in machine-learning-based science.

S23. [scikit-learn model-evaluation metrics](https://scikit-learn.org/stable/modules/model_evaluation.html)

Used in chapter 10. Classification and regression metric definitions.

S24. [Model Cards for Model Reporting](https://arxiv.org/abs/1810.03993)

Used in chapter 10. Structured reporting of model use, performance, and limitations.

S25. [W3C PROV primer](https://www.w3.org/TR/prov-primer/)

Used in chapter 11. Entities, activities, and agents in provenance.

S26. [Rubin on inference with missing data](https://dash.harvard.edu/entities/publication/73120378-8764-6bd4-e053-0100007fdf3b)

Used in chapter 11. Missing-data mechanisms and the conditions behind ignoring missingness.

S27. [GeoPandas projections](https://geopandas.org/en/stable/docs/user_guide/projections.html)

Used in chapter 11. Coordinate reference systems and assigning versus transforming coordinates.

S28. [Gebru and colleagues on datasheets](https://arxiv.org/abs/1803.09010)

Used in chapter 11. Dataset motivation, composition, collection, use, and documentation.

S29. [Python for Data Analysis](https://wesmckinney.com/book/)

Used in chapter 13. Legally available author online book and practical reading path; no text reproduced.

S30. [Fundamentals of Data Visualization](https://clauswilke.com/dataviz/)

Used in chapter 13. Author manuscript for visualization reading; no figures or text reproduced.

S31. [OpenIntro Statistics](https://www.openintro.org/book/os/)

Used in chapter 13. Foundational statistics reading recommendation and official availability.

S32. [NIST engineering statistics](https://www.itl.nist.gov/div898/handbook/)

Used in chapter 13. Engineering-statistics reference reading recommendation.

S33. [An Introduction to Statistical Learning](https://www.statlearning.com/)

Used in chapter 13. Authors’ statistical-learning book and Python edition reading recommendation.

S34. [Forecasting Principles and Practice](https://otexts.com/fpp3/)

Used in chapter 13. Forecasting book reading recommendation.

M01. [MIT projections and least squares](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/pages/least-squares-determinants-and-eigenvalues/projection-matrices-and-least-squares/)

Used in chapter 14. Geometric connection between projection and least-squares residuals.

M02. [NIST mean vector and covariance matrix](https://www.itl.nist.gov/div898/handbook/pmc/section5/pmc541.htm)

Used in chapter 14. Sample covariance definition and observation/feature orientation.

M03. [NumPy covariance](https://numpy.org/doc/stable/reference/generated/numpy.cov.html)

Used in chapter 14. rowvar orientation and covariance API.

M04. [MIT singular value decomposition](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/pages/positive-definite-matrices-and-applications/singular-value-decomposition/)

Used in chapter 14. Matrix factorization and singular directions; original example derived separately.

M05. [NumPy singular value decomposition](https://numpy.org/doc/stable/reference/generated/numpy.linalg.svd.html)

Used in chapter 14. Returned U, singular values, Vh and reconstruction conventions.

M06. [scikit-learn clustering guide](https://scikit-learn.org/stable/modules/clustering.html)

Used in chapter 14. Clustering objectives and contrasting method assumptions.

M07. [scikit-image image data types](https://scikit-image.org/docs/stable/user_guide/data_types.html)

Used in chapter 15. Image dtype and range conventions.

M08. [SciPy multidimensional convolution](https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.convolve.html)

Used in chapter 15. Convolution and boundary-mode concepts; companion implements its own explicit NumPy reflection convention.

M09. [NumPy discrete Fourier transform conventions](https://numpy.org/doc/stable/reference/routines.fft.html)

Used in chapter 15. Frequency ordering, transform normalization, real-valued transform representation.

M10. [scikit-image morphology](https://scikit-image.org/docs/stable/api/skimage.morphology.html)

Used in chapter 15. Erosion, dilation, opening, closing and footprints.

M11. [scikit-image region measurements](https://scikit-image.org/docs/stable/api/skimage.measure.html)

Used in chapter 15. Connected-region measurement, spacing, area and coordinates.

M12. [Boyd and Vandenberghe Convex Optimization](https://web.stanford.edu/~boyd/cvxbook/)

Used in chapter 18. Author-hosted legal book availability and further study of convex problems.

M13. [SciPy optimization guide](https://docs.scipy.org/doc/scipy/tutorial/optimize.html)

Used in chapter 18. Distinguishing solver families and problem structures.

M14. [NIST law of propagation of uncertainty](https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-appendix-law-propagation-uncertainty)

Used in chapter 18. First-order sensitivities, variances, and covariance terms.

M15. [NIST uncertainty budgets and sensitivity coefficients](https://www.itl.nist.gov/div898/handbook/mpc/section5/mpc56.htm)

Used in chapter 18. Relating input uncertainty to output uncertainty contributions.

M16. [JCGM 101 Monte Carlo propagation](https://www.bipm.org/documents/20126/2071204/JCGM_101_2008_E.pdf/325dcaad-c15a-407c-1105-8b7f322d651c)

Used in chapter 18. Propagation of distributions, conditions and separation from validity of the input model.

G01. [Projections](https://docs.geopandas.org/en/stable/docs/user_guide/projections.html)

Used in chapter 16. CRS metadata, declaring versus transforming coordinates, and GeoPandas longitude/latitude order. Does not establish the accuracy of any particular local projection.

G02. [Geodesic calculations](https://proj.org/en/stable/geodesic.html)

Used in chapter 16. Distinguishing ellipsoidal geodesics from the chapter’s explicitly spherical approximation. No claim that the synthetic sphere is survey grade.

G03. [Merging data](https://geopandas.org/en/stable/docs/user_guide/mergingdata.html)

Used in chapter 16. Attribute versus spatial joins, geometric predicates, one-to-many matches and nearest-join options. Rectangle half-open assignment is an original teaching convention.

G04. [Geotransform tutorial](https://gdal.org/en/stable/tutorials/geotransforms_tut.html)

Used in chapter 16. Six affine coefficients, top-left corner coordinates, north-up negative pixel height and half-cell center offset. Zonal overlap example independently derived.

G05. [GDAL Grid tutorial](https://gdal.org/en/stable/tutorials/gdal_grid_tut.html)

Used in chapter 16. Inverse distance to a power interpolation and neighborhood parameters. Chapter fixture uses all points, p=2, zero smoothing; measurement-only variance is separately derived.

G06. [How Kriging works](https://doc.esri.com/en/arcgis-pro/latest/tool-reference/spatial-analyst/how-kriging-works.html)

Used in chapter 16. Kriging relies on a modeled spatial relationship; prediction error is conditional on model assumptions. No kriging implementation or empirical calibration is claimed.

G07. [Cross-validation strategies for data with temporal spatial hierarchical or phylogenetic structure](https://nsojournals.onlinelibrary.wiley.com/doi/10.1111/ecog.02881)

Used in chapter 16. Structured validation must reflect interpolation versus transfer to new space; dependence can make random validation misleading. Not a universal endorsement of every blocking design.

G08. [Global Spatial Autocorrelation with Moran’s I](https://pysal.org/esda/stable/user-guide/global_morans_i.html)

Used in chapter 16. Moran statistic, spatial lag and random-label permutation reference. Chapter explicitly fixes locations and weights and defines its own right tail; it does not assert generic point-process CSR or reproduce software default p-value semantics.

G09. [Local Spatial Autocorrelation 1](https://geodacenter.github.io/workbook/6a_local_auto/lab6a.html)

Used in chapter 16. Local quadrant membership differs from significance; local tests raise multiplicity and permutation-resolution issues. Chapter implements descriptive local values only.

G10. [Choropleth Map Design for Cancer Incidence Part 2](https://www.cdc.gov/pcd/issues/2010/jan/09_0073.htm)

Used in chapter 16. Warnings about ecological inference, small denominators and geographic pattern interpretation. Chapter has no disease analysis and its four-person numerical counterexample is original.

F01. [Present Value Relations Slides 1–36](https://ocw.mit.edu/courses/15-401-finance-theory-i-fall-2008/resources/mit15_401f08_lec02/)

Used in chapter 17. Present value, compounding and real/nominal consistency. All project cash flows, break-even numbers and IRR counterexample are original calculations; no recommended discount rate.

F02. [Portfolio Theory Slides 1–46](https://ocw.mit.edu/courses/15-401-finance-theory-i-fall-2008/resources/mit15_401f08_lec13/)

Used in chapter 17. Weighted portfolio returns and the role of covariance in mean-variance analysis. Matrices and return observations are synthetic, not estimates for named assets.

F03. [Foundations of Portfolio Theory](https://onlinelibrary.wiley.com/doi/10.1111/j.1540-6261.1991.tb02669.x)

Used in chapter 17. Historical foundation and conditional role of mean-variance portfolio criteria. Does not supply the chapter’s numerical portfolio or current market claims.

F04. [The Statistics of Sharpe Ratios](https://alo.mit.edu/publications/page/18/)

Used in chapter 17. Sharpe estimates have sampling error; simple annualization is not generally valid under serial correlation. The additive-sum variance identity is derived independently in the chapter.

F05. [On the coherence of Expected Shortfall](https://arxiv.org/abs/cond-mat/0104295)

Used in chapter 17. Expected shortfall definitions need care for discontinuous distributions; precise tail probability mass. Chapter uses upper-tail loss confidence alpha, which must not be confused with an author’s lower-tail probability convention.

F06. [How Fees and Expenses Affect Your Investment Portfolio](https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins/updated)

Used in chapter 17. Fees reduce returns and the capital left to compound. Does not justify the toy 0.001 transaction cost as realistic or current.

F07. [The Probability of Backtest Overfitting](https://www.davidhbailey.com/dhbpapers/backtest-prob.pdf)

Used in chapter 17. Trying many alternatives creates selection risk even without a direct look-ahead bug; retain experiment history. Chapter does not implement CSCV or estimate a PBO.

F08. [The Delisting Bias in CRSP Data](https://doi.org/10.1111/j.1540-6261.1997.tb03818.x)

Used in chapter 17. Historical research example of missing delisting outcomes. Supports auditing terminal observations, not a claim that current CRSP data still has the reported defect.
