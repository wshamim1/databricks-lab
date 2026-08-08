#!/usr/bin/env python3

import argparse
import base64
from pathlib import Path

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.workspace import ExportFormat, ImportFormat, Language

from sdk_auth import add_auth_arguments, build_workspace_client


def import_source_notebook(
    client: WorkspaceClient,
    local_file: str,
    workspace_path: str,
    language: str,
    overwrite: bool,
) -> None:
    content = Path(local_file).read_bytes()
    client.workspace.upload(
        path=workspace_path,
        content=content,
        format=ImportFormat.SOURCE,
        language=Language(language),
        overwrite=overwrite,
    )
    print(workspace_path)


def import_jupyter_notebook(
    client: WorkspaceClient,
    local_file: str,
    workspace_path: str,
    overwrite: bool,
) -> None:
    content = Path(local_file).read_bytes()
    client.workspace.upload(
        path=workspace_path,
        content=content,
        format=ImportFormat.JUPYTER,
        overwrite=overwrite,
    )
    print(workspace_path)


def export_notebook(
    client: WorkspaceClient,
    workspace_path: str,
    output_file: str,
    export_format: str,
) -> None:
    response = client.workspace.export(path=workspace_path, format=ExportFormat(export_format))
    if not response.content:
        raise ValueError(f"No export content returned for {workspace_path}")

    decoded = base64.b64decode(response.content)
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(decoded)
    print(output_path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Databricks notebooks SDK examples")
    add_auth_arguments(parser)
    subparsers = parser.add_subparsers(dest="command", required=True)

    import_source_parser = subparsers.add_parser("import-source")
    import_source_parser.add_argument("local_file")
    import_source_parser.add_argument("workspace_path")
    import_source_parser.add_argument(
        "--language",
        choices=["PYTHON", "SQL", "SCALA", "R"],
        default="PYTHON",
        help="Notebook language for SOURCE imports",
    )
    import_source_parser.add_argument("--overwrite", action="store_true")

    import_jupyter_parser = subparsers.add_parser("import-jupyter")
    import_jupyter_parser.add_argument("local_file")
    import_jupyter_parser.add_argument("workspace_path")
    import_jupyter_parser.add_argument("--overwrite", action="store_true")

    export_parser = subparsers.add_parser("export")
    export_parser.add_argument("workspace_path")
    export_parser.add_argument("output_file")
    export_parser.add_argument(
        "--format",
        choices=["SOURCE", "JUPYTER", "DBC", "HTML", "R_MARKDOWN", "AUTO", "RAW"],
        default="SOURCE",
    )

    return parser


def main() -> None:
    args = build_parser().parse_args()
    client = build_workspace_client(args)

    if args.command == "import-source":
        import_source_notebook(client, args.local_file, args.workspace_path, args.language, args.overwrite)
    elif args.command == "import-jupyter":
        import_jupyter_notebook(client, args.local_file, args.workspace_path, args.overwrite)
    elif args.command == "export":
        export_notebook(client, args.workspace_path, args.output_file, args.format)


if __name__ == "__main__":
    main()
