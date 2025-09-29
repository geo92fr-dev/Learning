#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour convertir l'exercice 2 des pièges à éviter au format interactif
"""

import re

def fix_piege_exercise_2():
    file_path = "College_4ieme_Maths/01_Nombres_relatifs/cours/cours_principal.html"
    
    # Lire le fichier
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern pour l'exercice 2 avec "Voir la correction"
    old_pattern = r'''(<div class='card'>
    <h4>🕵️ Exercice : Trouve l'erreur</h4>
    <p><strong>Calcul :</strong> \(-6\) \+ \(-4\) = \+2</p>
    <details><summary class='summary-mini'>Voir la correction</summary>
     <p><strong>❌ Erreur :</strong> Soustraction au lieu d'addition \(même signe\)\.</p>
     <p><strong>✅ Correct :</strong> 6 \+ 4 = 10 → <strong>-10</strong></p>
    </details>
   </div>)'''
    
    # Nouveau format interactif
    new_format = '''   <div class='card'>
    <h4>🕵️ Exercice : Trouve l'erreur</h4>
    <p><strong>Calcul :</strong> (-6) + (-4) = +2</p>
    <p><strong>📝 Quelle est l'erreur ? Donne le bon résultat :</strong></p>
    <div class='quiz-input'>
        <input type='text' class='quiz-textbox' id='piege2Answer' placeholder='Ta réponse' maxlength='4'>
        <button class='quiz-btn' onclick='checkPiegeAnswer(2, "-10", "Erreur : soustraction au lieu d\\'addition (même signe). Correct : 6 + 4 = 10 → -10")'>✓ Valider</button>
    </div>
    <div class='feedback-zone' id='piege2Feedback'></div>
   </div>'''
    
    # Recherche et remplacement plus simple
    # Chercher spécifiquement le pattern de l'exercice 2
    exercise_2_pattern = r'''<div class='card'>
    <h4>🕵️ Exercice : Trouve l'erreur</h4>
    <p><strong>Calcul :</strong> \(-6\) \+ \(-4\) = \+2</p>
    <details><summary class='summary-mini'>Voir la correction</summary>
     <p><strong>❌ Erreur :</strong> Soustraction au lieu d'addition \(même signe\)\.</p>
     <p><strong>✅ Correct :</strong> 6 \+ 4 = 10 → <strong>-10</strong></p>
    </details>
   </div>'''
    
    if "Voir la correction" in content and "(-6) + (-4) = +2" in content:
        # Utiliser une approche plus simple avec des strings literals
        old_text = """    <details><summary class='summary-mini'>Voir la correction</summary>
     <p><strong>❌ Erreur :</strong> Soustraction au lieu d'addition (même signe).</p>
     <p><strong>✅ Correct :</strong> 6 + 4 = 10 → <strong>-10</strong></p>
    </details>"""
        
        new_text = """    <p><strong>📝 Quelle est l'erreur ? Donne le bon résultat :</strong></p>
    <div class='quiz-input'>
        <input type='text' class='quiz-textbox' id='piege2Answer' placeholder='Ta réponse' maxlength='4'>
        <button class='quiz-btn' onclick='checkPiegeAnswer(2, "-10", "Erreur : soustraction au lieu d\\'addition (même signe). Correct : 6 + 4 = 10 → -10")'>✓ Valider</button>
    </div>
    <div class='feedback-zone' id='piege2Feedback'></div>"""
        
        content = content.replace(old_text, new_text)
        
        # Écrire le fichier modifié
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Exercice 2 converti au format interactif avec succès!")
        return True
    else:
        print("❌ Pattern de l'exercice 2 non trouvé ou déjà converti")
        return False

if __name__ == "__main__":
    fix_piege_exercise_2()