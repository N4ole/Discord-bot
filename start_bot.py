#!/usr/bin/env python3
"""
Wrapper pour démarrer le bot et afficher tous les messages
"""

import subprocess
import sys
import os


def main():
    print("=== DÉMARRAGE DU BOT DISCORD ===")

    # Changer vers le répertoire du bot
    bot_dir = r"c:\Users\eloan\OneDrive\Documents\GitHub\Discord-bot"
    os.chdir(bot_dir)
    print(f"Répertoire: {os.getcwd()}")

    # Démarrer le bot avec capture des sorties
    try:
        process = subprocess.Popen(
            [sys.executable, "main.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )

        print("Bot démarré, lecture des logs...")

        # Lire les sorties en temps réel
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
                sys.stdout.flush()

    except KeyboardInterrupt:
        print("\n=== ARRÊT DU BOT ===")
        process.terminate()
    except Exception as e:
        print(f"Erreur: {e}")


if __name__ == "__main__":
    main()
