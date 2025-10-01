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
        registerScore('phases', 'phase-'+inputId, 1);
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
        registerScore('introduction', 'intro-q1', 1);
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
        registerScore('retention', 'retention-'+inputId, 1);
    } else {
        feedback.textContent = '❌ Relisez la règle correspondante ci-dessus.';
        feedback.style.color = '#ef4444';
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
        fb.textContent = '✅ Correct'; fb.style.color = '#10b981';
        registerScore('retention','retention-'+key,1);
    } else {
        fb.textContent = '❌ Faux'; fb.style.color = '#ef4444';
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
        fb.textContent = '✅ Correct : soustraction des valeurs absolues'; fb.style.color = '#10b981';
        registerScore('retention','retention-'+key,1);
    } else {
        fb.textContent = '❌ Non, on soustrait les valeurs absolues (réponse B)'; fb.style.color = '#ef4444';
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
        feedback.style.color = '#10b981';
        registerScore('methodes', 'method-step-'+step, 1);
        // highlight correct button
        event?.target?.classList?.remove('btn--secondary');
        event?.target?.classList?.add('btn--primary');
    } else {
        feedback.textContent = '❌ ' + message;
        feedback.style.color = '#ef4444';
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
        if(feedback){ feedback.textContent = '✅ ' + message; feedback.style.color = '#10b981'; }
        registerScore('pieges', key, 1);
    } else {
        button.classList.add('btn--danger','quiz-option--wrong');
        if(feedback){ feedback.textContent = '❌ ' + message; feedback.style.color = '#ef4444'; }
        const correctBtn = Array.from(buttons).find(b => b.dataset.correct === 'true');
        if (correctBtn) correctBtn.classList.add('btn--primary','quiz-option--correct');
    }
    button.setAttribute('aria-pressed','true');
    container.classList.add('done');
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
function checkExerciseAnswer(btn){
    const wrapper = btn.closest('.exercise');
    if(!wrapper) return;
    const input = wrapper.querySelector('input');
    const fb = wrapper.querySelector('.exercise-feedback');
    const expectedRaw = wrapper.getAttribute('data-expected') || '';
    const expectedList = expectedRaw.split('|').map(e=>normalizeUserValue(e));
    const user = normalizeUserValue(input.value);
    if(!user){
        fb.textContent = '📝 Entrez une réponse.';
        fb.style.color = 'var(--warning, #f59e0b)';
        return;
    }
    if(expectedList.includes(user)){
        fb.textContent = '✅ Correct !';
        fb.style.color = '#10b981';
        input.disabled = true; btn.disabled = true;
        // Determine section by DOM (closest h2 id marker already separated by sections)
        const section = wrapper.closest('[data-section]')?.getAttribute('data-section') || 'exercices-n1';
        const exId = wrapper.getAttribute('data-ex-id') || expectedRaw;
        // Weight: N1=1, N2=2, N3=3
        let weight = 1;
        if(section === 'exercices-n2') weight = 2;
        if(section === 'exercices-n3') weight = 3;
        registerScore(section, 'exercise-'+exId, weight);
    } else {
        fb.textContent = '❌ Vérifie les règles et réessaie.';
        fb.style.color = '#ef4444';
    }
}

// Score restoration & reset button wiring now relies on external ScoreEngine
document.addEventListener('DOMContentLoaded', ()=>{
    const engine = window.ScoreEngine;
    if(!engine) return;
    const st = engine.getState();
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
                if(fb){ fb.textContent = '✅ Correct (restauré)'; fb.style.color = '#10b981'; }
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
                if(fb && !fb.textContent.includes('Correct')){ fb.textContent = '✅ Correct (restauré)'; fb.style.color = '#10b981'; }
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
            const fb = ex.querySelector('.exercise-feedback'); if(fb){ fb.textContent = '✅ Correct (restauré)'; fb.style.color = '#10b981'; }
        }
    });

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
        return { type:'warning', text:'Commence par l’auto-évaluation des 3 règles dans la fiche synthèse.', extra:null };
    }
    if(weakRules.length){
        const first = weakRules[0];
        return { type:'danger', text:first.id+' : tu t’es déclaré « pas confiant » → relis la règle puis fais Ex N1 (Ex 5) et un Ex N2.', extra:'Priorité : sécuriser les bases avant de poursuivre.' };
    }
    if(globalRatio < .40){
        return { type:'warning', text:'Progression globale < 40% : refais 2 quiz Phase 1 puis 2 exercices N1.', extra:null };
    }
    // Check low sections (phases, exercices-n2/n3)
    const lowSection = ['phases','exercices-n2','exercices-n3'].find(sec => {
        const val = st.perSection[sec] || 0; const max = MAX_POINTS[sec]||0; return max && (val/max) < .5;
    });
    if(lowSection){
        return { type:'warning', text:'Renforce la section « '+lowSection+' » (<50%). Cible 2 items supplémentaires.', extra:null };
    }
    if(planScore === 0){
        return { type:'info', text:'Plan de réactivation non démarré : ajoute J+1 à ton agenda.', extra:null };
    }
    if(planScore < planMax){
        return { type:'info', text:'Réactivation en cours : ajoute les étapes restantes (J+'+(['1','4','8','15'].filter(d=> !awarded['reactivation-'+d]).join(', '))+').', extra:null };
    }
    if(mediumRules.length){
        return { type:'info', text:'Tu peux consolider : '+mediumRules.map(r=>r.id).join(', ')+' (niveau « moyen »).', extra:'Fais 1 ex N2 et 1 ex N3 pour chaque règle.' };
    }
    if(globalRatio >= .70 && c1==='confiant' && c2==='confiant' && c3==='confiant'){
        return { type:'success', text:'Base solide : enchaîne vers le chapitre suivant ou crée tes propres exemples.', extra:null };
    }
    return { type:'info', text:'Continue sur les exercices N3 pour consolider ta maîtrise.', extra:null };
}
