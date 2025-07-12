#!/usr/bin/env python3
"""
MedData CLI Tool - Command Line Interface for MedData Engineering Hub.

This module provides a unified CLI for managing MedData datasets, including
creating, processing, publishing and generating assets for datasets.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
import subprocess
import re

from scripts.utils.printer import printer
from scripts.utils.subprocess_handler import subprocess_handler
from scripts.utils.config_manager import config_manager

# Define module exports
__all__ = ["main", "create_parser"]


def init_dataset(args: argparse.Namespace) -> None:
    """
    Initialize a new dataset.
    
    Args:
        args: Command line arguments containing id, name, and description
    """
    try:
        printer.header(f"Initializing dataset: {args.id}")

        # Use subprocess handler to run the create-dataset.py script
        cmd = [str(config_manager.paths.project_root / "scripts" / "create-dataset.py"), args.id, args.name,
               args.description]
        subprocess_handler.run_python_script(
            cmd[0], cmd[1:],
            check=True
        )

        printer.success(f"Dataset '{args.id}' initialized successfully!")
    except subprocess.CalledProcessError as e:
        printer.error(f"Failed to initialize dataset '{args.id}'", e)
        sys.exit(1)


def process_dataset(args: argparse.Namespace) -> None:
    """
    Process a dataset.
    
    Args:
        args: Command line arguments containing dataset id
    """
    try:
        printer.header(f"Processing dataset: {args.id}")

        # Use subprocess handler to run the process-dataset.py script
        subprocess_handler.run_python_script(
            str(config_manager.paths.project_root / "scripts" / "process-dataset.py"),
            [args.id],
            check=True
        )

        printer.success(f"Dataset '{args.id}' processed successfully!")
    except subprocess.CalledProcessError as e:
        printer.error(f"Failed to process dataset '{args.id}'", e)
        sys.exit(1)


def publish_dataset(args: argparse.Namespace) -> None:
    """
    Publish a dataset.
    
    Args:
        args: Command line arguments containing dataset id, token, and platforms
    """
    try:
        printer.header(f"Publishing dataset: {args.id}")

        # Prepare command arguments
        cmd_args = [args.id]

        # Add token if provided, otherwise use from config
        if args.token:
            cmd_args.extend(["--token", args.token])

        # Add platforms if specified
        if args.platforms:
            cmd_args.extend(["--platforms"] + args.platforms)

        # Use subprocess handler to run the publish-dataset.py script
        subprocess_handler.run_python_script(
            str(config_manager.paths.project_root / "scripts" / "publish-dataset.py"),
            cmd_args,
            check=True
        )

        printer.success(f"Dataset '{args.id}' published successfully!")
    except subprocess.CalledProcessError as e:
        printer.error(f"Failed to publish dataset '{args.id}'", e)
        sys.exit(1)


def generate_assets(args: argparse.Namespace) -> None:
    """
    Generate assets for datasets.
    
    Args:
        args: Command line arguments, may contain dataset_id
    """
    try:
        if args.dataset_id:
            printer.header(f"Generating assets for dataset: {args.dataset_id}")
        else:
            printer.header("Generating assets for all datasets")

        # Prepare command arguments
        cmd_args = []
        if args.dataset_id:
            cmd_args.append(args.dataset_id)

        # Use subprocess handler to run the generate-assets.py script
        subprocess_handler.run_python_script(
            str(config_manager.paths.project_root / "scripts" / "generate-assets.py"),
            cmd_args,
            check=True
        )

        printer.success("Assets generated successfully!")
    except subprocess.CalledProcessError as e:
        printer.error("Failed to generate assets", e)
        sys.exit(1)


def generate_docs(args: argparse.Namespace) -> None:
    """
    Generate documentation for a dataset.
    
    Args:
        args: Command line arguments containing dataset id
    """
    try:
        printer.header(f"Generating documentation for dataset: {args.id}")

        # Use subprocess handler to run the generate-docs.py script
        subprocess_handler.run_python_script(
            str(config_manager.paths.project_root / "scripts" / "generate-docs.py"),
            [args.id],
            check=True
        )

        printer.success(f"Documentation for dataset '{args.id}' generated successfully!")
    except subprocess.CalledProcessError as e:
        printer.error(f"Failed to generate documentation for dataset '{args.id}'", e)
        sys.exit(1)


def generate_site(args: argparse.Namespace) -> None:
    """
    Generate the static site.
    
    Args:
        args: Command line arguments, may contain serve flag
    """
    try:
        if args.serve:
            printer.header("Generating and serving the static site")
            cmd = ["bundle", "exec", "jekyll", "serve"]
        else:
            printer.header("Generating the static site")
            cmd = ["bundle", "exec", "jekyll", "build"]

        # Use subprocess handler to run jekyll
        subprocess_handler.run(cmd, check=True)

        if args.serve:
            printer.success("Site is being served at http://localhost:4000")
        else:
            printer.success("Site generated successfully!")
    except subprocess.CalledProcessError as e:
        printer.error("Failed to generate site", e)
        sys.exit(1)


def doctor_dataset(args: argparse.Namespace) -> None:
    """Check dataset files required for publishing to Hugging Face or Kaggle.

    This command ensures that all mandatory files exist before attempting to
    publish a dataset. If files are missing it exits with a non-zero status so
    that CI/CD pipelines can fail early.
    """
    dataset_id = args.id

    # Determine selected platforms. If none passed, validate for both
    check_hf = args.hf or not (args.hf or args.kg)
    check_kg = args.kg or not (args.hf or args.kg)

    printer.header(f"Running doctor for dataset: {dataset_id}")

    def _auto_generate_missing_files(ds_id: str, ds_dir: Path, missing_files: list[str]) -> None:
        """Attempt to populate missing docs using templates located in example-docs.
        Will skip non-documentation files such as data.parquet.
        """
        template_root = config_manager.paths.project_root / "example-docs"
        generated: list[str] = []

        for abs_fp in missing_files:
            target = Path(abs_fp)
            if target.suffix == ".parquet":
                continue  # cannot auto-generate data file

            # Determine platform template folder that has the file
            rel_path = target.relative_to(ds_dir)
            template_path = None
            for plat in ["huggingface", "kaggle"]:
                cand = template_root / plat / rel_path
                if cand.exists():
                    template_path = cand
                    break
            if not template_path:
                continue  # no template available

            target.parent.mkdir(parents=True, exist_ok=True)
            content = template_path.read_text(encoding="utf-8")
            # simple placeholder replacements
            content = re.sub(r"example", ds_id, content, flags=re.IGNORECASE)
            target.write_text(content, encoding="utf-8")
            generated.append(str(target))

        if generated:
            printer.success("Generated missing files:")
            for fp in generated:
                printer.file_path(fp)
            printer.print("Please review and customise the generated templates before publishing.", "warning")
        else:
            printer.warning("No files were auto-generated (either not template found or only non-doc files were missing)")

    # Locate dataset directory (docs) – fall back across common locations
    candidate_dirs = [
        config_manager.paths.project_root / "dataset" / dataset_id,
        config_manager.paths.docs_dir / dataset_id,
        config_manager.paths.datasets_dir / dataset_id,
    ]
    dataset_dir = next((p for p in candidate_dirs if p.exists()), None)

    if dataset_dir is None:
        printer.error(f"Dataset directory not found for '{dataset_id}' in expected locations.")
        sys.exit(1)

    missing: list[str] = []  # Store absolute paths of missing files

    if check_hf:
        printer.print("Checking Hugging Face requirements", "info")
        hf_required = ["README.md", "dataset-card.md", "CITATION.cff", "LICENSE", "CHANGELOG.md"]
        for rel in hf_required:
            path = dataset_dir / rel
            if not path.exists():
                missing.append(str(path))

        # Processed data required for HF
        data_parquet = config_manager.paths.processed_data_dir / dataset_id / "data.parquet"
        if not data_parquet.exists():
            missing.append(str(data_parquet))

    if check_kg:
        printer.print("Checking Kaggle requirements", "info")
        kg_required = [Path(".kaggle") / "README.md", "dataset-card.md", "LICENSE", "CHANGELOG.md"]
        for rel in kg_required:
            path = dataset_dir / rel
            if not path.exists():
                missing.append(str(path))

    if missing:
        # Display table of missing files
        printer.table(["#", "Missing file"], [[str(i+1), p] for i, p in enumerate(missing)], title="Files to create")
        printer.guide("Next steps", [
            "Use --fix to auto-generate placeholder documents",
            "Or create the files manually as listed above",
            "Re-run the doctor command afterwards"
        ])

        if args.fix:
            _auto_generate_missing_files(dataset_id, dataset_dir, missing)
        else:
            sys.exit(1)

    printer.success("All required files exist. Dataset is ready for publishing!")


def _create_doctor_commands(subparsers) -> None:
    """Create the `doctor` command parser."""
    doctor_parser = subparsers.add_parser("doctor", help="Validate dataset files for publishing")
    doctor_parser.add_argument("id", help="Dataset ID to validate")

    platform_group = doctor_parser.add_mutually_exclusive_group(required=False)
    platform_group.add_argument("--hf", action="store_true", help="Check Hugging Face requirements only")
    platform_group.add_argument("--kg", action="store_true", help="Check Kaggle requirements only")

    doctor_parser.add_argument("--fix", action="store_true", help="Attempt to create any missing files using templates")

    doctor_parser.set_defaults(func=doctor_dataset)


def setup_env(args: argparse.Namespace) -> None:
    """
    Set up the environment configuration.
    
    Args:
        args: Command line arguments, may contain env_file path
    """
    try:
        printer.header("Setting up environment configuration")

        # Create .env file if it doesn't exist
        env_path = args.env_file or config_manager.paths.project_root / ".env"
        env_path = Path(env_path)

        if env_path.exists() and not args.force:
            printer.warning(f"Environment file already exists at {env_path}")
            printer.warning("Use --force to overwrite")
            return

        # Create template .env file
        env_content = """# MedData Environment Configuration

