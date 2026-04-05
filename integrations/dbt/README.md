# dbt on Databricks Example

This example shows a minimal dbt project structure for running SQL models on Databricks.

It is intentionally small so you can use it as a starting point for:

- transformation projects on Databricks SQL or job compute
- CI/CD validation for dbt models
- combining dbt with a medallion-style silver and gold layer

## Files included

- `dbt_project.yml`: basic dbt project configuration
- `profiles.yml.example`: sample Databricks connection profile
- `models/orders_daily_sales.sql`: example model reading from a silver table and producing a gold-style output

## Notes

- Update catalog, schema, host, and HTTP path for your workspace
- Store credentials in secrets or environment variables in real deployments
- Treat this as a template, not a production-ready project