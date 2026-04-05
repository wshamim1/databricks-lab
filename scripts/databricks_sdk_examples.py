#!/usr/bin/env python3

import argparse
from databricks.sdk import WorkspaceClient


def create_cluster(client: WorkspaceClient) -> None:
    cluster = client.clusters.create(
        cluster_name="demo-sdk-cluster",
        spark_version="15.4.x-scala2.12",
        node_type_id="Standard_DS3_v2",
        num_workers=2,
        autotermination_minutes=20,
    )
    print(cluster.cluster_id)


def list_clusters(client: WorkspaceClient) -> None:
    for cluster in client.clusters.list():
        print(cluster.cluster_id, cluster.cluster_name)


def create_job(client: WorkspaceClient) -> None:
    job = client.jobs.create(
        name="orders_daily_pipeline",
        max_concurrent_runs=1,
        tasks=[
            {
                "task_key": "ingest_orders",
                "notebook_task": {
                    "notebook_path": "/Workspace/Shared/notebooks/ingest_orders",
                    "base_parameters": {
                        "run_date": "2026-04-04",
                        "run_mode": "incremental",
                    },
                },
                "new_cluster": {
                    "spark_version": "15.4.x-scala2.12",
                    "node_type_id": "Standard_DS3_v2",
                    "num_workers": 2,
                },
            }
        ],
    )
    print(job.job_id)


def list_jobs(client: WorkspaceClient) -> None:
    for job in client.jobs.list():
        name = job.settings.name if job.settings else "<unknown>"
        print(job.job_id, name)


def run_job(client: WorkspaceClient, job_id: int) -> None:
    run = client.jobs.run_now(
        job_id=job_id,
        job_parameters={"run_date": "2026-04-04"},
    )
    print(run.run_id)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Databricks SDK examples")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("create-cluster")
    subparsers.add_parser("list-clusters")
    subparsers.add_parser("create-job")
    subparsers.add_parser("list-jobs")

    run_job_parser = subparsers.add_parser("run-job")
    run_job_parser.add_argument("job_id", type=int)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    client = WorkspaceClient()

    if args.command == "create-cluster":
        create_cluster(client)
    elif args.command == "list-clusters":
        list_clusters(client)
    elif args.command == "create-job":
        create_job(client)
    elif args.command == "list-jobs":
        list_jobs(client)
    elif args.command == "run-job":
        run_job(client, args.job_id)
    else:
        parser.error(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    main()