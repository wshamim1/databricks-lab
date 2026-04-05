# 07 - Databricks Glossary

This page is a quick-reference glossary for the most common Databricks terms.

## Platform terms

### Databricks

A cloud platform for data engineering, analytics, SQL, machine learning, governance, and orchestration.

### Workspace

The collaboration area where users work with notebooks, jobs, repos, dashboards, files, and related assets.

### Compute

The execution layer used to run notebooks, jobs, SQL queries, and machine learning workloads.

### All-purpose compute

Interactive compute typically used for development, exploration, and debugging.

### Job compute

Compute used for automated or scheduled job runs.

### SQL warehouse

Compute optimized for SQL analytics, BI queries, and dashboards.

## Storage and architecture terms

### Data lake

Low-cost scalable storage for raw and processed data, usually backed by cloud object storage.

### Data warehouse

A system optimized for structured analytics, reporting, and governed SQL access.

### Lakehouse

An architecture that combines data lake flexibility with warehouse-style management and analytics capabilities.

### Delta Lake

A table format and transaction layer that adds ACID transactions, schema control, and time travel to data lake storage.

### Medallion architecture

A layered pattern that organizes data into Bronze, Silver, and Gold stages.

### Bronze layer

Raw or minimally transformed data, usually closest to the source.

### Silver layer

Cleaned, standardized, and reusable data for downstream use.

### Gold layer

Business-ready data prepared for dashboards, KPIs, and end-user consumption.

## Governance terms

### Unity Catalog

Databricks' centralized governance layer for data and AI assets.

### Metastore

The top-level governance container that holds catalogs and related metadata.

### Catalog

A top-level namespace inside Unity Catalog that contains schemas.

### Schema

A namespace inside a catalog that contains tables, views, and functions.

### Table

A structured dataset stored and queried in Databricks.

### View

A saved SQL query that presents data as a virtual table.

### Volume

A governed storage abstraction for working with files in Unity Catalog.

### Lineage

Information about how data moves through systems, including source objects, transformations, and downstream dependencies.

## Notebook and workflow terms

### Notebook

An interactive document that combines code, markdown, outputs, and visualizations.

### Widget

A parameter input control used inside notebooks to make runs reusable and configurable.

### Job

An automated execution unit that runs notebooks, scripts, SQL, or workflows.

### Workflow

A multi-task orchestration structure with dependencies, retries, and scheduling.

### Scheduler

The mechanism that determines when a job runs, often using cron expressions.

### Task value

A value produced by one workflow task that can be consumed by another downstream task.

## Spark and streaming terms

### Apache Spark

A distributed processing engine used by Databricks for large-scale data workloads.

### Driver

The Spark process that coordinates query planning and job execution.

### Executor

A Spark process that performs distributed computation on partitions of data.

### Shuffle

Data movement between partitions during operations such as joins and aggregations.

### Structured Streaming

Spark's stream processing model for incremental and continuous data pipelines.

### Auto Loader

A Databricks ingestion feature for efficiently discovering and processing new files from cloud storage.

### Checkpoint

Persistent state used by streaming jobs to recover progress and ensure reliable execution.

## SQL and analytics terms

### Dashboard

A visual collection of charts, tables, and KPIs built from query results.

### KPI

A key performance indicator used to track important business metrics.

### Window function

A SQL function that performs calculations across a related set of rows without collapsing them into a grouped result.

## Practical distinction summary

- Databricks is the platform
- Lakehouse is the architecture pattern
- Delta Lake is the table and transaction layer
- Unity Catalog is the governance layer
- A catalog is one namespace inside Unity Catalog
- Compute runs workloads, while the workspace is where users collaborate