#!/usr/bin/env python3
"""
MedData Generate Assets Script - Generates visual assets for datasets.

This script creates SVG logos and other visual assets for datasets based on 
their configuration. It handles logo generation with customizable colors,
text, and shapes, as well as favicon and main logo generation.
"""
from __future__ import annotations
from string import Template
from typing import Dict, Any

import yaml
from scripts.utils.printer import printer
from scripts.utils.config_manager import config_manager

__all__ = ["load_dataset_config", "generate_svg_logo", "generate_favicon",
           "generate_logo", "main"]


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
    with open(config_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)


def generate_svg_logo(dataset_config: Dict[str, Any]) -> str:
    """
    Generate SVG logo from template and dataset configuration.
    
    Args:
        dataset_config: Dictionary containing the dataset configuration
        
    Returns:
        Path to the generated SVG logo file
        
    Raises:
        FileNotFoundError: If the template file doesn't exist
        KeyError: If required fields are missing from the configuration
    """
    # Load SVG template
    template_path = config_manager.paths.project_root / "assets" / "templates" / "dataset-logo.svg"
    with open(template_path, 'r', encoding='utf-8') as file:
        template = Template(file.read())

    # Extract configuration
    dataset_id = dataset_config['id']
    text = dataset_config.get('logo', {}).get('text', dataset_id[0].upper())
    background = dataset_config.get('logo', {}).get('background', 'circle')
    primary_color = dataset_config.get('logo', {}).get('colors', {}).get('primary', '#6366f1')
    secondary_color = dataset_config.get('logo', {}).get('colors', {}).get('secondary', '#14b8a6')

    # Generate SVG content
    svg_content = template.substitute(
        DATASET_ID=dataset_id,
        LOGO_TEXT=text,
        BACKGROUND_SHAPE=background,
        PRIMARY_COLOR=primary_color,
        SECONDARY_COLOR=secondary_color
    )

    # Write SVG file
    output_dir = config_manager.paths.project_root / "assets" / "images"
    output_dir.mkdir(exist_ok=True, parents=True)
    output_path = output_dir / f"{dataset_id}-logo.svg"
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(svg_content)

    printer.success(f"Generated logo: {output_path}")
    return str(output_path)


def generate_favicon() -> str:
    """
    Generate favicon from template.
    
    Returns:
        Path to the generated favicon file
        
    Raises:
        FileNotFoundError: If the template file doesn't exist
    """
    template_path = config_manager.paths.project_root / "assets" / "templates" / "favicon.svg"
    output_path = config_manager.paths.project_root / "assets" / "images" / "favicon.svg"

    with open(template_path, 'r', encoding='utf-8') as file:
        content = file.read()

    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(content)

    printer.success(f"Generated favicon: {output_path}")
    return str(output_path)


def generate_logo() -> str:
    """
    Generate main logo.
    
    Returns:
        Path to the generated logo file
        
    Raises:
        FileNotFoundError: If the template file doesn't exist
    """
    # For simplicity, we'll use a copy of the favicon for the main logo
    template_path = config_manager.paths.project_root / "assets" / "templates" / "favicon.svg"
    output_path = config_manager.paths.project_root / "assets" / "images" / "logo.svg"

    with open(template_path, 'r', encoding='utf-8') as file:
        content = file.read()

    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(content)

    printer.success(f"Generated logo: {output_path}")
    return str(output_path)


def main() -> None:
    """
    Main execution function.
    
    Generates assets for all datasets found in the _datasets directory,
    including dataset logos, favicon, and main logo.
    """
    printer.header("Generating assets...")

    # Ensure output directory exists
    output_dir = config_manager.paths.project_root / "assets" / "images"
    output_dir.mkdir(exist_ok=True, parents=True)

    # Generate dataset logos
    datasets_processed = 0
    for config_file in config_manager.paths.datasets_dir.glob("*.yml"):
        dataset_id = config_file.stem  # Remove .yml extension
        try:
            config = load_dataset_config(dataset_id)
            generate_svg_logo(config)
            datasets_processed += 1
        except Exception as e:
            printer.error(f"Error processing {dataset_id}", e)

    # Generate favicon and main logo
    generate_favicon()
    generate_logo()

    printer.success(f"Asset generation complete! Processed {datasets_processed} datasets.")


if __name__ == "__main__":
    main()
