"""Dashboard queries over the report-layer views. Plain SQL, portable between Snowflake and DuckDB.

Power BI and Tableau users can paste these into custom SQL or point at the views directly.
"""

STATUS_BY_GATE = """
SELECT gate, status, COUNT(*) AS rules
FROM V_RULE_STATUS
GROUP BY gate, status
ORDER BY gate, status
"""

BLOCKERS = """
SELECT gate, reason, item, source_id, title, responsibility, gate_date
FROM V_GATE_BLOCKERS
WHERE gate = ?
ORDER BY CASE reason WHEN 'Not met' THEN 1 WHEN 'Disputed' THEN 2 WHEN 'At risk' THEN 3
                     WHEN 'Stale' THEN 4 WHEN 'Overdue tracked item' THEN 5 ELSE 6 END, item
"""

BLOCKER_COUNTS = """
SELECT gate, reason, responsibility, COUNT(*) AS items
FROM V_GATE_BLOCKERS
GROUP BY gate, reason, responsibility
ORDER BY gate, reason, responsibility
"""

CALENDAR = """
SELECT due_date, item, item_type, detail
FROM V_CALENDAR
WHERE due_date IS NOT NULL
ORDER BY due_date
"""

TRENDS = """
SELECT generated_at, tagged_tests, passing, failing
FROM V_MAIN_TRENDS
ORDER BY generated_at
"""

TIME_TO_RESTORE = """
SELECT test_id, broke_at, restored_at,
       DATEDIFF('day', broke_at, COALESCE(restored_at, CURRENT_TIMESTAMP)) AS days_open
FROM V_TIME_TO_RESTORE
ORDER BY broke_at DESC
"""

GATES = "SELECT gate, planned_date, scenario FROM GATES ORDER BY planned_date"


def run(conn, sql: str, params=None):
    """Run a query on a DuckDB connection or a Snowpark session; returns (columns, rows)."""
    if hasattr(conn, "sql") and hasattr(conn, "get_current_database"):  # Snowpark session
        if params:
            for p in params:
                sql = sql.replace("?", "'" + str(p).replace("'", "''") + "'", 1)
        df = conn.sql(sql).to_pandas()
        return list(df.columns), df.values.tolist()
    rel = conn.execute(sql, params or [])
    return [d[0] for d in rel.description], rel.fetchall()
