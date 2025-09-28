import os
import json

def create_subject_templates():
    """Crée des templates JSON pour chaque matière de 4ème"""
    
    # Configuration des matières avec leurs spécificités
    subjects_config = {
        "College_4ieme_Francais": {
            "MATIERE": "Français",
            "EMOJI": "📖",
            "COULEUR": "#8B5CF6",
            "DESCRIPTION": "Maîtrise de la langue française, littérature et expression écrite/orale"
        },
        "College_4ieme_Histoire_Geo": {
            "MATIERE": "Histoire-Géographie", 
            "EMOJI": "🌍",
            "COULEUR": "#F59E0B",
            "DESCRIPTION": "Comprendre le monde contemporain à travers l'histoire et la géographie"
        },
        "College_4ieme_Anglais": {
            "MATIERE": "Anglais",
            "EMOJI": "🇬🇧", 
            "COULEUR": "#DC2626",
            "DESCRIPTION": "Communication en anglais et découverte de la culture anglophone"
        },
        "College_4ieme_Espagnol": {
            "MATIERE": "Espagnol",
            "EMOJI": "🇪🇸",
            "COULEUR": "#EF4444", 
            "DESCRIPTION": "Communication en espagnol et découverte de la culture hispanophone"
        },
        "College_4ieme_Sciences_Physiques": {
            "MATIERE": "Sciences Physiques",
            "EMOJI": "⚛️",
            "COULEUR": "#10B981",
            "DESCRIPTION": "Physique et chimie : comprendre les phénomènes naturels et technologiques"
        },
        "College_4ieme_SVT": {
            "MATIERE": "SVT",
            "EMOJI": "🧬",
            "COULEUR": "#059669",
            "DESCRIPTION": "Sciences de la Vie et de la Terre : biologie et géologie"
        },
        "College_4ieme_Technologie": {
            "MATIERE": "Technologie", 
            "EMOJI": "🔧",
            "COULEUR": "#6366F1",
            "DESCRIPTION": "Innovation, programmation et solutions technologiques"
        },
        "College_4ieme_Arts_Plastiques": {
            "MATIERE": "Arts Plastiques",
            "EMOJI": "🎨", 
            "COULEUR": "#EC4899",
            "DESCRIPTION": "Expression artistique, créativité et culture des arts visuels"
        },
        "College_4ieme_Musique": {
            "MATIERE": "Musique",
            "EMOJI": "🎵",
            "COULEUR": "#8B5CF6",
            "DESCRIPTION": "Pratique musicale, chant et culture musicale"
        },
        "College_4ieme_EPS": {
            "MATIERE": "EPS",
            "EMOJI": "🏃",
            "COULEUR": "#F97316", 
            "DESCRIPTION": "Activités physiques et sportives pour le développement personnel"
        },
        "College_4ieme_EMC": {
            "MATIERE": "EMC",
            "EMOJI": "⚖️",
            "COULEUR": "#3B82F6",
            "DESCRIPTION": "Enseignement moral et civique : valeurs républicaines et citoyenneté"
        }
    }
    
    base_path = "c:/Project_Learning_Simplified"
    
    for folder_name, config in subjects_config.items():
        # Créer un fichier README pour chaque matière
        readme_content = f"""# {config['EMOJI']} {config['MATIERE']} - 4ème

## 📋 Description

{config['DESCRIPTION']}

## 📚 Organisation

Cette matière comprend **12 chapitres** organisés selon le programme officiel de 4ème.

Chaque chapitre contient :
- **Cours** : Leçons magistrales et explications
- **Exercices** : Applications et entraînements 
- **Corrections** : Solutions détaillées
- **Fiches résumé** : Synthèses et mémos
- **Évaluations** : Contrôles et bilans

## 🎯 Objectifs

- Acquérir les compétences du programme de 4ème
- Développer l'autonomie dans l'apprentissage
- Préparer efficacement les évaluations
- Construire une méthode de travail solide

## 🚀 Utilisation

1. **Navigation** : Choisir le chapitre souhaité
2. **Progression** : Suivre l'ordre cours → exercices → évaluation
3. **Révision** : Utiliser les fiches résumé
4. **Approfondissement** : Ressources complémentaires disponibles

---

**{config['MATIERE']} 4ème** • Programme complet • Méthode progressive
"""
        
        readme_path = os.path.join(base_path, folder_name, "README.md")
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"✅ README créé pour {config['MATIERE']}")
    
    print(f"\n🎉 Templates créés pour {len(subjects_config)} matières !")

if __name__ == "__main__":
    create_subject_templates()