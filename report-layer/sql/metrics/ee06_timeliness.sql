-- cms:ee:EE6  Share of Medicaid determinations within the time limit, by month.
-- 45 days for MAGI, 90 days for non-MAGI here. Define the state's version to match its Performance
-- Indicator data so the two never disagree.
SELECT 'EE6-timely-determinations' AS metric_id,
       DATE_TRUNC('month', d.decided_at) AS period_month,
       SUM(CASE WHEN DATEDIFF('day', a.received_at, d.decided_at) <= CASE WHEN d.method = 'non-MAGI' THEN 90 ELSE 45 END
                THEN 1 ELSE 0 END) AS numerator,
       COUNT(*) AS denominator,
       ROUND(100.0 * SUM(CASE WHEN DATEDIFF('day', a.received_at, d.decided_at) <= CASE WHEN d.method = 'non-MAGI' THEN 90 ELSE 45 END
                THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) AS value
FROM C_DETERMINATION d
JOIN C_APPLICATION a ON a.application_id = d.application_id
WHERE d.program = 'medicaid'
GROUP BY 1, 2
ORDER BY 2;
