#!/usr/bin/env python3
"""
MedData Publish Dataset Script - Publishes datasets to external platforms.

This script handles the publishing of processed datasets to platforms like
Hugging Face and GitHub. It uploads both the data files and metadata files
(README, dataset card, citation, license) to make the dataset accessible.
"""
from __future__ import annotations

import argparse
import sys
from typing import Dict, Any, List, Optional

import yaml
from scripts.utils.printer import printer
from scripts.utils.config_manager import config_manager

__all__ = ["load_dataset_config", "publish_to_huggingface", "publish_to_github", "publish_dataset"]


def load_dataset_config(dataset_id: str) -> Dict[str, Any]:
    """
    Load dataset configuration from YAML file.
    
    Args:
        dataset_id: ID of the dataset to load
        
    Returns:
        Dictionary containing the dataset configuration
        
    Raises:
        FileNotFoundError: If the configuration file doesn't exist
        yaml.YAMLError: If the configuration file is not valid YAML
    """
    config_path = config_manager.paths.datasets_dir / f"{dataset_id}.yml"
    if not config_path.exists():
        printer.error(f"Dataset configuration not found: {config_path}")
        sys.exit(1)

    with open(config_path, 'r') as file:
        return yaml.safe_load(file)


def publish_to_huggingface(dataset_id: str, repository: str, token: Optional[str] = None) -> str:
    """
    Publish dataset to Hugging Face.
    
    Args:
        dataset_id: ID of the dataset to publish
        repository: Hugging Face repository name (e.g., 'username/dataset-name')
        token: Hugging Face API token (if None, will use token from config)
        
    Returns:
        URL of the published dataset
        
    Raises:
        ImportError: If required libraries are not installed
        FileNotFoundError: If processed dataset or metadata files don't exist
        Exception: For errors during the publishing process
    """
    # Use token from config if not provided
    if token is None:
        token = config_manager.tokens.huggingface
        if token is None:
            printer.error("No Hugging Face token provided and none found in environment")
            printer.guide("Set up token", [
                "Provide token with --token parameter",
                "Or set HF_TOKEN or HUGGINGFACE_TOKEN in your .env file"
            ])
            sys.exit(1)

    # Check if processed dataset exists
    data_path = config_manager.paths.processed_data_dir / dataset_id / "data.parquet"
    if not data_path.exists():
        printer.error(f"Processed dataset not found: {data_path}")
        printer.guide("Process dataset first", [f"Run 'python meddata.py process {dataset_id}' first"])
        sys.exit(1)

    try:
        from huggingface_hub import HfApi, login
        from datasets import load_dataset
    except ImportError:
        printer.smart_error("missing_dependency", {
            "dependency": "huggingface_hub datasets",
            "message": "Hugging Face libraries not installed. Run: pip install huggingface_hub datasets"
        })
        sys.exit(1)

    # Authenticate with Hugging Face
    printer.header(f"Authenticating with Hugging Face")
    login(token=token)

    # Load and push dataset
    printer.header(f"Loading dataset from {data_path}")
    dataset = load_dataset("parquet", data_files=str(data_path))

    printer.header(f"Pushing dataset to Hugging Face: {repository}")
    dataset.push_to_hub(repository)

    # Upload metadata files
    api = HfApi()

    metadata_files = {
        config_manager.paths.docs_dir / dataset_id / "README.md": "README.md",
        config_manager.paths.docs_dir / dataset_id / "dataset-card.md": "dataset-card.md",
        config_manager.paths.docs_dir / dataset_id / "CITATION.cff": "CITATION.cff",
        config_manager.paths.docs_dir / dataset_id / "LICENSE": "LICENSE",
    }

    for local_path, hub_path in metadata_files.items():
        if local_path.exists():
            printer.header(f"Uploading {local_path} -> {hub_path}")
            api.upload_file(
                path_or_fileobj=str(local_path),
                path_in_repo=hub_path,
                repo_id=repository,
                repo_type="dataset"
            )

    dataset_url = f"https://huggingface.co/datasets/{repository}"
    printer.success(f"Published dataset to Hugging Face: {repository}")
    printer.success(f"View at: {dataset_url}")

    return dataset_url


def publish_to_github(dataset_id: str, repository: str, token: Optional[str] = None) -> str:
    """
    Publish dataset to GitHub.
    
    Args:
        dataset_id: ID of the dataset to publish
        repository: GitHub repository name (e.g., 'username/repo-name')
        token: GitHub API token (if None, will use token from config)
        
    Returns:
        URL of the published repository
        
    Note:
        This function is a placeholder and not yet implemented
    """
    # Use token from config if not provided
    if token is None:
        token = config_manager.tokens.github
        if token is None:
            printer.error("No GitHub token provided and none found in environment")
            printer.guide("Set up token", [
                "Provide token with --token parameter",
                "Or set GITHUB_TOKEN in your .env file"
            ])
            sys.exit(1)

    printer.header(f"Publishing to GitHub: {repository}")
    printer.warning("GitHub publishing not yet implemented. Coming soon!")
    # TODO: Implement GitHub publishing

    return f"https://github.com/{repository}"


def publish_dataset(dataset_id: str, token: Optional[str] = None, platforms: Optional[List[str]] = None) -> None:
    """
    Publish dataset to specified platforms.
    
    Args:
        dataset_id: ID of the dataset to publish
        token: API token for authentication (if None, will use token from config)
        platforms: Optional list of platforms to publish to. If None, publish to all configured platforms.
    """
    # Load dataset configuration
    config = load_dataset_config(dataset_id)
    printer.header(f"Publishing dataset: {config['name']}")

    # Check for publishing targets
    if not config.get('publishing'):
        printer.error("No publishing targets specified in configuration.")
        sys.exit(1)

    # Publish to each platform
    published = False
    published_platforms = []
    published_urls = []

    for pub in config.get('publishing', []):
        platform = pub.get('platform')
        repository = pub.get('repository')

        if not repository:
            printer.warning(f"No repository specified for {platform}, skipping")
            continue

        if platforms and platform not in platforms:
            printer.print(f"Skipping {platform} (not in specified platforms)")
            continue

        # Get platform-specific token if available
        platform_token = token or config_manager.get_token_for_platform(platform)

        printer.header(f"\nPublishing to {platform}: {repository}")

        try:
            if platform == 'huggingface':
                url = publish_to_huggingface(dataset_id, repository, platform_token)
                published = True
                published_platforms.append(platform)
                published_urls.append(url)
            elif platform == 'github':
                url = publish_to_github(dataset_id, repository, platform_token)
                published = True
                published_platforms.append(platform)
                published_urls.append(url)
            else:
                printer.warning(f"Publishing to {platform} not implemented yet")
        except Exception as e:
            printer.error(f"Error publishing to {platform}", e)

    if not published:
        printer.warning("No platforms were published to. Check configuration and specified platforms.")
    else:
        printer.dataset_published(dataset_id, published_platforms, published_urls)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Publish dataset to platforms")
    parser.add_argument("dataset_id", help="Dataset ID (e.g., 'medium')")
    parser.add_argument("--token", help="API token for publishing (if not provided, will use token from .env)")
    parser.add_argument("--platforms", nargs="+", help="Specific platforms to publish to (e.g., huggingface github)")

    args = parser.parse_args()
    publish_dataset(args.dataset_id, args.token, args.platforms)
