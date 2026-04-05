#!/usr/bin/env bash

set -euo pipefail

: "${DATABRICKS_HOST:?Set DATABRICKS_HOST}"
: "${DATABRICKS_TOKEN:?Set DATABRICKS_TOKEN}"
: "${JOB_ID:?Set JOB_ID}"
: "${EVENT_HUBS_CONNECTION_STRING:?Set EVENT_HUBS_CONNECTION_STRING}"

EVENT_HUB_NAME="${EVENT_HUB_NAME:-iot-sensor-events}"
CONSUMER_GROUP="${CONSUMER_GROUP:-\$Default}"
RUN_DATE="${RUN_DATE:-2026-04-05}"

curl --request POST "$DATABRICKS_HOST/api/2.1/jobs/run-now" \
  --header "Authorization: Bearer $DATABRICKS_TOKEN" \
  --header "Content-Type: application/json" \
  --data "{
    \"job_id\": $JOB_ID,
    \"job_parameters\": {
      \"run_date\": \"$RUN_DATE\",
      \"source_type\": \"event_hubs\",
      \"event_hub_name\": \"$EVENT_HUB_NAME\",
      \"consumer_group\": \"$CONSUMER_GROUP\",
      \"event_hubs_connection_string\": \"$EVENT_HUBS_CONNECTION_STRING\"
    }
  }"