"""
Commandes utilitaires slash pour le bot Discord
"""
import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
import time
import platform
import psutil
import aiohttp


class UtilsSlash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()

    @app_commands.command(name="ping", description="Affiche la latence du bot")
    async def ping_slash(self, interaction: discord.Interaction):
        """Commande ping pour tester la latence"""
        start_time = time.time()

        embed = discord.Embed(
            title="🏓 Pong !",
            color=discord.Color.green()
        )

        # Latence de l'API Discord
        api_latency = round(self.bot.latency * 1000, 2)

        # Temps de réponse
        response_time = round((time.time() - start_time) * 1000, 2)

        embed.add_field(
            name="📡 Latence API",
            value=f"`{api_latency}ms`",
            inline=True
        )
        embed.add_field(
            name="⚡ Temps de réponse",
            value=f"`{response_time}ms`",
            inline=True
        )

        # Indicateur de qualité
        if api_latency < 100:
            quality = "🟢 Excellente"
        elif api_latency < 200:
            quality = "🟡 Bonne"
        elif api_latency < 300:
            quality = "🟠 Moyenne"
        else:
            quality = "🔴 Mauvaise"

        embed.add_field(
            name="📊 Qualité",
            value=quality,
            inline=True
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="info", description="Affiche les informations d'un utilisateur")
    @app_commands.describe(user="L'utilisateur dont afficher les informations")
    async def userinfo_slash(self, interaction: discord.Interaction, user: discord.Member = None):
        """Affiche les informations détaillées d'un utilisateur"""
        if user is None:
            user = interaction.user

        embed = discord.Embed(
            title=f"👤 Informations de {user.display_name}",
            color=user.accent_color or discord.Color.blurple()
        )

        embed.set_thumbnail(url=user.display_avatar.url)

        # Informations générales
        embed.add_field(
            name="🏷️ Nom d'utilisateur",
            value=f"`{user.name}`",
            inline=True
        )
        embed.add_field(
            name="🆔 ID",
            value=f"`{user.id}`",
            inline=True
        )
        embed.add_field(
            name="📅 Compte créé",
            value=f"<t:{int(user.created_at.timestamp())}:F>",
            inline=False
        )

        if interaction.guild:
            embed.add_field(
                name="📥 A rejoint le serveur",
                value=f"<t:{int(user.joined_at.timestamp())}:F>" if user.joined_at else "Inconnu",
                inline=False
            )

            # Rôles (maximum 10)
            roles = [role.mention for role in user.roles[1:]][:10]
            if roles:
                embed.add_field(
                    name=f"🎭 Rôles ({len(user.roles)-1})",
                    value=" ".join(roles) if len(
                        " ".join(roles)) < 1024 else f"{len(user.roles)-1} rôles",
                    inline=False
                )

            # Permissions clés
            perms = user.guild_permissions
            key_perms = []
            if perms.administrator:
                key_perms.append("👑 Administrateur")
            if perms.manage_guild:
                key_perms.append("⚙️ Gérer le serveur")
            if perms.manage_channels:
                key_perms.append("📝 Gérer les salons")
            if perms.manage_messages:
                key_perms.append("📋 Gérer les messages")
            if perms.kick_members:
                key_perms.append("👢 Expulser")
            if perms.ban_members:
                key_perms.append("🔨 Bannir")

            if key_perms:
                embed.add_field(
                    name="🔑 Permissions clés",
                    value="\n".join(key_perms),
                    inline=True
                )

        # Statut
        status_emoji = {
            discord.Status.online: "🟢",
            discord.Status.idle: "🟡",
            discord.Status.dnd: "🔴",
            discord.Status.offline: "⚫"
        }

        embed.add_field(
            name="📊 Statut",
            value=f"{status_emoji.get(user.status, '❓')} {str(user.status).title()}",
            inline=True
        )

        # Activité
        if user.activity:
            activity_type = {
                discord.ActivityType.playing: "🎮 Joue à",
                discord.ActivityType.streaming: "📺 Stream",
                discord.ActivityType.listening: "🎵 Écoute",
                discord.ActivityType.watching: "👀 Regarde",
                discord.ActivityType.custom: "💭",
                discord.ActivityType.competing: "🏆 Concours"
            }

            embed.add_field(
                name="🎯 Activité",
                value=f"{activity_type.get(user.activity.type, '❓')} {user.activity.name}",
                inline=True
            )

        embed.set_footer(text=f"Demandé par {interaction.user.display_name}")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="server", description="Affiche les informations du serveur")
    async def serverinfo_slash(self, interaction: discord.Interaction):
        """Affiche les informations du serveur"""
        if not interaction.guild:
            await interaction.response.send_message("❌ Cette commande ne peut être utilisée qu'dans un serveur!", ephemeral=True)
            return

        guild = interaction.guild

        embed = discord.Embed(
            title=f"🏰 {guild.name}",
            description=guild.description or "Aucune description",
            color=discord.Color.blue()
        )

        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        # Informations générales
        embed.add_field(
            name="👑 Propriétaire",
            value=guild.owner.mention if guild.owner else "Inconnu",
            inline=True
        )
        embed.add_field(
            name="🆔 ID",
            value=f"`{guild.id}`",
            inline=True
        )
        embed.add_field(
            name="📅 Créé le",
            value=f"<t:{int(guild.created_at.timestamp())}:F>",
            inline=False
        )

        # Statistiques des membres
        online_count = sum(
            1 for member in guild.members if member.status != discord.Status.offline)
        embed.add_field(
            name="👥 Membres",
            value=f"**Total:** {guild.member_count}\n**En ligne:** {online_count}",
            inline=True
        )

        # Canaux
        embed.add_field(
            name="📝 Canaux",
            value=f"**Texte:** {len(guild.text_channels)}\n**Vocal:** {len(guild.voice_channels)}\n**Catégories:** {len(guild.categories)}",
            inline=True
        )

        # Rôles et emojis
        embed.add_field(
            name="🎭 Autres",
            value=f"**Rôles:** {len(guild.roles)}\n**Émojis:** {len(guild.emojis)}\n**Boost:** Niveau {guild.premium_tier}",
            inline=True
        )

        # Fonctionnalités
        features = []
        if "COMMUNITY" in guild.features:
            features.append("🏘️ Communauté")
        if "PARTNERED" in guild.features:
            features.append("🤝 Partenaire")
        if "VERIFIED" in guild.features:
            features.append("✅ Vérifié")
        if "NEWS" in guild.features:
            features.append("📰 Actualités")
        if "DISCOVERABLE" in guild.features:
            features.append("🔍 Découvrable")

        if features:
            embed.add_field(
                name="✨ Fonctionnalités",
                value="\n".join(features),
                inline=False
            )

        # Niveaux de sécurité
        verification_levels = {
            discord.VerificationLevel.none: "Aucun",
            discord.VerificationLevel.low: "Faible",
            discord.VerificationLevel.medium: "Moyen",
            discord.VerificationLevel.high: "Élevé",
            discord.VerificationLevel.highest: "Maximum"
        }

        embed.add_field(
            name="🔒 Sécurité",
            value=f"**Vérification:** {verification_levels.get(guild.verification_level, 'Inconnu')}\n**Filtre:** {str(guild.explicit_content_filter).replace('_', ' ').title()}",
            inline=True
        )

        embed.set_footer(text=f"Demandé par {interaction.user.display_name}")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="avatar", description="Affiche l'avatar d'un utilisateur")
    @app_commands.describe(user="L'utilisateur dont afficher l'avatar")
    async def avatar_slash(self, interaction: discord.Interaction, user: discord.User = None):
        """Affiche l'avatar d'un utilisateur"""
        if user is None:
            user = interaction.user

        embed = discord.Embed(
            title=f"🖼️ Avatar de {user.display_name}",
            color=discord.Color.purple()
        )

        # Avatar principal
        embed.set_image(url=user.display_avatar.url)

        # Liens de téléchargement
        avatar_formats = ["png", "jpg", "webp"]
        if user.display_avatar.is_animated():
            avatar_formats.append("gif")

        links = [
            f"[{fmt.upper()}]({user.display_avatar.with_format(fmt).url})" for fmt in avatar_formats]

        embed.add_field(
            name="📥 Télécharger",
            value=" • ".join(links),
            inline=False
        )

        embed.set_footer(text=f"Demandé par {interaction.user.display_name}")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="uptime", description="Affiche le temps de fonctionnement du bot")
    async def uptime_slash(self, interaction: discord.Interaction):
        """Affiche l'uptime du bot"""
        current_time = time.time()
        uptime_seconds = int(current_time - self.start_time)

        days = uptime_seconds // 86400
        hours = (uptime_seconds % 86400) // 3600
        minutes = (uptime_seconds % 3600) // 60
        seconds = uptime_seconds % 60

        embed = discord.Embed(
            title="⏰ Temps de fonctionnement",
            color=discord.Color.green()
        )

        uptime_str = ""
        if days > 0:
            uptime_str += f"{days} jour{'s' if days > 1 else ''}, "
        if hours > 0:
            uptime_str += f"{hours} heure{'s' if hours > 1 else ''}, "
        if minutes > 0:
            uptime_str += f"{minutes} minute{'s' if minutes > 1 else ''}, "
        uptime_str += f"{seconds} seconde{'s' if seconds > 1 else ''}"

        embed.add_field(
            name="🚀 Actif depuis",
            value=f"`{uptime_str}`",
            inline=False
        )

        embed.add_field(
            name="📅 Démarré le",
            value=f"<t:{int(self.start_time)}:F>",
            inline=False
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="botinfo", description="Affiche les informations du bot")
    async def botinfo_slash(self, interaction: discord.Interaction):
        """Affiche les informations du bot"""
        embed = discord.Embed(
            title=f"🤖 {self.bot.user.name}",
            description="Bot Discord multifonctionnel avec système de logs avancé",
            color=discord.Color.blue()
        )

        embed.set_thumbnail(url=self.bot.user.display_avatar.url)

        # Statistiques
        embed.add_field(
            name="📊 Statistiques",
            value=f"**Serveurs:** {len(self.bot.guilds)}\n**Utilisateurs:** {len(self.bot.users)}\n**Commandes:** {len(self.bot.commands)}",
            inline=True
        )

        # Système
        embed.add_field(
            name="💻 Système",
            value=f"**Python:** {platform.python_version()}\n**Discord.py:** {discord.__version__}\n**OS:** {platform.system()}",
            inline=True
        )

        # Performance
        process = psutil.Process()
        memory_usage = process.memory_info().rss / 1024 / 1024  # MB
        cpu_usage = process.cpu_percent()

        embed.add_field(
            name="⚡ Performance",
            value=f"**RAM:** {memory_usage:.1f} MB\n**CPU:** {cpu_usage}%\n**Latence:** {round(self.bot.latency * 1000, 2)}ms",
            inline=True
        )

        # Uptime
        current_time = time.time()
        uptime_seconds = int(current_time - self.start_time)
        days = uptime_seconds // 86400
        hours = (uptime_seconds % 86400) // 3600
        minutes = (uptime_seconds % 3600) // 60

        uptime_str = f"{days}j {hours}h {minutes}m"

        embed.add_field(
            name="⏰ Uptime",
            value=f"`{uptime_str}`",
            inline=True
        )

        embed.add_field(
            name="🔗 Liens",
            value="[Panel Admin](http://127.0.0.1:8080) • [Support](https://discord.gg/example)",
            inline=False
        )

        embed.set_footer(
            text=f"Développé avec ❤️ • Demandé par {interaction.user.display_name}")
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    """Fonction pour charger le cog"""
    await bot.add_cog(UtilsSlash(bot))
    print("✅ Module slash/utils chargé")
