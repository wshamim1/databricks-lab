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

create_scope() {
  local scope_name="$1"
  local payload
  payload=$(cat <<EOF
{
  "scope": "${scope_name}"
}
EOF
)
  api_call POST "/api/2.0/secrets/scopes/create" "$payload"
}

list_scopes() {
  api_call GET "/api/2.0/secrets/scopes/list"
}

put_secret() {
  local scope_name="$1"
  local key_name="$2"
  local string_value="$3"
  local payload
  payload=$(cat <<EOF
{
  "scope": "${scope_name}",
  "key": "${key_name}",
  "string_value": "${string_value}"
}
EOF
)
  api_call POST "/api/2.0/secrets/put" "$payload"
}

list_secrets() {
  local scope_name="$1"
  api_call GET "/api/2.0/secrets/list?scope=${scope_name}"
}

usage() {
  cat <<EOF
Usage:
  $(basename "$0") create-scope <scope_name>
  $(basename "$0") list-scopes
  $(basename "$0") put-secret <scope_name> <key_name> <string_value>
  $(basename "$0") list-secrets <scope_name>
EOF
}

case "${1:-}" in
  create-scope)
    [[ $# -eq 2 ]] || { usage; exit 1; }
    create_scope "$2"
    ;;
  list-scopes)
    list_scopes
    ;;
  put-secret)
    [[ $# -eq 4 ]] || { usage; exit 1; }
    put_secret "$2" "$3" "$4"
    ;;
  list-secrets)
    [[ $# -eq 2 ]] || { usage; exit 1; }
    list_secrets "$2"
    ;;
  *)
    usage
    exit 1
    ;;
esac