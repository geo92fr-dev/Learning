# 📋 RÉTRO-SPÉCIFICATION - Système Éducatif 4ème
*Limite: 4. *3. **🚶 Apprendre étape par étape** (section unifiée)
   - 3.1. Visualisation (droite graduée SVG interactive + astuce navigation)
   - 3.2. Étapes guidées (Situer → Comparer → Calculer)
   - 3.3. Devenir autonome (100% guidé → semi-guidé → seul)
4. **💡 Méthode** - Règles encadrées + exemples concretsisualisation** - SVG interactif avec code couleur
5. **💡 Méthode** - Règles encadrées + exemples concrets
5. **🧠 Comprendre les erreurs fréquentes** (section unifiée)
   - 5.1. Les erreurs qui reviennent souvent (repérage + cartes Faux/Correct)
   - 5.2. Ce qu'il faut retenir pour ne plus les refaire (règles synthèse : signes différents / identiques, test mental)
   - 5.3. Pièges à éviter (anticipation + mini cas "Trouve l'erreur")
6. **✅ Auto-contrôle** - Checklist validation
7. **🗓️ Réactivation** - J+1, J+3, J+7, J+14 + **📅 Google Calendar**aractères | Actuel: ~4800 | Basée sur : `College_4ieme_Maths\01_Nombres_relatifs`*

## 🎯 **Architecture Globale**
```
Project_Learning_Simplified/
├── 📊 index_4ieme_master.html
├── 📚 College_4ieme_[MATIERE]/ (12 matières)
│   └── 📖 [NN]_[CHAPITRE]/ (12 chapitres)
│       ├── 📝 cours/ (Contenu principal)
│       ├── ✏️ exercices/ (3 niveaux)
│       └── 📋 fiches_resume/ (Synthèse)
```

## 📖 **STRUCTURE STANDARD**

### **📂 `/cours`**
- `cours_principal.html` - Contenu principal
- `data_chapitre.json` - Métadonnées

### **📂 `/exercices`**
- `exercices_niveau1_decouverte.html` - Découverte guidée
- `exercices_niveau2_pratique.html` - Application directe  
- `exercices_niveau3_defi.html` - Approfondissement

### **📂 `/fiches_resume`**
- `fiche_synthese.html` - Quiz interactif
- `fiche_methode.html` - Procédures
- `fiche_memorisation.html` - Points-clés

## 🎨 **DESIGN UNIFIÉ**

### **🎨 Système de Variables CSS (Octobre 2025)**
**Architecture centralisée** : `styles/variables.css` → `base.css` → `components.css`

#### **📋 Structure des Fichiers CSS**
```
styles/
├── variables.css     # ⭐ Variables centralisées (NOUVEAU)
├── base.css         # Reset + Layout global
└── components.css   # Composants réutilisables
```

#### **🎯 Variables Principales**
```css
/* Couleurs principales */
--primary: #67c7ff           /* Bleu mathématiques */
--accent: #67c7ff            /* Accent (même que primary) */

/* Couleurs sémantiques */
--success: #10b981           /* Vert succès */
--warning: #f59e0b           /* Orange avertissement */
--danger: #ef4444            /* Rouge erreur/échec */

/* Couleurs mathématiques spécialisées */
--math-positive: #10ac84     /* Vert nombres positifs */
--math-negative: #ff6b6b     /* Rouge nombres négatifs */
--math-neutral: #ff9f43      /* Orange zéro/neutre */
--math-axis: #67c7ff         /* Bleu axes/droites */
--math-highlight: #00d2d3    /* Cyan mise en évidence */

/* Fonds */
--bg-primary: #ffffff        /* Fond principal */
--bg-secondary: #f8fafc      /* Cartes, aides "Besoin d'aide ?" */
--bg-tertiary: #f1f5f9       /* Fond tertiaire */
--bg-card: #ffffff           /* Fond des cartes */
--bg-input: #f9fafb         /* Champs de saisie */
--bg-hover: #f0f9ff         /* Survol */

/* Transparences (nouvelles) */
--primary-alpha-05: rgba(103, 199, 255, 0.05)
--primary-alpha-15: rgba(103, 199, 255, 0.15)
--success-alpha-35: rgba(16, 185, 129, 0.35)
--warning-alpha-40: rgba(245, 158, 11, 0.4)
```

