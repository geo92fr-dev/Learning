/* =============================================================================
   APP.JS - Navigation Robuste & Gestion d''État
    CONTRÔLEUR PRINCIPAL DE L''APPLICATION
   ============================================================================= */

//  État global de l'utilisateur
const userState = {
  sectionsCompleted: new Set(),
  quizPassed: new Set(),
  currentSection: 'intro',
  startTime: Date.now(),
  sessionStats: {
    sectionsVisited: new Set(),
    quizAttempts: 0,
    quizSuccesses: 0
  }
};

//  Initialisation complète dans DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
  console.log(' Démarrage de l''application...');
  initializeApp();
});

//  Initialisation principale
function initializeApp() {
  try {
    // Vérification de l'intégrité du DOM
    const sections = document.querySelectorAll('[data-section]');
    const navButtons = document.querySelectorAll('nav button');
    
    if (sections.length === 0) {
      console.error(' Aucune section trouvée avec [data-section]');
      showAppError('Aucune section de contenu trouvée');
      return;
    }
    
    console.log(` ${sections.length} sections détectées`);
    
    if (navButtons.length === 0) {
      console.warn(' Aucun bouton de navigation trouvé');
    }
    
    // Initialisation des composants
    setupNavigation();
    setupProgressBar();
    setupKeyboardNavigation();
    
    // Section par défaut
    showSection('intro');
    
    // Statistiques initiales
    logAppStats();
    
    console.log(' Application initialisée avec succès');
    
  } catch (error) {
    console.error(' Erreur critique d''initialisation:', error);
    showAppError('Erreur d''initialisation de l''application');
  }
}

