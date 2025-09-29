# Scoring Engine Externalisation

Le système de score a été extrait de `main.js` vers `scoring.js` pour permettre :

- Modification indépendante des barèmes (`MAX_POINTS`)
- Réutilisation future dans d'autres chapitres
- Maintenance simplifiée (état, persistance, affichage)

## API Exposée
- `ScoreEngine.registerScore(section, key, value)`
- `ScoreEngine.resetScores()`
- `ScoreEngine.updateScoreDisplays()`
- `ScoreEngine.getState()` -> { total, perSection, awarded }
- Constantes : `ScoreEngine.MAX_POINTS`, `ScoreEngine.GLOBAL_MAX`, `ScoreEngine.SECTION_LABELS`

Pour compatibilité, les fonctions globales suivantes restent accessibles :
`registerScore`, `resetScores`, `updateScoreDisplays`.

## Personnalisation
Modifier les barèmes dans `scoring.js` :
```js
const MAX_POINTS = { /* ... */ };
```
Après modification, aucune autre action nécessaire si les IDs / sections restent identiques.
