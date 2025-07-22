"""
Commandes préfixées - Module logs (gestion des logs)
"""
import discord
from discord.ext import commands
from log_manager import log_manager


class LogsPrefixe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="setlog", help="Définit le canal de logs")
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def setlog(self, ctx, channel: discord.TextChannel):
        """Définit le canal où envoyer les logs"""
        success, message = log_manager.set_log_channel(
            ctx.guild.id, channel.id)

        if success:
            embed = discord.Embed(
                title="✅ Canal de Logs Configuré",
                description=message,
                color=discord.Color.green()
            )
            embed.add_field(
                name="📋 Prochaines étapes",
                value="Utilisez `logon` pour activer les logs",
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

        await ctx.send(embed=embed)

    @commands.command(name="logon", help="Active les logs pour ce serveur")
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def logon(self, ctx):
        """Active le système de logs"""
        success, message = log_manager.enable_logs(ctx.guild.id)

        if success:
            channel_id = log_manager.get_log_channel(ctx.guild.id)
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

        await ctx.send(embed=embed)

    @commands.command(name="logoff", help="Désactive les logs pour ce serveur")
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def logoff(self, ctx):
        """Désactive le système de logs"""
        success, message = log_manager.disable_logs(ctx.guild.id)

        if success:
            embed = discord.Embed(
                title="⚠️ Logs Désactivés",
                description=message,
                color=discord.Color.orange()
            )
            embed.add_field(
                name="ℹ️ Note",
                value="Le canal de logs reste configuré. Utilisez `logon` pour réactiver.",
                inline=False
            )
        else:
            embed = discord.Embed(
                title="❌ Erreur",
                description="Impossible de désactiver les logs",
                color=discord.Color.red()
            )

        await ctx.send(embed=embed)

    @commands.command(name="logstatus", help="Affiche le statut des logs")
    @commands.guild_only()
    async def logstatus(self, ctx):
        """Affiche le statut actuel du système de logs"""
        is_enabled = log_manager.is_logging_enabled(ctx.guild.id)
        channel_id = log_manager.get_log_channel(ctx.guild.id)

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
                value="Utilisez `logon` pour activer les logs",
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
                value="Utilisez `setlog <canal>` puis `logon`",
                inline=False
            )

        await ctx.send(embed=embed)

    # Gestion des erreurs
    @setlog.error
    async def setlog_error(self, ctx, error):
        """Gestion des erreurs pour setlog"""
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="❌ Permissions Insuffisantes",
                description="Tu as besoin de la permission `Gérer le serveur` pour configurer les logs.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="❌ Argument Manquant",
                description="Usage: `setlog <#canal>`\nExemple: `setlog #logs`",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.ChannelNotFound):
            embed = discord.Embed(
                title="❌ Canal Introuvable",
                description="Le canal spécifié n'existe pas ou n'est pas accessible.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    @logon.error
    @logoff.error
    async def log_toggle_error(self, ctx, error):
        """Gestion des erreurs pour logon/logoff"""
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="❌ Permissions Insuffisantes",
                description="Tu as besoin de la permission `Gérer le serveur` pour gérer les logs.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)


async def setup(bot):
    """Fonction pour charger le cog"""
    await bot.add_cog(LogsPrefixe(bot))
    print("✅ Module prefixe/logs chargé")
