#!/usr/bin/env python3

import argparse
from databricks.sdk import WorkspaceClient


def create_scope(client: WorkspaceClient, scope_name: str) -> None:
    client.secrets.create_scope(scope=scope_name)
    print(scope_name)


def list_scopes(client: WorkspaceClient) -> None:
    for scope in client.secrets.list_scopes():
        print(scope.name)


def put_secret(client: WorkspaceClient, scope_name: str, key_name: str, string_value: str) -> None:
    client.secrets.put_secret(scope=scope_name, key=key_name, string_value=string_value)
    print(f"{scope_name}:{key_name}")


def list_secrets(client: WorkspaceClient, scope_name: str) -> None:
    for secret in client.secrets.list_secrets(scope=scope_name):
        print(secret.key)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Databricks secrets SDK examples")
    subparsers = parser.add_subparsers(dest="command", required=True)

    create_scope_parser = subparsers.add_parser("create-scope")
    create_scope_parser.add_argument("scope_name")

    subparsers.add_parser("list-scopes")

    put_secret_parser = subparsers.add_parser("put-secret")
    put_secret_parser.add_argument("scope_name")
    put_secret_parser.add_argument("key_name")
    put_secret_parser.add_argument("string_value")

    list_secrets_parser = subparsers.add_parser("list-secrets")
    list_secrets_parser.add_argument("scope_name")

    return parser


def main() -> None:
    args = build_parser().parse_args()
    client = WorkspaceClient()

    if args.command == "create-scope":
        create_scope(client, args.scope_name)
    elif args.command == "list-scopes":
        list_scopes(client)
    elif args.command == "put-secret":
        put_secret(client, args.scope_name, args.key_name, args.string_value)
    elif args.command == "list-secrets":
        list_secrets(client, args.scope_name)


if __name__ == "__main__":
    main()