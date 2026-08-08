#!/usr/bin/env bash

set -euo pipefail

: "${DATABRICKS_HOST:?Set DATABRICKS_HOST}"
: "${DATABRICKS_TOKEN:?Set DATABRICKS_TOKEN}"
: "${JOB_ID:?Set JOB_ID}"

RUN_DATE="${RUN_DATE:-2026-08-08}"
ORDERS_PATH="${ORDERS_PATH:-s3://my-company-landing/retail/orders/}"
INVENTORY_PATH="${INVENTORY_PATH:-s3://my-company-landing/retail/inventory/}"
RETURNS_PATH="${RETURNS_PATH:-s3://my-company-landing/retail/returns/}"

curl --request POST "$DATABRICKS_HOST/api/2.1/jobs/run-now" \
  --header "Authorization: Bearer $DATABRICKS_TOKEN" \
  --header "Content-Type: application/json" \
  --data "{
    \"job_id\": $JOB_ID,
    \"job_parameters\": {
      \"run_date\": \"$RUN_DATE\",
      \"source_type\": \"s3_files\",
      \"orders_path\": \"$ORDERS_PATH\",
      \"inventory_path\": \"$INVENTORY_PATH\",
      \"returns_path\": \"$RETURNS_PATH\"
    }
  }"
