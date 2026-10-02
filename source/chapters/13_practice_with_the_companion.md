# 13 Practice with the companion

## Run a complete analysis first

The companion uses Python with NumPy, pandas, and matplotlib. The verified run used Python 3.12.14, NumPy 2.3.5, pandas 2.2.3, and matplotlib 3.10.8. These versions describe the environment that produced the book's outputs; they are not a requirement to upgrade an existing project blindly.

From the book directory, run:

```bash
python companion/analyze.py
python companion/check_outputs.py
```

The program verifies hashes in the snapshot manifest, reconstructs task and phase tables, checks arithmetic against the simulator reports, writes derived CSV files, and regenerates six figures. It also creates the labeled synthetic agent, paired-run, and research examples. It never runs or changes the scheduler itself.

If a hash check fails, stop. Do not edit the expected hash merely to make the test pass. You may have mixed versions, changed an input, or downloaded an incomplete file. Restore the intended snapshot or intentionally create and document a new analysis version.

The parser is intentionally strict for these five complete diagnostic traces. They contain one ready event and one accepted result per task, and all phases close. A production parser needs additional states for retries, cancellations, open intervals, and partial traces. A test fixture is not a universal ingestion library.

## Lab 1 Reproduce a metric from events

Open the generated scheduler_tasks.csv. Each row is one task within one diagnostic run. Inspect the fields before calculating anything: run_id, task_id, arrival_s, ready_s, first_phase_s, accepted_s, latency_s, ready_wait_s, and first_device.

Load it and check its key:

```python
from pathlib import Path
import pandas as pd

root = Path('.')
tasks = pd.read_csv(root / 'companion/derived/scheduler_tasks.csv')
assert not tasks.duplicated(['run_id', 'task_id']).any()
assert len(tasks) == 60

one = tasks[tasks.run_id == 'after_fix_proposed'].copy()
assert len(one) == 12
assert (one.accepted_s >= one.arrival_s).all()
print(one.accepted_s.max())
```

Expected result: approximately 56.642415 seconds. Trace timestamps are rounded to six decimal places, so use tolerances rather than exact floating-point equality when comparing them to full-precision reports.

Now sort latency_s and calculate the sixth value and the average of the sixth and seventh. The first reproduces the report's nearest-rank p50; the second is the conventional median for 12 values. Explain why they differ without calling either a software bug.

Next, compare first_phase_s minus arrival_s with ready_wait_s. They answer different questions because dependency time can occur before a task is ready. Write the endpoint definitions beside each result.

## Lab 2 Preserve a policy pair

Load holdout_runs.csv and filter to matched_service. Check uniqueness on regime, scenario, seed, and policy. Pivot policy into columns so each row is one scenario-seed combination:

```python
runs = pd.read_csv(root / 'companion/derived/holdout_runs.csv')
matched = runs[runs.regime == 'matched_service']
wide = matched.pivot(index=['scenario', 'seed'],
                     columns='policy', values='makespan_s')
assert len(wide) == 12
assert not wide.isna().any().any()
wide['difference_s'] = wide['proposed'] - wide['residency']
print(wide.loc['randomized'])
```

Show all three randomized differences before calculating a mean. At least one seed favors the proposed policy and others favor residency. The mean therefore hides important variation. Describe the result as three tested workloads, not a reliable estimate of all future randomized workloads.

Then compute the mean of per-seed ratios and the ratio of mean times. Explain why they need not be identical. State which weighting scheme each represents.

## Lab 3 Inspect one decision

Open scheduler_candidates.csv and select the repaired proposed run at time approximately 40.495955 seconds. The actions_json field preserves the candidate's structured action list. Identify the warm-CPU candidate, the no-action candidate, and the eviction candidate.

Write down their scores and score components. Do not convert a score into seconds. Use the forced-final-GPU trace to compare the resulting completion time, while preserving the fact that this was a single diagnostic intervention.

Expected interpretation: candidate coverage was repaired, but the scoring rule still preferred the warm CPU. The forced GPU continuation improved this one run substantially without reaching FIFO's finish time. A good answer names both the supported mechanism and the unexplained remainder.

## Lab 4 Audit a judge

Load synthetic_agent_trials.csv. Count tasks, variants, trials, and rows separately. Rebuild the confusion matrix between human_pass and judge_pass. These are generated reference and judge labels, not observations from actual human reviewers.

Calculate overall agreement, the false-positive rate among reference failures, and the false-discovery fraction among judge approvals. Expected values are about 87.4 percent, 31.8 percent, and 10.0 percent respectively. Explain which quantity matters if a false approval can trigger an unsafe action.

Break the results down by easy and hard task families. Then compare variants' observed success and total cost per verified success. Do not estimate uncertainty by treating all repeated rows as independent tasks. A task-level resampling or hierarchical analysis would be a more appropriate starting point if inference were needed.

