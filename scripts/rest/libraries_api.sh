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

install_libraries() {
  local cluster_id="$1"
  local payload
  payload=$(cat <<EOF
{
  "cluster_id": "${cluster_id}",
  "libraries": [
    {
      "pypi": {
        "package": "pandas==2.2.2"
      }
    },
    {
      "jar": "dbfs:/FileStore/jars/example-library.jar"
    }
  ]
}
EOF
)

  api_call POST "/api/2.0/libraries/install" "$payload"
}

cluster_status() {
  local cluster_id="$1"
  api_call GET "/api/2.0/libraries/cluster-status?cluster_id=${cluster_id}"
}

usage() {
  cat <<EOF
Usage:
  $(basename "$0") install <cluster_id>
  $(basename "$0") status <cluster_id>
EOF
}

main() {
  local command="${1:-}"

  case "$command" in
    install)
      if [[ $# -lt 2 ]]; then
        usage
        exit 1
      fi
      install_libraries "$2"
      ;;
    status)
      if [[ $# -lt 2 ]]; then
        usage
        exit 1
      fi
      cluster_status "$2"
      ;;
    *)
      usage
      exit 1
      ;;
  esac
}

main "$@"