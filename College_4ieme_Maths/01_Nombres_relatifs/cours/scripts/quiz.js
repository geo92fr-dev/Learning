/* =============================================================================
   QUIZ.JS - Logique Robuste des Quiz
    GESTION COMPLÈTE AVEC VALIDATION & FEEDBACK
   ============================================================================= */

//  Initialisation sécurisée dans DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
  console.log(' Initialisation du système de quiz...');
  initializeAllQuiz();
});

//  Fonction principale d'initialisation
function initializeAllQuiz() {
  // Vérification que QUIZ_CONFIG existe
  if (typeof QUIZ_CONFIG === 'undefined') {
    console.error(' QUIZ_CONFIG non trouvé. Vérifiez que config.js est chargé.');
    return;
  }

  const quizElements = document.querySelectorAll('.quiz');
  console.log(` Initialisation de ${quizElements.length} quiz`);

  if (quizElements.length === 0) {
    console.warn(' Aucun quiz trouvé avec la classe .quiz');
    return;
  }

  // Initialiser chaque quiz individuellement
  quizElements.forEach((quiz, index) => {
    try {
      initializeSingleQuiz(quiz, index);
    } catch (error) {
      console.error(` Erreur initialisation quiz ${index}:`, error);
    }
  });

  console.log(' Tous les quiz initialisés avec succès');
}

//  Initialisation d'un quiz individuel
function initializeSingleQuiz(quiz, index) {
  const key = quiz.dataset.key;
  const config = QUIZ_CONFIG[key];
  const button = quiz.querySelector('button');
  const input = quiz.querySelector('input');
  const feedback = quiz.querySelector('.feedback');

  // Validation structure HTML
  if (!key) {
    console.error(` Quiz ${index}: attribut data-key manquant`);
    showQuizError(quiz, 'Attribut data-key manquant');
    return;
  }

  if (!config) {
    console.error(` Quiz ${index}: configuration manquante pour clé "${key}"`);
    showQuizError(quiz, ERROR_MESSAGES.noConfig || 'Configuration manquante');
    return;
  }

  if (!button || !input) {
    console.error(` Quiz ${index}: structure HTML invalide`);
    showQuizError(quiz, ERROR_MESSAGES.invalidStructure || 'Structure HTML invalide');
    return;
  }

  // Créer feedback si manquant
  if (!feedback) {
    const feedbackEl = document.createElement('div');
    feedbackEl.className = 'feedback';
    quiz.appendChild(feedbackEl);
  }

  // Attacher les événements
  button.onclick = () => handleQuizSubmit(quiz, config);
  
  input.onkeypress = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleQuizSubmit(quiz, config);
    }
  };

  // État initial
  input.oninput = () => clearFeedback(quiz);
  
  console.log(` Quiz initialisé: ${key}`);
}

//  Gestion de la soumission du quiz
function handleQuizSubmit(quiz, config) {
  const input = quiz.querySelector('input');
  const userInput = input.value;

  // Validation input vide
  if (!userInput || !userInput.trim()) {
    showFeedback(quiz, false, ERROR_MESSAGES.emptyInput || 'Entrez votre réponse');
    input.focus();
    return;
  }

  // Normalisation et vérification
  const userAnswer = normalizeAnswer(userInput);
  const correctAnswer = normalizeAnswer(config.answer);
  
  console.log(` Quiz ${quiz.dataset.key}: "${userInput}"  "${userAnswer}" vs "${correctAnswer}"`);
  
  const isCorrect = userAnswer === correctAnswer;

  // Feedback visuel
  const message = isCorrect 
    ? config.explain 
    : ` Indice: ${config.explain}`;
    
  showFeedback(quiz, isCorrect, message);

  // Tracking progression
  if (isCorrect && typeof markQuizComplete === 'function') {
    setTimeout(() => {
      markQuizComplete(quiz.dataset.key);
    }, UI_CONFIG?.progressUpdateDelay || 200);
  }
}

