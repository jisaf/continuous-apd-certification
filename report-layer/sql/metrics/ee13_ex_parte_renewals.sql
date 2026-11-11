-- cms:ee:EE13  Share of completed Medicaid renewals done ex parte, by month.
SELECT 'EE13-ex-parte-renewals' AS metric_id,
       DATE_TRUNC('month', completed_at) AS period_month,
       SUM(CASE WHEN ex_parte THEN 1 ELSE 0 END) AS numerator,
       COUNT(*) AS denominator,
       ROUND(100.0 * SUM(CASE WHEN ex_parte THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) AS value
FROM C_RENEWAL
WHERE program = 'medicaid' AND completed_at IS NOT NULL
GROUP BY 1, 2
ORDER BY 2;
