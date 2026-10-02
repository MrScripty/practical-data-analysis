# 10 Analyze training data and model results

## Start with the deployment question

A model's test score is meaningful only relative to the cases it is supposed to handle. Is the model predicting durations for familiar task families on new days, recognizing new documents, evaluating new users, or generalizing to unseen organizations? Those are different forms of generalization and require different splits.

Define the target, prediction time, available inputs, and loss associated with errors. A duration predictor for scheduling might need a useful upper bound as much as an accurate mean. A classifier used to block a dangerous action has different error costs from one used to suggest a low-stakes tag.

Keep a simple baseline. For regression, a constant or group-average predictor may be informative. For classification, a majority-class or frequency-based predictor exposes whether a high accuracy is mostly a base-rate effect. A complex model should earn its complexity on the decision that matters.

## Split before learning from the data

Training data fits parameters. Validation data guides model or hyperparameter choices. A test set evaluates a frozen choice. Repeatedly selecting a model based on test performance converts the test set into another validation set.

Preprocessing can leak information too. Fit normalization, feature selection, imputation, vocabulary construction, and other learned transformations using only the training portion within each evaluation fold. Then apply the fitted transformation to the held-out portion. Pipeline tools help enforce this separation. [scikit-learn common pitfalls](https://scikit-learn.org/stable/common_pitfalls.html)

A random row split may be inappropriate when related rows share a document, person, device, source repository, or collection session. Keep related groups together if deployment requires generalization to new groups. Use time-respecting evaluation when the future is the target. The scikit-learn cross-validation guide distinguishes ordinary, grouped, stratified, and time-series split strategies for these reasons. [scikit-learn cross-validation](https://scikit-learn.org/stable/modules/cross_validation.html)

## Leakage can be semantic

A dataset can have no exact duplicate rows and still leak answers. A paraphrase of a training example may appear in the test set. A feature may be recorded only after the outcome. A document's filename may encode its label. A research dataset may include future information unavailable when the prediction would be made.

Audit the information path. For every feature, ask when and how it was created and whether the real model would know it at prediction time. For every split, ask which entities or source materials overlap. The research on leakage in machine-learning-based science shows that these problems can undermine apparently strong results across domains. [Kapoor and Narayanan on leakage](https://arxiv.org/abs/2207.07048)

For training corpora, provenance and duplicate-family identifiers are useful. Store source, version, license or allowed-use information, collection time, transformation history, and known links between derived examples. Do not assume that a public URL implies unrestricted reuse.

## Read learning curves carefully

A training-loss curve shows how an optimization process behaves on its training objective. It is not itself a measure of real task quality. A falling training loss with worsening validation loss may indicate overfitting under the chosen setup. A flat curve could reflect an optimization problem, insufficient model capacity, a difficult target, or an uninformative metric.

Plot against examples or tokens processed and against compute or elapsed time when comparing efficiency. Equal numbers of steps may represent different amounts of data or work. Record batch size, learning-rate schedule, data mixture, checkpoint, and evaluation procedure.

A data-scaling learning curve varies the amount of training data while holding the comparison as fair as possible. It helps ask whether more data appears useful. It does not guarantee that an extrapolated trend will continue or that more of a biased source improves the intended population.

## Choose metrics that expose the error

For a duration predictor, mean absolute error expresses typical error in seconds. Squared-error metrics emphasize large misses. Relative errors emphasize scale but become unstable near zero. Plot observed against predicted values and residuals against input size, task family, and time. A single average can hide systematic underprediction for long or cold tasks.

For classification, a confusion matrix exposes false positives and false negatives. Precision asks how many predicted positives are truly positive under the reference; recall asks how many reference positives were found. Accuracy can be uninformative when one class dominates. Precision-recall and ROC views answer threshold-dependent questions and should be read with class prevalence and deployment costs in mind. [scikit-learn model-evaluation metrics](https://scikit-learn.org/stable/modules/model_evaluation.html)

Do not compare scores calculated on different test populations as if they were head-to-head. Preserve the per-example predictions so you can make paired comparisons and inspect disagreement cases.

## Check probability and interval claims

If a model emits probabilities, evaluate calibration as in the agent chapter. If it emits an upper duration bound intended to cover 90 percent of outcomes, measure the fraction of observed outcomes below the bound. Also inspect bound width and coverage by relevant cohort. An extremely wide bound can have excellent coverage while being operationally useless.

Coverage in a small sample has uncertainty. The scheduler's handful of predictor observations per run cannot establish a stable guarantee. Training and evaluating the bound on the same observations can also make coverage optimistic. Use time-ordered or held-out predictions appropriate to deployment.

A confidence interval for an average is different from a prediction interval for a future individual outcome. Scheduling a single long task often requires understanding the latter. Confusing them can yield a very narrow but inappropriate resource or time promise.

## Use error analysis to choose the next data

Read a sample of failures. Categorize them by a useful mechanism rather than only severity: missing input evidence, label ambiguity, unfamiliar domain, truncation, retrieval failure, tool failure, or a predictable model limitation. Validate the categories on multiple cases before treating them as facts.

Then choose an intervention tied to the mechanism. More random data may help a broad coverage problem. Better labels may help ambiguous supervision. A new feature may help an unobserved state. A product constraint or fallback may be more effective than another training run.

Keep an evaluation report with intended use, test populations, important slices, limitations, and operational behavior. Model Cards provide a structured precedent for this kind of reporting; the goal is to make performance and scope visible to people deciding whether to use the model. [Model Cards for Model Reporting](https://arxiv.org/abs/1810.03993)

Exercise: identify one feature in a current or hypothetical training dataset that might only be available after the outcome. Explain how it could improve a test score while making deployment worse. Then design a split and a data audit that would reveal the problem.
