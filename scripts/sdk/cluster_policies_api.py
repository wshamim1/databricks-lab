#!/usr/bin/env python3

import argparse
from databricks.sdk import WorkspaceClient


POLICY_DEFINITION = """
{
  "autotermination_minutes": {"type": "fixed", "value": 20},
  "num_workers": {"type": "range", "minValue": 1, "maxValue": 4},
  "node_type_id": {"type": "allowlist", "values": ["Standard_DS3_v2", "Standard_DS4_v2"]}
}
""".strip()


def create_policy(client: WorkspaceClient) -> None:
    policy = client.cluster_policies.create(
        name="shared-compute-policy",
        definition=POLICY_DEFINITION,
    )
    print(policy.policy_id)


def list_policies(client: WorkspaceClient) -> None:
    for policy in client.cluster_policies.list():
        print(policy.policy_id, policy.name)


def delete_policy(client: WorkspaceClient, policy_id: str) -> None:
    client.cluster_policies.delete(policy_id=policy_id)
    print(policy_id)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Databricks cluster policies SDK examples")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("create")
    subparsers.add_parser("list")
    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("policy_id")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    client = WorkspaceClient()

    if args.command == "create":
        create_policy(client)
    elif args.command == "list":
        list_policies(client)
    elif args.command == "delete":
        delete_policy(client, args.policy_id)


if __name__ == "__main__":
    main()