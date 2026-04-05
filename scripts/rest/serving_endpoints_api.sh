#!/usr/bin/env bash

set -euo pipefail

if [[ -z "${DATABRICKS_HOST:-}" || -z "${DATABRICKS_TOKEN:-}" ]]; then
  echo "DATABRICKS_HOST and DATABRICKS_TOKEN must be set." >&2
  exit 1
fi

api_call() {
  local method="$1"
  local endpoint="$2"
  local payload="${3:-}"

  if [[ -n "$payload" ]]; then
    curl --silent --show-error --fail \
      --request "$method" \
      --url "$DATABRICKS_HOST$endpoint" \
      --header "Authorization: Bearer $DATABRICKS_TOKEN" \
      --header "Content-Type: application/json" \
      --data "$payload"
  else
    curl --silent --show-error --fail \
      --request "$method" \
      --url "$DATABRICKS_HOST$endpoint" \
      --header "Authorization: Bearer $DATABRICKS_TOKEN"
  fi
}

create_endpoint() {
  local payload='{
    "name": "demo-revenue-endpoint",
    "config": {
      "served_models": [
        {
          "name": "revenue-model-v1",
          "model_name": "demo_revenue_prediction_model",
          "model_version": "1",
          "workload_size": "Small",
          "scale_to_zero_enabled": true
        }
      ]
    }
  }'

  api_call POST "/api/2.0/serving-endpoints" "$payload"
}

list_endpoints() {
  api_call GET "/api/2.0/serving-endpoints"
}

delete_endpoint() {
  local endpoint_name="$1"
  api_call DELETE "/api/2.0/serving-endpoints/${endpoint_name}"
}

usage() {
  cat <<EOF
Usage:
  $(basename "$0") create
  $(basename "$0") list
  $(basename "$0") delete <endpoint_name>
EOF
}

case "${1:-}" in
  create)
    create_endpoint
    ;;
  list)
    list_endpoints
    ;;
  delete)
    [[ $# -eq 2 ]] || { usage; exit 1; }
    delete_endpoint "$2"
    ;;
  *)
    usage
    exit 1
    ;;
esac