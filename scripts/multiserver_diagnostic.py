"""
Commandes de diagnostic et gestion multi-serveurs
"""
import discord
from discord.ext import commands
from core.log_manager import log_manager


class MultiServerDiagnostic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="logdiag", help="Diagnostic du système de logs (Owner uniquement)")
    @commands.is_owner()
    async def log_diagnostic(self, ctx):
        """Commande de diagnostic pour vérifier la configuration multi-serveurs"""
        embed = discord.Embed(
            title="🔍 Diagnostic Multi-Serveurs",
            description="État du système de logs sur tous les serveurs",
            color=discord.Color.blue()
        )

        # Statistiques générales
        total_servers = len(self.bot.guilds)
        configured_servers = len(log_manager.log_configs)
        enabled_servers = sum(
            1 for config in log_manager.log_configs.values() if config.get("enabled", False))

        embed.add_field(
            name="📊 Statistiques Générales",
            value=f"""
            **Serveurs connectés:** {total_servers}
            **Serveurs configurés:** {configured_servers}
            **Serveurs avec logs actifs:** {enabled_servers}
            """,
            inline=False
        )

        # Détails par serveur (limité aux 10 premiers pour éviter un embed trop long)
        server_details = []
        for guild_id, config in list(log_manager.log_configs.items())[:10]:
            guild = self.bot.get_guild(int(guild_id))
            guild_name = guild.name if guild else f"Serveur inconnu ({guild_id})"

            status = "✅ Actif" if config.get(
                "enabled", False) else "⚠️ Inactif"
            channel_id = config.get("channel_id")
            channel_info = f"<#{channel_id}>" if channel_id else "Non défini"

            server_details.append(
                f"**{guild_name}**\n{status} - Canal: {channel_info}")

        if server_details:
            embed.add_field(
                name="🏠 Détails par Serveur",
                value="\n\n".join(server_details),
                inline=False
            )

        if configured_servers > 10:
            embed.add_field(
                name="ℹ️ Note",
                value=f"Seuls les 10 premiers serveurs sont affichés. Total: {configured_servers}",
                inline=False
            )

        embed.set_footer(
            text="💡 Chaque serveur a sa configuration indépendante")
        await ctx.send(embed=embed)

    @commands.command(name="logclear", help="Supprime la config d'un serveur spécifique (Owner uniquement)")
    @commands.is_owner()
    async def log_clear_server(self, ctx, guild_id: int = None):
        """Supprime la configuration de logs d'un serveur spécifique"""
        if guild_id is None:
            guild_id = ctx.guild.id if ctx.guild else None

        if guild_id is None:
            await ctx.send("❌ Impossible de déterminer l'ID du serveur")
            return

        guild_str = str(guild_id)
        if guild_str in log_manager.log_configs:
            del log_manager.log_configs[guild_str]
            success = log_manager.save_configs()

            if success:
                guild = self.bot.get_guild(guild_id)
                guild_name = guild.name if guild else f"ID: {guild_id}"

                embed = discord.Embed(
                    title="🗑️ Configuration Supprimée",
                    description=f"Configuration de logs supprimée pour **{guild_name}**",
                    color=discord.Color.green()
                )
            else:
                embed = discord.Embed(
                    title="❌ Erreur",
                    description="Impossible de sauvegarder les modifications",
                    color=discord.Color.red()
                )
        else:
            embed = discord.Embed(
                title="⚠️ Aucune Configuration",
                description="Ce serveur n'a pas de configuration de logs",
                color=discord.Color.orange()
            )

        await ctx.send(embed=embed)

    @commands.command(name="testlog", help="Test du système de logs (Admin)")
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def test_log_system(self, ctx):
        """Envoie un message de test dans le canal de logs"""
        if not log_manager.is_logging_enabled(ctx.guild.id):
            embed = discord.Embed(
                title="❌ Logs Désactivés",
                description="Les logs ne sont pas activés sur ce serveur.\nUtilisez `setlog` puis `logon` pour les configurer.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        channel_id = log_manager.get_log_channel(ctx.guild.id)
        channel = ctx.guild.get_channel(channel_id)

        if not channel:
            embed = discord.Embed(
                title="❌ Canal Introuvable",
                description="Le canal de logs configuré n'existe plus. Reconfigurez avec `setlog`.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        # Créer un embed de test
        test_embed = discord.Embed(
            title="🧪 Test du Système de Logs",
            description="Ceci est un message de test pour vérifier le bon fonctionnement du système de logs.",
            color=discord.Color.gold(),
            timestamp=discord.utils.utcnow()
        )

        test_embed.set_author(
            name=f"Testé par {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar.url
        )

        test_embed.add_field(
            name="🏠 Serveur",
            value=f"{ctx.guild.name} (ID: {ctx.guild.id})",
            inline=True
        )

        test_embed.add_field(
            name="📍 Canal de logs",
            value=channel.mention,
            inline=True
        )

        test_embed.set_footer(text="✅ Système de logs fonctionnel")

        try:
            await channel.send(embed=test_embed)

            success_embed = discord.Embed(
                title="✅ Test Réussi",
                description=f"Message de test envoyé avec succès dans {channel.mention}",
                color=discord.Color.green()
            )
            await ctx.send(embed=success_embed)

        except Exception as e:
            error_embed = discord.Embed(
                title="❌ Erreur de Test",
                description=f"Impossible d'envoyer le message de test: {e}",
                color=discord.Color.red()
            )
            await ctx.send(embed=error_embed)


async def setup(bot):
    """Fonction pour charger le cog"""
    await bot.add_cog(MultiServerDiagnostic(bot))
    print("✅ Module diagnostic multi-serveurs chargé")
