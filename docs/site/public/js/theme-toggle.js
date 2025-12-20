// Theme Toggle Functionality
(function() {
  const themeToggle = document.getElementById('theme-toggle');
  const html = document.documentElement;

  if (!themeToggle) {
    console.warn('Theme toggle button not found');
    return;
  }

  // Check for saved theme preference or default to 'dark'
  let currentTheme = localStorage.getItem('theme') || 'dark';
  html.setAttribute('data-theme', currentTheme);
  updateThemeIcon(currentTheme);

  // Toggle theme on button click
  themeToggle.addEventListener('click', () => {
    const currentTheme = html.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

    html.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);

    // Dispatch custom event for other components (e.g., Mermaid diagrams)
    const themeChangeEvent = new CustomEvent('themechange', {
      detail: { theme: newTheme }
    });
    window.dispatchEvent(themeChangeEvent);
  });

  // Update icon based on theme
  function updateThemeIcon(theme) {
    const icon = themeToggle.querySelector('.theme-icon');
    if (icon) {
      // Moon icon for dark mode (clicking will switch to light)
      // Sun icon for light mode (clicking will switch to dark)
      icon.textContent = theme === 'dark' ? '☀️' : '🌙';
      themeToggle.setAttribute('aria-label', `Switch to ${theme === 'dark' ? 'light' : 'dark'} theme`);
    }
  }

  // Respect prefers-color-scheme on first visit (if no saved preference)
  if (!localStorage.getItem('theme')) {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const initialTheme = prefersDark ? 'dark' : 'light';
    html.setAttribute('data-theme', initialTheme);
    localStorage.setItem('theme', initialTheme);
    updateThemeIcon(initialTheme);
  }

  // Listen for system theme changes (when user hasn't set a preference)
  const darkModeQuery = window.matchMedia('(prefers-color-scheme: dark)');
  darkModeQuery.addEventListener('change', (e) => {
    // Only update if user hasn't manually set a preference
    if (!localStorage.getItem('theme-user-set')) {
      const newTheme = e.matches ? 'dark' : 'light';
      html.setAttribute('data-theme', newTheme);
      localStorage.setItem('theme', newTheme);
      updateThemeIcon(newTheme);
    }
  });

  // Mark that user has set a preference when they click the toggle
  themeToggle.addEventListener('click', () => {
    localStorage.setItem('theme-user-set', 'true');
  }, { once: true });
})();
