// Scoring Engine Module (externalized)
// Responsibility: manage score state, persistence, and DOM display updates.
// Keeps backward compatibility by exposing original function names (registerScore, resetScores, updateScoreDisplays).
(function(global){
    'use strict';

    const SCORE_STORAGE_KEY = 'relatifs_scores_v1';
    // Section labels (not strictly required for logic but exposed for UI customisation)
    const SECTION_LABELS = {
        'introduction':'Introduction',
        'retention':'Règles',
        'phases':'Quiz',
        'methodes':'Méthodes',
        'pieges':'Pièges',
        'exercices-n1':'Ex N1',
        'exercices-n2':'Ex N2',
        'exercices-n3':'Ex N3',
        'fiche-synthese':'Synthèse',
        'plan-reactivation':'Réactivation'
    };

    // Barème maximum par section (modifiable sans toucher le HTML principal)
    const MAX_POINTS = {
        'introduction':1,
        'retention':4,
        'phases':9,
        'methodes':3,
    'pieges':2,
        'exercices-n1':5*1,
        'exercices-n2':5*2,
        'exercices-n3':5*3,
        // 3 auto-évals (règles) = 3 pts potentiels
        'fiche-synthese':3,
        // 4 ajouts agenda = 4 pts
        'plan-reactivation':4
    };
    let GLOBAL_MAX = Object.values(MAX_POINTS).reduce((a,b)=>a+b,0);

    let state = { total:0, perSection:{}, awarded:{} };

    function load(){
        try {
            const raw = localStorage.getItem(SCORE_STORAGE_KEY);
            if(raw){
                const parsed = JSON.parse(raw);
                if(parsed && typeof parsed === 'object') state = parsed;
            }
        } catch(e){ console.warn('[ScoreEngine] load failed', e); }
    }
    function persist(){
        try { localStorage.setItem(SCORE_STORAGE_KEY, JSON.stringify(state)); } catch(e){ /* ignore */ }
    }

    function updateDisplays(){
        // Global score badge
        const g = document.getElementById('global-score');
        if(g){
            g.textContent = 'Score : ' + state.total + ' / ' + GLOBAL_MAX;
            g.classList.add('max-known');
        }
        // Per section
        document.querySelectorAll('[data-section-score]').forEach(span=>{
            const key = span.getAttribute('data-section-score');
            const val = state.perSection[key] || 0;
            const max = MAX_POINTS[key] ?? 0;
            span.textContent = max ? (val + ' / ' + max) : (val + ' / 0');
            const ratio = max ? val / max : 0;
            span.dataset.ratio = ratio.toFixed(2);
            span.classList.remove('level-low','level-mid','level-good','level-excellent');
            if(max){
                if(ratio === 1){ span.classList.add('level-excellent'); }
                else if(ratio >= .66){ span.classList.add('level-good'); }
                else if(ratio >= .33){ span.classList.add('level-mid'); }
                else { span.classList.add('level-low'); }
            }
        });
    }

    function registerScore(section, itemKey, value, meta){
        if(!section || !itemKey || !value) return;
        if(state.awarded[itemKey]) return; // déjà compté
        state.awarded[itemKey] = { section, value, meta: meta || null };
        state.perSection[section] = (state.perSection[section]||0) + value;
        state.total += value;
        persist();
        updateDisplays();
        const span = document.querySelector('[data-section-score="'+section+'"]');
        if(span){ span.classList.add('updated'); setTimeout(()=>span.classList.remove('updated'), 700); }
    }

    function resetScores(){
        state = { total:0, perSection:{}, awarded:{} };
        persist();
        updateDisplays();
    }

    function init(){
        load();
        updateDisplays();
    }

    // Public API
    const api = {
        init,
        registerScore,
        resetScores,
        updateScoreDisplays: updateDisplays,
        getState: () => state,
        MAX_POINTS,
        get GLOBAL_MAX(){ return GLOBAL_MAX; },
        SECTION_LABELS
    };

    // Expose namespaced
    global.ScoreEngine = api;
    // Backward compatibility (existing code / inline handlers)
    global.registerScore = registerScore;
    global.resetScores = resetScores;
    global.updateScoreDisplays = updateDisplays;

    document.addEventListener('DOMContentLoaded', init);
})(window);
