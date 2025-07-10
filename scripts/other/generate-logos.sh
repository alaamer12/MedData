#!/bin/bash

# Install required dependencies if not already installed
if ! command -v npm &> /dev/null; then
    echo "npm is required but not installed. Please install Node.js and npm."
    exit 1
fi

# Check if js-yaml is installed
if ! npm list -g js-yaml &> /dev/null; then
    echo "Installing js-yaml globally..."
    npm install -g js-yaml
fi

# Navigate to the project root directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

# Create assets/images directory if it doesn't exist
mkdir -p assets/images

# Run the logo generator script
echo "Generating dataset logos..."
node assets/js/generate-logos.js

echo "Logo generation complete!"
echo "Generated logos are in assets/images/"

# List generated logos
echo "Generated logos:"
ls -la assets/images/*-logo.svg 