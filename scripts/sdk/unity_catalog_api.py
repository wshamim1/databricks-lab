#!/usr/bin/env python3

import argparse
import os
from pathlib import Path
from databricks.sdk import WorkspaceClient


def create_catalog(client: WorkspaceClient, name: str) -> None:
    catalog = client.catalogs.create(name=name, comment="Created by SDK automation example")
    print(catalog.name)


def list_catalogs(client: WorkspaceClient) -> None:
    for catalog in client.catalogs.list():
        print(catalog.name)


def create_schema(client: WorkspaceClient, catalog_name: str, schema_name: str) -> None:
    schema = client.schemas.create(
        name=schema_name,
        catalog_name=catalog_name,
        comment="Created by SDK automation example",
    )
    print(f"{schema.catalog_name}.{schema.name}")


def list_schemas(client: WorkspaceClient, catalog_name: str) -> None:
    for schema in client.schemas.list(catalog_name=catalog_name):
        print(f"{schema.catalog_name}.{schema.name}")


def get_grants(client: WorkspaceClient, securable_type: str, full_name: str) -> None:
    grants = client.grants.get(securable_type=securable_type, full_name=full_name)
    print(grants)


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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Databricks Unity Catalog SDK examples")
    parser.add_argument("--env-file", default=".env", help="Path to .env file with host/token values")
    parser.add_argument("--host", help="Databricks workspace host, for example https://adb-<id>.<region>.azuredatabricks.net")
    parser.add_argument("--token", help="Databricks personal access token")
    subparsers = parser.add_subparsers(dest="command")

    create_catalog_parser = subparsers.add_parser("create-catalog")
    create_catalog_parser.add_argument("name")

    subparsers.add_parser("list-catalogs")

    create_schema_parser = subparsers.add_parser("create-schema")
    create_schema_parser.add_argument("catalog_name")
    create_schema_parser.add_argument("schema_name")

    list_schemas_parser = subparsers.add_parser("list-schemas")
    list_schemas_parser.add_argument("catalog_name")

    get_grants_parser = subparsers.add_parser("get-grants")
    get_grants_parser.add_argument("securable_type")
    get_grants_parser.add_argument("full_name")

    return parser


def main() -> None:
    args = build_parser().parse_args()
    load_env_file(args.env_file)

    if not args.command:
        args.command = "list-catalogs"

    host = args.host or os.getenv("DATABRICKS_HOST") or os.getenv("host")
    token = args.token or os.getenv("DATABRICKS_TOKEN") or os.getenv("api_token")

    client = WorkspaceClient(host=host, token=token) if host and token else WorkspaceClient()

    if args.command == "create-catalog":
        create_catalog(client, args.name)
    elif args.command == "list-catalogs":
        list_catalogs(client)
    elif args.command == "create-schema":
        create_schema(client, args.catalog_name, args.schema_name)
    elif args.command == "list-schemas":
        list_schemas(client, args.catalog_name)
    elif args.command == "get-grants":
        get_grants(client, args.securable_type, args.full_name)


if __name__ == "__main__":
    main()