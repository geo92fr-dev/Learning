#!/usr/bin/env python3
"""
Script pour supprimer tous les raccourcis vers 'Corrections' et 'Évaluation' 
dans toutes les pages principales de toutes les matières
"""

import os
import re
from pathlib import Path
from typing import List, Dict

def get_all_subjects() -> List[str]:
    """Retourne la liste de tous les sujets College_4ieme"""
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
    return subjects

def remove_navigation_links(content: str) -> tuple[str, int]:
    """
    Supprime les liens Corrections et Évaluation de la navigation
    Retourne le contenu modifié et le nombre de suppressions
    """
    modifications = 0
    
    # Pattern pour les liens corrections dans la navigation
    corrections_patterns = [
        r"<a href='[^']*corrections[^']*\.html'>Corrections</a>\s*",
        r"<a href=\"[^\"]*corrections[^\"]*\.html\">Corrections</a>\s*",
    ]
    
    # Pattern pour les liens évaluations dans la navigation  
    evaluations_patterns = [
        r"<a href='[^']*evaluations[^']*\.html'>Évaluation</a>\s*",
        r"<a href=\"[^\"]*evaluations[^\"]*\.html\">Évaluation</a>\s*",
    ]
    
    # Supprimer les liens corrections
    for pattern in corrections_patterns:
        if re.search(pattern, content):
            content = re.sub(pattern, "", content)
            modifications += 1
    
    # Supprimer les liens évaluations
    for pattern in evaluations_patterns:
        if re.search(pattern, content):
            content = re.sub(pattern, "", content) 
            modifications += 1
    
    return content, modifications

def process_cours_principal_files():
    """Traite tous les fichiers cours_principal.html"""
    
    base_path = Path("c:/Project_Learning_Simplified")
    total_files = 0
    total_modifications = 0
    
    print("🎯 Suppression des raccourcis Corrections et Évaluation")
    print("=" * 65)
    
    for subject in get_all_subjects():
        subject_path = base_path / subject
        
        if not subject_path.exists():
            print(f"⚠️  Matière non trouvée: {subject}")
            continue
            
        print(f"\n📚 Traitement de {subject}...")
        subject_files = 0
        subject_modifications = 0
        
        # Trouver tous les dossiers de chapitres
        for chapter_dir in subject_path.iterdir():
            if chapter_dir.is_dir() and not chapter_dir.name.startswith('.'):
                cours_file = chapter_dir / "cours" / "cours_principal.html"
                
                if cours_file.exists():
                    try:
                        # Lire le fichier
                        with open(cours_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # Supprimer les liens
                        new_content, modifications = remove_navigation_links(content)
                        
                        if modifications > 0:
                            # Écrire le fichier modifié
                            with open(cours_file, 'w', encoding='utf-8') as f:
                                f.write(new_content)
                            
                            print(f"  📖 {chapter_dir.name}: {modifications} liens supprimés")
                            subject_modifications += modifications
                        else:
                            print(f"  📖 {chapter_dir.name}: aucun lien trouvé")
                        
                        subject_files += 1
                        
                    except Exception as e:
                        print(f"  ❌ Erreur avec {chapter_dir.name}: {e}")
                        
        print(f"  ✅ {subject}: {subject_files} fichiers traités, {subject_modifications} liens supprimés")
        total_files += subject_files
        total_modifications += subject_modifications
    
    return total_files, total_modifications

def process_index_files():
    """Traite les fichiers index_master_4ieme.html pour supprimer les boutons Éval."""
    
    base_path = Path("c:/Project_Learning_Simplified")
    total_modifications = 0
    
    print(f"\n📋 Traitement des fichiers index...")
    
    for subject in get_all_subjects():
        subject_path = base_path / subject
        index_file = subject_path / "index_master_4ieme.html"
        
        if index_file.exists():
            try:
                with open(index_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Pattern pour les boutons Éval. dans l'index
                eval_patterns = [
                    r'<a href="[^"]*evaluations[^"]*\.html" class="btn btn-secondary">Éval\.[^<]*</a>\s*',
                    r'<a href="[^"]*evaluations[^"]*\.html" class="btn btn-secondary">Éval\. formative</a>\s*'
                ]
                
                modifications = 0
                for pattern in eval_patterns:
                    matches = len(re.findall(pattern, content))
                    if matches > 0:
                        content = re.sub(pattern, "", content)
                        modifications += matches
                
                if modifications > 0:
                    with open(index_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print(f"  📄 {subject}: {modifications} boutons Éval. supprimés")
                    total_modifications += modifications
                else:
                    print(f"  📄 {subject}: aucun bouton Éval. trouvé")
                    
            except Exception as e:
                print(f"  ❌ Erreur avec {subject}: {e}")
    
    return total_modifications

def main():
    """Fonction principale"""
    
    # Traiter les cours principaux
    files_processed, links_removed = process_cours_principal_files()
    
    # Traiter les fichiers index
    index_modifications = process_index_files()
    
    # Résumé final
    print("\n" + "=" * 65)
    print("🎉 Suppression terminée !")
    print(f"\n📊 Résumé:")
    print(f"   📁 Fichiers cours_principal.html traités: {files_processed}")
    print(f"   🔗 Liens navigation supprimés: {links_removed}")
    print(f"   🔘 Boutons index supprimés: {index_modifications}")
    print(f"   📊 Total suppressions: {links_removed + index_modifications}")
    
    print(f"\n📋 Structure de navigation optimisée:")
    print(f"   ✅ Cours → Contenu principal")  
    print(f"   ✅ Ex N1/N2/N3 → Exercices pratiques")
    print(f"   ✅ Synthèse → Fiches résumé interactives")
    print(f"   ❌ Corrections → Supprimé (redondant)")
    print(f"   ❌ Évaluation → Supprimé (dossier inexistant)")
    
    print(f"\n✅ Navigation simplifiée et cohérente sur toutes les matières !")

if __name__ == "__main__":
    main()