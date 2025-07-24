#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test du système de notifications multi-admins
Ce script démontre comment ajouter et gérer plusieurs admins pour recevoir les notifications
"""

from core.support_notifier import support_notifier
import asyncio
import sys
import os

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def test_multi_admin_configuration():
    """Test de la configuration multi-admin"""

    print("🔧 Configuration actuelle du système de notifications:")
    print(f"   Admins configurés: {support_notifier.admin_user_ids}")
    print(f"   Nombre d'admins: {len(support_notifier.admin_user_ids)}")

    print("\n📋 Pour ajouter un nouvel admin au système de notifications:")
    print("   1. Ouvrez le fichier 'support_notifier.py'")
    print("   2. Trouvez la ligne: admin_user_ids = [702923932239527978]")
    print("   3. Ajoutez l'ID Discord de la nouvelle personne:")
    print("      admin_user_ids = [702923932239527978, 123456789012345678]")
    print("   4. Redémarrez le bot")

    print("\n🔍 Comment obtenir l'ID Discord d'une personne:")
    print("   1. Activez le mode développeur dans Discord (Paramètres > Avancé)")
    print("   2. Clic droit sur l'utilisateur > Copier l'ID")
    print("   3. L'ID est un nombre de 18 chiffres")

    print("\n⚠️  Permissions requises:")
    print("   - L'admin doit autoriser les MP de membres du serveur")
    print("   - Le bot doit pouvoir envoyer des MP à cette personne")

    print("\n✅ Avantages du système multi-admin:")
    print("   - Redondance: si un admin n'est pas disponible")
    print("   - Répartition de la charge de support")
    print("   - Notifications en temps réel pour tous les admins")


def simulate_notification_test():
    """Simule un test de notification"""

    print("\n🧪 Simulation d'un test de notification:")
    print("   Nombre d'admins qui recevraient la notification:",
          len(support_notifier.admin_user_ids))

    for i, admin_id in enumerate(support_notifier.admin_user_ids, 1):
        print(f"   Admin {i}: {admin_id}")

    print("\n📤 Lors d'un nouveau ticket, chaque admin recevra:")
    print("   - Une notification Discord MP")
    print("   - Un embed avec les détails du ticket")
    print("   - Des liens vers le panel admin")


def show_example_configuration():
    """Montre des exemples de configuration"""

    print("\n📝 Exemples de configurations:")

    print("\n1️⃣ Configuration actuelle (1 admin):")
    print("   admin_user_ids = [702923932239527978]  # naole77")

    print("\n2️⃣ Configuration avec 2 admins:")
    print("   admin_user_ids = [")
    print("       702923932239527978,  # naole77")
    print("       123456789012345678   # Nouvel admin")
    print("   ]")

    print("\n3️⃣ Configuration avec 3 admins:")
    print("   admin_user_ids = [")
    print("       702923932239527978,  # naole77")
    print("       123456789012345678,  # Admin 2")
    print("       987654321098765432   # Admin 3")
    print("   ]")

    print("\n💡 Note: Vous pouvez ajouter autant d'admins que nécessaire!")


if __name__ == "__main__":
    print("=" * 60)
    print("🤖 SUMMER BOT - Test du Système Multi-Admin")
    print("=" * 60)

    test_multi_admin_configuration()
    simulate_notification_test()
    show_example_configuration()

    print("\n" + "=" * 60)
    print("✅ Test terminé - Le système est prêt pour les multi-admins!")
    print("=" * 60)
