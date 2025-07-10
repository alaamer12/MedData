#!/usr/bin/env node

/**
 * This script ensures that dataset documentation pages exist 
 * and that links to them are correctly configured.
 */

const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

// Paths
const DATASETS_DIR = '_datasets';
const DATASET_DOCS_DIR = 'dataset';
const DOCS_DIR = 'docs';

// Templates
const docPageTemplate = `---
layout: documentation
title: DATASET_NAME Documentation
description: Comprehensive documentation for the DATASET_NAME including schema, usage, and technical details
---

<h1>DATASET_NAME Documentation</h1>

<p class="lead">Dataset documentation is being generated. Please check back soon.</p>

<div class="dataset-meta">
  <div class="meta-item">
    <strong>Status:</strong> DATASET_STATUS
  </div>
</div>

<h2 id="overview">Overview</h2>

<p>DATASET_DESCRIPTION</p>

<h2 id="getting-started">Getting Started</h2>

<p>Documentation for this dataset is currently in progress. Please refer to the <a href="/MedData/docs/">main documentation</a> for general information.</p>
`;

function ensureDirectoryExists(dirPath) {
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
    console.log(`Created directory: ${dirPath}`);
  }
}

function loadDatasetConfigs() {
  const datasets = [];
  
  try {
    // First try to load from _data/datasets.yml
    if (fs.existsSync('_data/datasets.yml')) {
      const datasetYaml = fs.readFileSync('_data/datasets.yml', 'utf8');
      const datasetList = yaml.load(datasetYaml);
      if (Array.isArray(datasetList)) {
        datasets.push(...datasetList);
        console.log(`Loaded ${datasetList.length} datasets from _data/datasets.yml`);
      }
    }
    
    // Also load individual dataset files from _datasets directory
    if (fs.existsSync(DATASETS_DIR)) {
      const files = fs.readdirSync(DATASETS_DIR);
      for (const file of files) {
        if (file.endsWith('.yml')) {
          const datasetYaml = fs.readFileSync(path.join(DATASETS_DIR, file), 'utf8');
          const datasetConfig = yaml.load(datasetYaml);
          
          // Check if this dataset is already loaded from _data/datasets.yml
          const existingIndex = datasets.findIndex(d => d.id === datasetConfig.id);
          if (existingIndex >= 0) {
            // Update with more detailed info from the individual file
            datasets[existingIndex] = { ...datasets[existingIndex], ...datasetConfig };
          } else {
            datasets.push(datasetConfig);
          }
        }
      }
      console.log(`Loaded datasets from ${DATASETS_DIR} directory`);
    }
  } catch (error) {
    console.error(`Error loading dataset configs: ${error.message}`);
  }
  
  return datasets;
}

function ensureDocsExist(datasets) {
  for (const dataset of datasets) {
    const datasetId = dataset.id;
    if (!datasetId) continue;
    
    // Create dataset directory if it doesn't exist
    const datasetDir = path.join(DATASET_DOCS_DIR, datasetId);
    ensureDirectoryExists(datasetDir);
    
    // Create or check docs.html file
    const docsPath = path.join(datasetDir, 'docs.html');
    if (!fs.existsSync(docsPath)) {
      const docContent = docPageTemplate
        .replace(/DATASET_NAME/g, dataset.name || datasetId.charAt(0).toUpperCase() + datasetId.slice(1))
        .replace(/DATASET_STATUS/g, dataset.status || 'Development')
        .replace(/DATASET_DESCRIPTION/g, dataset.description || 'A comprehensive dataset for machine learning and data science research.');
      
      fs.writeFileSync(docsPath, docContent);
      console.log(`Created documentation file: ${docsPath}`);
    } else {
      console.log(`Documentation file already exists: ${docsPath}`);
    }
  }
}

function fixDocLinks() {
  // Update links in docs/index.md
  if (fs.existsSync(path.join(DOCS_DIR, 'index.md'))) {
    let content = fs.readFileSync(path.join(DOCS_DIR, 'index.md'), 'utf8');
    
    // Fix links to dataset docs
    content = content.replace(/\]\(\.\.\/dataset\/([a-zA-Z0-9-_]+)\/docs\.md\)/g, ']({{ site.baseurl }}/dataset/$1/docs.html)');
    
    fs.writeFileSync(path.join(DOCS_DIR, 'index.md'), content);
    console.log('Updated links in docs/index.md');
  }
}

function main() {
  console.log('Fixing documentation pages...');
  
  // Load dataset configs
  const datasets = loadDatasetConfigs();
  console.log(`Found ${datasets.length} datasets`);
  
  // Ensure documentation pages exist
  ensureDocsExist(datasets);
  
  // Fix links to documentation pages
  fixDocLinks();
  
  console.log('Documentation fix complete!');
}

main(); 