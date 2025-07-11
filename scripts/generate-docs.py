#!/usr/bin/env python3
"""
MedData Generate Docs Script - Creates documentation for datasets.

This script generates various documentation files for datasets, including
README.md, dataset cards for Hugging Face, citation files, and licenses.
It uses templates to ensure consistency across datasets.
"""
from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path
from string import Template
from typing import Dict, Any

import yaml
from scripts.utils.printer import printer
from scripts.utils.config_manager import config_manager

__all__ = ["load_dataset_config", "ensure_templates_exist", "generate_readme",
           "generate_dataset_card", "generate_citation", "generate_license",
           "generate_dataset_docs"]


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


def ensure_templates_exist() -> None:
    """
    Create documentation templates if they don't exist.
    
    Generates standard templates for README, dataset card, and citation files
    if they don't already exist.
    """
    config_manager.paths.templates_dir.mkdir(exist_ok=True, parents=True)

    templates = {
        "dataset-readme.md.template": """# {{ name }}

[![Hugging Face](https://img.shields.io/badge/🤗%20Hugging%20Face-Dataset-yellow)]({{ huggingface_url }})
[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)]({{ github_url }})

{{ description }}

## Dataset Information

- **Size**: {{ stats.size }}
- **Format**: {{ stats.format }}
- **Last Updated**: {{ stats.updated }}

## Features

{% for feature in features %}
- **{{ feature.title }}**: {{ feature.description }}
{% endfor %}

## Usage

```python
from datasets import load_dataset

# Load dataset
dataset = load_dataset("{{ huggingface_repo }}")

# Basic usage
for item in dataset['train']:
    print(f"Title: {item['title']}")
```

## Citation

Please cite this dataset using:

```bibtex
{{ citation }}
```

## License

{{ license }}
""",
        "dataset-card.md.template": """---
annotations_creators:
- collected-from-web
language:
- en
language_creators:
- found
license:
- mit
multilinguality:
- monolingual
size_categories:
- {{ size_category }}
source_datasets:
- original
task_categories:
- text-classification
- text-generation
task_ids:
- topic-classification
- summarization
---

# Dataset Card for {{ name }}

## Dataset Description

- **Repository:** [{{ name }}]({{ repository_url }})
- **Point of Contact:** {{ contact }}

### Dataset Summary

{{ description }}

### Supported Tasks and Leaderboards

{{ tasks }}

### Languages

The dataset is in English.

### Dataset Structure

{{ structure }}

#### Data Instances

{{ data_instances }}

#### Data Fields

{{ data_fields }}

#### Data Splits

{{ data_splits }}

### Dataset Creation

{{ dataset_creation }}

### Considerations for Using the Data

{{ considerations }}

### Citation Information

{{ citation }}

### Contributions

{{ contributions }}
""",
        "citation.cff.template": """cff-version: 1.2.0
message: "If you use this dataset, please cite it as below."
authors:
  - family-names: "{{ author_family_name }}"
    given-names: "{{ author_given_name }}"
    orcid: "{{ author_orcid }}"
title: "{{ name }}"
date-released: {{ release_date }}
url: "{{ repository_url }}"
preferred-citation:
  type: dataset
  authors:
    - family-names: "{{ author_family_name }}"
      given-names: "{{ author_given_name }}"
      orcid: "{{ author_orcid }}"
  title: "{{ name }}"
  year: {{ release_year }}
  url: "{{ repository_url }}"
"""
    }

    for filename, content in templates.items():
        template_path = config_manager.paths.templates_dir / filename
        if not template_path.exists():
            with open(template_path, 'w') as file:
                file.write(content)
            printer.success(f"Created template: {template_path}")


