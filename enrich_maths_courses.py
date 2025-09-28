import os, json, textwrap

BASE_DIR = 'College_4ieme_Maths'

CHAPTERS = [
    ("01_Nombres_relatifs", "Nombres relatifs"),
    ("02_Fractions_et_calculs", "Fractions et calculs"),
    ("03_Puissances_et_notation_scientifique", "Puissances et notation scientifique"),
    ("04_Calcul_litteral", "Calcul littéral"),
    ("05_Equations_simples", "Équations simples"),
    ("06_Proportionnalite_et_pourcentages", "Proportionnalité et pourcentages"),
    ("07_Statistiques", "Statistiques"),
    ("08_Probabilites", "Probabilités"),
    ("09_Theoreme_de_Pythagore", "Théorème de Pythagore"),
    ("10_Geometrie_des_triangles_et_Thales", "Géométrie des triangles et Thalès"),
    ("11_Transformations_et_symetries", "Transformations et symétries"),
    ("12_Solides_et_volumes", "Solides et volumes"),
]

HTML_HEAD = """<!DOCTYPE html><html lang='fr'><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>{title}</title>
<style>
body{{font-family:Arial,system-ui,sans-serif;margin:0;padding:1.1rem 1.2rem;line-height:1.55;background:#0f1115;color:#f5f7fa;}}
header,footer{{background:rgba(255,255,255,0.05);padding:1rem 1.25rem;margin:0 0 1.2rem;border:1px solid #1e2530;border-radius:14px;-webkit-backdrop-filter:blur(9px);backdrop-filter:blur(9px);}}
section{{background:rgba(255,255,255,0.025);padding:1rem 1.1rem;margin:0 0 1rem;border:1px solid #1b222c;border-radius:12px;}}
h1,h2,h3{{line-height:1.2;margin:0 0 .65rem;font-weight:600;}}
nav a{{color:#67c7ff;text-decoration:none;margin-right:.85rem;font-size:.82rem;letter-spacing:.3px;}}nav a:hover{{text-decoration:underline;}}
.badge{{display:inline-block;padding:.28rem .6rem;border-radius:18px;font-size:.58rem;background:#17212b;margin:0 .35rem .4rem 0;border:1px solid #23303d;letter-spacing:.5px;text-transform:uppercase;opacity:.9;}}
.grid-auto{{display:grid;gap:.75rem;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));}}
.card{{background:#141a21;border:1px solid #232d38;padding:.75rem .85rem;border-radius:12px;position:relative;}}
.card h3{{margin-top:0;font-size:1.02rem;}}
.notice{{background:#162f47;border:1px solid #214b6b;padding:.65rem .8rem;border-radius:9px;font-size:.78rem;}}
small.ref{{font-size:.65rem;opacity:.75;}}
pre,code{{font-family:consolas,ui-monospace,monospace;font-size:.78rem;}}
.toggle{{background:#244b82;color:#fff;border:none;padding:.3rem .55rem;border-radius:6px;font-size:.65rem;cursor:pointer;margin-top:.35rem;}}
.toggle:hover{{background:#1d3f6d;}}
.solution{{display:none;margin-top:.4rem;padding:.5rem .6rem;background:#1b2733;border:1px solid #2a3948;border-radius:8px;font-size:.78rem;}}
.progress{{height:8px;background:#1d2733;border-radius:4px;overflow:hidden;margin:.55rem 0 1rem;}}
.progress span{{display:block;height:100%;background:linear-gradient(90deg,#2563eb,#4f46e5);}}
.table-eval{{width:100%;border-collapse:collapse;font-size:.75rem;}}
.table-eval th,.table-eval td{{border:1px solid #28323d;padding:.35rem .4rem;text-align:left;}}
blockquote{{margin:.6rem 0;padding:.55rem .75rem;background:#17212b;border-left:4px solid #2563eb;border-radius:4px;font-size:.85rem;}}
@media (max-width:760px){{nav a{{display:inline-block;margin:.25rem .6rem .25rem 0;}}}}
</style>
<script>
function toggleSolution(id){{const el=document.getElementById(id);if(!el)return;el.style.display=el.style.display==='none'||el.style.display===''?'block':'none';}}
</script>
</head><body>"""
HTML_FOOT = """<footer><small>Contenu enrichi – Génération structurée • Réactivation : J+1 / J+3 / J+7 / J+14</small></footer></body></html>"""

