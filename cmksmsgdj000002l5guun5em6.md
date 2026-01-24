---
title: "A/B Testing Interviews: Stop Using the Wrong Standard Error"
seoTitle: "A/B Testing Interviews — Use the Pooled Standard Error for Two-Proportion z-Tests"
seoDescription: "In A/B test interviews, use the pooled standard error for hypothesis tests of two proportions; use unpooled SE for confidence intervals."
datePublished: Sat Jan 24 2026 18:16:28 GMT+0000 (Coordinated Universal Time)
cuid: cmksmsgdj000002l5guun5em6
slug: ab-testing-pooled-standard-error
cover: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1769278558605.png
ogImage: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1769278558605.png

---

<div align="center">
  <img src="https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1769278558605.png" alt="A/B testing" width="700">
</div>

Most candidates miss a small but crucial point in two-proportion z-tests: when you test H0: CTR_A = CTR_B you must compute the standard error using the *pooled* rate.

Why? Because the null hypothesis says the two groups share the same underlying rate p. Under H0 you therefore estimate one shared p from all the data:

p_pooled = (clicks_A + clicks_B) / (impr_A + impr_B)

Then the standard error for the difference in sample proportions is

SE_pooled = sqrt( p_pooled * (1 - p_pooled) * (1/n_A + 1/n_B) )

If you don't pool (i.e., if you use the separate-sample SE), you can inflate or deflate the SE and flip your "significant" decision. The pooled SE is what the theory for the two-proportion z-test requires because the test assumes a common p under H0.

Quick numeric demonstration

- A: n_A = 10,000 impressions, x_A = 200 clicks -> p_A = 0.0200
- B: n_B = 1,000 impressions, x_B = 30 clicks -> p_B = 0.0300
- Difference in sample proportions = p_B - p_A = 0.01

Pooled estimate:
- p_pooled = 230 / 11,000 ≈ 0.020909
- SE_pooled = sqrt(0.020909 * 0.979091 * (1/10000 + 1/1000)) ≈ 0.00475
- z = 0.01 / 0.00475 ≈ 2.106 → two-sided p ≈ 0.035 (statistically significant at α = 0.05)

Unpooled (separate) SE:
- SE_unpooled = sqrt( p_A*(1-p_A)/n_A + p_B*(1-p_B)/n_B ) ≈ 0.00557
- z = 0.01 / 0.00557 ≈ 1.794 → two-sided p ≈ 0.072 (not significant at α = 0.05)

Same data, two different decisions—because one calculation pooled the rates (appropriate for hypothesis testing under H0) and the other didn't.

Interview-friendly rule of thumb

- For hypothesis testing of equality of two proportions (two-proportion z-test): use the pooled standard error.
- For estimating effect size or constructing confidence intervals for each proportion or for the difference: use the unpooled (separate) standard error.

Quick caveats and tips

- The two-proportion z-test (pooled SE) relies on large-sample approximations. For small counts (especially <5 expected events in a cell), use Fisher's exact test or exact/adjusted methods.
- If you want to be conservative when samples are small or assumptions shaky, consider exact tests or permutation/bootstrap approaches.
- In interviews: state the null hypothesis, show how you compute p_pooled, write the pooled SE formula, and say when you’d switch to an exact test. That demonstrates both theory and practical judgment.

Bottom line: pooled SE for hypothesis testing (equality under H0); unpooled SE for confidence intervals and estimation. Mixing them up is a common interview pitfall—now you won't make that mistake.