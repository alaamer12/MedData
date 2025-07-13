
const { PurgeCSS } = require('purgecss');
const fs = require('fs');
const path = require('path');

async function runPurgeCSS() {
  const purgeCSSResult = await new PurgeCSS().purge({
    content: ['E:/Projects/Languages/Python/DataEngineering/MedData/**/*.html'],
    css: ['E:/Projects/Languages/Python/DataEngineering/MedData/assets/css/*.css'],
  });

  const outputDir = 'E:/Projects/Languages/Python/DataEngineering/MedData/assets/css/purged';
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  purgeCSSResult.forEach(result => {
    const filePath = path.join(outputDir, path.basename(result.file));
    fs.writeFileSync(filePath, result.css);
    console.log(`Successfully purged ${result.file} and saved to ${filePath}`);
  });
}

runPurgeCSS().catch(console.error);
