#!/usr/bin/env python3
import os
import yaml
import shutil
import json
from pathlib import Path
from string import Template

# Define paths
DATASETS_DIR = "_datasets"
OUTPUT_DIR = "preview"
TEMPLATES_DIR = "assets/templates"

# HTML templates
PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MedData Preview</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        h1, h2, h3 {
            color: #2d3748;
        }
        .header {
            display: flex;
            align-items: center;
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 1px solid #e2e8f0;
        }
        .logo {
            width: 50px;
            height: 50px;
            margin-right: 15px;
        }
        .dataset-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
        }
        .dataset-card {
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 20px;
            background-color: #fff;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s;
        }
        .dataset-card:hover {
            transform: translateY(-5px);
        }
        .dataset-logo {
            width: 64px;
            height: 64px;
            margin-bottom: 15px;
        }
        .dataset-status {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 500;
            margin-bottom: 10px;
        }
        .published {
            background-color: #c6f6d5;
            color: #22543d;
        }
        .development {
            background-color: #fed7d7;
            color: #822727;
        }
        .dataset-stats {
            display: flex;
            margin-top: 15px;
            gap: 10px;
        }
        .dataset-stat {
            text-align: center;
            flex: 1;
        }
        .stat-number {
            font-size: 18px;
            font-weight: 600;
            display: block;
        }
        .stat-label {
            font-size: 12px;
            color: #718096;
        }
        .dataset-meta {
            display: flex;
            gap: 15px;
            margin-top: 15px;
            font-size: 14px;
            color: #718096;
        }
        .dataset-links {
            margin-top: 20px;
        }
        .button {
            display: inline-block;
            padding: 8px 16px;
            border-radius: 4px;
            font-size: 14px;
            font-weight: 500;
            text-decoration: none;
            margin-right: 10px;
        }
        .primary {
            background-color: #4f46e5;
            color: white;
        }
        .secondary {
            background-color: #e2e8f0;
            color: #4a5568;
        }
    </style>
</head>
<body>
    <div class="header">
        <img src="assets/images/logo.svg" alt="MedData Logo" class="logo">
        <h1>MedData Engineering Hub (Preview)</h1>
    </div>
    
    <section>
        <h2>Available Datasets</h2>
        <p>Explore our curated collection of high-quality datasets</p>
        
        <div class="dataset-grid">
            $DATASET_CARDS
        </div>
    </section>
</body>
</html>
"""

DATASET_CARD_TEMPLATE = """
<div class="dataset-card">
    <div class="dataset-status">
        <span class="status-badge $STATUS_CLASS">$STATUS</span>
    </div>
    
    <img src="assets/images/$DATASET_ID-logo.svg" alt="$NAME" class="dataset-logo">
    
    <h3>$NAME</h3>
    <p>$DESCRIPTION</p>
    
    <div class="dataset-stats">
        $STATS
    </div>
    
    <div class="dataset-meta">
        $META
    </div>
    
    <div class="dataset-links">
        <a href="dataset-$DATASET_ID.html" class="button primary">View Details</a>
        $PUBLISHING_LINKS
    </div>
</div>
"""

STAT_TEMPLATE = """
<div class="dataset-stat">
    <span class="stat-number">$VALUE</span>
    <span class="stat-label">$LABEL</span>
</div>
"""

META_ITEM_TEMPLATE = """
<div class="meta-item">
    $TEXT
