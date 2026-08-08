#!/usr/bin/env bash

set -euo pipefail

: "${DATABRICKS_HOST:?Set DATABRICKS_HOST}"
: "${DATABRICKS_TOKEN:?Set DATABRICKS_TOKEN}"
: "${JOB_ID:?Set JOB_ID}"

RUN_DATE="${RUN_DATE:-2026-08-08}"

# These values are intended for a local MinIO source/destination setup.
ORDERS_PATH="${ORDERS_PATH:-s3a://retail-source/orders/}"
INVENTORY_PATH="${INVENTORY_PATH:-s3a://retail-source/inventory/}"
RETURNS_PATH="${RETURNS_PATH:-s3a://retail-source/returns/}"
EXPORT_PATH="${EXPORT_PATH:-s3a://retail-destination/fulfillment_kpi/}"
S3_ENDPOINT="${S3_ENDPOINT:-http://host.docker.internal:9000}"
S3_ACCESS_KEY="${S3_ACCESS_KEY:-minioadmin}"
S3_SECRET_KEY="${S3_SECRET_KEY:-minioadmin}"

curl --request POST "$DATABRICKS_HOST/api/2.1/jobs/run-now" \
  --header "Authorization: Bearer $DATABRICKS_TOKEN" \
  --header "Content-Type: application/json" \
  --data "{
    \"job_id\": $JOB_ID,
    \"job_parameters\": {
      \"run_date\": \"$RUN_DATE\",
      \"source_type\": \"minio_local\",
      \"orders_path\": \"$ORDERS_PATH\",
      \"inventory_path\": \"$INVENTORY_PATH\",
      \"returns_path\": \"$RETURNS_PATH\",
      \"export_path\": \"$EXPORT_PATH\",
      \"s3_endpoint\": \"$S3_ENDPOINT\",
      \"s3_access_key\": \"$S3_ACCESS_KEY\",
      \"s3_secret_key\": \"$S3_SECRET_KEY\"
    }
  }"
