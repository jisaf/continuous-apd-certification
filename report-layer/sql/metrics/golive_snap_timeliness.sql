-- fna:golive:GL03  SNAP application processing timeliness: within 30 days, or 7 days for expedited service.
-- Go Live target: 95%. Compute the state's official rate per SNAP policy; this is the readiness indicator.
SELECT 'GL03-snap-timeliness' AS metric_id,
       DATE_TRUNC('month', d.decided_at) AS period_month,
       SUM(CASE WHEN DATEDIFF('day', a.received_at, d.decided_at) <= CASE WHEN a.expedited THEN 7 ELSE 30 END
                THEN 1 ELSE 0 END) AS numerator,
       COUNT(*) AS denominator,
       ROUND(100.0 * SUM(CASE WHEN DATEDIFF('day', a.received_at, d.decided_at) <= CASE WHEN a.expedited THEN 7 ELSE 30 END
                THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) AS value
FROM C_DETERMINATION d
JOIN C_APPLICATION a ON a.application_id = d.application_id
WHERE d.program = 'snap'
GROUP BY 1, 2
ORDER BY 2;
