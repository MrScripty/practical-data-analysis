# 2 Measure what happened

## Build an account of work

A system is easier to analyze when its records preserve the life of a piece of work. For a scheduler, a task may be submitted, become ready, wait, load a model, execute, drain output, and have its result accepted. It may also fail, retry, be cancelled, or produce a stale result that is correctly rejected. Those are different events with different meanings.

Start with identifiers. A workflow identifier ties together dependent tasks. A task identifier refers to logical work. An attempt identifier distinguishes retries. A run identifier identifies the policy and environment used for an experiment. A trace identifier can connect events across components. Do not overload one field to mean all of them.

An accepted result is especially important. A worker can finish computation after a lease expires or another attempt succeeds. Counting every worker completion as delivered work inflates throughput. For systems with retries, record both executed work and accepted useful output. Extra execution can increase cost without increasing the user's benefit.

OpenTelemetry's trace model provides a useful vocabulary: a trace connects an operation's path, spans represent operations with start and end times, and attributes attach context. You do not have to adopt a particular telemetry stack to benefit from those distinctions. Our book's event schema is deliberately small and domain-specific. [OpenTelemetry traces](https://opentelemetry.io/docs/concepts/signals/traces/)

## An event schema you can reason about

A practical event record contains an event identifier, schema version, run identifier, timestamp, event type, relevant entity identifiers, and a small set of event-specific fields. A phase-start event might include task, attempt, host, device, model, and phase. A policy-decision event might include the eligible candidates, their scores, the chosen action, and the reason other actions were excluded.

Record the facts available at decision time. If the scheduler predicted an 8 second duration but observed 13 seconds later, keep both fields with clear names. Never overwrite the original prediction with the observed duration. Doing so destroys the evidence needed to evaluate prediction quality or detect leakage.

For a policy decision, the complete candidate universe can be large. You may keep a compact structured record of candidate identifiers and score components, plus a separate artifact for full detail. What matters is that a future investigation can distinguish “the good action was unavailable,” “it was feasible but not generated,” and “it was scored lower.” These lead to different fixes.

Keep schema changes explicit. If version 1 measures completion at worker finish and version 2 measures accepted delivery, a single continuous latency chart hides a change in meaning. Preserve the old definition, add the new definition, and annotate the transition. A versioned metric can be more trustworthy than a superficially uninterrupted time series.

## Time has more than one meaning

Wall-clock time identifies when an event happened in the outside world. A monotonic clock measures elapsed duration without moving backward when the system clock changes. Simulated time is the clock inside a model. They are not interchangeable.

Use a monotonic clock for local elapsed durations. Distributed clocks may disagree, so a negative duration formed by subtracting timestamps from different machines is a data-quality warning rather than evidence of time travel. Preserve clock source and synchronization assumptions when you need cross-host timing.

The scheduler case has a particularly important distinction: simulated task durations and measured planner execution times. The simulator can advance its model clock while spending real CPU time computing a decision. Unless the simulator explicitly charges planner time to the modeled schedule, adding the planner's milliseconds to simulated makespan is not a valid correction. Report both and explain how a deployment would account for planning overhead.

Choose and label units at the boundary. Store seconds or milliseconds consistently. Bytes, decimal gigabytes, and binary gibibytes are different units. A number such as 8.5 in a memory field is incomplete evidence until its unit and meaning are known: physical allocation, reservation, peak usage, or model size.

## Derive durations from events

For a simple task with one accepted attempt, define submission latency as accepted-result time minus submission time. Define ready waiting time as dispatch time minus ready time. Define compute time as compute-end minus compute-start. Define setup time from actual load intervals, not from a guess based on whether a model name changed.

These components may overlap. A GPU can load one model while a CPU computes another task. A task's output drain may overlap another task's computation. Summing all task durations does not give wall-clock makespan when work runs concurrently. A timeline makes the overlap visible.

Similarly, waiting time is not necessarily submission-to-start. A task whose dependencies are unfinished is not ready to run. Keep dependency-blocked time separate from ready-queue time if the question concerns scheduler responsiveness. Otherwise you can blame a scheduling policy for work it was not yet allowed to schedule.

For retries, decide whether the user-facing latency starts at the original submission and ends at the accepted result. Usually that is the useful quantity. Attempt-level duration is still valuable for diagnosing execution failures. It belongs in a separate table, with a many-to-one relationship to the logical task.

## Counters, gauges, and distributions

A counter accumulates events, such as accepted results or failures. A gauge describes a current level, such as queue length or allocated memory. A distribution retains variation across observations, such as latency. These types answer different questions.

A high total completion count may simply mean that a system ran longer. Divide by an appropriate observation duration to obtain a rate. A high average resource usage can coexist with severe short bursts that cause failures. Preserve peaks and a time series where burst behavior matters. A low mean latency can coexist with a long tail. Preserve the distribution.

Do not average percentiles from separate groups and call the result the combined percentile. The percentile of a union of observations depends on the full distributions and group sizes. Histograms can support aggregation when their bucket definitions align; precomputed quantiles generally cannot be combined that way. [Prometheus histograms and summaries](https://prometheus.io/docs/practices/histograms/)

## Measure absence as carefully as presence

An event stream naturally contains what occurred. It may omit what never finished. If you calculate latency only from completed tasks, a policy can look faster by leaving hard tasks unfinished. Always reconcile submitted, completed, failed, cancelled, and still-pending work at a stated cutoff.

At cutoff time, an incomplete task has a known minimum age but an unknown eventual completion time. Record its state and age. Do not replace its latency with zero, delete it silently, or pretend the cutoff is its completion. Later chapters discuss censored observations and decision-oriented alternatives such as completion probability by a deadline.

Logging itself can fail. Include counts that reconcile producer and collector views where possible. A missing phase-end event might mean the process crashed or the telemetry was lost. Those are different explanations with the same visible symptom. Keep a quality flag until you can distinguish them.

## Instrument economically

More telemetry is not always better. Fine-grained traces can consume storage, slow the system, and retain private information. Start with fields tied to a decision or a known debugging need. Prefer structured identifiers and compact result summaries to raw user content. Record sampling rules because a sample enriched for errors cannot estimate the ordinary error rate without accounting for that design.

For a first implementation, add a run manifest and a small set of lifecycle events. Then write a validator that checks whether every observed accepted result can be traced back to a submission and a compatible attempt. A measurement system that can explain its own gaps is more useful than one that merely produces many records.

Exercise: draw the lifecycle of one task in your system. Mark which transitions are observed, inferred, or missing. Circle every duration whose endpoints are on different clocks. Those circles identify where you need a measurement decision before a performance conclusion.
