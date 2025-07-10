# Troubleshooting Guide

This document provides solutions for common issues you might encounter with the MedData Engineering Hub.

## Missing Dataset Content

If your dataset pages are showing blank or missing content, follow these steps:

1. Check that your dataset configuration files exist in the `_datasets` directory
2. Make sure each dataset has a corresponding page in the `dataset/[dataset-id]/index.md` directory
3. Verify that the dataset pages are using the correct include:

```markdown
---
layout: dataset
title: Your Dataset Title
description: Your dataset description
---

{% assign dataset_file = site.datasets | where: "id", "your-dataset-id" | first %}
{% if dataset_file %}
  {% include dataset-content.html dataset=dataset_file %}
{% else %}
  {% assign dataset_data = site.data.datasets | where: "id", "your-dataset-id" | first %}
  {% assign dataset_config = site.data.your-dataset-id %}
  {% if dataset_config %}
    {% include dataset-content.html dataset=dataset_config %}
  {% else %}
    <div class="error-message">
      <p>Dataset configuration not found. Please check that <code>_datasets/your-dataset-id.yml</code> exists and is properly formatted.</p>
    </div>
  {% endif %}
{% endif %}
```

## Missing Logo Images (404 Errors)

If you see 404 errors for logo images in the browser console, you need to generate the logo SVG files:

1. Install dependencies:
   ```bash
   npm install
   ```

2. Generate the logos:
   ```bash
   npm run generate-logos
   ```

3. Verify that the logo files were created in the `assets/images` directory

## Jekyll Logo Not Found

If you're seeing a 404 error specifically for `jekyll-logo.svg`, the logo generator script will create this file along with all dataset logos. Run:

```bash
npm run generate-logos
```

This will create all the necessary logo files, including the Jekyll logo.

## Manual Logo Creation

If you need to manually create a logo for a dataset:

1. Copy the template from `assets/templates/dataset-logo.svg`
2. Replace the following placeholders:
   - `DATASET_ID_PLACEHOLDER` with your dataset ID
   - `LOGO_TEXT_PLACEHOLDER` with the text to display (usually the first letter of your dataset name)
   - `PRIMARY_COLOR_PLACEHOLDER` with your primary color (e.g., `#6366f1`)
   - `SECONDARY_COLOR_PLACEHOLDER` with your secondary color (e.g., `#14b8a6`)
3. Save the file as `assets/images/your-dataset-id-logo.svg`

## Jekyll Collection Issues

If your dataset content isn't showing up correctly, make sure your `_config.yml` has the correct collections configuration:

```yaml
collections:
  datasets:
    output: true
    permalink: /dataset/:path/

defaults:
  - scope:
      path: ""
      type: "datasets"
    values:
      layout: "dataset"
``` 