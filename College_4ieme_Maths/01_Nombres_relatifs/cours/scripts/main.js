// (toggleSolution) obsolète : les solutions complètes sont injectées après validation maintenant
function toggleSolution(id, btn){
    // Affiche l'indice à la première ouverture puis toggle ensuite
    const el = document.getElementById(id);
    if(!el) return;
    if(!el.dataset.mode){
        const { hintHtml } = extractHintAndSolution(el.innerHTML);
        el.dataset.full = el.innerHTML;
        el.innerHTML = hintHtml && hintHtml.trim() ? hintHtml : '<p><em>Aucun indice disponible.</em></p>';
        el.dataset.mode = 'prepared';
        // Première ouverture : rendre visible
        el.removeAttribute('hidden');
        el.style.display = 'block'; // sécurité
        if(btn) btn.setAttribute('aria-expanded','true');
        el.dataset.preparedDisplayed = '1';
        console.debug('[Indice] affiché pour', id);
        // Tracking usage indice (1 seul enregistrement par bloc)
        try {
            if(window.registerScore && !el.dataset.hintAwarded){
                // section déterminée via parent data-section
                const section = el.closest('[data-section]')?.getAttribute('data-section') || 'exercices-n1';
                registerScore(section, 'hint-'+id, 0, { hint:true }); // valeur 0: pas d'impact sur score mais trace dans awarded
                el.dataset.hintAwarded = '1';
            }
        } catch(e){ /* ignore */ }
        return;
    }
    const isHidden = el.hasAttribute('hidden');
    if(isHidden){
        el.removeAttribute('hidden');
        el.style.display = 'block';
        if(btn) btn.setAttribute('aria-expanded','true');
    } else {
        el.setAttribute('hidden','');
        el.style.display = 'none';
        if(btn) btn.setAttribute('aria-expanded','false');
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
        feedback.style.color = 'var(--success)';
        input.disabled = true;
        input.nextElementSibling.disabled = true;
        registerScore('phases', 'phase-'+inputId, 1);
    } else {
    feedback.textContent = '❌ Réessaie. Pense aux règles.';
        feedback.style.color = 'var(--danger)';
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
    feedback.textContent = '✅ Oui ! -2 est plus grand que -8 et -10 sur la droite graduée.';
        feedback.style.color = 'var(--success)';
        registerScore('introduction', 'intro-q1', 1);
    } else {
        button.classList.add('btn--danger', 'quiz-option--wrong');
    feedback.textContent = '❌ Non. Regarde la droite graduée : plus à droite = plus grand.';
        feedback.style.color = 'var(--danger)';
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
        feedback.textContent = '✅ Bien ! Tu connais la règle.';
        feedback.style.color = 'var(--success)';
        input.disabled = true;
        input.nextElementSibling.disabled = true;
        registerScore('retention', 'retention-'+inputId, 1);
    } else {
        feedback.textContent = '❌ Relis la règle juste au-dessus.';
        feedback.style.color = 'var(--danger)';
    }
}

// Nouveau quiz de mémorisation (Vrai/Faux & choix multiple)
function answerRetentionVF(btn, key, expected){
    const container = btn.closest('.quiz-card');
    if(!container) return;
    const fb = document.getElementById('retention-'+key);
    if(!fb) return;
    // Si déjà répondu, ignorer
    if(container.classList.contains('done')) return;
    const isTrueBtn = btn.textContent.trim().toLowerCase() === 'vrai';
    const userValue = (btn.textContent.trim().toLowerCase() === 'vrai');
    const correct = expected === userValue;
    container.querySelectorAll('button').forEach(b=>{ b.disabled = true; });
    if(correct){
        fb.textContent = '✅ Oui'; fb.style.color = 'var(--success)';
        registerScore('retention','retention-'+key,1);
    } else {
        fb.textContent = '❌ Non'; fb.style.color = 'var(--danger)';
    }
    container.classList.add('done');
}
function answerRetentionMC(btn, key, choice){
    const container = btn.closest('.quiz-card');
    if(!container) return;
    const fb = document.getElementById('retention-'+key);
    if(!fb) return;
    if(container.classList.contains('done')) return;
    const correctChoice = 'B';
    container.querySelectorAll('button').forEach(b=> b.disabled = true);
    if(choice === correctChoice){
        fb.textContent = '✅ Oui : on soustrait les valeurs'; fb.style.color = 'var(--success)';
        registerScore('retention','retention-'+key,1);
    } else {
        fb.textContent = '❌ Non : on soustrait (réponse B)'; fb.style.color = 'var(--danger)';
    }
    container.classList.add('done');
}

