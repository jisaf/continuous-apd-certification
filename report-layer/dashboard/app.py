"""Certification readiness dashboard (Streamlit).

Snowflake:  create a Streamlit in Snowflake app with this file and queries.py, in the CERT schema,
            owned by a role that can read the CERT views (CERT_VIEWER). Viewers use their own login.
Locally:    pip install streamlit duckdb
            streamlit run report-layer/dashboard/app.py -- --duckdb out/report-layer/cert.duckdb
"""

from __future__ import annotations

import sys

import queries as q
import streamlit as st


def connect():
    try:
        from snowflake.snowpark.context import get_active_session  # Streamlit in Snowflake
        return get_active_session()
    except Exception:
        import duckdb
        path = sys.argv[sys.argv.index("--duckdb") + 1] if "--duckdb" in sys.argv else "out/report-layer/cert.duckdb"
        return duckdb.connect(path, read_only=True)


def table(conn, sql, params=None):
    cols, rows = q.run(conn, sql, params)
    data = [dict(zip(cols, r, strict=False)) for r in rows]
    try:  # newer Streamlit
        st.dataframe(data, width="stretch", hide_index=True)
    except Exception:  # older Streamlit (for example in Streamlit in Snowflake) rejects width="stretch"
        st.dataframe(data, use_container_width=True, hide_index=True)
    return cols, rows


st.set_page_config(page_title="Certification readiness", layout="wide")
conn = connect()
st.title("Certification readiness")
st.caption("Readiness signal from pipeline evidence and the state's tracked items. "
           "Met is not CMS's 'Evidence Satisfactory' or FNA's concurrence; only the agencies make those findings.")

_, gates = q.run(conn, q.GATES)
gate_names = [g[0] for g in gates] or ["ORR", "FNA-UAT", "FNA-PILOT", "CR"]
gate = st.selectbox("Gate", gate_names)

st.header("Open blockers")
st.write("A list, never a percentage: one missing letter matters as much as many passing tests.")
table(conn, q.BLOCKERS, [gate])

c1, c2 = st.columns(2)
with c1:
    st.header("Blockers by reason and owner")
    table(conn, q.BLOCKER_COUNTS)
with c2:
    st.header("Rule status by gate")
    table(conn, q.STATUS_BY_GATE)

st.header("Calendar")
table(conn, q.CALENDAR)

st.header("Tagged tests on main over time")
cols, rows = q.run(conn, q.TRENDS)
if rows:
    st.line_chart({c: [r[i] for r in rows] for i, c in enumerate(cols) if c != "generated_at"})

st.header("Time to restore (blameless: by test, never by person)")
table(conn, q.TIME_TO_RESTORE)