# Enriched pedagogical data per chapter
META = {
    "01_Nombres_relatifs": {
        "motivation": "Interpréter gains/pertes, températures, altitudes et soldes.",
        "context": "Un jeu vidéo affiche -120 PV puis +45 PV.",
        "objectif_final": "additionner, soustraire et comparer des nombres relatifs dans des situations concrètes",
        "prerequis": ["Sens du signe moins","Lecture droite graduée","Priorités calcul simple"],
        "etapes": [
            ("Situer", "Placer chaque nombre sur une droite graduée."),
            ("Comparer", "Observer positions relatives pour décider signe final."),
            ("Calculer", "Additionner ou soustraire les valeurs absolues selon les signes."),
        ],
        "schema": "Droite graduée avec -8, -3, 0, +4, +7 colorés.",
        "methode": [
            "Même signe → additionner les valeurs et garder le signe.",
            "Signes différents → soustraire la plus petite valeur absolue de la plus grande.",
            "Résultat prend le signe de la plus grande valeur absolue.",
            "Contrôle : exemple concret (température ou argent).",
        ],
        "erreurs": [
            "Retirer mécaniquement le signe du plus grand nombre.",
            "Confondre soustraction et 'prendre la différence' des valeurs absolues.",
            "Oublier de justifier le signe final.",
        ],
        "notion": "Addition/Soustraction relatifs",
    },
    "02_Fractions_et_calculs": {
        "motivation": "Partager équitablement, adapter des recettes, calculer des portions.",
        "context": "Recette pour 6 personnes à adapter pour 4.",
        "objectif_final": "réduire, additionner, multiplier des fractions et interpréter le résultat",
        "prerequis": ["Multiples et diviseurs","Simplification par un même nombre","Lien fraction ↔ quotient"],
        "etapes": [
            ("Observer", "Identifier numérateurs et dénominateurs; repérer simplifications possibles."),
            ("Uniformiser", "Mettre au même dénominateur si addition/soustraction."),
            ("Calculer", "Opérer sur numérateurs ou multiplier/dénominateurs."),
        ],
        "schema": "Barres fractionnaires colorées montrant 3/4 et 2/3.",
        "methode": [
            "Pour simplifier : diviser haut et bas par un diviseur commun.",
            "Addition : dénominateurs identiques → additionner numérateurs; sinon les rendre identiques.",
            "Multiplication : multiplier numérateurs entre eux et dénominateurs entre eux.",
            "Contrôle : résultat entre 0 et 1 ? supérieur ? sens cohérent ?",
        ],
        "erreurs": [
            "Additionner numérateurs et dénominateurs en même temps.",
            "Oublier de simplifier le résultat.",
            "Chercher un PPCM trop grand inutilement.",
        ],
        "notion": "Fractions – opérations",
    },
    "03_Puissances_et_notation_scientifique": {
        "motivation": "Exprimer très grands/petits nombres simplement.",
        "context": "Distance Terre–Soleil ≈ 1,496 × 10^11 m.",
        "objectif_final": "utiliser les règles de puissances et écrire en notation scientifique",
        "prerequis": ["Multiplication de facteurs identiques","Valeur de 10,100,1000","Place des zéros"],
        "etapes": [
            ("Développer", "Écrire explicitement le produit répété."),
            ("Rassembler", "Compter le nombre de facteurs."),
            ("Réduire", "Appliquer lois (produit, quotient, puissance)."),
        ],
        "schema": "Tableau: 10^3 = 1000, 10^-2 = 0,01.",
        "methode": [
            "a^m × a^n = a^(m+n)",
            "a^m ÷ a^n = a^(m−n)",
            "(a^m)^n = a^(m×n)",
            "Notation scientifique : a × 10^n avec 1 ≤ a < 10.",
        ],
        "erreurs": [
            "Confondre (a^m)^n avec a^(m+n).",
            "Mettre deux chiffres avant la virgule en notation scientifique.",
            "Oublier signe de l'exposant quand nombre < 1.",
        ],
        "notion": "Puissances / Notation scientifique",
    },
    "04_Calcul_litteral": {
        "motivation": "Généraliser au lieu de refaire des calculs répétitifs.",
        "context": "Périmètre d'un rectangle de longueur L et largeur l.",
        "objectif_final": "simplifier et développer des expressions simples puis factoriser basiquement",
        "prerequis": ["Priorités opératoires","Distributivité intuitive","Multiplication signes"],
        "etapes": [
            ("Identifier", "Repérer termes semblables et parenthèses."),
            ("Développer", "Appliquer distributivité si besoin."),
            ("Réduire", "Regrouper termes semblables."),
        ],
        "schema": "Schéma d'un rectangle annoté L et l.",
        "methode": [
            "Développer : a(b + c) = ab + ac",
            "Réduire : additionner coefficients des mêmes lettres",
            "Factoriser simple : ab + ac = a(b + c)",
            "Vérifier en testant valeurs numériques.",
        ],
        "erreurs": [
            "Oublier de multiplier chaque terme lors du développement.",
            "Changer l'ordre des lettres et perdre un signe.",
            "Confondre factoriser et développer.",
        ],
        "notion": "Expression algébrique",
    },
    "05_Equations_simples": {
        "motivation": "Trouver une valeur inconnue dans des situations concrètes.",
        "context": "Total payé 37€ pour 4 articles identiques + 5€ de frais.",
        "objectif_final": "résoudre des équations du 1er degré simples et vérifier",
        "prerequis": ["Équilibrer une égalité","Calculs relatifs simples","Distributivité"],
        "etapes": [
            ("Isoler", "Mettre les termes avec inconnue d'un côté."),
            ("Simplifier", "Réduire termes semblables."),
            ("Résoudre", "Appliquer opération inverse."),
        ],
        "schema": "Balance illustrant équation.",
        "methode": [
            "Transposer en effectuant la même opération des deux côtés.",
            "Réduire avant d'isoler.",
            "Vérifier en remplaçant dans l'équation initiale.",
        ],
        "erreurs": [
            "Changer de signe sans raison.",
            "Diviser seulement un côté.",
            "Oublier de tester la solution.",
        ],
        "notion": "Équations linéaires",
    },
    "06_Proportionnalite_et_pourcentages": {
        "motivation": "Appliquer remises, échelles, vitesses, recettes.",
        "context": "Remise de 15% sur un article à 48€.",
        "objectif_final": "reconnaître et utiliser proportionnalité + pourcentages (augmentation / diminution)",
        "prerequis": ["Fractions de base","Multiplication décimaux","Ratio simple"],
        "etapes": [
            ("Détecter", "Table proportionnelle ou pas ?"),
            ("Modéliser", "Mettre sous forme de tableau ou produit en croix."),
            ("Calculer", "Appliquer coefficient multiplicateur."),
        ],
        "schema": "Table de proportionnalité 3 colonnes.",
        "methode": [
            "Coefficient = image / original.",
            "Pourcentage p% → multiplier par (1 ± p/100).",
            "Inverse : diviser par coefficient.",
        ],
        "erreurs": [
            "Additionner des pourcentages successifs.",
            "Confondre diminution de p% et division par p.",
            "Produit en croix mal aligné.",
        ],
        "notion": "Proportionnalité / Pourcentages",
    },
    "07_Statistiques": {
        "motivation": "Résumer un ensemble de données (notes, mesures).",
        "context": "Notes : 8, 11, 11, 14, 17.",
        "objectif_final": "calculer moyenne, médiane, étendue et interpréter",
        "prerequis": ["Addition série","Ordre croissant","Division"],
        "etapes": [
            ("Organiser", "Classer les données."),
            ("Calculer", "Appliquer formules moyenne / étendue."),
            ("Interpréter", "Comparer valeurs aux indicateurs."),
        ],
        "schema": "Diagramme en bâtons simplifié.",
        "methode": [
            "Moyenne = somme / effectif.",
            "Étendue = max – min.",
            "Médiane = valeur centrale (ou moyenne des deux centrales).",
        ],
        "erreurs": [
            "Oublier une valeur dans la somme.",
            "Confondre médiane et moyenne.",
            "Inverser max et min pour l'étendue.",
        ],
        "notion": "Indicateurs statistiques",
    },
    "08_Probabilites": {
        "motivation": "Anticiper issues d'un jeu ou d'un tirage.",
        "context": "Sac : 3 billes rouges, 2 bleues, 1 verte.",
        "objectif_final": "modéliser une expérience simple et calculer probabilités élémentaires",
        "prerequis": ["Fraction d'un tout","Dénombrement simple","Addition cas incompatibles"],
        "etapes": [
            ("Lister", "Écrire issues possibles."),
            ("Compter", "Associer effectifs à chaque issue."),
            ("Calculer", "P(issue)= effectif / total."),
        ],
        "schema": "Arbre simple pour 2 tirages avec remise.",
        "methode": [
            "Probabilité entre 0 et 1.",
            "Somme des probabilités = 1.",
            "Cas favorables / cas possibles.",
        ],
        "erreurs": [
            "Additionner des probabilités non exclusives.",
            "Oublier un cas dans le total.",
            "Confondre tirage avec et sans remise.",
        ],
        "notion": "Probabilités simples",
    },
    "09_Theoreme_de_Pythagore": {
        "motivation": "Calculer une distance inaccessible directement.",
        "context": "Ladder contre un mur : hauteur recherchée.",
        "objectif_final": "reconnaître un triangle rectangle et appliquer théorème direct/inverse",
        "prerequis": ["Carré d'un nombre","Triangle rectangle définition","Opposé / adjacent / hypothénuse"],
        "etapes": [
            ("Identifier", "Vérifier présence angle droit."),
            ("Associer", "Nommer l'hypoténuse."),
            ("Appliquer", "c^2 = a^2 + b^2 ou test inverse."),
        ],
        "schema": "Triangle rectangle avec longueurs a,b,c.",
        "methode": [
            "Toujours isoler c^2.",
            "Comparer c^2 et a^2+b^2 pour l'inverse.",
            "Carrés exacts avant racine.",
        ],
        "erreurs": [
            "Prendre le plus petit côté comme hypoténuse.",
            "Oublier racine finale.",
            "Comparer c au lieu de c^2.",
        ],
        "notion": "Théorème de Pythagore",
    },
    "10_Geometrie_des_triangles_et_Thales": {
        "motivation": "Mesurer indirectement des longueurs (ombre, maquette).",
        "context": "Ombre d'un arbre et d'un bâton.",
        "objectif_final": "reconnaître configuration de Thalès et calculer une longueur",
        "prerequis": ["Triangles semblables idée","Rapport de longueur","Proportionnalité"],
        "etapes": [
            ("Repérer", "Identifier droites parallèles."),
            ("Associer", "Placer rapports correspondants."),
            ("Calculer", "Résoudre proportion."),
        ],
        "schema": "Deux triangles imbriqués partagent un angle.",
        "methode": [
            "Ordre des points conservé.",
            "Rapports correspondants = égalité.",
            "Isolement de l'inconnue.",
        ],
        "erreurs": [
            "Intervertir rapports.",
            "Confondre côtés homologues.",
            "Appliquer hors configuration parallèle.",
        ],
        "notion": "Thalès (configuration)",
    },
    "11_Transformations_et_symetries": {
        "motivation": "Analyser motifs, pavages, logos.",
        "context": "Motif symétrique d'un tapis.",
        "objectif_final": "identifier et réaliser symétries axiales et centrales",
        "prerequis": ["Repérage points","Utilisation règle/équerre","Perception axes"],
        "etapes": [
            ("Tracer", "Placer l'axe ou le centre."),
            ("Reporter", "Mesurer distances pour construire image."),
            ("Vérifier", "Alignement / distances égales."),
        ],
        "schema": "Figure et son image miroir.",
        "methode": [
            "Axe : perpendiculaire passant par milieu segment AA'.",
            "Centre : vecteur (A→A') constant.",
            "Angles conservés, longueurs conservées.",
        ],
        "erreurs": [
            "Axe mal perpendiculaire.",
            "Centre mal localisé.",
            "Confusion rotation / symétrie centrale.",
        ],
        "notion": "Symétries",
    },
    "12_Solides_et_volumes": {
        "motivation": "Calculer contenances, emballages, matériaux nécessaires.",
        "context": "Remplir un aquarium prismatique.",
        "objectif_final": "calculer volumes et relier unités (cm3, L)",
        "prerequis": ["Aires de base","Multiplications décimales","Unités longueurs"],
        "etapes": [
            ("Identifier", "Reconnaître la base (carré, rectangle, disque)."),
            ("Formule", "Rappeler volume = aire base × hauteur."),
            ("Calculer", "Convertir si nécessaire et appliquer."),
        ],
        "schema": "Prisme droit + cylindre.",
        "methode": [
            "Prisme : V = A_base × h",
            "Cylindre : V = πr²h",
            "1 L = 1 dm³ (1000 cm³)",
        ],
        "erreurs": [
            "Oublier carré sur rayon.",
            "Confondre unités (cm² vs cm³).",
            "Multiplier par mauvaise hauteur.",
        ],
        "notion": "Volumes",
    },
}

