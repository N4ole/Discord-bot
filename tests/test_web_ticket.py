"""
Test de support via interface web
"""
import requests
import time


def test_web_ticket():
    """Test de création de ticket via web"""
    print("🌐 Test création ticket via interface web")
    print("=" * 50)

    base_url = "http://127.0.0.1:8080"

    try:
        # Session
        session = requests.Session()

        # 1. Créer un compte d'abord
        print("👤 Création d'un compte utilisateur...")

        register_data = {
            'username': f'WebUser_{int(time.time())}',
            'email': f'webtest_{int(time.time())}@example.com',
            'password': 'testpass123',
            'discord_username': 'WebTestUser#1234',
            'discord_id': '987654321'
        }

        response = session.post(
            f"{base_url}/support/register", data=register_data)
        print(f"Inscription Status: {response.status_code}")

        # 2. Se connecter
        print("🔐 Connexion...")
        login_data = {
            'email': register_data['email'],
            'password': register_data['password']
        }

        response = session.post(f"{base_url}/support/login", data=login_data)
        print(f"Connexion Status: {response.status_code}")

        # 3. Créer un ticket
        print("🎫 Création d'un ticket...")
        print(f"📱 Notification sera envoyée à naole77 (ID: 702923932239527978)")

        ticket_data = {
            'category': 'bug',
            'priority': 'high',
            'subject': f'🔔 Test Final Notification {int(time.time())}',
            'description': f'Test de notification Discord pour naole77.\nCréé le {time.strftime("%Y-%m-%d %H:%M:%S")}\n\nCe ticket devrait déclencher une notification Discord vers votre compte naole77.'
        }

        # Faire la requête POST vers la création de ticket
        response = session.post(
            f"{base_url}/support/ticket/new", data=ticket_data)

        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Ticket créé - Vérifiez Discord!")
        else:
            print(f"❌ Erreur: {response.text[:300]}")

    except Exception as e:
        print(f"❌ Erreur: {e}")


if __name__ == "__main__":
    test_web_ticket()
