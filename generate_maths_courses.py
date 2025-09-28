import os, textwrap, json

BASE_DIR = 'College_4ieme_Maths'

chapters = [
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

SUBFOLDERS = ["cours", "exercices", "corrections", "fiches_resume", "evaluations"]

HTML_HEAD = """<!DOCTYPE html><html lang='fr'><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>{title}</title>
<style>
body{{font-family:Arial,system-ui,sans-serif;margin:0;padding:1.2rem;line-height:1.5;background:#0f1115;color:#f5f7fa;}}
header,footer{{background:rgba(255,255,255,0.05);padding:1rem 1.2rem;margin:0 0 1.2rem;border:1px solid #222;border-radius:12px;-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);}} 
section{{background:rgba(255,255,255,0.03);padding:1rem 1.2rem;margin:0 0 1rem;border:1px solid #1e1e1e;border-radius:10px;}} 
h1,h2,h3{{line-height:1.2;margin:0 0 .6rem;font-weight:600;}} 
nav a{{color:#6bc1ff;text-decoration:none;margin-right:.9rem;font-size:.9rem;}} nav a:hover{{text-decoration:underline;}} 
.badge{{display:inline-block;padding:.2rem .55rem;border-radius:20px;font-size:.65rem;background:#1d2733;margin:0 .35rem .35rem 0;border:1px solid #283848;letter-spacing:.5px;text-transform:uppercase;}} 
.table-like{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:.6rem;margin:.6rem 0;}} 
.card{{background:#13171d;border:1px solid #232a33;padding:.6rem .75rem;border-radius:10px;}} 
pre{{background:#1b222b;padding:.75rem;border-radius:8px;overflow:auto;font-size:.85rem;}} code{{font-family:consolas,monospace;color:#ffdd8b;}} 
ul{{margin:.4rem 0 .8rem;padding-left:1.2rem;}} li{{margin:.15rem 0;}} a.btn{{display:inline-block;background:#2563eb;color:#fff;padding:.55rem .9rem;border-radius:6px;font-size:.8rem;text-decoration:none;margin:.35rem 0;}} a.btn:hover{{background:#1d4ed8;}} 
.notice{{background:#162f47;border:1px solid #214b6b;padding:.6rem .75rem;border-radius:8px;font-size:.8rem;}} 
.progress{{height:8px;background:#1d2733;border-radius:4px;overflow:hidden;margin:.4rem 0 1rem;}} .progress span{{display:block;height:100%;background:linear-gradient(90deg,#2563eb,#4f46e5);}} 
</style></head><body>"""

HTML_FOOT = """<footer><small>Généré automatiquement - Structure 4ème | Révisions: J+1 • J+3 • J+7 • J+14</small></footer></body></html>"""

COURSE_TEMPLATE = """
<header>
  <h1>{chapter_number} – {chapter_title}</h1>
  <nav>
    <a href="../exercices/exercices_niveau1_decouverte.html">Exercices N1</a>
    <a href="../exercices/exercices_niveau2_pratique.html">Exercices N2</a>
    <a href="../exercices/exercices_niveau3_defi.html">Exercices N3</a>
    <a href="../corrections/corrections_detaillees.html">Corrections</a>
    <a href="../fiches_resume/fiche_synthese.html">Fiche Synthèse</a>
    <a href="../evaluations/evaluation_formative.html">Évaluation</a>
  </nav>
  <div class="progress" aria-label="Progression estimée"><span style="width:8%"></span></div>
  <div>
    <span class="badge">Objectifs</span>
    <span class="badge">Prérequis</span>
    <span class="badge">Différenciation</span>
    <span class="badge">Métacognition</span>
  </div>
</header>

<section>
  <h2>1. Introduction & Motivation</h2>
  <p><strong>Pourquoi c'est utile :</strong> {motivation}</p>
  <p><strong>Contexte concret :</strong> {context}</p>
  <p><strong>Objectif final :</strong> Être capable de {objectif_final}.</p>
</section>

<section>
  <h2>2. Prérequis Indispensables</h2>
  <ul>
    {prerequis_list}
  </ul>
  <div class="notice">Si un prérequis est manquant : revoir rapidement l'exemple guidé ou utiliser une mini-fiche.</div>
</section>

<section>
  <h2>3. Découverte Guidée (Étapes)</h2>
  {etapes_blocs}
</section>

<section>
  <h2>4. Schéma / Visualisation</h2>
  <p>{schema}</p>
</section>

<section>
  <h2>5. Méthode en 3 étapes</h2>
  <ol>
    {methode_steps}
  </ol>
  <p class="notice">Indice auto-contrôle : « Ai-je appliqué chaque étape dans l'ordre ? »</p>
</section>

<section>
  <h2>6. Erreurs Fréquentes</h2>
  <ul>
    {erreurs}
  </ul>
</section>

<section>
  <h2>7. Mini Auto-Évaluation Immédiate</h2>
  <ul>
    <li>Je peux expliquer avec mes mots : {notion_cle}.</li>
    <li>Je sais appliquer la méthode sans modèle.</li>
    <li>Je repère mes erreurs et je les corrige.</li>
  </ul>
</section>

<section>
  <h2>8. Plan de Réactivation</h2>
  <ul>
    <li>J+1 : refaire 2 ex. N1 + 1 ex. N2</li>
    <li>J+3 : refaire 2 ex. N2 + 1 ex. N3</li>
    <li>J+7 : mini-quiz 5 questions</li>
    <li>J+14 : problème mixte</li>
  </ul>
</section>
"""

EXERCISES_LEVEL = {
    1: {
        "intro": "Exercices guidés pour comprendre pas à pas.",
        "types": ["Compléter des opérations simples", "Choisir la bonne représentation", "Vrai/Faux avec justification"],
    },
    2: {
        "intro": "Consolider la méthode avec des situations standard.",
        "types": ["Résolution directe", "Choisir la bonne stratégie", "Problèmes courts"],
    },
    3: {
        "intro": "Défis pour transférer et réfléchir.",
        "types": ["Problèmes ouverts", "Situation inverse", "Erreur à analyser"],
    },
}

EXERCICES_TEMPLATE = """
<header><h1>{chapter_title} – Exercices Niveau {niveau}</h1><nav><a href="../cours/cours_principal.html">Cours</a></nav></header>
<section>
<p><strong>Objectif du niveau {niveau} :</strong> {intro}</p>
<h2>Formats</h2>
<ul>{formats}</ul>
<h2>Série d'exercices</h2>
{exercices}
</section>
"""

CORRECTIONS_DETAILLEES = """
<header><h1>{chapter_title} – Corrections détaillées</h1><nav><a href="../cours/cours_principal.html">Cours</a></nav></header>
<section>
<h2>Corrections pas à pas</h2>
{corrections_blocs}
</section>
<section>
<h2>Stratégies de vérification</h2>
<ul>{verifications}</ul>
</section>
"""

AUTO_CORRECTION = """
<header><h1>{chapter_title} – Auto-correction</h1><nav><a href="../cours/cours_principal.html">Cours</a></nav></header>
<section>
<table style='width:100%;border-collapse:collapse;font-size:.85rem;'>
<tr><th style='text-align:left;border-bottom:1px solid #333;'>Élément</th><th style='text-align:left;border-bottom:1px solid #333;'>Je réussis ?</th><th style='text-align:left;border-bottom:1px solid #333;'>Action si non</th></tr>
{rows}
</table>
</section>
"""

ERREURS_FREQ = """
<header><h1>{chapter_title} – Erreurs fréquentes</h1><nav><a href="../cours/cours_principal.html">Cours</a></nav></header>
<section>
{items}
</section>
"""

FICHE_SYNTHESE = """
<header><h1>Fiche Synthèse – {chapter_title}</h1><nav><a href="../cours/cours_principal.html">Cours</a></nav></header>
<section><h2>À retenir</h2><ul>{points}</ul></section>
<section><h2>Mini Quiz</h2><ol>{quiz}</ol></section>
"""

FICHE_METHODE = """
<header><h1>Fiche Méthode – {chapter_title}</h1><nav><a href="../cours/cours_principal.html">Cours</a></nav></header>
<section><ol>{etapes}</ol></section>
"""

FICHE_MEMO = """
<header><h1>Fiche Mémorisation – {chapter_title}</h1><nav><a href="../cours/cours_principal.html">Cours</a></nav></header>
<section><ul>{memotech}</ul></section>
"""

EVAL_FORM = """
<header><h1>Évaluation formative – {chapter_title}</h1><nav><a href="../cours/cours_principal.html">Cours</a></nav></header>
<section><ol>{questions}</ol></section>
"""

EVAL_SOMM = """
<header><h1>Évaluation sommative – {chapter_title}</h1><nav><a href="../cours/cours_principal.html">Cours</a></nav></header>
<section><ol>{questions}</ol></section>
"""

GRILLE_COMP = """
<header><h1>Grille de compétences – {chapter_title}</h1><nav><a href="../cours/cours_principal.html">Cours</a></nav></header>
<section>
<table style='width:100%;border-collapse:collapse;font-size:.8rem;'>
<tr><th style='text-align:left;border-bottom:1px solid #333;'>Compétence</th><th style='text-align:left;border-bottom:1px solid #333;'>Niveau 1</th><th style='text-align:left;border-bottom:1px solid #333;'>Niveau 2</th><th style='text-align:left;border-bottom:1px solid #333;'>Niveau 3</th></tr>
{rows}
</table>
</section>
"""

# Minimal pedagogical metadata per chapter (simplified)
CHAPTER_META = {
    "01_Nombres_relatifs": {
        "motivation": "Gérer les gains et pertes, températures et altitudes.",
        "context": "Comparaison de températures : -3°C / +5°C.",
        "objectif_final": "additionner et soustraire des nombres relatifs correctement",
        "prerequis": ["Sens du signe -", "Droite graduée", "Addition de nombres entiers"],
        "etapes": [
            ("Observer", "Repérer les signes et magnitudes."),
            ("Représenter", "Placer sur une droite graduée pour visualiser."),
            ("Calculer", "Appliquer règle selon signes identiques ou différents."),
        ],
        "schema": "Droite graduée avec positions -5, -2, 0, +3, +6.",
        "methode": [
            "Même signe : additionner les valeurs absolues et garder le signe.",
            "Signes différents : soustraire les valeurs absolues et prendre le signe du plus grand en valeur absolue.",
            "Vérifier avec un exemple concret (température ou argent).",
        ],
        "erreurs": [
            "Ignorer le signe devant le nombre.",
            "Faire addition au lieu de soustraction quand signes différents.",
            "Oublier de re-vérifier avec un exemple concret.",
        ],
        "notion": "Addition/Soustraction relatifs",
    },
}

# For other chapters, we can clone template with slight adjustments
DEFAULT_META = {
    "motivation": "Compétence essentielle pour comprendre d'autres notions.",
    "context": "Situation concrète simple liée à la vie quotidienne.",
    "objectif_final": "appliquer correctement la notion dans des exercices standards",
    "prerequis": ["Notions précédentes essentielles", "Vocabulaire de base"],
    "etapes": [
        ("Observer", "Identifier les données, mots-clés ou structures."),
        ("Structurer", "Mettre en forme / schéma / classification."),
        ("Appliquer", "Utiliser la règle ou méthode correspondante."),
    ],
    "schema": "Schéma simple illustrant la relation clé.",
    "methode": [
        "Identifier ce qu'on cherche.",
        "Choisir la règle / propriété adaptée.",
        "Appliquer et vérifier la cohérence du résultat.",
    ],
    "erreurs": [
        "Confusion de vocabulaire.",
        "Application d'une mauvaise règle.",
        "Absence de vérification finale.",
    ],
    "notion": "Notion principale",
}

# Fill missing metadata
for slug, title in chapters:
    if slug not in CHAPTER_META:
        CHAPTER_META[slug] = DEFAULT_META.copy()


def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def html_wrap(title: str, body: str) -> str:
    return HTML_HEAD.format(title=title) + body + HTML_FOOT


def build_course(slug: str, title: str, meta: dict) -> str:
    prereq_html = "\n".join(f"<li>{p}</li>" for p in meta["prerequis"])
    etapes_blocks = "".join(
        f"<article class='card'><h3>Étape {i+1} – {nom}</h3><p>{desc}</p>" \
        f"<p><em>Variante si blocage :</em> reformuler avec un exemple concret.</p></article>"
        for i, (nom, desc) in enumerate(meta["etapes"])
    )
    methode_steps = "\n".join(f"<li>{s}</li>" for s in meta["methode"])
    erreurs = "\n".join(f"<li>{e}</li>" for e in meta["erreurs"])
    return COURSE_TEMPLATE.format(
        chapter_number=slug.split('_')[0],
        chapter_title=title,
        motivation=meta["motivation"],
        context=meta["context"],
        objectif_final=meta["objectif_final"],
        prerequis_list=prereq_html,
        etapes_blocs=etapes_blocks,
        schema=meta["schema"],
        methode_steps=methode_steps,
        erreurs=erreurs,
        notion_cle=meta["notion"],
    )


def build_exercises(slug: str, title: str, level: int) -> str:
    spec = EXERCISES_LEVEL[level]
    formats = "".join(f"<li>{t}</li>" for t in spec["types"])
    # 5 placeholder exercises
    exercices = []
    for i in range(1,6):
        exercices.append(f"<article class='card'><h3>Exercice {i}</h3><p>Énoncé adapté niveau {level}. Ajouter contexte concret.</p><p><em>Indice 1 :</em> Penser à identifier les données.</p></article>")
    return EXERCICES_TEMPLATE.format(chapter_title=title, niveau=level, intro=spec["intro"], formats=formats, exercices="\n".join(exercices))


def build_corrections(title: str) -> str:
    corrections_blocs = "".join(
        f"<article class='card'><h3>Exercice {i}</h3><p>Rappel de l'énoncé (résumé).</p><ol><li>Étape 1 justifiée</li><li>Étape 2</li><li>Conclusion</li></ol><p><strong>Auto-vérif :</strong> Le résultat est-il cohérent ?</p></article>" for i in range(1,6)
    )
    verifications = "\n".join(
        f"<li>{txt}</li>" for txt in [
            "Ai-je recopié correctement les données ?",
            "Chaque transformation est-elle autorisée ?",
            "Le résultat final a-t-il du sens ?",
        ]
    )
    return CORRECTIONS_DETAILLEES.format(chapter_title=title, corrections_blocs=corrections_blocs, verifications=verifications)


def build_auto_correction(title: str) -> str:
    rows = "".join(
        f"<tr><td>{c}</td><td>[ ]</td><td>{a}</td></tr>" for c, a in [
            ("Je lis l'énoncé entièrement", "Relire à voix basse"),
            ("Je repère ce qui est demandé", "Entourer le verbe clé"),
            ("J'applique une méthode adaptée", "Revoir fiche méthode"),
            ("Je vérifie le sens du résultat", "Comparer à un exemple"),
        ]
    )
    return AUTO_CORRECTION.format(chapter_title=title, rows=rows)


def build_erreurs_freq(title: str, meta: dict) -> str:
    items = "".join(
        f"<article class='card'><h3>Erreur</h3><p>{e}</p><p><strong>Stratégie :</strong> Ajouter justification / exemple.</p></article>" for e in meta["erreurs"]
    )
    return ERREURS_FREQ.format(chapter_title=title, items=items)


def build_fiche_synthese(title: str, meta: dict) -> str:
    points = "".join(f"<li>{p}</li>" for p in meta["methode"][:3])
    quiz = "".join(f"<li>Question courte {i}</li>" for i in range(1,6))
    return FICHE_SYNTHESE.format(chapter_title=title, points=points, quiz=quiz)


def build_fiche_methode(title: str, meta: dict) -> str:
    etapes = "".join(f"<li>{i+1}. {s}</li>" for i, s in enumerate(meta["methode"]))
    return FICHE_METHODE.format(chapter_title=title, etapes=etapes)


def build_fiche_memo(title: str, meta: dict) -> str:
    memotech = "".join(f"<li>Astuce : {s[:50]}...</li>" for s in meta["methode"]) + "<li>Repérer mots-clés.</li>"
    return FICHE_MEMO.format(chapter_title=title, memotech=memotech)


def build_eval_form(title: str) -> str:
    questions = "".join(f"<li>Question formative {i}</li>" for i in range(1,8))
    return EVAL_FORM.format(chapter_title=title, questions=questions)


def build_eval_somm(title: str) -> str:
    questions = "".join(f"<li>Exercice sommative {i}</li>" for i in range(1,6))
    return EVAL_SOMM.format(chapter_title=title, questions=questions)


def build_grille_comp(title: str) -> str:
    rows = "".join(
        f"<tr><td>{c}</td><td>Guidé</td><td>Autonome</td><td>Transfert</td></tr>" for c in [
            "Comprendre l'énoncé",
            "Choisir la méthode",
            "Réaliser le calcul",
            "Justifier le résultat",
        ]
    )
    return GRILLE_COMP.format(chapter_title=title, rows=rows)


def write(path: str, content: str):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html_wrap(os.path.basename(path), content))


