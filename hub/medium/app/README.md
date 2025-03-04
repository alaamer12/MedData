---
annotations_creators:
- no-annotation
language:
- en
language_creators:
- found
license: mit
multilinguality:
- monolingual
pretty_name: Medium Articles Dataset
size_categories:
- n>1K
source_datasets:
- original
tags:
- medium
- articles
- blog-posts
task_categories:
- text-classification
- text-generation
task_ids:
- topic-classification
- language-modeling
---

# Medium Articles Dataset Generator

This project combines multiple datasets from Kaggle and Hugging Face to create a comprehensive collection of Medium articles. The combined dataset is available on [Hugging Face Hub](https://huggingface.co/datasets/Alaamer/medium-articles-posts-with-content).

## Dataset Description

This dataset is a unique compilation that not only combines multiple sources but also ensures data quality through normalization and deduplication. A key feature is that all entries in the `text` column are unique - there are no duplicate articles in the final dataset.

### Data Sources:
#### Kaggle Sources:
- aiswaryaramachandran/medium-articles-with-content
- hsankesara/medium-articles
- meruvulikith/1300-towards-datascience-medium-articles-dataset

#### Hugging Face Sources:
- fabiochiu/medium-articles
- Falah/medium_articles_posts

## Features

- Combines multiple data sources into a single, unified dataset
- **Ensures uniqueness**: Each article appears only once in the dataset
- **Quality control**: 
  - Removes duplicate entries based on article text
  - Handles missing values
  - Normalizes data format
- Saves the final dataset in efficient Parquet format
- Publishes the dataset to Hugging Face Hub

## Requirements

```bash
pip install datasets
pip install kagglehub huggingface_hub tqdm
```

## Usage

1. Set up your Hugging Face authentication token
2. Run the script:
```bash
python combined_medium_ds_generator.py
```

## Data Processing Steps

1. Downloads datasets from Kaggle and Hugging Face
2. Normalizes each dataset by:
   - Removing null values
   - Eliminating duplicates
   - Standardizing column names
3. Combines all datasets into a single DataFrame
4. Saves the result as a Parquet file
5. Uploads the final dataset to Hugging Face Hub

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

- [@Alaamer](https://huggingface.co/Alaamer)

## Acknowledgments

Special thanks to the original dataset creators:
- aiswaryaramachandran
- hsankesara
- meruvulikith
- fabiochiu
- Falah
