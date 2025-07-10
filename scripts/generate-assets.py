#!/usr/bin/env python3
import os
import yaml
from string import Template

SVG_TEMPLATE_PATH = "assets/templates/dataset-logo.svg"
OUTPUT_DIR = "assets/images"

def load_dataset_config(dataset_id):
    """Load dataset configuration from YAML file."""
    with open(f"_datasets/{dataset_id}.yml", 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def generate_svg_logo(dataset_config):
    """Generate SVG logo from template and dataset configuration."""
    # Load SVG template
    with open(SVG_TEMPLATE_PATH, 'r', encoding='utf-8') as file:
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
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = f"{OUTPUT_DIR}/{dataset_id}-logo.svg"
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(svg_content)
    
    print(f"Generated logo: {output_path}")

def generate_favicon():
    """Generate favicon from template."""
    with open("assets/templates/favicon.svg", 'r', encoding='utf-8') as file:
        content = file.read()
    
    with open("assets/images/favicon.svg", 'w', encoding='utf-8') as file:
        file.write(content)
    
    print("Generated favicon: assets/images/favicon.svg")

def generate_logo():
    """Generate main logo."""
    # For simplicity, we'll use a copy of the favicon for the main logo
    with open("assets/templates/favicon.svg", 'r', encoding='utf-8') as file:
        content = file.read()
    
    with open("assets/images/logo.svg", 'w', encoding='utf-8') as file:
        file.write(content)
    
    print("Generated logo: assets/images/logo.svg")

def main():
    """Main execution function."""
    print("Generating assets...")
    
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Generate dataset logos
    for filename in os.listdir("_datasets"):
        if filename.endswith(".yml"):
            dataset_id = filename[:-4]  # Remove .yml extension
            try:
                config = load_dataset_config(dataset_id)
                generate_svg_logo(config)
            except Exception as e:
                print(f"Error processing {dataset_id}: {str(e)}")
    
    # Generate favicon and main logo
    generate_favicon()
    generate_logo()
    
    print("Asset generation complete!")

if __name__ == "__main__":
    main() 