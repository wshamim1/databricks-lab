# Retail Ingestion Integrations

This folder contains integration templates that trigger the retail ingestion and transformation pipeline.

## Files

- `airflow_retail_ingestion_orchestration.py`: Airflow DAG that calls Databricks `jobs/run-now`

For local source/destination setup, see `../local_podman/`.

## Typical production pattern

1. Source loaders push data to cloud landing paths or event streams.
2. Orchestrator triggers Databricks pipeline with run parameters.
3. Databricks executes bronze, silver, and gold tasks with retries.
4. Monitoring stack checks freshness, quality, and SLA breaches.

## Security practices

- Use service principals or workload identity where available.
- Store Databricks host/token and source credentials in secrets managers.
- Avoid embedding credentials directly in DAGs or state machines.
