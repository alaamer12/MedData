#!/usr/bin/env python3
import os
import sys
import yaml
import pandas as pd

def load_dataset_config(dataset_id):
    """Load dataset configuration from YAML file."""
    config_path = f"_datasets/{dataset_id}.yml"
    if not os.path.exists(config_path):
        print(f"Error: Dataset configuration not found: {config_path}")
        sys.exit(1)
        
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def process_kaggle_source(source_config, dataset_id):
    """Process a Kaggle data source."""
    try:
        import kaggle
        import kagglehub
    except ImportError:
        print("Error: Kaggle libraries not installed. Run: pip install kaggle kagglehub")
        sys.exit(1)
    
    if not source_config.get('dataset'):
        print("Error: Kaggle dataset not specified in configuration.")
        sys.exit(1)
        
    print(f"Downloading dataset: {source_config['dataset']}")
    
    try:
        # Try using kagglehub first
        dataset_path = kagglehub.dataset_download(source_config['dataset'])
        print(f"Downloaded to: {dataset_path}")
    except Exception as e:
        # Fall back to kaggle API
        print(f"KaggleHub download failed: {str(e)}")
        print("Falling back to Kaggle API...")
        
        # Parse username and dataset slug
        username, dataset_slug = source_config['dataset'].split('/')
        
        # Set download path
        download_path = f"_data/raw/{dataset_id}/kaggle"
        os.makedirs(download_path, exist_ok=True)
        
        # Download dataset
        kaggle.api.authenticate()
        kaggle.api.dataset_download_files(
            source_config['dataset'],
            path=download_path,
            unzip=True
        )
        dataset_path = download_path
        print(f"Downloaded to: {dataset_path}")
    
    # Load data file
    file_path = os.path.join(dataset_path, source_config['file'])
    if not os.path.exists(file_path):
        print(f"Error: Data file not found: {file_path}")
        print(f"Available files:")
        for root, dirs, files in os.walk(dataset_path):
            for file in files:
                print(f"  - {os.path.join(root, file)}")
        sys.exit(1)
    
    # Determine file format and load
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path, on_bad_lines='skip')
    elif file_path.endswith('.parquet'):
        df = pd.read_parquet(file_path)
    else:
        print(f"Error: Unsupported file format: {file_path}")
        sys.exit(1)
    
    return df

def process_huggingface_source(source_config):
    """Process a Hugging Face data source."""
    try:
        from datasets import load_dataset
    except ImportError:
        print("Error: Hugging Face datasets library not installed. Run: pip install datasets")
        sys.exit(1)
    
    if not source_config.get('dataset'):
        print("Error: Hugging Face dataset not specified in configuration.")
        sys.exit(1)
        
    print(f"Loading dataset: {source_config['dataset']}")
    
    try:
        dataset = load_dataset(source_config['dataset'])
        df = dataset["train"].to_pandas()
        return df
    except Exception as e:
        print(f"Error loading Hugging Face dataset: {str(e)}")
        sys.exit(1)

def normalize_dataframe(df):
    """Apply common normalization to a dataframe."""
    print("\nDataframe Information:")
    print(f"Shape before: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    
    # Handle common text column names
    text_col = None
    for potential_col in ['text', 'Text', 'content', 'Content', 'body', 'Body']:
        if potential_col in df.columns:
            text_col = potential_col
            break
    
    if text_col:
        # Drop rows with null text values
        null_count = df[text_col].isna().sum()
        if null_count > 0:
            print(f"Dropping {null_count} rows with null {text_col}")
            df = df[df[text_col].notna()]
        
        # Drop duplicate rows based on the text column
        duplicate_count = df.duplicated(subset=[text_col]).sum()
        if duplicate_count > 0:
            print(f"Dropping {duplicate_count} duplicate rows based on {text_col}")
            df.drop_duplicates(subset=[text_col], keep='first', inplace=True)
    else:
        print("Warning: No text column found for normalization")
    
    print(f"Shape after: {df.shape}")
    return df

def process_dataset(dataset_id):
    """Process a dataset according to its configuration."""
    # Load dataset configuration
    config = load_dataset_config(dataset_id)
    print(f"Processing dataset: {config['name']}")
    
    # Check for sources
    if not config.get('sources'):
        print("Error: No data sources specified in configuration.")
        sys.exit(1)
    
    # Process each source
    combined_df = pd.DataFrame()
    
    for source in config['sources']:
        platform = source.get('platform')
        print(f"\nProcessing source: {platform}")
        
        if platform == 'kaggle':
            df = process_kaggle_source(source, dataset_id)
        elif platform == 'huggingface':
            df = process_huggingface_source(source)
        else:
            print(f"Warning: Unknown platform: {platform}")
            continue
        
        # Normalize dataframe
        print(f"\nNormalizing data from {platform}")
        df = normalize_dataframe(df)
        
        # Combine dataframes
        if combined_df.empty:
            combined_df = df
        else:
            print("\nCombining dataframes")
            combined_df = pd.concat([combined_df, df], ignore_index=True)
            print(f"Combined shape: {combined_df.shape}")
    
    # Save processed dataset
    output_dir = f"_data/processed/{dataset_id}"
    os.makedirs(output_dir, exist_ok=True)
    
    # Save as parquet
    parquet_path = f"{output_dir}/data.parquet"
    combined_df.to_parquet(parquet_path, index=False)
    print(f"\nSaved processed dataset: {parquet_path}")
    
    # Save a sample as CSV for inspection
    sample_size = min(1000, len(combined_df))
    sample_path = f"{output_dir}/sample.csv"
    combined_df.sample(sample_size).to_csv(sample_path, index=False)
    print(f"Saved sample dataset: {sample_path}")
    
    # Print dataset stats
    print(f"\nDataset Stats:")
    print(f"Total rows: {len(combined_df)}")
    print(f"Columns: {combined_df.columns.tolist()}")
    
    # Update dataset stats in config file
    print("\nNote: Consider updating the dataset statistics in the configuration file:")
    print(f"  - {len(combined_df)} items")
    print(f"  - {len(combined_df.columns)} fields")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python process-dataset.py <dataset_id>")
        print("Example: python process-dataset.py medium")
        sys.exit(1)
    
    process_dataset(sys.argv[1]) 