# Architecture de Composants - Spécifications Techniques

## 🧩 Système de Composants Standardisés

### 1. Quiz Component - Composant de Base Réutilisable

#### Structure HTML Template
```html
<template id="quiz-component-template">
  <div class="quiz-block" data-component="quiz">
    <input 
      type="text" 
      class="quiz-input" 
      placeholder="Ta réponse"
      maxlength="10"
    >
    <button type="button" class="quiz-button">
      ✓ Valider
    </button>
    <div class="quiz-feedback" aria-live="polite"></div>
  </div>
</template>
```

#### Utilisation Simplifiée
```html
<!-- Au lieu de répéter le code 20 fois -->
<quiz-component 
  id="phase1"
  answer="+2"
  explanation-key="phase1"
  type="phase">
</quiz-component>

<quiz-component 
  id="method1"
  answer="-14" 
  explanation-key="checkM1"
  type="method"
  size="mini">
</quiz-component>
```

## 🎨 Système de Tokens CSS - Variables Centralisées

### Avantage Principal
**Changement d'une couleur = 1 seule ligne à modifier**

```css
/* tokens.css - SEUL POINT DE MODIFICATION */
:root {
  --primary-color: #67c7ff; /* ← Changer ICI seulement */
  --font-size-base: 0.8rem;  /* ← Ajuster ICI seulement */
}

/* Répercussion automatique dans TOUS les composants */
.quiz-button { background: var(--primary-color); }
.card-title { color: var(--primary-color); }
.progress-bar { background: var(--primary-color); }
```

## 📂 Structure de Fichiers Proposée

```
cours/
├── cours_principal.html (30% plus léger)
├── components/
│   ├── quiz-component.js
│   ├── card-component.js
│   └── progress-component.js
├── sections/
│   ├── retention-rules.html ✅
│   ├── method-illustrated.html
│   └── pitfalls-avoid.html
├── design/
│   ├── tokens.css (variables globales)
│   ├── components.css (styles composants)
│   └── layouts.css (grilles, alignements)
└── scripts/
    ├── app.js (orchestrateur)
    └── component-loader.js
```

## 🚀 Bénéfices Concrets

### Maintenir Couleurs (exemple concret)
**AVANT** : Modifier 47 endroits dans le fichier
**APRÈS** : Modifier 1 variable dans tokens.css

### Ajouter Quiz
**AVANT** : Copier-coller 15 lignes + risque d'erreur
**APRÈS** : `<quiz-component id="newquiz" answer="5">`

### Corriger Bug
**AVANT** : Bug répété dans 20 quiz différents
**APRÈS** : 1 correction dans quiz-component.js

## 📋 Plan d'Implémentation

### Phase 1 - Urgence (15 min)
1. ✅ Créer section retention propre
2. 🔄 Remplacer section corrompue
3. 🔄 Ajouter mémo 🎯

### Phase 2 - Fondations (45 min)
1. Créer système de tokens CSS
2. Extraire composants quiz répétés
3. Créer loader de sections

### Phase 3 - Migration (2h)
1. Migrer toutes les sections
2. Unifier tous les quiz
3. Tests et validation

## 🤝 Décision Requise

Voulez-vous que je commence par :
- **🚨 Correction urgente** de la section corrompue ?
- **🏗️ Architecture complète** (plus long mais plus propre) ?

Ma recommandation : **Correction urgente PUIS architecture progressive**