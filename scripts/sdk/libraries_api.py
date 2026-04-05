#!/usr/bin/env python3

import argparse

from databricks.sdk import WorkspaceClient


def install_libraries(client: WorkspaceClient, cluster_id: str) -> None:
    client.libraries.install(
        cluster_id=cluster_id,
        libraries=[
            {"pypi": {"package": "pandas==2.2.2"}},
            {"jar": "dbfs:/FileStore/jars/example-library.jar"},
        ],
    )
    print(cluster_id)


def cluster_status(client: WorkspaceClient, cluster_id: str) -> None:
    statuses = client.libraries.cluster_status(cluster_id=cluster_id)
    print(statuses)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Databricks libraries SDK examples")
    subparsers = parser.add_subparsers(dest="command", required=True)

    install_parser = subparsers.add_parser("install")
    install_parser.add_argument("cluster_id")

    status_parser = subparsers.add_parser("status")
    status_parser.add_argument("cluster_id")

    return parser


def main() -> None:
    args = build_parser().parse_args()
    client = WorkspaceClient()

    if args.command == "install":
        install_libraries(client, args.cluster_id)
    elif args.command == "status":
        cluster_status(client, args.cluster_id)


if __name__ == "__main__":
    main()