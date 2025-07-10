---
layout: home
title: MedData Engineering Hub
description: A premier data engineering hub providing comprehensive datasets for machine learning and data science research
---

<section id="datasets" class="datasets">
  <div class="container">
    <h2>Available Datasets</h2>
    <div class="dataset-grid">
      {% for dataset in site.data.datasets %}
        {% include dataset-card.html dataset=dataset %}
      {% endfor %}
    </div>
  </div>
</section>

<section class="features">
  <div class="container">
    <h2>Why Choose Our Datasets?</h2>
    <div class="feature-grid">
      <div class="feature-card">
        <h3>✨ Data Quality</h3>
        <p>Clean, normalized data with rich metadata and regular updates. Our datasets undergo thorough quality assurance checks.</p>
      </div>
      <div class="feature-card">
        <h3>🤗 Easy Integration</h3>
        <p>Fully compatible with Hugging Face's datasets library and the Python ecosystem for seamless integration into your projects.</p>
      </div>
      <div class="feature-card">
        <h3>📚 Comprehensive Documentation</h3>
        <p>Detailed documentation with usage examples, best practices, and API references to get you started quickly.</p>
      </div>
    </div>
  </div>
</section> 