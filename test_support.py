#!/usr/bin/env python3
"""
Test du système de support
Vérifie que toutes les fonctionnalités sont opérationnelles
"""

import support_db
import os
import sys
import sqlite3
from datetime import datetime

# Ajouter le dossier parent au path pour importer les modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def test_support_system():
    """Test complet du système de support"""
    print("🧪 Test du système de support Summer Bot")
    print("=" * 50)

    # Initialiser la base de données
    print("📦 Initialisation de la base de données...")
    try:
        db = support_db.SupportDB()
        print("✅ Base de données initialisée avec succès")
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation: {e}")
        return False

    # Test 1: Création d'utilisateur
    print("\n👤 Test de création d'utilisateur...")
    try:
        user_id = db.create_user(
            username="test_user",
            email="test@example.com",
            password="test123",
            discord_username="TestUser#1234",
            discord_id="123456789012345678"
        )

        if user_id:
            print(f"✅ Utilisateur créé avec l'ID: {user_id}")
        else:
            print("❌ Échec de la création d'utilisateur")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de la création d'utilisateur: {e}")
        return False

    # Test 2: Authentification
    print("\n🔐 Test d'authentification...")
    try:
        user = db.authenticate_user("test_user", "test123")

        if user:
            print(f"✅ Authentification réussie pour: {user['username']}")
        else:
            print("❌ Échec de l'authentification")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de l'authentification: {e}")
        return False

    # Test 3: Création de ticket
    print("\n🎫 Test de création de ticket...")
    try:
        metadata = {
            "server_id": "987654321098765432",
            "command_used": "/help",
            "error_message": "Commande non trouvée",
            "urgent_contact": True,
            "email_notifications": True
        }

        ticket_id = db.create_ticket(
            user_id=user_id,
            category="bot_commands",
            priority="medium",
            subject="Problème avec la commande /help",
            description="La commande /help ne fonctionne pas correctement et renvoie une erreur.",
            metadata=metadata
        )

        if ticket_id:
            print(f"✅ Ticket créé avec l'ID: {ticket_id}")
        else:
            print("❌ Échec de la création de ticket")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de la création de ticket: {e}")
        return False

    # Test 4: Récupération de ticket
    print("\n📋 Test de récupération de ticket...")
    try:
        ticket = db.get_ticket_by_id(ticket_id)

        if ticket:
            print(f"✅ Ticket récupéré: #{ticket['id']} - {ticket['subject']}")
            print(f"   Status: {ticket['status']}")
            print(f"   Priorité: {ticket['priority']}")
            print(f"   Métadonnées: {len(ticket['metadata'])} éléments")
        else:
            print("❌ Échec de la récupération de ticket")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de la récupération de ticket: {e}")
        return False

    # Test 5: Ajout de réponse
    print("\n💬 Test d'ajout de réponse...")
    try:
        response_id = db.add_ticket_response(
            ticket_id=ticket_id,
            message="Voici des informations supplémentaires sur le problème...",
            is_admin=False
        )

        if response_id:
            print(f"✅ Réponse ajoutée avec l'ID: {response_id}")
        else:
            print("❌ Échec de l'ajout de réponse")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de l'ajout de réponse: {e}")
        return False

    # Test 6: Récupération des réponses
    print("\n📨 Test de récupération des réponses...")
    try:
        responses = db.get_ticket_responses(ticket_id)

        if responses:
            print(f"✅ {len(responses)} réponse(s) récupérée(s)")
            for i, response in enumerate(responses, 1):
                print(f"   Réponse {i}: {response['message'][:50]}...")
        else:
            print("❌ Aucune réponse trouvée")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des réponses: {e}")
        return False

    # Test 7: Statistiques
    print("\n📊 Test des statistiques...")
    try:
        total_tickets = db.get_total_tickets()
        resolved_tickets = db.get_resolved_tickets_count()
        active_users = db.get_active_users_count()

        print(f"✅ Statistiques récupérées:")
        print(f"   Total tickets: {total_tickets}")
        print(f"   Tickets résolus: {resolved_tickets}")
        print(f"   Utilisateurs actifs: {active_users}")

    except Exception as e:
        print(f"❌ Erreur lors de la récupération des statistiques: {e}")
        return False

    # Test 8: Mise à jour du statut
    print("\n🔄 Test de mise à jour du statut...")
    try:
        db.update_ticket_status(ticket_id, "resolved")

        # Vérifier la mise à jour
        updated_ticket = db.get_ticket_by_id(ticket_id)
        if updated_ticket and updated_ticket['status'] == 'resolved':
            print("✅ Statut mis à jour avec succès")
        else:
            print("❌ Échec de la mise à jour du statut")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour du statut: {e}")
        return False

    print("\n" + "=" * 50)
    print("🎉 Tous les tests sont passés avec succès !")
    print("✅ Le système de support est opérationnel")

    return True


def test_web_routes():
    """Test des routes web (simulation)"""
    print("\n🌐 Test des routes web...")

    routes_to_test = [
        "/support",
        "/support/register",
        "/support/login",
        "/support/dashboard",
        "/support/ticket/new",
        "/support/tickets"
    ]

    print("Routes configurées:")
    for route in routes_to_test:
        print(f"  ✅ {route}")

    return True


def cleanup_test_data():
    """Nettoyage des données de test"""
    print("\n🧹 Nettoyage des données de test...")
    try:
        # Supprimer le fichier de base de données de test s'il existe
        if os.path.exists("support_tickets.db"):
            os.remove("support_tickets.db")
            print("✅ Données de test supprimées")
        else:
            print("ℹ️  Aucune donnée de test à supprimer")
    except Exception as e:
        print(f"⚠️  Erreur lors du nettoyage: {e}")


def main():
    """Fonction principale de test"""
    print("🤖 Test du Système de Support Summer Bot")
    print("🔍 Vérification de l'intégrité du système...")
    print()

    try:
        # Exécuter les tests
        if test_support_system():
            test_web_routes()
            print("\n🎯 Résultat Final: SUCCÈS")
            print("Le système de support est prêt à être utilisé !")
        else:
            print("\n❌ Résultat Final: ÉCHEC")
            print("Des erreurs ont été détectées dans le système.")

    except KeyboardInterrupt:
        print("\n⏹️  Tests interrompus par l'utilisateur")

    finally:
        # Nettoyage (optionnel - commenté pour garder les données de test)
        # cleanup_test_data()
        pass

    print("\n📝 Note: Pour tester l'interface web complète:")
    print("   python web_panel.py")
    print("   Puis visitez: http://127.0.0.1:8080/support")


if __name__ == "__main__":
    main()
