#!/usr/bin/env python3
import os
import sys
import yaml
import argparse

def load_dataset_config(dataset_id):
    """Load dataset configuration from YAML file."""
    config_path = f"_datasets/{dataset_id}.yml"
    if not os.path.exists(config_path):
        print(f"Error: Dataset configuration not found: {config_path}")
        sys.exit(1)
        
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def publish_to_huggingface(dataset_id, repository, token):
    """Publish dataset to Hugging Face."""
    # Check if processed dataset exists
    data_path = f"_data/processed/{dataset_id}/data.parquet"
    if not os.path.exists(data_path):
        print(f"Error: Processed dataset not found: {data_path}")
        print("Run 'python scripts/process-dataset.py {dataset_id}' first")
        sys.exit(1)
    
    try:
        from huggingface_hub import HfApi, login
        from datasets import load_dataset
    except ImportError:
        print("Error: Hugging Face libraries not installed. Run: pip install huggingface_hub datasets")
        sys.exit(1)
    
    # Authenticate with Hugging Face
    print(f"Authenticating with Hugging Face using provided token")
    login(token=token)
    
    # Load and push dataset
    print(f"Loading dataset from {data_path}")
    dataset = load_dataset("parquet", data_files=data_path)
    
    print(f"Pushing dataset to Hugging Face: {repository}")
    dataset.push_to_hub(repository)
    
    # Upload metadata files
    api = HfApi()
    
    metadata_files = {
        f"docs/{dataset_id}/README.md": "README.md",
        f"docs/{dataset_id}/dataset-card.md": "dataset-card.md",
        f"docs/{dataset_id}/CITATION.cff": "CITATION.cff",
        f"docs/{dataset_id}/LICENSE": "LICENSE",
    }
    
    for local_path, hub_path in metadata_files.items():
        if os.path.exists(local_path):
            print(f"Uploading {local_path} -> {hub_path}")
            api.upload_file(
                path_or_fileobj=local_path,
                path_in_repo=hub_path,
                repo_id=repository,
                repo_type="dataset"
            )
    
    print(f"Published dataset to Hugging Face: {repository}")
    print(f"View at: https://huggingface.co/datasets/{repository}")

def publish_to_github(dataset_id, repository, token):
    """Publish dataset to GitHub."""
    print(f"Publishing to GitHub: {repository}")
    print("GitHub publishing not implemented yet. Coming soon!")
    # TODO: Implement GitHub publishing

def publish_dataset(dataset_id, token, platforms=None):
    """Publish dataset to specified platforms."""
    # Load dataset configuration
    config = load_dataset_config(dataset_id)
    print(f"Publishing dataset: {config['name']}")
    
    # Check for publishing targets
    if not config.get('publishing'):
        print("Error: No publishing targets specified in configuration.")
        sys.exit(1)
    
    # Publish to each platform
    published = False
    for pub in config.get('publishing', []):
        platform = pub.get('platform')
        repository = pub.get('repository')
        
        if not repository:
            print(f"Warning: No repository specified for {platform}, skipping")
            continue
            
        if platforms and platform not in platforms:
            print(f"Skipping {platform} (not in specified platforms)")
            continue
        
        print(f"\nPublishing to {platform}: {repository}")
        
        if platform == 'huggingface':
            publish_to_huggingface(dataset_id, repository, token)
            published = True
        elif platform == 'github':
            publish_to_github(dataset_id, repository, token)
            published = True
        else:
            print(f"Warning: Publishing to {platform} not implemented yet")
    
    if not published:
        print("No platforms were published to. Check configuration and specified platforms.")
    else:
        print("\nPublishing complete!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Publish dataset to platforms")
    parser.add_argument("dataset_id", help="Dataset ID (e.g., 'medium')")
    parser.add_argument("--token", required=True, help="API token for publishing")
    parser.add_argument("--platforms", nargs="+", help="Specific platforms to publish to (e.g., huggingface github)")
    
    args = parser.parse_args()
    publish_dataset(args.dataset_id, args.token, args.platforms) 