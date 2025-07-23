"""
Fichier principal pour lancer le bot Discord
"""
import os
from dotenv import load_dotenv
from engine import DiscordBot


def main():
    """Point d'entrée principal du bot"""
    # Charge les variables d'environnement depuis le fichier .env
    load_dotenv()

    # Récupère le token depuis les variables d'environnement
    token = os.getenv('DISCORD_TOKEN')

    if not token:
        print("Erreur: DISCORD_TOKEN n'est pas défini dans les variables d'environnement")
        print("Veuillez créer un fichier .env avec votre token Discord")
        return

    # Crée et lance le bot
    bot = DiscordBot()

    # Initialiser le système de notifications de support
    try:
        from web_panel import set_bot_instance
        set_bot_instance(bot)
        print("📱 Système de notifications de support initialisé")
    except ImportError as e:
        print(f"⚠️ Impossible d'importer le module web_panel: {e}")
    except Exception as e:
        print(f"⚠️ Erreur lors de l'initialisation des notifications: {e}")

    bot.run(token)


if __name__ == "__main__":
    main()
