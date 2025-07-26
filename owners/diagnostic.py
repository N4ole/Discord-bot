"""
Commandes de diagnostic réservées aux propriétaires du bot
"""
import discord
from discord.ext import commands
from core.bot_owner_manager import is_bot_owner
import os
import psutil
from datetime import datetime, timedelta


class DiagnosticOwnerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="diag", help="Commandes de diagnostic pour propriétaires", invoke_without_command=True)
    async def diag_group(self, ctx):
        """Commandes de diagnostic réservées aux propriétaires"""
        if not is_bot_owner(ctx.author.id):
            await ctx.send("❌ Ces commandes sont réservées aux propriétaires du bot.")
            return

        embed = discord.Embed(
            title="🔧 Commandes de Diagnostic - Propriétaires",
            description="Outils de diagnostic et de monitoring du bot",
            color=0x3498db
        )

        embed.add_field(
            name="📊 Informations Système",
            value="`!diag system` - Informations système\n"
                  "`!diag bot` - Statistiques du bot\n"
                  "`!diag servers` - Liste des serveurs\n"
                  "`!diag uptime` - Temps de fonctionnement\n"
                  "`!serveur [page]` - Liste détaillée des serveurs\n"
                  "`!link <server_id>` - Lien d'invitation par MP",
            inline=False
        )

        embed.add_field(
            name="🔧 Maintenance",
            value="`!diag sync` - Synchroniser les commandes slash\n"
                  "`!diag reload <module>` - Recharger un module\n"
                  "`!diag cache` - Informations cache",
            inline=False
        )

        await ctx.send(embed=embed)

    @diag_group.command(name='system', aliases=['sys'])
    async def diag_system(self, ctx):
        """Affiche les informations système"""
        if not is_bot_owner(ctx.author.id):
            await ctx.send("❌ Cette commande est réservée aux propriétaires du bot.")
            return

        # Informations système
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        embed = discord.Embed(
            title="🖥️ Informations Système",
            color=0x3498db
        )

        embed.add_field(
            name="💻 CPU",
            value=f"{cpu_percent}% utilisé",
            inline=True
        )

        embed.add_field(
            name="🧠 RAM",
            value=f"{memory.percent}% utilisé\n{memory.used // (1024**3):.1f}GB / {memory.total // (1024**3):.1f}GB",
            inline=True
        )

        embed.add_field(
            name="💾 Disque",
            value=f"{disk.percent}% utilisé\n{disk.used // (1024**3):.1f}GB / {disk.total // (1024**3):.1f}GB",
            inline=True
        )

        embed.add_field(
            name="🐍 Python",
            value=f"Version {os.sys.version.split()[0]}",
            inline=True
        )

        embed.add_field(
            name="📦 Discord.py",
            value=f"Version {discord.__version__}",
            inline=True
        )

        embed.add_field(
            name="🕒 Heure serveur",
            value=datetime.now().strftime("%H:%M:%S"),
            inline=True
        )

        await ctx.send(embed=embed)

    @diag_group.command(name='bot')
    async def diag_bot(self, ctx):
        """Affiche les statistiques du bot"""
        if not is_bot_owner(ctx.author.id):
            await ctx.send("❌ Cette commande est réservée aux propriétaires du bot.")
            return

        # Calcul de l'uptime
        if hasattr(self.bot, 'start_time'):
            uptime = datetime.now() - self.bot.start_time
            # Supprimer les microsecondes
            uptime_str = str(uptime).split('.')[0]
        else:
            uptime_str = "Inconnu"

        embed = discord.Embed(
            title="🤖 Statistiques du Bot",
            color=0x2ecc71
        )

        embed.add_field(
            name="📊 Serveurs",
            value=f"{len(self.bot.guilds)} serveurs connectés",
            inline=True
        )

        embed.add_field(
            name="👥 Utilisateurs",
            value=f"{len(self.bot.users)} utilisateurs visibles",
            inline=True
        )

        embed.add_field(
            name="⏰ Uptime",
            value=uptime_str,
            inline=True
        )

        embed.add_field(
            name="🏓 Latence",
            value=f"{round(self.bot.latency * 1000)}ms",
            inline=True
        )

        embed.add_field(
            name="📡 Statut",
            value="🟢 En ligne" if self.bot.is_ready() else "🔴 Hors ligne",
            inline=True
        )

        # Informations sur les modules chargés
        cogs_count = len(self.bot.cogs)
        embed.add_field(
            name="📦 Modules",
            value=f"{cogs_count} modules chargés",
            inline=True
        )

        await ctx.send(embed=embed)

    @diag_group.command(name='servers', aliases=['guilds'])
    async def diag_servers(self, ctx):
        """Liste les serveurs où le bot est connecté"""
        if not is_bot_owner(ctx.author.id):
            await ctx.send("❌ Cette commande est réservée aux propriétaires du bot.")
            return

        embed = discord.Embed(
            title=f"🏠 Serveurs Connectés ({len(self.bot.guilds)})",
            color=0x3498db
        )

        for guild in self.bot.guilds[:10]:  # Limiter à 10 serveurs
            embed.add_field(
                name=f"📍 {guild.name}",
                value=f"ID: `{guild.id}`\n"
                f"Membres: {guild.member_count}\n"
                f"Propriétaire: {guild.owner.mention if guild.owner else 'Inconnu'}",
                inline=True
            )

        if len(self.bot.guilds) > 10:
            embed.add_field(
                name="📋 Note",
                value=f"... et {len(self.bot.guilds) - 10} autres serveurs",
                inline=False
            )

        await ctx.send(embed=embed)

    @diag_group.command(name='sync')
    async def diag_sync(self, ctx):
        """Synchronise les commandes slash"""
        if not is_bot_owner(ctx.author.id):
            await ctx.send("❌ Cette commande est réservée aux propriétaires du bot.")
            return

        try:
            synced = await self.bot.tree.sync()
            embed = discord.Embed(
                title="✅ Synchronisation Réussie",
                description=f"{len(synced)} commande(s) slash synchronisée(s)",
                color=0x2ecc71
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="❌ Erreur de Synchronisation",
                description=f"Erreur: {str(e)}",
                color=0xe74c3c
            )
            await ctx.send(embed=embed)

    @diag_group.command(name='uptime')
    async def diag_uptime(self, ctx):
        """Affiche le temps de fonctionnement détaillé"""
        if not is_bot_owner(ctx.author.id):
            await ctx.send("❌ Cette commande est réservée aux propriétaires du bot.")
            return

        if not hasattr(self.bot, 'start_time'):
            await ctx.send("❌ L'heure de démarrage n'est pas disponible.")
            return

        now = datetime.now()
        uptime = now - self.bot.start_time

        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        embed = discord.Embed(
            title="⏰ Temps de Fonctionnement",
            color=0x3498db
        )

        embed.add_field(
            name="🚀 Démarré le",
            value=self.bot.start_time.strftime("%d/%m/%Y à %H:%M:%S"),
            inline=False
        )

        embed.add_field(
            name="⏱️ Durée totale",
            value=f"{days} jour(s), {hours}h {minutes}m {seconds}s",
            inline=False
        )

        embed.add_field(
            name="📅 Maintenant",
            value=now.strftime("%d/%m/%Y à %H:%M:%S"),
            inline=False
        )

        await ctx.send(embed=embed)

    @commands.command(name="serveur", aliases=["serveurs", "servers"], help="Liste détaillée des serveurs du bot (propriétaires uniquement)")
    async def serveur_command(self, ctx, page: int = 1):
        """Affiche la liste détaillée des serveurs où le bot est présent"""
        if not is_bot_owner(ctx.author.id):
            await ctx.send("❌ Cette commande est réservée aux propriétaires du bot.")
            return

        guilds = self.bot.guilds
        if not guilds:
            await ctx.send("❌ Le bot n'est présent sur aucun serveur.")
            return

        # Pagination
        per_page = 5
        total_pages = (len(guilds) + per_page - 1) // per_page

        if page < 1 or page > total_pages:
            await ctx.send(f"❌ Page invalide. Utilisez une page entre 1 et {total_pages}.")
            return

        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        page_guilds = guilds[start_idx:end_idx]

        embed = discord.Embed(
            title=f"🌐 Serveurs Discord - Page {page}/{total_pages}",
            description=f"Le bot est présent sur **{len(guilds)}** serveur(s)",
            color=0x3498db
        )

        for guild in page_guilds:
            try:
                # Informations de base
                member_count = guild.member_count or len(guild.members)
                online_count = sum(
                    1 for member in guild.members if member.status != discord.Status.offline)

                # Propriétaire du serveur
                owner_info = "Inconnu"
                if guild.owner:
                    owner_info = f"{guild.owner.display_name} ({guild.owner.name}#{guild.owner.discriminator})"

                # Date de création
                created_at = guild.created_at.strftime("%d/%m/%Y")

                # Date d'arrivée du bot
                bot_member = guild.get_member(self.bot.user.id)
                joined_at = "Inconnue"
                if bot_member and bot_member.joined_at:
                    joined_at = bot_member.joined_at.strftime("%d/%m/%Y")

                # Informations sur les canaux
                text_channels = len(guild.text_channels)
                voice_channels = len(guild.voice_channels)

                # Rôles
                role_count = len(guild.roles) - 1  # -1 pour exclure @everyone

                field_value = (
                    f"**👥 Membres:** {member_count} ({online_count} en ligne)\n"
                    f"**👑 Propriétaire:** {owner_info}\n"
                    f"**📅 Créé le:** {created_at}\n"
                    f"**🤖 Bot arrivé le:** {joined_at}\n"
                    f"**📝 Canaux texte:** {text_channels}\n"
                    f"**🔊 Canaux vocaux:** {voice_channels}\n"
                    f"**🎭 Rôles:** {role_count}\n"
                    f"**🆔 ID:** `{guild.id}`"
                )

                # Émoji pour indiquer le niveau de permissions
                permissions = guild.get_member(
                    self.bot.user.id).guild_permissions
                admin_status = "🛡️" if permissions.administrator else "⚙️"

                embed.add_field(
                    name=f"{admin_status} {guild.name}",
                    value=field_value,
                    inline=False
                )

            except Exception as e:
                embed.add_field(
                    name=f"❌ {guild.name}",
                    value=f"Erreur lors de la récupération des informations: {str(e)[:100]}...",
                    inline=False
                )

        # Statistiques globales
        total_members = sum(guild.member_count or 0 for guild in guilds)
        embed.set_footer(
            text=f"📊 Total: {len(guilds)} serveurs • {total_members} membres • Page {page}/{total_pages}"
        )

        await ctx.send(embed=embed)

    @commands.command(name="link", help="Envoie un lien d'invitation pour un serveur spécifique")
    async def link_server(self, ctx, server_id: int = None):
        """Envoie un lien d'invitation pour un serveur spécifique par MP"""
        if not is_bot_owner(ctx.author.id):
            await ctx.send("❌ Cette commande est réservée aux propriétaires du bot.")
            return

        if server_id is None:
            await ctx.send("❌ Veuillez spécifier l'ID du serveur.\nUtilisation: `!link <server_id>`")
            return

        # Rechercher le serveur
        guild = self.bot.get_guild(server_id)
        if not guild:
            await ctx.send(f"❌ Serveur avec l'ID `{server_id}` introuvable ou le bot n'y est pas présent.")
            return

        try:
            # Chercher un canal où le bot peut créer une invitation
            invite_channel = None

            # Priorité 1: Canal général/système
            if guild.system_channel and guild.system_channel.permissions_for(guild.me).create_instant_invite:
                invite_channel = guild.system_channel
            # Priorité 2: Premier canal texte où le bot peut créer des invitations
            else:
                for channel in guild.text_channels:
                    if channel.permissions_for(guild.me).create_instant_invite:
                        invite_channel = channel
                        break

            if not invite_channel:
                await ctx.send(f"❌ Impossible de créer une invitation pour `{guild.name}`. Le bot n'a pas les permissions nécessaires.")
                return

            # Créer l'invitation
            invite = await invite_channel.create_invite(
                max_age=86400,  # 24 heures
                max_uses=1,     # Une seule utilisation
                unique=True,
                reason=f"Invitation demandée par le propriétaire {ctx.author}"
            )

            # Créer l'embed d'informations
            embed = discord.Embed(
                title="🔗 Lien d'invitation généré",
                description=f"Invitation pour le serveur **{guild.name}**",
                color=0x00ff00,
                timestamp=datetime.utcnow()
            )

            embed.add_field(
                name="📋 Informations du serveur",
                value=f"**Nom:** {guild.name}\n"
                f"**ID:** {guild.id}\n"
                f"**Propriétaire:** {guild.owner.mention if guild.owner else 'Inconnu'}\n"
                f"**Membres:** {guild.member_count}\n"
                f"**Créé le:** {guild.created_at.strftime('%d/%m/%Y à %H:%M')}",
                inline=False
            )

            embed.add_field(
                name="🔗 Lien d'invitation",
                value=f"[Cliquez ici pour rejoindre]({invite.url})\n"
                f"`{invite.url}`",
                inline=False
            )

            embed.add_field(
                name="⚙️ Paramètres de l'invitation",
                value=f"**Expire dans:** 24 heures\n"
                f"**Utilisations max:** 1\n"
                f"**Canal:** {invite_channel.mention}",
                inline=False
            )

            if guild.icon:
                embed.set_thumbnail(url=guild.icon.url)

            embed.set_footer(
                text=f"Demandé par {ctx.author}",
                icon_url=ctx.author.avatar.url if ctx.author.avatar else None
            )

            # Envoyer en MP
            try:
                await ctx.author.send(embed=embed)
                await ctx.send(f"✅ Lien d'invitation pour `{guild.name}` envoyé en message privé.")
            except discord.Forbidden:
                # Si impossible d'envoyer en MP, envoyer dans le canal (avec avertissement)
                await ctx.send("⚠️ Impossible d'envoyer en MP. Voici le lien (supprimez ce message rapidement):")
                await ctx.send(embed=embed)

        except discord.HTTPException as e:
            await ctx.send(f"❌ Erreur lors de la création de l'invitation: {str(e)}")
        except Exception as e:
            await ctx.send(f"❌ Une erreur inattendue s'est produite: {str(e)}")


async def setup(bot):
    await bot.add_cog(DiagnosticOwnerCommands(bot))
