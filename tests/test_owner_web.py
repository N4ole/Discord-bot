#!/usr/bin/env python3
"""
Script de test pour vérifier la récupération des informations des propriétaires
dans l'interface web.
"""

import requests
import json
import sys


def test_owner_management():
    """Test de la gestion des propriétaires via l'interface web"""
    base_url = "http://127.0.0.1:8080"

    # Session pour maintenir les cookies
    session = requests.Session()

    print("=== TEST DE L'INTERFACE WEB DES PROPRIÉTAIRES ===")

    # 1. Test de connexion à la page de login
    print("\n1. Test de la page de login...")
    try:
        response = session.get(f"{base_url}/login")
        if response.status_code == 200:
            print("✅ Page de login accessible")
        else:
            print(f"❌ Erreur page de login: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

    # 2. Connexion admin
    print("\n2. Connexion admin...")
    try:
        login_data = {"username": "admin", "password": "admin123"}
        response = session.post(f"{base_url}/login", data=login_data)
        if response.status_code == 302 or "dashboard" in response.text:
            print("✅ Connexion admin réussie")
        else:
            print(f"❌ Erreur de connexion admin: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur de connexion admin: {e}")
        return False

    # 3. Test de la page de gestion des propriétaires
    print("\n3. Test de la page des propriétaires...")
    try:
        response = session.get(f"{base_url}/owner_management")
        if response.status_code == 200:
            print("✅ Page des propriétaires accessible")
            # Vérifier si on voit les IDs dans le HTML
            if "702923932239527978" in response.text:
                print("✅ ID propriétaire visible dans la page")
            if "avatar" in response.text.lower():
                print("✅ Section avatar présente")
        else:
            print(f"❌ Erreur page propriétaires: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur page propriétaires: {e}")

    # 4. Test de l'API des propriétaires
    print("\n4. Test de l'API des propriétaires...")
    try:
        response = session.get(f"{base_url}/api/owners")
        if response.status_code == 200:
            print("✅ API propriétaires accessible")
            data = response.json()
            print(f"📊 Nombre de propriétaires: {data.get('total', 0)}")

            for i, owner in enumerate(data.get('owners', []), 1):
                print(f"\n--- Propriétaire {i} ---")
                print(f"ID: {owner.get('id')}")
                print(f"Nom: {owner.get('name')}")
                print(
                    f"Avatar: {'✅ Présent' if owner.get('avatar') else '❌ Absent'}")
                print(f"Trouvé: {'✅' if owner.get('found') else '❌'}")
        else:
            print(f"❌ Erreur API propriétaires: {response.status_code}")
            print(f"Réponse: {response.text[:200]}...")
    except Exception as e:
        print(f"❌ Erreur API propriétaires: {e}")

    return True


if __name__ == "__main__":
    test_owner_management()
