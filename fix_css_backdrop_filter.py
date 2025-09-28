#!/usr/bin/env python3
"""
Script pour corriger les problèmes de compatibilité CSS backdrop-filter
Ajoute la propriété standard 'backdrop-filter' après '-webkit-backdrop-filter'
"""

import os
import re
from pathlib import Path
from typing import List

def fix_backdrop_filter_compatibility(file_path: Path) -> bool:
    """
    Corrige la compatibilité backdrop-filter dans un fichier HTML/CSS
    Retourne True si des modifications ont été faites
    """
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Pattern pour -webkit-backdrop-filter sans backdrop-filter standard
        pattern = r'(-webkit-backdrop-filter:\s*blur\([^;]+\);)(?!\s*backdrop-filter:)'
        
        # Remplacer par la version avec les deux propriétés
        def replacement(match):
            webkit_prop = match.group(1)
            standard_prop = webkit_prop.replace('-webkit-backdrop-filter:', 'backdrop-filter:')
            return webkit_prop + standard_prop
        
        # Appliquer le remplacement
        content = re.sub(pattern, replacement, content)
        
        # Écrire le fichier seulement si modifié
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
            
    except Exception as e:
        print(f"❌ Erreur avec {file_path}: {e}")
        return False
    
    return False

def scan_and_fix_css_compatibility():
    """Scanne et corrige tous les fichiers HTML du projet"""
    
    base_path = Path("c:/Project_Learning_Simplified")
    
    print("🔧 Correction compatibilité CSS backdrop-filter")
    print("=" * 55)
    
    # Extensions de fichiers à traiter
    extensions = ['.html', '.css']
    total_files = 0
    total_fixed = 0
    
    # Parcourir tous les fichiers HTML/CSS
    for ext in extensions:
        files_found = list(base_path.rglob(f"*{ext}"))
        
        for file_path in files_found:
            # Ignorer certains dossiers
            if any(skip in str(file_path) for skip in ['.git', 'node_modules', '__pycache__']):
                continue
                
            total_files += 1
            
            if fix_backdrop_filter_compatibility(file_path):
                # Calculer le chemin relatif pour affichage
                try:
                    relative_path = file_path.relative_to(base_path)
                    print(f"✅ Corrigé: {relative_path}")
                    total_fixed += 1
                except ValueError:
                    print(f"✅ Corrigé: {file_path}")
                    total_fixed += 1
    
    print("\n" + "=" * 55)
    print("🎉 Correction terminée !")
    print(f"📊 Résumé:")
    print(f"   📄 Fichiers scannés: {total_files}")
    print(f"   🔧 Fichiers corrigés: {total_fixed}")
    
    if total_fixed > 0:
        print(f"\n✅ Améliorations apportées:")
        print(f"   • Ajout propriété standard 'backdrop-filter'")
        print(f"   • Compatibilité étendue navigateurs modernes")
        print(f"   • Suppression warnings CSS")
        print(f"   • Meilleure prise en charge Chrome 76+, Firefox 103+")
    else:
        print(f"\n✅ Tous les fichiers sont déjà conformes !")
    
    return total_fixed

def main():
    """Fonction principale"""
    
    print("🎯 CORRECTION COMPATIBILITÉ CSS")
    print("=" * 55)
    print("🔍 Problème détecté:")
    print("   • Propriété '-webkit-backdrop-filter' sans équivalent standard")
    print("   • Warning CSS dans VS Code")
    print("   • Compatibilité limitée navigateurs")
    print("\n💡 Solution:")
    print("   • Ajout 'backdrop-filter' après '-webkit-backdrop-filter'")
    print("   • Support Chrome 76+, Firefox 103+, Edge 79+")
    print("   • Suppression des avertissements")
    print("=" * 55)
    
    # Exécuter la correction
    files_fixed = scan_and_fix_css_compatibility()
    
    if files_fixed > 0:
        print(f"\n🚀 Recommandation:")
        print(f"   git add -A && git commit -m 'Fix CSS backdrop-filter compatibility'")

if __name__ == "__main__":
    main()