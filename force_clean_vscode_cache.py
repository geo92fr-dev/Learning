#!/usr/bin/env python3
"""
NETTOYAGE CACHE VS CODE - Solution radicale
Élimine les références fantômes des extensions et diagnostics

PROBLÈME: 
Extensions (Microsoft Edge Tools) conservent des diagnostics
sur des fichiers supprimés dans leur cache interne

SOLUTION:
1. Nettoyage cache utilisateur VS Code
2. Reset des données d'extensions
3. Suppression diagnostics persistants
4. Vérification workspace settings
"""

import os
import shutil
import json
import glob
from pathlib import Path

def get_vscode_cache_paths():
    """Retourne les chemins de cache VS Code selon l'OS"""
    user_profile = os.environ.get('USERPROFILE', '')
    
    cache_paths = [
        # Cache principal VS Code
        os.path.join(user_profile, 'AppData', 'Roaming', 'Code', 'User', 'workspaceStorage'),
        os.path.join(user_profile, 'AppData', 'Roaming', 'Code', 'logs'),
        os.path.join(user_profile, 'AppData', 'Roaming', 'Code', 'CachedExtensions'),
        
        # Cache extensions
        os.path.join(user_profile, 'AppData', 'Roaming', 'Code', 'User', 'globalStorage'),
        
        # Temp VS Code
        os.path.join(user_profile, 'AppData', 'Local', 'Temp', 'vscode*'),
        
        # Cache workspace local
        '.vscode',
        os.path.join('.vscode', 'settings.json'),
    ]
    
    return [path for path in cache_paths if path]

def clean_workspace_vscode_settings():
    """Nettoie les settings workspace VS Code"""
    vscode_dir = '.vscode'
    
    if os.path.exists(vscode_dir):
        print(f"🔍 Nettoyage dossier workspace: {vscode_dir}")
        
        # Sauvegarde settings si important
        settings_file = os.path.join(vscode_dir, 'settings.json')
        if os.path.exists(settings_file):
            try:
                with open(settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                
                # Supprime les références aux diagnostics
                keys_to_remove = [
                    'problems.decorations.enabled',
                    'problems.showCurrentInStatus',
                    'html.validate.scripts', 
                    'html.validate.styles',
                    'webhint',
                    'edge-tools'
                ]
                
                for key in keys_to_remove:
                    settings.pop(key, None)
                
                # Réécrit settings nettoyés
                with open(settings_file, 'w', encoding='utf-8') as f:
                    json.dump(settings, f, indent=2, ensure_ascii=False)
                
                print(f"✅ Settings workspace nettoyés")
                
            except Exception as e:
                print(f"⚠️  Erreur settings: {e}")

def force_clean_extension_cache():
    """Nettoyage forcé du cache des extensions"""
    user_profile = os.environ.get('USERPROFILE', '')
    
    # Chemins cache extensions Microsoft Edge Tools
    edge_cache_patterns = [
        os.path.join(user_profile, 'AppData', 'Roaming', 'Code', 'User', 'globalStorage', '*edge*'),
        os.path.join(user_profile, 'AppData', 'Roaming', 'Code', 'User', 'globalStorage', '*microsoft*'),
        os.path.join(user_profile, 'AppData', 'Roaming', 'Code', 'User', 'workspaceStorage', '*', 'ms-edgedevtools*'),
    ]
    
    cleaned_count = 0
    
    for pattern in edge_cache_patterns:
        matching_paths = glob.glob(pattern)
        for path in matching_paths:
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path)
                    print(f"🗑️  Supprimé cache extension: {os.path.basename(path)}")
                    cleaned_count += 1
                elif os.path.isfile(path):
                    os.remove(path)
                    print(f"🗑️  Supprimé fichier cache: {os.path.basename(path)}")
                    cleaned_count += 1
            except Exception as e:
                print(f"⚠️  Impossible de supprimer {path}: {e}")
    
    return cleaned_count

def create_workspace_reset_script():
    """Crée un script de reset complet workspace"""
    script_content = '''@echo off
echo RESET COMPLET VS CODE - Elimination fichiers fantomes
echo.

echo Fermeture forcée VS Code...
taskkill /F /IM "Code.exe" 2>nul

echo Attente 3 secondes...
timeout /t 3 /nobreak >nul

echo Nettoyage cache extensions...
python force_clean_vscode_cache.py

echo Suppression workspace storage...
rd /S /Q "%APPDATA%\\Code\\User\\workspaceStorage" 2>nul

echo Reset diagnostics...
rd /S /Q "%APPDATA%\\Code\\logs" 2>nul

echo.
echo ✅ RESET TERMINÉ
echo Redémarrez VS Code maintenant
echo.
pause
'''
    
    with open('reset_vscode_complete.bat', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print("📝 Script reset complet créé: reset_vscode_complete.bat")

def main():
    print("🚀 NETTOYAGE CACHE VS CODE - Solution radicale")
    print("=" * 60)
    
    # 1. Nettoyage workspace settings
    clean_workspace_vscode_settings()
    
    # 2. Nettoyage cache extensions
    cleaned = force_clean_extension_cache()
    print(f"🧹 {cleaned} éléments de cache supprimés")
    
    # 3. Création script reset complet
    create_workspace_reset_script()
    
    # 4. Vérification fichier corrompu
    corrupted_file = "College_4ieme_Maths/01_Nombres_relatifs/fiches_resume/fiche_synthese_corrupted.html"
    if os.path.exists(corrupted_file):
        print(f"❌ ATTENTION: Le fichier existe encore: {corrupted_file}")
        print("   Suppression recommandée avant redémarrage VS Code")
    else:
        print(f"✅ Fichier corrompu confirmé supprimé: {corrupted_file}")
    
    print("\n" + "=" * 60)
    print("🎯 ACTIONS REQUISES POUR ÉLIMINER LES WARNINGS:")
    print("1. Fermer VS Code COMPLÈTEMENT")
    print("2. Exécuter: reset_vscode_complete.bat")  
    print("3. OU manuellement:")
    print("   - Supprimer %APPDATA%\\Code\\User\\workspaceStorage")
    print("   - Supprimer %APPDATA%\\Code\\logs")
    print("4. Redémarrer VS Code")
    print("5. Rouvrir le workspace")
    print("\n✨ Les warnings de Microsoft Edge Tools seront éliminés!")

if __name__ == "__main__":
    main()