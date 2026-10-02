# 8 Analyze a system over time

## Keep order when order matters

A table of durations loses the sequence that produced them. For a queue, sequence is part of the system: arrivals create backlog, backlog affects waiting, model residency changes future setup costs, and failures can trigger retries. Preserve event time and analyze the sequence alongside the distribution.

Start with a timeline of arrivals, completions, queue length, active work, and resource usage. Use a common time axis. A burst of arrivals followed by a growing queue tells a different story from a stable arrival rate followed by collapsing completion throughput.

Distinguish rates from counts. Ten completions in one second and ten in one minute are different workloads. When resampling events into windows, state the window width and boundary convention. A five-minute average can hide a ten-second overload that violates a latency requirement.

## Queue length connects demand and delay

A queue accumulates when arrivals exceed departures over an interval. Even when average capacity exceeds average demand, bursts and variable service times can create waits. High utilization leaves less spare capacity to absorb variation, so optimizing utilization alone can damage responsiveness.

Little's law relates long-run average number in a stable system, throughput, and average time in that same system: L equals lambda times W. If a stable service completes 2 jobs per second and jobs spend an average of 5 seconds in the chosen boundary, the average number inside is 10. The boundary must match: queue-only counts go with queue-only waiting time; in-system counts include service. Finite windows, changing backlog, and inconsistent populations can break a naive application. [Columbia notes on Little's law](https://www.columbia.edu/~ks20/stochastic-I/stochastic-I-LL.pdf)

Use the relationship as a consistency check and a way to think, not as a promise that doubling hardware will halve latency. Bottlenecks, parallelism limits, and workload composition can change when capacity changes.

## Measure a queue by area

A time-weighted average queue length is the area under the queue-length curve divided by elapsed time. If the queue has length 2 for 9 seconds and length 20 for 1 second, the average is 3.8. Averaging just two recorded states gives 11, which is wrong because the states lasted different durations.

For an event-based trace, reconstruct queue length after each arrival or dispatch and integrate until the next change. Make the event ordering convention explicit when several events share a timestamp. For a sampled gauge, account for the sampling interval and missing samples.

This idea generalizes to memory residency and resource utilization. Event counts do not equal time exposure. A state that appears in one log line may persist much longer than a state that produces a hundred lines.

## Separate stable patterns from change

Time-series behavior can include a long-term trend, recurring daily or weekly structure, abrupt shifts, and irregular variation. Compare like periods before declaring an anomaly. Monday morning traffic may differ from Saturday night even when nothing is broken.

For a performance predictor, plot residuals over time: observed duration minus predicted duration, or a clearly defined ratio. Break them down by model, device, size range, and warm or cold state. A persistent positive residual in one cohort suggests underprediction there. A global average near zero can hide offsetting cohort errors.

Do not calculate prediction errors using predictions regenerated after the observation. Preserve the prediction made at the time. Otherwise the model can appear calibrated because it has already learned from the outcome you are testing.

## Drift and anomalies are hypotheses

Drift means that a relevant distribution or relationship changes. Inputs may become longer, a model may load more slowly, a new task family may arrive, or the relationship between features and duration may shift. An anomaly is an observation or interval that is unusual relative to a chosen reference. The reference is part of the claim.

A detector that fires frequently can create more work than it saves. Evaluate its false alarms, missed important events, detection delay, and operational response. An alert should connect to an action or investigation. “Some number changed” is rarely enough.

Control charts are one established way to monitor a process against a reference under stated assumptions. Their limits are not interchangeable with specification limits or user requirements. A stable process can consistently fail a requirement, and a useful process can show a genuine change without becoming unacceptable. [NIST process monitoring](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm)

## Validate on the future direction

When forecasting or predicting time-dependent outcomes, a random train-test split can allow future information to influence a model evaluated on the past. Use splits that respect time. A rolling-origin evaluation repeatedly trains using data available before a cutoff and tests on a later period. The forecast horizon and retraining schedule should resemble the intended use. [Forecasting Principles and Practice on time-series cross-validation](https://otexts.com/fpp3/tscv.html)

Temporal splitting does not automatically eliminate leakage. A feature computed from a full dataset, a label added later, or duplicated entities across periods may still reveal future information. Audit when every feature becomes available.

## Keep unfinished work visible

Suppose one scheduler completes 90 short tasks and leaves 10 long tasks unresolved at cutoff. Another completes all 100. Comparing mean latency only among completed tasks can reward the first policy for leaving work behind.

Useful summaries include completion fraction by a fixed deadline, unresolved count and age, failure count, and a curve of the fraction completed over elapsed time. If you use survival-analysis methods for right-censored observations, their assumptions about censoring need attention. A policy-dependent timeout or selective abandonment can be informative censoring rather than a harmless observation cutoff.

For a beginner, a clear joint report of completion and latency is often safer than a sophisticated estimator used without understanding the missing outcomes. Do not rank an unfinished run as “faster” merely because its last observed completion occurred early. The snapshot distinguishes a completed-batch metric from the last accepted completion for this reason.

## A small operational view

A useful first dashboard can be small: request or task volume, completion or error rate, latency distribution, and saturation or backlog, each with a meaningful time window. Google SRE's monitoring guidance emphasizes latency, traffic, errors, and saturation, while distinguishing user-visible symptoms from internal causes. [Google SRE monitoring](https://sre.google/sre-book/monitoring-distributed-systems/)

Use the dashboard to notice and localize a change. Use a saved trace and controlled analysis to explain it. Dashboards are optimized for repeated observation; investigations need richer context and a record of competing explanations.

Exercise: construct a queue that has the same average arrival rate in two runs but different burst patterns. Predict which should have larger waits, then simulate or calculate the sequence. Keep the service rule fixed. Explain why the average arrival rate alone was insufficient.
