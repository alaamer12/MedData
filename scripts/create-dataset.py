#!/usr/bin/env python3
"""
MedData Create Dataset Script - Creates a new dataset configuration.

This script handles the creation of a new dataset configuration file based on a template,
including validation of dataset ID, creation of required directories, and setup of
initial dataset structure.
"""
from __future__ import annotations

import sys
from datetime import datetime
from scripts.utils.printer import printer
from scripts.utils.config_manager import config_manager

__all__ = ["ensure_directories", "create_template_if_not_exists", "create_dataset"]


def ensure_directories() -> None:
    """
    Ensure required directories exist.
    
    Creates the template and output directories if they don't exist.
    
    Raises:
        PermissionError: If the user doesn't have permission to create the directories
        OSError: If there's an error creating the directories
    """
    try:
        config_manager.ensure_directories_exist()
    except PermissionError as e:
        printer.error(f"Permission denied when creating directories", e)
        sys.exit(1)
    except Exception as e:
        printer.error(f"Error creating directories", e)
        sys.exit(1)


def create_template_if_not_exists() -> None:
    """
    Create the dataset template if it doesn't exist.
    
    Generates a default dataset configuration template file.
    
    Raises:
        PermissionError: If the user doesn't have permission to create the template
        OSError: If there's an error creating the template
    """
    template_path = config_manager.paths.templates_dir / "dataset.yml.template"

    if not template_path.exists():
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
            template_path.parent.mkdir(exist_ok=True, parents=True)
            with open(template_path, 'w') as file:
                file.write(template_content)
            printer.success(f"Created template: {template_path}")
        except PermissionError as e:
            printer.error(f"Permission denied when creating template file", e)
            sys.exit(1)
        except Exception as e:
            printer.error(f"Error creating template file", e)
            sys.exit(1)


def create_dataset(dataset_id: str, name: str, description: str) -> None:
    """
    Create a new dataset configuration file.
    
    Args:
        dataset_id: Unique identifier for the dataset (alphanumeric with hyphens)
        name: Human-readable name for the dataset
        description: Brief description of the dataset
        
    Raises:
        ValueError: If the dataset ID is invalid
        FileExistsError: If the dataset already exists
        PermissionError: If the user doesn't have permission to create files
        OSError: If there's an error creating files
    """
    # Validate dataset ID
    if not dataset_id.isalnum() and not all(c.isalnum() or c == '-' for c in dataset_id):
        printer.error(f"Invalid dataset ID: '{dataset_id}'. Use only alphanumeric characters and hyphens.")
        sys.exit(1)

    # Check if dataset already exists
    output_path = config_manager.paths.datasets_dir / f"{dataset_id}.yml"
    if output_path.exists():
        printer.error(f"Dataset '{dataset_id}' already exists at {output_path}")
        sys.exit(1)

    # Ensure directories and template exist
    ensure_directories()
    create_template_if_not_exists()

    # Load template
    template_path = config_manager.paths.templates_dir / "dataset.yml.template"
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
        dataset_dir = config_manager.paths.project_root / "dataset" / dataset_id
        dataset_dir.mkdir(exist_ok=True, parents=True)

        # Create basic index file
        with open(dataset_dir / "index.md", 'w') as file:
            file.write(f"""---
layout: dataset
title: {name}
description: {description}
---

# {name}

{description}
""")

        # Show success message with next steps
        printer.dataset_created(dataset_id, str(output_path))

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
