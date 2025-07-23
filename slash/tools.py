"""
Commandes slash - Module tools (outils avancés)
"""
import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timedelta
import json
import re
import asyncio


class ToolsSlash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # === COMMANDES D'ANALYSE ===

    @app_commands.command(name="analyze", description="Analyse un serveur ou un utilisateur")
    @app_commands.describe(
        target="Utilisateur à analyser (optionnel, par défaut analysera le serveur)"
    )
    @app_commands.guild_only()
    async def analyze_slash(self, interaction: discord.Interaction, target: discord.Member = None):
        """Analyse détaillée d'un serveur ou utilisateur"""
        if target:
            # Analyse d'utilisateur
            embed = discord.Embed(
                title=f"📊 Analyse de {target.display_name}",
                color=target.color if target.color != discord.Color.default() else discord.Color.blue(),
                timestamp=datetime.utcnow()
            )

            # Activité récente (approximative)
            embed.add_field(
                name="📱 Statut",
                value=f"{target.status}".replace('Status.', '').title(),
                inline=True
            )

            # Ancienneté dans le serveur
            if target.joined_at:
                days_in_server = (datetime.utcnow() -
                                  target.joined_at.replace(tzinfo=None)).days
                embed.add_field(
                    name="📅 Ancienneté",
                    value=f"{days_in_server} jours",
                    inline=True
                )

            # Analyse des rôles
            roles_count = len(target.roles) - 1  # Exclut @everyone
            embed.add_field(name="🎭 Rôles", value=str(
                roles_count), inline=True)

            # Permissions importantes
            perms = []
            if target.guild_permissions.administrator:
                perms.append("👑 Admin")
            if target.guild_permissions.manage_guild:
                perms.append("🛠️ Gérer serveur")
            if target.guild_permissions.ban_members:
                perms.append("🔨 Bannir")
            if target.guild_permissions.kick_members:
                perms.append("👢 Expulser")
            if target.guild_permissions.manage_messages:
                perms.append("📝 Gérer messages")

            if perms:
                embed.add_field(
                    name="🛡️ Permissions clés",
                    value=" • ".join(perms),
                    inline=False
                )

            embed.set_thumbnail(url=target.display_avatar.url)

        else:
            # Analyse du serveur
            guild = interaction.guild
            embed = discord.Embed(
                title=f"📊 Analyse de {guild.name}",
                color=discord.Color.blue(),
                timestamp=datetime.utcnow()
            )

            # Statistiques générales
            total_members = guild.member_count
            bots = len([m for m in guild.members if m.bot])
            humans = total_members - bots

            embed.add_field(name="👥 Membres totaux",
                            value=f"{total_members:,}", inline=True)
            embed.add_field(name="🤖 Bots", value=f"{bots:,}", inline=True)
            embed.add_field(name="👤 Humains", value=f"{humans:,}", inline=True)

            # Analyse des rôles
            roles_with_perms = len(
                [r for r in guild.roles if r.permissions.administrator or r.permissions.manage_guild])
            embed.add_field(name="🎭 Rôles totaux",
                            value=f"{len(guild.roles)}", inline=True)
            embed.add_field(name="🛡️ Rôles avec permissions",
                            value=f"{roles_with_perms}", inline=True)

            # Analyse des canaux
            text_channels = len(guild.text_channels)
            voice_channels = len(guild.voice_channels)
            categories = len(guild.categories)

            embed.add_field(name="📝 Canaux texte",
                            value=f"{text_channels}", inline=True)
            embed.add_field(name="🔊 Canaux vocaux",
                            value=f"{voice_channels}", inline=True)
            embed.add_field(name="📁 Catégories",
                            value=f"{categories}", inline=True)

            # Sécurité
            security_score = 0
            security_items = []

            if guild.verification_level >= discord.VerificationLevel.medium:
                security_score += 2
                security_items.append("✅ Vérification élevée")
            else:
                security_items.append("⚠️ Vérification faible")

            if guild.explicit_content_filter != discord.ContentFilter.disabled:
                security_score += 1
                security_items.append("✅ Filtre de contenu")
            else:
                security_items.append("⚠️ Pas de filtre")

            if guild.default_notifications == discord.NotificationLevel.only_mentions:
                security_score += 1
                security_items.append("✅ Notifications optimisées")

            embed.add_field(
                name=f"🔒 Sécurité ({security_score}/4)",
                value="\n".join(security_items),
                inline=False
            )

            if guild.icon:
                embed.set_thumbnail(url=guild.icon.url)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="clean", description="Supprime des messages selon des critères")
    @app_commands.describe(
        amount="Nombre de messages à vérifier (1-100)",
        user="Supprimer seulement les messages de cet utilisateur",
        contains="Supprimer les messages contenant ce texte",
        bots="Supprimer seulement les messages de bots"
    )
    @app_commands.guild_only()
    async def clean_slash(self, interaction: discord.Interaction, amount: int = 10, user: discord.Member = None, contains: str = None, bots: bool = False):
        """Nettoyage avancé des messages"""
        # Vérification des permissions
        if not interaction.user.guild_permissions.manage_messages:
            embed = discord.Embed(
                title="❌ Permissions Insuffisantes",
                description="Tu as besoin de la permission `Gérer les messages` pour cette commande.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if amount < 1 or amount > 100:
            await interaction.response.send_message("❌ Le nombre doit être entre 1 et 100 !", ephemeral=True)
            return

        # Defer pour avoir plus de temps
        await interaction.response.defer(ephemeral=True)

        def check_message(message):
            # Ne pas supprimer les messages épinglés
            if message.pinned:
                return False

            # Filtrage par utilisateur
            if user and message.author != user:
                return False

            # Filtrage par contenu
            if contains and contains.lower() not in message.content.lower():
                return False

            # Filtrage bots
            if bots and not message.author.bot:
                return False

            return True

        try:
            deleted = await interaction.channel.purge(limit=amount, check=check_message)

            embed = discord.Embed(
                title="🧹 Nettoyage Terminé",
                description=f"**{len(deleted)}** message(s) supprimé(s)",
                color=discord.Color.green(),
                timestamp=datetime.utcnow()
            )

            if user:
                embed.add_field(name="👤 Utilisateur",
                                value=user.mention, inline=True)
            if contains:
                embed.add_field(name="📝 Contenant",
                                value=f"`{contains}`", inline=True)
            if bots:
                embed.add_field(
                    name="🤖 Type", value="Messages de bots", inline=True)

            embed.add_field(name="🛡️ Modérateur",
                            value=interaction.user.mention, inline=True)

            await interaction.followup.send(embed=embed)

            # Message temporaire dans le canal
            if len(deleted) > 0:
                temp_msg = await interaction.channel.send(f"🧹 {len(deleted)} message(s) supprimé(s) par {interaction.user.mention}")
                await asyncio.sleep(5)
                try:
                    await temp_msg.delete()
                except:
                    pass

        except discord.HTTPException as e:
            await interaction.followup.send(f"❌ Erreur lors du nettoyage: {e}")

    @app_commands.command(name="remind", description="Crée un rappel")
    @app_commands.describe(
        time="Temps (ex: 10m, 2h, 1d)",
        message="Message du rappel"
    )
    async def remind_slash(self, interaction: discord.Interaction, time: str, *, message: str = "Rappel !"):
        """Système de rappels"""
        # Conversion du temps
        time_dict = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}
        time_regex = re.compile(r'(\d+)([smhdw])')
        matches = time_regex.findall(time.lower())

        if not matches:
            await interaction.response.send_message("❌ Format de temps invalide ! Utilisez: 10s, 5m, 2h, 1d, 1w", ephemeral=True)
            return

        total_seconds = 0
        for amount, unit in matches:
            total_seconds += int(amount) * time_dict[unit]

        if total_seconds < 1:
            await interaction.response.send_message("❌ Le temps doit être d'au moins 1 seconde !", ephemeral=True)
            return

        if total_seconds > 2592000:  # 30 jours max
            await interaction.response.send_message("❌ Le temps maximum est de 30 jours !", ephemeral=True)
            return

        # Confirmation immédiate
        end_time = datetime.utcnow() + timedelta(seconds=total_seconds)
        embed = discord.Embed(
            title="⏰ Rappel Programmé",
            description=f"Je te rappellerai dans **{time}**",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="📝 Message", value=message, inline=False)
        embed.add_field(name="📅 Rappel prévu",
                        value=f"<t:{int(end_time.timestamp())}:R>", inline=True)
        embed.set_footer(text="Le rappel sera envoyé en MP et ici")

        await interaction.response.send_message(embed=embed)

        # Attendre et envoyer le rappel
        await asyncio.sleep(total_seconds)

        remind_embed = discord.Embed(
            title="⏰ Rappel !",
            description=message,
            color=discord.Color.gold(),
            timestamp=datetime.utcnow()
        )
        remind_embed.add_field(name="⏱️ Programmé il y a",
                               value=time, inline=True)
        remind_embed.set_footer(text="Rappel automatique")

        # Envoyer en MP
        try:
            await interaction.user.send(embed=remind_embed)
        except discord.Forbidden:
            pass

        # Envoyer dans le canal
        try:
            await interaction.channel.send(f"{interaction.user.mention}", embed=remind_embed)
        except discord.Forbidden:
            pass

    # === SONDAGES ===

    @app_commands.command(name="poll", description="Crée un sondage avancé")
    @app_commands.describe(
        question="Question du sondage",
        options="Options séparées par des virgules (max 10)",
        duration="Durée en minutes (optionnel, max 10080 = 1 semaine)"
    )
    async def poll_slash(self, interaction: discord.Interaction, question: str, options: str, duration: int = None):
        """Crée un sondage avec réactions"""
        # Parser les options
        option_list = [opt.strip()
                       for opt in options.split(',') if opt.strip()]

        if len(option_list) < 2:
            await interaction.response.send_message("❌ Il faut au moins 2 options !", ephemeral=True)
            return

        if len(option_list) > 10:
            await interaction.response.send_message("❌ Maximum 10 options !", ephemeral=True)
            return

        # Vérifier la durée
        if duration is not None:
            if duration < 1 or duration > 10080:
                await interaction.response.send_message("❌ La durée doit être entre 1 minute et 1 semaine (10080 minutes) !", ephemeral=True)
                return

        # Émojis pour les réactions
        emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣',
                  '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']

        # Créer l'embed
        embed = discord.Embed(
            title="📊 Sondage",
            description=question,
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )

        # Ajouter les options
        options_text = []
        for i, option in enumerate(option_list):
            options_text.append(f"{emojis[i]} {option}")

        embed.add_field(
            name="🗳️ Options",
            value="\n".join(options_text),
            inline=False
        )

        embed.add_field(name="👤 Créé par",
                        value=interaction.user.mention, inline=True)

        if duration:
            end_time = datetime.utcnow() + timedelta(minutes=duration)
            embed.add_field(
                name="⏰ Se termine", value=f"<t:{int(end_time.timestamp())}:R>", inline=True)
        else:
            embed.add_field(name="⏰ Durée", value="Illimitée", inline=True)

        embed.set_footer(text="Cliquez sur les réactions pour voter !")

        await interaction.response.send_message(embed=embed)
        message = await interaction.original_response()

        # Ajouter les réactions
        for i in range(len(option_list)):
            await message.add_reaction(emojis[i])

        # Si durée définie, programmer la fermeture
        if duration:
            await asyncio.sleep(duration * 60)

            # Récupérer le message mis à jour
            try:
                updated_message = await interaction.channel.fetch_message(message.id)

                # Compter les votes
                results = []
                total_votes = 0

                for i, reaction in enumerate(updated_message.reactions):
                    if str(reaction.emoji) in emojis[:len(option_list)]:
                        vote_count = reaction.count - 1  # -1 pour enlever le vote du bot
                        total_votes += vote_count
                        results.append((option_list[i], vote_count))

                # Créer l'embed des résultats
                result_embed = discord.Embed(
                    title="📊 Sondage Terminé",
                    description=question,
                    color=discord.Color.green(),
                    timestamp=datetime.utcnow()
                )

                if total_votes > 0:
                    results.sort(key=lambda x: x[1], reverse=True)

                    result_text = []
                    for i, (option, votes) in enumerate(results):
                        percentage = (votes / total_votes) * \
                            100 if total_votes > 0 else 0
                        emoji = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "📍"
                        result_text.append(
                            f"{emoji} **{option}**: {votes} vote(s) ({percentage:.1f}%)")

                    result_embed.add_field(
                        name="🏆 Résultats",
                        value="\n".join(result_text),
                        inline=False
                    )
                else:
                    result_embed.add_field(
                        name="😔 Résultats",
                        value="Aucun vote reçu",
                        inline=False
                    )

                result_embed.add_field(
                    name="🗳️ Total des votes", value=str(total_votes), inline=True)
                result_embed.set_footer(text="Sondage automatiquement fermé")

                await interaction.channel.send(embed=result_embed)

            except discord.NotFound:
                pass  # Message supprimé


async def setup(bot):
    """Fonction pour charger le cog"""
    await bot.add_cog(ToolsSlash(bot))
    print("✅ Module slash/tools chargé")
