/* =============================================================================
   CONFIG.JS - Configuration Centralisée des Quiz
    TOUTES LES DONNÉES EN UN SEUL ENDROIT
   ============================================================================= */

//  Configuration des Quiz - Facile à modifier
const QUIZ_CONFIG = {
  //  Phase 1 - Apprentissage guidé
  phase1_1: {
    answer: '+2',
    explain: 'Signes différents : |7| - |5| = 2, signe de la plus grande distance (+7)  +2'
  },
  phase1_2: {
    answer: '-3',
    explain: 'Signes différents : |8| - |5| = 3, signe de la plus grande distance (-8)  -3'
  },
  phase1_3: {
    answer: '+9',
    explain: 'Signes identiques positifs : 4 + 5 = 9  +9'
  },
  
  //  Phase 2 - Pratique autonome
  phase2_1: {
    answer: '-5',
    explain: 'Signes différents : |9| - |4| = 5, signe de la plus grande distance (-9)  -5'
  },
  phase2_2: {
    answer: '+11',
    explain: 'Signes différents : |15| - |4| = 11, signe de la plus grande distance (+15)  +11'
  },
  phase2_3: {
    answer: '-12',
    explain: 'Signes identiques négatifs : 7 + 5 = 12, même signe négatif  -12'
  },
  
  //  Phase 3 - Maîtrise
  phase3_1: {
    answer: '+6',
    explain: 'Signes différents : |10| - |4| = 6, signe de la plus grande distance (+10)  +6'
  },
  phase3_2: {
    answer: '-8',
    explain: 'Signes identiques négatifs : 3 + 5 = 8, même signe négatif  -8'
  },
  phase3_3: {
    answer: '0',
    explain: 'Nombres opposés : (+7) + (-7) = 0 (ils s''annulent)'
  },
  
  //  Méthodes - Mini-vérifications
  method1: {
    answer: '-14',
    explain: 'Même signe négatif : j''additionne 8+6=14 et je garde le signe  -14'
  },
  method2: {
    answer: '+3',
    explain: 'Signes différents : je soustrais 9-6=3, signe du plus grand (+9)  +3'
  },
  method3: {
    answer: '-7',
    explain: 'Signes différents : je soustrais 12-5=7, signe du plus grand (-12)  -7'
  },
  
  //  Pièges classiques
  piege1: {
    answer: '+8',
    explain: 'PIÈGE évité ! Même signe positif : 3+5=8  +8 (pas -8)'
  },
  piege2: {
    answer: '-2',
    explain: 'PIÈGE évité ! Signes différents : 6-8=2, signe du plus grand (-8)  -2 (pas +2)'
  },
  piege3: {
    answer: '+10',
    explain: 'PIÈGE évité ! Signes différents : 15-5=10, signe du plus grand (+15)  +10'
  }
};

//  Messages d'encouragement aléatoires
const ENCOURAGEMENT_MESSAGES = {
  success: [
    'Excellent ! ',
    'Parfait ! ',
    'Bravo ! ',
    'Génial ! ',
    'Top ! ',
    'Super ! '
  ],
  error: [
    'Pas tout à fait...',
    'Presque ! Réessaye',
    'Pas grave, continue !',
    'On y est presque !',
    'Allez, encore un effort !'
  ]
};

//  Configuration UI
const UI_CONFIG = {
  animationDuration: 600,
  feedbackDelay: 50,
  successCelebrationDuration: 600,
  progressUpdateDelay: 200
};

//  Messages d'erreurs techniques
const ERROR_MESSAGES = {
  noConfig: ' Configuration quiz invalide',
  invalidStructure: ' Structure HTML incorrecte',
  emptyInput: ' Entrez votre réponse',
  networkError: ' Problème de connexion'
};

//  Fonction utilitaire pour récupérer un message aléatoire
function getRandomMessage(type) {
  const messages = ENCOURAGEMENT_MESSAGES[type] || ['Continuez !'];
  return messages[Math.floor(Math.random() * messages.length)];
}

//  Export pour compatibilité (si nécessaire)
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    QUIZ_CONFIG,
    ENCOURAGEMENT_MESSAGES,
    UI_CONFIG,
    ERROR_MESSAGES,
    getRandomMessage
  };
}

console.log(' Config chargée -', Object.keys(QUIZ_CONFIG).length, 'quiz disponibles');