# Exercises dataset per chapter (short sets to keep size reasonable)
EXOS = {}
for slug, title in CHAPTERS:
    base = slug[:2]
    if slug == "01_Nombres_relatifs":
        EXOS[slug] = {
            "niveau1": [
                {"titre": "+ et - basiques", "enonce": "Calculer : (+5) + (-3)", "solution": "= +2", "indice": "Comparer valeurs absolues."},
                {"titre": "Températures", "enonce": "Matin : -2°C, après-midi : +4°C. Variation ?", "solution": "+6°C", "indice": "Final - initial"},
            ],
            "niveau2": [
                {"titre": "Somme", "enonce": "(-7) + (+12) + (-5)", "solution": "0", "indice": "Associer positifs / négatifs."},
                {"titre": "Différence", "enonce": "(-15) - (-9)", "solution": "-6", "indice": "Soustraction = ajouter l'opposé."},
            ],
            "niveau3": [
                {"titre": "Expression", "enonce": "Simplifier : (-4) + (+9) - (+3) - (-2)", "solution": "+4", "indice": "Transformer en additions."},
                {"titre": "Contexte argent", "enonce": "Compte : -18€ puis dépôt 25€ puis retrait 11€. Solde ?", "solution": "-4€", "indice": "Appliquer successivement."},
            ],
        }
    else:
        # Generic lighter data - can be enriched further
        EXOS[slug] = {
            "niveau1": [
                {"titre": "Ex1", "enonce": "(placeholder) simplifié niveau 1", "solution": "—", "indice": "Identifier données."},
            ],
            "niveau2": [
                {"titre": "Ex1", "enonce": "(placeholder) standard niveau 2", "solution": "—", "indice": "Appliquer méthode."},
            ],
            "niveau3": [
                {"titre": "Ex1", "enonce": "(placeholder) défi niveau 3", "solution": "—", "indice": "Réfléchir structure."},
            ],
        }


