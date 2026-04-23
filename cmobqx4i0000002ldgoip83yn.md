---
title: "Stop Using Accuracy on Imbalanced Data (Interview-Proof Evaluation Checklist)"
seoTitle: "Stop Using Accuracy on Imbalanced Data — Interview-Proof Evaluation Checklist"
seoDescription: "Don't use accuracy on imbalanced data. Lead with the confusion matrix, use precision/recall/F1, PR-AUC/ROC-AUC, tune thresholds, stratified CV, and use SMOTE cautiously."
datePublished: Thu Apr 23 2026 17:18:49 GMT+0000 (Coordinated Universal Time)
cuid: cmobqx4i0000002ldgoip83yn
slug: stop-using-accuracy-imbalanced-data-evaluation-checklist
cover: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1776964570152.png
ogImage: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1776964570152.png

---

<p align="center"><img src="https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1776964570152.png" alt="Cover image" style="max-width:800px;width:100%;height:auto;"/></p>

# Stop Using Accuracy on Imbalanced Data (Interview-Proof Evaluation Checklist)

Accuracy is seductive but dangerous on imbalanced datasets. When positives are rare (e.g., 1% fraud), a model that predicts "negative" for everything gets 99% accuracy — and is worthless. In interviews and production reviews, lead with the confusion matrix and justify the metrics you choose.

## Key concepts (start here in an interview)

- Confusion matrix: report TP, TN, FP, FN — these are the building blocks for every metric.
- Precision (positive predictive value): Precision = TP / (TP + FP). Use when false alarms are costly.
- Recall (sensitivity, true positive rate): Recall = TP / (TP + FN). Use when missing positives is costly.
- F1 score: harmonic mean of Precision and Recall — useful when you want a balance.
- ROC-AUC: threshold-independent measure comparing TPR vs FPR across thresholds.
- PR-AUC: for extreme class imbalance, Precision-Recall AUC often reflects performance on the rare class better than ROC-AUC.

Example: 10,000 examples, 1% positive (100 positives). A model that predicts all negatives: Accuracy = 99% but Recall = 0% and Precision = undefined. This is why accuracy alone lies.

## When to pick which metric

- Business cares about false alarms (e.g., support cost): prioritize Precision.
- Business cares about catching every positive (e.g., medical screening): prioritize Recall (sensitivity).
- You need a single scalar for model selection but both errors matter: use F1 or a weighted F-score tuned to business harm.
- Comparing models regardless of threshold: use ROC-AUC, but prefer PR-AUC when positives are rare.

## Interview-proof evaluation checklist

1. Show the confusion matrix (TP / TN / FP / FN) for at least one realistic threshold.
2. Report Precision, Recall, and F1 — explain which one maps to business cost.
3. Report threshold-independent metrics (ROC-AUC and PR-AUC) for model comparison.
4. Use stratified train/validation/test splits to preserve class ratios.
5. Use k-fold cross-validation (stratified) to reduce variance in estimates.
6. Tune the decision threshold based on business cost (cost matrix or expected value), not just default 0.5.
7. Consider model calibration (Platt scaling, isotonic) if you use probabilities in downstream decisions.
8. Try ensembles (stacking, bagging) — they often improve rare-class detection.
9. If you resample (SMOTE, oversampling), do it only inside cross-validation folds to avoid leakage.
10. Check for label quality: rare events often have noisier labels — audit a sample.

## Practical tips and pitfalls

- Threshold tuning: convert model scores to business outcomes. Example: if catching a fraud saves $500 and investigating a false alarm costs $20, choose the threshold that maximizes expected profit.
- PR-AUC vs ROC-AUC: ROC can be overly optimistic when negatives dominate. Use PR curves to see precision-recall trade-offs at low recall levels.
- SMOTE and synthetic oversampling: useful but can cause overfitting if synthetic samples leak information or if minority subgroups are heterogeneous. Prefer careful feature engineering and ensemble methods first.
- Calibration: a well-calibrated probability lets you compute expected costs directly and set thresholds sensibly.

## Short summary (what to say in an interview)

"I never report accuracy on imbalanced data. I start with a confusion matrix, report Precision/Recall/F1 and PR-AUC/ROC-AUC, and tune the decision threshold to business costs. I use stratified CV, guard against leakage with resampling, and validate model calibration before deployment." 

## Quick checklist you can memorize

- Confusion matrix ✓
- Precision / Recall / F1 ✓
- PR-AUC / ROC-AUC ✓
- Stratified splits & k-fold CV ✓
- Threshold tuned to cost ✓
- Calibration & leakage checks ✓
- SMOTE only inside folds ✓

#MachineLearning #DataScience #MLOps