def build_json_meta(slug: str, title: str, meta: dict, base_path: str):
    data = {
        "slug": slug,
        "titre": title,
        "objectifs": meta["methode"],
        "prerequis": meta["prerequis"],
        "erreurs_frequentes": meta["erreurs"],
        "plan_reactivation": ["J+1", "J+3", "J+7", "J+14"],
    }
    with open(os.path.join(base_path, 'cours', 'data_chapitre.json'), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    for slug, title in chapters:
        chapter_dir = os.path.join(BASE_DIR, slug)
        for sf in SUBFOLDERS:
            ensure_dir(os.path.join(chapter_dir, sf))
        meta = CHAPTER_META[slug]

        # Cours
        course_html = build_course(slug, title, meta)
        write(os.path.join(chapter_dir, 'cours', 'cours_principal.html'), course_html)

        # Exercices N1-N3
        for lvl in (1,2,3):
            ex_html = build_exercises(slug, title, lvl)
            write(os.path.join(chapter_dir, 'exercices', f'exercices_niveau{lvl}_decouverte.html' if lvl==1 else f'exercices_niveau{lvl}_pratique.html' if lvl==2 else f'exercices_niveau{lvl}_defi.html'), ex_html)

        # Corrections
        write(os.path.join(chapter_dir, 'corrections', 'corrections_detaillees.html'), build_corrections(title))
        write(os.path.join(chapter_dir, 'corrections', 'auto_correction.html'), build_auto_correction(title))
        write(os.path.join(chapter_dir, 'corrections', 'erreurs_frequentes.html'), build_erreurs_freq(title, meta))

        # Fiches
        write(os.path.join(chapter_dir, 'fiches_resume', 'fiche_synthese.html'), build_fiche_synthese(title, meta))
        write(os.path.join(chapter_dir, 'fiches_resume', 'fiche_methode.html'), build_fiche_methode(title, meta))
        write(os.path.join(chapter_dir, 'fiches_resume', 'fiche_memorisation.html'), build_fiche_memo(title, meta))

        # Evaluations
        write(os.path.join(chapter_dir, 'evaluations', 'evaluation_formative.html'), build_eval_form(title))
        write(os.path.join(chapter_dir, 'evaluations', 'evaluation_sommative.html'), build_eval_somm(title))
        write(os.path.join(chapter_dir, 'evaluations', 'grille_competences.html'), build_grille_comp(title))

        # JSON meta
        build_json_meta(slug, title, meta, chapter_dir)

    print("Génération terminée pour", len(chapters), "chapitres.")

if __name__ == '__main__':
    main()
