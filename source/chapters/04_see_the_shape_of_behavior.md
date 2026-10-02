# 4 See the shape of behavior

## Explore before compressing

Exploratory data analysis means looking for structure, exceptions, and problems before committing to one summary or model. Graphics are central because a mean and a standard deviation can conceal very different shapes. The NIST engineering-statistics handbook treats plots and assumption checks as part of understanding the data rather than decoration after a calculation. [NIST exploratory data analysis](https://www.itl.nist.gov/div898/handbook/eda/eda.htm)

Start with counts and ranges. How many eligible records are present? What are the minimum and maximum values? Which categories dominate? Are there impossible values or a surprising mass at exactly zero? Are values repeated because of rounding, simulation defaults, or duplicate records? A simple sorted table is often the fastest first plot.

Then look at a distribution. Latency is often right-skewed: many ordinary cases and a smaller number of much slower ones. The mean is sensitive to those slow cases, which may be exactly what matters for total resource cost. The median describes the middle case, which may better describe typical responsiveness. Neither is the “correct” statistic for every decision.

## Read an empirical cumulative distribution

An empirical cumulative distribution function, or ECDF, answers: what fraction of observations are at or below this value? Sort the observations. At each observed value, plot the cumulative fraction. No bins are required.

For latency, pick a time on the horizontal axis and read upward to find the fraction completed within it. Pick a fraction on the vertical axis and read across to find an approximate percentile. A curve farther left generally represents smaller values, but curves can cross. Crossing curves tell you that the winner depends on which part of the distribution matters.

In the five-task example, B is faster for most tasks but has the slower maximum. An ECDF preserves that tradeoff. A single bar labeled “average latency” erases it.

At small sample sizes, an ECDF has large steps. That is honest. A smoothed density curve can make a dozen observations look like a richly known population. Show points or steps when data is sparse. A percentile near the extreme of a small sample is essentially a statement about one or two observations, not a stable description of a production tail.

## Histograms and box plots have jobs

A histogram groups values into bins and shows how often each range occurs. It helps reveal multiple modes, skew, and outliers. The choice of bin width changes the picture, so inspect more than one reasonable choice. Keep bins consistent when comparing policies.

A box plot compresses a distribution into a median, quartiles, and whiskers under a stated convention. It is useful for comparing many groups. It can hide multimodal behavior and sample size, so add points or counts when groups are small. A box plot of three runs does not provide rich evidence just because the software draws a box.

Logarithmic axes are useful when values span orders of magnitude. They emphasize ratios rather than absolute differences. Label them clearly and remember that zero cannot be plotted on a log axis. Do not quietly drop zeros or negative differences to make a log plot work.

## Choose the visual encoding from the question

Use a timeline when the question is what happened first, what overlapped, and where time was spent. Use an ECDF when the question is how a distribution changes. Use a paired dot or line plot when the question is how each matched workload changed. Use a scatter plot when the question is whether two quantities move together. Use a heatmap when two categorical or ordered dimensions organize many comparable cells.

A stacked bar can show how a fixed accounting total is divided among phases. A Pareto plot can show quality and cost together. A calibration plot can compare predicted confidence with observed frequency. Each visual has a reason to exist; a chart gallery without a question is a distraction.

For bars representing magnitudes, start the quantitative axis at zero unless there is a compelling, clearly communicated reason. For small differences around a reference, a dot plot with an explicit scale is often better than a truncated bar. Do not use 3D perspective to display ordinary 2D quantities. It makes value comparisons harder without adding evidence.

## Compare cohorts before telling a story

A cohort is a group defined by something relevant: CPU versus GPU tasks, cold versus warm starts, short versus long inputs, task family, model size, customer class, or collection source. Break down an aggregate when those groups plausibly behave differently.

Here is a synthetic example of a composition reversal. Policy A succeeds on 90 of 100 easy tasks and 1 of 10 hard tasks. Policy B succeeds on 19 of 20 easy tasks and 20 of 100 hard tasks. B is better within both groups: 95 versus 90 percent on easy tasks and 20 versus 10 percent on hard tasks. Yet its overall rate is 39 of 120, about 32.5 percent, below A's 91 of 110, about 82.7 percent. B received many more hard tasks.

This is a form of Simpson's paradox. The aggregate uses different group weights. The practical lesson is to inspect workload composition before attributing an aggregate change to the policy. You can compare within groups and, when justified, calculate both policies under the same explicitly chosen group weights.

Do not create dozens of cohorts after seeing the data and treat the best-looking result as a confirmed finding. Exploration is good for finding hypotheses. Confirmation needs fresh evidence or a procedure that accounts for the search.

## Outliers are questions

A very slow task may be a data error, a legitimate rare event, an operational failure, or the most valuable clue in the dataset. Inspect it before removal. A timeout recorded as a completed duration is different from a true completion at that duration. A stale worker result is different from an accepted result. A memory-unit mistake can look like a dramatic resource spike.

If you exclude a point, record the reason and show how the conclusion changes with and without it. “It looked too large” is not a sufficient rule. Predefined invalid-data criteria are safer than criteria chosen to improve the result.

Pay attention to points that disagree with your preferred explanation. If model reloads supposedly explain slowness, find the slow runs with few reloads and fast runs with many reloads. These cases reveal whether the explanation is incomplete.

## Write a caption that makes a claim checkable

A good caption tells the reader what was plotted, which observations are included, the unit, and the bounded takeaway. For example: “Task submission-to-accepted-result latency in one simulated workload, 12 completed tasks per policy. The proposed policy has a lower middle latency but a later upper tail. This is a descriptive within-workload comparison.”

A caption should not say that a chart proves a cause it cannot identify. If a scatter plot shows high queue length alongside high latency, it establishes an association in the plotted records. It does not tell you whether queue length caused the delay, a slow service caused the queue, or both responded to a traffic burst.

Exercise: take one chart you have made or seen. Write the question it answers in one sentence. Then name one important question it cannot answer. If those two sentences sound almost identical, the chart may be encouraging an overclaim.
