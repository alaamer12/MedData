/**
 * Dataset Setup Script
 * Converts dataset YAML files into Jekyll collection files
 */

const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

// Paths
const DATASETS_DIR = path.join(__dirname, '../_datasets');
const JEKYLL_DATASETS_DIR = path.join(__dirname, '../_datasets_collection');

// Ensure output directory exists
if (!fs.existsSync(JEKYLL_DATASETS_DIR)) {
  fs.mkdirSync(JEKYLL_DATASETS_DIR, { recursive: true });
}

// Process each dataset
const datasetFiles = fs.readdirSync(DATASETS_DIR).filter(file => file.endsWith('.yml'));

datasetFiles.forEach(file => {
  const datasetPath = path.join(DATASETS_DIR, file);
  const datasetContent = fs.readFileSync(datasetPath, 'utf8');
  const dataset = yaml.load(datasetContent);
  
  // Extract needed values
  const datasetId = dataset.id;
  
  // Create a new object with all the front matter data
  const frontMatterData = {
    layout: 'dataset',
    title: dataset.name,
    description: dataset.description,
    id: datasetId,
    status: dataset.status,
    release_date: dataset.release_date,
    expected_update: dataset.expected_update,
    logo: {
      text: dataset.logo?.text || datasetId.charAt(0).toUpperCase(),
      background: dataset.logo?.background || 'circle',
      colors: {
        primary: dataset.logo?.colors?.primary || '#6366f1',
        secondary: dataset.logo?.colors?.secondary || '#14b8a6'
      }
    },
    stats: dataset.stats,
    sources: dataset.sources,
    publishing: dataset.publishing,
    features: dataset.features,
    dataset_details: dataset.dataset_details
  };
  
  // Convert the entire object to properly formatted YAML
  const yamlFrontMatter = yaml.dump(frontMatterData);
  
  // Create Jekyll collection file with proper front matter
  const jekyllContent = `---
${yamlFrontMatter}---
`;

  // Write to file
  const outputPath = path.join(JEKYLL_DATASETS_DIR, `${datasetId}.md`);
  fs.writeFileSync(outputPath, jekyllContent);
  
  console.log(`Created Jekyll collection file for ${datasetId} at ${outputPath}`);
});

console.log('All dataset collection files generated successfully!'); 