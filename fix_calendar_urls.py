#!/usr/bin/env python3
"""
Script pour corriger les URLs Google Calendar
Remplace les chemins relatifs par les URLs GitHub Pages complètes
"""

import os
import re
from pathlib import Path

def fix_calendar_urls(file_path: Path, chapter_slug: str):
    """
    Corrige les URLs dans les événements Google Calendar d'un fichier cours
    """
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Remplacer les URLs relatives par les URLs GitHub Pages complètes
        if 'addSingleEventToCalendar' in content:
            # Pattern pour les URLs relatives
            base_url = f'https://geo92fr-dev.github.io/Learning/College_4ieme_Maths/{chapter_slug}'
            
            # Corrections des URLs
            replacements = [
                (f"url: '/College_4ieme_Maths/{chapter_slug}/exercices/exercices_niveau1_decouverte.html'",
                 f"url: '{base_url}/exercices/exercices_niveau1_decouverte.html'"),
                (f"url: '/College_4ieme_Maths/{chapter_slug}/exercices/exercices_niveau2_pratique.html'",
                 f"url: '{base_url}/exercices/exercices_niveau2_pratique.html'"),
                (f"url: '/College_4ieme_Maths/{chapter_slug}/fiches_resume/fiche_synthese.html'",
                 f"url: '{base_url}/fiches_resume/fiche_synthese.html'"),
                (f"url: '/College_4ieme_Maths/{chapter_slug}/exercices/exercices_niveau3_defi.html'",
                 f"url: '{base_url}/exercices/exercices_niveau3_defi.html'")
            ]
            
            for old_url, new_url in replacements:
                content = content.replace(old_url, new_url)
            
            # Corriger l'utilisation de window.location.origin
            content = content.replace(
                '`${config.description}\\n\\nLien direct : ${window.location.origin}${config.url}`',
                '`${config.description}\\n\\nLien direct : ${config.url}`'
            )
        
        # Sauvegarder seulement si des modifications ont été apportées
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"Erreur lors du traitement de {file_path}: {e}")
        return False

def fix_all_calendar_urls():
    """
    Corrige les URLs dans tous les chapitres de maths
    """
    
    base_dir = Path("c:/Project_Learning_Simplified/College_4ieme_Maths")
    
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
        ("12_Solides_et_volumes", "Solides et volumes")
    ]
    
    fixed_count = 0
    
    for chapter_slug, chapter_title in chapters:
        cours_file = base_dir / chapter_slug / "cours" / "cours_principal.html"
        
        if cours_file.exists():
            print(f"Correction URLs : {chapter_title}")
            if fix_calendar_urls(cours_file, chapter_slug):
                print(f"  ✅ URLs corrigées vers GitHub Pages")
                fixed_count += 1
            else:
                print(f"  ℹ️ URLs déjà correctes")
        else:
            print(f"  ❌ Fichier manquant : {cours_file}")
    
    print(f"\n📊 Résumé : {fixed_count} fichiers corrigés sur {len(chapters)} chapitres")

if __name__ == "__main__":
    fix_all_calendar_urls()