#### **🔧 Migration Effectuée**
✅ **JavaScript** : `main.js` 
- `#10b981` → `var(--success)`
- `#ef4444` → `var(--danger)`  
- `#f59e0b` → `var(--warning)`

✅ **CSS** : `components.css`
- Suppression des définitions codées en dur
- Utilisation systématique des variables

✅ **Styles spéciaux** : `memo-styles.css`
- `#67c7ff` → `var(--primary)`
- `rgba(103, 199, 255, *)` → `var(--primary-alpha-*)`

✅ **SVG dynamique** : `cours_principal.html`
- Script JavaScript pour appliquer les variables CSS aux éléments SVG
- Support des couleurs mathématiques spécialisées

#### **💡 Avantages du Système**
- **Cohérence** : Une seule source de vérité pour les couleurs
- **Maintenabilité** : Modification centralisée possible
- **Évolutivité** : Thème sombre facilement implémentable
- **Performance** : Variables CSS natives (pas de préprocesseur)

#### **📏 Autres Variables Standardisées**
```css
/* Espacements */
--space-xs: 0.25rem  --space-sm: 0.5rem   --space-md: 1rem
--space-lg: 1.5rem   --space-xl: 2rem     --space-xxl: 3rem

/* Rayons */
--radius-sm: 4px     --radius-md: 6px     --radius-lg: 8px
--radius-xl: 12px    --radius-full: 9999px

/* Ombres */
--shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05)
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1)
--shadow-primary: 0 4px 15px var(--primary-alpha-20)

/* Transitions */
--transition-fast: 150ms ease
--transition-normal: 250ms ease
--transition-slow: 350ms ease
```

### **Palette CSS Héritée** 
```css
--bg-primary: #0f1115    --text-primary: #f5f7fa
--bg-card: #141a21       --accent-blue: #67c7ff
--border-subtle: #1b222c --success-green: #10ac84
.btn-calendar-mini: #059669 + flexbox gap:0.5rem
.reactivation-item: display:flex align-items:center
```

### **Navigation Standard**
```html
<nav>
 <a href='../exercices/exercices_niveau1_decouverte.html'>Exercice Niveau 1</a>
 <a href='../exercices/exercices_niveau2_pratique.html'>Exercice Niveau 2</a>
 <a href='../exercices/exercices_niveau3_defi.html'>Exercice Niveau 3</a>
 <a href='../fiches_resume/fiche_synthese.html'>Synthèse</a>
</nav>
```

## 📝 **CONTENU PÉDAGOGIQUE**

### **Structure Cours Principal**
1. **🎯 Introduction** - Accroche concrète + objectif clair
2. **🛠️ Prérequis** - Cartes interactives avec mini-tests
3. **🚶 Apprendre étape par étape** (section unifiée)
   - 3.1. Étapes guidées (Situer → Comparer → Calculer)
   - 3.2. Devenir autonome (100% guidé → semi-guidé → seul)
5. **🎨 Visualisation** - SVG interactif avec code couleur
6. **💡 Méthode** - Règles encadrées + exemples concrets
7. **🧠 Comprendre les erreurs fréquentes** (section unifiée)
  - 1. Les erreurs qui reviennent souvent (repérage + cartes Faux/Correct)
  - 2. Ce qu’il faut retenir pour ne plus les refaire (règles synthèse : signes différents / identiques, test mental)
  - 3. Pièges à éviter (anticipation + mini cas "Trouve l'erreur")
8. **✅ Auto-contrôle** - Checklist validation
9. **🗓️ Réactivation** - J+1, J+3, J+7, J+14 + **📅 Google Calendar**

### **Structure Exercices**
- **Niveau 1** - Découverte guidée (5 max, contextes concrets)
- **Niveau 2** - Application directe (difficulté progressive)
- **Niveau 3** - Défi et approfondissement

### **Fiche Synthèse**
1. Règles colorées encadrées
2. Droite graduée interactive
3. Exemples de pièges
4. Quiz 5 niveaux + score dynamique
5. Hints gradués

