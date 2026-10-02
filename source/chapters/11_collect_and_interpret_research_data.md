# 11 Collect and interpret research data

## A collection is not automatically a sample

A research tool can gather thousands of records quickly. That does not mean the records represent the population you care about. Search rankings, accessible sources, language, geography, publication incentives, and duplicate syndication can shape what is collected.

For a Nearwork-style research workflow, begin with the question and the unit. Is one row a source document, a claim, a person, an organization, a location, or an observation at a place and time? One document can contain many claims, and several documents can repeat the same underlying report. Counting every extracted sentence as independent evidence creates false confidence.

This chapter proposes a research-data workflow for the stated need. It does not assume Nearwork currently has a particular database, extraction model, map, or user interface.

## Separate sources from claims

Keep a source table with a stable identifier, URL or artifact reference, publisher or author when relevant, publication and retrieval dates, content hash or version, access conditions, and collection method. Keep a claim table with the extracted statement, source identifier, location in the source, extraction version, review state, and scope.

A claim should retain context. “The system improved by 20 percent” is incomplete without the baseline, metric, population, conditions, and uncertainty. Store those fields when the research question depends on them. If the source does not provide them, mark the gap rather than supplying a plausible interpretation.

Track whether a field was directly observed, extracted by a model, inferred by a rule, or entered by a reviewer. A downstream analyst should not have to guess which facts have been checked.

Provenance describes how an artifact came to exist. The W3C PROV model distinguishes entities, activities, and agents involved in producing or transforming information. A lightweight application can use those ideas without implementing the entire standard: identify the input, the transformation, the actor or software version, and the output. [W3C PROV primer](https://www.w3.org/TR/prov-primer/)

## Deduplicate at the level of evidence

Exact hashes find identical bytes. Normalized text can find copies with formatting changes. Near-duplicate detection can find paraphrases or syndicated versions. Entity resolution tries to determine whether different names refer to the same real-world entity. These are related but different tasks.

Keep duplicate groups rather than blindly deleting everything that resembles something else. Several copies can be useful for availability or provenance, while still counting as one underlying evidence source for a claim. A correction may look nearly identical to the original but change the one sentence that matters.

Review false merges and false splits. Merging two distinct organizations can corrupt every later statistic about them. Treat ambiguous entity matches as uncertainty, not as a resolved identifier merely because a similarity score is high.

## Missingness is a property of the process

The companion includes 100 synthetic research records. Some difficult records remain unverified, so their verification time is missing. The missingness was generated intentionally to demonstrate a bias: the completed cases make the collection process look easier than it really is.

Count missing values by source, task type, collection stage, and review status. Ask what mechanism makes a value absent. Missing completely at random means the absence is unrelated to the data of interest. Missing at random is a technical assumption that missingness can depend on observed information but, after conditioning on that information, does not depend on the missing values themselves. Missing not at random allows dependence on unobserved values even after conditioning on observed information. The labels are assumptions about a process, not properties you can reliably infer from a null-count table alone. [Rubin on inference with missing data](https://dash.harvard.edu/entities/publication/73120378-8764-6bd4-e053-0100007fdf3b)

In the generated example, 84 records have observed times and 16 are unresolved. The observed mean is 5.5 minutes. Because this is a constructed example, we also know the complete-data mean implied by its generating rule: 7.5 minutes. The easy records dominate the observed subset. In real research you usually do not know the missing values, which is precisely why documenting the collection process matters.

For a practical first pass, report which records are missing and why, compare the observed groups, and perform a sensitivity analysis. If all unresolved records took much longer than observed ones, would the conclusion change? If it would, the missing records are decision-relevant and deserve follow-up.

Do not confuse a field that was not collected with a negative answer. “No evidence found” is different from “evidence that the statement is false.” This distinction is particularly important when a research agent searches only a limited set of sources.

## Model extraction needs evaluation too

If an agent extracts facts from documents, evaluate the extraction stage separately from the final analysis. Sample source passages and compare extracted fields to a reference review. Measure errors that matter: omitted claims, unsupported additions, wrong units, wrong dates, mixed entities, and lost qualifications.

A model can return valid JSON containing incorrect content. Schema validation catches structural failure; source-grounded review catches semantic failure. Keep both checks. Confidence scores from the extractor need calibration before they can support automatic acceptance.

Stratify the review sample when failures are likely to differ across source types or languages. If you oversample difficult cases to find problems, do not report the resulting raw error rate as the overall production rate without accounting for the sampling design.

## Spatial data adds another measurement layer

If a research question genuinely involves location, record what a coordinate represents: an exact observation, an address geocode, an approximate city center, or a region. Store the coordinate reference system and precision. A point displayed on a map can look exact even when the source is vague.

Latitude and longitude are angular coordinates, not distances in meters. Distance and area calculations require a method appropriate to the coordinate system, geography, and desired accuracy. GeoPandas distinguishes assigning a coordinate reference system from transforming coordinates to another system; confusing those operations can place data incorrectly. [GeoPandas projections](https://geopandas.org/en/stable/docs/user_guide/projections.html)

A map of raw counts often reflects where more people or records exist. If the question concerns rates, use a relevant denominator such as population, exposure, or collection effort. Show uncertainty for small counts and avoid precise-looking rates based on tiny denominators.

Spatially nearby observations may be correlated. A random split that puts neighboring or repeated sites in both training and test sets can overstate generalization to new areas. Consider geographic holdouts when that matches the intended use. Also treat precise personal locations as sensitive information: collect and expose only what the research purpose requires.

## Write a dataset description before reuse

A reusable dataset needs a short description of why it was collected, what it contains, how it was collected and transformed, what is missing, who or what is underrepresented, and what uses are inappropriate. Datasheets for Datasets offers a systematic model for documenting those questions. [Gebru and colleagues on datasheets](https://arxiv.org/abs/1803.09010)

The description should travel with exported data. A CSV without its population and collection history can be easy to misuse. A provenance field is not just paperwork; it is what lets an analyst distinguish ten independent studies from ten articles describing one study.

Exercise: design source and claim tables for a question you might research. Include one field that preserves uncertainty, one that identifies duplicate evidence, and one that records review status. Then write a query that counts independent source groups rather than raw extracted claims.
