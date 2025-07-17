// Initialize Highlight.js
  hljs.highlightAll();

  // Smooth scrolling for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });

  // Add reveal animation to sections
  const revealElements = document.querySelectorAll('.reveal');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('active');
      }
    });
  });

  revealElements.forEach(el => observer.observe(el));

  // Scroll progress indicator
  function updateScrollProgress() {
    const scrollTop = window.pageYOffset;
    const docHeight = document.body.offsetHeight - window.innerHeight;
    const scrollPercent = (scrollTop / docHeight) * 100;

    // Create or update progress bar
    let progressBar = document.querySelector('.scroll-progress');
    if (!progressBar) {
      progressBar = document.createElement('div');
      progressBar.className = 'scroll-progress';
      document.body.appendChild(progressBar);
    }

    progressBar.style.width = Math.min(scrollPercent, 100) + '%';
  }

  // Add scroll event listener for progress bar
  window.addEventListener('scroll', updateScrollProgress);

  // Enhanced hover effects for cards
  const cards = document.querySelectorAll('.offering-item, .sidebar-card, .contact-method');
  cards.forEach(card => {
    card.addEventListener('mouseenter', function() {
      this.style.transform = 'translateY(-5px) scale(1.02)';
    });

    card.addEventListener('mouseleave', function() {
      this.style.transform = 'translateY(0) scale(1)';
    });
  });

  // Animate stats numbers
  const statNumbers = document.querySelectorAll('.stat-number');
  const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const target = entry.target;
        const finalValue = target.textContent;
        const isNumber = /^\d+\+?$/.test(finalValue);

        if (isNumber) {
          const numValue = parseInt(finalValue.replace('+', ''));
          const hasPlus = finalValue.includes('+');
          let current = 0;
          const increment = numValue / 50;

          const timer = setInterval(() => {
            current += increment;
            if (current >= numValue) {
              target.textContent = numValue + (hasPlus ? '+' : '');
              clearInterval(timer);
            } else {
              target.textContent = Math.floor(current) + (hasPlus ? '+' : '');
            }
          }, 30);
        }

        statsObserver.unobserve(target);
      }
    });
  });

  statNumbers.forEach(stat => statsObserver.observe(stat));
});