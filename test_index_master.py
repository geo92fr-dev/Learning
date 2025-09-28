import os
import webbrowser
from pathlib import Path

def check_links_and_open():
    """Vérifie les liens de l'index master et ouvre la page"""
    
    base_path = Path("c:/Project_Learning_Simplified")
    index_file = base_path / "index_4ieme_master.html"
    
    print("🔍 Vérification des liens de l'index master...")
    
    # Vérifier que le fichier index existe
    if not index_file.exists():
        print("❌ Fichier index_4ieme_master.html non trouvé!")
        return False
    
    # Vérifier les dossiers de matières
    subjects = [
        "College_4ieme_Maths",
        "College_4ieme_Francais", 
        "College_4ieme_Histoire_Geo",
        "College_4ieme_Anglais",
        "College_4ieme_Espagnol", 
        "College_4ieme_Sciences_Physiques",
        "College_4ieme_SVT",
        "College_4ieme_Technologie",
        "College_4ieme_Arts_Plastiques",
        "College_4ieme_Musique",
        "College_4ieme_EPS",
        "College_4ieme_EMC"
    ]
    
    missing_folders = []
    ready_folders = []
    
    for subject in subjects:
        folder_path = base_path / subject
        if folder_path.exists():
            ready_folders.append(subject)
            print(f"✅ {subject}")
        else:
            missing_folders.append(subject)
            print(f"❌ {subject} - Dossier manquant")
    
    # Vérifier le fichier spécial des maths
    maths_index = base_path / "College_4ieme_Maths" / "index_master_4ieme.html"
    if maths_index.exists():
        print("✅ Interface Maths complète trouvée")
    else:
        print("⚠️ Interface Maths non trouvée (lien sera cassé)")
    
    # Résumé
    print(f"\n📊 Résumé:")
    print(f"✅ Dossiers prêts: {len(ready_folders)}/11")
    print(f"❌ Dossiers manquants: {len(missing_folders)}")
    
    if missing_folders:
        print("\n🔧 Dossiers à créer:")
        for folder in missing_folders:
            print(f"   - {folder}")
    
    # Ouvrir dans le navigateur
    if index_file.exists():
        print(f"\n🚀 Ouverture de l'index master...")
        file_url = f"file:///{index_file.as_posix()}"
        try:
            webbrowser.open(file_url)
            print("✅ Page ouverte dans le navigateur!")
        except Exception as e:
            print(f"❌ Erreur d'ouverture: {e}")
            print(f"🔗 URL manuelle: {file_url}")
    
    return len(missing_folders) == 0

if __name__ == "__main__":
    print("🎓 Test de l'index master - Collège 4ème")
    print("=" * 50)
    
    success = check_links_and_open()
    
    if success:
        print("\n🎉 Tous les liens sont fonctionnels!")
    else:
        print("\n⚠️ Certains liens peuvent être cassés.")
    
    print("\n📝 Note: Seules les Maths ont une interface complète.")
    print("   Les autres matières mènent aux dossiers de structure.")