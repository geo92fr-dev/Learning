// Helper to toggle solution blocks (used by integrated exercise cards)
function toggleSolution(id, btn){
    const el = document.getElementById(id);
    if (!el) return;
    const isHidden = (el.style.display === 'none' || el.style.display === '');
    el.style.display = isHidden ? 'block' : 'none';
    if (btn) {
        const expanded = isHidden ? 'true' : 'false';
        btn.setAttribute('aria-expanded', expanded);
    }
}

// Navigation par scroll (comme l'original)
function showSection(sectionId) {
    console.log('Navigation vers:', sectionId);
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth', block: 'start' });
        updateProgress(sectionId);
    }
}

// Navigation entre phases de quiz
function showPhase(phaseNum) {
    console.log('Navigation vers phase:', phaseNum);
    
    // Mettre à jour les boutons
    const phaseBtns = document.querySelectorAll('.phase-btn');
    phaseBtns.forEach(btn => btn.classList.remove('active'));
    document.querySelector(`.phase-btn:nth-child(${phaseNum})`).classList.add('active');
    
    // Masquer toutes les phases
    const phases = document.querySelectorAll('.quiz-phase');
    phases.forEach(phase => phase.classList.remove('active'));
    
    // Afficher la phase ciblée
    const targetPhase = document.getElementById(`phase-${phaseNum}`);
    if (targetPhase) {
        targetPhase.classList.add('active');
    }
}

// Fonction générique de vérification de réponse
function normalizeAnswer(answer) {
    return answer.toLowerCase().trim().replace(/\s+/g, '');
}

function checkPhaseAnswer(inputId, correctAnswer, explanation) {
    const input = document.getElementById(inputId);
    const feedback = document.getElementById(inputId + '-feedback');
    
    if (!input || !feedback) return;
    
    const userAnswer = normalizeAnswer(input.value);
    const correct = normalizeAnswer(correctAnswer);
    
    if (userAnswer === correct || userAnswer === correct.replace('+', '')) {
        feedback.textContent = '✅ Correct ! ' + explanation;
        feedback.style.color = '#10b981';
        input.disabled = true;
        input.nextElementSibling.disabled = true;
    } else {
        feedback.textContent = '❌ Essayez encore. Pensez aux règles !';
        feedback.style.color = '#ef4444';
    }
}

function checkAnswer(button, isCorrect) {
    const feedback = document.getElementById('intro-feedback');
    const buttons = document.querySelectorAll('.quiz-option');

    // Désactiver tous les boutons et retirer anciens états
    buttons.forEach(btn => {
        btn.disabled = true;
        btn.classList.remove('btn--primary', 'btn--danger', 'quiz-option--correct', 'quiz-option--wrong');
        btn.setAttribute('aria-pressed', 'false');
    });

    // Appliquer l'état sur le bouton cliqué
    if (isCorrect) {
        button.classList.add('btn--primary', 'quiz-option--correct');
        feedback.textContent = '✅ Correct ! -2 est plus grand que -8 et -10 sur la droite graduée.';
        feedback.style.color = '#10b981';
    } else {
        button.classList.add('btn--danger', 'quiz-option--wrong');
        feedback.textContent = '❌ Non, regardez la droite graduée : plus on va à droite, plus c\'est grand.';
        feedback.style.color = '#ef4444';
        // Mettre aussi en évidence le bon bouton pour l'apprentissage
        const correctBtn = Array.from(buttons).find(b => b.dataset.correct === 'true');
        if (correctBtn) correctBtn.classList.add('btn--primary', 'quiz-option--correct');
    }
    button.setAttribute('aria-pressed', 'true');
}

function checkRetention(inputId, expectedWord) {
    const input = document.getElementById(inputId);
    const feedback = document.getElementById(inputId + '-feedback');
    
    const userAnswer = normalizeAnswer(input.value);
    
    if (userAnswer.includes(expectedWord)) {
        feedback.textContent = '✅ Parfait ! Vous maîtrisez la règle.';
        feedback.style.color = '#10b981';
        input.disabled = true;
        input.nextElementSibling.disabled = true;
    } else {
        feedback.textContent = '❌ Relisez la règle correspondante ci-dessus.';
        feedback.style.color = '#ef4444';
    }
}

function checkMethodStep(step, isCorrect, message) {
    const feedback = document.getElementById(`method-step${step}-feedback`);
    const buttons = document.querySelectorAll('.guided-question button');
    
    buttons.forEach(btn => btn.disabled = true);
    
    if (isCorrect) {
        feedback.textContent = '✅ ' + message;
        feedback.style.color = '#10b981';
    } else {
        feedback.textContent = '❌ ' + message;
        feedback.style.color = '#ef4444';
    }
}

