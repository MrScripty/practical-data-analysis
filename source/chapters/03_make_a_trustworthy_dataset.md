# 3 Make a trustworthy dataset

## Keep raw evidence separate

Treat the raw input as an immutable record. Copy it into a versioned analysis snapshot, record a cryptographic hash, and do transformations elsewhere. A hash does not prove that data is correct; it proves which bytes your analysis used. That is enough to prevent an important class of confusion when reports are regenerated during development.

Keep a manifest with the source, collection or run time, software revision, configuration, random seed, relevant environment, and interpretation notes. If some of these are unavailable, say so. An honest missing field is better than a guessed revision identifier.

A simple directory layout has raw inputs, derived tables, analysis code, figures, and a short README. Raw inputs should not change when you rerun analysis. Derived outputs may be rebuilt. The separation lets you test whether a changed result came from different data, different transformation logic, or different plotting choices.

## Decide what one row means

A table becomes much easier to use when each column holds one variable and each row is one observation of a defined kind. A task table, an attempt table, and an event table are different observational levels. The tidy-data principle formalizes that separation. [Wickham, Tidy Data](https://www.jstatsoft.org/article/view/v059i10)

For the scheduler, use a run table with one row per policy, workload, seed, and configuration combination. Use a task table with one row per logical task within a run. Use a phase table with one row per observed phase interval. A decision table can hold one row per planning decision, and a candidate table one row per candidate within that decision.

Do not force everything into one giant flat table. If a task has three phases and five candidate scores, joining both onto the task without care creates fifteen rows. A later sum can count its latency fifteen times. This is a data-model error that a beautiful chart will not reveal.

Choose keys explicitly. A task identifier may repeat across runs, so the key is usually run identifier plus task identifier, not task identifier alone. An attempt adds another key. Before a join, state whether it should be one-to-one, many-to-one, or many-to-many.

## Validate before calculating

Validation checks whether the data satisfies expectations that must be true before interpretation. Begin with key uniqueness, allowed values, required fields, units, nonnegative durations, and event ordering. Then add domain checks: accepted work must have a submission; phase ends need matching starts; completion counts must agree across tables; and resources must stay within modeled capacity when the model promises that constraint.

A failed check is useful information. Do not delete the row simply to make the code continue. Put suspect records in a quarantine output with the reason, and decide whether they prevent answering the question. For a performance comparison, missing all the slowest results is a serious problem. A missing optional model label may only prevent one cohort breakdown.

Different checks have different severity. A duplicate run key should usually stop a policy comparison. A missing optional diagnostic field may trigger a warning. Document the choice so another person knows what the analysis accepted.

In pandas, use explicit join validation when possible. For example, joining a task table to run metadata can use validate="many_to_one". An outer merge with an indicator can reveal unmatched keys before you choose the intended analysis join. Be aware that pandas can match null join keys to each other, unlike usual SQL null behavior; reject or handle missing identifiers explicitly. [pandas merge documentation](https://pandas.pydata.org/docs/reference/api/pandas.merge.html)

## A small transformation you can audit

Suppose each event has run_id, task_id, event, and time_s. Extract arrival and accepted-result events into separate tables. Validate one arrival and one accepted result per logical task for the simple one-attempt case. Left-join completion onto arrival, preserving tasks that have not completed. Derive latency only where completion exists. Add status and age_at_cutoff for the rest.

The key choice is the left join from submissions. Starting with completions would hide unfinished work. An inner join is convenient because it yields clean durations; convenience is not a justification for changing the population.

A compact SQL pattern is:

```sql
SELECT
    s.run_id,
    s.task_id,
    s.submitted_s,
    c.accepted_s,
    CASE WHEN c.accepted_s IS NOT NULL
         THEN c.accepted_s - s.submitted_s END AS latency_s
FROM submissions AS s
LEFT JOIN accepted_results AS c
  ON s.run_id = c.run_id AND s.task_id = c.task_id;
```

This query assumes the tables have already passed key-uniqueness checks. SQL does not automatically protect you from duplicate matching rows. If accepted_results contains duplicate accepted outcomes, the join replicates submissions and corrupts aggregates.

## Missing is not zero

A missing duration can mean not yet complete, not applicable, not instrumented, redacted, or corrupted. These are different states. Keep a reason field when the distinction changes interpretation. The value zero means the observed quantity was zero. It should not become a universal placeholder.

Consider research records with an optional quality rating. If difficult cases are less likely to receive a rating, the average among rated cases overstates overall quality. More rows will not remove that selection problem. First inspect missingness by relevant groups and process stages.

Imputation replaces missing values with estimates. It can be useful in a carefully designed predictive pipeline, but it does not recover the true unobserved measurement. A beginner-safe first analysis reports missingness and uses an explicit complete-case subset only where its limitations are acceptable. For a decision-critical outcome, try to recover the data or measure bounds rather than silently filling it.

## Work at the right aggregation level

A common first calculation is group-by followed by an average. Ask what each row contributes to the answer. Averaging one number per workflow weights workflows equally. Averaging all task latencies weights workflows with more tasks more heavily. Neither is universally correct. The decision determines which population should receive equal weight.

The same issue appears in agent evaluation. A task with ten repeated trials can contribute ten times as much as a task with one trial if you pool all rows. If your question is performance on a typical task, first summarize within task or use equal planned trial counts. If your question is the success rate of a random production attempt, the production attempt distribution may be the appropriate weight.

Always show the number of runs, tasks, and attempts separately. It prevents a large event count from being mistaken for broad coverage.

## When the data stops fitting in memory

You do not need a distributed system just because a dataset is larger than a spreadsheet. First estimate its size, select only needed columns, filter the relevant time range, and avoid making unnecessary copies. A columnar file format can make repeated analytical reads more efficient because queries can read selected columns. A database can filter and aggregate near the stored data before returning a small result.

The important distinction is between the logical analysis and its execution. A group-by mean is a logical operation. It might run in pandas, SQL, or a larger processing system. Learn the operation and its assumptions first; then choose the smallest tool that handles the volume and update pattern reliably.

pandas documents strategies such as efficient dtypes, loading fewer columns, and chunking. Chunking works naturally when each chunk can be reduced to a small summary that can be combined correctly. More complex global operations need different treatment. [pandas scaling guidance](https://pandas.pydata.org/docs/user_guide/scale.html)

For example, the overall mean of a nonmissing numeric field can be computed from its total sum and total count across chunks. Do not average the chunk means unless all chunks have the same nonmissing count. The final chunk is often smaller, and missingness can change counts within every chunk. Keep missing and invalid counts alongside the valid sum.

A global percentile cannot generally be recovered by averaging chunk percentiles. For exact quantiles, use an appropriate database, sorting procedure, or retained data. Approximate streaming quantiles can be useful at scale, but their approximation method and error properties become part of the metric definition.

Large joins deserve care. Filter and deduplicate keys before joining, inspect expected cardinality, and materialize a small diagnostic sample before launching an expensive computation. A many-to-many mistake can turn a manageable dataset into an enormous intermediate result. Faster hardware does not repair the wrong relationship between tables.

Keep an economical development loop. Validate the analysis on a small representative extract and known edge cases, then run the same logic over the full eligible population. A random sample can miss rare failures, so also inspect important error strata and boundary cases. Label sample-based exploratory results separately from full-population calculations. Do not treat a dataset that fits in memory as necessarily representative, or one that needs a cluster as necessarily informative.

## Reproducibility is a chain

A trustworthy result can be followed from an input hash to transformation code, a derived table, a calculation, and a figure. Every figure should identify its data population, units, and exclusions. Keep the code that generated it. Manual edits to a plot can be useful for publication polish, but they should not change the data or hide inconvenient points.

Use relative paths, fixed seeds for synthetic examples and resampling, and a clear command that reproduces the outputs. Record installed library versions. A seed makes a particular random computation repeatable under an implementation; it does not make the experiment valid or guarantee identical results across all versions and hardware.

Exercise: make three tests for an existing dataset: one key test, one arithmetic reconciliation, and one population test. The population test should answer, “Which expected observations are absent?” It is often the most informative of the three.