def generate_readme(dataset_id: str, config: Dict[str, Any]) -> Path:
    """
    Generate README.md for the dataset.
    
    Args:
        dataset_id: ID of the dataset
        config: Dataset configuration dictionary
        
    Returns:
        Path to the generated README file
    """
    printer.header(f"Generating README for {dataset_id}...")

    # Load template
    template_path = config_manager.paths.templates_dir / "dataset-readme.md.template"
    with open(template_path, 'r') as file:
        template = Template(file.read())

    # Find Hugging Face and GitHub URLs
    huggingface_url = ""
    github_url = ""
    huggingface_repo = ""

    for pub in config.get('publishing', []):
        if pub['platform'] == 'huggingface':
            huggingface_url = pub.get('url', f"https://huggingface.co/datasets/{pub['repository']}")
            huggingface_repo = pub['repository']
        elif pub['platform'] == 'github':
            github_url = pub.get('url', f"https://github.com/{pub['repository']}")

    # Prepare template variables
    size_value = "Unknown"
    for stat in config.get('stats', []):
        if stat['label'].lower() in ['articles', 'items', 'entries']:
            size_value = stat['value']

    variables = {
        'name': config['name'],
        'description': config['description'],
        'huggingface_url': huggingface_url,
        'github_url': github_url,
        'huggingface_repo': huggingface_repo,
        'stats': {
            'size': size_value,
            'format': 'Parquet/CSV',
            'updated': datetime.now().strftime("%Y-%m-%d")
        },
        'features': config.get('features', []),
        'citation': 'Please see CITATION.cff file',
        'license': 'MIT License'
    }

    # Generate README content
    try:
        content = template.substitute(**variables)
    except KeyError as e:
        printer.warning(f"Missing template variable: {e}")
        content = template.safe_substitute(**variables)

    # Write README file
    output_dir = config_manager.paths.docs_dir / dataset_id
    output_dir.mkdir(exist_ok=True, parents=True)
    output_path = output_dir / "README.md"

    with open(output_path, 'w') as file:
        file.write(content)

    printer.success(f"Generated README: {output_path}")
    return output_path


def generate_dataset_card(dataset_id: str, config: Dict[str, Any]) -> Path:
    """
    Generate dataset card for Hugging Face.
    
    Args:
        dataset_id: ID of the dataset
        config: Dataset configuration dictionary
        
    Returns:
        Path to the generated dataset card file
    """
    printer.header(f"Generating dataset card for {dataset_id}...")

    # Load template
    template_path = config_manager.paths.templates_dir / "dataset-card.md.template"
    with open(template_path, 'r') as file:
        template = Template(file.read())

    # Determine size category
    size_category = "unknown"
    for stat in config.get('stats', []):
        if stat['label'].lower() in ['articles', 'items', 'entries']:
            size_value = stat['value']
            if isinstance(size_value, str):
                if "k+" in size_value.lower() or "thousand" in size_value.lower():
                    size_category = "10K<n<100K"
                elif "100k+" in size_value.lower():
                    size_category = "100K<n<1M"
                elif "m+" in size_value.lower() or "million" in size_value.lower():
                    size_category = "1M<n<10M"
            elif isinstance(size_value, int):
                if size_value < 10000:
                    size_category = "n<10K"
                elif size_value < 100000:
                    size_category = "10K<n<100K"
                elif size_value < 1000000:
                    size_category = "100K<n<1M"
                else:
                    size_category = "1M<n<10M"

    # Find repository URL
    repository_url = ""
    for pub in config.get('publishing', []):
        if pub['platform'] == 'huggingface':
            repository_url = pub.get('url', f"https://huggingface.co/datasets/{pub['repository']}")
            break

    # Prepare template variables
    variables = {
        'name': config['name'],
        'description': config['description'],
        'repository_url': repository_url,
        'size_category': size_category,
        'contact': 'Alaamer',
        'tasks': 'This dataset is suitable for text classification, topic analysis, content analysis, and text generation tasks.',
        'structure': 'The dataset contains the full text of articles along with metadata.',
        'data_instances': 'Each instance represents an article with its content and associated metadata.',
        'data_fields': 'The dataset includes fields such as title, content, author, and publication date.',
        'data_splits': 'The dataset is provided as a single train split.',
        'dataset_creation': 'The dataset was collected from public web sources and processed for research purposes.',
        'considerations': 'The dataset contains publicly available content. Users should respect copyright and terms of use.',
        'citation': 'Please see the citation information in the CITATION.cff file.',
        'contributions': 'Thanks to the MedData Engineering Hub team for preparing and publishing this dataset.'
    }

    # Generate dataset card content
    try:
        content = template.substitute(**variables)
    except KeyError as e:
        printer.warning(f"Missing template variable: {e}")
        content = template.safe_substitute(**variables)

    # Write dataset card file
    output_dir = config_manager.paths.docs_dir / dataset_id
    output_dir.mkdir(exist_ok=True, parents=True)
    output_path = output_dir / "dataset-card.md"

    with open(output_path, 'w') as file:
        file.write(content)

    printer.success(f"Generated dataset card: {output_path}")
    return output_path