def ensure():
    if not os.path.isdir(BASE_DIR):
        raise SystemExit(f"Dossier {BASE_DIR} introuvable. Lancer d'abord generate_maths_courses.py")


def html(title: str, body: str) -> str:
    return HTML_HEAD.format(title=title) + body + HTML_FOOT


def build_course(slug: str, title: str, meta: dict) -> str:
    badges = "".join(f"<span class='badge'>{b}</span>" for b in ["Objectifs","Prérequis","Différenciation","Métacognition"])    
    etapes_html = "".join(
        f"<div class='card'><h3>Étape {i+1} – {nom}</h3><p>{desc}</p><p><em>Variante blocage :</em> Donner un exemple concret chiffré.</p></div>" for i,(nom,desc) in enumerate(meta['etapes'])
    )
    methode = "<ol>" + "".join(f"<li>{m}</li>" for m in meta['methode']) + "</ol>"
    erreurs = "<ul>" + "".join(f"<li>{e}</li>" for e in meta['erreurs']) + "</ul>"
    prereq = "<ul>" + "".join(f"<li>{p}</li>" for p in meta['prerequis']) + "</ul>"
    body = f"""
<header>
 <h1>{title}</h1>
 <nav>
  <a href='../exercices/exercices_niveau1_decouverte.html'>Ex N1</a>
  <a href='../exercices/exercices_niveau2_pratique.html'>Ex N2</a>
  <a href='../exercices/exercices_niveau3_defi.html'>Ex N3</a>
  <a href='../corrections/corrections_detaillees.html'>Corrections</a>
  <a href='../fiches_resume/fiche_synthese.html'>Synthèse</a>
  <a href='../evaluations/evaluation_formative.html'>Évaluation</a>
 </nav>
 <div class='progress'><span style='width:6%'></span></div>
 {badges}
</header>
<section><h2>1. Mise en situation</h2><p><strong>Pourquoi ?</strong> {meta['motivation']}</p><blockquote>{meta['context']}</blockquote></section>
<section><h2>2. Objectif final</h2><p>Être capable de {meta['objectif_final']}.</p></section>
<section><h2>3. Prérequis rapides</h2>{prereq}<div class='notice'>Si un prérequis manque → mini réactivation avant de poursuivre.</div></section>
<section><h2>4. Étapes guidées</h2><div class='grid-auto'>{etapes_html}</div></section>
<section><h2>5. Visualisation</h2><p>{meta['schema']}</p></section>
<section><h2>6. Méthode</h2>{methode}</section>
<section><h2>7. Erreurs fréquentes</h2>{erreurs}</section>
<section><h2>8. Auto-contrôle immédiat</h2><ul><li>Je peux expliquer la notion « {meta['notion']} ».</li><li>Je sais appliquer sans modèle.</li><li>Je justifie mon signe / choix / formule.</li></ul></section>
<section><h2>9. Plan de réactivation</h2><ul><li>J+1 : 2 ex. N1</li><li>J+3 : 2 ex. N2</li><li>J+7 : mini quiz</li><li>J+14 : défi mélange</li></ul></section>
"""
    return html(title, body)


