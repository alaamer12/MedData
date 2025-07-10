#!/usr/bin/env python3
import os
import yaml
from string import Template

SVG_TEMPLATE_PATH = "assets/templates/dataset-logo.svg"
OUTPUT_DIR = "assets/images"

def load_dataset_config(dataset_id):
    """Load dataset configuration from YAML file."""
    with open(f"_datasets/{dataset_id}.yml", 'r') as file:
        return yaml.safe_load(file)

def generate_svg_logo(dataset_config):
    """Generate SVG logo from template and dataset configuration."""
    # Load SVG template
    with open(SVG_TEMPLATE_PATH, 'r') as file:
        template = Template(file.read())
    
    # Extract configuration
    dataset_id = dataset_config['id']
    text = dataset_config['logo']['text']
    background = dataset_config['logo']['background']
    primary_color = dataset_config['logo']['colors']['primary']
    secondary_color = dataset_config['logo']['colors']['secondary']
    
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
    with open(output_path, 'w') as file:
        file.write(svg_content)
    
    print(f"Generated logo: {output_path}")

def generate_favicon():
    """Generate favicon from template."""
    with open("assets/templates/favicon.svg", 'r') as file:
        content = file.read()
    
    with open("assets/images/favicon.svg", 'w') as file:
        file.write(content)
    
    print("Generated favicon: assets/images/favicon.svg")

def generate_logo():
    """Generate main logo."""
    # For simplicity, we'll use a copy of the favicon for the main logo
    with open("assets/templates/favicon.svg", 'r') as file:
        content = file.read()
    
    with open("assets/images/logo.svg", 'w') as file:
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
            config = load_dataset_config(dataset_id)
            generate_svg_logo(config)
    
    # Generate favicon and main logo
    generate_favicon()
    generate_logo()
    
    print("Asset generation complete!")

if __name__ == "__main__":
    main() 