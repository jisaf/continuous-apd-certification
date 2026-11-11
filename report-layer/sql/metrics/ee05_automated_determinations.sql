-- cms:ee:EE5  Share of Medicaid determinations made with no manual touch, by month.
SELECT 'EE5-automated-determinations' AS metric_id,
       DATE_TRUNC('month', decided_at) AS period_month,
       SUM(CASE WHEN automated THEN 1 ELSE 0 END) AS numerator,
       COUNT(*) AS denominator,
       ROUND(100.0 * SUM(CASE WHEN automated THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) AS value
FROM C_DETERMINATION
WHERE program = 'medicaid'
GROUP BY 1, 2
ORDER BY 2;
