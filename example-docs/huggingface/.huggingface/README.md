---
language:
- en
license: mit
annotations_creators:
- no-annotation
language_creators:
- found
pretty_name: Medium Articles Dataset
size_categories:
- n>1K
source_datasets:
- original
task_categories:
- text-classification
- text-generation
task_ids:
- topic-classification
- language-modeling
tags:
- medium
- articles
- blog-posts
dataset_info:
  features:
    - name: text
      dtype: string
    - name: title
      dtype: string
    - name: url
      dtype: string
---

# Medium Articles Dataset

## Dataset Description

### Dataset Summary

This dataset is a comprehensive collection of Medium articles, combining and normalizing data from multiple sources on both Kaggle and Hugging Face. A key feature is that all entries in the `text` column are unique - there are no duplicate articles in the final dataset.

### Languages

The dataset primarily contains articles in English.

### Dataset Structure

The dataset is provided in Parquet format with unique entries in the text column.

### Data Fields

- `text`: The main content of the article (unique across the dataset)
- `title`: The title of the article (if available in source dataset)
- `url`: URL of the original article (if available in source dataset)
- Additional fields may vary based on source datasets

### Dataset Creation

This dataset was created by combining and normalizing multiple existing datasets from Kaggle and Hugging Face. The process includes:
1. Downloading source datasets
2. Normalizing data format
3. Removing duplicate articles based on text content
4. Handling missing values
5. Converting to Parquet format

### Source Data

#### Kaggle Sources:
- aiswaryaramachandran/medium-articles-with-content
- hsankesara/medium-articles
- meruvulikith/1300-towards-datascience-medium-articles-dataset

#### Hugging Face Sources:
- fabiochiu/medium-articles
- Falah/medium_articles_posts

### Licensing Information

This dataset is released under MIT License.

### Citation Information

If you use this dataset in your research, please cite:

```bibtex
@dataset{medium_articles_2025,
  author = {Alaamer},
  title = {Medium Articles Dataset},
  year = {2025},
  publisher = {Hugging Face},
  journal = {Hugging Face Data Repository},
  howpublished = {\url{https://huggingface.co/datasets/Alaamer/medium-articles-posts-with-content}}
}
```

### Contributions

Thanks to all the original dataset creators and contributors. Contributions are welcome via pull requests.
