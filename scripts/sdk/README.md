# Databricks SDK Scripts

This folder contains Python examples that call Databricks APIs through `databricks-sdk`.

## Auth behavior

All SDK scripts support:

- `.env` auto-loading (default path: `.env`)
- standard variables: `DATABRICKS_HOST`, `DATABRICKS_TOKEN`
- fallback variables: `host`, `api_token`
- CLI overrides: `--env-file`, `--host`, `--token`

## Quick start

Run commands from repository root:

```bash
python3 scripts/sdk/jobs_api.py list
python3 scripts/sdk/workspace_api.py list /Workspace
python3 scripts/sdk/notebooks_api.py import-source local_notebook.py /Workspace/Shared/local_notebook --overwrite
```

## Scripts

- `jobs_api.py`: create, list, and run jobs
- `clusters_api.py`: create, list, and delete clusters
- `cluster_policies_api.py`: create, list, and delete cluster policies
- `dbfs_api.py`: create directories, list paths, and put files in DBFS
- `libraries_api.py`: install libraries and check cluster library status
- `notebooks_api.py`: import/export notebooks through Workspace API
- `permissions_api.py`: get or set object permissions
- `repos_api.py`: list, create, and update repos
- `secrets_api.py`: create scopes, put secrets, list scopes/secrets
- `serving_endpoints_api.py`: create, list, and delete model serving endpoints
- `sql_warehouses_api.py`: create, list, and delete SQL warehouses
- `workspace_api.py`: list, create, and delete workspace paths
- `unity_catalog_api.py`: list/create catalogs and schemas, get grants

## Notebook import/export examples

Import source notebook as Python:

```bash
python3 scripts/sdk/notebooks_api.py import-source \
  scripts/sdk/jobs_api.py \
  /Workspace/Shared/demo_jobs_sdk_notebook \
  --language PYTHON \
  --overwrite
```

Import Jupyter notebook:

```bash
python3 scripts/sdk/notebooks_api.py import-jupyter \
  notebooks/databricks_fundamentals_examples.ipynb \
  /Workspace/Shared/databricks_fundamentals_examples \
  --overwrite
```

Export workspace notebook to local file:

```bash
python3 scripts/sdk/notebooks_api.py export \
  /Workspace/Shared/databricks_fundamentals_examples \
  exports/databricks_fundamentals_examples.ipynb \
  --format JUPYTER
```

## Common permission errors

If you get `PermissionDenied` or `required scopes` errors, your token is valid but lacks API scope/ACLs for that resource domain (for example jobs, unity-catalog, or workspace).
