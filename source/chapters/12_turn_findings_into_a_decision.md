# 12 Turn findings into an engineering decision

## Decide what the evidence permits

An investigation should end with an action, a deliberate choice to wait, or a specific missing piece of evidence. “More research is needed” is rarely enough. Name the uncertainty that could change the decision and the cheapest credible way to reduce it.

For the scheduler, the evidence permits keeping a repaired candidate-coverage test and investigating the score. It does not justify calling the proposed policy generally superior. A stronger simple baseline wins the held-out randomized mean, the seed count is small, and real-device behavior has not been measured.

A useful decision can still be made under uncertainty. Keep the simpler default while testing a promising mechanism. Ship a narrow improvement only where its preconditions and guardrails are clear. Choose a fallback for failure cases. Uncertainty changes the scope and reversibility of the decision rather than forcing all work to stop.

## Distinguish constraints from preferences

A hard constraint defines an unacceptable outcome: exceeding a memory limit, violating a required permission, corrupting a result, or leaving critical work unbounded. A preference trades one desirable property against another: lower latency, lower cost, fewer reloads, or simpler implementation.

Do not blend a hard constraint into a weighted average where enough speed can compensate for violating it. Evaluate feasibility first, then compare tradeoffs among feasible choices. For soft objectives, state the weights or present the frontier without pretending there is one universal winner.

The scheduler's shaped score illustrates why units and scale matter. A setup penalty and a progress reward may be mathematically combinable but poorly aligned with the user-facing objective. Sensitivity analysis should show whether modest changes to weights alter the choice. If a recommendation flips under plausible weights, that is a decision-relevant fact.

## Include the cost of complexity

A policy's total cost includes computation, observability, testing, debugging, maintenance, and operational risk. A small benchmark win can disappear when planning overhead, failed attempts, or human review are included. Conversely, a modest speed improvement on a heavily used critical path may be worth substantial engineering effort.

Use the costs relevant to the decision, in their own units where possible. Report simulated time, real planning time, monetary cost, and developer burden separately before combining them. If you convert them into one utility score, make the conversion assumptions visible.

Prefer reversible experiments when the evidence is early. A shadow mode or feature flag can reduce the cost of learning. Define rollback conditions before rollout, and preserve enough version and trace information to diagnose a regression.

## Write a decision memo that can be challenged

A compact memo can have five parts: decision, evidence, interpretation, limitations, and next test. Put the strongest result first, including an inconvenient one. Link the data and reproducible calculation. State what would change the recommendation.

Here is a worked example based on the simulator investigation:

“Keep the current simple policy as the general default while testing revised completion-oriented scoring. On seed 7, repairing candidate coverage did not change the proposed policy's 56.642 second batch finish, compared with FIFO's 45.695 seconds. Forcing one final GPU continuation reduced the proposed run to 47.039 seconds, demonstrating a large local contribution from that placement decision under the simulator. It did not remove the full gap. On three fresh seeds per scenario with matched service controls, the proposed randomized mean was 47.084 seconds, versus residency's 40.343. The next test will compare fixed objective profiles and stronger simple baselines on fresh workloads, while tracking completion, tail waits, unfinished work, and planning cost. Real-device validation remains necessary before deployment claims.”

This memo is useful because another engineer can disagree with the decision while checking the same facts. It does not bury the caveats in a footnote or call a local intervention a general policy.

## Keep the analysis alive only while it has a purpose

Save the data snapshot, code, report, and decision. Add important counterexamples to regression tests. Track the follow-up experiment with a clear stopping condition. Do not turn every completed investigation into a permanent dashboard or an endless stream of alerts.

A mature analytical practice reduces repeated uncertainty. It gives future you a way to know what was tried, why a choice was made, and what would justify revisiting it. The value is better decisions, not the number of plots produced.
