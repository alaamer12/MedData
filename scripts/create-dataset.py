#!/usr/bin/env python3
import os
import sys
from datetime import datetime

TEMPLATE_DIR = "templates"
OUTPUT_DIR = "_datasets"

def ensure_directories():
    """Ensure required directories exist."""
    os.makedirs(TEMPLATE_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

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

        os.makedirs(os.path.dirname(template_path), exist_ok=True)
        with open(template_path, 'w') as file:
            file.write(template_content)
        print(f"Created template: {template_path}")

def create_dataset(dataset_id, name, description):
    """Create a new dataset configuration file."""
    # Ensure directories and template exist
    ensure_directories()
    create_template_if_not_exists()
    
    # Load template
    template_path = f"{TEMPLATE_DIR}/dataset.yml.template"
    with open(template_path, 'r') as file:
        template = file.read()
    
    # Replace placeholders
    content = template.replace("{{id}}", dataset_id)
    content = content.replace("{{name}}", name)
    content = content.replace("{{description}}", description)
    content = content.replace("{{date}}", datetime.now().strftime("%Y-%m-%d"))
    
    # Write dataset configuration
    output_path = f"{OUTPUT_DIR}/{dataset_id}.yml"
    with open(output_path, 'w') as file:
        file.write(content)
    
    print(f"Created dataset configuration: {output_path}")
    print()
    print("Next steps:")
    print(f"1. Edit {output_path} to customize dataset properties")
    print(f"2. Run 'python scripts/generate-assets.py' to generate assets")
    print(f"3. Create dataset directory: mkdir -p dataset/{dataset_id}")
    print(f"4. Create dataset page: dataset/{dataset_id}/index.md")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python create-dataset.py <id> <name> <description>")
        print("Example: python create-dataset.py kaggle 'Kaggle Dataset' 'A collection of Kaggle articles'")
        sys.exit(1)
    
    create_dataset(sys.argv[1], sys.argv[2], sys.argv[3]) 