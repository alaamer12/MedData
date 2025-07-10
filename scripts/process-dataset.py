#!/usr/bin/env python3
import os
import sys
import yaml
import pandas as pd
import importlib.util

# Try to import the printer, if not available fallback to simple printing
try:
    # Check if utils.printer is available
    if importlib.util.find_spec("utils.printer"):
        from utils.printer import printer
    else:
        # Try to import from parent directory
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from utils.printer import printer
except ImportError:
    # Define a simple printer fallback with basic methods if module not found
    class SimplePrinter:
        def header(self, msg): print(f"\n=== {msg} ===")
        def print(self, msg, *args): print(msg)
        def success(self, msg): print(f"[SUCCESS] {msg}")
        def warning(self, msg): print(f"[WARNING] {msg}")
        def error(self, msg, e=None): 
            print(f"[ERROR] {msg}")
            if e: print(f"  Details: {str(e)}")
        def guide(self, title, steps):
            print(f"\n{title}:")
            for i, step in enumerate(steps):
                print(f"{i+1}. {step}")
        def dataset_processed(self, dataset_id, stats):
            print(f"\n[SUCCESS] Dataset '{dataset_id}' processed successfully!")
            print("\nDataset Stats:")
            for key, value in stats.items():
                print(f"  {key}: {value}")
        def smart_error(self, error_type, context=None):
            print(f"[ERROR] {error_type}")
            if context and 'message' in context:
                print(f"  {context['message']}")
    
    printer = SimplePrinter()

def load_dataset_config(dataset_id):
    """Load dataset configuration from YAML file."""
    config_path = f"_datasets/{dataset_id}.yml"
    if not os.path.exists(config_path):
        printer.smart_error("dataset_config", {
            "dataset_id": dataset_id,
            "config_path": config_path,
            "message": f"Dataset configuration not found: {config_path}"
        })
        sys.exit(1)
        
    try:
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)
    except yaml.YAMLError as e:
        printer.smart_error("dataset_config", {
            "dataset_id": dataset_id,
            "config_path": config_path,
            "message": f"Invalid YAML in configuration file: {config_path}"
        })
        printer.error("YAML parsing error", e)
        sys.exit(1)
    except Exception as e:
        printer.error(f"Error loading dataset configuration: {config_path}", e)
        sys.exit(1)

def process_kaggle_source(source_config, dataset_id):
    """Process a Kaggle data source."""
    try:
        import kaggle
        import kagglehub
    except ImportError:
        printer.smart_error("missing_dependency", {
            "dependency": "kaggle kagglehub",
            "message": "Kaggle libraries not installed. Run: pip install kaggle kagglehub"
        })
        sys.exit(1)
    
    if not source_config.get('dataset'):
        printer.smart_error("dataset_config", {
            "dataset_id": dataset_id,
            "message": "Kaggle dataset not specified in configuration"
        })
        sys.exit(1)
        
    printer.header(f"Downloading dataset: {source_config['dataset']}")
    
    try:
        # Try using kagglehub first
        dataset_path = kagglehub.dataset_download(source_config['dataset'])
        printer.success(f"Downloaded to: {dataset_path}")
    except Exception as e:
        # Fall back to kaggle API
        printer.warning(f"KaggleHub download failed: {str(e)}")
        printer.print("Falling back to Kaggle API...")
        
        # Parse username and dataset slug
        username, dataset_slug = source_config['dataset'].split('/')
        
        # Set download path
        download_path = f"_data/raw/{dataset_id}/kaggle"
        os.makedirs(download_path, exist_ok=True)
        
        try:
            # Download dataset
            kaggle.api.authenticate()
            kaggle.api.dataset_download_files(
                source_config['dataset'],
                path=download_path,
                unzip=True
            )
            dataset_path = download_path
            printer.success(f"Downloaded to: {dataset_path}")
        except Exception as nested_e:
            printer.smart_error("network", {
                "service": "Kaggle API",
                "message": f"Failed to download dataset: {str(nested_e)}"
            })
            sys.exit(1)
    
    # Load data file
    file_path = os.path.join(dataset_path, source_config['file'])
    if not os.path.exists(file_path):
        available_files = []
        for root, dirs, files in os.walk(dataset_path):
            for file in files:
                available_files.append(os.path.join(root, file))
                
        printer.smart_error("missing_file", {
            "path": file_path,
            "message": f"Data file not found: {file_path}"
        })
        printer.print("Available files:")
        for file in available_files[:10]:  # Show at most 10 files
            printer.print(f"  - {file}")
        if len(available_files) > 10:
            printer.print(f"  ... and {len(available_files) - 10} more")
        sys.exit(1)
    
    # Determine file format and load
    if file_path.endswith('.csv'):
        try:
            df = pd.read_csv(file_path, on_bad_lines='skip')
            printer.success(f"Loaded CSV file: {file_path} ({len(df)} rows)")
            return df
        except Exception as e:
            printer.error(f"Failed to load CSV file: {file_path}", e)
            sys.exit(1)
    elif file_path.endswith('.parquet'):
        try:
            df = pd.read_parquet(file_path)
            printer.success(f"Loaded Parquet file: {file_path} ({len(df)} rows)")
            return df
        except Exception as e:
            printer.error(f"Failed to load Parquet file: {file_path}", e)
            sys.exit(1)
    else:
        printer.smart_error("dataset_processing", {
            "dataset_id": dataset_id,
            "message": f"Unsupported file format: {file_path}"
        })
        sys.exit(1)

