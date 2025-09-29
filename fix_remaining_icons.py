#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script complémentaire pour repositionner les icônes restantes
dans les sections de méthode illustrée et phases d'apprentissage.
"""

import re

def fix_remaining_icons():
    file_path = "College_4ieme_Maths/01_Nombres_relatifs/cours/cours_principal.html"
    
    # Lire le fichier
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Rechercher et remplacer les patterns plus complexes
    
    # 1. Astuce de navigation - Mémo
    content = re.sub(
        r'(<h4>🎯 Astuce de navigation</h4>\n)   (<p><strong>Règle simple.*?</p>\n   <p><em>Exemple.*?</p>\n)   (<div class=\'tip-method\'>⚡.*?</div>)',
        r'\1   \3\n   \2',
        content,
        flags=re.DOTALL
    )
    
    # 2. Phase 1 - Vérification  
    content = re.sub(
        r'(<h4>Phase 1 – 100% guidé</h4>\n)    (<p><em>Calcul.*?</em> \(.*?\)</p>\n    <ol class=\'mt-narrow\'>.*?</ol>\n)    (<div class=\'tip-verify\'>💡.*?</div>)',
        r'\1    \3\n    \2',
        content,
        flags=re.DOTALL
    )
    
    # 3. Étape 1 Même signe - Contexte
    content = re.sub(
        r'(<h3>🔹 Étape 1 : Même signe</h3>\n)   (<div class=\'regle-encadree\'>.*?</div>\n   <p><em>Exemple.*?</p>\n   <p>.*?</p>\n)   (<div class=\'tip-context\'>🌍.*?</div>)',
        r'\1   \3\n   \2',
        content,
        flags=re.DOTALL
    )
    
    # 4. Étape 2 Signes différents - Contexte
    content = re.sub(
        r'(<h3>🔸 Étape 2 : Signes différents</h3>\n)   (<div class=\'regle-encadree\'>.*?</div>\n   <p><em>Exemple.*?</p>\n   <p>.*?</p>\n)   (<div class=\'tip-context\'>🌍.*?</div>)',
        r'\1   \3\n   \2',
        content,
        flags=re.DOTALL
    )
    
    # 5. Étape 2 bis - Contexte  
    content = re.sub(
        r'(<h3>🔸 Étape 2 bis : Signes différents \(inverse\)</h3>\n)   (<div class=\'regle-encadree\'>.*?</div>\n   <p><em>Exemple.*?</p>\n   <p>.*?</p>\n)   (<div class=\'tip-context\'>🌍.*?</div>)',
        r'\1   \3\n   \2',
        content,
        flags=re.DOTALL
    )
    
    # 6. Étape 3 Contrôle - Question clé et Tests
    content = re.sub(
        r'(<h3>✅ Étape 3 : Contrôle</h3>\n)   (<div class=\'regle-encadree\'>.*?</div>\n)   (<div class=\'tip-method\'>⚡.*?</div>\n   <div class=\'tip-verify\'>💡.*?</div>)',
        r'\1   \3\n   \2',
        content,
        flags=re.DOTALL
    )
    
    # Écrire le fichier modifié
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Repositionnement des icônes restantes terminé!")

if __name__ == "__main__":
    fix_remaining_icons()