def generate_citation(dataset_id: str, config: Dict[str, Any]) -> Path:
    """
    Generate CITATION.cff for the dataset.
    
    Args:
        dataset_id: ID of the dataset
        config: Dataset configuration dictionary
        
    Returns:
        Path to the generated citation file
    """
    printer.header(f"Generating citation for {dataset_id}...")

    # Load template
    template_path = config_manager.paths.templates_dir / "citation.cff.template"
    with open(template_path, 'r') as file:
        template = Template(file.read())

    # Find repository URL
    repository_url = ""
    for pub in config.get('publishing', []):
        if pub['platform'] == 'huggingface':
            repository_url = pub.get('url', f"https://huggingface.co/datasets/{pub['repository']}")
            break
        elif pub['platform'] == 'github' and not repository_url:
            repository_url = pub.get('url', f"https://github.com/{pub['repository']}")

    # Prepare template variables
    release_date = config.get('release_date', datetime.now().strftime("%Y-%m-%d"))
    if isinstance(release_date, datetime):
        release_date = release_date.strftime("%Y-%m-%d")

    variables = {
        'name': config['name'],
        'repository_url': repository_url,
        'author_family_name': 'Alaamer',
        'author_given_name': '',
        'author_orcid': '',
        'release_date': release_date,
        'release_year': release_date.split('-')[0] if isinstance(release_date, str) and '-' in release_date else "2025"
    }

    # Generate citation content
    try:
        content = template.substitute(**variables)
    except KeyError as e:
        printer.warning(f"Missing template variable: {e}")
        content = template.safe_substitute(**variables)

    # Write citation file
    output_dir = config_manager.paths.docs_dir / dataset_id
    output_dir.mkdir(exist_ok=True, parents=True)
    output_path = output_dir / "CITATION.cff"

    with open(output_path, 'w') as file:
        file.write(content)

    printer.success(f"Generated citation: {output_path}")
    return output_path


def generate_license(dataset_id: str) -> Path:
    """
    Generate LICENSE file for the dataset.
    
    Args:
        dataset_id: ID of the dataset
        
    Returns:
        Path to the generated license file
    """
    printer.header(f"Generating license for {dataset_id}...")

    license_content = """MIT License

Copyright (c) 2025 MedData Engineering Hub

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

    # Write license file
    output_dir = config_manager.paths.docs_dir / dataset_id
    output_dir.mkdir(exist_ok=True, parents=True)
    output_path = output_dir / "LICENSE"

    with open(output_path, 'w') as file:
        file.write(license_content)

    printer.success(f"Generated license: {output_path}")
    return output_path


def generate_dataset_docs(dataset_id: str) -> None:
    """
    Generate all documentation for a dataset.
    
    Args:
        dataset_id: ID of the dataset to generate documentation for
    """
    printer.header(f"Generating documentation for dataset: {dataset_id}")

    # Ensure directories exist
    config_manager.ensure_directories_exist()

    # Ensure templates exist
    ensure_templates_exist()

    # Load dataset configuration
    config = load_dataset_config(dataset_id)

    # Generate documentation files
    readme_path = generate_readme(dataset_id, config)
    card_path = generate_dataset_card(dataset_id, config)
    citation_path = generate_citation(dataset_id, config)
    license_path = generate_license(dataset_id)

    printer.success(f"\nDocumentation generation complete for {dataset_id}!")
    printer.table(
        ["Document Type", "Path"],
        [
            ["README", str(readme_path)],
            ["Dataset Card", str(card_path)],
            ["Citation", str(citation_path)],
            ["License", str(license_path)]
        ],
        "Generated Files"
    )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        printer.error("Usage: python generate-docs.py <dataset_id>")
        printer.guide("Example", ["python generate-docs.py medium"])
        sys.exit(1)

    generate_dataset_docs(sys.argv[1])
