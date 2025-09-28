#!/usr/bin/env python3
"""
Script de mise à jour des fonctionnalités Google Calendar
Migre vers la version améliorée avec boutons individuels
"""

import os
import re
from pathlib import Path

def update_calendar_to_individual_buttons(file_path: Path, chapter_title: str, chapter_slug: str):
    """
    Met à jour un cours vers la version avec boutons individuels
    """
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. Ajouter les nouveaux styles CSS
        if '.btn-calendar-mini' not in content:
            # Ajouter après les styles existants
            new_styles = """.btn-calendar-mini{background:#059669;padding:0.3rem 0.5rem;font-size:0.7rem;color:#fff;border:none;border-radius:4px;cursor:pointer;display:inline-block;flex-shrink:0;}
.btn-calendar-mini:hover{background:#047857;}
.reactivation-item{margin:0.5rem 0;display:flex;align-items:center;gap:0.5rem;}
.calendar-tip{margin-top:1rem;text-align:center;font-size:0.75rem;opacity:0.8;}"""
            
            content = re.sub(
                r'(\.calendar-info\{[^}]+\})',
                r'\1' + new_styles,
                content
            )
        
        # 2. Remplacer l'ancienne section calendar-section par les nouveaux boutons individuels
        if 'calendar-section' in content and 'reactivation-item' not in content:
            old_calendar_section = r"<div class='notice calendar-section'>[^<]*<p><strong>📅 Ajouter à ton agenda :</strong></p>[^<]*<button[^>]*id='addToCalendar'[^>]*>[^<]*📅 Ajouter au Google Calendar[^<]*</button>[^<]*<p class='calendar-info'>[^<]*✨ Crée automatiquement 4 rappels de révision dans ton agenda ![^<]*</p>[^<]*</div>"
            
            new_tip = """<div class='notice calendar-tip'>
  💡 Clique sur 📅 pour ajouter chaque rappel individuellement à ton Google Calendar
 </div>"""
            
            content = re.sub(old_calendar_section, new_tip, content, flags=re.DOTALL)
        
        # 3. Remplacer la liste ul par des div avec boutons
        if '<ul>' in content and 'reactivation-item' not in content:
            # Pattern pour la liste ul complète
            ul_pattern = r'<ul>\s*<li><strong>J\+1</strong>[^<]*<span id=[\'"]dateJ1[\'"][^<]*</span>\)[^<]*<a[^>]*>[^<]+</a></li>\s*<li><strong>J\+3</strong>[^<]*<span id=[\'"]dateJ3[\'"][^<]*</span>\)[^<]*<a[^>]*>[^<]+</a></li>\s*<li><strong>J\+7</strong>[^<]*<span id=[\'"]dateJ7[\'"][^<]*</span>\)[^<]*<a[^>]*>[^<]+</a></li>\s*<li><strong>J\+14</strong>[^<]*<span id=[\'"]dateJ14[\'"][^<]*</span>\)[^<]*<a[^>]*>[^<]+</a></li>\s*</ul>'
            
            new_reactivation = """<div class='reactivation-item'>
  <button class='btn-calendar-mini' data-interval='1' data-type='decouverte'>📅</button>
  <span><strong>J+1</strong> (<span id='dateJ1'></span>) : <a href='../exercices/exercices_niveau1_decouverte.html'>2 ex. N1 découverte</a></span>
 </div>
 <div class='reactivation-item'>
  <button class='btn-calendar-mini' data-interval='3' data-type='pratique'>📅</button>
  <span><strong>J+3</strong> (<span id='dateJ3'></span>) : <a href='../exercices/exercices_niveau2_pratique.html'>2 ex. N2 pratique</a></span>
 </div>
 <div class='reactivation-item'>
  <button class='btn-calendar-mini' data-interval='7' data-type='synthese'>📅</button>
  <span><strong>J+7</strong> (<span id='dateJ7'></span>) : <a href='../fiches_resume/fiche_synthese.html'>mini quiz synthèse</a></span>
 </div>
 <div class='reactivation-item'>
  <button class='btn-calendar-mini' data-interval='14' data-type='defi'>📅</button>
  <span><strong>J+14</strong> (<span id='dateJ14'></span>) : <a href='../exercices/exercices_niveau3_defi.html'>défi mélange N3</a></span>
 </div>
 <div class='notice calendar-tip'>
  💡 Clique sur 📅 pour ajouter chaque rappel individuellement à ton Google Calendar
 </div>"""
            
            content = re.sub(ul_pattern, new_reactivation, content, flags=re.DOTALL)
        
        # 4. Remplacer le JavaScript pour les boutons individuels
        if 'addAllToGoogleCalendar' in content and 'addSingleEventToCalendar' not in content:
            # Remplacer la fonction addAllToGoogleCalendar par addSingleEventToCalendar
            old_js_pattern = r"// Fonction pour ajouter tous les événements au Google Calendar.*?alert\('🎉 4 rappels de révision ajoutés à ton Google Calendar[^']*'\);\s*}"
            
            new_js = f'''// Fonction pour ajouter un événement individuel au Google Calendar
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
   url: '/College_4ieme_Maths/{chapter_slug}/exercices/exercices_niveau1_decouverte.html',
   description: 'Révision programmée : 2 exercices niveau 1 (découverte).\\n\\n💡 Objectif : Réactiver les notions de base avec des exercices guidés.'
  }},
  pratique: {{
   icon: '📖',
   title: 'Exercices Pratique',
   url: '/College_4ieme_Maths/{chapter_slug}/exercices/exercices_niveau2_pratique.html',
   description: 'Révision programmée : 2 exercices niveau 2 (pratique).\\n\\n💡 Objectif : Application directe des règles apprises.'
  }},
  synthese: {{
   icon: '🧠',
   title: 'Quiz Synthèse',
   url: '/College_4ieme_Maths/{chapter_slug}/fiches_resume/fiche_synthese.html',
   description: 'Révision programmée : Mini quiz de synthèse.\\n\\n💡 Objectif : Vérifier la mémorisation des règles essentielles.'
  }},
  defi: {{
   icon: '🏆',
   title: 'Défi Niveau 3',
   url: '/College_4ieme_Maths/{chapter_slug}/exercices/exercices_niveau3_defi.html',
   description: 'Révision programmée : Exercices défi et approfondissement.\\n\\n💡 Objectif : Consolider avec des problèmes complexes et créatifs.'
  }}
 }};
 
 const config = eventConfig[type];
 const title = `${{config.icon}} Révision ${{chapterTitle}} - ${{config.title}}`;
 const description = `${{config.description}}\\n\\nLien direct : ${{window.location.origin}}${{config.url}}`;
 
 const calendarUrl = createGoogleCalendarLink(eventDate, title, description);
 window.open(calendarUrl, '_blank');
 
 // Feedback discret
 const dayName = eventDate.toLocaleDateString('fr-FR', {{ weekday: 'long', day: 'numeric', month: 'long' }});
 alert(`📅 Rappel "${{config.title}}" ajouté pour le ${{dayName}} !\\n\\nVérifie le nouvel onglet pour confirmer l'événement.`);
}}'''
            
            content = re.sub(old_js_pattern, new_js, content, flags=re.DOTALL)
        
        # 5. Remplacer l'event listener
        if 'getElementById(\'addToCalendar\')' in content:
            old_listener = r"// Ajouter l'événement au bouton Google Calendar\s*const calendarBtn = document\.getElementById\('addToCalendar'\);\s*if \(calendarBtn\) \{\s*calendarBtn\.addEventListener\('click', addAllToGoogleCalendar\);\s*\}"
            
            new_listener = """// Ajouter les événements aux boutons calendrier individuels
 const calendarBtns = document.querySelectorAll('.btn-calendar-mini');
 calendarBtns.forEach(btn => {
  btn.addEventListener('click', function() {
   const interval = parseInt(this.getAttribute('data-interval'));
   const type = this.getAttribute('data-type');
   addSingleEventToCalendar(interval, type);
  });
 });"""
            
            content = re.sub(old_listener, new_listener, content, flags=re.DOTALL)
        
        # Sauvegarder seulement si des modifications ont été apportées
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"Erreur lors du traitement de {file_path}: {e}")
        return False

def update_all_math_chapters():
    """
    Met à jour tous les chapitres de maths vers la nouvelle version
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
            print(f"Mise à jour : {chapter_title}")
            if update_calendar_to_individual_buttons(cours_file, chapter_title, chapter_slug):
                print(f"  ✅ Migré vers boutons individuels")
                updated_count += 1
            else:
                print(f"  ℹ️ Déjà à jour")
        else:
            print(f"  ❌ Fichier manquant : {cours_file}")
    
    print(f"\n📊 Résumé : {updated_count} fichiers mis à jour sur {len(chapters)} chapitres")

if __name__ == "__main__":
    update_all_math_chapters()