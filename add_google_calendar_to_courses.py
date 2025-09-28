#!/usr/bin/env python3
"""
Script pour ajouter la fonctionnalité Google Calendar à tous les cours
Ajoute le bouton et les scripts JavaScript pour le plan de réactivation
"""

import os
import re
from pathlib import Path

def add_google_calendar_feature(file_path: Path, chapter_title: str, chapter_slug: str):
    """
    Ajoute la fonctionnalité Google Calendar à un fichier cours_principal.html
    """
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. Ajouter les styles CSS si pas déjà présents
        css_styles = """
.calendar-section{text-align:center;margin-top:1rem;}
.btn-calendar{background:#059669;padding:0.6rem 1rem;font-size:0.8rem;margin:0.5rem;color:#fff;border:none;border-radius:6px;cursor:pointer;}
.btn-calendar:hover{background:#047857;}
.calendar-info{font-size:0.7rem;opacity:0.8;margin-top:0.5rem;}"""
        
        if '.calendar-section' not in content:
            # Ajouter après les autres styles toggle
            content = re.sub(
                r'(\.toggle:hover\{[^}]+\})',
                r'\1' + css_styles,
                content
            )
        
        # 2. Ajouter le bouton Google Calendar si section réactivation existe
        if 'Plan de réactivation' in content and 'addToCalendar' not in content:
            # Remplacer la notice existante par la nouvelle version avec bouton
            notice_pattern = r'<p class=[\'"]notice[\'"][^>]*><strong>Astuce :</strong>[^<]+</p>'
            calendar_button = '''<div class='notice calendar-section'>
  <p><strong>📅 Ajouter à ton agenda :</strong></p>
  <button id='addToCalendar' class='btn-calendar'>
   📅 Ajouter au Google Calendar
  </button>
  <p class='calendar-info'>
   ✨ Crée automatiquement 4 rappels de révision dans ton agenda !
  </p>
 </div>'''
            
            content = re.sub(notice_pattern, calendar_button, content)
        
        # 3. Ajouter le JavaScript Google Calendar si pas déjà présent
        if 'createGoogleCalendarLink' not in content:
            js_code = f'''
// Fonction pour créer un lien Google Calendar
function createGoogleCalendarLink(date, title, description, duration = 30) {{
 const startDate = new Date(date);
 // Programmer à 18h00 par défaut (heure de révision)
 startDate.setHours(18, 0, 0, 0);
 
 const endDate = new Date(startDate);
 endDate.setMinutes(startDate.getMinutes() + duration);
 
 // Formatage des dates pour Google Calendar (format UTC)
 const formatDate = (d) => d.toISOString().replace(/[-:]/g, '').split('.')[0] + 'Z';
 
 const params = new URLSearchParams({{
  action: 'TEMPLATE',
  text: title,
  dates: formatDate(startDate) + '/' + formatDate(endDate),
  details: description,
  location: 'Révisions Maths - {chapter_title}'
 }});
 
 return 'https://calendar.google.com/calendar/render?' + params.toString();
}}

// Fonction pour ajouter tous les événements au Google Calendar
function addAllToGoogleCalendar() {{
 const today = new Date();
 const chapterTitle = "{chapter_title}";
 
 const events = [
  {{
   interval: 1,
   title: `📚 Révision ${{chapterTitle}} - Exercices Découverte`,
   description: `Révision programmée : 2 exercices niveau 1 (découverte).\\n\\nLien direct : ${{window.location.origin}}/College_4ieme_Maths/{chapter_slug}/exercices/exercices_niveau1_decouverte.html\\n\\n💡 Objectif : Réactiver les notions de base avec des exercices guidés.`
  }},
  {{
   interval: 3,
   title: `📖 Révision ${{chapterTitle}} - Exercices Pratique`,
   description: `Révision programmée : 2 exercices niveau 2 (pratique).\\n\\nLien direct : ${{window.location.origin}}/College_4ieme_Maths/{chapter_slug}/exercices/exercices_niveau2_pratique.html\\n\\n💡 Objectif : Application directe des règles apprises.`
  }},
  {{
   interval: 7,
   title: `🧠 Révision ${{chapterTitle}} - Quiz Synthèse`,
   description: `Révision programmée : Mini quiz de synthèse.\\n\\nLien direct : ${{window.location.origin}}/College_4ieme_Maths/{chapter_slug}/fiches_resume/fiche_synthese.html\\n\\n💡 Objectif : Vérifier la mémorisation des règles essentielles.`
  }},
  {{
   interval: 14,
   title: `🏆 Révision ${{chapterTitle}} - Défi Niveau 3`,
   description: `Révision programmée : Exercices défi et approfondissement.\\n\\nLien direct : ${{window.location.origin}}/College_4ieme_Maths/{chapter_slug}/exercices/exercices_niveau3_defi.html\\n\\n💡 Objectif : Consolider avec des problèmes complexes et créatifs.`
  }}
 ];
 
 // Ouvrir chaque événement dans un nouvel onglet
 events.forEach(event => {{
  const eventDate = new Date(today);
  eventDate.setDate(today.getDate() + event.interval);
  
  const calendarUrl = createGoogleCalendarLink(eventDate, event.title, event.description);
  window.open(calendarUrl, '_blank');
 }});
 
 // Feedback utilisateur
 alert('🎉 4 rappels de révision ajoutés à ton Google Calendar !\\n\\nVérifie tes nouveaux onglets pour confirmer chaque événement.');
}}'''
            
            # Ajouter le JavaScript avant la dernière fonction DOMContentLoaded
            content = re.sub(
                r'(// Initialiser au chargement de la page\s*document\.addEventListener\([^}]+\}\);)',
                js_code + '\n\n// Initialiser au chargement de la page\ndocument.addEventListener(\'DOMContentLoaded\', function() {\n initRevisionDates();\n \n // Ajouter l\'événement au bouton Google Calendar\n const calendarBtn = document.getElementById(\'addToCalendar\');\n if (calendarBtn) {\n  calendarBtn.addEventListener(\'click\', addAllToGoogleCalendar);\n }\n});',
                content
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

def process_all_math_chapters():
    """
    Traite tous les chapitres de maths pour ajouter la fonctionnalité Google Calendar
    """
    
    base_dir = Path("c:/Project_Learning_Simplified/College_4ieme_Maths")
    
    # Liste des chapitres avec leurs titres
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
    
    processed_count = 0
    
    for chapter_slug, chapter_title in chapters:
        cours_file = base_dir / chapter_slug / "cours" / "cours_principal.html"
        
        if cours_file.exists():
            print(f"Traitement : {chapter_title}")
            if add_google_calendar_feature(cours_file, chapter_title, chapter_slug):
                print(f"  ✅ Fonctionnalité Google Calendar ajoutée")
                processed_count += 1
            else:
                print(f"  ℹ️ Aucune modification nécessaire")
        else:
            print(f"  ❌ Fichier manquant : {cours_file}")
    
    print(f"\n📊 Résumé : {processed_count} fichiers modifiés sur {len(chapters)} chapitres")

if __name__ == "__main__":
    process_all_math_chapters()