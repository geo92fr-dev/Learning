#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour transformer la liste "Pièges à éviter" en tuiles visuelles
"""

def transform_pieges_list():
    file_path = "College_4ieme_Maths/01_Nombres_relatifs/cours/cours_principal.html"
    
    # Lire le fichier
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern à remplacer - la liste simple
    old_list = """  <ul class='liste-pieges'>
   <li>Ne pas additionner quand les signes sont différents.</li>
   <li>Ne pas décider le signe "au hasard" : toujours le justifier.</li>
   <li>Ne pas confondre "soustraire" et "comparer les distances".</li>
   <li>Ne pas oublier le contexte : vérifier si le résultat "raconte une histoire logique".</li>
  </ul>"""
    
    # Nouveau format en tuiles
    new_cards = """  
  <div class='card'>
   <h4>⚠️ Checklist anti-pièges</h4>
   <div class='grid-auto'>
    <div class='card'>
     <h5>🚫 Signes différents</h5>
     <p><strong>Piège :</strong> Additionner directement</p>
     <p><strong>✅ Bon réflexe :</strong> Je soustrais !</p>
    </div>
    <div class='card'>
     <h5>🎲 Signe au hasard</h5>
     <p><strong>Piège :</strong> Choisir sans réfléchir</p>
     <p><strong>✅ Bon réflexe :</strong> Je justifie toujours</p>
    </div>
    <div class='card'>
     <h5>🤔 Distances vs soustraire</h5>
     <p><strong>Piège :</strong> Confondre les méthodes</p>
     <p><strong>✅ Bon réflexe :</strong> Distances à zéro d'abord</p>
    </div>
    <div class='card'>
     <h5>🌍 Contexte oublié</h5>
     <p><strong>Piège :</strong> Résultat illogique</p>
     <p><strong>✅ Bon réflexe :</strong> Je vérifie avec température/argent</p>
    </div>
   </div>
  </div>"""
    
    # Remplacer
    if old_list in content:
        content = content.replace(old_list, new_cards)
        
        # Écrire le fichier modifié
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Liste 'Pièges à éviter' transformée en tuiles visuelles !")
        return True
    else:
        print("❌ Liste 'Pièges à éviter' non trouvée ou déjà transformée")
        return False

if __name__ == "__main__":
    transform_pieges_list()