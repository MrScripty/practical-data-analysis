# 1 Begin with a decision

## The first useful question

“Analyze the data” is too broad to guide an investigation. It does not tell you which rows matter, what comparison is fair, or what a useful answer would change. Begin with a decision you could actually make: should we replace the scheduler policy, adjust a scoring term, add a faster execution path, or leave the current design alone?

A workable first question is: “On workloads we expect to run, does the new policy reduce completion time enough to justify its extra planning cost, while keeping failures and long waits acceptable?” This already contains a population, an alternative, an outcome, a cost, and constraints. Each part can become a measurement.

Avoid trying to answer every version of “better” at once. A policy may finish the whole workload sooner while making the typical task slower. It may improve average speed but create rare unacceptable waits. It may reduce simulated completion time while taking much more real time to make a decision. These are different outcomes. Data will not choose your priorities for you.

## A complete investigation in miniature

Consider five tasks run under policies A and B. The following numbers are synthetic task latencies in seconds, matched by task identifier:

| Task | Policy A | Policy B | B minus A |
| --- | ---: | ---: | ---: |
| t1 | 4 | 3 | -1 |
| t2 | 5 | 4 | -1 |
| t3 | 6 | 5 | -1 |
| t4 | 7 | 6 | -1 |
| t5 | 18 | 22 | 4 |

Both policies have mean latency 8 seconds: the sums are both 40 and there are five tasks. B has a better median, 5 instead of 6 seconds. It wins on four of five tasks, but its slowest task takes 4 seconds longer. If a dashboard shows only the mean, you will see no difference. If it shows only the win rate, B looks excellent. If the last task is the urgent one, that recommendation may be wrong.

Suppose the product requirement says that every task in this tiny test must finish within 20 seconds. A passes; B fails. That does not prove A is universally better. It answers a narrower question under an explicit constraint. Suppose instead that the requirement values typical responsiveness and permits the observed tail. The same measurements could justify a different choice. This is why the decision comes first.

Now ask whether these were fair trials. Did both policies see the same inputs? Were the machine and model already warm in one run but cold in the other? Were failed tasks included? Did the policy that ran second benefit from a cache? These questions can matter more than choosing a sophisticated statistical test.

Finally, inspect t5. Its trace may show a long queue, a slow tool call, a retry, or an unfavorable resource assignment. A summary tells you that an important difference exists. A trace helps you construct a testable explanation. You then change one relevant mechanism and rerun. That is a complete analysis loop, even with a spreadsheet and five rows.

## Translate an intention into a measurement

A metric is a rule for turning observations into a number. It needs more than a name. “Latency” might mean submission to first response, ready to execution start, execution time alone, or submission to an accepted final result. All could be useful; mixing them invalidates the comparison.

Write a metric contract before implementation. For each important metric, state the unit of observation, start and end events, physical unit, eligible population, treatment of failures, aggregation rule, and desired direction. For example: “For every submitted workflow, measure seconds from accepted submission to accepted final output; count incomplete workflows separately at the observation cutoff; report median, a tail percentile, and completion fraction.”

There are two kinds of units here. A physical unit is seconds, bytes, dollars, or a fraction. An observational unit is a task, attempt, workflow, user, machine, or independent experimental run. “100 observations” is almost meaningless until you know what was observed. One run can produce a million log messages without becoming a million independent tests.

Choose one primary outcome for the decision. Add guardrails that can veto an apparently good result, such as correctness, failure rate, memory limits, or maximum waiting time. Keep diagnostic metrics, such as cache hits or model loads, because they help explain changes. A diagnostic metric does not automatically deserve to be optimized.

## Write the analysis plan in ordinary language

A useful plan fits in a few paragraphs. State what decision is pending, what alternatives will be compared, what inputs will be held constant, and what evidence would change your mind. Define the smallest improvement worth acting on. A 0.1 percent speedup may be irrelevant if the new policy doubles maintenance cost. A 5 millisecond improvement may matter greatly on a critical interaction path.

Then state what you will not know after the test. A short simulation can compare mechanisms under its own assumptions. It cannot establish device throughput, production stability, or user satisfaction. A labeled agent test can measure behavior on those tasks. It cannot establish that unseen tasks have the same distribution.

This does not weaken the analysis. It makes the result usable. An engineer needs to know whether a number supports changing a line of code, running a wider experiment, or shipping a new default.

## Baselines are part of the argument

A baseline is the alternative you would use without the proposed change. First-in-first-out is a natural scheduler baseline because it is easy to understand. It may not be the strongest practical alternative. A simple policy that avoids unnecessary model reloads could perform better without the complexity of a planner.

Compare against a plausible simple competitor as well as the current implementation. If a new system barely beats a weak baseline and loses to a stronger simple one, the result is a design lesson. It suggests that the useful insight may be much smaller than the architecture built around it.

Keep baseline capabilities aligned. If one policy gets fairness protection, priority boosts, retry handling, or a larger resource budget and another does not, the comparison is between bundles of features. That can be a legitimate product comparison, but it cannot identify the effect of just the scheduling algorithm.

## What to produce

Your first deliverable should be a small evidence package: a question, a metric contract, a table with all eligible cases, one or two informative plots, a statement of what is observed, and a next test or decision. A notebook with many charts is not automatically a better package. The reader should be able to follow the chain from source events to conclusion.

Exercise: choose one system you are building. Complete this sentence: “I need to decide whether to ___ rather than ___, for ___, because ___ is the outcome that matters, subject to ___.” If you cannot finish it, the next useful work is clarifying the decision rather than collecting more data.
