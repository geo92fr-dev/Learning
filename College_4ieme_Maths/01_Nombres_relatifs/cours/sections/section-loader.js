// Module loader for section inclusion
function loadSection(sectionPath, targetId) {
  return fetch(sectionPath)
    .then(response => response.text())
    .then(html => {
      const target = document.getElementById(targetId);
      if (target) {
        target.innerHTML = html;
      }
    })
    .catch(error => console.warn('Section load failed:', sectionPath, error));
}

// Load CSS module
function loadCSS(cssPath) {
  const link = document.createElement('link');
  link.rel = 'stylesheet';
  link.href = cssPath;
  document.head.appendChild(link);
}

// Initialize modular sections
document.addEventListener('DOMContentLoaded', function() {
  // Load memo styles
  loadCSS('sections/memo-styles.css');
  
  // Replace corrupted retention section if it exists
  const retentionSection = document.querySelector('.sous-section-erreurs h3');
  if (retentionSection && retentionSection.textContent.includes('Ce qu\'il faut retenir')) {
    loadSection('sections/regles-retention.html', retentionSection.parentElement.id || 'retention-target');
  }
});