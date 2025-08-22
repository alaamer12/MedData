
/**
 * Dynamic Favicon Updater
 * Updates the page favicon and title based on the current dataset
 */

class FaviconUpdater {
  constructor() {
    this.defaultFavicon = '/assets/images/favicon.svg';
    this.defaultTitle = 'MedData Engineering Hub';
    this.init();
  }

  init() {
    // Update favicon on page load
    this.updateFavicon();
    
    // Listen for navigation changes (for SPAs or dynamic content)
    window.addEventListener('popstate', () => {
      setTimeout(() => this.updateFavicon(), 100);
    });
    
    // Also listen for any dataset page updates
    document.addEventListener('DOMContentLoaded', () => {
      this.updateFavicon();
    });
  }

  getCurrentDatasetId() {
    // Try to get dataset ID from URL path
    const path = window.location.pathname;
    const match = path.match(/\/dataset\/([^\/]+)/);
    if (match) {
      return match[1];
    }
    
    // Try to get from meta tags or page data
    const metaDataset = document.querySelector('meta[name="dataset-id"]');
    if (metaDataset) {
      return metaDataset.getAttribute('content');
    }
    
    // Try to get from body class or data attributes
    const body = document.body;
    if (body.classList.contains('dataset-page')) {
      const datasetClass = Array.from(body.classList).find(cls => cls.startsWith('dataset-'));
      if (datasetClass) {
        return datasetClass.replace('dataset-', '');
      }
    }
    
    return null;
  }

  async checkImageExists(url) {
    return new Promise((resolve) => {
      const img = new Image();
      img.onload = () => resolve(true);
      img.onerror = () => resolve(false);
      img.src = url;
    });
  }

  async updateFavicon() {
    const datasetId = this.getCurrentDatasetId();
    
    if (datasetId) {
      const datasetFavicon = `/assets/images/${datasetId}-logo.svg`;
      
      // Check if dataset favicon exists
      const exists = await this.checkImageExists(datasetFavicon);
      
      if (exists) {
        this.setFavicon(datasetFavicon);
        this.updatePageTitle(datasetId);
      } else {
        // Fallback to default favicon
        this.setFavicon(this.defaultFavicon);
        this.updatePageTitle();
      }
    } else {
      // Use default favicon for non-dataset pages
      this.setFavicon(this.defaultFavicon);
      this.updatePageTitle();
    }
  }

  setFavicon(faviconUrl) {
    // Remove existing favicon links
    const existingLinks = document.querySelectorAll('link[rel*="icon"]');
    existingLinks.forEach(link => link.remove());
    
    // Add new favicon link
    const link = document.createElement('link');
    link.rel = 'icon';
    link.type = 'image/svg+xml';
    link.href = faviconUrl;
    document.head.appendChild(link);
    
    // Add apple-touch-icon as well
    const appleLink = document.createElement('link');
    appleLink.rel = 'apple-touch-icon';
    appleLink.href = faviconUrl;
    document.head.appendChild(appleLink);
  }

  updatePageTitle(datasetId = null) {
    if (datasetId) {
      // Try to get dataset name from page content
      const datasetHeader = document.querySelector('.dataset-header h1');
      const datasetName = datasetHeader ? datasetHeader.textContent.trim() : this.formatDatasetName(datasetId);
      document.title = `${datasetName} | ${this.defaultTitle}`;
    } else {
      // Keep existing title or use default
      if (!document.title.includes(this.defaultTitle)) {
        const currentTitle = document.title;
        document.title = currentTitle ? `${currentTitle} | ${this.defaultTitle}` : this.defaultTitle;
      }
    }
  }

  formatDatasetName(datasetId) {
    // Convert dataset ID to readable name
    return datasetId
      .split('-')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  }
}

// Initialize the favicon updater
if (typeof window !== 'undefined') {
  window.faviconUpdater = new FaviconUpdater();
}