def build_exercises(slug: str, title: str, level: int) -> str:
    key = {1:'decouverte',2:'pratique',3:'defi'}[level]
    data = EXOS.get(slug, {})
    serie = data.get(f"niveau{level}", [])
    blocs = []
    for i, ex in enumerate(serie, start=1):
        sid = f"sol_{slug}_{level}_{i}"
        blocs.append(
            f"<div class='card'><h3>Exercice {i} – {ex['titre']}</h3><p>{ex['enonce']}</p>"
            f"<button class='toggle' onclick=\"toggleSolution('{sid}')\">Afficher / Masquer solution</button>"
            f"<div id='{sid}' class='solution'><p><strong>Indice :</strong> {ex['indice']}</p><p><strong>Solution :</strong> {ex['solution']}</p></div></div>"
        )
    body = f"""
<header><h1>{title} – Exercices niveau {level}</h1><nav><a href='../cours/cours_principal.html'>Cours</a></nav></header>
<section><h2>Série ciblée</h2><div class='grid-auto'>{''.join(blocs)}</div></section>
"""
    return html(f"Exercices N{level}", body)


def build_corrections(slug: str, title: str) -> str:
    parts = []
    for lvl in (1,2,3):
        serie = EXOS.get(slug, {}).get(f"niveau{lvl}", [])
        if not serie: continue
        parts.append(f"<h2>Niveau {lvl}</h2>")
        for i, ex in enumerate(serie, start=1):
            parts.append(
                f"<div class='card'><h3>Ex {lvl}.{i} – {ex['titre']}</h3>"
                f"<p><em>Énoncé :</em> {ex['enonce']}</p>"
                f"<p><strong>Démarche :</strong> Justifier chaque transformation.</p>"
                f"<p><strong>Solution :</strong> {ex['solution']}</p>"
                f"<small class='ref'>Auto-contrôle : cohérent ? unités ? signe ?</small></div>"
            )
    body = f"""
<header><h1>{title} – Corrections détaillées</h1><nav><a href='../cours/cours_principal.html'>Cours</a></nav></header>
<section>{''.join(parts)}</section>
"""
    return html("Corrections", body)


