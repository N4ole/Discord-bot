"""
Gestionnaire des préfixes personnalisés par serveur
"""
import json
import os
import asyncio
from discord.ext import commands


class PrefixManager:
    def __init__(self, file_path="prefixes.json"):
        self.file_path = file_path
        self.prefixes = {}
        self.default_prefix = "!"
        self.load_prefixes()

    def load_prefixes(self):
        """Charge les préfixes depuis le fichier JSON"""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    self.prefixes = json.load(f)
                print(
                    f"✅ {len(self.prefixes)} préfixe(s) personnalisé(s) chargé(s)")
            except Exception as e:
                print(f"❌ Erreur lors du chargement des préfixes: {e}")
                self.prefixes = {}
        else:
            print("📝 Aucun fichier de préfixes trouvé, utilisation du préfixe par défaut")

    def save_prefixes(self):
        """Sauvegarde les préfixes dans le fichier JSON"""
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.prefixes, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde des préfixes: {e}")
            return False

    def get_prefix(self, guild_id):
        """Récupère le préfixe pour un serveur donné"""
        if guild_id is None:
            return self.default_prefix
        return self.prefixes.get(str(guild_id), self.default_prefix)

    def set_prefix(self, guild_id, prefix):
        """Définit le préfixe pour un serveur donné"""
        if guild_id is None:
            return False

        # Validation du préfixe
        if len(prefix) > 5:
            return False, "Le préfixe ne peut pas dépasser 5 caractères"

        if not prefix.strip():
            return False, "Le préfixe ne peut pas être vide"

        # Caractères interdits
        forbidden_chars = ['@', '#', '`', '\\', '/']
        if any(char in prefix for char in forbidden_chars):
            return False, f"Le préfixe ne peut pas contenir: {', '.join(forbidden_chars)}"

        self.prefixes[str(guild_id)] = prefix
        success = self.save_prefixes()

        if success:
            return True, f"Préfixe changé en `{prefix}` pour ce serveur"
        else:
            return False, "Erreur lors de la sauvegarde"

    def reset_prefix(self, guild_id):
        """Remet le préfixe par défaut pour un serveur"""
        if guild_id is None:
            return False

        if str(guild_id) in self.prefixes:
            del self.prefixes[str(guild_id)]
            success = self.save_prefixes()
            return success, f"Préfixe remis à `{self.default_prefix}` pour ce serveur"
        else:
            return True, f"Ce serveur utilise déjà le préfixe par défaut `{self.default_prefix}`"


# Instance globale du gestionnaire
prefix_manager = PrefixManager()


def get_prefix(bot, message):
    """Fonction pour obtenir le préfixe dynamiquement"""
    if message.guild:
        prefix = prefix_manager.get_prefix(message.guild.id)
    else:
        prefix = prefix_manager.default_prefix

    # Retourne une liste de préfixes possibles (mention + préfixe personnalisé)
    return commands.when_mentioned_or(prefix)(bot, message)