def process_huggingface_source(source_config, dataset_id):
    """Process a Hugging Face data source."""
    try:
        from datasets import load_dataset
    except ImportError:
        printer.smart_error("missing_dependency", {
            "dependency": "datasets",
            "message": "Hugging Face datasets library not installed. Run: pip install datasets"
        })
        sys.exit(1)
    
    if not source_config.get('dataset'):
        printer.smart_error("dataset_config", {
            "dataset_id": dataset_id,
            "message": "Hugging Face dataset not specified in configuration"
        })
        sys.exit(1)
        
    printer.header(f"Loading dataset: {source_config['dataset']}")
    
    try:
        dataset = load_dataset(source_config['dataset'])
        df = dataset["train"].to_pandas()
        printer.success(f"Loaded Hugging Face dataset: {source_config['dataset']} ({len(df)} rows)")
        return df
    except Exception as e:
        printer.smart_error("network", {
            "service": "Hugging Face Hub",
            "message": f"Error loading Hugging Face dataset: {str(e)}"
        })
        sys.exit(1)

def normalize_dataframe(df):
    """Apply common normalization to a dataframe."""
    printer.header("Normalizing dataframe")
    
    original_shape = df.shape
    printer.print(f"Shape before: {original_shape}")
    printer.print(f"Columns: {df.columns.tolist()}")
    
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
            printer.print(f"Dropping {null_count} rows with null {text_col}")
            df = df[df[text_col].notna()]
        
        # Drop duplicate rows based on the text column
        duplicate_count = df.duplicated(subset=[text_col]).sum()
        if duplicate_count > 0:
            printer.print(f"Dropping {duplicate_count} duplicate rows based on {text_col}")
            df.drop_duplicates(subset=[text_col], keep='first', inplace=True)
    else:
        printer.warning("No text column found for normalization")
    
    new_shape = df.shape
    printer.print(f"Shape after: {new_shape}")
    
    # Calculate changes
    rows_removed = original_shape[0] - new_shape[0]
    percent_change = (rows_removed / original_shape[0]) * 100 if original_shape[0] > 0 else 0
    
    if rows_removed > 0:
        printer.print(f"Removed {rows_removed} rows ({percent_change:.2f}%)")
    
    return df

def process_dataset(dataset_id):
    """Process a dataset according to its configuration."""
    # Load dataset configuration
    config = load_dataset_config(dataset_id)
    printer.header(f"Processing dataset: {config['name']}")
    
    # Check for sources
    if not config.get('sources'):
        printer.smart_error("dataset_config", {
            "dataset_id": dataset_id,
            "message": "No data sources specified in configuration"
        })
        sys.exit(1)
    
    # Process each source
    combined_df = pd.DataFrame()
    
    for source in config['sources']:
        platform = source.get('platform')
        printer.header(f"Processing source: {platform}")
        
        try:
            if platform == 'kaggle':
                df = process_kaggle_source(source, dataset_id)
            elif platform == 'huggingface':
                df = process_huggingface_source(source, dataset_id)
            else:
                printer.warning(f"Unknown platform: {platform}")
                continue
            
            # Normalize dataframe
            printer.header(f"Normalizing data from {platform}")
            df = normalize_dataframe(df)
            
            # Combine dataframes
            if combined_df.empty:
                combined_df = df
            else:
                printer.header("Combining dataframes")
                combined_df = pd.concat([combined_df, df], ignore_index=True)
                printer.print(f"Combined shape: {combined_df.shape}")
        except Exception as e:
            printer.error(f"Error processing source {platform}", e)
            if platform == 'kaggle':
                printer.guide("Kaggle Authentication", [
                    "Make sure your Kaggle API credentials are set up correctly",
                    "Create a kaggle.json file with your API credentials",
                    "Place it in ~/.kaggle/ directory or set KAGGLE_CONFIG_DIR environment variable"
                ])
            continue
    
    if combined_df.empty:
        printer.error("No data was processed. Check your source configurations.")
        sys.exit(1)
    
    # Save processed dataset
    output_dir = f"_data/processed/{dataset_id}"
    try:
        os.makedirs(output_dir, exist_ok=True)
        
        # Save as parquet
        parquet_path = f"{output_dir}/data.parquet"
        combined_df.to_parquet(parquet_path, index=False)
        
        # Save a sample as CSV for inspection
        sample_size = min(1000, len(combined_df))
        sample_path = f"{output_dir}/sample.csv"
        combined_df.sample(sample_size).to_csv(sample_path, index=False)
        
        # Prepare stats
        stats = {
            "Total rows": len(combined_df),
            "Columns": len(combined_df.columns),
            "File size": f"{os.path.getsize(parquet_path) / (1024 * 1024):.2f} MB",
            "Column names": ", ".join(combined_df.columns.tolist()[:5]) + 
                          (", ..." if len(combined_df.columns) > 5 else ""),
            "Sample path": sample_path,
            "Parquet path": parquet_path
        }
        
        # Print success message with stats
        printer.dataset_processed(dataset_id, stats)
        
        # Update stats in configuration file suggestion
        printer.guide("Next Steps", [
            f"Run 'python meddata.py generate-docs {dataset_id}' to generate documentation",
            f"Consider updating the dataset statistics in _datasets/{dataset_id}.yml:",
            f"  - value: {len(combined_df)}+",
            f"    label: Items",
            f"  - value: {len(combined_df.columns)}",
            f"    label: Fields"
        ])
        
    except PermissionError as e:
        printer.error("Permission denied when saving processed dataset", e)
        sys.exit(1)
    except Exception as e:
        printer.error("Error saving processed dataset", e)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        printer.error("Usage: python process-dataset.py <dataset_id>")
        printer.guide("Example", ["python process-dataset.py medium"])
        sys.exit(1)
    
    process_dataset(sys.argv[1]) 