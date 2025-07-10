---
layout: dataset
title: Medium Articles Dataset
description: A comprehensive collection of Medium articles with rich metadata
id: medium
status: published
release_date: 2023-01-15T00:00:00.000Z
expected_update: quarterly
logo:
  text: M
  background: circle
  colors:
    primary: '#6366f1'
    secondary: '#14b8a6'
stats:
  - value: 500K+
    label: Articles
  - value: 10+
    label: Fields
  - value: 100%
    label: Unique Entries
sources:
  - platform: kaggle
    dataset: aiswaryaramachandran/medium-articles-with-content
    file: Medium_AggregatedData.csv
  - platform: huggingface
    dataset: fabiochiu/medium-articles
publishing:
  - platform: huggingface
    repository: Alaamer/medium-articles-posts-with-content
    url: https://huggingface.co/datasets/Alaamer/medium-articles-posts-with-content
  - platform: github
    repository: alaamer12/medium-articles-dataset
    url: https://github.com/alaamer12/medium-articles-dataset
features:
  - icon: 🔍
    title: Rich Metadata
    description: >-
      Each article comes with comprehensive metadata including title, subtitle,
      author, publication, claps, and more.
  - icon: 📊
    title: Clean & Normalized
    description: >-
      Data is thoroughly cleaned, normalized, and deduplicated for immediate use
      in your projects.
  - icon: 🚀
    title: Easy Integration
    description: >-
      Compatible with popular ML frameworks and available through Hugging Face's
      datasets library.
dataset_details:
  size: 4.8 GB
  file_format: CSV, JSON, Parquet
  splits:
    - name: train
      records: 487,692
    - name: validation
      records: 12,308
  schema:
    - name: title
      type: string
      description: The title of the article
      nullable: false
    - name: subtitle
      type: string
      description: The subtitle or description of the article
      nullable: true
    - name: author
      type: string
      description: The name of the article's author
      nullable: false
    - name: publication
      type: string
      description: The name of the publication the article belongs to
      nullable: true
    - name: date
      type: datetime
      description: The publication date of the article
      nullable: false
    - name: url
      type: string
      description: The URL of the article
      nullable: false
    - name: content
      type: string
      description: The full text content of the article
      nullable: false
    - name: claps
      type: integer
      description: Number of claps (likes) the article received
      nullable: true
    - name: reading_time
      type: float
      description: Estimated reading time in minutes
      nullable: true
    - name: topics
      type: list[string]
      description: List of topics/tags associated with the article
      nullable: true
  statistics:
    avg_content_length: 4,256 words
    avg_reading_time: 12.3 minutes
    top_topics:
      - Data Science
      - Machine Learning
      - Programming
      - Technology
      - AI
    language_distribution:
      - English: 92%
      - Spanish: 3%
      - French: 2%
      - Other: 3%
  preprocessing:
    - Removed duplicate articles based on URL and content similarity
    - Cleaned HTML tags and special characters from content
    - Normalized dates to ISO format
    - Extracted topics from article metadata
    - Calculated reading time based on word count
---
