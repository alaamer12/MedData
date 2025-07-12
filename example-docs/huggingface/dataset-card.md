# Medium Articles Dataset

## Dataset Description

### Dataset Summary

This dataset is a comprehensive collection of Medium articles, combining and normalizing data from multiple sources on both Kaggle and Hugging Face. The dataset ensures uniqueness of articles by removing duplicates based on article text content.

### Languages

The dataset primarily contains articles in English.

### Dataset Structure

The dataset is provided in Parquet format with unique entries in the text column.

### Data Fields

- `text`: The main content of the article
- Additional fields may vary based on source datasets

### Dataset Creation

This dataset was created by combining and normalizing multiple existing datasets from Kaggle and Hugging Face. The process includes:
1. Downloading source datasets
2. Normalizing data format
3. Removing duplicate articles
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

If you use this dataset in your research, please cite it using the citation information in the CITATION.cff file.

### Contributions

Thanks to all the original dataset creators and contributors. Contributions are welcome via pull requests.