</div>
"""

PUBLISHING_LINK_TEMPLATE = """
<a href="$URL" class="button secondary" target="_blank">$PLATFORM</a>
"""

DATASET_PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>$NAME - MedData Preview</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        h1, h2, h3 {
            color: #2d3748;
        }
        .header {
            display: flex;
            align-items: center;
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 1px solid #e2e8f0;
        }
        .logo {
            width: 50px;
            height: 50px;
            margin-right: 15px;
        }
        .dataset-header {
            display: flex;
            align-items: center;
            margin-bottom: 30px;
        }
        .dataset-logo {
            width: 100px;
            height: 100px;
            margin-right: 30px;
        }
        .dataset-info {
            flex: 1;
        }
        .dataset-status {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 500;
            margin-bottom: 10px;
        }
        .published {
            background-color: #c6f6d5;
            color: #22543d;
        }
        .development {
            background-color: #fed7d7;
            color: #822727;
        }
        .dataset-meta {
            display: flex;
            gap: 15px;
            margin-top: 15px;
            font-size: 14px;
            color: #718096;
        }
        .dataset-stats {
            display: flex;
            margin-top: 20px;
            gap: 20px;
        }
        .dataset-stat {
            text-align: center;
            background-color: #f7fafc;
            padding: 15px;
            border-radius: 8px;
            min-width: 100px;
        }
        .stat-number {
            font-size: 24px;
            font-weight: 600;
            display: block;
            color: #4a5568;
        }
        .stat-label {
            font-size: 14px;
            color: #718096;
        }
        .section {
            margin: 40px 0;
        }
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .feature-card {
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 20px;
            background-color: #fff;
        }
        .feature-icon {
            font-size: 24px;
            margin-bottom: 10px;
            display: block;
        }
        .schema-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        .schema-table th, .schema-table td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #e2e8f0;
        }
        .schema-table th {
            background-color: #f7fafc;
            font-weight: 500;
        }
        .back-link {
            display: inline-block;
            margin-top: 40px;
            color: #4a5568;
            text-decoration: none;
        }
        .back-link:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="header">
        <img src="assets/images/logo.svg" alt="MedData Logo" class="logo">
        <h1>MedData Engineering Hub (Preview)</h1>
    </div>
    
    <div class="dataset-header">
        <img src="assets/images/$DATASET_ID-logo.svg" alt="$NAME" class="dataset-logo">
        <div class="dataset-info">
            <div class="dataset-status">
                <span class="status-badge $STATUS_CLASS">$STATUS</span>
            </div>
            <h1>$NAME</h1>
            <p>$DESCRIPTION</p>
            <div class="dataset-meta">
                $META
            </div>
        </div>
    </div>
    
    <div class="dataset-stats">
        $STATS
    </div>
    
    <div class="section">
        <h2>Features</h2>
        <div class="feature-grid">
            $FEATURES
        </div>
    </div>
    
    <div class="section">
        <h2>Dataset Details</h2>
        <p><strong>Size:</strong> $SIZE</p>
        <p><strong>Format:</strong> $FORMAT</p>
        
        <h3>Schema</h3>
        <table class="schema-table">
            <thead>
                <tr>
                    <th>Field</th>
                    <th>Type</th>
                    <th>Description</th>
                    <th>Nullable</th>
                </tr>
            </thead>
            <tbody>
                $SCHEMA
            </tbody>
        </table>
    </div>
    
    <a href="index.html" class="back-link">← Back to Datasets</a>
</body>
</html>
"""

FEATURE_CARD_TEMPLATE = """
<div class="feature-card">
    <span class="feature-icon">$ICON</span>
    <h3>$TITLE</h3>
    <p>$DESCRIPTION</p>
</div>
"""

SCHEMA_ROW_TEMPLATE = """
<tr>
    <td>$NAME</td>
    <td>$TYPE</td>
    <td>$DESCRIPTION</td>
    <td>$NULLABLE</td>
</tr>
"""

