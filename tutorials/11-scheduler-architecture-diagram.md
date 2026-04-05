# 11 - Scheduler Architecture Diagram

This page shows how internal and external schedulers can work with Databricks.

## Diagram

```mermaid
flowchart LR
    subgraph schedulers[Scheduling and Orchestration]
        native[Databricks Native Scheduler]
        airflow[Apache Airflow]
        adf[Azure Data Factory]
        step[AWS Step Functions]
        events[Event Triggers]
    end

    subgraph control[Trigger Layer]
        jobsapi[Databricks Jobs API]
        workflow[Databricks Workflows]
    end

    subgraph processing[Databricks Execution]
        notebooks[Notebooks and Python Tasks]
        sql[SQL Tasks]
        compute[Job Compute]
    end

    subgraph storage[Lakehouse]
        bronze[Bronze]
        silver[Silver]
        gold[Gold]
    end

    subgraph consumers[Downstream Consumers]
        bi[BI and Dashboards]
        apps[Applications]
        ml[ML and Serving]
    end

    native --> workflow
    airflow --> jobsapi
    adf --> jobsapi
    step --> jobsapi
    events --> jobsapi

    jobsapi --> workflow
    workflow --> notebooks
    workflow --> sql
    notebooks --> compute
    sql --> compute

    compute --> bronze
    bronze --> silver
    silver --> gold

    gold --> bi
    gold --> apps
    silver --> ml
```

## Interpretation

- Databricks native scheduling feeds directly into Databricks workflows
- External orchestrators usually trigger Databricks through the Jobs API
- Workflows run notebooks, Python tasks, and SQL tasks on Databricks compute
- Processed data flows into Bronze, Silver, and Gold layers
- Downstream BI, apps, and ML consumers read curated outputs

## Main takeaway

Internal scheduling is simplest when Databricks is the orchestration center.

External scheduling is usually the better choice when Databricks is only one part of a larger enterprise workflow.