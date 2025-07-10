---
layout: dataset
title: Medium Articles Dataset
description: A comprehensive collection of Medium articles with rich metadata
canonical_url: https://huggingface.co/datasets/Alaamer/medium-articles-posts-with-content
---

{% assign dataset_file = site.datasets | where: "id", "medium" | first %}
{% if dataset_file %}
  {% include dataset-content.html dataset=dataset_file %}
{% else %}
  {% assign dataset_data = site.data.datasets | where: "id", "medium" | first %}
  {% assign dataset_config = site.data.medium %}
  {% if dataset_config %}
    {% include dataset-content.html dataset=dataset_config %}
  {% else %}
    <div class="error-message">
      <p>Dataset configuration not found. Please check that <code>_datasets/medium.yml</code> exists and is properly formatted.</p>
    </div>
  {% endif %}
{% endif %} 