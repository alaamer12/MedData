---
layout: home
title: MedData Engineering Hub
description: A premier data engineering hub providing comprehensive datasets for machine learning and data science research
---

<section id="datasets" class="datasets">
  <div class="container">
    <div class="section-header">
      <h2>Available Datasets [_blank 2]</h2>
      <p class="section-subtitle">Explore our curated collection of high-quality datasets</p>
    </div>
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
    <div class="section-header">
      <h2>Why Choose Our Datasets?</h2>
      <p class="section-subtitle">Built for researchers, by researchers</p>
    </div>
    <div class="feature-grid">
      <div class="feature-card reveal">
        <div class="feature-icon-wrapper">
          <span class="feature-icon">✨</span>
        </div>
        <h3>Data Quality</h3>
        <p>Clean, normalized data with rich metadata and regular updates. Our datasets undergo thorough quality assurance checks to ensure reliability and accuracy.</p>
      </div>
      <div class="feature-card reveal">
        <div class="feature-icon-wrapper">
          <span class="feature-icon">🤗</span>
        </div>
        <h3>Easy Integration</h3>
        <p>Fully compatible with Hugging Face's datasets library and the Python ecosystem for seamless integration into your machine learning projects.</p>
      </div>
      <div class="feature-card reveal">
        <div class="feature-icon-wrapper">
          <span class="feature-icon">📚</span>
        </div>
        <h3>Comprehensive Documentation</h3>
        <p>Detailed documentation with usage examples, best practices, and API references to get you started quickly and efficiently.</p>
      </div>
    </div>
  </div>
</section>

<section class="workflow-section">
  <div class="container">
    <div class="section-header">
      <h2>How It Works</h2>
      <p class="section-subtitle">Get started in three simple steps</p>
    </div>
    <div class="workflow-steps">
      <div class="workflow-step reveal">
        <div class="step-number">1</div>
        <div class="step-content">
          <h3>Browse Datasets</h3>
          <p>Explore our collection of high-quality, curated datasets for machine learning and data science research.</p>
        </div>
      </div>
      <div class="workflow-step reveal">
        <div class="step-number">2</div>
        <div class="step-content">
          <h3>Import Data</h3>
          <p>Easily import datasets into your projects using Hugging Face's datasets library or direct downloads.</p>
        </div>
      </div>
      <div class="workflow-step reveal">
        <div class="step-number">3</div>
        <div class="step-content">
          <h3>Build & Deploy</h3>
          <p>Focus on building your models and applications with clean, ready-to-use data at your fingertips.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="cta-section">
  <div class="container">
    <div class="cta-content">
      <h2>Ready to Get Started?</h2>
      <p>Join thousands of researchers and data scientists using our datasets to power their next breakthrough.</p>
      <div class="cta-buttons">
        <a href="#datasets" class="btn btn-primary">Browse Datasets</a>
        <a href="/about/" class="btn btn-secondary">Learn More</a>
      </div>
    </div>
  </div>
</section>