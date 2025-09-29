#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour repositionner les éléments avec icônes juste après les titres
selon la nouvelle règle de la rétro-spécification.
"""

import re

def fix_icons_position():
    file_path = "College_4ieme_Maths/01_Nombres_relatifs/cours/cours_principal.html"
    
    # Lire le fichier
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Définir les patterns de remplacement
    replacements = [
        # 1. Objectif du chapitre juste après le titre Introduction
        {
            'old': r'(<h2>🎯 1\. Introduction et objectif</h2>\n) (<p><strong>Pourquoi.*?</p>\n <blockquote>.*?</blockquote>\n) (<div class=\'tip-context\'>🌍.*?</div>)',
            'new': r'\1\3\n \2'
        },
        
        # 2. Mini-tests après les titres de prérequis
        {
            'old': r'(<h3>📍 Sens du signe moins</h3>\n)   (<p><strong>Je reconnais.*?</p>\n   <p><em>Exemples.*?</p>\n)   (<div class=\'tip-verify\'>💡.*?</div>)',
            'new': r'\1   \3\n   \2'
        },
        
        {
            'old': r'(<h3>📏 Lecture droite graduée</h3>\n)   (<p><strong>Je sais.*?</p>\n   <p><em>Exemples.*?</p>\n)   (<div class=\'tip-verify\'>💡.*?</div>)',
            'new': r'\1   \3\n   \2'
        },
        
        {
            'old': r'(<h3>⚡ Priorités calcul simple</h3>\n)   (<p><strong>Je respecte.*?</p>\n   <p><em>Exemples.*?</p>\n)   (<div class=\'tip-verify\'>💡.*?</div>)',
            'new': r'\1   \3\n   \2'
        },
        
        # 3. Mémo après le titre Astuce de navigation  
        {
            'old': r'(<h4>🎯 Astuce de navigation</h4>\n)   (<p><strong>Règle simple.*?</p>\n   <p><em>Exemple.*?</p>\n)   (<div class=\'tip-method\'>⚡.*?</div>)',
            'new': r'\1   \3\n   \2'
        },
        
        # 4. Vérification après le titre Phase 1
        {
            'old': r'(<h4>Phase 1 – 100% guidé</h4>\n)    (<p><em>Calcul.*?</p>\n    <ol.*?</ol>\n)    (<div class=\'tip-verify\'>💡.*?</div>)',
            'new': r'\1    \3\n    \2'
        },
    ]
    
    # Appliquer les remplacements
    for replacement in replacements:
        pattern = replacement['old']
        new_text = replacement['new']
        content = re.sub(pattern, new_text, content, flags=re.DOTALL)
    
    # Écrire le fichier modifié
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Repositionnement des icônes terminé avec succès!")

if __name__ == "__main__":
    fix_icons_position()