//  Configuration de la navigation
function setupNavigation() {
  const navButtons = document.querySelectorAll('nav button');
  
  navButtons.forEach(button => {
    // Récupérer l'ID de section depuis onclick existant
    const onclick = button.getAttribute('onclick');
    if (onclick) {
      const sectionMatch = onclick.match(/showSection\([''"]([^''"]+)[''"]\)/);
      if (sectionMatch) {
        const sectionId = sectionMatch[1];
        
        // Remplacer par gestionnaire d'événement propre
        button.removeAttribute('onclick');
        button.onclick = (e) => {
          e.preventDefault();
          showSection(sectionId);
        };
        
        // Ajouter attribut data pour identification
        button.dataset.section = sectionId;
        
        console.log(` Navigation configurée: bouton  ${sectionId}`);
      }
    }
  });
}

//  Configuration de la barre de progression
function setupProgressBar() {
  const progressContainer = document.querySelector('.progress-container');
  
  if (!progressContainer) {
    // Créer barre de progression si manquante
    const nav = document.querySelector('nav');
    if (nav) {
      const progressHTML = `
        <div class="progress-container">
          <div class="progress-bar" style="width: 0%;">0% - Commencez !</div>
        </div>
      `;
      nav.insertAdjacentHTML('afterend', progressHTML);
      console.log(' Barre de progression créée');
    }
  }
  
  updateProgress(); // Mise à jour initiale
}

//  Navigation au clavier
function setupKeyboardNavigation() {
  document.addEventListener('keydown', (e) => {
    // Alt + numéro pour navigation rapide
    if (e.altKey && e.key >= '1' && e.key <= '9') {
      const sections = Array.from(document.querySelectorAll('[data-section]'));
      const index = parseInt(e.key) - 1;
      
      if (sections[index]) {
        const sectionId = sections[index].dataset.section;
        showSection(sectionId);
        console.log(` Navigation clavier vers: ${sectionId}`);
      }
    }
    
    // Échap pour retour au début
    if (e.key === 'Escape') {
      showSection('intro');
    }
  });
}

//  Navigation entre sections avec validation
function showSection(sectionId) {
  console.log(` Navigation demandée vers: ${sectionId}`);
  
  const targetSection = document.querySelector(`[data-section="${sectionId}"]`);
  
  if (!targetSection) {
    console.error(` Section introuvable: ${sectionId}`);
    showNotification(`Section "${sectionId}" introuvable`, 'error');
    return;
  }
  
  // Sauvegarder section précédente
  const previousSection = userState.currentSection;
  
  // Activer/désactiver sections avec classes CSS
  document.querySelectorAll('[data-section]').forEach(section => {
    const isActive = section.dataset.section === sectionId;
    section.classList.toggle('active', isActive);
  });
  
  // Mettre à jour navigation
  document.querySelectorAll('nav button').forEach(btn => {
    const isActive = btn.dataset.section === sectionId;
    btn.classList.toggle('active', isActive);
  });
  
  // Mettre à jour état utilisateur
  userState.currentSection = sectionId;
  userState.sessionStats.sectionsVisited.add(sectionId);
  
  // Auto-marquer section précédente comme complétée
  if (previousSection && previousSection !== sectionId && previousSection !== 'intro') {
    markSectionComplete(previousSection);
  }
  
  // Scroll vers le haut
  window.scrollTo({ top: 0, behavior: 'smooth' });
  
  console.log(` Navigation réussie: ${previousSection}  ${sectionId}`);
  
  // Mettre à jour progression
  updateProgress();
}

//  Marquer une section comme complétée
function markSectionComplete(sectionId) {
  if (userState.sectionsCompleted.has(sectionId)) return;
  
  userState.sectionsCompleted.add(sectionId);
  updateProgress();
  
  console.log(` Section complétée: ${sectionId}`);
  showNotification(`Section "${sectionId}" terminée !`, 'success');
}

//  Marquer un quiz comme réussi (appelé depuis quiz.js)
function markQuizComplete(quizKey) {
  if (userState.quizPassed.has(quizKey)) return;
  
  userState.quizPassed.add(quizKey);
  userState.sessionStats.quizSuccesses++;
  
  updateProgress();
  
  console.log(` Quiz réussi: ${quizKey}`);
  
  // Encouragement spécial si tous les quiz d'une section sont réussis
  checkSectionCompletion();
}

//  Vérifier si une section est entièrement complétée
function checkSectionCompletion() {
  const currentSectionElement = document.querySelector(`[data-section="${userState.currentSection}"]`);
  if (!currentSectionElement) return;
  
  const sectionQuiz = currentSectionElement.querySelectorAll('.quiz');
  const sectionQuizKeys = Array.from(sectionQuiz).map(q => q.dataset.key);
  
  const allCompleted = sectionQuizKeys.every(key => 
    key && userState.quizPassed.has(key)
  );
  
  if (allCompleted && sectionQuizKeys.length > 0) {
    markSectionComplete(userState.currentSection);
    showNotification(` Parfait ! Tous les quiz de cette section sont réussis !`, 'celebration');
  }
}

//  Mise à jour de la barre de progression
function updateProgress() {
  const totalSections = document.querySelectorAll('[data-section]').length;
  const totalQuiz = Object.keys(typeof QUIZ_CONFIG !== 'undefined' ? QUIZ_CONFIG : {}).length;
  
  const sectionsCompleted = userState.sectionsCompleted.size;
  const quizCompleted = userState.quizPassed.size;
  
  // Calcul: 40% sections + 60% quiz (les quiz sont plus importants)
  const sectionProgress = totalSections > 0 ? (sectionsCompleted / totalSections) * 40 : 0;
  const quizProgress = totalQuiz > 0 ? (quizCompleted / totalQuiz) * 60 : 0;
  const overallProgress = Math.round(sectionProgress + quizProgress);
  
  const progressBar = document.querySelector('.progress-bar');
  if (progressBar) {
    progressBar.style.width = `${overallProgress}%`;
    progressBar.textContent = `${overallProgress}% - ${sectionsCompleted}/${totalSections} sections, ${quizCompleted}/${totalQuiz} quiz`;
    
    // Couleur dynamique selon progression
    if (overallProgress >= 100) {
      progressBar.style.background = 'linear-gradient(90deg, var(--success), var(--primary))';
    } else if (overallProgress >= 70) {
      progressBar.style.background = 'linear-gradient(90deg, var(--primary), var(--success))';
    }
  }
  
  // Événement personnalisé pour extensibilité
  document.dispatchEvent(new CustomEvent('progressUpdate', {
    detail: { 
      sectionsCompleted, 
      quizCompleted, 
      overallProgress,
      totalSections,
      totalQuiz
    }
  }));
}

//  Système de notifications
function showNotification(message, type = 'info', duration = 3000) {
  // Créer notification si pas de système existant
  let notification = document.querySelector('.app-notification');
  
  if (!notification) {
    notification = document.createElement('div');
    notification.className = 'app-notification';
    notification.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      padding: var(--space-md);
      border-radius: var(--radius-md);
      z-index: var(--z-tooltip, 1070);
      font-size: var(--text-sm);
      font-weight: var(--font-weight-medium, 500);
      transform: translateX(100%);
      transition: transform var(--transition);
      max-width: 300px;
    `;
    document.body.appendChild(notification);
  }
  
  // Style selon le type
  const styles = {
    success: `background: var(--success-light); border: 1px solid var(--success); color: var(--text-primary);`,
    error: `background: var(--error-light); border: 1px solid var(--error); color: var(--text-primary);`,
    celebration: `background: linear-gradient(45deg, var(--success-light), var(--primary-light)); border: 1px solid var(--primary); color: var(--text-primary);`,
    info: `background: var(--bg-card); border: 1px solid var(--border-medium); color: var(--text-primary);`
  };
  
  notification.style.cssText += styles[type] || styles.info;
  notification.textContent = message;
  
  // Animation d'entrée
  requestAnimationFrame(() => {
    notification.style.transform = 'translateX(0)';
  });
  
  // Auto-masquage
  setTimeout(() => {
    notification.style.transform = 'translateX(100%)';
  }, duration);
}

//  Gestion d'erreur globale de l'app
function showAppError(message) {
  const errorHTML = `
    <div class="app-error" style="
      position: fixed;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      background: var(--error-light);
      border: 2px solid var(--error);
      padding: var(--space-lg);
      border-radius: var(--radius-lg);
      z-index: var(--z-modal, 1050);
      text-align: center;
      max-width: 400px;
    ">
      <h3 style="color: var(--error); margin-bottom: var(--space-md);"> Erreur Application</h3>
      <p style="margin-bottom: var(--space-lg);">${message}</p>
      <button onclick="location.reload()" style="
        background: var(--error);
        color: white;
        border: none;
        padding: var(--space-sm) var(--space-lg);
        border-radius: var(--radius-md);
        cursor: pointer;
      ">Recharger la page</button>
    </div>
  `;
  
  document.body.insertAdjacentHTML('beforeend', errorHTML);
}

//  Statistiques de session
function logAppStats() {
  const sessionDuration = Math.round((Date.now() - userState.startTime) / 1000);
  const stats = {
    sessionDuration,
    sectionsCompleted: userState.sectionsCompleted.size,
    sectionsVisited: userState.sessionStats.sectionsVisited.size,
    quizSuccesses: userState.sessionStats.quizSuccesses,
    currentSection: userState.currentSection
  };
  
  console.log(' Statistiques session:', stats);
  return stats;
}

//  Exposition de l'API publique
window.AppManager = {
  showSection,
  markSectionComplete,
  markQuizComplete,
  updateProgress,
  getStats: logAppStats,
  getUserState: () => ({ ...userState }),
  reinitialize: initializeApp
};

//  Fonction globale pour compatibilité (appelée depuis HTML)
window.showSection = showSection;
window.markQuizComplete = markQuizComplete;

console.log(' App.js chargé - Manager disponible via window.AppManager');
