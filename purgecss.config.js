const path = require('path');

module.exports = {
  content: [path.resolve(__dirname, '**/*.html')],
  css: [path.resolve(__dirname, 'assets/css/*.css')],
  output: path.resolve(__dirname, 'assets/css/purged')
};