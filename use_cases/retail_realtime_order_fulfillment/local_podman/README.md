# Local Podman Setup for Sources and Destination

This setup creates a local object-store environment for the retail use case using MinIO.

## What is provisioned

- source bucket: `retail-source`
- destination bucket: `retail-destination`
- checkpoint bucket: `retail-checkpoints`
- seeded source files under prefixes:
  - `orders/`
  - `inventory/`
  - `returns/`

## Start the stack

If you use Podman:

```bash
podman compose -f local_podman/compose.yaml up -d
```

If your local container setup maps compose to Docker-compatible commands:

```bash
docker compose -f local_podman/compose.yaml up -d
```

## Verify MinIO

- API endpoint: `http://localhost:9000`
- Console endpoint: `http://localhost:9001`
- Default credentials: `minioadmin` / `minioadmin`

## Connect this to Databricks jobs

Use `scripts/trigger_retail_ingestion_local_minio.sh` and pass these values as job parameters:

- `orders_path=s3a://retail-source/orders/`
- `inventory_path=s3a://retail-source/inventory/`
- `returns_path=s3a://retail-source/returns/`
- `export_path=s3a://retail-destination/fulfillment_kpi/`
- `s3_endpoint=http://host.docker.internal:9000`
- `s3_access_key=minioadmin`
- `s3_secret_key=minioadmin`

## Industry practice notes

- Keep source and destination paths physically separate.
- Keep checkpoint data in a dedicated bucket/prefix.
- Seed deterministic sample files for repeatable integration tests.
- Use non-admin credentials and bucket policies outside local demos.