def build_erreurs(slug: str, title: str, meta: dict) -> str:
    items = "".join(f"<li>{e} → <em>Stratégie :</em> reformuler, vérifier avec un exemple chiffré.</li>" for e in meta['erreurs'])
    body = f"""
<header><h1>{title} – Erreurs fréquentes</h1><nav><a href='../cours/cours_principal.html'>Cours</a></nav></header>
<section><ul>{items}</ul></section>
"""
    return html("Erreurs fréquentes", body)


def build_fiche_synthese(slug: str, title: str, meta: dict) -> str:
    points = "".join(f"<li>{p}</li>" for p in meta['methode'][:4])
    quiz = "".join(f"<li>Question rapide {i} (adapter).</li>" for i in range(1,6))
    body = f"""
<header><h1>Fiche Synthèse – {title}</h1><nav><a href='../cours/cours_principal.html'>Cours</a></nav></header>
<section><h2>Essentiel</h2><ul>{points}</ul></section>
<section><h2>Mini Quiz</h2><ol>{quiz}</ol></section>
"""
    return html("Fiche Synthèse", body)


def build_fiche_methode(slug: str, title: str, meta: dict) -> str:
    etapes = "".join(f"<li>{i+1}. {s}</li>" for i,s in enumerate(meta['methode']))
    body = f"""
<header><h1>Fiche Méthode – {title}</h1><nav><a href='../cours/cours_principal.html'>Cours</a></nav></header>
<section><ol>{etapes}</ol></section>
"""
    return html("Fiche Méthode", body)


