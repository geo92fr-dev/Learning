import json
import sys

def inject_master_template(json_file, template_file, output_file):
    """Injecte les données JSON dans le template master simplifié"""
    
    # Lire les données JSON
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Lire le template HTML
    with open(template_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Remplacer les variables globales
    html_content = html_content.replace('[MATIERE]', data['MATIERE'])
    html_content = html_content.replace('[NIVEAU]', data['NIVEAU'])
    html_content = html_content.replace('[ELEVE_TYPE]', data['ELEVE_TYPE'])
    html_content = html_content.replace('[ANNEE]', data['ANNEE'])
    
    # Générer le contenu des chapitres
    chapters_content = ""
    for chapitre in data['CHAPITRES']:
        # Déterminer la classe de difficulté
        difficulty_class = f"difficulty-{chapitre['CHAPITRE_DIFFICULTE']}"
        
        # Générer les objectifs
        objectifs_html = ""
        if 'CHAPITRE_OBJECTIFS' in chapitre:
            objectifs_html = "<ul>"
            for objectif in chapitre['CHAPITRE_OBJECTIFS']:
                objectifs_html += f"<li>{objectif}</li>"
            objectifs_html += "</ul>"
        
        # Générer la carte du chapitre
        chapter_card = f'''
      <div class="chapter-card">
        <div class="chapter-header">
          <div class="chapter-number">{chapitre['CHAPITRE_NUM']}</div>
          <h3 class="chapter-title">{chapitre['CHAPITRE_TITRE']}</h3>
        </div>
        
        <div class="chapter-meta">
          <span class="tag {difficulty_class}">{chapitre['CHAPITRE_DIFFICULTE_TEXT']}</span>
          <span class="tag">{chapitre['CHAPITRE_TYPE']}</span>
        </div>
        
        <div class="chapter-desc">{chapitre['CHAPITRE_DESCRIPTION']}</div>
        
        <div class="chapter-objectives">
          <strong>Objectifs :</strong>
          {objectifs_html}
        </div>
        
        <div class="chapter-actions">
          <a href="{chapitre['CHAPITRE_LIEN_COURS']}" class="btn btn-primary" {chapitre.get('CHAPITRE_COURS_DISABLED', '')}>📖 Cours</a>
          <a href="{chapitre['CHAPITRE_LIEN_EXERCICES']}" class="btn btn-secondary" {chapitre.get('CHAPITRE_EXERCICES_DISABLED', '')}>✏️ Exercices</a>
          <a href="{chapitre['CHAPITRE_LIEN_FICHE']}" class="btn btn-secondary" {chapitre.get('CHAPITRE_FICHE_DISABLED', '')}>📋 Fiche</a>
        </div>
      </div>'''
        
        chapters_content += chapter_card
    
    # Remplacer le placeholder des chapitres
    html_content = html_content.replace('[CHAPITRES_CONTENT]', chapters_content)
    
    # Écrire le fichier de sortie
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Index master simplifié généré: {output_file}")
    print(f"📊 {len(data['CHAPITRES'])} chapitres traités")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python inject_master_simple.py <json_file> <template_file> <output_file>")
        sys.exit(1)
    
    inject_master_template(sys.argv[1], sys.argv[2], sys.argv[3])