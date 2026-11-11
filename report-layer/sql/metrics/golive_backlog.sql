-- fna:golive:GL10 (backlog report)  Open work items by days overdue, as of today.
SELECT 'GL10-backlog' AS metric_id,
       item_type,
       CASE WHEN DATEDIFF('day', due_date, CURRENT_DATE) <= 30 THEN '1-30'
            WHEN DATEDIFF('day', due_date, CURRENT_DATE) <= 60 THEN '31-60'
            WHEN DATEDIFF('day', due_date, CURRENT_DATE) <= 90 THEN '61-90'
            ELSE '90+' END AS days_overdue,
       COUNT(*) AS items
FROM C_WORK_ITEM
WHERE status <> 'closed' AND due_date < CURRENT_DATE
GROUP BY 1, 2, 3
ORDER BY 2, 3;
