# Outil de génération de cours accessibles (Smartphone / Élève en difficulté)

Ce dossier propose une première approche pour transformer un contenu pédagogique (ex: généré via le template de prompt) en une page HTML très lisible et accessible sur un smartphone.

## Objectifs
- Affichage clair en petits écrans
- Mode contraste et police adaptée Dys
- Segmentation en blocs repliables
- Bouton lecture audio (synthèse vocale Web Speech API)
- Navigation rapide par sections

## Fichiers
- `generate_course_page.py` : Script Python qui prend un fichier Markdown source et génère une page HTML responsive.
- `template_base.html` : Modèle HTML avec styles et scripts d’accessibilité.
- `exemple_fractions.md` : Exemple complet prêt à transformer.
- `generer_cours.bat` : Double-clic Windows pour générer un HTML à partir de l'exemple.
- `course_template_html.html` : Template HTML normalisé avec placeholders `[PLACEHOLDER]`.
- `inject_course.py` : Injecte les valeurs d'un JSON dans `course_template_html.html`.
- `exemple_cours.json` : Exemple de données d'un cours (fractions).

## Utilisation (méthode rapide)
1. Double-cliquez sur `generer_cours.bat` (génère un fichier horodaté : `cours_YYYYMMDD_HHMMSS.html`).
2. Le fichier s'ouvre dans le navigateur.
3. Copie automatique (si configuré) vers le dossier local défini dans `drive_path.txt`.
4. Ouverture automatique du lien Drive partagé (dossier en ligne) pour vérifier la présence / partager.
5. Résultat disponible côté élève via l'appli ou le site Google Drive.
 6. Un index parent `College_4ieme_Maths.html` est régénéré listant tous les cours (tri du plus récent au plus ancien) avec recherche.

### Lancer avec un autre fichier source
```bat
generer_cours.bat mon_cours.md
```
Si non précisé : utilise `exemple_fractions.md`.

## Utilisation (méthode personnalisée)
1. Copiez votre contenu balisé dans un fichier ex: `mon_cours.md` (utilisez les balises <INTRO> ... </INTRO> etc.).
2. Ouvrez un PowerShell dans le dossier `course_tools`.
3. Lancez :
	```powershell
	python generate_course_page.py mon_cours.md -o mon_cours.html -t template_base.html
	```
4. Ouvrez `mon_cours.html` dans un navigateur puis transférez-le sur un smartphone.

## Envoi sur smartphone (options)
1. Email : joindre le fichier HTML et l'envoyer à l'adresse de l'élève.
2. Cloud : déposer sur Google Drive / OneDrive puis ouvrir et télécharger.
3. Messagerie : envoyer via WhatsApp / Signal / Telegram (fichier). L'élève peut l'ouvrir et l'ajouter en favori.
4. Renommer (optionnel) en `cours_fractions.html` pour que ce soit plus compréhensible.
5. Astuce : Ajouter en écran d'accueil depuis Chrome (Menu → Ajouter à l'écran d'accueil) pour usage rapide.

## Configuration du dossier Google Drive
- Le fichier `drive_path.txt` contient le chemin cible (par défaut : `C:\Users\%USERNAME%\Google Drive\Partages\CoursLucas`).
- Adaptez ce chemin selon le répertoire réel de votre Google Drive local (ex : `C:\Users\Geoffroy\Google Drive\PartageCours\Lucas`).
- Si le dossier n'existe pas, le script tente de le créer.
- Assurez-vous que le dossier est bien partagé avec le compte de l'élève (dans l'interface web Google Drive) pour qu'il y accède depuis son téléphone.
 - Le script ouvre aussi l'URL publique définie (modifiable dans `generer_cours.bat` via `SET SHARE_URL=`).

### Partage recommandé
1. Créez un dossier racine: `Cours_Maths_Lucas` dans Google Drive.
2. Partagez-le avec le compte concerné (lecture + éventuellement téléchargement).
3. Synchronisez ce dossier sur votre PC (Google Drive desktop installé).
4. Mettez ce chemin dans `drive_path.txt`.
5. Chaque génération = nouvelle version dispo automatiquement.

