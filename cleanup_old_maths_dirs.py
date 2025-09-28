import os, shutil, datetime

BASE = 'College_4ieme_Maths'
ARCHIVE_NAME = f'_ARCHIVE_OBSOLETE_{datetime.date.today()}'
ARCHIVE_PATH = os.path.join(BASE, ARCHIVE_NAME)

# Canonical (to keep) according to enrich_maths_courses.py
KEEP = {
    '01_Nombres_relatifs',
    '02_Fractions_et_calculs',
    '03_Puissances_et_notation_scientifique',
    '04_Calcul_litteral',
    '05_Equations_simples',
    '06_Proportionnalite_et_pourcentages',
    '07_Statistiques',
    '08_Probabilites',
    '09_Theoreme_de_Pythagore',
    '10_Geometrie_des_triangles_et_Thales',
    '11_Transformations_et_symetries',
    '12_Solides_et_volumes'
}

# Detect candidates: any directory inside BASE starting with 0* or 1* not in KEEP
candidates = []
for name in os.listdir(BASE):
    full = os.path.join(BASE, name)
    if os.path.isdir(full) and (name[:2].isdigit()):
        if name not in KEEP:
            candidates.append(name)

if not candidates:
    print('Aucun dossier obsolète détecté. Rien à faire.')
    raise SystemExit

os.makedirs(ARCHIVE_PATH, exist_ok=True)

log_lines = []
for d in sorted(candidates):
    src = os.path.join(BASE, d)
    dest = os.path.join(ARCHIVE_PATH, d)
    # Build file listing
    listing = []
    for root, dirs, files in os.walk(src):
        rel_root = os.path.relpath(root, src)
        for f in files:
            listing.append(os.path.join(rel_root, f))
    log_lines.append(f'## {d}\n' + ("\n".join(sorted(listing)) or '(vide)') + '\n')
    print(f'Déplacement : {d} -> {ARCHIVE_NAME}/{d}')
    shutil.move(src, dest)

# Write log
with open(os.path.join(ARCHIVE_PATH, 'ARCHIVE_CONTENTS.md'), 'w', encoding='utf-8') as f:
    f.write('# Archive des dossiers mathématiques obsolètes\n\n')
    f.write('Les dossiers suivants ont été déplacés au lieu d\'être supprimés pour conservation.\n\n')
    f.write('\n---\n'.join(log_lines))

print('\nOpération terminée. Dossiers archivés :', ', '.join(sorted(candidates)))
print('Archive située dans :', ARCHIVE_PATH)
print('Vous pouvez supprimer manuellement ce répertoire plus tard si tout est validé.')