# Hugging Face API token
# Get your token from https://huggingface.co/settings/tokens
HF_TOKEN=

# Kaggle API token
# Get your token from https://www.kaggle.com/settings
KAGGLE_USERNAME=
KAGGLE_TOKEN=

# GitHub API token
# Get your token from https://github.com/settings/tokens
GITHUB_TOKEN=

# Other configuration settings
"""

        # Write the file
        with open(env_path, 'w') as f:
            f.write(env_content)

        # Set permissions to avoid exposing tokens
        env_path.chmod(0o600)

        printer.success(f"Created environment configuration file at {env_path}")
        printer.guide("Next Steps", [
            "Edit the .env file and add your API tokens",
            "Restart your application to apply the changes"
        ])

    except Exception as e:
        printer.error("Failed to set up environment configuration", e)
        sys.exit(1)


def _create_init_commands(subparsers) -> None:
    """
    Create the init command parser.
    
    Args:
        subparsers: Subparser collection to add the command to
    """
    init_parser = subparsers.add_parser("init", help="Initialize a new dataset")
    init_parser.add_argument("id", help="Dataset ID (e.g., 'kaggle')")
    init_parser.add_argument("name", help="Dataset name (e.g., 'Kaggle Articles')")
    init_parser.add_argument("description", help="Short dataset description")
    init_parser.set_defaults(func=init_dataset)


def _create_process_commands(subparsers) -> None:
    """
    Create the process command parser.
    
    Args:
        subparsers: Subparser collection to add the command to
    """
    process_parser = subparsers.add_parser("process", help="Process a dataset")
    process_parser.add_argument("id", help="Dataset ID to process")
    process_parser.set_defaults(func=process_dataset)


def _create_publish_commands(subparsers) -> None:
    """
    Create the publish command parser.
    
    Args:
        subparsers: Subparser collection to add the command to
    """
    publish_parser = subparsers.add_parser("publish", help="Publish a dataset")
    publish_parser.add_argument("id", help="Dataset ID to publish")
    publish_parser.add_argument("--token", help="API token for publishing (if not provided, will use token from .env)")
    publish_parser.add_argument("--platforms", nargs="+",
                                help="Specific platforms to publish to (e.g., huggingface github)")
    publish_parser.set_defaults(func=publish_dataset)


def _create_assets_commands(subparsers) -> None:
    """
    Create the assets command parser.
    
    Args:
        subparsers: Subparser collection to add the command to
    """
    assets_parser = subparsers.add_parser("assets", help="Generate assets for datasets")
    assets_parser.add_argument("dataset_id", nargs="?",
                               help="Optional dataset ID. If not provided, generates assets for all datasets.")
    assets_parser.set_defaults(func=generate_assets)


def _create_docs_commands(subparsers) -> None:
    """
    Create the docs command parser.
    
    Args:
        subparsers: Subparser collection to add the command to
    """
    docs_parser = subparsers.add_parser("docs", help="Generate documentation for a dataset")
    docs_parser.add_argument("id", help="Dataset ID to generate documentation for")
    docs_parser.set_defaults(func=generate_docs)


def _create_site_commands(subparsers) -> None:
    """
    Create the site command parser.
    
    Args:
        subparsers: Subparser collection to add the command to
    """
    site_parser = subparsers.add_parser("site", help="Generate the static site")
    site_parser.add_argument("--serve", action="store_true", help="Serve the site locally")
    site_parser.set_defaults(func=generate_site)


def _create_setup_commands(subparsers) -> None:
    """
    Create the setup command parser.
    
    Args:
        subparsers: Subparser collection to add the command to
    """
    setup_parser = subparsers.add_parser("setup", help="Set up the environment configuration")
    setup_parser.add_argument("--env-file", help="Path to the environment file (default: .env in project root)")
    setup_parser.add_argument("--force", action="store_true", help="Force overwrite if the file already exists")
    setup_parser.set_defaults(func=setup_env)


def create_commands(subparsers) -> None:
    """
    Create all command parsers.
    
    Args:
        subparsers: Subparser collection to add commands to
    """
    # init command
    _create_init_commands(subparsers)

    # process command
    _create_process_commands(subparsers)

    # publish command
    _create_publish_commands(subparsers)

    # assets command
    _create_assets_commands(subparsers)

    # docs command
    _create_docs_commands(subparsers)

    # site command
    _create_site_commands(subparsers)

    # doctor command
    _create_doctor_commands(subparsers)

    # setup command
    _create_setup_commands(subparsers)


def create_parser() -> argparse.ArgumentParser:
    """
    Create the argument parser for the CLI.
    
    Returns:
        Configured argument parser for the MedData CLI
    """
    parser = argparse.ArgumentParser(description="MedData CLI Tool")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    create_commands(subparsers)

    return parser


def validate_environment() -> bool:
    """
    Validate that the script is running in the correct environment.
    
    Returns:
        True if the environment is valid, False otherwise
    """
    # Check if required directories exist
    missing_dirs = []

    if not config_manager.paths.project_root.exists():
        missing_dirs.append(str(config_manager.paths.project_root))

    if not (config_manager.paths.project_root / "scripts").exists():
        missing_dirs.append(str(config_manager.paths.project_root / "scripts"))

    if not config_manager.paths.datasets_dir.exists():
        missing_dirs.append(str(config_manager.paths.datasets_dir))

    if missing_dirs:
        printer.smart_error("missing_file", {
            "path": ", ".join(missing_dirs),
            "message": f"Required directories not found: {', '.join(missing_dirs)}"
        })
        printer.warning("Make sure you're running this command from the project root directory.")
        return False

    return True


def main() -> int:
    """
    Main entry point for the CLI.
    
    Returns:
        Exit code (0 for success, non-zero for error)
    """
    parser = create_parser()
    args = parser.parse_args()

    # Show logo on startup
    printer.logo()

    if args.command is None:
        parser.print_help()
        return 1

    # Validate environment (except for setup command which can run anywhere)
    if args.command != "setup" and not validate_environment():
        return 1

    # Execute the corresponding function
    args.func(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
