"""
Gestion des mentions du bot et événements généraux
"""
import discord
from discord.ext import commands
from datetime import datetime
import re


class BotMentions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        """Écoute les messages pour détecter les mentions du bot"""
        # Ignore les messages des bots
        if message.author.bot:
            return

        # Ignore les messages sans contenu
        if not message.content:
            return

        # Vérifie si le bot est mentionné
        if self.bot.user in message.mentions:
            # Si c'est juste une mention simple (pas une commande)
            content = message.content.strip()
            bot_mention = self.bot.user.mention

            # Nettoie le message de la mention
            clean_content = re.sub(
                f'<@!?{self.bot.user.id}>', '', content).strip()

            # Si le message ne contient que la mention ou des salutations simples
            greeting_words = ['salut', 'hello', 'bonjour',
                              'hey', 'hi', 'aide', 'help', '?']
            if not clean_content or any(word in clean_content.lower() for word in greeting_words):
                await self.send_mention_help(message)

    async def send_mention_help(self, message):
        """Envoie l'aide quand le bot est mentionné"""
        # Récupère le préfixe pour ce serveur
        # Importer le prefix_manager
        from .prefix_manager import prefix_manager
        prefix = "!"  # défaut
        if message.guild:
            prefix = prefix_manager.get_prefix(message.guild.id)

        embed = discord.Embed(
            title="👋 Salut ! Je suis là pour t'aider !",
            description=f"Tu m'as mentionné, {message.author.mention} ! Voici ce que je peux faire :",
            color=discord.Color.green(),
            timestamp=datetime.utcnow()
        )

        embed.set_thumbnail(url=self.bot.user.display_avatar.url)

        # Commandes principales
        embed.add_field(
            name="🚀 Pour commencer",
            value=f"""
            • `{prefix}help` - Aide complète
            • `/help` - Aide avec menus interactifs
            • `{prefix}bonjour` - Une petite salutation
            """,
            inline=False
        )

        # Modération
        embed.add_field(
            name="🛡️ Modération",
            value=f"""
            • `{prefix}ban` / `/ban` - Bannir un membre
            • `{prefix}kick` / `/kick` - Expulser un membre
            • `{prefix}mute` / `/mute` - Mettre en timeout
            """,
            inline=True
        )

        # Configuration
        embed.add_field(
            name="⚙️ Configuration",
            value=f"""
            • `{prefix}setlog` / `/setlog` - Canal de logs
            • `{prefix}prefix` - Gérer le préfixe
            • `{prefix}logon` / `/logon` - Activer les logs
            """,
            inline=True
        )

        # Infos sur le serveur
        if message.guild:
            embed.add_field(
                name="🏠 Serveur Actuel",
                value=f"""
                • **Préfixe**: `{prefix}`
                • **Membres**: {message.guild.member_count}
                • **Nom**: {message.guild.name}
                """,
                inline=False
            )

        embed.add_field(
            name="💡 Astuce",
            value=f"""
            • Tu peux toujours m'utiliser en me mentionnant : {self.bot.user.mention}
            • Les commandes slash (/) sont disponibles partout
            • Tape `{prefix}help <commande>` pour plus de détails
            """,
            inline=False
        )

        # Lien vers le panel de support
        embed.add_field(
            name="🎫 Support & Panel Web",
            value="""
            • [🎫 Système de Support](http://127.0.0.1:8080/support) - Créer un ticket d'aide
            • [🎉 Page de Promotion](http://127.0.0.1:8080/promo) - Découvrir le bot
            """,
            inline=False
        )

        embed.set_footer(
            text=f"🤖 {len(self.bot.guilds)} serveurs • {len(self.bot.users)} utilisateurs")

        try:
            await message.channel.send(embed=embed)
        except discord.HTTPException:
            # Si l'embed échoue, envoie un message simple
            await message.channel.send(
                f"👋 Salut {message.author.mention} ! "
                f"Utilise `{prefix}help` ou `/help` pour voir toutes mes commandes !"
            )

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """Message quand le bot rejoint un serveur"""
        print(
            f"🎉 Bot ajouté au serveur: {guild.name} (ID: {guild.id}) - {guild.member_count} membres")

        # Essaie de trouver un canal pour envoyer un message de bienvenue
        welcome_channels = ['général', 'general',
                            'accueil', 'welcome', 'bot-commands', 'commands']

        channel = None
        # Cherche un canal avec un nom approprié
        for ch in guild.text_channels:
            if ch.name.lower() in welcome_channels:
                channel = ch
                break

        # Si aucun canal spécifique trouvé, prend le premier canal accessible
        if not channel:
            for ch in guild.text_channels:
                if ch.permissions_for(guild.me).send_messages:
                    channel = ch
                    break

        if channel:
            embed = discord.Embed(
                title="🎉 Merci de m'avoir ajouté !",
                description=f"Salut **{guild.name}** ! Je suis prêt à vous aider !",
                color=discord.Color.green(),
                timestamp=datetime.utcnow()
            )

            embed.set_thumbnail(url=self.bot.user.display_avatar.url)

            embed.add_field(
                name="🚀 Pour commencer",
                value="""
                • `/help` - Menu d'aide interactif
                • `!help` - Aide complète (préfixe par défaut)
                • Mentionnez-moi pour de l'aide rapide !
                """,
                inline=False
            )

            embed.add_field(
                name="⚙️ Configuration recommandée",
                value="""
                1. `/setlog #votre-canal` - Configurez les logs
                2. `/logon` - Activez le système de logs
                3. `!prefix set <nouveau>` - Changez le préfixe si besoin
                """,
                inline=False
            )

            embed.add_field(
                name="🛡️ Permissions recommandées",
                value="""
                • Gérer les messages • Bannir/Expulser des membres
                • Modérer les membres • Gérer les rôles
                • Voir l'historique des messages
                """,
                inline=False
            )

            embed.add_field(
                name="🎫 Panel Web & Support",
                value="""
                • [🎫 Système de Support](http://127.0.0.1:8080/support) - Créer un ticket d'aide
                • [� Page de Promotion](http://127.0.0.1:8080/promo) - Découvrir le bot
                 """,
                inline=False
            )

            embed.set_footer(
                text="💡 Vous pouvez me mentionner à tout moment pour de l'aide !")

            try:
                await channel.send(embed=embed)
            except discord.HTTPException:
                pass

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        """Message quand le bot quitte un serveur"""
        print(f"😢 Bot retiré du serveur: {guild.name} (ID: {guild.id})")


async def setup(bot):
    """Fonction pour charger le cog"""
    await bot.add_cog(BotMentions(bot))
    print("✅ Module mentions et événements chargé")
