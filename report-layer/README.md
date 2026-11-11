# Report layer

Optional SQL templates, a local DuckDB builder, and a dashboard that join pipeline evidence with the state's
own data on the state's existing platform. Start with [`docs/report-layer.md`](../docs/report-layer.md).

```sh
python report-layer/duckdb/build_local.py
streamlit run report-layer/dashboard/app.py -- --duckdb out/report-layer/cert.duckdb
```