### **💬 Éléments Interactifs**
- **Textbox + Validation** : `.quiz-textbox` + `.quiz-btn` (pattern fiche_synthese.html)
- **3 Phases Autonomie** : Phase 1 (100% guidé), Phase 2 (Semi-guidé), Phase 3 (Autonome 🏆)
- **Feedback Temps Réel** : `.feedback-success` (vert), `.feedback-error` (rouge), `.feedback-neutral` (bleu)
- **JavaScript** : `checkPhaseAnswer(phaseNum, correctAnswer, explanation)`
- **Validation Flexible** : Accepte +2, 2, ou variantes textuelles selon contexte
- **État Post-Succès** : Input désactivé, bouton "✓ Validé", couleur verte

### **🎯 Règle Positionnement Icônes**
**RÈGLE :** Tous les éléments avec icônes se placent **juste après les titres** (h2, h3, h4)

**Icônes Uniques par Contexte :**
- 🌍 **Contexte/Objectif** : Situations concrètes et buts pédagogiques
- 💡 **Mini-test/Vérification** : Questions rapides et contrôles
- ⚡ **Mémo/Question clé** : Règles synthèses et points cruciaux  
- 🤔 **Pourquoi** : Justifications pédagogiques et explications
- 🎯 **Défi/Astuce** : Défis autonomes et astuces navigation
- ✅ **Contrôle/Validation** : Étapes de vérification finale
- 🆘 **Besoin d'aide** : Liens vers aide contextuelle

## 📊 **MÉTADONNÉES**

### **`data_chapitre.json`**
```json
{
  "slug": "NN_Nom_chapitre", "titre": "Titre Lisible",
  "objectifs": ["..."], "prerequis": ["..."], "etapes": ["..."],
  "plan_reactivation": ["J+1", "J+3", "J+7", "J+14"],
  "erreurs_frequentes": ["..."], "vocabulaire": [{"terme": "...", "definition": "..."}]
}
```

### **Fonctionnalité Google Calendar** 
- **Boutons individuels** : 📅 en début de chaque ligne J+1, J+3, J+7, J+14
- **Ajout personnalisé** : Chaque rappel ajouté séparément selon besoin
- **Auto-génération** : Événements à 18h00 avec titre/description adaptés
- **Feedback ciblé** : Alert personnalisé par type (découverte, pratique, etc.)
- **Interface optimisée** : Flexbox, boutons compacts, UX intuitive
- **JavaScript** : `addSingleEventToCalendar()` + event listeners individuels

## 🛠️ **TECHNIQUE**

### **Technologies**
- HTML5, CSS3, JavaScript, SVG
- Responsive mobile-first
- Compatible Chrome/Firefox/Edge/Safari
- Fonctionnement offline

### **Scripts Maintenance**
```python
optimize_all_subjects_structure.py       # Nettoyage dossiers
uniformize_cours_navigation.py           # Navigation
validate_navigation_cleanup.py           # Validation
add_google_calendar_to_courses.py        # Intégration Google Calendar
update_calendar_individual_buttons.py    # Migration boutons individuels
```

## 🎯 **PÉDAGOGIE**

### **Public & Approche**
- **Cible** : Élèves 4ème avec difficultés d'apprentissage
- **Méthode** : Progressive, bienveillante, fading
- **Progression** : Cours → Ex N1 → Ex N2/N3 → Synthèse
- **Réactivation** : J+1, J+3, J+7, J+14

### **Ton & Style**
- Direct et bienveillant, tutoiement
- Émojis cohérents, code couleur pédagogique
- Formatage : `<strong>` essentiels, `<em>` exemples, `<code>` formules

### **🛠️ Bonnes Pratiques CSS (Variables)**

#### **✅ À FAIRE**
```css
/* ✅ Utiliser les variables */
.exercise-feedback { background: var(--bg-secondary); }
.success-message { color: var(--success); }
.math-positive { color: var(--math-positive); }

/* ✅ Avec fallback pour compatibilité */
background: var(--primary, #67c7ff);

/* ✅ Combinaisons avec transparence */
box-shadow: 0 0 0 3px var(--success-alpha-35);
```

