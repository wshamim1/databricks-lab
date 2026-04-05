# Databricks Integration Examples

This folder contains simple examples of how external platforms can trigger or coordinate Databricks jobs and notebooks.

These examples are templates for learning and adaptation rather than production-ready deployments.

## Included examples by platform

### Generic orchestration and CI/CD

- `airflow_databricks_job_example.py`: trigger a Databricks job from Apache Airflow
- `github_actions_trigger_job.yml`: call the Databricks Jobs API from GitHub Actions

### Azure-focused

- `azure_data_factory_databricks_activity.json`: run a Databricks notebook from Azure Data Factory
- `azure_event_hubs_databricks_activity.json`: trigger a Databricks notebook pattern for Event Hubs ingestion

### AWS-focused

- `aws_step_functions_databricks_job.json`: orchestrate a Databricks job from AWS Step Functions

### Transformation tooling

- `dbt/`: minimal dbt on Databricks project structure and model example

## Common use cases

- central enterprise orchestration
- CI/CD-driven job execution
- cross-platform dependencies
- cloud-native workflow integration

## Choosing an example

- Choose Airflow when you need a scheduler that coordinates many systems.
- Choose Azure Data Factory when Databricks is part of an Azure-first data platform.
- Choose the Event Hubs example when IoT or other Azure event streams need to land in Databricks.
- Choose GitHub Actions when source control or CI/CD should trigger Databricks work.
- Choose Step Functions when AWS-native workflows need to include Databricks.
- Choose dbt when SQL transformation models are the main abstraction for curated tables.

## Authentication notes

Typical integrations use one of these patterns:

- personal access token for demos and local testing
- service principal or workload identity for automation
- secret-backed environment variables in the orchestrator

Avoid hardcoding tokens in workflow files.

## Related script examples

- `../scripts/external/kafka_databricks_run_job.sh`: call a Databricks job with Kafka source parameters
- `../scripts/external/event_hubs_databricks_run_job.sh`: call a Databricks job with Azure Event Hubs parameters