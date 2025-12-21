// Mobile Menu Toggle
document.addEventListener('DOMContentLoaded', () => {
  const mobileToggle = document.getElementById('mobile-menu-toggle');
  const sidebar = document.querySelector('.sidebar-left');
  const overlay = document.getElementById('mobile-overlay');

  if (mobileToggle && sidebar && overlay) {
    mobileToggle.addEventListener('click', () => {
      mobileToggle.classList.toggle('active');
      sidebar.classList.toggle('mobile-open');
      overlay.classList.toggle('active');
    });

    // Close mobile menu when clicking overlay
    overlay.addEventListener('click', () => {
      mobileToggle.classList.remove('active');
      sidebar.classList.remove('mobile-open');
      overlay.classList.remove('active');
    });

    // Close mobile menu when clicking a link
    sidebar.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        mobileToggle.classList.remove('active');
        sidebar.classList.remove('mobile-open');
        overlay.classList.remove('active');
      });
    });
  }
});

// Collapsible Sidebar Sections
function toggleSection(sectionId) {
  const content = document.getElementById(sectionId);
  if (!content) return;

  const header = content.previousElementSibling;
  const icon = header ? header.querySelector('.section-icon') : null;

  if (content.style.display === 'none' || content.classList.contains('collapsed')) {
    content.style.display = 'flex';
    content.classList.remove('collapsed');
    if (icon) icon.textContent = '▼';
    localStorage.setItem(`nav-${sectionId}`, 'open');
  } else {
    content.style.display = 'none';
    content.classList.add('collapsed');
    if (icon) icon.textContent = '▶';
    localStorage.setItem(`nav-${sectionId}`, 'closed');
  }
}

// Restore Navigation State from localStorage
document.addEventListener('DOMContentLoaded', () => {
  // Start with all sections collapsed by default
  document.querySelectorAll('.section-content').forEach(section => {
    const sectionId = section.id;
    if (!sectionId) return;

    const state = localStorage.getItem(`nav-${sectionId}`);
    const header = section.previousElementSibling;
    const icon = header ? header.querySelector('.section-icon') : null;

    // Default to collapsed unless explicitly saved as open
    if (state === 'open') {
      section.style.display = 'flex';
      section.classList.remove('collapsed');
      if (icon) icon.textContent = '▼';
    } else {
      section.style.display = 'none';
      section.classList.add('collapsed');
      if (icon) icon.textContent = '▶';
    }
  });

  // Always expand section containing current page (active link), overriding saved state
  const activeLink = document.querySelector('.sidebar-link.active, .subsection-link.active, .nested-link.active');
  if (activeLink) {
    let parent = activeLink.closest('.section-content');
    while (parent) {
      parent.style.display = 'flex';
      parent.classList.remove('collapsed');
      const header = parent.previousElementSibling;
      const icon = header ? header.querySelector('.section-icon') : null;
      if (icon) icon.textContent = '▼';

      // Move up to next parent section
      parent = parent.parentElement.closest('.section-content');
    }
  }
});

// Smooth Scrolling for Anchor Links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const targetId = this.getAttribute('href');
    const target = document.querySelector(targetId);
    if (target) {
      target.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
      // Update URL without triggering page reload
      history.pushState(null, null, targetId);
    }
  });
});

// Highlight active TOC link on scroll
let ticking = false;
function updateTOCActive() {
  const headings = document.querySelectorAll('.main-content h1[id], .main-content h2[id], .main-content h3[id]');
  const tocLinks = document.querySelectorAll('.toc-link');

  let currentActiveId = null;
  const scrollPos = window.scrollY + 100; // Offset for navbar

  // Find the current heading in view
  headings.forEach(heading => {
    if (heading.offsetTop <= scrollPos) {
      currentActiveId = heading.id;
    }
  });

  // Update active state
  tocLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (href === `#${currentActiveId}`) {
      link.classList.add('active');
    } else {
      link.classList.remove('active');
    }
  });

  ticking = false;
}

// Throttle scroll event
window.addEventListener('scroll', () => {
  if (!ticking) {
    window.requestAnimationFrame(() => {
      updateTOCActive();
    });
    ticking = true;
  }
});

// Initial TOC update
document.addEventListener('DOMContentLoaded', updateTOCActive);