## Lab 5 Make missingness visible

Load synthetic_research_records.csv. Count nonmissing verification_minutes and missing values by hard_to_verify and source. Compute the observed mean. Expected result: 84 observed records, 16 missing records, and an observed mean of 5.5 minutes.

Read the generation rule in analyze.py. In this constructed population, 75 easy records would take 4 minutes and 25 hard records would take 18 minutes, for a complete-data mean of 7.5. The gap comes from which records are missing, not random arithmetic noise.

In a real research workflow, the generating rule would be unknown. Write a short note explaining what you could observe, what you would have to assume, and which additional records you would try to verify first.

## Lab 6 Write the next experiment

Choose one scheduler hypothesis: a completion-oriented score, a stronger baseline, or a predictor improvement. Write a one-page protocol with a fixed primary outcome, guardrails, eligible workloads, fresh workload generation rules, pairing, run budget, failure handling, and stopping condition.

Include at least one case designed to disprove the hypothesis. For example, a stronger delay penalty could improve batch finish while harming a background-work requirement. Define how you would detect that regression. Do not choose a new default based only on the same seed 7 case that suggested the change.

## Common mistakes and their repairs

If a join multiplies rows, check its key cardinality before adjusting the aggregate. If a percentile differs from the report, check the definition and population before blaming the library. If a policy looks faster after excluding timeouts, put the timeouts back into the population accounting. If a chart has a dramatic trend, inspect the denominator and collection process. If an agent judge agrees 90 percent of the time, inspect what happens in the other 10 percent and whether the label distribution makes agreement easy.

If a parameter change wins one famous failing case, add that case to development tests and evaluate a frozen choice on fresh workloads. If a simulator looks excellent, test the assumptions that would be most costly to get wrong in deployment. If the conclusion cannot be reproduced from saved inputs, repair the evidence chain before making it more persuasive.

## A compact working checklist

Before collecting: name the decision, primary outcome, population, observational unit, and guardrails.

Before analyzing: preserve raw inputs, record provenance, validate keys and units, reconcile counts, and inspect missingness.

Before comparing: align controls, preserve pairs, identify independent units, include failures, and choose meaningful effect units.

Before explaining: inspect traces, consider alternative mechanisms, separate correlation from intervention, and seek counterexamples.

Before deciding: show uncertainty and limits, include cost, choose a reversible next step when evidence is early, and record what would change your mind.

## A short glossary

Baseline: the alternative used as a reference.

Cohort: a group defined by a relevant shared characteristic.

Confounding: distortion of a comparison by a factor affecting both assignment and outcome.

Counterfactual: the outcome under an alternative intervention that was not observed for the same event.

ECDF: a plot of the fraction of observations at or below each value.

Effect size: the magnitude of a difference in useful units or a specified standardized scale.

Estimand: the precise quantity an analysis is trying to estimate, such as mean paired completion-time difference for a defined workload population.

Guardrail: a constraint or secondary outcome that prevents an unacceptable tradeoff.

Leakage: use of information in development or evaluation that would not be legitimately available in the intended prediction setting.

Observational unit: the kind of thing represented by one observation, such as a task, attempt, or independent run.

Provenance: the origin and transformation history of information.

Right censoring: knowing that an outcome time exceeds an observation cutoff without knowing its eventual value.

Surrogate: a proxy quantity optimized or measured in place of a harder or more expensive goal.

## Where to read next

For hands-on Python data manipulation, read the author's online edition of Wes McKinney's Python for Data Analysis. Work through indexing, grouping, joining, missing data, and time-series chapters as the need arises. [Python for Data Analysis](https://wesmckinney.com/book/)

For plots and graphical choices, use Claus Wilke's Fundamentals of Data Visualization. Recreate one relevant chart with your own data rather than reading it only as a gallery. [Fundamentals of Data Visualization](https://clauswilke.com/dataviz/)

For statistical foundations, OpenIntro Statistics is a gentler starting point than a machine-learning text. For engineering examples and reference procedures, keep the NIST handbook nearby. [OpenIntro Statistics](https://www.openintro.org/book/os/) and [NIST engineering statistics](https://www.itl.nist.gov/div898/handbook/)

When you are ready to model data, An Introduction to Statistical Learning with Applications in Python provides an accessible progression with practical labs. Use the authors' legally available edition. [An Introduction to Statistical Learning](https://www.statlearning.com/)

For time-dependent problems, use Forecasting Principles and Practice. For causal questions, begin with the first, less model-heavy part of Causal Inference What If. These are deeper follow-on texts, not prerequisites for your first useful engineering investigation. [Forecasting Principles and Practice](https://otexts.com/fpp3/) and [Causal Inference What If](https://miguelhernan.org/whatifbook)

The best next exercise is still a small real question from your own system. Preserve the evidence, make one fair comparison, and write down what the result allows you to do.
