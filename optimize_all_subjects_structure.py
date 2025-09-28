#!/usr/bin/env python3
"""
Script d'optimisation de la structure des matières de 4ème
Supprime les dossiers redondants corrections/ et evaluations/ 
dans toutes les matières et tous les chapitres.

Philosophie: Chaque dossier doit avoir un rôle unique
- cours/ : Contenu principal d'apprentissage
- exercices/ : Pratique avec corrections intégrées  
- fiches_resume/ : Synthèses avec quiz interactifs
"""

import os
import shutil
from pathlib import Path

def optimize_subject_structure():
    """Optimise la structure de toutes les matières"""
    base_dir = Path("c:/Project_Learning_Simplified")
    
    # Liste des matières à traiter
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
    
    # Dossiers à supprimer (redondants)
    folders_to_remove = ["corrections", "evaluations"]
    
    total_removed = 0
    
    print("🎯 Optimisation de la structure des matières de 4ème")
    print("=" * 60)
    
    for subject in subjects:
        subject_path = base_dir / subject
        
        if not subject_path.exists():
            print(f"⚠️  Matière {subject} non trouvée, ignorée")
            continue
            
        print(f"\n📚 Traitement de {subject}...")
        
        # Parcourir tous les chapitres dans la matière
        chapter_count = 0
        removed_count = 0
        
        for chapter_dir in subject_path.iterdir():
            if chapter_dir.is_dir() and not chapter_dir.name.startswith('.'):
                # Ignorer les fichiers spéciaux
                if chapter_dir.name in ['index_master_4ieme.html', 'README.md']:
                    continue
                    
                chapter_count += 1
                print(f"  📖 Chapitre: {chapter_dir.name}")
                
                # Supprimer les dossiers redondants
                for folder_name in folders_to_remove:
                    folder_path = chapter_dir / folder_name
                    if folder_path.exists():
                        try:
                            shutil.rmtree(folder_path)
                            print(f"    ❌ Supprimé: {folder_name}/")
                            removed_count += 1
                            total_removed += 1
                        except Exception as e:
                            print(f"    ⚠️  Erreur suppression {folder_name}/: {e}")
                    else:
                        print(f"    ✅ {folder_name}/ déjà absent")
                        
                # Vérifier la structure finale
                remaining_folders = [d.name for d in chapter_dir.iterdir() if d.is_dir()]
                print(f"    📁 Structure finale: {', '.join(remaining_folders)}")
        
        print(f"  ✅ {subject}: {chapter_count} chapitres traités, {removed_count} dossiers supprimés")
    
    print("\n" + "=" * 60)
    print(f"🎉 Optimisation terminée ! {total_removed} dossiers redondants supprimés")
    print("\n📋 Structure optimisée:")
    print("   cours/ → Contenu principal d'apprentissage")
    print("   exercices/ → Pratique avec corrections intégrées") 
    print("   fiches_resume/ → Synthèses avec quiz interactifs")

if __name__ == "__main__":
    try:
        optimize_subject_structure()
        print("\n✅ Script exécuté avec succès !")
    except Exception as e:
        print(f"\n❌ Erreur lors de l'exécution: {e}")