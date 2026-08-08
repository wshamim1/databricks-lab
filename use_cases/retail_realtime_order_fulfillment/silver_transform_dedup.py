import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Silver transform for retail order fulfillment use case")
    parser.add_argument("--catalog", required=True)
    parser.add_argument("--schema", required=True)
    return parser.parse_args()


def ensure_schema(catalog: str, schema: str) -> None:
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.{schema}")


def transform_orders(catalog: str, schema: str) -> None:
    spark.sql(
        f"""
        CREATE OR REPLACE TABLE {catalog}.{schema}.orders_silver AS
        WITH ranked AS (
          SELECT
            order_id,
            customer_id,
            sku,
            CAST(order_ts AS TIMESTAMP) AS order_ts,
            CAST(quantity AS INT) AS quantity,
            CAST(unit_price AS DOUBLE) AS unit_price,
            status,
            ingest_ts,
            source_file,
            ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY ingest_ts DESC) AS rn
          FROM main.retail_raw.orders_bronze
          WHERE order_id IS NOT NULL
            AND customer_id IS NOT NULL
            AND sku IS NOT NULL
            AND quantity > 0
        )
        SELECT
          order_id,
          customer_id,
          sku,
          order_ts,
          quantity,
          unit_price,
          status,
          ingest_ts,
          source_file
        FROM ranked
        WHERE rn = 1
        """
    )


def transform_inventory(catalog: str, schema: str) -> None:
    spark.sql(
        f"""
        CREATE OR REPLACE TABLE {catalog}.{schema}.inventory_silver AS
        WITH typed AS (
          SELECT
            warehouse_id,
            sku,
            CAST(snapshot_ts AS TIMESTAMP) AS snapshot_ts,
            CAST(on_hand_qty AS INT) AS on_hand_qty,
            CAST(reserved_qty AS INT) AS reserved_qty,
            ingest_ts,
            source_file
          FROM main.retail_raw.inventory_bronze
          WHERE warehouse_id IS NOT NULL
            AND sku IS NOT NULL
        ),
        ranked AS (
          SELECT *,
            ROW_NUMBER() OVER (
              PARTITION BY warehouse_id, sku
              ORDER BY snapshot_ts DESC, ingest_ts DESC
            ) AS rn
          FROM typed
        )
        SELECT
          warehouse_id,
          sku,
          snapshot_ts,
          on_hand_qty,
          reserved_qty,
          ingest_ts,
          source_file
        FROM ranked
        WHERE rn = 1
        """
    )


def transform_returns(catalog: str, schema: str) -> None:
    spark.sql(
        f"""
        CREATE OR REPLACE TABLE {catalog}.{schema}.returns_silver AS
        SELECT
          return_id,
          order_id,
          sku,
          CAST(return_ts AS TIMESTAMP) AS return_ts,
          reason_code,
          api_source,
          ingest_ts,
          source_file
        FROM main.retail_raw.returns_bronze
        WHERE return_id IS NOT NULL
          AND order_id IS NOT NULL
        """
    )


def main() -> None:
    args = parse_args()
    ensure_schema(args.catalog, args.schema)
    transform_orders(args.catalog, args.schema)
    transform_inventory(args.catalog, args.schema)
    transform_returns(args.catalog, args.schema)


if __name__ == "__main__":
    main()
