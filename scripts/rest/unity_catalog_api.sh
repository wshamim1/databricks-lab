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

create_catalog() {
  local name="$1"
  local payload
  payload=$(cat <<EOF
{
  "name": "${name}",
  "comment": "Created by REST automation example"
}
EOF
)
  api_call POST "/api/2.1/unity-catalog/catalogs" "$payload"
}

list_catalogs() {
  api_call GET "/api/2.1/unity-catalog/catalogs"
}

create_schema() {
  local catalog_name="$1"
  local schema_name="$2"
  local payload
  payload=$(cat <<EOF
{
  "name": "${schema_name}",
  "catalog_name": "${catalog_name}",
  "comment": "Created by REST automation example"
}
EOF
)
  api_call POST "/api/2.1/unity-catalog/schemas" "$payload"
}

list_schemas() {
  local catalog_name="$1"
  api_call GET "/api/2.1/unity-catalog/schemas?catalog_name=${catalog_name}"
}

get_grants() {
  local securable_type="$1"
  local full_name="$2"
  api_call GET "/api/2.1/unity-catalog/permissions/${securable_type}/${full_name}"
}

usage() {
  cat <<EOF
Usage:
  $(basename "$0") create-catalog <catalog_name>
  $(basename "$0") list-catalogs
  $(basename "$0") create-schema <catalog_name> <schema_name>
  $(basename "$0") list-schemas <catalog_name>
  $(basename "$0") get-grants <securable_type> <full_name>

Examples:
  $(basename "$0") get-grants catalog main
  $(basename "$0") get-grants schema main.demo
EOF
}

case "${1:-}" in
  create-catalog)
    [[ $# -eq 2 ]] || { usage; exit 1; }
    create_catalog "$2"
    ;;
  list-catalogs)
    list_catalogs
    ;;
  create-schema)
    [[ $# -eq 3 ]] || { usage; exit 1; }
    create_schema "$2" "$3"
    ;;
  list-schemas)
    [[ $# -eq 2 ]] || { usage; exit 1; }
    list_schemas "$2"
    ;;
  get-grants)
    [[ $# -eq 3 ]] || { usage; exit 1; }
    get_grants "$2" "$3"
    ;;
  *)
    usage
    exit 1
    ;;
esac