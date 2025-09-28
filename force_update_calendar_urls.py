#!/usr/bin/env python3
"""
Script de force-mise à jour pour les URLs Google Calendar
Force l'ajout du JavaScript complet avec les bonnes URLs GitHub Pages
"""

import os
import re
from pathlib import Path

def force_update_calendar_js(file_path: Path, chapter_title: str, chapter_slug: str):
    """
    Force la mise à jour complète du JavaScript Google Calendar
    """
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Supprimer l'ancien JavaScript si présent
        if 'addSingleEventToCalendar' in content:
            # Supprimer tout le JS entre les balises script
            content = re.sub(
                r'<script>.*?</script>',
                '',
                content,
                flags=re.DOTALL
            )
        
        # Ajouter le nouveau JavaScript complet avant </body>
        base_url = f'https://geo92fr-dev.github.io/Learning/College_4ieme_Maths/{chapter_slug}'
        
        new_js = f'''<script>
// Calcul dynamique des dates de réactivation
function initRevisionDates() {{
 const today = new Date();
 const options = {{ 
  weekday: 'long', 
  day: 'numeric', 
  month: 'long', 
  year: 'numeric' 
 }};
 
 // Date du jour
 document.getElementById('dateToday').textContent = today.toLocaleDateString('fr-FR', options);
 
 // Calcul des dates J+1, J+3, J+7, J+14
 const intervals = [1, 3, 7, 14];
 const dateIds = ['dateJ1', 'dateJ3', 'dateJ7', 'dateJ14'];
 
 intervals.forEach((interval, index) => {{
  const futureDate = new Date(today);
  futureDate.setDate(today.getDate() + interval);
  
  const dateStr = futureDate.toLocaleDateString('fr-FR', {{ 
   weekday: 'short', 
   day: 'numeric', 
   month: 'short' 
  }});
  
  document.getElementById(dateIds[index]).textContent = dateStr;
 }});
}}

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

// Fonction pour ajouter un événement individuel au Google Calendar
function addSingleEventToCalendar(interval, type) {{
 const today = new Date();
 const eventDate = new Date(today);
 eventDate.setDate(today.getDate() + interval);
 
 const chapterTitle = "{chapter_title}";
 
 // Configuration selon le type d'événement
 const eventConfig = {{
  decouverte: {{
   icon: '📚',
   title: 'Exercices Découverte',
   url: '{base_url}/exercices/exercices_niveau1_decouverte.html',
   description: 'Révision programmée : 2 exercices niveau 1 (découverte).\\n\\n💡 Objectif : Réactiver les notions de base avec des exercices guidés.'
  }},
  pratique: {{
   icon: '📖',
   title: 'Exercices Pratique',
   url: '{base_url}/exercices/exercices_niveau2_pratique.html',
   description: 'Révision programmée : 2 exercices niveau 2 (pratique).\\n\\n💡 Objectif : Application directe des règles apprises.'
  }},
  synthese: {{
   icon: '🧠',
   title: 'Quiz Synthèse',
   url: '{base_url}/fiches_resume/fiche_synthese.html',
   description: 'Révision programmée : Mini quiz de synthèse.\\n\\n💡 Objectif : Vérifier la mémorisation des règles essentielles.'
  }},
  defi: {{
   icon: '🏆',
   title: 'Défi Niveau 3',
   url: '{base_url}/exercices/exercices_niveau3_defi.html',
   description: 'Révision programmée : Exercices défi et approfondissement.\\n\\n💡 Objectif : Consolider avec des problèmes complexes et créatifs.'
  }}
 }};
 
 const config = eventConfig[type];
 const title = `${{config.icon}} Révision ${{chapterTitle}} - ${{config.title}}`;
 const description = `${{config.description}}\\n\\nLien direct : ${{config.url}}`;
 
 const calendarUrl = createGoogleCalendarLink(eventDate, title, description);
 window.open(calendarUrl, '_blank');
 
 // Feedback discret
 const dayName = eventDate.toLocaleDateString('fr-FR', {{ weekday: 'long', day: 'numeric', month: 'long' }});
 alert(`📅 Rappel "${{config.title}}" ajouté pour le ${{dayName}} !\\n\\nVérifie le nouvel onglet pour confirmer l'événement.`);
}}

// Initialiser au chargement de la page
document.addEventListener('DOMContentLoaded', function() {{
 initRevisionDates();
 
 // Ajouter les événements aux boutons calendrier individuels
 const calendarBtns = document.querySelectorAll('.btn-calendar-mini');
 calendarBtns.forEach(btn => {{
  btn.addEventListener('click', function() {{
   const interval = parseInt(this.getAttribute('data-interval'));
   const type = this.getAttribute('data-type');
   addSingleEventToCalendar(interval, type);
  }});
 }});
}});
</script>'''
        
        # Insérer avant </body>
        content = content.replace('</body>', new_js + '\n</body>')
        
        # Sauvegarder
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
        
    except Exception as e:
        print(f"Erreur lors du traitement de {file_path}: {e}")
        return False

def force_update_all_chapters():
    """
    Force la mise à jour de tous les chapitres
    """
    
    base_dir = Path("c:/Project_Learning_Simplified/College_4ieme_Maths")
    
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
    
    updated_count = 0
    
    for chapter_slug, chapter_title in chapters:
        cours_file = base_dir / chapter_slug / "cours" / "cours_principal.html"
        
        if cours_file.exists():
            print(f"Force-update : {chapter_title}")
            if force_update_calendar_js(cours_file, chapter_title, chapter_slug):
                print(f"  ✅ JavaScript Google Calendar mis à jour avec URLs correctes")
                updated_count += 1
            else:
                print(f"  ❌ Erreur lors de la mise à jour")
        else:
            print(f"  ❌ Fichier manquant : {cours_file}")
    
    print(f"\n📊 Résumé : {updated_count} fichiers mis à jour sur {len(chapters)} chapitres")

if __name__ == "__main__":
    force_update_all_chapters()