function checkTrap(button, isCorrect, message) {
    const feedback = document.getElementById('trap-feedback');
    const buttons = document.querySelectorAll('.trap-option');

    buttons.forEach(btn => {
        btn.disabled = true;
        btn.classList.remove('btn--primary','btn--danger','quiz-option--correct','quiz-option--wrong');
        btn.setAttribute('aria-pressed','false');
    });

    if (isCorrect) {
        button.classList.add('btn--primary','quiz-option--correct');
        feedback.textContent = '✅ ' + message;
        feedback.style.color = '#10b981';
    } else {
        button.classList.add('btn--danger','quiz-option--wrong');
        feedback.textContent = '❌ ' + message;
        feedback.style.color = '#ef4444';
        const correctBtn = Array.from(buttons).find(b => b.dataset.correct === 'true');
        if (correctBtn) correctBtn.classList.add('btn--primary','quiz-option--correct');
    }
    button.setAttribute('aria-pressed','true');
}

function updateProgress(sectionId) {
    const progressBar = document.querySelector('.progress-bar');
    if (!progressBar) return;
    const sections = ['introduction', 'retention', 'phases', 'methodes', 'pieges', 'exercices-n1', 'exercices-n2', 'exercices-n3', 'fiche-synthese'];
    const sectionNames = {
        'introduction': 'Introduction',
        'retention': 'Règles',
        'phases': 'Quiz',
        'methodes': 'Méthodes',
        'pieges': 'Pièges',
        'exercices-n1': 'Exercice 1',
        'exercices-n2': 'Exercice 2',
        'exercices-n3': 'Exercice 3',
        'fiche-synthese': 'Synthèse'
    };
    const currentIndex = sections.indexOf(sectionId);
    if (currentIndex >= 0) {
        const progress = ((currentIndex + 1) / sections.length) * 100;
        const sectionName = sectionNames[sectionId] || 'Section';
        const rounded = Math.round(progress);
        progressBar.style.width = progress + '%';
        progressBar.textContent = `${rounded}% - ${sectionName} (${currentIndex + 1}/${sections.length})`;
        progressBar.setAttribute('aria-valuenow', String(rounded));
        progressBar.setAttribute('aria-label', `Progression du chapitre : ${rounded}%. Section : ${sectionName}`);
        // Add completion banner once when reaching 100%
        if (rounded === 100 && !document.getElementById('end-banner')) {
            const synthese = document.getElementById('fiche-synthese');
            if (synthese) {
                const endDiv = document.createElement('div');
                endDiv.id = 'end-banner';
                endDiv.className = 'memo-box';
                endDiv.innerHTML = '<h3>🎉 Bravo ! Vous avez complété 100% du chapitre.</h3><p>Suggestion : enchaînez avec la multiplication des nombres relatifs.</p>';
                synthese.appendChild(endDiv);
            }
        }
    }
}

// Initialisation
document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ Application initialisée - Toutes les sections visibles');
    // Make all sections visible (the base CSS hides [data-section] by default)
    // This preserves the original behavior where all sections are present and
    // navigation simply scrolls to the chosen section.
    document.querySelectorAll('[data-section]').forEach(function(s) {
        s.classList.add('active');
    });

    // Initialize progress to the introduction section
    updateProgress('introduction');
    
    // Navigation au clavier
    document.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowLeft') showPreviousSection();
        if (e.key === 'ArrowRight') showNextSection();
        if (e.key === 'Escape') showSection('introduction');
        // Shortcuts: 1/2/3/4/S navigate in-page to exercise levels and synthesis
        if (e.key === '1') { showSection('exercices-n1'); }
        if (e.key === '2') { showSection('exercices-n2'); }
        if (e.key === '3') { showSection('exercices-n3'); }
        if (e.key === '4' || e.key.toLowerCase() === 's') { showSection('fiche-synthese'); }
    });
});

// =========================
// Plan de réactivation -> création d'événement Google Agenda
// =========================
function pad(n){ return n < 10 ? '0'+n : ''+n; }
function formatDateForGCal(date){
    // Google demande format YYYYMMDDTHHMMSSZ (UTC) ou sans Z pour date locale
    // On crée un événement de 30 minutes par défaut à 17h locale
    const start = new Date(date.getFullYear(), date.getMonth(), date.getDate(), 17, 0, 0);
    const end = new Date(start.getTime() + 30*60000);
    function toStr(d){
        return d.getFullYear()+ pad(d.getMonth()+1)+ pad(d.getDate()) + 'T' + pad(d.getHours()) + pad(d.getMinutes()) + '00';
    }
    return { start: toStr(start), end: toStr(end) };
}

