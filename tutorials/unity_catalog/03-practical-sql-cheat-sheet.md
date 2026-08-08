# 03 - Practical SQL Cheat Sheet

## Create and inspect structure

```sql
CREATE CATALOG IF NOT EXISTS retail;
CREATE SCHEMA IF NOT EXISTS retail.curated;
SHOW CATALOGS;
SHOW SCHEMAS IN retail;
SHOW TABLES IN retail.curated;
```

## Create a managed table

```sql
CREATE TABLE IF NOT EXISTS retail.curated.orders_summary (
  order_date DATE,
  orders_count BIGINT,
  gross_revenue DECIMAL(18,2)
);
```

## Read and write pattern

```sql
INSERT INTO retail.curated.orders_summary
SELECT
  current_date() AS order_date,
  COUNT(*) AS orders_count,
  CAST(SUM(amount) AS DECIMAL(18,2)) AS gross_revenue
FROM retail.silver.orders_clean;
```

## Permissions quick commands

```sql
GRANT USE CATALOG ON CATALOG retail TO `retail_analysts`;
GRANT USE SCHEMA ON SCHEMA retail.curated TO `retail_analysts`;
GRANT SELECT ON TABLE retail.curated.orders_summary TO `retail_analysts`;
SHOW GRANTS ON TABLE retail.curated.orders_summary;
```

## Ownership and transfer

```sql
ALTER TABLE retail.curated.orders_summary OWNER TO `retail_data_eng`;
```

## Helpful checks

```sql
DESCRIBE TABLE EXTENDED retail.curated.orders_summary;
```
