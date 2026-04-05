#!/usr/bin/env bash

set -euo pipefail

: "${DATABRICKS_HOST:?Set DATABRICKS_HOST}"
: "${DATABRICKS_TOKEN:?Set DATABRICKS_TOKEN}"
: "${JOB_ID:?Set JOB_ID}"

KAFKA_BOOTSTRAP_SERVERS="${KAFKA_BOOTSTRAP_SERVERS:-broker1:9092,broker2:9092}"
KAFKA_TOPIC="${KAFKA_TOPIC:-orders.events}"
RUN_DATE="${RUN_DATE:-2026-04-05}"

curl --request POST "$DATABRICKS_HOST/api/2.1/jobs/run-now" \
  --header "Authorization: Bearer $DATABRICKS_TOKEN" \
  --header "Content-Type: application/json" \
  --data "{
    \"job_id\": $JOB_ID,
    \"job_parameters\": {
      \"run_date\": \"$RUN_DATE\",
      \"source_type\": \"kafka\",
      \"kafka_bootstrap_servers\": \"$KAFKA_BOOTSTRAP_SERVERS\",
      \"kafka_topic\": \"$KAFKA_TOPIC\"
    }
  }"