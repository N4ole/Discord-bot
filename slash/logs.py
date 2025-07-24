"""
Commandes slash - Module logs (gestion des logs)
"""
import discord
from discord import app_commands
from discord.ext import commands
from core.log_manager import log_manager


class LogsSlash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="setlog", description="Définit le canal de logs")
    @app_commands.describe(channel="Le canal où envoyer les logs")
    @app_commands.guild_only()
    async def setlog_slash(self, interaction: discord.Interaction, channel: discord.TextChannel):
        """Commande slash pour définir le canal de logs"""
        # Vérification des permissions
        if not interaction.user.guild_permissions.manage_guild:
            embed = discord.Embed(
                title="❌ Permissions Insuffisantes",
                description="Tu as besoin de la permission `Gérer le serveur` pour configurer les logs.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        success, message = log_manager.set_log_channel(
            interaction.guild.id, channel.id)

        if success:
            embed = discord.Embed(
                title="✅ Canal de Logs Configuré",
                description=message,
                color=discord.Color.green()
            )
            embed.add_field(
                name="📋 Prochaines étapes",
                value="Utilisez `/logon` pour activer les logs",
                inline=False
            )
            embed.add_field(
                name="📊 Types de logs",
                value="Messages, membres, vocal, modération, canaux...",
                inline=False
            )
        else:
            embed = discord.Embed(
                title="❌ Erreur",
                description=message,
                color=discord.Color.red()
            )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="logon", description="Active les logs pour ce serveur")
    @app_commands.guild_only()
    async def logon_slash(self, interaction: discord.Interaction):
        """Commande slash pour activer les logs"""
        # Vérification des permissions
        if not interaction.user.guild_permissions.manage_guild:
            embed = discord.Embed(
                title="❌ Permissions Insuffisantes",
                description="Tu as besoin de la permission `Gérer le serveur` pour gérer les logs.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        success, message = log_manager.enable_logs(interaction.guild.id)

        if success:
            channel_id = log_manager.get_log_channel(interaction.guild.id)
            embed = discord.Embed(
                title="✅ Logs Activés",
                description=message,
                color=discord.Color.green()
            )
            embed.add_field(
                name="📍 Canal de logs",
                value=f"<#{channel_id}>",
                inline=False
            )
            embed.add_field(
                name="📊 Événements surveillés",
                value="""
                • 💬 Messages (suppression, modification)
                • 👥 Membres (arrivée, départ, rôles)
                • 🔊 Vocal (connexion, déconnexion, changement)
                • 🔨 Modération (ban, unban)
                • 📝 Canaux (création, suppression)
                """,
                inline=False
            )
        else:
            embed = discord.Embed(
                title="❌ Erreur",
                description=message,
                color=discord.Color.red()
            )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="logoff", description="Désactive les logs pour ce serveur")
    @app_commands.guild_only()
    async def logoff_slash(self, interaction: discord.Interaction):
        """Commande slash pour désactiver les logs"""
        # Vérification des permissions
        if not interaction.user.guild_permissions.manage_guild:
            embed = discord.Embed(
                title="❌ Permissions Insuffisantes",
                description="Tu as besoin de la permission `Gérer le serveur` pour gérer les logs.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        success, message = log_manager.disable_logs(interaction.guild.id)

        if success:
            embed = discord.Embed(
                title="⚠️ Logs Désactivés",
                description=message,
                color=discord.Color.orange()
            )
            embed.add_field(
                name="ℹ️ Note",
                value="Le canal de logs reste configuré. Utilisez `/logon` pour réactiver.",
                inline=False
            )
        else:
            embed = discord.Embed(
                title="❌ Erreur",
                description="Impossible de désactiver les logs",
                color=discord.Color.red()
            )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="logstatus", description="Affiche le statut des logs")
    @app_commands.guild_only()
    async def logstatus_slash(self, interaction: discord.Interaction):
        """Commande slash pour afficher le statut des logs"""
        is_enabled = log_manager.is_logging_enabled(interaction.guild.id)
        channel_id = log_manager.get_log_channel(interaction.guild.id)

        if is_enabled and channel_id:
            embed = discord.Embed(
                title="📊 Statut des Logs",
                description="✅ **Logs activés**",
                color=discord.Color.green()
            )
            embed.add_field(
                name="📍 Canal configuré",
                value=f"<#{channel_id}>",
                inline=False
            )
        elif channel_id:
            embed = discord.Embed(
                title="📊 Statut des Logs",
                description="⚠️ **Canal configuré mais logs désactivés**",
                color=discord.Color.orange()
            )
            embed.add_field(
                name="📍 Canal configuré",
                value=f"<#{channel_id}>",
                inline=False
            )
            embed.add_field(
                name="💡 Action requise",
                value="Utilisez `/logon` pour activer les logs",
                inline=False
            )
        else:
            embed = discord.Embed(
                title="📊 Statut des Logs",
                description="❌ **Logs non configurés**",
                color=discord.Color.red()
            )
            embed.add_field(
                name="💡 Configuration requise",
                value="Utilisez `/setlog <canal>` puis `/logon`",
                inline=False
            )

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    """Fonction pour charger le cog"""
    await bot.add_cog(LogsSlash(bot))
    print("✅ Module slash/logs chargé")
