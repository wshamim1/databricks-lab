# 01 - Unity Catalog Fundamentals

## What Unity Catalog is

Unity Catalog is Databricks' centralized governance layer for data and AI assets.

It gives a single place to manage:

- object permissions
- discovery and metadata
- lineage
- audit behavior

## Core hierarchy

The common object hierarchy is:

`metastore -> catalog -> schema -> table/view`

Also commonly used:

- `volume` for non-tabular files
- `function` for SQL UDFs
- model assets depending on platform setup

## Why teams adopt it

- one governance model across workspaces
- cleaner domain ownership boundaries
- better security posture than scattered per-workspace ACLs
- easier compliance and audits

## Typical environment pattern

Many teams use separate catalogs for major domains and environments:

- `sales_dev`, `sales_qa`, `sales_prod`
- `finance_dev`, `finance_prod`

Another pattern is a domain catalog with environment-specific schemas:

- `finance.raw_dev`, `finance.raw_prod`
- `finance.curated_dev`, `finance.curated_prod`

## Key point to remember

Unity Catalog is the governance system.
A catalog is one namespace inside that system.
