import os

# Définition des matières et leurs chapitres
matieres = {
    "College_4ieme_Francais": [
        "01_Dire_amour",
        "02_Regarder_monde_agir",
        "03_Individu_societe",
        "04_Questionnement_complement",
        "05_Grammaire_phrase",
        "06_Grammaire_texte",
        "07_Orthographe",
        "08_Lexique",
        "09_Expression_ecrite",
        "10_Expression_orale",
        "11_Lecture_cursive",
        "12_Brevet_blanc"
    ],
    
    "College_4ieme_Histoire_Geo": [
        "01_Europe_XVIII_siecle",
        "02_Revolution_Empire",
        "03_Societes_XIXe_siecle",
        "04_Conquetes_societes_coloniales",
        "05_Espaces_productifs_francais",
        "06_Espaces_faible_densite",
        "07_Espaces_forte_densite",
        "08_Adaptation_territoire_francais",
        "09_Monde_urbanise",
        "10_Mobilites_humaines",
        "11_Migrations_internationales",
        "12_Tourisme_loisirs"
    ],
    
    "College_4ieme_Anglais": [
        "01_Meeting_people",
        "02_School_life",
        "03_Hobbies_free_time",
        "04_Family_friends",
        "05_Food_cooking",
        "06_Shopping_money",
        "07_Travel_holidays",
        "08_Technology_media",
        "09_Environment_nature",
        "10_Jobs_future",
        "11_Culture_traditions",
        "12_Final_projects"
    ],
    
    "College_4ieme_Espagnol": [
        "01_Presentarse_familia",
        "02_Vida_cotidiana",
        "03_Colegio_estudios",
        "04_Tiempo_libre",
        "05_Alimentacion_salud",
        "06_Viajes_turismo",
        "07_Medio_ambiente",
        "08_Tecnologia_comunicacion",
        "09_Cultura_hispana",
        "10_Historia_tradiciones",
        "11_Futuro_proyectos",
        "12_Repaso_general"
    ],
    
    "College_4ieme_Sciences_Physiques": [
        "01_Signaux_vision",
        "02_Signaux_son",
        "03_Air_respiration",
        "04_Transformation_chimique",
        "05_Mouvement_vitesse",
        "06_Forces_equilibre",
        "07_Energie_convertisseurs",
        "08_Electricite_circuits",
        "09_Atomes_molecules",
        "10_Combustions",
        "11_Piles_energie",
        "12_Projet_experimental"
    ],
    
    "College_4ieme_SVT": [
        "01_Nutrition_digestion",
        "02_Respiration_circulation",
        "03_Excretion_elimination",
        "04_Activite_nerveuse",
        "05_Reproduction_humaine",
        "06_Heredite_variation",
        "07_Evolution_especes",
        "08_Ecosystemes_biodiversite",
        "09_Geologie_seismes",
        "10_Volcans_risques",
        "11_Meteorologie_climat",
        "12_Projets_scientifiques"
    ],
    
    "College_4ieme_Technologie": [
        "01_Analyse_objet_technique",
        "02_Materiaux_proprietes",
        "03_Energie_sources",
        "04_Information_signal",
        "05_Programmation_algorithme",
        "06_Automatisme_capteurs",
        "07_Reseaux_communication",
        "08_Design_innovation",
        "09_Modelisation_simulation",
        "10_Fabrication_prototype",
        "11_Impact_environnemental",
        "12_Projet_final"
    ],
    
    "College_4ieme_Arts_Plastiques": [
        "01_Dessin_observation",
        "02_Couleur_peinture",
        "03_Volume_sculpture",
        "04_Image_numerique",
        "05_Architecture_espace",
        "06_Art_histoire",
        "07_Expression_gestuelle",
        "08_Collage_assemblage",
        "09_Photographie_cadrage",
        "10_Installation_performance",
        "11_Art_contemporain",
        "12_Exposition_projets"
    ],
    
    "College_4ieme_Musique": [
        "01_Voix_chant",
        "02_Rythme_pulsation",
        "03_Melodie_harmonie",
        "04_Instruments_orchestre",
        "05_Musique_baroque",
        "06_Musique_classique",
        "07_Musique_romantique",
        "08_Jazz_blues",
        "09_Musique_actuelles",
        "10_Musique_monde",
        "11_Creation_composition",
        "12_Concert_spectacle"
    ],
    
    "College_4ieme_EPS": [
        "01_Athletisme_course",
        "02_Athletisme_saut_lancer",
        "03_Natation_techniques",
        "04_Gymnastique_acrosport",
        "05_Sports_collectifs_1",
        "06_Sports_collectifs_2",
        "07_Sports_raquettes",
        "08_Combat_opposition",
        "09_Activites_pleine_nature",
        "10_Danse_expression",
        "11_Musculation_fitness",
        "12_Evaluation_bilan"
    ],
    
    "College_4ieme_EMC": [
        "01_Liberte_droits",
        "02_Egalite_discrimination",
        "03_Fraternite_solidarite",
        "04_Laicite_vivre_ensemble",
        "05_Justice_lois",
        "06_Citoyennete_participation",
        "07_Medias_information",
        "08_Developpement_durable",
        "09_Europe_citoyennete",
        "10_Discrimination_harcelement",
        "11_Engagement_responsabilite",
        "12_Debat_argumentation"
    ]
}

# Sous-dossiers standard pour chaque chapitre
sous_dossiers = ["cours", "exercices", "corrections", "fiches_resume", "evaluations"]

base_path = "c:/Project_Learning_Simplified"

def create_structure():
    for matiere, chapitres in matieres.items():
        matiere_path = os.path.join(base_path, matiere)
        
        # Créer les dossiers de chapitres
        for chapitre in chapitres:
            chapitre_path = os.path.join(matiere_path, chapitre)
            
            # Créer le dossier du chapitre
            os.makedirs(chapitre_path, exist_ok=True)
            
            # Créer les sous-dossiers
            for sous_dossier in sous_dossiers:
                sous_path = os.path.join(chapitre_path, sous_dossier)
                os.makedirs(sous_path, exist_ok=True)
        
        print(f"✅ Structure créée pour {matiere}: {len(chapitres)} chapitres")

if __name__ == "__main__":
    create_structure()
    print("\n🎉 Toutes les structures de matières créées avec succès !")