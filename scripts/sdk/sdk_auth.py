#!/usr/bin/env python3

import argparse
import os
from pathlib import Path

from databricks.sdk import WorkspaceClient


def load_env_file(env_file: str) -> None:
    path = Path(env_file)
    if not path.exists() or not path.is_file():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        if line.startswith("export "):
            line = line[len("export "):].strip()

        if "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()

        if not key:
            continue

        if len(value) >= 2 and ((value[0] == '"' and value[-1] == '"') or (value[0] == "'" and value[-1] == "'")):
            value = value[1:-1]

        os.environ.setdefault(key, value)


def add_auth_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--env-file", default=".env", help="Path to .env file with host/token values")
    parser.add_argument("--host", help="Databricks workspace host, for example https://adb-<id>.<region>.azuredatabricks.net")
    parser.add_argument("--token", help="Databricks personal access token")


def build_workspace_client(args: argparse.Namespace) -> WorkspaceClient:
    load_env_file(args.env_file)

    host = args.host or os.getenv("DATABRICKS_HOST") or os.getenv("host")
    token = args.token or os.getenv("DATABRICKS_TOKEN") or os.getenv("api_token")

    kwargs = {}
    if host:
        kwargs["host"] = host
    if token:
        kwargs["token"] = token

    return WorkspaceClient(**kwargs)