#### **❌ ÉVITER**
```css
/* ❌ Couleurs codées en dur */
color: #10b981;
background: #f8fafc;

/* ❌ Magic numbers */
padding: 16px;  /* → var(--space-md) */
border-radius: 8px;  /* → var(--radius-lg) */
```

#### **📱 Application dans JavaScript**
```javascript
// ✅ Utiliser les variables CSS
feedback.style.color = 'var(--success)';
fb.style.setProperty('background', 'var(--bg-secondary)', 'important');

// ✅ Pour SVG (nécessite script)
const primaryColor = getComputedStyle(root).getPropertyValue('--primary').trim();
svgElement.setAttribute('fill', primaryColor);
```

#### **🔄 Workflow Mise à Jour**
1. **Modifier** `variables.css` uniquement
2. **Tester** sur plusieurs composants
3. **Vérifier** JavaScript et SVG
4. **Commit** avec message descriptif

#### **🎨 Guide Couleurs Mathématiques**
- **Positif** : `var(--math-positive)` → +7, +15, etc.
- **Négatif** : `var(--math-negative)` → -3, -12, etc.  
- **Zéro/Neutre** : `var(--math-neutral)` → 0, points neutres
- **Axes/Droites** : `var(--math-axis)` → droite graduée, axes
- **Highlight** : `var(--math-highlight)` → résultats, focus

## 🚀 **DÉPLOIEMENT**

### **Organisation**
- Nommage : `NN_Nom_chapitre`
- Encodage UTF-8, liens relatifs
- Git avec commits descriptifs

### **🎨 CSS Architecture (Nouveau Standard)**
```html
<!-- Ordre d'inclusion OBLIGATOIRE -->
<link rel="stylesheet" href="styles/variables.css">  <!-- 1. Variables -->
<link rel="stylesheet" href="styles/base.css">      <!-- 2. Base -->
<link rel="stylesheet" href="styles/components.css"> <!-- 3. Composants -->
```

### **Qualité**
- Structure standard respectée
- Navigation fonctionnelle
- Responsive + accessibilité
- Performance < 2s
- **NOUVEAU** : Variables CSS cohérentes

### **📊 Checklist Validation CSS**
- [ ] `variables.css` inclus en premier
- [ ] Aucune couleur codée en dur (`#ffffff`, `rgb()`)
- [ ] Variables sémantiques utilisées (`--success`, `--danger`)
- [ ] Couleurs mathématiques pour contenus spécialisés
- [ ] SVG mis à jour par script JavaScript
- [ ] Compatibilité mobile testée

### **🔮 Évolutions Prévues**

#### **Phase 2 : Thème Sombre (À Venir)**
```css
@media (prefers-color-scheme: dark) {
  :root {
    --bg-primary: #0f172a;
    --bg-secondary: #1e293b; 
    --text-primary: #f1f5f9;
    /* Couleurs math inchangées pour contraste */
  }
}
```

#### **Phase 3 : Variables Matières**
- Variables spécifiques par matière (Français, Sciences, etc.)
- Palette étendue pour besoins disciplinaires
- Système de thèmes commutables

### **🛠️ Maintenance Variables CSS**

#### **Vérification Périodique**
```bash
# Rechercher couleurs codées en dur oubliées
grep -r "#[0-9a-fA-F]\{6\}" styles/ scripts/
grep -r "rgb\(" styles/ scripts/

# Vérifier utilisation variables
grep -r "var(--" styles/ scripts/
```

#### **Tests de Régression**
- Vérifier toutes les couleurs après modification `variables.css`
- Tester sur 3 navigateurs minimum (Chrome, Firefox, Safari)
- Validation mobile + mode sombre si implémenté

## 📊 **MÉTRIQUES**
- Engagement, scores quiz, progression
- Performance, stabilité JavaScript
- Accessibilité Lighthouse >90

---
*Spécification 28/09/2025 - Référence système 4ème*
*✨ MAJ : Google Calendar avec boutons individuels optimisés ; Section erreurs unifiée (3 niveaux : repérer / retenir / éviter)*