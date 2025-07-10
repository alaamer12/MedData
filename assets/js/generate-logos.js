/**
 * Dataset Logo Generator
 * Generates SVG logos for datasets based on the template
 */

const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

// Paths
const DATASETS_DIR = path.join(__dirname, '../../_datasets');
const TEMPLATE_PATH = path.join(__dirname, '../templates/dataset-logo.svg');
const OUTPUT_DIR = path.join(__dirname, '../images');

// Ensure output directory exists
if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

// Read template
const template = fs.readFileSync(TEMPLATE_PATH, 'utf8');

// Process each dataset
const datasetFiles = fs.readdirSync(DATASETS_DIR).filter(file => file.endsWith('.yml'));

datasetFiles.forEach(file => {
  const datasetPath = path.join(DATASETS_DIR, file);
  const datasetContent = fs.readFileSync(datasetPath, 'utf8');
  const dataset = yaml.load(datasetContent);
  
  // Extract needed values
  const datasetId = dataset.id;
  const logoText = dataset.logo?.text || datasetId.charAt(0).toUpperCase();
  const primaryColor = dataset.logo?.colors?.primary || '#6366f1';
  const secondaryColor = dataset.logo?.colors?.secondary || '#14b8a6';
  
  // Replace placeholders in template
  let logoSvg = template
    .replace(/DATASET_ID_PLACEHOLDER/g, datasetId)
    .replace(/LOGO_TEXT_PLACEHOLDER/g, logoText)
    .replace(/PRIMARY_COLOR_PLACEHOLDER/g, primaryColor)
    .replace(/SECONDARY_COLOR_PLACEHOLDER/g, secondaryColor);
  
  // Write to file
  const outputPath = path.join(OUTPUT_DIR, `${datasetId}-logo.svg`);
  fs.writeFileSync(outputPath, logoSvg);
  
  console.log(`Generated logo for ${datasetId} at ${outputPath}`);
});

// Generate Jekyll logo for the site
const jekyllLogoSvg = template
  .replace(/DATASET_ID_PLACEHOLDER/g, 'jekyll')
  .replace(/LOGO_TEXT_PLACEHOLDER/g, 'J')
  .replace(/PRIMARY_COLOR_PLACEHOLDER/g, '#fc5d5d')
  .replace(/SECONDARY_COLOR_PLACEHOLDER/g, '#ff8a5b');

const jekyllLogoPath = path.join(OUTPUT_DIR, 'jekyll-logo.svg');
fs.writeFileSync(jekyllLogoPath, jekyllLogoSvg);
console.log(`Generated Jekyll logo at ${jekyllLogoPath}`);

console.log('All logos generated successfully!'); 