def load_dataset_config(dataset_id):
    """Load dataset configuration from YAML file."""
    with open(f"{DATASETS_DIR}/{dataset_id}.yml", 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def generate_stat_html(stat):
    """Generate HTML for a single stat."""
    return Template(STAT_TEMPLATE).substitute(
        VALUE=stat.get('value', ''),
        LABEL=stat.get('label', '')
    )

def generate_meta_html(dataset):
    """Generate HTML for metadata items."""
    meta_items = []
    
    if dataset.get('release_date'):
        meta_items.append(Template(META_ITEM_TEMPLATE).substitute(
            TEXT=f"Released: {dataset['release_date']}"
        ))
    
    if dataset.get('expected_update'):
        meta_items.append(Template(META_ITEM_TEMPLATE).substitute(
            TEXT=f"Updates: {dataset['expected_update']}"
        ))
    
    return ''.join(meta_items)

def generate_publishing_links(dataset):
    """Generate HTML for publishing links."""
    links = []
    
    if 'publishing' in dataset and dataset['publishing']:
        for pub in dataset['publishing']:
            if 'url' in pub and 'platform' in pub:
                links.append(Template(PUBLISHING_LINK_TEMPLATE).substitute(
                    URL=pub['url'],
                    PLATFORM=pub['platform'].capitalize()
                ))
    
    return ''.join(links)

def generate_dataset_card(dataset):
    """Generate HTML for a dataset card."""
    stats_html = ''.join([generate_stat_html(stat) for stat in dataset.get('stats', [])])
    
    return Template(DATASET_CARD_TEMPLATE).substitute(
        DATASET_ID=dataset['id'],
        NAME=dataset['name'],
        DESCRIPTION=dataset['description'],
        STATUS=dataset['status'].capitalize(),
        STATUS_CLASS=dataset['status'],
        STATS=stats_html,
        META=generate_meta_html(dataset),
        PUBLISHING_LINKS=generate_publishing_links(dataset)
    )

def generate_feature_html(feature):
    """Generate HTML for a feature card."""
    return Template(FEATURE_CARD_TEMPLATE).substitute(
        ICON=feature.get('icon', '✨'),
        TITLE=feature.get('title', ''),
        DESCRIPTION=feature.get('description', '')
    )

def generate_schema_row_html(field):
    """Generate HTML for a schema row."""
    return Template(SCHEMA_ROW_TEMPLATE).substitute(
        NAME=field.get('name', ''),
        TYPE=field.get('type', ''),
        DESCRIPTION=field.get('description', ''),
        NULLABLE='Yes' if field.get('nullable') else 'No'
    )

def generate_dataset_page(dataset):
    """Generate HTML for a dataset detail page."""
    stats_html = ''.join([generate_stat_html(stat) for stat in dataset.get('stats', [])])
    features_html = ''.join([generate_feature_html(feature) for feature in dataset.get('features', [])])
    
    schema_html = ''
    if 'dataset_details' in dataset and 'schema' in dataset['dataset_details']:
        schema_html = ''.join([generate_schema_row_html(field) for field in dataset['dataset_details']['schema']])
    
    return Template(DATASET_PAGE_TEMPLATE).substitute(
        DATASET_ID=dataset['id'],
        NAME=dataset['name'],
        DESCRIPTION=dataset['description'],
        STATUS=dataset['status'].capitalize(),
        STATUS_CLASS=dataset['status'],
        META=generate_meta_html(dataset),
        STATS=stats_html,
        FEATURES=features_html,
        SIZE=dataset.get('dataset_details', {}).get('size', 'Unknown'),
        FORMAT=dataset.get('dataset_details', {}).get('file_format', 'Unknown'),
        SCHEMA=schema_html
    )

def main():
    """Main execution function."""
    print("Generating preview site...")
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Copy assets
    os.makedirs(f"{OUTPUT_DIR}/assets/images", exist_ok=True)
    for file in os.listdir("assets/images"):
        if file.endswith(".svg"):
            shutil.copy(f"assets/images/{file}", f"{OUTPUT_DIR}/assets/images/{file}")
    
    # Process datasets
    dataset_cards = []
    for filename in os.listdir(DATASETS_DIR):
        if filename.endswith(".yml"):
            dataset_id = filename[:-4]  # Remove .yml extension
            try:
                dataset = load_dataset_config(dataset_id)
                
                # Generate dataset card for index
                dataset_cards.append(generate_dataset_card(dataset))
                
                # Generate dataset detail page
                dataset_page = generate_dataset_page(dataset)
                with open(f"{OUTPUT_DIR}/dataset-{dataset_id}.html", 'w', encoding='utf-8') as file:
                    file.write(dataset_page)
                
                print(f"Generated preview page for {dataset_id}")
            except Exception as e:
                print(f"Error processing {dataset_id}: {str(e)}")
    
    # Generate index page
    index_html = Template(PAGE_TEMPLATE).substitute(
        DATASET_CARDS=''.join(dataset_cards)
    )
    with open(f"{OUTPUT_DIR}/index.html", 'w', encoding='utf-8') as file:
        file.write(index_html)
    
    print(f"Preview site generated in '{OUTPUT_DIR}' directory!")
    print("Open 'preview/index.html' in your browser to view the site.")

if __name__ == "__main__":
    main() 