# 📋 RÉTRO-SPÉCIFICATION - Système Éducatif 4ème
*Limite: 4. **🎨 Visualisation** - SVG interactif avec code couleur
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

### **Palette CSS**
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

## 🚀 **DÉPLOIEMENT**

### **Organisation**
- Nommage : `NN_Nom_chapitre`
- Encodage UTF-8, liens relatifs
- Git avec commits descriptifs

### **Qualité**
- Structure standard respectée
- Navigation fonctionnelle
- Responsive + accessibilité
- Performance < 2s

## 📊 **MÉTRIQUES**
- Engagement, scores quiz, progression
- Performance, stabilité JavaScript
- Accessibilité Lighthouse >90

---
*Spécification 28/09/2025 - Référence système 4ème*
*✨ MAJ : Google Calendar avec boutons individuels optimisés ; Section erreurs unifiée (3 niveaux : repérer / retenir / éviter)*