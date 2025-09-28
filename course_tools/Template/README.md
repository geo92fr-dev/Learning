# 📚 Templates de Cours - Système Final Simplifié

## 🎯 Vue d'ensemble

Système de templates nettoyé et optimisé pour créer des cours de mathématiques 4ème adaptés aux élèves en difficulté.

**Contact élève :** lucasgeoffroy2701@gmail.com

## 📁 Fichiers essentiels (4 fichiers uniquement)

### 1. Template HTML
- **`index_master_template.html`** - Template pour pages d'index
  - Design moderne et responsive
  - Sans trimestres, sans vue d'ensemble
  - Focus direct sur les chapitres
  - Mode sombre intégré

### 2. Données JSON
- **`exemple_index_master_simple.json`** - Structure de données
  - 12 chapitres de 4ème mathématiques
  - Format simple sans complexité
  - Prêt à personnaliser

### 3. Script Python  
- **`inject_master_simple.py`** - Générateur optimisé
  - Injection automatique des données
  - Compatible avec le template simplifié
  - Une commande = page prête

### 4. Documentation
- **`README_Templates.md`** - Ce fichier guide

## 🚀 Utilisation (ultra-simple)

### Générer une page d'index
```bash
python inject_master_simple.py exemple_index_master_simple.json index_master_template.html ma_page.html
```

### Personnaliser
1. Modifier `exemple_index_master_simple.json` (titres, descriptions, liens)
2. Relancer la génération
3. Ouvrir `ma_page.html` dans le navigateur

## ✨ Caractéristiques

### Design
- **Moderne** : Dégradés, animations, cartes
- **Responsive** : Tablette, mobile, desktop
- **Accessible** : Mode sombre, contrastes, navigation clavier

### Structure
- **Directe** : Header → 12 cartes de chapitres
- **Simple** : Pas de navigation complexe
- **Informative** : Difficulté, objectifs, liens

### Optimisations pour élèves en difficulté
- Interface épurée et non intimidante
- Navigation intuitive
- Informations claires et bien structurées
- Feedback visuel encourageant

## 🎓 Adapté pour Lucas - 4ème Mathématiques
- Approche progressive et bienveillante
- 12 chapitres essentiels du programme
- Interface motivante et accessible

## 📋 Variables JSON principales

### Globales
- `MATIERE` : "Mathématiques"
- `NIVEAU` : "4ème" 
- `ELEVE_TYPE` : "élèves en difficulté"
- `ANNEE` : "2025"

### Par chapitre
- `CHAPITRE_NUM` : Numéro (1-12)
- `CHAPITRE_TITRE` : Titre du chapitre
- `CHAPITRE_DESCRIPTION` : Description courte
- `CHAPITRE_DIFFICULTE` : 1=Facile, 2=Moyen, 3=Difficile
- `CHAPITRE_OBJECTIFS` : Liste des objectifs
- `CHAPITRE_LIEN_*` : Liens vers cours/exercices/fiches

## 🎯 Résultat

**Une page d'index moderne** avec 12 cartes de chapitres, design professionnel, navigation directe et interface adaptée aux élèves en difficulté.