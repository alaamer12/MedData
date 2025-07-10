# Troubleshooting Guide

This guide provides solutions for common issues you might encounter when working with the MedData Engineering Hub.

## Website and Asset Issues

### Missing Dataset Logos or Incorrect Rendering

If you encounter issues with dataset pages not displaying correctly or missing logos, try these steps:

1. **Generate missing logos**:
   ```bash
   npm run generate-logos
   ```

2. **Setup dataset collections**:
   ```bash
   npm run setup-datasets
   ```

3. **Run both steps at once**:
   ```bash
   npm run setup
   ```

### Jekyll Rendering Issues

If Jekyll is not rendering the site correctly:

1. **Check Jekyll installation**:
   ```bash
   bundle exec jekyll -v
   ```

2. **Clear Jekyll cache**:
   ```bash
   bundle exec jekyll clean
   ```

3. **Check for syntax errors in front matter**:
   ```bash
   bundle exec jekyll build --verbose
   ```

## Dataset Processing Issues

### Data Download Failures

If you're experiencing issues downloading dataset source data:

1. **Check network connectivity**:
   ```bash
   ping api.example.com
   ```

2. **Verify API tokens** in your environment variables

3. **Check rate limits** on the API services you're using

### Processing Pipeline Errors

If the dataset processing pipeline fails:

1. **Enable verbose logging**:
   ```bash
   python meddata.py process <dataset_id> --verbose
   ```

2. **Check disk space** for large datasets:
   ```bash
   df -h
   ```

3. **Try processing a subset** of the data:
   ```bash
   python meddata.py process <dataset_id> --limit 1000
   ```

## Hugging Face Integration Issues

If you're having trouble with Hugging Face dataset uploads or downloads:

1. **Verify Hugging Face token**:
   ```bash
   huggingface-cli whoami
   ```

2. **Check dataset visibility settings** in your Hugging Face account

3. **Try with a smaller dataset** to isolate the issue:
   ```bash
   python meddata.py publish <dataset_id> --sample --token <token>
   ```

## Common Error Messages and Solutions

### "Cannot find module 'xyz'"

```
npm install --save xyz
```

### "Permission denied when writing to directory"

```bash
chmod +w <directory_path>
```

### "Dataset configuration not found"

Ensure your dataset configuration file exists at `_datasets/<dataset_id>.yml` and follows the correct format.

## Getting Additional Help

If you're still experiencing issues:

1. **Check existing GitHub issues** to see if others have encountered the same problem

2. **Open a new issue** with:
   - Detailed description of the problem
   - Steps to reproduce
   - Error messages and logs
   - System information (OS, Python version, etc.)

3. **Join our Discord community** for real-time support 