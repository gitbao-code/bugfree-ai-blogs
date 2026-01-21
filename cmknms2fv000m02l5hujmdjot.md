---
title: "SQL Interview Edge: Master Window Functions in 60 Seconds"
seoTitle: "SQL Interview Edge: Master Window Functions in 60 Seconds"
seoDescription: "Master SQL window functions fast: ROW_NUMBER, RANK, running totals, and moving averages with examples and 3 interview practice tasks."
datePublished: Wed Jan 21 2026 06:17:19 GMT+0000 (Coordinated Universal Time)
cuid: cmknms2fv000m02l5hujmdjot
slug: sql-interview-edge-master-window-functions-60-seconds
cover: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1768976213057.png
ogImage: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1768976213057.png

---

<p align="center"><img src="https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1768976213057.png" alt="SQL window functions" style="max-width:700px; width:100%; height:auto;"/></p>

# SQL Interview Edge: Master Window Functions in 60 Seconds

Window functions are an interview favorite because they compute per-row results without collapsing your data. The core pattern to remember:

```
<function>(...) OVER (
  PARTITION BY <cols>    -- optional: splits rows into groups
  ORDER BY <cols>        -- optional: defines ordering inside each partition
  ROWS|RANGE BETWEEN ...  -- optional: frame control for moving aggregates
)
```

Quick guide to the most-used functions:

- ROW_NUMBER(): gives a unique sequential number to rows in the window. Use when you need a deterministic, tie-breaking sequence.
- RANK(): assigns the same rank to ties but leaves gaps after ties (1, 2, 2, 4).
- DENSE_RANK(): like RANK() but without gaps (1, 2, 2, 3).
- SUM() OVER (ORDER BY ... ROWS UNBOUNDED PRECEDING): running total.
- AVG() OVER (... ROWS BETWEEN n PRECEDING AND CURRENT ROW): moving average.

Important tips:

- Window functions do NOT reduce the number of rows — they add per-row calculations.
- You must specify ORDER BY for running totals and moving aggregates to be deterministic.
- Use ROWS for a physical number of rows (e.g., last 3 rows), RANGE for value-based frames (can behave differently with ties).
- Window functions cannot be used in WHERE (use a subquery or CTE), but they can appear in SELECT and ORDER BY.

Examples you can memorize and adapt:

1) Running total by date

```sql
SELECT
  order_id,
  order_date,
  amount,
  SUM(amount) OVER (ORDER BY order_date
                    ROWS UNBOUNDED PRECEDING) AS running_total
FROM orders;
```

2) Salary rank within a department

```sql
SELECT
  employee_id,
  department,
  salary,
  RANK() OVER (PARTITION BY department
               ORDER BY salary DESC) AS dept_rank
FROM employees;
```

If you want no gaps in ranks, replace RANK() with DENSE_RANK().

3) 3-month moving average (per store)

```sql
SELECT
  store_id,
  month_date,
  sales,
  AVG(sales) OVER (PARTITION BY store_id
                    ORDER BY month_date
                    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS moving_avg_3m
FROM store_monthly_sales;
```

Practice these 3 exercises until you can write the queries from memory:

- Running total for orders (global or per-customer).
- Department salary rank (and switch between RANK/DENSE_RANK/ROW_NUMBER).
- 3-period moving average using ROWS BETWEEN n PRECEDING AND CURRENT ROW.

Mastering these patterns gives you immediate leverage in interviews — window functions are a fast way to show SQL fluency.