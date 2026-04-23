---
title: "Stop Using Accuracy on Imbalanced Data (Interview-Proof Evaluation Checklist)"
seoTitle: "Stop Using Accuracy on Imbalanced Data — Interview-Proof Evaluation Checklist"
seoDescription: "Why accuracy fails for imbalanced data and an interview-proof checklist: confusion matrix, precision/recall/F1, PR-AUC, stratified CV, threshold tuning, SMOTE cautions."
datePublished: Thu Apr 23 2026 17:16:37 GMT+0000 (Coordinated Universal Time)
cuid: cmobqualk000002jo0byw81ch
slug: stop-using-accuracy-on-imbalanced-data-evaluation-checklist
cover: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1776964570152.png
ogImage: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1776964570152.png

---

# Stop Using Accuracy on Imbalanced Data

<img src="https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1776964570152.png" alt="Confusion matrix and evaluation checklist" style="max-width:700px;height:auto;display:block;margin:12px 0;" />

Accuracy is misleading when classes are imbalanced. If fraud is 1% of transactions, a model that always predicts "no fraud" is 99% accurate but utterly useless. In interviews (and reports), lead with the confusion matrix and choose metrics that reflect business risk.

## Quick refresher: confusion matrix

| Actual \ Predicted | Positive | Negative |
|---:|:---:|:---:|
| Positive | True Positive (TP) | False Negative (FN) |
| Negative | False Positive (FP) | True Negative (TN) |

Report these four numbers first — they make every subsequent metric meaningful.

## Core metrics and when to use them

- Precision = TP / (TP + FP)
  - Use when false alarms are costly (e.g., manual review workload).
- Recall (a.k.a. Sensitivity) = TP / (TP + FN)
  - Use when missing positives is costly (e.g., undetected fraud or disease).
- F1 = 2 * (Precision * Recall) / (Precision + Recall)
  - Harmonic mean of precision and recall; balances both.
- F-beta
  - Use when you want to weight recall (beta>1) or precision (beta<1) more heavily.
- Specificity = TN / (TN + FP)
  - When true negatives matter.
- Balanced Accuracy = (Sensitivity + Specificity) / 2
  - Corrects plain accuracy for imbalanced classes.
- Matthews Correlation Coefficient (MCC)
  - A single-number summary that handles imbalance well.
- ROC-AUC
  - Good for threshold-independent ranking performance, but can be optimistic on very imbalanced data.
- Precision-Recall AUC (PR-AUC)
  - Often more informative than ROC-AUC for highly imbalanced problems because it focuses on the positive class.

## Evaluation and model-selection best practices (interview checklist)

1. Lead with the confusion matrix and class prevalence. Always show TP/TN/FP/FN and the base rate.
2. Show a naive baseline (e.g., predict majority class) so your model’s lift is clear.
3. Pick metrics that map to business cost: precision, recall, F-beta, PR-AUC, or cost-weighted expected value.
4. Use PR-AUC alongside ROC-AUC for imbalanced tasks — PR-AUC highlights performance on the rare class.
5. Use stratified train/validation/test splits and/or stratified k-fold CV to preserve class ratios.
6. Calibrate probabilities (Platt scaling, isotonic) if you’ll threshold on probability or combine models.
7. Tune the decision threshold to optimize business metrics (cost matrix, expected utility), not just a symmetric threshold.
8. Consider ensembles (stacking, bagging) to stabilize predictions on rare classes.
9. Use resampling (SMOTE, ADASYN) carefully — validate that synthetic examples improve real-world performance and avoid leakage.
10. Report uncertainty: confidence intervals, bootstrapped metrics, or CV variability.
11. Visualize: confusion matrix heatmap, Precision-Recall curve, ROC curve, and calibration plot.
12. Test on a realistic holdout (temporal split if data is time-dependent) and monitor post-deployment for drift.

## Practical tips

- Always state class prevalence up front — a 0.1% positive rate changes interpretation.
- If business costs are known, convert FP/FN into dollars and optimize expected value directly.
- When precision matters, show how many false positives per 1,000 alerts your system will generate.
- When recall matters, report how many positives you’ll miss at your chosen operating point.

## One-sentence takeaway

Don't report accuracy alone on imbalanced datasets. Start with the confusion matrix, choose metrics tied to business consequences (precision/recall/F-beta/PR-AUC), and tune thresholds and validation strategies accordingly.

#MachineLearning #DataScience #MLOps
