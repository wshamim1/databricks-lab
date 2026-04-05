#!/usr/bin/env python3

import argparse
from databricks.sdk import WorkspaceClient


def create_warehouse(client: WorkspaceClient) -> None:
    warehouse = client.warehouses.create(
        name="analytics-demo-warehouse",
        cluster_size="2X-Small",
        min_num_clusters=1,
        max_num_clusters=1,
        auto_stop_mins=20,
        enable_serverless_compute=False,
    )
    print(warehouse.id)


def list_warehouses(client: WorkspaceClient) -> None:
    for warehouse in client.warehouses.list():
        print(warehouse.id, warehouse.name)


def delete_warehouse(client: WorkspaceClient, warehouse_id: str) -> None:
    client.warehouses.delete(id=warehouse_id)
    print(warehouse_id)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Databricks SQL warehouses SDK examples")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("create")
    subparsers.add_parser("list")
    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("warehouse_id")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    client = WorkspaceClient()

    if args.command == "create":
        create_warehouse(client)
    elif args.command == "list":
        list_warehouses(client)
    elif args.command == "delete":
        delete_warehouse(client, args.warehouse_id)


if __name__ == "__main__":
    main()