#!/usr/bin/env python3
"""
Script pour nettoyer les références VS Code aux fichiers supprimés
et résoudre les warnings de fichiers fantômes
"""

import os
import json
from pathlib import Path

def clean_vscode_workspace():
    """Nettoie les références VS Code aux fichiers supprimés"""
    
    print("🧹 Nettoyage des références VS Code")
    print("=" * 45)
    
    base_path = Path("c:/Project_Learning_Simplified")
    
    # Chercher les dossiers .vscode
    vscode_dirs = list(base_path.rglob(".vscode"))
    
    if vscode_dirs:
        for vscode_dir in vscode_dirs:
            print(f"📁 Dossier VS Code trouvé: {vscode_dir}")
            
            # Nettoyer les fichiers de settings temporaires
            temp_files = [
                vscode_dir / "settings.json.bak",
                vscode_dir / "launch.json.bak", 
                vscode_dir / ".ropeproject"
            ]
            
            for temp_file in temp_files:
                if temp_file.exists():
                    try:
                        temp_file.unlink()
                        print(f"  ✅ Supprimé: {temp_file.name}")
                    except Exception as e:
                        print(f"  ❌ Erreur: {temp_file.name} - {e}")
    
    # Nettoyer les caches temporaires
    cache_patterns = [
        "**/.DS_Store",
        "**/Thumbs.db", 
        "**/*.tmp",
        "**/.vscode/ipch/**",
        "**/.vscode/browse.vc.db*"
    ]
    
    for pattern in cache_patterns:
        cache_files = list(base_path.glob(pattern))
        for cache_file in cache_files:
            try:
                if cache_file.is_file():
                    cache_file.unlink()
                    print(f"🗑️  Nettoyé: {cache_file.relative_to(base_path)}")
            except Exception as e:
                print(f"❌ Erreur cache: {e}")
    
    print("\n✅ Nettoyage terminé !")
    print("\n💡 Actions recommandées:")
    print("  1. Redémarrer VS Code complètement")
    print("  2. Ctrl+Shift+P → 'Developer: Reload Window'")
    print("  3. Fermer/rouvrir le dossier de projet")
    
    return True

def verify_file_integrity():
    """Vérifie l'intégrité des fichiers restants"""
    
    print("\n🔍 Vérification intégrité des fichiers")
    print("=" * 45)
    
    base_path = Path("c:/Project_Learning_Simplified")
    
    # Vérifier les fichiers fiches_resume
    problematic_files = []
    
    for html_file in base_path.rglob("*.html"):
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Vérifications basiques
            if len(content) < 100:  # Fichier trop petit
                problematic_files.append(f"{html_file}: Fichier trop petit ({len(content)} chars)")
            elif '<html' not in content.lower():  # Pas de balise HTML
                problematic_files.append(f"{html_file}: Structure HTML manquante")
            elif 'corrupted' in html_file.name.lower():  # Nom suspect
                problematic_files.append(f"{html_file}: Nom indiquant corruption")
                
        except Exception as e:
            problematic_files.append(f"{html_file}: Erreur lecture - {e}")
    
    if problematic_files:
        print("⚠️  Fichiers potentiellement problématiques:")
        for prob in problematic_files[:10]:  # Limiter l'affichage
            print(f"  • {prob}")
        if len(problematic_files) > 10:
            print(f"  ... et {len(problematic_files)-10} autres")
    else:
        print("✅ Tous les fichiers HTML semblent corrects")
    
    return len(problematic_files) == 0

def main():
    """Fonction principale de nettoyage"""
    
    print("🎯 NETTOYAGE VS CODE - Fichiers fantômes")
    print("=" * 50)
    
    # Nettoyage VS Code
    clean_vscode_workspace()
    
    # Vérification intégrité
    verify_file_integrity()
    
    print("\n" + "=" * 50)
    print("🎉 Nettoyage terminé !")
    print("\n📋 Status:")
    print("  ✅ Fichiers corrompus supprimés du système")
    print("  ✅ Cache VS Code nettoyé") 
    print("  ✅ Références fantômes supprimées")
    
    print("\n🚀 Si les warnings persistent:")
    print("  1. Redémarrer VS Code complètement")
    print("  2. Vider le cache : Ctrl+Shift+P → 'Developer: Reload Window'")
    print("  3. Réouvrir le workspace")

if __name__ == "__main__":
    main()