function checkMethodStep(step, isCorrect, message) {
    const feedback = document.getElementById(`method-step${step}-feedback`);
    const buttons = document.querySelectorAll('.guided-question button');
    // Scope to this guided-question only
    const container = feedback ? feedback.closest('.guided-question') : null;
    const localButtons = container ? container.querySelectorAll('button') : buttons;
    localButtons.forEach(btn => btn.disabled = true);
    if (isCorrect) {
        feedback.textContent = '✅ ' + message;
        feedback.style.color = 'var(--success)';
        registerScore('methodes', 'method-step-'+step, 1);
        // highlight correct button
        event?.target?.classList?.remove('btn--secondary');
        event?.target?.classList?.add('btn--primary');
    } else {
        feedback.textContent = '❌ ' + message;
        feedback.style.color = 'var(--danger)';
        event?.target?.classList?.add('btn--danger');
    }
}

function checkTrap(button, isCorrect, message, key='trap-q1') {
    const container = button.closest('.mini-trap-quiz');
    if(!container || container.classList.contains('done')) return;
    const feedback = container.querySelector('.quiz-feedback');
    const buttons = container.querySelectorAll('.trap-option');
    buttons.forEach(btn => {
        btn.disabled = true;
        btn.classList.remove('btn--primary','btn--danger','quiz-option--correct','quiz-option--wrong');
        btn.setAttribute('aria-pressed','false');
    });
    if (isCorrect) {
        button.classList.add('btn--primary','quiz-option--correct');
        if(feedback){ feedback.textContent = '✅ ' + message; feedback.style.color = 'var(--success)'; }
        registerScore('pieges', key, 1);
    } else {
        button.classList.add('btn--danger','quiz-option--wrong');
        if(feedback){ feedback.textContent = '❌ ' + message; feedback.style.color = 'var(--danger)'; }
        const correctBtn = Array.from(buttons).find(b => b.dataset.correct === 'true');
        if (correctBtn) correctBtn.classList.add('btn--primary','quiz-option--correct');
    }
    button.setAttribute('aria-pressed','true');
    container.classList.add('done');
}

const VISITED_STORAGE_KEY = 'relatifs_sections_seen_v1';
let visitedSections = new Set();
try {
    const rawVisited = localStorage.getItem(VISITED_STORAGE_KEY);
    if(rawVisited){ JSON.parse(rawVisited).forEach(s=>visitedSections.add(s)); }
} catch(e){ /* ignore */ }

function persistVisited(){
    try { localStorage.setItem(VISITED_STORAGE_KEY, JSON.stringify(Array.from(visitedSections))); } catch(e){ /* ignore */ }
}

