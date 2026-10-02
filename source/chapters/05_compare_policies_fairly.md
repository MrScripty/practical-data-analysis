# 5 Compare policies fairly

## Preserve the pair

If two policies run the same workload, the natural observation is their difference on that workload. Define difference as new minus baseline, so negative values favor the new policy for a duration metric. Calculate the difference before averaging. This preserves the pairing and makes good and bad cases visible.

Why does pairing help? A difficult workload may make both policies slow, while an easy workload makes both fast. Comparing their difference within the same workload removes much of that shared difficulty from the comparison. It does not remove a systematic bias such as always running one policy with a warm cache.

The scheduler follow-up contains three held-out seeds for each of four scenarios, three policies, and two service regimes. That is 72 report rows. It is not 72 independent pieces of evidence that the proposed policy is better. A comparison within one scenario and one regime has three matched workload pairs per baseline. The multiple policy rows are alternatives applied to the same workload, not extra workloads.

## Absolute and relative effects answer different questions

If a baseline takes 50 seconds and a proposal takes 45 seconds, the difference is -5 seconds, the proposal-to-baseline ratio is 0.9, and the reduction relative to baseline is 10 percent. The baseline is 11.1 percent slower than the proposal because that statement uses 45 as the denominator. State the reference explicitly.

Averaging per-workload percentage changes gives each workload equal weight in percentage terms. Dividing mean proposed time by mean baseline time is a different calculation. A tiny 1 second workload and a 100 second workload can influence those summaries very differently. Choose the summary that matches the workload mix and decision; show the per-pair values so the reader can inspect the choice.

An equal-weight mean across scenario families answers a hypothetical question in which those families are equally likely. It does not estimate production performance unless production has that mix. If you know the real mix, report a weighted estimate and its source. If you do not, report the scenarios separately.

## Variation is not uncertainty

Variation describes how observations differ. Uncertainty describes how much you do not know about a quantity you are trying to estimate. The spread of task latencies is variation. The uncertainty in a policy's mean improvement on future workloads is a different object.

A confidence interval is produced by a procedure with a stated long-run coverage property under its assumptions. A 95 percent confidence procedure would cover the target in 95 percent of repetitions in the relevant idealized setting. It is not a promise that the particular interval contains the truth, and it does not include every source of uncertainty. A narrow interval from a biased sample can be precisely wrong. For paired observations, conventional mean-difference intervals are based on the distribution of within-pair differences. [NIST intervals for paired differences](https://itl.nist.gov/div898/handbook/prc/section3/prc312.htm)

With only three held-out seeds, display all differences and be cautious about generalization. A numerical interval can still be calculated, but strong distributional assumptions or extremely limited resampling support may dominate its interpretation. This book does not use a tiny-sample interval to turn the scheduler follow-up into a deployment claim.

## Bootstrap a quantity you can name

The bootstrap constructs repeated resamples from the observed data and recalculates a statistic. For paired runs, resample entire pairs, or equivalently their differences. Do not resample the new and baseline columns independently; that breaks the relationship you intended to use.

The companion includes 30 independent synthetic blocks. Their measured mean difference is about -1.240 seconds. A seeded 20,000-resample percentile bootstrap gives an illustrative 95 percent interval of approximately -2.508 to 0.059 seconds. These are generated teaching data. The interval crosses zero, so this particular method and sample do not clearly establish the sign of the population mean difference. The point estimate still describes the sample.

Here is the core calculation, assuming differences is a one-dimensional array containing one value per independent paired block:

```python
rng = np.random.default_rng(82)
indices = rng.integers(0, len(differences),
                       size=(20000, len(differences)))
resampled_means = differences[indices].mean(axis=1)
low, high = np.quantile(resampled_means, [0.025, 0.975])
```

This simple percentile example teaches the mechanics. It is not a universal best method. Bootstrap variants differ, and small, highly skewed, dependent, or degenerate data can cause difficulties. SciPy documents several methods and explicitly supports paired resampling. Check a chosen method's assumptions rather than treating its output as automatic validation. [SciPy bootstrap](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html)

If observations share a user, workflow, document, machine session, or collection batch, that group may be the resampling unit. Randomly resampling individual rows from a strongly correlated group makes the sample look more informative than it is. Time series may require blocks that preserve temporal dependence. If you cannot identify a defensible independent unit, pause before attaching an inferential interval.

## A p value does not make the decision

A p value describes how incompatible the observed data are with a specified statistical model, often a no-effect model. It does not measure the probability that the hypothesis is true, the size of the benefit, or the importance of the result. The American Statistical Association warns against reducing scientific conclusions to whether a threshold is crossed. [ASA statement on p values](https://www.amstat.org/asa/files/pdfs/P-ValueStatement.pdf)

For engineering, report the effect in useful units, uncertainty, cost, and guardrails. A tiny effect can be statistically detectable in a huge dataset but not worth maintaining. A potentially large effect can be uncertain in a small dataset and deserve a better experiment. “Not statistically significant” does not establish equivalence. If your decision requires proving that two alternatives differ by less than a tolerable amount, formulate an equivalence or noninferiority question with a justified margin and suitable design.

## Searching changes what a result means

Suppose you try 40 parameter settings, inspect 15 metrics, and publish the best improvement. Even if none is genuinely better, some may look good through chance or idiosyncratic fit to the test cases. The issue is the selection process, not just one final comparison.

Separate exploration from confirmation. Use development workloads to find candidates. Freeze a promising choice and its primary outcome. Evaluate on a fresh set that was not used for tuning. Once you inspect that set and change the design in response, it becomes part of development history. You need new evidence for the next strong confirmation claim.

For a predeclared family of tests, methods such as Bonferroni can bound the chance of one or more false positives by allocating the error budget across comparisons. They trade sensitivity for control and do not repair biased data or an undefined search process. [NIST multiple comparisons](https://www.itl.nist.gov/div898/handbook/prc/section4/prc463.htm)

## Make the comparison auditable

A comparison table should state the policies, workload population, independent unit, number of pairs, common controls, metric definition, and direction of improvement. Show failures and missing pairs. Do not quietly compare different subsets after one policy fails to finish.

The scheduler's quantile convention also deserves a note. Its report uses nearest rank: sort values and select rank ceiling(p times n). For 12 completed tasks, its p95 selects the maximum. Its p50 selects the sixth value, whereas the conventional median of an even sample averages the sixth and seventh. The companion reproduces the report's convention rather than silently changing it. That small distinction is a useful example of measurement precision: two libraries can disagree without either being broken.

Exercise: choose a metric and write three different summaries you could report: mean difference, mean percentage change, and ratio of means. Explain which would be most relevant to your decision and why. Then identify the independent unit you would resample if you wanted an uncertainty interval.
