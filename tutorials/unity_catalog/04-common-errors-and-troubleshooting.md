# 04 - Common Errors and Troubleshooting

## Error: insufficient privileges

Typical message includes words like `PERMISSION_DENIED` or `INSUFFICIENT_PRIVILEGES`.

Check:

- does the principal have `USE CATALOG`?
- does the principal have `USE SCHEMA`?
- does the principal have object-level permission like `SELECT` or `MODIFY`?

## Error: object not found

Often caused by:

- wrong catalog/schema in fully-qualified names
- typo in object path
- querying an object from the wrong workspace context

Use fully-qualified names to avoid ambiguity:

`catalog.schema.table`

## Error: workspace access but no data access

This is expected when workspace permissions exist but Unity Catalog grants are missing.

Fix by granting at appropriate catalog/schema/table levels.

## Error: external table or location access failures

Common causes:

- storage credential is missing or misconfigured
- external location grants are missing
- cloud IAM policy does not allow backing storage access

## Operational checklist

1. Confirm the identity actually running the query or job.
2. Check `SHOW GRANTS` on relevant objects.
3. Validate full object path (`catalog.schema.object`).
4. Verify storage credential and external location grants if external data is involved.
5. Re-test with least-permission grants added step by step.

## One practical tip

When debugging permissions, test with a minimal query against one known table and expand scope only after that succeeds.
