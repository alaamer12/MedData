# 🚀 MedData Engineering Hub

[![GitHub stars](https://img.shields.io/github/stars/Alaamer/meddata?style=social)](https://github.com/alaamer12/meddata/stargazers)
[![HuggingFace](https://img.shields.io/badge/🤗%20Hugging%20Face-Datasets-yellow)](https://huggingface.co/Alaamer)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Website](https://img.shields.io/badge/Website-Live-green)](https://meddata.ai)

A premier data engineering hub providing comprehensive datasets for machine learning and data science research. Our datasets include rich collections from Medium and Dev.to, perfect for NLP, content analysis, and research applications.

## 📊 Available Datasets

### Medium Articles Dataset
- **Size**: 500K+ articles
- **Content**: Full articles with rich metadata
- **Features**: Author info, claps, responses, tags
- **Use Cases**: NLP, content analysis, recommendation systems
- **Access**: [Dataset Page](https://meddata.ai/dataset/medium) | [Hugging Face](https://huggingface.co/datasets/Alaamer/medium-articles-posts-with-content)

### Dev.to Articles Dataset (Coming Soon)
- **Status**: In development
- **Expected**: Q2 2025
- **Features**: Technical articles, code snippets, community metrics
- **Preview**: [Dataset Preview](https://meddata.ai/dataset/devto)

## 🛠️ Quick Start

### Installation
```bash
# Install Python dependencies
pip install -r requirements.txt

# For website development
gem install bundler
bundle install
```

### Usage Example
```python
from datasets import load_dataset

# Load Medium Articles Dataset
dataset = load_dataset("Alaamer/medium-articles-posts-with-content")

# Basic usage
for article in dataset['train']:
    print(f"Title: {article['title']}")
    print(f"Author: {article['author']['name']}")
    print(f"Claps: {article['claps']}")
    print("---")
```

## 🌟 Features

### Data Quality
- ✨ Clean, normalized data
- 🔍 Rich metadata
- 📈 Regular updates
- 🔒 Quality assurance

### Integration
- 🤗 Hugging Face compatibility
- 🐍 Python ecosystem support
- 📦 Easy-to-use client library
- 🔌 RESTful API access

### Documentation
- 📚 Comprehensive guides
- 💡 Usage examples
- 🎯 Best practices
- 🔧 API reference

## 📖 Documentation

Visit our [Documentation Hub](docs/README.md) for:
- Getting Started Guide
- Dataset Management
- Website Development
- Best Practices
- Use Cases

## 🗺️ Project Structure

```
meddata/
├── _config.yml                    # Jekyll configuration
├── _datasets/                     # Dataset definitions (collection)
│   ├── medium.yml                 # Medium dataset configuration
│   └── devto.yml                  # Dev.to dataset configuration
├── _layouts/                      # Jekyll templates
├── _includes/                     # Reusable components
├── assets/                        # Static assets
├── scripts/                       # Automation scripts
├── _data/                         # Jekyll data files
├── docs/                          # Documentation
└── dataset/                       # Dataset pages (generated)
```

## 🤖 CLI Tool

The MedData CLI tool provides commands for managing datasets:

```bash
# Initialize a new dataset
python meddata.py init <dataset_id> "<Dataset Name>" "Short description"

# Process a dataset
python meddata.py process <dataset_id>

# Generate documentation
python meddata.py docs <dataset_id>

# Generate assets
python meddata.py assets <dataset_id>

# Build and serve website locally
python meddata.py site --serve
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](docs/CONTRIBUTING.md) for details on how to contribute.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- [Website](https://meddata.ai)
- [Documentation](docs/README.md)
- [GitHub Repository](https://github.com/alaamer12/meddata)
- [Hugging Face](https://huggingface.co/Alaamer)
- [Issue Tracker](https://github.com/alaamer12/meddata/issues)

---

<p align="center">Made with ❤️ by the MedData team</p>
