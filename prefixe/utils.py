"""
Commandes utilitaires préfixées pour le bot Discord
"""
import discord
from discord.ext import commands
from datetime import datetime
import time
import platform
import psutil


class UtilsPrefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()

    @commands.command(name="ping", help="Affiche la latence du bot")
    async def ping_prefix(self, ctx):
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

        await ctx.send(embed=embed)

    @commands.command(name='info', aliases=['user', 'member'], help='Affiche les informations d\'un utilisateur')
    async def userinfo_prefix(self, ctx, user: discord.Member = None):
        """Affiche les informations détaillées d'un utilisateur"""
        if user is None:
            user = ctx.author

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

        if ctx.guild:
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

        embed.set_footer(text=f"Demandé par {ctx.author.display_name}")
        await ctx.send(embed=embed)

    @commands.command(name="avatar", help="Affiche l'avatar d'un utilisateur", aliases=["av", "pfp"])
    async def avatar_prefix(self, ctx, user: discord.User = None):
        """Affiche l'avatar d'un utilisateur"""
        if user is None:
            user = ctx.author

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

        embed.set_footer(text=f"Demandé par {ctx.author.display_name}")
        await ctx.send(embed=embed)

    @commands.command(name="myid", help="Affiche votre ID Discord")
    async def myid_prefix(self, ctx):
        """Commande pour obtenir son ID Discord"""
        user_id = ctx.author.id

        embed = discord.Embed(
            title="🆔 Votre ID Discord",
            description=f"Votre ID Discord est : `{user_id}`",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="📋 Comment utiliser cet ID",
            value="• Pour devenir propriétaire du bot\n"
                  "• Pour la configuration des permissions\n"
                  "• Pour les commandes administratives",
            inline=False
        )

        embed.add_field(
            name="⚙️ Configuration .env",
            value=f"```env\nOWNER_ID={user_id}\n```",
            inline=False
        )

        embed.add_field(
            name="💡 Astuce",
            value="Copiez cet ID dans votre fichier `.env` pour devenir propriétaire du bot",
            inline=False
        )

        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        embed.set_footer(text=f"Demandé par {ctx.author.display_name}")

        await ctx.send(embed=embed)

    @commands.command(name="uptime", help="Affiche le temps de fonctionnement du bot")
    async def uptime_prefix(self, ctx):
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

        await ctx.send(embed=embed)

    @commands.command(name="botinfo", help="Affiche les informations du bot", aliases=["bot", "about"])
    async def botinfo_prefix(self, ctx):
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
        try:
            process = psutil.Process()
            memory_usage = process.memory_info().rss / 1024 / 1024  # MB
            cpu_usage = process.cpu_percent()
        except:
            memory_usage = 0
            cpu_usage = 0

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
            name="🔗 Liens Utiles",
            value="""
            [🎫 Support](http://127.0.0.1:8080/support) • [� Promo](http://127.0.0.1:8080/promo)
            [� Panel Admin](http://127.0.0.1:8080) - Interface complète
            """,
            inline=False
        )

        embed.set_footer(
            text=f"Développé avec ❤️ • Demandé par {ctx.author.display_name}")
        await ctx.send(embed=embed)

    @commands.command(name="support", help="Affiche les liens vers le système de support")
    async def support_prefix(self, ctx):
        """Affiche les informations sur le système de support"""
        embed = discord.Embed(
            title="🎫 Système de Support",
            description="Besoin d'aide ? Utilisez notre système de support intégré !",
            color=discord.Color.blue()
        )

        embed.set_thumbnail(url=self.bot.user.display_avatar.url)

        embed.add_field(
            name="🌐 Panel Web de Support",
            value="[🎫 Créer un Ticket](http://127.0.0.1:8080/support)\n"
                  "Créez un ticket d'aide pour obtenir de l'assistance",
            inline=False
        )

        embed.add_field(
            name="📊 Autres Services Web",
            value="[🎉 Page de Promotion](http://127.0.0.1:8080/promo) - Découvrir le bot\n"
                  "[🏠 Panel Principal](http://127.0.0.1:8080) - Interface d'administration",
            inline=False
        )

        embed.add_field(
            name="💡 Comment utiliser",
            value="1. Cliquez sur le lien **Créer un Ticket**\n"
                  "2. Remplissez le formulaire avec votre problème\n"
                  "3. Attendez une réponse de l'équipe de support\n"
                  "4. Suivez l'évolution de votre ticket",
            inline=False
        )

        embed.add_field(
            name="🔧 Support Direct",
            value=f"Vous pouvez aussi me mentionner {self.bot.user.mention} "
            "ou utiliser les commandes d'aide disponibles !",
            inline=False
        )

        embed.set_footer(text=f"Demandé par {ctx.author.display_name}")
        await ctx.send(embed=embed)

    @commands.command(name="invite", help="Affiche le lien d'invitation du bot")
    async def invite_prefix(self, ctx):
        """Affiche le lien d'invitation du bot"""
        # Permissions recommandées pour le bot
        permissions = discord.Permissions(
            send_messages=True,
            read_messages=True,
            embed_links=True,
            attach_files=True,
            read_message_history=True,
            use_external_emojis=True,
            add_reactions=True,
            manage_messages=True,
            kick_members=True,
            ban_members=True,
            manage_channels=True,
            manage_guild=True,
            view_audit_log=True,
            use_application_commands=True
        )

        invite_url = discord.utils.oauth_url(
            self.bot.user.id,
            permissions=permissions,
            scopes=["bot", "applications.commands"]
        )

        embed = discord.Embed(
            title="🔗 Inviter le bot",
            description="Cliquez sur le lien ci-dessous pour ajouter le bot à votre serveur !",
            color=discord.Color.green()
        )

        embed.add_field(
            name="📝 Lien d'invitation",
            value=f"[Cliquez ici pour inviter le bot]({invite_url})",
            inline=False
        )

        embed.add_field(
            name="⚠️ Permissions",
            value="Le bot demande les permissions nécessaires à son bon fonctionnement. Vous pouvez désactiver certaines permissions si nécessaire.",
            inline=False
        )

        await ctx.send(embed=embed)

    @commands.command(name="roll", help="Lance un ou plusieurs dés", aliases=["dice", "random"])
    async def roll_prefix(self, ctx, dice: str = "1d6"):
        """Lance des dés (format: NbDSides, ex: 2d20)"""
        try:
            if 'd' not in dice.lower():
                await ctx.send("❌ Format invalide ! Utilisez le format `NbDSides` (ex: 2d20, 1d6)")
                return

            nb_dice, sides = dice.lower().split('d')
            nb_dice = int(nb_dice) if nb_dice else 1
            sides = int(sides)

            if nb_dice <= 0 or sides <= 0:
                await ctx.send("❌ Le nombre de dés et de faces doit être positif !")
                return

            if nb_dice > 20:
                await ctx.send("❌ Maximum 20 dés autorisés !")
                return

            if sides > 1000:
                await ctx.send("❌ Maximum 1000 faces par dé !")
                return

            import random
            results = [random.randint(1, sides) for _ in range(nb_dice)]
            total = sum(results)

            embed = discord.Embed(
                title="🎲 Lancer de dés",
                color=discord.Color.gold()
            )

            if nb_dice == 1:
                embed.add_field(
                    name=f"Résultat (1d{sides})",
                    value=f"🎯 **{results[0]}**",
                    inline=False
                )
            else:
                embed.add_field(
                    name=f"Résultats ({nb_dice}d{sides})",
                    value=f"Dés: {', '.join(map(str, results))}\n🎯 **Total: {total}**",
                    inline=False
                )

                embed.add_field(
                    name="📊 Statistiques",
                    value=f"Minimum: {min(results)}\nMaximum: {max(results)}\nMoyenne: {total/nb_dice:.1f}",
                    inline=True
                )

            await ctx.send(embed=embed)

        except ValueError:
            await ctx.send("❌ Format invalide ! Utilisez le format `NbDSides` (ex: 2d20, 1d6)")
        except Exception as e:
            await ctx.send(f"❌ Erreur: {str(e)}")


async def setup(bot):
    """Fonction pour charger le cog"""
    await bot.add_cog(UtilsPrefix(bot))
    print("✅ Module prefixe/utils chargé")
