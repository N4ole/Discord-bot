"""
Test des notifications Discord pour le système de support
"""
from support_db import SupportDB
import sys
import os

# Ajouter le dossier racine au chemin
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def test_notification_system():
    """Test de création de ticket avec notification"""
    print("🧪 Test du système de notifications Discord")
    print("=" * 60)

    try:
        # Initialiser la base de données
        db = SupportDB()
        print("✅ Base de données initialisée")

        # Vérifier si l'utilisateur de test existe déjà
        existing_user = db.get_user_by_email("test@notification.com")

        if existing_user:
            print(
                f"ℹ️ Utilisateur existant trouvé avec l'ID: {existing_user['id']}")
            user_id = existing_user['id']
        else:
            # Créer un utilisateur de test avec un timestamp unique
            import time
            timestamp = int(time.time())

            user_id = db.create_user(
                username=f"testnotif_{timestamp}",
                email=f"test_{timestamp}@notification.com",
                password="testpass123",
                discord_id="123456789",
                discord_username="TestUser#1234"
            )

            if user_id:
                print(f"✅ Nouvel utilisateur créé avec l'ID: {user_id}")
            else:
                print("❌ Échec de la création de l'utilisateur")
                return False

        # Créer un ticket de test
        import time
        ticket_timestamp = int(time.time())

        ticket_id = db.create_ticket(
            user_id=user_id,
            category="bug",
            priority="high",
            subject=f"Test de notification Discord #{ticket_timestamp}",
            description="Ceci est un test pour vérifier que les notifications Discord fonctionnent correctement. Le bot devrait envoyer un message privé à naole77 avec les détails de ce ticket.",
            metadata={"test": True, "source": "notification_test",
                      "timestamp": ticket_timestamp}
        )

        if ticket_id:
            print(f"✅ Ticket créé avec l'ID: {ticket_id}")
            print("📱 Une notification Discord devrait être envoyée à naole77")
            print(f"   ID utilisateur Discord: 702923932239527978")
            print(
                f"   Sujet: Test de notification Discord #{ticket_timestamp}")
            print(f"   Priorité: HIGH")
            print(f"   Catégorie: bug")
            print("\n🔍 Vérifiez vos messages privés Discord pour confirmer la réception.")
        else:
            print("❌ Échec de la création du ticket")
            return False

        print("\n🎯 Test terminé avec succès !")
        return True

    except Exception as e:
        print(f"❌ Erreur pendant le test: {e}")
        return False
        return False


if __name__ == "__main__":
    test_notification_system()
