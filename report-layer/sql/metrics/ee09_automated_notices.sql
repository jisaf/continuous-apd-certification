-- cms:ee:EE9  Share of eligibility notices generated and sent automatically, by month.
SELECT 'EE9-automated-notices' AS metric_id,
       DATE_TRUNC('month', generated_at) AS period_month,
       SUM(CASE WHEN automatic THEN 1 ELSE 0 END) AS numerator,
       COUNT(*) AS denominator,
       ROUND(100.0 * SUM(CASE WHEN automatic THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) AS value
FROM C_NOTICE
GROUP BY 1, 2
ORDER BY 2;
