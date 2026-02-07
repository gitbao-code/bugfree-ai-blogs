---
title: "Mean vs Median: Avoid Interview Traps Caused by Outliers"
seoTitle: "Mean vs Median: Avoid Interview Traps Caused by Outliers"
seoDescription: "Prefer median (and IQR) over mean in interviews for skewed data like salaries or latency—median resists outliers and better represents the typical."
datePublished: Sat Feb 07 2026 18:16:19 GMT+0000 (Coordinated Universal Time)
cuid: cmlcmy66u000402jygacp574q
slug: mean-vs-median-interview-outliers
cover: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1770488163955.png
ogImage: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1770488163955.png

---

<img src="https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1770488163955.png" alt="Mean vs Median" style="max-width:100%;width:600px;height:auto;">

# Mean vs Median: The One Interview Trap Outliers Set for You

Quick takeaway: In interviews, don't reflexively report the mean. For skewed data (salaries, latency, revenue), report the median — and often the IQR — because the median resists extreme outliers and better represents the "typical".

## Mean vs Median — the essentials

- Mean: the arithmetic average; it uses every value. Great for symmetric, well-behaved distributions.
- Median: the middle value of the sorted data. It ignores magnitude of extremes and remains stable when outliers appear.

Why this matters in interviews: a single extreme value (an outlier) can drag the mean far from the center of the bulk of your data. If you present the mean as the typical number without qualifying the distribution shape, you risk giving a misleading answer — and showing weak statistical judgment.

## A quick numeric example

Dataset A (typical salaries, in $k): 50, 55, 60, 62, 65
- Mean = 58.4
- Median = 60

Dataset B (one outlier): 50, 55, 60, 62, 1000
- Mean = 245.4 (pulled up heavily by the outlier)
- Median = 60 (unchanged)

In Dataset B the mean implies a "typical" salary near $245k, which is clearly wrong for the majority of employees. The median remains a faithful summary.

## What to report in an interview

- If the data are skewed or contain outliers, report the median and a measure of spread (IQR: interquartile range).
- If the data look symmetric and roughly normal, the mean (with SD) is fine.
- Optionally mention alternatives if appropriate: trimmed mean, geometric mean, or a log transform can help in some analyses.

Sample phrasing you can use in an interview:

- "If outliers or skew exist, I report the median (and often the IQR), not the mean."
- "I'll check the distribution first — if it's roughly symmetric I'll use the mean and SD; if it's skewed I'll report the median and IQR."

## Why this shows good judgment

Choosing the median when appropriate demonstrates you understand data robustness and can communicate realistic, actionable summaries. It signals you won't be misled by a single extreme value and that you're thoughtful about which summary statistics match the data.

## TL;DR

Defaulting to the mean is the common interview trap. Look at the distribution; if it's skewed or has outliers, use median + IQR and explain your choice.

#DataScience #Statistics #MachineLearning