def build_fiche_memo(slug: str, title: str, meta: dict) -> str:
    memos = ["Repérer mots-clés","Encadrer données utiles","Vérifier cohérence finale"]
    memos.extend([m.split(':')[0] for m in meta['methode'][:2]])
    lis = "".join(f"<li>{m}</li>" for m in memos)
    body = f"""
<header><h1>Fiche Mémorisation – {title}</h1><nav><a href='../cours/cours_principal.html'>Cours</a></nav></header>
<section><ul>{lis}</ul></section>
"""
    return html("Fiche Mémorisation", body)


def build_eval_form(slug: str, title: str, meta: dict) -> str:
    q = "".join(f"<li>Vérifier : {meta['notion']} – question d'application simple {i}.</li>" for i in range(1,6))
    body = f"""
<header><h1>Évaluation Formative – {title}</h1><nav><a href='../cours/cours_principal.html'>Cours</a></nav></header>
<section><ol>{q}</ol></section>
"""
    return html("Évaluation formative", body)


def build_eval_somm(slug: str, title: str, meta: dict) -> str:
    q = "".join(f"<li>Exercice sommative structuré {i}</li>" for i in range(1,6))
    body = f"""
<header><h1>Évaluation Sommative – {title}</h1><nav><a href='../cours/cours_principal.html'>Cours</a></nav></header>
<section><ol>{q}</ol></section>
"""
    return html("Évaluation sommative", body)


