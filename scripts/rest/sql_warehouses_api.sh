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

create_warehouse() {
  local payload='{
    "name": "analytics-demo-warehouse",
    "cluster_size": "2X-Small",
    "min_num_clusters": 1,
    "max_num_clusters": 1,
    "auto_stop_mins": 20,
    "enable_serverless_compute": false
  }'

  api_call POST "/api/2.0/sql/warehouses" "$payload"
}

list_warehouses() {
  api_call GET "/api/2.0/sql/warehouses"
}

delete_warehouse() {
  local warehouse_id="$1"
  api_call DELETE "/api/2.0/sql/warehouses/${warehouse_id}"
}

usage() {
  cat <<EOF
Usage:
  $(basename "$0") create
  $(basename "$0") list
  $(basename "$0") delete <warehouse_id>
EOF
}

case "${1:-}" in
  create)
    create_warehouse
    ;;
  list)
    list_warehouses
    ;;
  delete)
    [[ $# -eq 2 ]] || { usage; exit 1; }
    delete_warehouse "$2"
    ;;
  *)
    usage
    exit 1
    ;;
esac