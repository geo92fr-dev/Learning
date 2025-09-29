#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script alternatif pour convertir l'exercice 2 - approche plus directe
"""

def fix_piege_exercise_2_v2():
    file_path = "College_4ieme_Maths/01_Nombres_relatifs/cours/cours_principal.html"
    
    # Lire le fichier
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Trouver et remplacer les lignes spécifiques de l'exercice 2
    in_exercise_2 = False
    exercise_2_start = False
    new_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Détecter le début de l'exercice 2
        if "(-6) + (-4) = +2" in line:
            exercise_2_start = True
            new_lines.append(line)  # Garder la ligne du calcul
            i += 1
            continue
        
        # Si on est dans l'exercice 2 et qu'on trouve la section details
        if exercise_2_start and "details><summary" in line:
            # Remplacer toute la section details par le format interactif
            new_lines.append("    <p><strong>📝 Quelle est l'erreur ? Donne le bon résultat :</strong></p>\n")
            new_lines.append("    <div class='quiz-input'>\n")
            new_lines.append("        <input type='text' class='quiz-textbox' id='piege2Answer' placeholder='Ta réponse' maxlength='4'>\n")
            new_lines.append("        <button class='quiz-btn' onclick='checkPiegeAnswer(2, \"-10\", \"Erreur : soustraction au lieu d\\'addition (même signe). Correct : 6 + 4 = 10 → -10\")'>✓ Valider</button>\n")
            new_lines.append("    </div>\n")
            new_lines.append("    <div class='feedback-zone' id='piege2Feedback'></div>\n")
            
            # Ignorer les lignes jusqu'à la fermeture du details
            while i < len(lines) and "</details>" not in lines[i]:
                i += 1
            if i < len(lines):
                i += 1  # Skip the </details> line
            exercise_2_start = False
            continue
        
        # Ajouter la ligne normale
        new_lines.append(line)
        i += 1
    
    # Écrire le fichier modifié
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print("✅ Exercice 2 converti au format interactif (version 2)!")

if __name__ == "__main__":
    fix_piege_exercise_2_v2()