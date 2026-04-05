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

mkdirs() {
  local path="${1:-dbfs:/tmp/demo-sdk}"
  api_call POST "/api/2.0/dbfs/mkdirs" "{\"path\": \"${path}\"}"
}

list_status() {
  local path="${1:-dbfs:/tmp}"
  api_call GET "/api/2.0/dbfs/list?path=${path}"
}

put_file() {
  local path="${1:-dbfs:/tmp/demo-sdk/hello.txt}"
  local contents="${2:-Hello from Databricks DBFS REST API examples}"
  local base64_contents
  base64_contents=$(printf '%s' "$contents" | base64)
  api_call POST "/api/2.0/dbfs/put" "{\"path\": \"${path}\", \"contents\": \"${base64_contents}\", \"overwrite\": true}"
}

usage() {
  cat <<EOF
Usage:
  $(basename "$0") mkdirs [dbfs_path]
  $(basename "$0") list [dbfs_path]
  $(basename "$0") put [dbfs_path] [text_contents]
EOF
}

main() {
  local command="${1:-}"

  case "$command" in
    mkdirs)
      mkdirs "${2:-}"
      ;;
    list)
      list_status "${2:-}"
      ;;
    put)
      put_file "${2:-}" "${3:-}"
      ;;
    *)
      usage
      exit 1
      ;;
  esac
}

main "$@"