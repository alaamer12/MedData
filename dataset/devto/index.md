---
layout: dataset
title: Dev.to Articles Dataset
description: A comprehensive collection of technical articles from Dev.to with code snippets and rich metadata
canonical_url: https://huggingface.co/datasets/Alaamer/devto-articles-with-code
---

{% assign dataset_file = site.datasets | where: "id", "devto" | first %}
{% if dataset_file %}
  {% include dataset-content.html dataset=dataset_file %}
{% else %}
  {% assign dataset_data = site.data.datasets | where: "id", "devto" | first %}
  {% assign dataset_config = site.data.devto %}
  {% if dataset_config %}
    {% include dataset-content.html dataset=dataset_config %}
  {% else %}
    <div class="error-message">
      <p>Dataset configuration not found. Please check that <code>_datasets/devto.yml</code> exists and is properly formatted.</p>
    </div>
  {% endif %}
{% endif %} 