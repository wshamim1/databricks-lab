#!/usr/bin/env python3

from datetime import datetime

from airflow import DAG
from airflow.providers.databricks.operators.databricks import DatabricksRunNowOperator


with DAG(
    dag_id="databricks_orders_pipeline_integration",
    start_date=datetime(2026, 4, 1),
    schedule="0 6 * * *",
    catchup=False,
    tags=["databricks", "integration"],
) as dag:
    run_orders_pipeline = DatabricksRunNowOperator(
        task_id="run_orders_pipeline",
        databricks_conn_id="databricks_default",
        job_id=12345,
        job_parameters={
            "run_date": "{{ ds }}",
            "run_mode": "incremental",
        },
    )