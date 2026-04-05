#!/usr/bin/env python3

import argparse
from databricks.sdk import WorkspaceClient


def create_endpoint(client: WorkspaceClient) -> None:
    endpoint = client.serving_endpoints.create(
        name="demo-revenue-endpoint",
        config={
            "served_models": [
                {
                    "name": "revenue-model-v1",
                    "model_name": "demo_revenue_prediction_model",
                    "model_version": "1",
                    "workload_size": "Small",
                    "scale_to_zero_enabled": True,
                }
            ]
        },
    )
    print(endpoint.name)


def list_endpoints(client: WorkspaceClient) -> None:
    for endpoint in client.serving_endpoints.list():
        print(endpoint.name)


def delete_endpoint(client: WorkspaceClient, endpoint_name: str) -> None:
    client.serving_endpoints.delete(name=endpoint_name)
    print(endpoint_name)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Databricks serving endpoints SDK examples")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("create")
    subparsers.add_parser("list")
    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("endpoint_name")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    client = WorkspaceClient()

    if args.command == "create":
        create_endpoint(client)
    elif args.command == "list":
        list_endpoints(client)
    elif args.command == "delete":
        delete_endpoint(client, args.endpoint_name)


if __name__ == "__main__":
    main()