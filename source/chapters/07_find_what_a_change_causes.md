# 7 Find out what a change causes

## Observation and intervention

Observational data records what happened under the process that produced it. An experiment changes something deliberately and compares outcomes under a design. Both are useful. They answer different questions.

Suppose GPU tasks finish faster than CPU tasks. Perhaps the GPU is faster for those tasks. Perhaps the scheduler sends easy tasks to the GPU and difficult ones to the CPU. Perhaps GPU tasks are more likely to arrive when the queue is short. A raw comparison mixes these explanations.

A causal question asks what would happen if the same relevant population received one intervention rather than another. You cannot usually observe both outcomes for the exact same real-world event. A design tries to make the observed comparison stand in for that missing counterfactual. Hernán and Robins' open textbook develops this framework and the assumptions needed to use observational comparisons causally. [Causal Inference What If](https://miguelhernan.org/whatifbook)

## Draw the process before adjusting for it

Use a simple causal sketch in words. Task difficulty influences device choice and completion time. Queue state influences device choice and completion time. Policy influences device choice, queue state, and completion time. Those relationships tell you why comparing device groups may be confounded.

A confounder is a pre-intervention common cause that can distort the treatment-outcome comparison. A mediator is part of the pathway through which an intervention works. If a policy changes cache hits and cache hits change latency, cache hits may be a mediator. Adjusting away that change can remove part of the effect you wanted to measure.

Not every available variable should be added to a regression. Conditioning on consequences of the policy or selection process can introduce bias. For a beginner, a clear controlled comparison is often safer than a complicated observational adjustment whose assumptions are hard to defend.

## A practical controlled experiment

Write the protocol before running the comparison. Name the treatment, baseline, eligible workloads, assignment unit, primary outcome, guardrails, run budget, stopping rule, and exclusion criteria. Record the code and configuration versions. Decide how failed runs count.

Randomize assignment or run order when the environment can drift. If all baseline runs occur in the morning and all new-policy runs occur after a driver change or under different machine load, the policy comparison is confounded with time. Alternating or randomizing order within a block reduces that risk.

Block on major known sources of variation. For example, compare both policies on the same workload and machine class, then repeat across seeds or workload batches. A block is a group within which the alternatives are made comparable. NIST's experimental-design guidance distinguishes comparative designs, screening designs, and response-surface designs because those questions call for different experiments. [NIST design selection](https://www.itl.nist.gov/div898/handbook/pri/section3/pri33.htm)

## A seed is not a complete fairness guarantee

Simulation often uses common random inputs so alternatives face the same arrivals and task characteristics. This can make paired comparisons more precise. However, if each policy consumes a single random-number stream in a different order, later draws may no longer refer to equivalent events. “Same seed” then does not guarantee the same realized disturbances.

Separate workload generation from policy execution when possible. Save the generated workload itself. For execution noise, key random draws to stable entities such as task, attempt, phase, and scenario when that matches the model. Document when the alternative legitimately changes which events occur.

The book's companion reads saved results and traces; it does not assume a seed proves identical all-purpose stochastic conditions. The snapshot's configuration and the simulator's explicit limitations remain part of the interpretation.

## Interference changes the unit of assignment

Two tasks sharing one scheduler can affect each other's outcomes. Assigning policy A to some tasks and policy B to others in the same queue may not create two independent systems. One group's long tasks or model loads can delay the other. This is interference.

For a scheduler, consider randomizing whole isolated workload runs, clusters, or time windows rather than individual tasks, depending on the real architecture. Time-window experiments need washout or carryover analysis if queues, caches, or resident models persist across windows. Isolation improves interpretability but may reduce realism. State that tradeoff.

Agents can also interfere. Two agents may share a rate limit, modify the same repository, read one another's outputs, or compete for a tool. Evaluation environments must distinguish intended collaboration from accidental leakage between trials.

## Change one thing when diagnosing

An ablation removes or changes one component to learn what it contributes. The scheduler's protection-off diagnostic asks a narrower question than a full policy replacement. Its delay-weight change is another ablation. These are useful because they avoid bundling a new objective, a wider search, a different predictor, and a bigger memory budget into one opaque improvement.

One-factor-at-a-time tests can miss interactions. Increasing search depth might help only after the score is improved. Changing the score might help only when the candidate generator includes the relevant option. After a local diagnosis, a small factorial design can test combinations deliberately.

For two binary factors, run all four combinations: old and new objective crossed with narrow and wide search. Compare the effect of the objective at each search setting. If the effect changes substantially, there is an interaction worth understanding. Do not average it away and claim a universal component effect.

## Stop for a reason you chose in advance

Watching results and stopping the moment a desired threshold is crossed changes the statistical procedure. A fixed-horizon analysis should use its planned sample size or stopping condition. A sequential design can permit repeated looks, but it must account for them.

Operational guardrails are different. If an experiment causes unacceptable failures or resource use, stop it to protect the system. Record why it stopped and include the failure in the outcome. Safety-driven stopping does not justify reporting only the earlier favorable performance window.

There is no universal minimum number of runs. Plan around the smallest worthwhile effect, expected variation, dependence, and cost of the wrong decision. Use a pilot to estimate variation, then design the confirming test. If resources only permit a small sample, give a descriptive result and a bounded decision rather than an artificially confident claim.

## Transfer from simulation to deployment

Simulation lets you manipulate states that are difficult or costly to reproduce. It is excellent for finding counterexamples and testing an accounting or scheduling mechanism. Its external validity depends on what it models: setup latency, contention, memory behavior, device heterogeneity, failure patterns, and scheduling overhead.

A staged path is reasonable: unit fixtures for correctness; synthetic workloads for mechanism coverage; replay or shadow analysis on observed workloads; isolated real-device benchmarks; then a limited deployment with guardrails. At each stage, ask what new uncertainty is being reduced. Passing one stage does not silently grant the evidence of the next.

Exercise: write a four-run factorial design for two changes you are considering. State the assignment unit and one plausible source of interference. Then explain which result would make you keep only one of the changes.
