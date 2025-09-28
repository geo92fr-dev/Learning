# Déploiement des cours 4ème sur GitHub Pages

## 1. Dépôt distant
URL distante stockée dans `GitHub.txt` :
```
https://github.com/geo92fr-dev/Learning.git
```

## 2. Initialisation locale (à exécuter une fois)
```
git init
git add .
git commit -m "Initial commit : contenu cours 4ème (mode sombre permanent + index matières)"
git branch -M main
git remote add origin https://github.com/geo92fr-dev/Learning.git
git push -u origin main
```

## 3. Activer GitHub Pages
Dans le dépôt GitHub :
1. Settings > Pages
2. Build and deployment : Source = Deploy from a branch
3. Branch = `main` / folder = `/ (root)`
4. Sauvegarder

URL probable après activation :
```
https://geo92fr-dev.github.io/Learning/index_4ieme_master.html
```

## 4. Structure importante
- `index_4ieme_master.html` : page d'accueil principale
- `College_4ieme_Maths/index_master_4ieme.html` et autres matières : index par matière
- Sous-dossiers chapitre : ex. `College_4ieme_Maths/01_Nombres_relatifs/...`

## 5. Ajouter de nouveaux contenus
Après génération/enrichissement :
```
git add .
git commit -m "Ajout contenus: maths chapitres X à Y"
git push
```

## 6. Vérification après déploiement
- Ouvrir l’URL GitHub Pages
- Vérifier liens relatifs (navigation matières/chapitres)
- Si cache : forcer Ctrl+F5

## 7. Bonnes pratiques
- Commits courts et descriptifs
- Éviter d’ajouter des fichiers volumineux inutiles
- Pas de données personnelles (anonymiser si nécessaires)

## 8. Options futures
- Ajouter un workflow GitHub Actions (validation liens)
- Génération automatique d’index via script
- Compression/minification optionnelle

---
Dernière mise à jour : 28/09/2025