## Accessibilité côté élève
Dans la page générée, votre enfant peut :
- Activer mode sombre
- Activer police Dys (si installée) sinon fallback
- Agrandir la police
- Lire une sélection avec le bouton « Lecture section »
- Activer le mode focus pour réduire la distraction

## Mise à jour du contenu
Refaire un envoi = régénérer le HTML → renvoyer. Ancienne version peut être supprimée du téléphone.

## Prochaines améliorations potentielles
- Ajout quiz interactifs auto-corrigés (localStorage)
- Export PDF accessible
- Packager en mini PWA (installation écran d'accueil)
- Bouton statistiques d’usage (progression locale)
- Génération de tags plus fins (thème, difficulté)
- Ajout d'un indicateur « déjà consulté » (localStorage)

## Problèmes fréquents
| Problème | Cause probable | Solution |
|----------|----------------|----------|
| Caractères spéciaux mal rendus | Encodage | Sauvegarder en UTF-8 |
| Lecture vocale absente | Navigateur non compatible | Essayer Chrome / Edge |
| Police Dys non visible | Non installée | Installer OpenDyslexic ou garder défaut |
| Script Python introuvable | Python non installé | Installer depuis python.org |
| Placeholders non remplacés | Clé manquante dans JSON | Ajouter la clé au JSON ou lancer avec --strict pour repérer |

## Génération à partir d'un JSON (nouveau)
Pour créer un cours standardisé à partir de `course_template_html.html` :

1. Éditer / dupliquer `exemple_cours.json`.
2. Lancer :
	```powershell
	python inject_course.py -t course_template_html.html -j exemple_cours.json -o cours_fractions_struct.html
	```
3. Le fichier de sortie est prêt à être copié dans le dossier Drive.

Option stricte (signale les placeholders non remplis) :
```powershell
python inject_course.py -t course_template_html.html -j exemple_cours.json -o cours_fractions_struct.html --strict
```

Clés de liste (ex: `POINTS_CLES`, `ETAPES_METHODE`) sont fusionnées en lignes séparées.

## Placeholders supportés (extraits)
`[TITRE_COURS]`, `[DATE_MAJ]`, `[DUREE]`, `[CRITERE_GLOBAL]`, `[ACCROCHE]`, `[MESSAGE_REASSURANCE]`, `[QUESTION_DIAG]`, `[REP_DIAG]`, `[ANALOGIE]`, `[MANIP]`, `[VERBALISATION]`, `[TERMES]`, `[SIMPLIFICATION]`, `[PIEGE]`, `[EXEMPLE_COMMENTE]`, `[VARIANTE_LENTE]`, `[VARIANTE_RAPIDE]`, `[CAS_REELS]`, `[INDICE_1]`, `[INDICE_2]`, `[INDICE_3]`, `[OBJECTIF_STARS]`, `[DETAIL_BAREME]`, `[PHRASE_MNEMO]`, `[EXEMPLE_FINAL]`, `[PALIER_SUIVANT]`, `[REV_J1]`, `[REV_J3]`, `[REV_J7]`, `[CONF_DEBUT]`, `[CONF_FIN]`, `[NOTION]`, `[DECLENCHEUR]`, `[ETAPES_FICHE]`, `[PIEGE_FICHE]`, `[REFLEXE]`, `[AUTO_CHECK]`.

Les listes JSON :
- `POINTS_CLES` → insérées sous forme de `<li>` si vous faites un post-traitement ou laisser comme texte brut.
- Actuellement insertion brute : pour produire des `<li>` vous pouvez préparer déjà le HTML dans la valeur JSON.

## Amélioration future suggérée
- Générateur combiné : Markdown balisé → JSON → Template HTML
- Minification optionnelle
- Export PDF (headless Chromium)

---
**Bon à savoir :** L'adresse email de l'élève peut être utilisée pour l'envoi manuel du fichier, mais ne l'intégrez pas en dur dans des scripts partagés publiquement.

## Améliorations possibles (liste originale)
- Export en PDF allégé
- Génération d’une version audio complète (via TTS externe)
- Ajout de quiz interactifs (localStorage)

