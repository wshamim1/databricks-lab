#!/usr/bin/env python3

from datetime import datetime
from airflow import DAG
from airflow.providers.databricks.operators.databricks import DatabricksRunNowOperator


with DAG(
    dag_id="retail_order_fulfillment_ingestion",
    start_date=datetime(2026, 8, 1),
    schedule="*/15 * * * *",
    catchup=False,
    tags=["retail", "databricks", "ingestion"],
) as dag:
    run_databricks_ingestion = DatabricksRunNowOperator(
        task_id="run_databricks_ingestion",
        databricks_conn_id="databricks_default",
        job_id=12345,
        job_parameters={
            "run_date": "{{ ds }}",
            "run_ts": "{{ ts }}",
            "source_type": "mixed_stream_and_files"
        },
    )
