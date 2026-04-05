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

create_policy() {
  local payload='{
    "name": "shared-compute-policy",
    "definition": "{\"autotermination_minutes\":{\"type\":\"fixed\",\"value\":20},\"num_workers\":{\"type\":\"range\",\"maxValue\":4,\"minValue\":1},\"node_type_id\":{\"type\":\"allowlist\",\"values\":[\"Standard_DS3_v2\",\"Standard_DS4_v2\"]}}"
  }'

  api_call POST "/api/2.0/policies/clusters/create" "$payload"
}

list_policies() {
  api_call GET "/api/2.0/policies/clusters/list"
}

delete_policy() {
  local policy_id="$1"
  local payload
  payload=$(cat <<EOF
{
  "policy_id": "${policy_id}"
}
EOF
)

  api_call POST "/api/2.0/policies/clusters/delete" "$payload"
}

usage() {
  cat <<EOF
Usage:
  $(basename "$0") create
  $(basename "$0") list
  $(basename "$0") delete <policy_id>
EOF
}

case "${1:-}" in
  create)
    create_policy
    ;;
  list)
    list_policies
    ;;
  delete)
    [[ $# -eq 2 ]] || { usage; exit 1; }
    delete_policy "$2"
    ;;
  *)
    usage
    exit 1
    ;;
esac