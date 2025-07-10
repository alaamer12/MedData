#!/usr/bin/env python3
"""
Demo script for the Printer class functionality.

This script demonstrates the various features of the Printer class
for providing rich, informative output in the MedData Engineering Hub.
"""

import os
import sys
import time

# Add parent directory to path to allow direct execution
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.printer import printer

def demonstrate_basic_output():
    """Demonstrate basic output types."""
    printer.header("Basic Output Demo")
    printer.print("This is a regular informational message")
    printer.success("This is a success message")
    printer.warning("This is a warning message")
    printer.error("This is an error message")
    printer.error("This is an error with an exception", Exception("Sample exception"))
    
    # Pause for readability
    time.sleep(1)

def demonstrate_guides():
    """Demonstrate guide output."""
    printer.header("Guide Demo")
    printer.guide("Getting Started", [
        "Install dependencies with pip install -r requirements.txt",
        "Configure your settings in config.yml",
        "Run the application with python meddata.py init example 'Example Dataset' 'A sample dataset'",
        "Process the dataset with python meddata.py process example"
    ])
    
    # Pause for readability
    time.sleep(1)

def demonstrate_dataset_operations():
    """Demonstrate dataset operation outputs."""
    printer.header("Dataset Operations Demo")
    
    # Dataset created
    printer.dataset_created("demo-dataset", "_datasets/demo-dataset.yml")
    
    # Pause for readability
    time.sleep(2)
    
    # Dataset processed
    stats = {
        "Total rows": 15000,
        "Columns": 8,
        "File size": "3.42 MB",
        "Column names": "title, author, content, date, tags",
        "Sample path": "_data/processed/demo-dataset/sample.csv",
        "Parquet path": "_data/processed/demo-dataset/data.parquet"
    }
    printer.dataset_processed("demo-dataset", stats)
    
    # Pause for readability
    time.sleep(2)
    
    # Dataset published
    platforms = ["Hugging Face", "GitHub"]
    urls = [
        "https://huggingface.co/datasets/MedData/demo-dataset",
        "https://github.com/MedData/datasets/demo-dataset"
    ]
    printer.dataset_published("demo-dataset", platforms, urls)

def demonstrate_smart_errors():
    """Demonstrate smart error messages."""
    printer.header("Smart Errors Demo")
    
    # Missing file error
    printer.smart_error("missing_file", {
        "path": "config/settings.yml",
        "message": "Configuration file is missing"
    })
    
    # Pause for readability
    time.sleep(1)
    
    # Network error
    printer.smart_error("network", {
        "service": "Kaggle API",
        "message": "Failed to connect to Kaggle API"
    })
    
    # Pause for readability
    time.sleep(1)
    
    # Missing dependency
    printer.smart_error("missing_dependency", {
        "dependency": "rich",
        "message": "The rich library is required for enhanced output"
    })
    
    # Pause for readability
    time.sleep(1)
    
    # Dataset configuration error
    printer.smart_error("dataset_config", {
        "dataset_id": "example",
        "config_path": "_datasets/example.yml",
        "message": "Invalid configuration in dataset file"
    })

def demonstrate_code_and_tables():
    """Demonstrate code blocks and tables."""
    printer.header("Code and Tables Demo")
    
    # Display code sample
    sample_code = """
def process_dataset(dataset_id):
    \"\"\"Process a dataset.\"\"\"
    config = load_config(dataset_id)
    data = extract_data(config)
    return transform_data(data)
"""
    printer.code(sample_code)
    
    # Pause for readability
    time.sleep(2)
    
    # Display table
    columns = ["Dataset", "Size", "Status"]
    rows = [
        ["medium", "500K+ articles", "Published"],
        ["devto", "200K+ articles", "Development"],
        ["twitter", "1M+ tweets", "Planned"],
        ["reddit", "300K+ posts", "Testing"]
    ]
    printer.table(columns, rows, title="Available Datasets")

def demonstrate_logo_and_progress():
    """Demonstrate logo and progress indicators."""
    # Show logo
    printer.logo()
    
    # Pause for readability
    time.sleep(2)
    
    # Show progress
    printer.header("Progress Demo")
    
    with printer.progress_context() as progress:
        task1 = progress.add_task("Downloading data...", total=100)
        for i in range(101):
            progress.update(task1, advance=1)
            time.sleep(0.02)

def main():
    """Run the full demonstration."""
    printer.header("MedData Printer Demo")
    printer.print("This demo showcases the various output features of the Printer class.")
    
    # Run each demo section
    demonstrate_logo_and_progress()
    demonstrate_basic_output()
    demonstrate_guides()
    demonstrate_dataset_operations()
    demonstrate_smart_errors()
    demonstrate_code_and_tables()
    
    # Final message
    printer.header("Demo Complete")
    printer.success("You've seen all the features of the Printer class!")
    printer.print("Use this in your MedData scripts for enhanced user experience.")

if __name__ == "__main__":
    main() 