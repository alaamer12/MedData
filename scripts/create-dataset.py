#!/usr/bin/env python3
import os
import sys
from datetime import datetime
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
        def success(self, msg): print(f"[SUCCESS] {msg}")
        def warning(self, msg): print(f"[WARNING] {msg}")
        def error(self, msg, e=None): 
            print(f"[ERROR] {msg}")
            if e: print(f"  Details: {str(e)}")
        def guide(self, title, steps):
            print(f"\n{title}:")
            for i, step in enumerate(steps):
                print(f"{i+1}. {step}")
        def dataset_created(self, dataset_id, config_path):
            self.success(f"Dataset '{dataset_id}' created successfully!")
            print(f"Configuration file: {config_path}")
            print("\nNext steps:")
            print(f"1. Edit {config_path} to customize dataset properties")
            print(f"2. Run 'python scripts/generate-assets.py' to generate assets")
            print(f"3. Create dataset directory: mkdir -p dataset/{dataset_id}")
            print(f"4. Create dataset page: dataset/{dataset_id}/index.md")
    
    printer = SimplePrinter()

TEMPLATE_DIR = "templates"
OUTPUT_DIR = "_datasets"

def ensure_directories():
    """Ensure required directories exist."""
    try:
        os.makedirs(TEMPLATE_DIR, exist_ok=True)
        os.makedirs(OUTPUT_DIR, exist_ok=True)
    except PermissionError as e:
        printer.error(f"Permission denied when creating directories", e)
        sys.exit(1)
    except Exception as e:
        printer.error(f"Error creating directories", e)
        sys.exit(1)

def create_template_if_not_exists():
    """Create the dataset template if it doesn't exist."""
    template_path = f"{TEMPLATE_DIR}/dataset.yml.template"
    
    if not os.path.exists(template_path):
        template_content = """id: {{id}}
name: {{name}}
description: {{description}}
status: development
release_date: {{date}}
expected_update: quarterly
logo:
  text: {{id|first|upper}}
  background: circle
  colors:
    primary: "#6366f1"
    secondary: "#14b8a6"
stats:
  - value: 0+
    label: Items
  - value: 0+
    label: Fields
sources:
  - platform: kaggle
    dataset: ""
    file: ""
publishing:
  - platform: huggingface
    repository: ""
    url: ""
  - platform: github
    repository: ""
    url: ""
features:
  - icon: 🔍
    title: Feature One
    description: Description of feature one.
  - icon: 📊
    title: Feature Two
    description: Description of feature two.
  - icon: 🚀
    title: Feature Three
    description: Description of feature three."""

        try:
            os.makedirs(os.path.dirname(template_path), exist_ok=True)
            with open(template_path, 'w') as file:
                file.write(template_content)
            printer.success(f"Created template: {template_path}")
        except PermissionError as e:
            printer.error(f"Permission denied when creating template file", e)
            sys.exit(1)
        except Exception as e:
            printer.error(f"Error creating template file", e)
            sys.exit(1)

def create_dataset(dataset_id, name, description):
    """Create a new dataset configuration file."""
    # Validate dataset ID
    if not dataset_id.isalnum() and not all(c.isalnum() or c == '-' for c in dataset_id):
        printer.error(f"Invalid dataset ID: '{dataset_id}'. Use only alphanumeric characters and hyphens.")
        sys.exit(1)
    
    # Check if dataset already exists
    output_path = f"{OUTPUT_DIR}/{dataset_id}.yml"
    if os.path.exists(output_path):
        printer.error(f"Dataset '{dataset_id}' already exists at {output_path}")
        sys.exit(1)
    
    # Ensure directories and template exist
    ensure_directories()
    create_template_if_not_exists()
    
    # Load template
    template_path = f"{TEMPLATE_DIR}/dataset.yml.template"
    try:
        with open(template_path, 'r') as file:
            template = file.read()
    except FileNotFoundError:
        printer.error(f"Template file not found: {template_path}")
        sys.exit(1)
    except Exception as e:
        printer.error(f"Error reading template file", e)
        sys.exit(1)
    
    # Replace placeholders
    content = template.replace("{{id}}", dataset_id)
    content = content.replace("{{name}}", name)
    content = content.replace("{{description}}", description)
    content = content.replace("{{date}}", datetime.now().strftime("%Y-%m-%d"))
    
    # Write dataset configuration
    try:
        with open(output_path, 'w') as file:
            file.write(content)
        
        # Create dataset directory structure
        dataset_dir = f"dataset/{dataset_id}"
        os.makedirs(dataset_dir, exist_ok=True)
        
        # Create basic index file
        with open(f"{dataset_dir}/index.md", 'w') as file:
            file.write(f"""---
layout: dataset
title: {name}
description: {description}
---

# {name}

{description}
""")
        
        # Show success message with next steps
        printer.dataset_created(dataset_id, output_path)
        
    except PermissionError as e:
        printer.error(f"Permission denied when writing dataset file", e)
        sys.exit(1)
    except Exception as e:
        printer.error(f"Error creating dataset", e)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        printer.error("Usage: python create-dataset.py <id> <name> <description>")
        printer.guide("Example", ["python create-dataset.py kaggle 'Kaggle Dataset' 'A collection of Kaggle articles'"])
        sys.exit(1)
    
    create_dataset(sys.argv[1], sys.argv[2], sys.argv[3]) 