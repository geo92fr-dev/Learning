#!/usr/bin/env python3
"""
Script pour uniformiser tous les cours_principal.html :
- Expliciter les noms des exercices (Ex N1 -> Exercice Niveau 1)
- Supprimer les éléments de progression et badges
- Supprimer la légende avec bullet points
"""

import os
import re
from pathlib import Path
from typing import List

def update_cours_principal_file(file_path: Path) -> bool:
    """
    Met à jour un fichier cours_principal.html avec les nouvelles conventions
    Retourne True si des modifications ont été faites
    """
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        modifications = 0
        
        # 1. Expliciter les noms des exercices dans la navigation
        nav_patterns = [
            (r"<a href='([^']*)'>Ex N1</a>", r"<a href='\1'>Exercice Niveau 1</a>"),
            (r"<a href='([^']*)'>Ex N2</a>", r"<a href='\1'>Exercice Niveau 2</a>"),
            (r"<a href='([^']*)'>Ex N3</a>", r"<a href='\1'>Exercice Niveau 3</a>")
        ]
        
        for pattern, replacement in nav_patterns:
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content)
                modifications += 1
        
        # 2. Supprimer la barre de progression et les badges
        progress_pattern = r"</nav>\s*<div class='progress'><span[^>]*></span></div>\s*<span class='badge'>[^<]*</span>(?:<span class='badge'>[^<]*</span>)*"
        if re.search(progress_pattern, content):
            content = re.sub(progress_pattern, "</nav>", content)
            modifications += 1
        
        # 3. Supprimer la légende des tips
        legend_pattern = r"<div class='tips-legend'>.*?</div>"
        if re.search(legend_pattern, content, re.DOTALL):
            content = re.sub(legend_pattern, "", content, flags=re.DOTALL)
            modifications += 1
        
        # 4. Nettoyer les styles CSS inutilisés
        css_patterns_to_remove = [
            r"\.progress\{[^}]+\}",
            r"\.progress span\{[^}]+\}",
            r"\.progress-\d+\{[^}]+\}",
            r"\.badge\{[^}]+\}",
            r"\.tips-legend\{[^}]+\}",
            r"\.legend-item\{[^}]+\}",
            r"\.legend-dot\{[^}]+\}",
            r"\.dot-verify\{[^}]+\}",
            r"\.dot-context\{[^}]+\}",
            r"\.dot-method\{[^}]+\}",
        ]
        
        for css_pattern in css_patterns_to_remove:
            if re.search(css_pattern, content):
                content = re.sub(css_pattern, "", content)
                modifications += 1
        
        # 5. Nettoyer les media queries qui référencent .tips-legend
        media_pattern = r"@media \(max-width:760px\)\{[^}]*\.tips-legend[^}]*\}"
        if re.search(media_pattern, content):
            # Remplacer par une version simplifiée
            simple_media = "@media (max-width:760px){nav a{display:inline-block;margin:.25rem .6rem .25rem 0;}}"
            content = re.sub(media_pattern, simple_media, content)
            modifications += 1
        
        # Écrire le fichier seulement s'il y a eu des modifications
        if modifications > 0 and content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
            
    except Exception as e:
        print(f"❌ Erreur avec {file_path}: {e}")
        return False
    
    return False

def main():
    """Fonction principale"""
    
    base_path = Path("c:/Project_Learning_Simplified")
    subjects = [
        "College_4ieme_Maths",
        "College_4ieme_Francais", 
        "College_4ieme_Histoire_Geo",
        "College_4ieme_Sciences_Physiques",
        "College_4ieme_SVT",
        "College_4ieme_Technologie", 
        "College_4ieme_Anglais",
        "College_4ieme_Espagnol",
        "College_4ieme_Arts_Plastiques",
        "College_4ieme_Musique",
        "College_4ieme_EPS",
        "College_4ieme_EMC"
    ]
    
    print("🎯 Uniformisation des cours principaux")
    print("=" * 50)
    print("📝 Modifications à appliquer:")
    print("  • Ex N1 → Exercice Niveau 1")
    print("  • Ex N2 → Exercice Niveau 2") 
    print("  • Ex N3 → Exercice Niveau 3")
    print("  • Suppression barres de progression")
    print("  • Suppression badges (Objectifs, Prérequis, etc.)")
    print("  • Suppression légende bullet points")
    print("  • Nettoyage CSS associé")
    print("=" * 50)
    
    total_files = 0
    total_modified = 0
    
    for subject in subjects:
        subject_path = base_path / subject
        
        if not subject_path.exists():
            continue
            
        print(f"\n📚 {subject}...")
        subject_files = 0
        subject_modified = 0
        
        # Trouver tous les cours_principal.html
        cours_files = list(subject_path.rglob("**/cours/cours_principal.html"))
        
        for cours_file in cours_files:
            chapter_name = cours_file.parent.parent.name
            
            if update_cours_principal_file(cours_file):
                print(f"  ✅ {chapter_name}: Modifié")
                subject_modified += 1
            else:
                print(f"  📄 {chapter_name}: Aucune modification nécessaire")
            
            subject_files += 1
        
        if subject_files > 0:
            print(f"  📊 {subject}: {subject_modified}/{subject_files} fichiers modifiés")
        
        total_files += subject_files
        total_modified += subject_modified
    
    print("\n" + "=" * 50)
    print("🎉 Uniformisation terminée !")
    print(f"📊 Résumé: {total_modified}/{total_files} fichiers modifiés")
    print("\n✅ Interface simplifiée et cohérente !")
    print("✅ Navigation claire avec noms explicites")
    print("✅ Suppression des éléments de progression superflus")

if __name__ == "__main__":
    main()