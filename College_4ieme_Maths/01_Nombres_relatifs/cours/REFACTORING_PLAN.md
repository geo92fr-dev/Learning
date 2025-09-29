# Plan de Refactoring - Cours Principal

## Problème actuel
- Structure HTML corrompue avec éléments mélangés
- Sections complexes difficiles à maintenir
- Code répétitif et fragile

## Solution proposée : Architecture modulaire

### 1. Structure des fichiers
```
cours/
├── cours_principal.html (fichier principal allégé)
├── sections/
│   ├── erreurs-frequentes.html
│   ├── regles-retention.html ✅ (créé)
│   ├── pieges-eviter.html
│   ├── methode-illustree.html
│   └── apprentissage-progressif.html
├── styles/
│   ├── base.css (styles de base)
│   ├── memo-styles.css ✅ (créé)
│   └── components.css (quiz, cartes, etc.)
└── scripts/
    ├── section-loader.js ✅ (créé)
    ├── quiz-handler.js
    └── interactive-elements.js
```

### 2. Avantages immédiats
✅ **Maintenance facilitée** - 1 fichier = 1 responsabilité
✅ **Évite les corruptions** - sections isolées
✅ **Réutilisabilité** - sections réutilisables dans d'autres cours
✅ **Lisibilité** - code plus petit et focalisé
✅ **Collaboration** - plusieurs personnes peuvent travailler simultanément

### 3. Migration progressive
1. **Phase 1** (immédiat) : Corriger la section "Ce qu'il faut retenir" ✅
2. **Phase 2** : Externaliser les autres sections corrompues
3. **Phase 3** : Implémenter le système de chargement modulaire
4. **Phase 4** : Migrer toutes les sections

### 4. Actions immédiates recommandées
1. ✅ Créer section retention propre avec mémo 🎯
2. 🔄 Remplacer la section corrompue dans le fichier principal
3. 📦 Créer les autres sections modulaires
4. 🚀 Implémenter le loader automatique

## Temps estimé
- Correction immédiate: 15 min
- Refactoring complet: 2-3h
- Bénéfices: Maintenance 3x plus rapide

Voulez-vous que je commence par corriger immédiatement le problème actuel puis implémenter le refactoring ?