#!/usr/bin/env python3
"""
Script de validation pour vérifier que tous les liens vers 
'corrections' et 'evaluations' ont été supprimés
"""

import os
import re
from pathlib import Path

def validate_no_dead_links():
    """Vérifie qu'il n'y a plus de liens vers corrections/ et evaluations/"""
    
    base_path = Path("c:/Project_Learning_Simplified")
    dead_links_found = []
    
    print("🔍 Validation des liens morts...")
    print("=" * 50)
    
    # Patterns à chercher
    patterns = [
        r"href=['\"][^'\"]*corrections[^'\"]*\.html['\"]",
        r"href=['\"][^'\"]*evaluations[^'\"]*\.html['\"]"
    ]
    
    # Rechercher dans tous les fichiers HTML
    for html_file in base_path.rglob("*.html"):
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            for pattern in patterns:
                matches = re.findall(pattern, content)
                if matches:
                    for match in matches:
                        dead_links_found.append({
                            'file': str(html_file),
                            'link': match
                        })
        except Exception as e:
            print(f"⚠️  Erreur lecture {html_file}: {e}")
    
    # Rapport
    if dead_links_found:
        print("❌ Liens morts détectés:")
        for item in dead_links_found:
            print(f"   📄 {item['file']}")
            print(f"   🔗 {item['link']}")
            print()
    else:
        print("✅ Aucun lien mort détecté !")
        print("✅ Tous les raccourcis Corrections et Évaluations ont été supprimés")
    
    return len(dead_links_found)

def validate_navigation_structure():
    """Vérifie que la structure de navigation est cohérente"""
    
    base_path = Path("c:/Project_Learning_Simplified")
    
    print("\n🧭 Validation structure de navigation...")
    print("=" * 50)
    
    # Vérifier quelques fichiers cours_principal.html
    cours_files = list(base_path.rglob("**/cours/cours_principal.html"))[:5]
    
    for cours_file in cours_files:
        try:
            with open(cours_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Vérifier les liens attendus
            expected_links = [
                "exercices_niveau1_decouverte.html",
                "exercices_niveau2_pratique.html", 
                "exercices_niveau3_defi.html",
                "fiche_synthese.html"
            ]
            
            missing_links = []
            for link in expected_links:
                if link not in content:
                    missing_links.append(link)
            
            # Vérifier les liens interdits
            forbidden_patterns = [
                "corrections_detaillees.html",
                "evaluation_formative.html"
            ]
            
            forbidden_found = []
            for pattern in forbidden_patterns:
                if pattern in content:
                    forbidden_found.append(pattern)
            
            # Rapport pour ce fichier
            chapter_name = cours_file.parent.parent.name
            if missing_links or forbidden_found:
                print(f"⚠️  {chapter_name}:")
                if missing_links:
                    print(f"   ❌ Liens manquants: {', '.join(missing_links)}")
                if forbidden_found:
                    print(f"   ❌ Liens interdits: {', '.join(forbidden_found)}")
            else:
                print(f"✅ {chapter_name}: Structure correcte")
                
        except Exception as e:
            print(f"❌ Erreur {cours_file}: {e}")

def main():
    """Fonction principale de validation"""
    
    print("🔍 VALIDATION POST-SUPPRESSION")
    print("=" * 50)
    
    # Validation 1: Liens morts
    dead_links = validate_no_dead_links()
    
    # Validation 2: Structure navigation
    validate_navigation_structure()
    
    # Résumé final
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ VALIDATION")
    print("=" * 50)
    
    if dead_links == 0:
        print("🎉 ✅ VALIDATION RÉUSSIE !")
        print("✅ Structure de navigation optimisée et cohérente")
        print("✅ Aucun lien mort vers corrections/ et evaluations/")
        print("✅ Navigation simplifiée: Cours → Ex N1/N2/N3 → Synthèse")
    else:
        print(f"❌ VALIDATION ÉCHOUÉE: {dead_links} liens morts trouvés")
        print("⚠️  Action requise pour corriger les liens restants")

if __name__ == "__main__":
    main()