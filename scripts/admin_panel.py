"""
Utilitaire d'administration pour le Panel Web
"""
import os
import sys
from werkzeug.security import generate_password_hash
import secrets


def generate_secret_key():
    """Génère une clé secrète sécurisée pour Flask"""
    return secrets.token_urlsafe(32)


def hash_password(password):
    """Hash un mot de passe"""
    return generate_password_hash(password)


def create_admin_user():
    """Crée un nouvel utilisateur admin"""
    print("🔐 Création d'un nouvel utilisateur administrateur")
    print("-" * 50)

    username = input("Nom d'utilisateur: ")
    if not username:
        print("❌ Le nom d'utilisateur ne peut pas être vide !")
        return

    password = input("Mot de passe: ")
    if len(password) < 6:
        print("❌ Le mot de passe doit contenir au moins 6 caractères !")
        return

    password_confirm = input("Confirmez le mot de passe: ")
    if password != password_confirm:
        print("❌ Les mots de passe ne correspondent pas !")
        return

    hashed = generate_password_hash(password)

    print("\n✅ Utilisateur créé avec succès !")
    print(f"Nom d'utilisateur: {username}")
    print(f"Hash du mot de passe: {hashed}")
    print("\n📝 Ajoutez cette ligne dans web_panel.py dans ADMIN_CREDENTIALS:")
    print(f"    '{username}': '{hashed}',")


def generate_flask_config():
    """Génère une configuration Flask sécurisée"""
    print("🔧 Génération de la configuration Flask")
    print("-" * 40)

    secret_key = generate_secret_key()

    config = f"""# Configuration Flask générée automatiquement
FLASK_SECRET_KEY='{secret_key}'
WEB_HOST='127.0.0.1'
WEB_PORT=8080

# Sécurité renforcée
SESSION_TIMEOUT=3600  # 1 heure
MAX_LOGIN_ATTEMPTS=5
LOCKOUT_DURATION=900  # 15 minutes

# Logs
LOG_LEVEL='INFO'
MAX_LOGS_IN_MEMORY=1000
"""

    print("✅ Configuration générée !")
    print("\n📄 Contenu à ajouter dans .env.panel:")
    print(config)

    save = input("\n💾 Sauvegarder dans .env.panel ? (o/n): ")
    if save.lower() in ['o', 'oui', 'y', 'yes']:
        with open('.env.panel', 'w', encoding='utf-8') as f:
            f.write(config)
        print("✅ Configuration sauvegardée !")


def view_stats():
    """Affiche les statistiques du panel"""
    print("📊 Statistiques du Panel Web")
    print("-" * 30)

    try:
        # Tentative de lecture des logs si disponibles
        if os.path.exists('data/panel_logs.json'):
            import json
            with open('data/panel_logs.json', 'r') as f:
                logs = json.load(f)
            print(f"📝 Logs disponibles: {len(logs)} entrées")
        else:
            print("📝 Aucun log trouvé")

        # Vérifier si le panel est accessible
        try:
            import requests
            response = requests.get('http://127.0.0.1:8080', timeout=2)
            if response.status_code == 200:
                print("🟢 Panel web accessible")
            else:
                print("🟡 Panel web répond mais avec erreur")
        except:
            print("🔴 Panel web non accessible")

    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")


def main():
    """Menu principal"""
    print("🤖 Panel Web Discord Bot - Utilitaire d'Administration")
    print("=" * 60)

    while True:
        print("\n🔧 Options disponibles:")
        print("1. 👤 Créer un utilisateur admin")
        print("2. 🔐 Générer une configuration Flask")
        print("3. 📊 Voir les statistiques")
        print("4. 🚪 Quitter")

        choice = input("\nVotre choix (1-4): ")

        if choice == '1':
            create_admin_user()
        elif choice == '2':
            generate_flask_config()
        elif choice == '3':
            view_stats()
        elif choice == '4':
            print("👋 Au revoir !")
            break
        else:
            print("❌ Choix invalide !")


if __name__ == "__main__":
    main()