def build_grille(slug: str, title: str, meta: dict) -> str:
    competences = ["Comprendre énoncé","Choisir méthode","Exécuter correctement","Justifier / vérifier"]
    rows = "".join(f"<tr><td>{c}</td><td>Guidé</td><td>Autonome</td><td>Transfert</td></tr>" for c in competences)
    body = f"""
<header><h1>Grille Compétences – {title}</h1><nav><a href='../cours/cours_principal.html'>Cours</a></nav></header>
<section><table class='table-eval'><tr><th>Compétence</th><th>N1</th><th>N2</th><th>N3</th></tr>{rows}</table></section>
"""
    return html("Grille compétences", body)


def write(path: str, content: str):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def enrich():
    ensure()
    for slug, title in CHAPTERS:
        meta = META[slug]
        chapter_dir = os.path.join(BASE_DIR, slug)
        # Cours
        write(os.path.join(chapter_dir, 'cours', 'cours_principal.html'), build_course(slug, title, meta))
        # Exercices
        write(os.path.join(chapter_dir, 'exercices', 'exercices_niveau1_decouverte.html'), build_exercises(slug, title, 1))
        write(os.path.join(chapter_dir, 'exercices', 'exercices_niveau2_pratique.html'), build_exercises(slug, title, 2))
        write(os.path.join(chapter_dir, 'exercices', 'exercices_niveau3_defi.html'), build_exercises(slug, title, 3))
        # Corrections
        write(os.path.join(chapter_dir, 'corrections', 'corrections_detaillees.html'), build_corrections(slug, title))
        write(os.path.join(chapter_dir, 'corrections', 'erreurs_frequentes.html'), build_erreurs(slug, title, meta))
        # Fiches
        write(os.path.join(chapter_dir, 'fiches_resume', 'fiche_synthese.html'), build_fiche_synthese(slug, title, meta))
        write(os.path.join(chapter_dir, 'fiches_resume', 'fiche_methode.html'), build_fiche_methode(slug, title, meta))
        write(os.path.join(chapter_dir, 'fiches_resume', 'fiche_memorisation.html'), build_fiche_memo(slug, title, meta))
        # Evaluations
        write(os.path.join(chapter_dir, 'evaluations', 'evaluation_formative.html'), build_eval_form(slug, title, meta))
        write(os.path.join(chapter_dir, 'evaluations', 'evaluation_sommative.html'), build_eval_somm(slug, title, meta))
        write(os.path.join(chapter_dir, 'evaluations', 'grille_competences.html'), build_grille(slug, title, meta))
        # JSON meta enrichi
        meta_json = {
            "slug": slug,
            "titre": title,
            "notion": meta['notion'],
            "objectifs": meta['methode'],
            "prerequis": meta['prerequis'],
            "etapes": [e[0] for e in meta['etapes']],
            "plan_reactivation": ["J+1","J+3","J+7","J+14"],
            "erreurs_frequentes": meta['erreurs']
        }
        with open(os.path.join(chapter_dir, 'cours', 'data_chapitre.json'), 'w', encoding='utf-8') as jf:
            json.dump(meta_json, jf, ensure_ascii=False, indent=2)
    print("Enrichissement terminé pour", len(CHAPTERS), "chapitres.")

if __name__ == '__main__':
    enrich()
