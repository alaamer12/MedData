---
layout: home
title: MedData Engineering Hub
description: A premier data engineering hub providing comprehensive datasets for machine learning and data science research
---

<section id="datasets" class="datasets">
  <div class="container">
    <h2>Available Datasets</h2>
    <div class="dataset-grid">
      {% for dataset_entry in site.data.datasets %}
        {% assign dataset = site.datasets | where: "id", dataset_entry.id | first %}
        {% if dataset %}
          {% include dataset-card.html dataset=dataset %}
        {% else %}
          {% include dataset-card.html dataset=dataset_entry %}
        {% endif %}
      {% endfor %}
    </div>
  </div>
</section>

<section class="features">
  <div class="container">
    <h2>Why Choose Our Datasets?</h2>
    <div class="feature-grid">
      <div class="feature-card reveal">
        <h3><span class="feature-icon">✨</span> Data Quality</h3>
        <p>Clean, normalized data with rich metadata and regular updates. Our datasets undergo thorough quality assurance checks.</p>
      </div>
      <div class="feature-card reveal">
        <h3><span class="feature-icon">🤗</span> Easy Integration</h3>
        <p>Fully compatible with Hugging Face's datasets library and the Python ecosystem for seamless integration into your projects.</p>
      </div>
      <div class="feature-card reveal">
        <h3><span class="feature-icon">📚</span> Comprehensive Documentation</h3>
        <p>Detailed documentation with usage examples, best practices, and API references to get you started quickly.</p>
      </div>
    </div>
  </div>
</section>

<section class="workflow-section">
  <div class="container">
    <h2>How It Works</h2>
    <div class="workflow-steps">
      <div class="workflow-step reveal">
        <div class="step-number">1</div>
        <h3>Browse Datasets</h3>
        <p>Explore our collection of high-quality, curated datasets for machine learning and data science.</p>
      </div>
      <div class="workflow-step reveal">
        <div class="step-number">2</div>
        <h3>Import Data</h3>
        <p>Easily import datasets into your projects using Hugging Face's datasets library or direct downloads.</p>
      </div>
      <div class="workflow-step reveal">
        <div class="step-number">3</div>
        <h3>Build & Deploy</h3>
        <p>Focus on building your models and applications with clean, ready-to-use data.</p>
      </div>
    </div>
  </div>
</section> 