const COURSE_URL = 'https://geo92fr-dev.github.io/Learning/College_4ieme_Maths/01_Nombres_relatifs/cours/cours_principal.html';
function createCalendarEvent(dayOffset, label, sectionId){
    const base = new Date();
    base.setHours(0,0,0,0);
    const target = new Date(base.getTime() + dayOffset*24*60*60*1000);
    const times = formatDateForGCal(target);
    const title = encodeURIComponent('Réactivation: ' + label);
    const anchorUrl = COURSE_URL + (sectionId ? '#' + sectionId : '');
    const details = encodeURIComponent('Session de réactivation du chapitre Nombres relatifs. Objectif: ' + label + '\nAccès direct: ' + anchorUrl);
    const location = encodeURIComponent('En ligne / Classe');
    const url = `https://www.google.com/calendar/render?action=TEMPLATE&text=${title}&dates=${times.start}/${times.end}&details=${details}&location=${location}&trp=false&sprop=name:`;
    window.open(url, '_blank');
}

// =========================
// Génération dynamique du plan de réactivation
// =========================
const REACTIVATION_STEPS = [
    { d:1,  type:'rappel',      section:'retention',      label:'Relire les 3 règles + 2 ex. N1',         focus:'Règles + Exos découverte', icon:'📘'},
    { d:3,  type:'application', section:'exercices-n2',   label:'2 ex. N2 + 1 méthode guidée',           focus:'Automatisation',           icon:'🛠️'},
    { d:5,  type:'pièges',      section:'pieges',         label:'Revoir 2 pièges + 1 ex. N2',            focus:'Éviter erreurs',           icon:'⚠️'},
    { d:7,  type:'synthèse',    section:'fiche-synthese', label:'Mini quiz synthèse + 1 ex. N3',         focus:'Consolidation',            icon:'🧠'},
    { d:10, type:'défi',        section:'exercices-n3',   label:'2 ex. N3 (défi)',                       focus:'Transfert avancé',         icon:'🔥'},
    { d:14, type:'bilan',       section:'phases',         label:'Quiz récap + 1 ex. mixte',              focus:'Stabilité mémoire',        icon:'✅'}
];

function formatFrenchDate(date){
    return date.toLocaleDateString('fr-FR',{ weekday:'short', day:'numeric', month:'short'}).replace('.', '');
}

function buildReactivationPlan(){
    const container = document.getElementById('reactivation-list');
    const baseDateEl = document.getElementById('plan-base-date');
    if(!container || !baseDateEl) return;
    const today = new Date(); today.setHours(0,0,0,0);
    const longBase = today.toLocaleDateString('fr-FR',{ weekday:'long', day:'numeric', month:'long', year:'numeric'});
    baseDateEl.textContent = 'Cours fait le : ' + longBase;
    container.innerHTML='';
    REACTIVATION_STEPS.forEach(step => {
         const target = new Date(today.getTime() + step.d*24*60*60*1000);
         const li = document.createElement('div');
         li.className = 'reactivation-item';
         li.innerHTML = `
             <button class="reactivation-add" onclick="createCalendarEvent(${step.d},'${step.label.replace(/'/g,"\'")}', '${step.section}')" aria-label="Ajouter J+${step.d} au Google Agenda (section ${step.section})">📅</button>
             <strong>J+${step.d}</strong> (${formatFrenchDate(target)}) : ${step.icon} ${step.label} <span class="reactivation-focus" aria-label="Focus pédagogique">→ ${step.focus}</span>
         `;
         container.appendChild(li);
    });
}

document.addEventListener('DOMContentLoaded', buildReactivationPlan);

// Shortcut helpers

function goToExercise(level) {
    showSection('phases');
    showPhase(level);
    const el = document.getElementById('phase-' + level);
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function goToSynthesis() {
    showSection('methodes');
    const el = document.getElementById('methodes');
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function showNextSection() {
    const sections = ['introduction', 'retention', 'phases', 'methodes', 'pieges'];
    const currentVisible = getCurrentVisibleSection();
    const currentIndex = sections.indexOf(currentVisible);
    if (currentIndex < sections.length - 1) {
        showSection(sections[currentIndex + 1]);
    }
}

function showPreviousSection() {
    const sections = ['introduction', 'retention', 'phases', 'methodes', 'pieges'];
    const currentVisible = getCurrentVisibleSection();
    const currentIndex = sections.indexOf(currentVisible);
if (currentIndex > 0) {
        showSection(sections[currentIndex - 1]);
    }
}

function getCurrentVisibleSection() {
    const sections = document.querySelectorAll('[data-section]');
    let visibleSection = 'introduction';
    
    sections.forEach(section => {
        const rect = section.getBoundingClientRect();
        if (rect.top <= 150 && rect.bottom > 150) {
            visibleSection = section.getAttribute('data-section');
        }
    });
    
    return visibleSection;
}

// Responsive navigation toggle
function toggleNav(btn){
    const nav = document.getElementById('nav-main');
    if(!nav) return;
    const isOpen = nav.classList.toggle('open');
    btn.setAttribute('aria-expanded', isOpen ? 'true':'false');
}
