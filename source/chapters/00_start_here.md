# Practical Data Analysis for Engineering Decisions

## Start here

This book is for someone who can build software but is beginning to learn data analysis. The aim is practical: inspect what went into a system, what it did, and what came out; find the pattern that matters; then decide what to change and how to check it.

Our running example is a scheduler whose elaborate policy sometimes loses to a simple one. We investigate possible measurement errors, unfair comparisons, missing scheduling actions, inaccurate predictions, and a score that rewards the wrong thing.

The same methods apply to evaluating agents and their judges, understanding training results, and collecting research data. Chrema and Nearwork appear as possible applications based on the needs described for them. Their private implementations were not inspected. Those examples are proposals, not claims about their current code or data.

### What is real in this book

The scheduler case uses actual reports and event traces from a Python simulator. These are measured simulator results, not measurements of a production service or real GPU. Simulation exposes mechanisms and enables controlled comparisons, but can omit effects that matter in reality.

Other datasets are labeled synthetic. They isolate concepts and make calculations reproducible. A convincing chart made from invented data remains an illustration; it is never evidence that a real project works.

### A route through the book

Read Chapters 1 through 6 in order, from a question to a complete investigation. Chapters 7 and 8 cover experiments and behavior over time. Read Chapters 9 through 11 for your current project. Chapter 12 turns findings into a decision; Chapter 13 provides labs, solutions, a glossary, and further reading.

The companion includes data, executable analysis, and the numbers behind the figures. Run it unchanged, then alter one question or chart. A small analysis you understand is a better starting point than a complicated notebook you cannot explain.

### Four sentences to keep separate

An observation states what was measured. An interpretation proposes a reason. An experiment tests a change under stated conditions. A decision says what you will do given the evidence, costs, and remaining uncertainty.

For example: “This run took longer” is an observation. “CPU placement may have caused the delay” is an interpretation. “We changed only the placement rule and reran matched workloads” describes an experiment. “Keep the simple policy while testing a revised objective” is a decision. Many bad analyses become plausible by silently moving from the first sentence to the last.
