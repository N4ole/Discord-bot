"""
Système d'événements de logs pour Discord
"""
import discord
from discord.ext import commands
from .log_manager import log_manager, LogFormatter
from datetime import datetime


class LogEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_log(self, guild, embed):
        """Envoie un log dans le canal configuré"""
        if not log_manager.is_logging_enabled(guild.id):
            return

        channel_id = log_manager.get_log_channel(guild.id)
        if channel_id:
            try:
                channel = guild.get_channel(channel_id)
                if channel:
                    await channel.send(embed=embed)
            except Exception as e:
                print(f"❌ Erreur envoi log: {e}")

    # === ÉVÉNEMENTS DE MESSAGES ===
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        """Log des messages supprimés"""
        if message.author.bot or not message.guild:
            return

        # Rechercher qui a supprimé le message dans les audit logs
        deleted_by = None
        try:
            # Chercher dans les audit logs récents (dernières 30 secondes)
            import asyncio
            # Petit délai pour que l'audit log soit disponible
            await asyncio.sleep(0.5)

            async for entry in message.guild.audit_logs(
                action=discord.AuditLogAction.message_delete,
                limit=5,  # Regarder les 5 dernières entrées
                oldest_first=False
            ):
                # Vérifier si l'entrée correspond à notre message
                if (entry.target and entry.target.id == message.author.id and
                    entry.extra and hasattr(entry.extra, 'channel') and
                    entry.extra.channel.id == message.channel.id and
                    # L'audit log doit être très récent (dans les 10 dernières secondes)
                        abs((datetime.now() - entry.created_at.replace(tzinfo=None)).total_seconds()) < 10):
                    deleted_by = entry.user
                    break
        except (discord.Forbidden, discord.HTTPException, AttributeError) as e:
            # Si on ne peut pas accéder aux audit logs
            pass

        # Déterminer qui a supprimé le message
        if deleted_by and deleted_by.id != message.author.id:
            suppressed_by_text = f"{deleted_by.mention} ({deleted_by})"
            action_by = f"Supprimé par **{deleted_by.display_name}**"
        elif deleted_by and deleted_by.id == message.author.id:
            suppressed_by_text = f"{message.author.mention} (lui-même)"
            action_by = f"Supprimé par l'**auteur lui-même**"
        else:
            suppressed_by_text = "Auteur lui-même ou inconnu"
            action_by = "Supprimé par l'**auteur** ou raison **inconnue**"

        embed = LogFormatter.create_log_embed(
            title="🗑️ Message Supprimé",
            description=f"**Contenu:** {message.content[:1000] if message.content else '*Aucun contenu texte*'}\n\n{action_by}",
            color=LogFormatter.get_color_for_event("message_delete"),
            user=message.author,
            channel=message.channel,
            extra_fields=[
                {"name": "👤 Auteur du message",
                    "value": f"{message.author.mention}", "inline": True},
                {"name": "🗑️ Supprimé par",
                    "value": suppressed_by_text, "inline": True},
                {"name": "🕐 Créé le",
                    "value": f"<t:{int(message.created_at.timestamp())}:f>", "inline": True}
            ]
        )

        if message.attachments:
            embed.add_field(
                name="📎 Pièces jointes",
                value=f"{len(message.attachments)} fichier(s)",
                inline=True
            )

        # Log simplifié vers le panel web
        from web_panel import log_bot_event
        log_bot_event(
            'INFO',
            f'Message supprimé de {message.author} dans #{message.channel.name}' +
            (f' par {deleted_by}' if deleted_by and deleted_by.id !=
             message.author.id else ''),
            guild_id=message.guild.id,
            guild_name=message.guild.name
        )

        await self.send_log(message.guild, embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        """Log des messages édités"""
        if before.author.bot or not before.guild or before.content == after.content:
            return

        embed = LogFormatter.create_log_embed(
            title="✏️ Message Modifié",
            description=f"**Avant:** {before.content[:500] if before.content else '*Aucun contenu*'}\n\n**Après:** {after.content[:500] if after.content else '*Aucun contenu*'}",
            color=LogFormatter.get_color_for_event("message_edit"),
            user=after.author,
            channel=after.channel
        )

        embed.add_field(
            name="🔗 Lien",
            value=f"[Aller au message]({after.jump_url})",
            inline=True
        )

        await self.send_log(after.guild, embed)

    # === ÉVÉNEMENTS DE MEMBRES ===
    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Log des arrivées de membres"""
        embed = LogFormatter.create_log_embed(
            title="👋 Membre Rejoint",
            description=f"{member.mention} a rejoint le serveur",
            color=LogFormatter.get_color_for_event("join"),
            user=member,
            extra_fields=[
                {"name": "📅 Compte créé",
                    "value": f"<t:{int(member.created_at.timestamp())}:R>", "inline": True},
                {"name": "📊 Membre n°", "value": str(
                    member.guild.member_count), "inline": True}
            ]
        )

        await self.send_log(member.guild, embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Log des départs de membres"""
        embed = LogFormatter.create_log_embed(
            title="👋 Membre Parti",
            description=f"{member.mention} a quitté le serveur",
            color=LogFormatter.get_color_for_event("leave"),
            user=member,
            extra_fields=[
                {"name": "📅 Avait rejoint",
                    "value": f"<t:{int(member.joined_at.timestamp())}:R>" if member.joined_at else "Inconnu", "inline": True},
                {"name": "🎭 Rôles", "value": ", ".join([r.mention for r in member.roles[1:]]) if len(
                    member.roles) > 1 else "Aucun", "inline": False}
            ]
        )

        await self.send_log(member.guild, embed)

    # === ÉVÉNEMENTS VOCAUX ===
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """Log des changements d'état vocal"""
        if member.bot:
            return

        # Connexion à un canal vocal
        if before.channel is None and after.channel is not None:
            embed = LogFormatter.create_log_embed(
                title="🔊 Connexion Vocale",
                description=f"{member.mention} a rejoint {after.channel.mention}",
                color=LogFormatter.get_color_for_event("voice_join"),
                user=member,
                extra_fields=[
                    {"name": "🎤 Canal", "value": after.channel.mention, "inline": True},
                    {"name": "👥 Membres dans le canal", "value": str(
                        len(after.channel.members)), "inline": True}
                ]
            )
            await self.send_log(member.guild, embed)

        # Déconnexion d'un canal vocal
        elif before.channel is not None and after.channel is None:
            embed = LogFormatter.create_log_embed(
                title="🔇 Déconnexion Vocale",
                description=f"{member.mention} a quitté {before.channel.mention}",
                color=LogFormatter.get_color_for_event("voice_leave"),
                user=member,
                extra_fields=[
                    {"name": "🎤 Canal quitté",
                        "value": before.channel.mention, "inline": True}
                ]
            )
            await self.send_log(member.guild, embed)

        # Changement de canal vocal
        elif before.channel != after.channel and before.channel is not None and after.channel is not None:
            embed = LogFormatter.create_log_embed(
                title="🔄 Changement de Canal Vocal",
                description=f"{member.mention} a changé de canal",
                color=LogFormatter.get_color_for_event("voice_move"),
                user=member,
                extra_fields=[
                    {"name": "📤 Ancien canal",
                        "value": before.channel.mention, "inline": True},
                    {"name": "📥 Nouveau canal",
                        "value": after.channel.mention, "inline": True}
                ]
            )
            await self.send_log(member.guild, embed)

    # === ÉVÉNEMENTS DE MODÉRATION ===
    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        """Log des bannissements"""
        embed = LogFormatter.create_log_embed(
            title="🔨 Membre Banni",
            description=f"{user.mention} a été banni du serveur",
            color=LogFormatter.get_color_for_event("ban"),
            user=user
        )

        await self.send_log(guild, embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        """Log des débannissements"""
        embed = LogFormatter.create_log_embed(
            title="🔓 Membre Débanni",
            description=f"{user.mention} a été débanni du serveur",
            color=LogFormatter.get_color_for_event("unban"),
            user=user
        )

        await self.send_log(guild, embed)

    # === ÉVÉNEMENTS DE RÔLES ===
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        """Log des changements de rôles"""
        if before.roles != after.roles:
            added_roles = set(after.roles) - set(before.roles)
            removed_roles = set(before.roles) - set(after.roles)

            if added_roles:
                embed = LogFormatter.create_log_embed(
                    title="➕ Rôle(s) Ajouté(s)",
                    description=f"Rôle(s) ajouté(s) à {after.mention}",
                    color=LogFormatter.get_color_for_event("role_add"),
                    user=after,
                    extra_fields=[
                        {"name": "🎭 Rôles ajoutés", "value": ", ".join(
                            [r.mention for r in added_roles]), "inline": False}
                    ]
                )
                await self.send_log(after.guild, embed)

            if removed_roles:
                embed = LogFormatter.create_log_embed(
                    title="➖ Rôle(s) Retiré(s)",
                    description=f"Rôle(s) retiré(s) de {after.mention}",
                    color=LogFormatter.get_color_for_event("role_remove"),
                    user=after,
                    extra_fields=[
                        {"name": "🎭 Rôles retirés", "value": ", ".join(
                            [r.mention for r in removed_roles]), "inline": False}
                    ]
                )
                await self.send_log(after.guild, embed)

    # === ÉVÉNEMENTS DE CANAUX ===
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        """Log de création de canaux"""
        embed = LogFormatter.create_log_embed(
            title="📝 Canal Créé",
            description=f"Le canal {channel.mention} a été créé",
            color=LogFormatter.get_color_for_event("channel_create"),
            extra_fields=[
                {"name": "📋 Nom", "value": channel.name, "inline": True},
                {"name": "🔖 Type", "value": str(
                    channel.type).title(), "inline": True},
                {"name": "🆔 ID", "value": channel.id, "inline": True}
            ]
        )

        await self.send_log(channel.guild, embed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        """Log de suppression de canaux"""
        embed = LogFormatter.create_log_embed(
            title="🗑️ Canal Supprimé",
            description=f"Le canal **{channel.name}** a été supprimé",
            color=LogFormatter.get_color_for_event("channel_delete"),
            extra_fields=[
                {"name": "📋 Nom", "value": channel.name, "inline": True},
                {"name": "🔖 Type", "value": str(
                    channel.type).title(), "inline": True},
                {"name": "🆔 ID", "value": channel.id, "inline": True}
            ]
        )

        await self.send_log(channel.guild, embed)


async def setup(bot):
    """Fonction pour charger le cog"""
    await bot.add_cog(LogEvents(bot))
    print("✅ Système d'événements de logs chargé")
