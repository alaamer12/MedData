# Kaggle Configuration

This directory contains Kaggle API configuration files.

## Setup Instructions

1. Go to your Kaggle account settings (https://www.kaggle.com/account)
2. Scroll to the API section and click "Create New API Token"
3. Download the `kaggle.json` file
4. Replace the contents of the `kaggle.json` file in this directory with your downloaded file
5. Ensure the file permissions are set correctly (600 on Unix systems)

**Important**: Never commit your actual API credentials to version control. The `kaggle.json` file in this directory is just a template.
