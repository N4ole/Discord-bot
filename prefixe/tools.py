"""
Commandes préfixées - Module tools (outils avancés)
"""
import discord
from discord.ext import commands
from datetime import datetime, timedelta
import json
import re
import asyncio


class ToolsPrefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # === COMMANDES D'ANALYSE ===

    @commands.command(name='analyze', aliases=['analyse', 'stats'], help='Analyse un serveur ou un utilisateur')
    @commands.guild_only()
    async def analyze_prefix(self, ctx, *, target: discord.Member = None):
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
            guild = ctx.guild
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

        await ctx.send(embed=embed)

    @commands.command(name='clean', aliases=['purge', 'clear'], help='Supprime des messages selon des critères')
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def clean_prefix(self, ctx, amount: int = 10, *, filters: str = None):
        """Nettoyage avancé des messages

        Exemples:
        !clean 20 - Supprime 20 messages
        !clean 50 user:@John - Supprime 50 messages de John
        !clean 30 contains:spam - Supprime 30 messages contenant 'spam'
        !clean 25 bots - Supprime 25 messages de bots
        """
        if amount < 1 or amount > 100:
            await ctx.send("❌ Le nombre doit être entre 1 et 100 !", delete_after=5)
            return

        # Parser les filtres
        target_user = None
        contains_text = None
        only_bots = False

        if filters:
            filters_lower = filters.lower()

            # Filtre utilisateur
            user_match = re.search(r'user:(<@!?(\d+)>|@?([^@\s]+))', filters)
            if user_match:
                if user_match.group(2):  # Mention d'utilisateur
                    target_user = ctx.guild.get_member(
                        int(user_match.group(2)))
                else:  # Nom d'utilisateur
                    username = user_match.group(3)
                    target_user = discord.utils.find(lambda m: m.name.lower() == username.lower(
                    ) or m.display_name.lower() == username.lower(), ctx.guild.members)

            # Filtre contenu
            contains_match = re.search(r'contains:([^\s]+)', filters)
            if contains_match:
                contains_text = contains_match.group(1)

            # Filtre bots
            if 'bots' in filters_lower:
                only_bots = True

        def check_message(message):
            # Ne pas supprimer les messages épinglés
            if message.pinned:
                return False

            # Filtrage par utilisateur
            if target_user and message.author != target_user:
                return False

            # Filtrage par contenu
            if contains_text and contains_text.lower() not in message.content.lower():
                return False

            # Filtrage bots
            if only_bots and not message.author.bot:
                return False

            return True

        try:
            # +1 pour inclure la commande
            deleted = await ctx.channel.purge(limit=amount + 1, check=check_message)

            # Retirer la commande elle-même du compte si elle était dans les messages supprimés
            if ctx.message in deleted:
                deleted.remove(ctx.message)

            embed = discord.Embed(
                title="🧹 Nettoyage Terminé",
                description=f"**{len(deleted)}** message(s) supprimé(s)",
                color=discord.Color.green(),
                timestamp=datetime.utcnow()
            )

            if target_user:
                embed.add_field(name="👤 Utilisateur",
                                value=target_user.mention, inline=True)
            if contains_text:
                embed.add_field(name="📝 Contenant",
                                value=f"`{contains_text}`", inline=True)
            if only_bots:
                embed.add_field(
                    name="🤖 Type", value="Messages de bots", inline=True)

            embed.add_field(name="🛡️ Modérateur",
                            value=ctx.author.mention, inline=True)

            # Message temporaire
            temp_msg = await ctx.send(embed=embed)
            await asyncio.sleep(5)
            try:
                await temp_msg.delete()
            except:
                pass

        except discord.HTTPException as e:
            await ctx.send(f"❌ Erreur lors du nettoyage: {e}", delete_after=10)

    @commands.command(name='remind', aliases=['reminder', 'rappel'], help='Crée un rappel')
    async def remind_prefix(self, ctx, time: str, *, message: str = "Rappel !"):
        """Système de rappels

        Exemples:
        !remind 10m Réunion dans 10 minutes
        !remind 2h Prendre médicament
        !remind 1d Anniversaire demain
        """
        # Conversion du temps
        time_dict = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}
        time_regex = re.compile(r'(\d+)([smhdw])')
        matches = time_regex.findall(time.lower())

        if not matches:
            await ctx.send("❌ Format de temps invalide ! Utilisez: 10s, 5m, 2h, 1d, 1w", delete_after=10)
            return

        total_seconds = 0
        for amount, unit in matches:
            total_seconds += int(amount) * time_dict[unit]

        if total_seconds < 1:
            await ctx.send("❌ Le temps doit être d'au moins 1 seconde !", delete_after=5)
            return

        if total_seconds > 2592000:  # 30 jours max
            await ctx.send("❌ Le temps maximum est de 30 jours !", delete_after=10)
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

        await ctx.send(embed=embed)

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
            await ctx.author.send(embed=remind_embed)
        except discord.Forbidden:
            pass

        # Envoyer dans le canal
        try:
            await ctx.send(f"{ctx.author.mention}", embed=remind_embed)
        except discord.Forbidden:
            pass

    # === SONDAGES ===

    @commands.command(name='poll', aliases=['sondage', 'vote'], help='Crée un sondage avancé')
    @commands.guild_only()
    async def poll_prefix(self, ctx, duration: str = None, *, question_and_options: str):
        """Crée un sondage avec réactions

        Format: !poll [durée] "Question" option1,option2,option3...

        Exemples:
        !poll "Quel est votre plat préféré ?" Pizza,Burger,Sushi
        !poll 30m "Film ce soir ?" Action,Comédie,Horreur
        """
        # Parser la durée si fournie
        duration_minutes = None
        if duration and re.match(r'\d+[mhd]', duration):
            time_dict = {"m": 1, "h": 60, "d": 1440}
            match = re.match(r'(\d+)([mhd])', duration)
            if match:
                amount, unit = match.groups()
                duration_minutes = int(amount) * time_dict[unit]
                if duration_minutes > 10080:  # 1 semaine max
                    await ctx.send("❌ Durée maximale: 1 semaine (10080 minutes) !", delete_after=5)
                    return
        else:
            # Pas de durée, réintégrer dans la question
            if duration:
                question_and_options = f"{duration} {question_and_options}"

        # Parser la question et les options
        # Format: "Question" option1,option2,option3
        question_match = re.match(r'"([^"]+)"\s*(.+)', question_and_options)
        if question_match:
            question = question_match.group(1)
            options_text = question_match.group(2)
        else:
            # Pas de guillemets, prendre tout avant la première virgule comme question
            parts = question_and_options.split(',', 1)
            if len(parts) < 2:
                await ctx.send('❌ Format: `!poll [durée] "Question" option1,option2,option3`', delete_after=10)
                return
            question = parts[0].strip()
            options_text = parts[1]

        # Parser les options
        option_list = [opt.strip()
                       for opt in options_text.split(',') if opt.strip()]

        if len(option_list) < 2:
            await ctx.send("❌ Il faut au moins 2 options !", delete_after=5)
            return

        if len(option_list) > 10:
            await ctx.send("❌ Maximum 10 options !", delete_after=5)
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
                        value=ctx.author.mention, inline=True)

        if duration_minutes:
            end_time = datetime.utcnow() + timedelta(minutes=duration_minutes)
            embed.add_field(
                name="⏰ Se termine", value=f"<t:{int(end_time.timestamp())}:R>", inline=True)
        else:
            embed.add_field(name="⏰ Durée", value="Illimitée", inline=True)

        embed.set_footer(text="Cliquez sur les réactions pour voter !")

        message = await ctx.send(embed=embed)

        # Ajouter les réactions
        for i in range(len(option_list)):
            await message.add_reaction(emojis[i])

        # Si durée définie, programmer la fermeture
        if duration_minutes:
            await asyncio.sleep(duration_minutes * 60)

            # Récupérer le message mis à jour
            try:
                updated_message = await ctx.channel.fetch_message(message.id)

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

                await ctx.send(embed=result_embed)

            except discord.NotFound:
                pass  # Message supprimé

    @commands.command(name='count', aliases=['wc'], help='Compte les caractères, mots et lignes')
    async def count_prefix(self, ctx, *, text: str):
        """Compte les statistiques d'un texte"""
        lines = text.split('\n')
        words = text.split()
        chars = len(text)
        chars_no_space = len(text.replace(
            ' ', '').replace('\n', '').replace('\t', ''))

        embed = discord.Embed(
            title="📊 Statistiques du Texte",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )

        embed.add_field(name="📝 Caractères", value=f"{chars:,}", inline=True)
        embed.add_field(name="🔤 Caractères (sans espaces)",
                        value=f"{chars_no_space:,}", inline=True)
        embed.add_field(name="📖 Mots", value=f"{len(words):,}", inline=True)
        embed.add_field(name="📄 Lignes", value=f"{len(lines):,}", inline=True)

        # Aperçu du texte
        preview = text[:100] + "..." if len(text) > 100 else text
        embed.add_field(name="👁️ Aperçu",
                        value=f"```{preview}```", inline=False)

        await ctx.send(embed=embed)


async def setup(bot):
    """Fonction pour charger le cog"""
    await bot.add_cog(ToolsPrefix(bot))
    print("✅ Module prefixe/tools chargé")
