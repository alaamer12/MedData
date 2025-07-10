#!/usr/bin/env python3
import argparse
import os
import sys
import subprocess

def init_dataset(args):
    """Initialize a new dataset."""
    cmd = ["python", "scripts/create-dataset.py", args.id, args.name, args.description]
    subprocess.run(cmd)

def process_dataset(args):
    """Process a dataset."""
    cmd = ["python", "scripts/process-dataset.py", args.id]
    subprocess.run(cmd)

def publish_dataset(args):
    """Publish a dataset."""
    cmd = ["python", "scripts/publish-dataset.py", args.id, "--token", args.token]
    if args.platforms:
        cmd.extend(["--platforms"] + args.platforms)
    subprocess.run(cmd)

def generate_assets(args):
    """Generate assets for datasets."""
    cmd = ["python", "scripts/generate-assets.py"]
    if args.dataset_id:
        cmd.append(args.dataset_id)
    subprocess.run(cmd)

def generate_docs(args):
    """Generate documentation for a dataset."""
    cmd = ["python", "scripts/generate-docs.py", args.id]
    subprocess.run(cmd)

def generate_site(args):
    """Generate the static site."""
    if args.serve:
        cmd = ["bundle", "exec", "jekyll", "serve"]
    else:
        cmd = ["bundle", "exec", "jekyll", "build"]
    subprocess.run(cmd)

def create_parser():
    """Create the argument parser for the CLI."""
    parser = argparse.ArgumentParser(description="MedData CLI Tool")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # init command
    init_parser = subparsers.add_parser("init", help="Initialize a new dataset")
    init_parser.add_argument("id", help="Dataset ID (e.g., 'kaggle')")
    init_parser.add_argument("name", help="Dataset name (e.g., 'Kaggle Articles')")
    init_parser.add_argument("description", help="Short dataset description")
    init_parser.set_defaults(func=init_dataset)
    
    # process command
    process_parser = subparsers.add_parser("process", help="Process a dataset")
    process_parser.add_argument("id", help="Dataset ID to process")
    process_parser.set_defaults(func=process_dataset)
    
    # publish command
    publish_parser = subparsers.add_parser("publish", help="Publish a dataset")
    publish_parser.add_argument("id", help="Dataset ID to publish")
    publish_parser.add_argument("--token", required=True, help="API token for publishing")
    publish_parser.add_argument("--platforms", nargs="+", help="Specific platforms to publish to (e.g., huggingface github)")
    publish_parser.set_defaults(func=publish_dataset)
    
    # assets command
    assets_parser = subparsers.add_parser("assets", help="Generate assets for datasets")
    assets_parser.add_argument("dataset_id", nargs="?", help="Optional dataset ID. If not provided, generates assets for all datasets.")
    assets_parser.set_defaults(func=generate_assets)
    
    # docs command
    docs_parser = subparsers.add_parser("docs", help="Generate documentation for a dataset")
    docs_parser.add_argument("id", help="Dataset ID to generate documentation for")
    docs_parser.set_defaults(func=generate_docs)
    
    # site command
    site_parser = subparsers.add_parser("site", help="Generate the static site")
    site_parser.add_argument("--serve", action="store_true", help="Serve the site locally")
    site_parser.set_defaults(func=generate_site)
    
    return parser

def main():
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        sys.exit(1)
    
    # Check if required directories exist
    required_dirs = ["scripts", "_datasets"]
    for directory in required_dirs:
        if not os.path.exists(directory):
            print(f"Error: Required directory '{directory}' not found.")
            print("Make sure you're running this command from the project root directory.")
            sys.exit(1)
    
    # Execute the corresponding function
    args.func(args)

if __name__ == "__main__":
    main() 