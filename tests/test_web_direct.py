"""
Test direct avec l'instance support_db du web_panel
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def test_web_support_db():
    """Test avec l'instance support_db du web_panel"""
    print("🧪 Test avec l'instance support_db du web_panel")
    print("=" * 60)

    try:
        # Importer l'instance du web_panel
        from web_panel import support_db
        print("✅ Instance support_db importée depuis web_panel")

        # Créer un utilisateur de test
        import time
        timestamp = int(time.time())

        user_id = support_db.create_user(
            username=f"webtest_{timestamp}",
            email=f"webtest_{timestamp}@example.com",
            password="testpass123",
            discord_id="555666777",
            discord_username="WebTestUser#5678"
        )

        if user_id:
            print(f"✅ Utilisateur créé avec l'ID: {user_id}")

            # Créer un ticket
            ticket_id = support_db.create_ticket(
                user_id=user_id,
                category="test",
                priority="high",
                subject=f"Test direct web_panel {timestamp}",
                description="Test direct avec l'instance support_db du web_panel pour vérifier les notifications.",
                metadata={"test_direct": True}
            )

            if ticket_id:
                print(f"✅ Ticket créé avec l'ID: {ticket_id}")
                print("📱 Les logs de notification devraient apparaître maintenant...")
            else:
                print("❌ Échec de la création du ticket")
        else:
            print("❌ Échec de la création de l'utilisateur")

    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_web_support_db()
