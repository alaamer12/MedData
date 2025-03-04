# Medium Articles Dataset

## Dataset Description

This dataset contains articles from Medium, focusing on various topics and publications.

### Features
- id: Unique identifier for each article
- title: The title of the article
- text: The main content of the article
- url: The URL where the article was published
- publication: The name of the publication
- date: The publication date

## Usage

```python
from kaggle.api.kaggle_api_extended import KaggleApi
api = KaggleApi()
api.authenticate()
# Download and process dataset
```

## Citation

If you use this dataset, please cite:

```
@dataset{medium_articles_2025,
  author = {MedData Project},
  title = {Medium Articles Dataset},
  year = {2025},
  publisher = {Kaggle},
  version = {1.0.0}
}
```