//  Normalisation robuste des réponses
function normalizeAnswer(answer) {
  if (!answer || typeof answer !== 'string') {
    return '';
  }

  return answer
    .trim()                           // Supprimer espaces début/fin
    .replace(/\s+/g, '')              // Supprimer TOUS les espaces internes
    .toUpperCase()                    // Insensible à la casse
    .replace(/^(?![+-])([0-9])/, '+$1'); // Ajouter + si nombre sans signe
}

//  Affichage du feedback avec animations
function showFeedback(quiz, isCorrect, message) {
  const feedback = quiz.querySelector('.feedback');
  if (!feedback) return;

  // Reset pour nouvelle animation
  feedback.className = 'feedback';
  feedback.innerHTML = '';

  // Délai pour transition fluide
  setTimeout(() => {
    const messageText = isCorrect 
      ? getRandomMessage?.('success') || 'Excellent !' 
      : getRandomMessage?.('error') || 'Pas tout à fait...';

    feedback.className = `feedback ${isCorrect ? 'success' : 'error'}`;
    feedback.innerHTML = `
      <div class="feedback-icon">${isCorrect ? '' : ''}</div>
      <div class="feedback-text">
        <strong>${messageText}</strong>
        <p>${message}</p>
      </div>
    `;

    // Animation de célébration si correct
    if (isCorrect) {
      celebrateSuccess(quiz);
    }
    
  }, UI_CONFIG?.feedbackDelay || 50);
}

//  Animation de célébration
function celebrateSuccess(quiz) {
  quiz.classList.add('quiz-success');
  
  setTimeout(() => {
    quiz.classList.remove('quiz-success');
  }, UI_CONFIG?.successCelebrationDuration || 600);

  // Effet sonore (si disponible)
  try {
    // Future: ajouter son de succès
    console.log(' Son de succès (à implémenter)');
  } catch (e) {
    // Son non disponible, pas grave
  }
}

//  Effacer le feedback
function clearFeedback(quiz) {
  const feedback = quiz.querySelector('.feedback');
  if (feedback && feedback.classList.contains('success', 'error')) {
    feedback.className = 'feedback';
    feedback.innerHTML = '';
  }
}

//  Affichage d'erreur de quiz
function showQuizError(quiz, errorMessage) {
  quiz.innerHTML = `
    <div class="error">
      ${errorMessage}
      <br><small>Contactez l'assistance si le problème persiste.</small>
    </div>
  `;
}

//  Fonction utilitaire: réinitialiser un quiz
function resetQuiz(quizKey) {
  const quiz = document.querySelector(`[data-key="${quizKey}"]`);
  if (!quiz) return;

  const input = quiz.querySelector('input');
  const feedback = quiz.querySelector('.feedback');

  if (input) input.value = '';
  if (feedback) {
    feedback.className = 'feedback';
    feedback.innerHTML = '';
  }
  
  console.log(` Quiz "${quizKey}" réinitialisé`);
}

//  Fonction utilitaire: réinitialiser tous les quiz
function resetAllQuiz() {
  document.querySelectorAll('.quiz input').forEach(input => {
    input.value = '';
  });
  
  document.querySelectorAll('.quiz .feedback').forEach(feedback => {
    feedback.className = 'feedback';
    feedback.innerHTML = '';
  });
  
  console.log(' Tous les quiz réinitialisés');
}

//  Fonction utilitaire: statistiques des quiz
function getQuizStats() {
  const allQuiz = document.querySelectorAll('.quiz');
  const successfulQuiz = document.querySelectorAll('.quiz .feedback.success');
  
  const stats = {
    total: allQuiz.length,
    completed: successfulQuiz.length,
    remaining: allQuiz.length - successfulQuiz.length,
    percentage: allQuiz.length > 0 ? Math.round((successfulQuiz.length / allQuiz.length) * 100) : 0
  };
  
  console.log(' Statistiques quiz:', stats);
  return stats;
}

//  Exposition de fonctions utilitaires globales
window.QuizManager = {
  reset: resetQuiz,
  resetAll: resetAllQuiz,
  stats: getQuizStats,
  reinitialize: initializeAllQuiz
};

console.log(' Quiz.js chargé - Manager disponible via window.QuizManager');
