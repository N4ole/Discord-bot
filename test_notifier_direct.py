"""
Test direct du notificateur de support
"""
import sys
import os
import time

# Ajouter le dossier racine au chemin
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def test_notifier():
    """Test direct du notificateur"""
    print("🧪 Test direct du système de notifications")
    print("=" * 50)

    try:
        from support_notifier import support_notifier
        print("✅ Module support_notifier importé")

        # Vérifier si le bot est configuré
        if support_notifier.bot is None:
            print("❌ Instance du bot non configurée dans le notificateur")
            print("⚠️ Le bot Discord principal doit être en cours d'exécution")
            return False
        else:
            print(
                f"✅ Instance du bot configurée: {type(support_notifier.bot)}")
            print(f"✅ Bot connecté: {support_notifier.bot.is_ready()}")
            print(f"✅ ID admin configuré: {support_notifier.admin_user_id}")

        # Créer des données de test
        ticket_data = {
            'id': 999,
            'subject': 'Test direct de notification',
            'username': 'TestUser',
            'email': 'test@example.com',
            'category': 'test',
            'priority': 'high',
            'description': 'Ceci est un test direct du système de notifications.',
            'created_at': time.strftime('%Y-%m-%d %H:%M:%S')
        }

        print("\n📱 Tentative d'envoi de notification...")
        print(f"   Vers l'utilisateur ID: {support_notifier.admin_user_id}")

        # Note: On ne peut pas facilement tester l'envoi sans bloquer le thread principal
        # car le bot utilise déjà sa boucle d'événements
        print("ℹ️ Test de configuration terminé.")
        print("💡 Pour tester l'envoi, utilisez l'interface web du support.")

        return True

    except ImportError as e:
        print(f"❌ Erreur d'importation: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


if __name__ == "__main__":
    test_notifier()
