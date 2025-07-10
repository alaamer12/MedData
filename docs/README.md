# MedData Engineering Hub - Documentation

This documentation provides information on the structure and usage of the MedData Engineering Hub.

## Project Structure

```
meddata/
├── _config.yml                    # Jekyll configuration
├── _datasets/                     # Dataset definitions (collection)
│   ├── medium.yml                 # Medium dataset configuration
│   └── devto.yml                  # Dev.to dataset configuration
├── _layouts/                      # Jekyll templates
│   ├── default.html               # Base layout
│   ├── dataset.html               # Dataset page layout
│   └── home.html                  # Homepage layout
├── _includes/                     # Reusable components
│   ├── header.html                # Site header
│   ├── footer.html                # Site footer
│   ├── dataset-card.html          # Dataset card component
│   └── stats-display.html         # Statistics display component
├── assets/                        # Static assets
│   ├── css/                       # Stylesheets
│   ├── js/                        # JavaScript files
│   ├── images/                    # Image files
│   └── templates/                 # SVG templates for auto-generation
├── scripts/                       # Automation scripts
│   ├── create-dataset.py          # Dataset scaffolding script
│   ├── process-dataset.py         # Dataset processing pipeline
│   ├── publish-dataset.py         # Dataset publishing script
│   └── generate-assets.py         # Asset generation script
├── _data/                         # Jekyll data files
│   └── datasets.yml               # Global dataset metadata
├── docs/                          # Documentation
├── index.md                       # Homepage
└── dataset/                       # Dataset pages (generated)
    ├── medium/                    # Medium dataset page
    └── devto/                     # Dev.to dataset page
```

## Adding a New Dataset

To add a new dataset to the MedData Engineering Hub, follow these steps:

1. **Initialize Dataset Configuration**:
   ```bash
   python meddata.py init <dataset_id> "<Dataset Name>" "Short description of the dataset"
   ```
   This will create a configuration file in `_datasets/<dataset_id>.yml`.

2. **Customize Configuration**:
   Edit the generated configuration file to add details about the dataset, such as sources, publishing information, and features.

3. **Generate Assets**:
   ```bash
   python meddata.py assets <dataset_id>
   ```
   This will generate assets like dataset logo based on the configuration.

4. **Create Dataset Page**:
   Create a directory and index file for the dataset page:
   ```bash
   mkdir -p dataset/<dataset_id>
   ```
   Create an `index.md` file in the directory with the appropriate front matter.

5. **Process Dataset Data** (if applicable):
   ```bash
   python meddata.py process <dataset_id>
   ```
   This will download and process the data from the sources specified in the configuration.

6. **Generate Documentation**:
   ```bash
   python meddata.py docs <dataset_id>
   ```
   This will generate documentation files for the dataset.

7. **Publish Dataset** (if applicable):
   ```bash
   python meddata.py publish <dataset_id> --token <api_token>
   ```
   This will publish the dataset to the platforms specified in the configuration.

## Building the Website

To build and test the website locally:

```bash
python meddata.py site --serve
```

This will build the Jekyll site and serve it locally for testing.

## Deploying the Website

The website is automatically deployed via GitHub Actions when changes are pushed to the main branch. See `.github/workflows/build-deploy.yml` for deployment configuration.

## Additional Resources

- For more detailed information about each script, see the comments in the script files.
- For information about the dataset processing pipeline, see the documentation in `docs/pipeline.md`.
- For information about the template system, see the documentation in `docs/templates.md`. 