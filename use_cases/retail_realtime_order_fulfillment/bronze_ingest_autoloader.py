import argparse
from pyspark.sql.functions import col, current_timestamp, input_file_name


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bronze ingestion for retail order fulfillment use case")
    parser.add_argument("--catalog", required=True)
    parser.add_argument("--schema", required=True)
    return parser.parse_args()


def ensure_tables(catalog: str, schema: str) -> None:
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.{schema}")


def ingest_orders(catalog: str, schema: str) -> None:
    orders_path = "s3://my-company-landing/retail/orders/"
    checkpoint = "s3://my-company-checkpoints/retail/orders_bronze/"

    (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .option("cloudFiles.inferColumnTypes", "true")
        .load(orders_path)
        .withColumn("ingest_ts", current_timestamp())
        .withColumn("source_file", input_file_name())
        .writeStream.option("checkpointLocation", checkpoint)
        .option("mergeSchema", "true")
        .trigger(availableNow=True)
        .toTable(f"{catalog}.{schema}.orders_bronze")
    )


def ingest_inventory(catalog: str, schema: str) -> None:
    inventory_path = "s3://my-company-landing/retail/inventory/"
    checkpoint = "s3://my-company-checkpoints/retail/inventory_bronze/"

    (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "csv")
        .option("header", "true")
        .option("cloudFiles.inferColumnTypes", "true")
        .load(inventory_path)
        .withColumn("ingest_ts", current_timestamp())
        .withColumn("source_file", input_file_name())
        .writeStream.option("checkpointLocation", checkpoint)
        .option("mergeSchema", "true")
        .trigger(availableNow=True)
        .toTable(f"{catalog}.{schema}.inventory_bronze")
    )


def ingest_returns(catalog: str, schema: str) -> None:
    returns_path = "s3://my-company-landing/retail/returns/"
    checkpoint = "s3://my-company-checkpoints/retail/returns_bronze/"

    (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .option("cloudFiles.inferColumnTypes", "true")
        .load(returns_path)
        .withColumn("ingest_ts", current_timestamp())
        .withColumn("source_file", input_file_name())
        .withColumn("api_source", col("source_system"))
        .writeStream.option("checkpointLocation", checkpoint)
        .option("mergeSchema", "true")
        .trigger(availableNow=True)
        .toTable(f"{catalog}.{schema}.returns_bronze")
    )


def main() -> None:
    args = parse_args()
    ensure_tables(args.catalog, args.schema)
    ingest_orders(args.catalog, args.schema)
    ingest_inventory(args.catalog, args.schema)
    ingest_returns(args.catalog, args.schema)


if __name__ == "__main__":
    main()
