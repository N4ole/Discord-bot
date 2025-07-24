#!/usr/bin/env python3
"""
Test direct de la récupération d'utilisateurs Discord
"""

import asyncio
import sys
import os
from pathlib import Path

# Ajouter le répertoire du bot au path
bot_dir = Path(r"c:\Users\eloan\OneDrive\Documents\GitHub\Discord-bot")
sys.path.insert(0, str(bot_dir))


async def test_user_fetch():
    """Test de récupération d'utilisateurs"""

    print("=== TEST DE RÉCUPÉRATION D'UTILISATEURS DISCORD ===")

    try:
        # Importer le token et créer un client Discord
        from core.bot_owner_manager import get_bot_owners

        # Obtenir les propriétaires
        owners = get_bot_owners()
        print(f"Propriétaires configurés: {owners}")

        # Créer un client Discord simple
        import discord

        # Lire le token depuis les variables d'environnement
        import os
        token = os.getenv('DISCORD_TOKEN')

        if not token:
            print("❌ Token non trouvé dans les variables d'environnement")
            return

        print("✅ Token trouvé")

        # Créer un client Discord
        intents = discord.Intents.default()
        client = discord.Client(intents=intents)

        @client.event
        async def on_ready():
            print(f"✅ Bot connecté: {client.user}")

            # Tester la récupération des utilisateurs
            for owner_id in owners:
                try:
                    user = await client.fetch_user(owner_id)
                    print(
                        f"✅ Utilisateur {owner_id}: {user.name} - Avatar: {'✅' if user.avatar else '❌'}")
                except Exception as e:
                    print(f"❌ Erreur pour {owner_id}: {e}")

            await client.close()

        # Se connecter
        await client.start(token)

    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_user_fetch())
