#!/usr/bin/env python3

import argparse
import base64

from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import DatabricksError, PermissionDenied

from sdk_auth import add_auth_arguments, build_workspace_client


def mkdirs(client: WorkspaceClient, path: str) -> None:
    client.dbfs.mkdirs(path=path)
    print(path)


def list_path(client: WorkspaceClient, path: str) -> None:
    try:
        found = False
        for item in client.dbfs.list(path=path):
            found = True
            print(item.path, item.file_size)

        if not found:
            print(f"No DBFS objects found under: {path}")
    except PermissionDenied:
        print(f"Access denied for path: {path}")
        print("Hint: public DBFS root may be disabled. Try Unity Catalog Volumes, for example /Volumes.")
    except DatabricksError as exc:
        print(f"Could not list path: {path}")
        print(f"Databricks API error: {exc}")
        print("Hint: for DBFS API, try an explicit DBFS path like dbfs:/FileStore or dbfs:/tmp if enabled.")


def put_file(client: WorkspaceClient, path: str, contents: str) -> None:
    client.dbfs.put(path=path, contents=base64.b64encode(contents.encode()).decode(), overwrite=True)
    print(path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Databricks DBFS SDK examples")
    add_auth_arguments(parser)
    subparsers = parser.add_subparsers(dest="command", required=True)

    mkdirs_parser = subparsers.add_parser("mkdirs")
    mkdirs_parser.add_argument("path")

    list_parser = subparsers.add_parser("list")
    list_parser.add_argument("path", nargs="?", default="/Volumes")

    put_parser = subparsers.add_parser("put")
    put_parser.add_argument("path")
    put_parser.add_argument("contents")

    return parser


def main() -> None:
    args = build_parser().parse_args()
    client = build_workspace_client(args)

    if args.command == "mkdirs":
        mkdirs(client, args.path)
    elif args.command == "list":
        list_path(client, args.path)
    elif args.command == "put":
        put_file(client, args.path, args.contents)


if __name__ == "__main__":
    main()