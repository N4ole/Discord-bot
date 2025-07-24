"""
Gestionnaire du système de logs
"""
import json
import os
import discord
from datetime import datetime
from discord.ext import commands


class LogManager:
    def __init__(self, file_path="config/logs_config.json"):
        self.file_path = file_path
        self.log_configs = {}
        self.load_configs()

    def load_configs(self):
        """Charge la configuration des logs depuis le fichier JSON"""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    self.log_configs = json.load(f)
                print(
                    f"✅ Configuration de logs chargée pour {len(self.log_configs)} serveur(s)")
            except Exception as e:
                print(f"❌ Erreur lors du chargement des configs logs: {e}")
                self.log_configs = {}
        else:
            print("📝 Aucun fichier de configuration de logs trouvé")

    def save_configs(self):
        """Sauvegarde la configuration des logs dans le fichier JSON"""
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.log_configs, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde des configs logs: {e}")
            return False

    def set_log_channel(self, guild_id, channel_id):
        """Définit le canal de logs pour un serveur"""
        if guild_id is None:
            return False, "Impossible d'utiliser cette commande en MP"

        guild_str = str(guild_id)
        if guild_str not in self.log_configs:
            self.log_configs[guild_str] = {
                "channel_id": None, "enabled": False}

        self.log_configs[guild_str]["channel_id"] = channel_id
        success = self.save_configs()

        if success:
            return True, f"Canal de logs défini sur <#{channel_id}>"
        else:
            return False, "Erreur lors de la sauvegarde"

    def enable_logs(self, guild_id):
        """Active les logs pour un serveur"""
        if guild_id is None:
            return False, "Impossible d'utiliser cette commande en MP"

        guild_str = str(guild_id)
        if guild_str not in self.log_configs or self.log_configs[guild_str]["channel_id"] is None:
            return False, "Aucun canal de logs configuré. Utilisez d'abord `setlog <canal>`"

        self.log_configs[guild_str]["enabled"] = True
        success = self.save_configs()

        if success:
            return True, "✅ Logs activés pour ce serveur"
        else:
            return False, "Erreur lors de la sauvegarde"

    def disable_logs(self, guild_id):
        """Désactive les logs pour un serveur"""
        if guild_id is None:
            return False, "Impossible d'utiliser cette commande en MP"

        guild_str = str(guild_id)
        if guild_str in self.log_configs:
            self.log_configs[guild_str]["enabled"] = False
            success = self.save_configs()

            if success:
                return True, "❌ Logs désactivés pour ce serveur"
            else:
                return False, "Erreur lors de la sauvegarde"
        else:
            return True, "Les logs n'étaient pas configurés"

    def get_log_channel(self, guild_id):
        """Récupère le canal de logs pour un serveur"""
        if guild_id is None:
            return None

        guild_str = str(guild_id)
        config = self.log_configs.get(guild_str)
        if config and config.get("enabled", False):
            return config.get("channel_id")
        return None

    def is_logging_enabled(self, guild_id):
        """Vérifie si les logs sont activés pour un serveur"""
        if guild_id is None:
            return False

        guild_str = str(guild_id)
        config = self.log_configs.get(guild_str, {})
        return config.get("enabled", False) and config.get("channel_id") is not None


# Instance globale du gestionnaire
log_manager = LogManager()


class LogFormatter:
    """Classe utilitaire pour formater les logs"""

    @staticmethod
    def create_log_embed(title, description, color, user=None, channel=None, extra_fields=None):
        """Crée un embed standardisé pour les logs"""
        embed = discord.Embed(
            title=title,
            description=description,
            color=color,
            timestamp=datetime.utcnow()
        )

        if user:
            embed.set_author(
                name=f"{user.display_name} ({user})",
                icon_url=user.display_avatar.url
            )
            embed.add_field(name="👤 Utilisateur ID",
                            value=user.id, inline=True)

        if channel:
            embed.add_field(name="📍 Canal", value=channel.mention, inline=True)

        if extra_fields:
            for field in extra_fields:
                embed.add_field(**field)

        return embed

    @staticmethod
    def get_color_for_event(event_type):
        """Retourne une couleur appropriée selon le type d'événement"""
        colors = {
            "join": discord.Color.green(),
            "leave": discord.Color.red(),
            "message_delete": discord.Color.orange(),
            "message_edit": discord.Color.yellow(),
            "voice_join": discord.Color.blue(),
            "voice_leave": discord.Color.purple(),
            "voice_move": discord.Color.blurple(),
            "ban": discord.Color.dark_red(),
            "unban": discord.Color.dark_green(),
            "kick": discord.Color.red(),
            "role_add": discord.Color.green(),
            "role_remove": discord.Color.red(),
            "channel_create": discord.Color.green(),
            "channel_delete": discord.Color.red(),
            "default": discord.Color.light_grey()
        }
        return colors.get(event_type, colors["default"])
