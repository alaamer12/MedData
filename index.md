---
layout: home
title: MedData Engineering Hub
description: A premier data engineering hub providing comprehensive datasets for machine learning and data science research
---

<section id="datasets" class="datasets">
  <div class="container">
    <div class="section-header">
      <h2>Available Datasets [_blank 5]</h2>
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
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feature-icon"><polyline points="20 6 9 17 4 12"></polyline></svg>
        </div>
        <h3>Data Quality</h3>
        <p>Clean, normalized data with rich metadata and regular updates. Our datasets undergo thorough quality assurance checks to ensure reliability and accuracy.</p>
      </div>
      <div class="feature-card reveal">
        <div class="feature-icon-wrapper">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feature-icon"><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h7"></path><path d="M18 12h-5V7"></path><path d="M18 7l5 5-5 5"></path></svg>
        </div>
        <h3>Easy Integration</h3>
        <p>Fully compatible with Hugging Face's datasets library and the Python ecosystem for seamless integration into your machine learning projects.</p>
      </div>
      <div class="feature-card reveal">
        <div class="feature-icon-wrapper">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feature-icon"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>
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
