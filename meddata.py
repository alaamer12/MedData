#!/usr/bin/env python3
import argparse
import os
import sys
import subprocess
from utils.printer import printer

def init_dataset(args):
    """Initialize a new dataset."""
    try:
        printer.header(f"Initializing dataset: {args.id}")
        cmd = ["python", "scripts/create-dataset.py", args.id, args.name, args.description]
        result = subprocess.run(cmd, check=True)
        if result.returncode == 0:
            printer.success(f"Dataset '{args.id}' initialized successfully!")
    except subprocess.CalledProcessError as e:
        printer.error(f"Failed to initialize dataset '{args.id}'", e)
        sys.exit(1)

def process_dataset(args):
    """Process a dataset."""
    try:
        printer.header(f"Processing dataset: {args.id}")
        cmd = ["python", "scripts/process-dataset.py", args.id]
        result = subprocess.run(cmd, check=True)
        if result.returncode == 0:
            printer.success(f"Dataset '{args.id}' processed successfully!")
    except subprocess.CalledProcessError as e:
        printer.error(f"Failed to process dataset '{args.id}'", e)
        sys.exit(1)

def publish_dataset(args):
    """Publish a dataset."""
    try:
        printer.header(f"Publishing dataset: {args.id}")
        cmd = ["python", "scripts/publish-dataset.py", args.id, "--token", args.token]
        if args.platforms:
            cmd.extend(["--platforms"] + args.platforms)
        result = subprocess.run(cmd, check=True)
        if result.returncode == 0:
            printer.success(f"Dataset '{args.id}' published successfully!")
    except subprocess.CalledProcessError as e:
        printer.error(f"Failed to publish dataset '{args.id}'", e)
        sys.exit(1)

def generate_assets(args):
    """Generate assets for datasets."""
    try:
        if args.dataset_id:
            printer.header(f"Generating assets for dataset: {args.dataset_id}")
        else:
            printer.header("Generating assets for all datasets")
        cmd = ["python", "scripts/generate-assets.py"]
        if args.dataset_id:
            cmd.append(args.dataset_id)
        result = subprocess.run(cmd, check=True)
        if result.returncode == 0:
            printer.success("Assets generated successfully!")
    except subprocess.CalledProcessError as e:
        printer.error("Failed to generate assets", e)
        sys.exit(1)

def generate_docs(args):
    """Generate documentation for a dataset."""
    try:
        printer.header(f"Generating documentation for dataset: {args.id}")
        cmd = ["python", "scripts/generate-docs.py", args.id]
        result = subprocess.run(cmd, check=True)
        if result.returncode == 0:
            printer.success(f"Documentation for dataset '{args.id}' generated successfully!")
    except subprocess.CalledProcessError as e:
        printer.error(f"Failed to generate documentation for dataset '{args.id}'", e)
        sys.exit(1)

def generate_site(args):
    """Generate the static site."""
    try:
        if args.serve:
            printer.header("Generating and serving the static site")
            cmd = ["bundle", "exec", "jekyll", "serve"]
        else:
            printer.header("Generating the static site")
            cmd = ["bundle", "exec", "jekyll", "build"]
        result = subprocess.run(cmd, check=True)
        if result.returncode == 0:
            if args.serve:
                printer.success("Site is being served at http://localhost:4000")
            else:
                printer.success("Site generated successfully!")
    except subprocess.CalledProcessError as e:
        printer.error("Failed to generate site", e)
        sys.exit(1)

def _create_init_commands(subparsers: argparse.ArgumentParser):
    """Create the argument parser for the CLI."""
    
    init_parser = subparsers.add_parser("init", help="Initialize a new dataset")
    init_parser.add_argument("id", help="Dataset ID (e.g., 'kaggle')")
    init_parser.add_argument("name", help="Dataset name (e.g., 'Kaggle Articles')")
    init_parser.add_argument("description", help="Short dataset description")
    init_parser.set_defaults(func=init_dataset)

def _create_process_commands(subparsers: argparse.ArgumentParser):
    """Create the argument parser for the CLI."""
    
    process_parser = subparsers.add_parser("process", help="Process a dataset")
    process_parser.add_argument("id", help="Dataset ID to process")
    process_parser.set_defaults(func=process_dataset)

def _create_publish_commands(subparsers: argparse.ArgumentParser):
    """Create the argument parser for the CLI."""
    
    publish_parser = subparsers.add_parser("publish", help="Publish a dataset")
    publish_parser.add_argument("id", help="Dataset ID to publish")
    publish_parser.add_argument("--token", required=True, help="API token for publishing")
    publish_parser.add_argument("--platforms", nargs="+", help="Specific platforms to publish to (e.g., huggingface github)")
    publish_parser.set_defaults(func=publish_dataset)

def _create_assets_commands(subparsers: argparse.ArgumentParser):
    """Create the argument parser for the CLI."""
    
    assets_parser = subparsers.add_parser("assets", help="Generate assets for datasets")
    assets_parser.add_argument("dataset_id", nargs="?", help="Optional dataset ID. If not provided, generates assets for all datasets.")
    assets_parser.set_defaults(func=generate_assets)

def _create_docs_commands(subparsers: argparse.ArgumentParser):
    """Create the argument parser for the CLI."""
    
    docs_parser = subparsers.add_parser("docs", help="Generate documentation for a dataset")
    docs_parser.add_argument("id", help="Dataset ID to generate documentation for")
    docs_parser.set_defaults(func=generate_docs)

def _create_site_commands(subparsers: argparse.ArgumentParser):
    """Create the argument parser for the CLI."""
    
    site_parser = subparsers.add_parser("site", help="Generate the static site")
    site_parser.add_argument("--serve", action="store_true", help="Serve the site locally")
    site_parser.set_defaults(func=generate_site)


def create_commands(subparsers: argparse.ArgumentParser):
    """Create the argument parser for the CLI."""
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

def create_parser():
    """Create the argument parser for the CLI."""
    parser = argparse.ArgumentParser(description="MedData CLI Tool")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    create_commands(subparsers)
    
    return parser

def main():
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Show logo on startup
    printer.logo()
    
    if args.command is None:
        parser.print_help()
        sys.exit(1)
    
    # Check if required directories exist
    required_dirs = ["scripts", "_datasets"]
    missing_dirs = []
    for directory in required_dirs:
        if not os.path.exists(directory):
            missing_dirs.append(directory)
    
    if missing_dirs:
        printer.smart_error("missing_file", {
            "path": ", ".join(missing_dirs),
            "message": f"Required directories not found: {', '.join(missing_dirs)}"
        })
        printer.warning("Make sure you're running this command from the project root directory.")
        sys.exit(1)
    
    # Execute the corresponding function
    args.func(args)

if __name__ == "__main__":
    main() 