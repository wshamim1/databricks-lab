import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Gold KPI and destination write for retail order fulfillment")
    parser.add_argument("--catalog", required=True)
    parser.add_argument("--schema", required=True)
    parser.add_argument("--export-path", required=True)
    return parser.parse_args()


def ensure_schema(catalog: str, schema: str) -> None:
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.{schema}")


def build_gold_kpi(catalog: str, schema: str) -> None:
    spark.sql(
        f"""
        CREATE OR REPLACE TABLE {catalog}.{schema}.fulfillment_kpi_gold AS
        WITH orders AS (
          SELECT
            order_id,
            sku,
            date_trunc('hour', order_ts) AS order_hour,
            quantity,
            unit_price,
            status
          FROM main.retail_curated.orders_silver
        ),
        inventory AS (
          SELECT
            sku,
            SUM(on_hand_qty - reserved_qty) AS available_qty
          FROM main.retail_curated.inventory_silver
          GROUP BY sku
        ),
        returns AS (
          SELECT
            order_id,
            COUNT(*) AS return_count
          FROM main.retail_curated.returns_silver
          GROUP BY order_id
        )
        SELECT
          o.order_hour,
          o.sku,
          COUNT(DISTINCT o.order_id) AS orders_count,
          SUM(o.quantity) AS units_ordered,
          ROUND(SUM(o.quantity * o.unit_price), 2) AS gross_revenue,
          COALESCE(i.available_qty, 0) AS available_qty,
          SUM(CASE WHEN o.status IN ('late', 'delayed') THEN 1 ELSE 0 END) AS late_order_count,
          SUM(CASE WHEN r.return_count > 0 THEN 1 ELSE 0 END) AS returned_order_count,
          current_timestamp() AS kpi_generated_ts
        FROM orders o
        LEFT JOIN inventory i ON o.sku = i.sku
        LEFT JOIN returns r ON o.order_id = r.order_id
        GROUP BY o.order_hour, o.sku, i.available_qty
        """
    )


def write_destination_extract(catalog: str, schema: str, export_path: str) -> None:
    df = spark.table(f"{catalog}.{schema}.fulfillment_kpi_gold")

    (
        df.write.mode("overwrite")
        .option("compression", "snappy")
        .partitionBy("order_hour")
        .parquet(export_path)
    )

    spark.sql(
        f"""
        CREATE OR REPLACE VIEW {catalog}.{schema}.fulfillment_kpi_latest_vw AS
        SELECT *
        FROM {catalog}.{schema}.fulfillment_kpi_gold
        WHERE order_hour >= current_timestamp() - INTERVAL 24 HOURS
        """
    )


def main() -> None:
    args = parse_args()
    ensure_schema(args.catalog, args.schema)
    build_gold_kpi(args.catalog, args.schema)
    write_destination_extract(args.catalog, args.schema, args.export_path)


if __name__ == "__main__":
    main()