function getMasteryRatio(){
    const engine = window.ScoreEngine; if(!engine) return 0;
    const st = engine.getState();
    const max = Object.values(engine.MAX_POINTS).reduce((a,b)=>a+b,0) || 1;
    return st.total / max;
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
    if(sectionId) { visitedSections.add(sectionId); persistVisited(); }
    // Progression basée sur sections réellement visitées (et non simple index)
    const visitedCount = Array.from(visitedSections).filter(s=>sections.includes(s)).length;
    const progress = (visitedCount / sections.length) * 100;
    const currentName = sectionNames[sectionId] || 'Section';
    const rounded = Math.round(progress);
    progressBar.style.width = progress + '%';
    progressBar.textContent = `${rounded}% (parcours) - ${currentName} (${visitedCount}/${sections.length})`;
    progressBar.setAttribute('aria-valuenow', String(rounded));
    progressBar.setAttribute('aria-label', `Progression de lecture : ${rounded}%. Section courante : ${currentName}`);

    // Gestion des bannières de fin
    const existing = document.getElementById('end-banner');
    const synthese = document.getElementById('fiche-synthese');
    if(!synthese) return;
    const mastery = getMasteryRatio();
    const masteryPct = Math.round(mastery*100);
    if(visitedCount === sections.length){
        if(!existing){
            const endDiv = document.createElement('div');
            endDiv.id = 'end-banner';
            endDiv.className = 'memo-box';
            if(mastery === 1){
                endDiv.innerHTML = `<h3>🎉 Bravo ! Tu as tout lu et tout maîtrisé (100%).</h3><p>Suite possible : multiplication des nombres relatifs.</p>`;
            } else if(mastery >= .7){
                endDiv.innerHTML = `<h3>✅ Tu as tout lu. Maîtrise solide : ${masteryPct}%.</h3><p>Encore quelques points pour atteindre 100%.</p>`;
            } else {
                endDiv.innerHTML = `<h3>📘 Tu as tout lu. Maîtrise actuelle : ${masteryPct}%.</h3><p>Fais d'autres quiz, exercices ou révisions pour monter ton score.</p>`;
            }
            synthese.appendChild(endDiv);
        } else {
            // Mettre à jour dynamiquement si la maîtrise évolue
            if(mastery === 1 && !existing.innerHTML.includes('🎉')){
                existing.innerHTML = `<h3>🎉 Bravo ! Tu as tout lu et tout maîtrisé (100%).</h3><p>Suite possible : multiplication des nombres relatifs.</p>`;
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
        const tag = e.target.tagName;
        const typingContext = ['INPUT','TEXTAREA'].includes(tag) || e.target.isContentEditable;
        // Allow Escape to still work, but block navigation keys while typing to avoid scroll jumps
        if (typingContext) {
            if(e.key === 'Escape') { showSection('introduction'); }
            return; // prevent arrow / numeric shortcuts during text entry
        }
        if (e.key === 'ArrowLeft') { e.preventDefault(); showPreviousSection(); }
        if (e.key === 'ArrowRight') { e.preventDefault(); showNextSection(); }
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
    // Scoring (1 point par ajout si pas déjà pris)
    if(window.registerScore){
        registerScore('plan-reactivation', 'reactivation-'+dayOffset, 1, {label});
    }
}

// =========================
// Génération dynamique du plan de réactivation
// =========================
// Version simplifiée (4 étapes majeures)
const REACTIVATION_STEPS = [
    { d:1,  type:'ancrage',     section:'retention',      label:'Relire règles + 2 ex. N1',              focus:'Ancrer fondamentaux',      icon:'📘'},
    { d:4,  type:'automatisation', section:'exercices-n2', label:'3 ex. N2 + 1 méthode',                 focus:'Automatiser procédures',   icon:'🛠️'},
    { d:8,  type:'consolidation', section:'fiche-synthese', label:'Mini quiz + 2 ex. N3',                focus:'Consolider + transférer',  icon:'🧠'},
    { d:15, type:'bilan',       section:'phases',         label:'Quiz récap + 1 mixte',                  focus:'Stabilité à long terme',   icon:'✅'}
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

// =========================
// Vérification des réponses d'exercices (inputs libres)
// =========================
function normalizeUserValue(val){
    return val.toLowerCase().trim().replace(/\s+/g,'').replace('°c','c');
}
function extractHintAndSolution(solutionHtml){
    // Retire balises extérieures si besoin puis sépare Indice/Méthode/Règle/Étapes et Solution
    // On récupère les paragraphes et on re-classe.
    const container = document.createElement('div');
    container.innerHTML = solutionHtml;
    const ps = Array.from(container.querySelectorAll('p'));
    let hintParts = [];
    let solutionParts = [];
    ps.forEach(p => {
        const raw = p.textContent || '';
        const txt = raw.trim();
        const lower = txt.toLowerCase();
        if(/^indice\s*:/.test(lower) || /^(méthode|methode)\s*:/.test(lower) || /^(règle|regle)\s*:/.test(lower) || /^(étapes|etapes)\s*:/.test(lower)){
            // Retire le label initial pour allèger
            const cleaned = txt.replace(/^\w+\s*:\s*/i,'').trim();
            if(cleaned) hintParts.push('<p>'+cleaned+'</p>');
        } else if(/^solution\s*:/.test(lower)) {
            const cleaned = txt.replace(/^solution\s*:\s*/i,'').trim();
            if(cleaned) solutionParts.push('<p>'+cleaned+'</p>');
        } else {
            if(solutionParts.length===0) hintParts.push(p.outerHTML); else solutionParts.push(p.outerHTML);
        }
    });
    return { hintHtml: hintParts.join(''), solutionHtml: solutionParts.join('') };
}

// Helper pour forcer un style succès inline (contourne overrides externes)
function applySuccessFeedback(fb, restored=false){
    if(!fb) return;
    fb.classList.add('exercise-feedback--success');
    fb.style.setProperty('background','var(--bg-secondary)','important');
    fb.style.setProperty('border-left','3px solid var(--success)','important');
    fb.style.setProperty('box-shadow','inset 0 0 0 1px rgba(16,185,129,0.15)','important');
    const baseMsg = restored ? 'Correct (restauré)' : 'Bien !';
    // Ne pas écraser si une solution inline est déjà injectée (on reconstruit seulement l'entête)
    const existingInline = fb.querySelector('.success-head');
    if(!existingInline){
        // Conserver éventuelle solution déjà injectée
        const solutionNodes = Array.from(fb.querySelectorAll('.inline-solution'));
        fb.innerHTML = `<div class="success-head"><span class="assist-icon" aria-hidden="true">✅</span><span class="assist-text">${baseMsg}</span></div>`;
        solutionNodes.forEach(n=> fb.appendChild(n));
    } else {
        const label = existingInline.querySelector('.assist-text');
        if(label) label.textContent = baseMsg;
    }
}

function checkExerciseAnswer(btn){
    const wrapper = btn.closest('.exercise');
    if(!wrapper) return;
    const input = wrapper.querySelector('input');
    const fb = wrapper.querySelector('.exercise-feedback');
    const expectedRaw = wrapper.getAttribute('data-expected') || '';
    const expectedList = expectedRaw.split('|').map(e=>normalizeUserValue(e));
    const user = normalizeUserValue(input.value);
    if(!user){
        fb.textContent = '📝 Écris ta réponse.';
        fb.style.color = 'var(--warning, var(--warning))';
        // Force same background as help boxes even for empty input message
        fb.className = 'exercise-feedback exercise-feedback--helplike';
        fb.style.setProperty('background','var(--bg-secondary)','important');
        fb.style.setProperty('border-left','3px solid var(--warning, var(--warning))','important');
        fb.style.setProperty('padding','.45rem .6rem','important');
        fb.style.setProperty('border-radius','6px','important');
        return;
    }
    if(expectedList.includes(user)){
    // Affichage succès (structure harmonisée)
    applySuccessFeedback(fb, false);
        input.disabled = true; btn.disabled = true;
        const section = wrapper.closest('[data-section]')?.getAttribute('data-section') || 'exercices-n1';
        const exId = wrapper.getAttribute('data-ex-id') || expectedRaw;
        let weight = 1; if(section === 'exercices-n2') weight = 2; if(section === 'exercices-n3') weight = 3;
        registerScore(section, 'exercise-'+exId, weight);
        const card = wrapper.closest('.card');
        if(card){
            const solutionEl = card.querySelector('.solution');
            if(solutionEl && !solutionEl.dataset.injected){
                solutionEl.setAttribute('hidden','');
                // Récupère solution complète à partir du full stocké si existant
                let original = solutionEl.dataset.full || solutionEl.innerHTML;
                const { solutionHtml } = extractHintAndSolution(original);
                const container = document.createElement('div');
                container.className = 'inline-solution';
                container.innerHTML = solutionHtml || solutionEl.innerHTML;
                fb.appendChild(container);
                // Icône d'achèvement
                container.insertAdjacentHTML('afterbegin','<div class="solution-badge" aria-hidden="true">✅</div>');
                solutionEl.dataset.injected = 'true';
                // make feedback visually similar to help
                fb.classList.add('exercise-feedback--helplike');
                // record that this exercise was solved (no implicit hint used here)
            }
        }
    } else {
        // Reset and clear any existing content/styling first
        fb.innerHTML = '';
        fb.className = 'exercise-feedback exercise-feedback--helplike';
        fb.style.setProperty('background','var(--bg-secondary)','important');
        fb.style.setProperty('border-left','3px solid var(--accent,var(--primary))','important');
        fb.style.setProperty('padding','.45rem .6rem','important');
        fb.style.setProperty('border-radius','6px','important');
        
        // Add error message
        const errorMsg = document.createElement('div');
        errorMsg.style.color = 'var(--danger)';
        errorMsg.textContent = '❌ Vérifie la règle et réessaie.';
        fb.appendChild(errorMsg);
        // Fournir explication + solution complète après une erreur (selon la consigne)
        const card = wrapper.closest('.card');
        if(card){
            const solutionEl = card.querySelector('.solution');
            if(solutionEl && !solutionEl.dataset.errorShown){
                // On récupère solution + hint
                let original = solutionEl.dataset.full || solutionEl.innerHTML;
                const { hintHtml, solutionHtml } = extractHintAndSolution(original);
                const container = document.createElement('div');
                container.className = 'inline-solution';
                     // Construire bloc erreur : n'afficher les sous-titres que si contenu
                     let parts = [];
                     if(hintHtml){
                   parts.push('<div class="sol-hint"><span class="hint-icon" aria-hidden="true">💡</span>'+hintHtml+'</div>');
                     }
                     const finalSolution = solutionHtml || extractHintAndSolution(original).solutionHtml || '';
                     if(finalSolution){
                         parts.push('<div class="sol-correction">'+finalSolution+'</div>');
                     }
                     if(parts.length===0){
                         parts.push('<p><em>Aucun détail disponible.</em></p>');
                     }
                     container.innerHTML = parts.join('');
                fb.appendChild(container);
                solutionEl.dataset.errorShown = 'true';
                // mark that a hint was shown for this exercise
                try{ if(window.registerScore){ registerScore(wrapper.closest('[data-section]')?.getAttribute('data-section')||'exercices-n1', 'hint-'+(wrapper.closest('.card')?.querySelector('.exercise')?.getAttribute('data-ex-id')||''), 0, {hint:true}); } }catch(e){}
            }
        }
    }
}

// Score restoration & reset button wiring now relies on external ScoreEngine
document.addEventListener('DOMContentLoaded', ()=>{
    const engine = window.ScoreEngine;
    if(!engine) return;
    const st = engine.getState();
    // Masquer toutes les solutions par défaut (elles seront ouvertes via le bouton ou injectées après validation)
    document.querySelectorAll('.solution').forEach(sol=>{
        if(!sol.dataset.injected){ sol.setAttribute('hidden',''); }
    });
    const resetBtn = document.getElementById('reset-score-btn');
    if(resetBtn){
        resetBtn.addEventListener('click', ()=>{
            if(confirm('Réinitialiser toutes les scores ?')){ engine.resetScores(); location.reload(); }
        });
    }
    // Disable already awarded items heuristically (UI sync)
    Object.keys(st.awarded).forEach(key=>{
        if(key.startsWith('intro-q1')){
            document.querySelectorAll('.quiz-option').forEach(b=> b.disabled = true);
        }
        if(key.startsWith('phase-')){
            const id = key.replace('phase-','');
            const input = document.getElementById(id);
            if(input){
                input.disabled = true;
                const btn = input.nextElementSibling; if(btn) btn.disabled = true;
            }
        }
        if(key.startsWith('retention-')){
            const simpleKey = key.replace('retention-','');
            const card = document.querySelector('.quiz-card[data-retention-item="'+simpleKey+'"]');
            if(card){
                card.classList.add('done');
                card.querySelectorAll('button').forEach(b=> b.disabled = true);
                const fb = document.getElementById('retention-'+simpleKey);
                if(fb){ fb.textContent = '✅ Correct (restauré)'; fb.style.color = 'var(--success)'; }
            }
        }
        if(key.startsWith('method-step-')){
            document.querySelectorAll('.guided-question button').forEach(b=> b.disabled = true);
        }
        if(key.startsWith('trap-q')){
            const trapContainer = document.querySelector('.mini-trap-quiz[data-trap-id="'+key+'"]');
            if(trapContainer){
                trapContainer.classList.add('done');
                trapContainer.querySelectorAll('.trap-option').forEach(b=> b.disabled = true);
                const fb = trapContainer.querySelector('.quiz-feedback');
                if(fb && !fb.textContent.includes('Correct')){ fb.textContent = '✅ Correct (restauré)'; fb.style.color = 'var(--success)'; }
            }
        }
        if(key.startsWith('selfeval-r')){
            const ruleNum = key.replace('selfeval-r','');
            const awarded = st.awarded[key];
            const choice = awarded && awarded.meta ? awarded.meta.choice : null;
            if(choice){
                const input = document.querySelector('input[name="eval-r'+ruleNum+'"][value="'+choice+'"]');
                if(input){ input.checked = true; }
            }
        }
        if(key.startsWith('reactivation-')){
            const day = key.replace('reactivation-','');
            const btn = document.querySelector('.reactivation-add[onclick*="createCalendarEvent('+day+',"]');
            if(btn){ btn.classList.add('done'); btn.setAttribute('title','Déjà ajouté'); }
        }
    });
    // Assign data-ex-id to each exercise for stable keys
    let autoId = 1;
    document.querySelectorAll('.exercise').forEach(ex=>{
        if(!ex.getAttribute('data-ex-id')){
            ex.setAttribute('data-ex-id', 'ex'+autoId++);
        }
        const exKey = 'exercise-'+ex.getAttribute('data-ex-id');
        if(st.awarded[exKey]){
            const input = ex.querySelector('input'); const btn = ex.querySelector('button');
            if(input) input.disabled = true; if(btn) btn.disabled = true;
            const fb = ex.querySelector('.exercise-feedback'); if(fb){
                applySuccessFeedback(fb, true);
                const card = ex.closest('.card');
                if(card){
                    const solutionEl = card.querySelector('.solution');
                    if(solutionEl && !solutionEl.dataset.injected){
                        solutionEl.setAttribute('hidden','');
                        const { solutionHtml } = extractHintAndSolution(solutionEl.innerHTML);
                        const container = document.createElement('div');
                        container.className = 'inline-solution';
                        container.innerHTML = solutionHtml || solutionEl.innerHTML;
                        fb.appendChild(container);
                        solutionEl.dataset.injected = 'true';
                    }
                }
            }
        }
    });
    // Sécurité : forcer style succès sur anciennes restaurations manquées
    setTimeout(()=>{
        document.querySelectorAll('.exercise-feedback').forEach(fb=>{
            if(/Correct \(restauré\)/.test(fb.textContent) || fb.querySelector('.assist-text')?.textContent.includes('restauré')){
                applySuccessFeedback(fb, true);
            }
        });
    },50);

    // Auto-évaluation (fiche synthèse) -> 1 point par règle évaluée (3 max)
    ['r1','r2','r3'].forEach(r=>{
        const radios = document.querySelectorAll('input[name="eval-'+r+'"]');
        radios.forEach(rd=>{
            rd.addEventListener('change', ()=>{
                const key = 'selfeval-'+r;
                if(!st.awarded[key]){
                    registerScore('fiche-synthese', key, 1, { choice: rd.value });
                } else {
                    // Mise à jour de la meta choice si l'utilisateur change (optionnel)
                    const a = st.awarded[key];
                    if(a){ a.meta = { choice: rd.value }; engine.updateScoreDisplays(); }
                }
                // Coloration dynamique
                applyConfidenceColor(r, rd.value);
                buildMiniRecap();
            });
        });
    });
    // Restauration coloration
    ['r1','r2','r3'].forEach(r=>{
        const key = 'selfeval-'+r;
        if(st.awarded[key] && st.awarded[key].meta && st.awarded[key].meta.choice){
            applyConfidenceColor(r, st.awarded[key].meta.choice);
        }
    });
    buildMiniRecap();
});

function applyConfidenceColor(ruleId, level){
    const map = { 'confiant':'conf-level-confiant', 'moyen':'conf-level-moyen', 'pas-confiant':'conf-level-pas-confiant' };
    const cls = map[level];
    if(!cls) return;
    // regle boxes order: r1 -> first .regle-box inside fiche-synthese etc.
    const synth = document.getElementById('fiche-synthese');
    if(!synth) return;
    const boxes = synth.querySelectorAll('.regle-box');
    const idx = ruleId === 'r1' ? 0 : ruleId === 'r2' ? 1 : 2;
    const box = boxes[idx];
    if(!box) return;
    box.classList.remove('conf-level-confiant','conf-level-moyen','conf-level-pas-confiant');
    box.classList.add(cls);
}

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

// =============================
// Mini Récap Recommandation
// =============================
document.addEventListener('score:updated', ()=>{
    buildMiniRecap();
    // Re-évaluer bannière de fin (maîtrise) si progression déjà complète
    updateProgress();
});

function buildMiniRecap(){
    const engine = window.ScoreEngine; if(!engine) return;
    const st = engine.getState();
    const targetParent = document.getElementById('plan-reactivation') || document.querySelector('main');
    if(!targetParent) return;
    let container = document.getElementById('mini-recap-reco');
    if(!container){
        container = document.createElement('div');
        container.id = 'mini-recap-reco';
        container.className = 'mini-recap';
        container.setAttribute('role','region');
        container.setAttribute('aria-label','Recommandation');
        targetParent.appendChild(container);
    }
    const msg = computeRecommendation(st, engine.MAX_POINTS);
    container.className = 'mini-recap mini-recap--'+msg.type;
    container.innerHTML = `
        <h3 class="mini-recap-title">🎯 Recommandation</h3>
        <p class="mini-recap-main">${msg.text}</p>
        ${msg.extra ? `<p class="mini-recap-extra">${msg.extra}</p>`: ''}
        <button type="button" class="mini-recap-reset" onclick="resetScores()" title="Réinitialiser toutes les données (scores & recommandations)">↺ Reset</button>
    `;
    // Append hint-used indicators if any
    const awarded = st.awarded || {};
    const hintKeys = Object.keys(awarded).filter(k=>k.startsWith('hint-'));
    if(hintKeys.length){
        const hintList = document.createElement('div');
        hintList.className = 'mini-recap-hints';
        hintList.innerHTML = '<strong>Indices utilisés :</strong> ' + hintKeys.slice(0,5).map(k=>{
            const meta = awarded[k] && awarded[k].meta ? awarded[k].meta : {};
            const sec = awarded[k] ? awarded[k].section : '';
            const id = k.replace('hint-','');
            return `<span class="hint-badge">💡 ${id || sec}</span>`;
        }).join(' ');
        container.appendChild(hintList);
    }
}

function computeRecommendation(st, MAX_POINTS){
    const awarded = st.awarded || {};
    const getChoice = r => awarded['selfeval-'+r] && awarded['selfeval-'+r].meta ? awarded['selfeval-'+r].meta.choice : null;
    const c1 = getChoice('r1');
    const c2 = getChoice('r2');
    const c3 = getChoice('r3');
    const selfDoneCount = [c1,c2,c3].filter(Boolean).length;
    const globalRatio = st.total / Object.values(MAX_POINTS).reduce((a,b)=>a+b,0);
    const planScore = st.perSection['plan-reactivation'] || 0;
    const planMax = MAX_POINTS['plan-reactivation'] || 4;

    const weakMap = { 'pas-confiant':1, 'moyen':2, 'confiant':3 };
    const rules = [
        {id:'Règle 1 (même signe)', level:c1},
        {id:'Règle 2 (signes différents)', level:c2},
        {id:'Règle 3 (contrôle)', level:c3}
    ];
    const weakRules = rules.filter(r=>r.level==='pas-confiant');
    const mediumRules = rules.filter(r=>r.level==='moyen');

    // Priority logic
    if(selfDoneCount === 0){
        const link = '<a href="#fiche-synthese" onclick="showSection(\'fiche-synthese\')" class="mini-recap-link" aria-label="Aller à la section Fiche Synthèse">📋 Fiche Synthèse</a>';
        return { 
            type:'warning', 
            text:'Commence par l’auto‑évaluation des trois règles dans la section '+link+' (bloc Auto‑évaluation).', 
            extra:'Une fois tes niveaux (Confiant / Moyen / Pas confiant) choisis, une recommandation plus précise apparaîtra.' 
        };
    }
    if(weakRules.length){
        const first = weakRules[0];
        const synthLink = '<a href="#fiche-synthese" onclick="showSection(\'fiche-synthese\')" class="mini-recap-link">Fiche Synthèse</a>';
        const reglesLink = '<a href="#retention" onclick="showSection(\'retention\')" class="mini-recap-link">Règles</a>';
        return { type:'danger', text:first.id+' : niveau « pas confiant » → relis dans '+reglesLink+' puis valide dans '+synthLink+'. Entraîne-toi via <a href="#exercices-n1" onclick="showSection(\'exercices-n1\')" class="mini-recap-link">Ex N1</a> & <a href="#exercices-n2" onclick="showSection(\'exercices-n2\')" class="mini-recap-link">Ex N2</a>.', extra:'Priorité : sécuriser les bases avant de poursuivre.' };
    }
    if(globalRatio < .40){
        return { type:'warning', text:'Progression globale < 40% : fais 2 quiz dans <a href="#phases" onclick="showSection(\'phases\')" class="mini-recap-link">Quiz Phases</a> puis 2 exercices dans <a href="#exercices-n1" onclick="showSection(\'exercices-n1\')" class="mini-recap-link">Ex N1</a>.', extra:null };
    }
    // Check low sections (phases, exercices-n2/n3)
    const lowSection = ['phases','exercices-n2','exercices-n3'].find(sec => {
        const val = st.perSection[sec] || 0; const max = MAX_POINTS[sec]||0; return max && (val/max) < .5;
    });
    if(lowSection){
        const labelMap = { 'phases':'Quiz Phases', 'exercices-n2':'Exercices N2', 'exercices-n3':'Exercices N3' };
        return { type:'warning', text:'Renforce <a href="#'+lowSection+'" onclick="showSection(\''+lowSection+'\')" class="mini-recap-link">'+labelMap[lowSection]+'</a> (<50%). Cible 2 items supplémentaires.', extra:null };
    }
    if(planScore === 0){
        return { type:'info', text:'Plan de réactivation non démarré : ajoute J+1 dans <a href="#plan-reactivation" onclick="showSection(\'plan-reactivation\')" class="mini-recap-link">Plan de réactivation</a>.', extra:null };
    }
    if(planScore < planMax){
        return { type:'info', text:'Réactivation en cours : ajoute les étapes restantes dans <a href="#plan-reactivation" onclick="showSection(\'plan-reactivation\')" class="mini-recap-link">Plan de réactivation</a> (J+'+(['1','4','8','15'].filter(d=> !awarded['reactivation-'+d]).join(', '))+').', extra:null };
    }
    if(mediumRules.length){
        return { type:'info', text:'Tu peux consolider : '+mediumRules.map(r=>r.id).join(', ')+' (niveau « moyen ») via <a href="#exercices-n2" onclick="showSection(\'exercices-n2\')" class="mini-recap-link">Ex N2</a> puis <a href="#exercices-n3" onclick="showSection(\'exercices-n3\')" class="mini-recap-link">Ex N3</a>.', extra:'Astuce : vérifie ensuite dans la <a href="#fiche-synthese" onclick="showSection(\'fiche-synthese\')" class="mini-recap-link">Fiche Synthèse</a> si le ressenti progresse.' };
    }
    if(globalRatio >= .70 && c1==='confiant' && c2==='confiant' && c3==='confiant'){
        return { type:'success', text:'Base solide : explore d’autres chapitres ou crée des variantes dans <a href="#exercices-n3" onclick="showSection(\'exercices-n3\')" class="mini-recap-link">Ex N3</a>.', extra:null };
    }
    return { type:'info', text:'Poursuis dans <a href="#exercices-n3" onclick="showSection(\'exercices-n3\')" class="mini-recap-link">Exercices N3</a> pour consolider ta maîtrise.', extra:null };
}
