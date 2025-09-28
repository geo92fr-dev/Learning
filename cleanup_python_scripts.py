#!/usr/bin/env python3
"""
Script de nettoyage des fichiers Python obsolètes
Catégorise et supprime les scripts qui ne servent plus à rien

Catégories:
1. SCRIPTS UTILES À CONSERVER - Outils d'automatisation réutilisables
2. SCRIPTS HISTORIQUES À ARCHIVER - Références pour la documentation  
3. SCRIPTS OBSOLÈTES À SUPPRIMER - One-shot terminés, doublons, etc.
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

def analyze_and_cleanup_python_scripts():
    """Analyse et nettoie les scripts Python"""
    
    base_dir = Path("c:/Project_Learning_Simplified")
    
    # Catégorisation des scripts
    scripts_to_keep = {
        # Scripts d'automatisation réutilisables
        "fix_css_backdrop_filter.py": "Outil de correction CSS réutilisable",
        "clean_vscode_references.py": "Outil de nettoyage VS Code",
        "force_clean_vscode_cache.py": "Outil de nettoyage cache avancé"
    }
    
    scripts_to_archive = {
        # Scripts de référence historique
        "optimize_all_subjects_structure.py": "Référence de la grande optimisation du 28/09",
        "remove_shortcuts_corrections_evaluations.py": "Référence nettoyage navigation",
        "uniformize_cours_navigation.py": "Référence standardisation interface",
        "validate_navigation_cleanup.py": "Script de validation post-optimization"
    }
    
    scripts_to_delete = {
        # Scripts obsolètes / one-shot / doublons
        "add_webkit_backdrop_filter_prefix.py": "Doublon de fix_css_backdrop_filter.py",
        "build_index.py": "Script de construction obsolète", 
        "cleanup_old_maths_dirs.py": "One-shot terminé",
        "create_all_subjects_structure.py": "One-shot de création terminé",
        "create_subject_readmes.py": "One-shot de création terminé",
        "enrich_maths_courses.py": "Générateur de cours obsolète",
        "generate_course_page.py": "Générateur obsolète",
        "generate_maths_courses.py": "Générateur de cours obsolète",
        "inject_course.py": "Script d'injection obsolète",
        "inject_master_simple.py": "Script d'injection obsolète", 
        "test_index_master.py": "Script de test obsolète"
    }
    
    # Créer le dossier d'archive
    archive_dir = base_dir / "scripts_archive"
    archive_dir.mkdir(exist_ok=True)
    
    print("=== ANALYSE DES SCRIPTS PYTHON ===\n")
    
    # Traitement des scripts
    deleted_count = 0
    archived_count = 0
    kept_count = 0
    
    # Conserver les scripts utiles
    print("📦 SCRIPTS CONSERVÉS (utiles):")
    for script, reason in scripts_to_keep.items():
        script_path = base_dir / script
        if script_path.exists():
            print(f"  ✅ {script} - {reason}")
            kept_count += 1
    
    print(f"\n📁 SCRIPTS ARCHIVÉS ({archive_dir}):")
    for script, reason in scripts_to_archive.items():
        script_path = base_dir / script
        if script_path.exists():
            # Archiver avec timestamp
            timestamp = datetime.now().strftime("%Y%m%d")
            archived_name = f"{timestamp}_{script}"
            shutil.move(str(script_path), str(archive_dir / archived_name))
            print(f"  📦 {script} → {archived_name} - {reason}")
            archived_count += 1
    
    print(f"\n🗑️  SCRIPTS SUPPRIMÉS:")
    for script, reason in scripts_to_delete.items():
        script_path = base_dir / script
        if script_path.exists():
            os.remove(script_path)
            print(f"  ❌ {script} - {reason}")
            deleted_count += 1
    
    print(f"\n=== RÉSUMÉ DU NETTOYAGE ===")
    print(f"Scripts conservés: {kept_count}")
    print(f"Scripts archivés: {archived_count}")  
    print(f"Scripts supprimés: {deleted_count}")
    print(f"Total traité: {kept_count + archived_count + deleted_count}")
    
    return kept_count, archived_count, deleted_count

if __name__ == "__main__":
    analyze_and_cleanup_python_scripts()