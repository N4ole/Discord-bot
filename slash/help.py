"""
Commandes slash - Module help (système d'aide)
"""
import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime


class HelpSlash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Affiche l'aide du bot")
    @app_commands.describe(category="Catégorie d'aide à afficher")
    @app_commands.choices(category=[
        app_commands.Choice(name="🏠 Vue d'ensemble", value="overview"),
        app_commands.Choice(name="🛡️ Modération", value="moderation"),
        app_commands.Choice(name="🎭 Rôles", value="roles"),
        app_commands.Choice(name="📊 Logs", value="logs"),
        app_commands.Choice(name="🛠️ Configuration", value="config"),
        app_commands.Choice(name="📋 Informations", value="info"),
        app_commands.Choice(name="🎮 Divertissement", value="fun"),
        app_commands.Choice(name="🔧 Outils Avancés", value="tools"),
        app_commands.Choice(name="⚙️ Utilitaires", value="utils")
    ])
    async def help_slash(self, interaction: discord.Interaction, category: app_commands.Choice[str] = None):
        """Commande slash d'aide"""
        if not category:
            embed = await self.create_overview_embed(interaction)
        else:
            embed = await self.create_category_embed(interaction, category.value)

        await interaction.response.send_message(embed=embed)

    async def create_overview_embed(self, interaction):
        """Crée l'embed d'aperçu général"""
        embed = discord.Embed(
            title="🤖 Aide du Bot Discord",
            description="Bot Discord multi-fonctions avec modération, logs et gestion des rôles",
            color=discord.Color.gold(),
            timestamp=datetime.utcnow()
        )

        embed.set_thumbnail(url=self.bot.user.display_avatar.url)

        # Statistiques rapides
        embed.add_field(
            name="📊 Statistiques",
            value=f"""
            • **Serveurs**: {len(self.bot.guilds)}
            • **Commandes slash**: {len([cmd for cmd in self.bot.tree.walk_commands()])}
            • **Commandes préfixées**: {len(self.bot.commands)}
            • **Uptime**: Actif
            """,
            inline=True
        )

        # Catégories disponibles
        embed.add_field(
            name="📂 Catégories",
            value="""
            🛡️ **Modération** - Ban, kick, mute, clean...
            🎭 **Rôles** - Gestion des rôles
            📊 **Logs** - Système de journalisation
            🛠️ **Configuration** - Préfixes, paramètres
            📋 **Informations** - Stats et infos
            🎮 **Divertissement** - Jeux et fun
            🔧 **Outils Avancés** - Cryptographie, sondages
            ⚙️ **Utilitaires** - Ping, météo, traduction
            """,
            inline=True
        )

        embed.add_field(
            name="💡 Comment utiliser",
            value="""
            • **Commandes slash**: Tapez `/` puis choisissez
            • **Commandes préfixées**: Tapez le préfixe + commande
            • **Mention**: Mentionnez-moi pour de l'aide
            • **Aide détaillée**: `/help <catégorie>`
            """,
            inline=False
        )

        # Panel Web et Support
        embed.add_field(
            name="🌐 Panel Web & Support",
            value="""
            • [🎫 Système de Support](http://127.0.0.1:8080/support) - Créer un ticket d'aide
            • [🎉 Page de Promotion](http://127.0.0.1:8080/promo) - Découvrir le bot
            """,
            inline=False
        )

        embed.set_footer(
            text="💡 Utilisez /help <catégorie> pour plus de détails")
        return embed

    async def create_category_embed(self, interaction, category):
        """Crée l'embed pour une catégorie spécifique"""
        embed = discord.Embed(
            title=f"📖 Aide - {category.title()}",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )

        if category == "moderation":
            embed.description = "Commandes de modération pour maintenir l'ordre sur votre serveur"
            embed.add_field(
                name="🔨 Bannissement",
                value="""
                `/ban <membre> [raison]` - Bannit un membre
                `/unban <user_id> [raison]` - Débannit un utilisateur
                
                **Permission requise**: Bannir des membres
                """,
                inline=False
            )

            embed.add_field(
                name="👢 Expulsion",
                value="""
                `/kick <membre> [raison]` - Expulse un membre
                
                **Permission requise**: Expulser des membres
                """,
                inline=False
            )

            embed.add_field(
                name="🔇 Timeout",
                value="""
                `/mute <membre> [durée] [raison]` - Met en timeout
                `/unmute <membre> [raison]` - Retire le timeout
                
                **Durées**: 10s, 5m, 2h, 1d (max 28 jours)
                **Permission requise**: Modérer les membres
                """,
                inline=False
            )

            embed.add_field(
                name="🧹 Nettoyage",
                value="""
                `/clean <nombre> [utilisateur] [contient] [bots]` - Supprime des messages
                
                **Exemples**:
                • `/clean 20` - Supprime 20 messages
                • `/clean 50 user:@John` - 50 messages de John
                • `/clean 30 contains:spam` - Messages avec "spam"
                
                **Permission requise**: Gérer les messages
                """,
                inline=False
            )

        elif category == "roles":
            embed.description = "Gestion avancée des rôles et permissions"
            embed.add_field(
                name="🎭 Gestion des Rôles",
                value="""
                `/addrole <membre> <rôle>` - Ajoute un rôle
                `/removerole <membre> <rôle>` - Retire un rôle
                `/roles [membre]` - Affiche les rôles
                
                **Permission requise**: Gérer les rôles
                """,
                inline=False
            )

        elif category == "logs":
            embed.description = "Système de journalisation complet pour surveiller votre serveur"
            embed.add_field(
                name="⚙️ Configuration",
                value="""
                `/setlog <canal>` - Définit le canal de logs
                `/logon` - Active les logs
                `/logoff` - Désactive les logs
                `/logstatus` - Vérifie le statut
                
                **Permission requise**: Gérer le serveur
                """,
                inline=False
            )

            embed.add_field(
                name="📊 Événements Surveillés",
                value="""
                • Messages (suppression, modification)
                • Membres (arrivée, départ, rôles)
                • Vocal (connexion, déconnexion)
                • Modération (ban, unban)
                • Canaux (création, suppression)
                """,
                inline=False
            )

        elif category == "config":
            embed.description = "Configuration et personnalisation du bot"
            embed.add_field(
                name="🛠️ Préfixes",
                value="""
                `/prefix` - Affiche le préfixe actuel
                Commandes préfixées uniquement:
                `!prefix set <nouveau>` - Change le préfixe
                `!prefix reset` - Remet par défaut
                
                **Permission requise**: Gérer le serveur
                """,
                inline=False
            )

        elif category == "info":
            embed.description = "Commandes d'information et statistiques"
            embed.add_field(
                name="👤 Utilisateurs",
                value="""
                `/info [membre]` - Informations détaillées
                `/avatar [membre]` - Avatar d'un utilisateur
                `/roles [membre]` - Rôles d'un membre
                """,
                inline=False
            )

            embed.add_field(
                name="🏰 Serveur",
                value="""
                `/server` - Statistiques du serveur
                `/botinfo` - Informations du bot
                `/uptime` - Temps de fonctionnement
                """,
                inline=False
            )

        elif category == "fun":
            embed.description = "Commandes de divertissement et jeux"
            embed.add_field(
                name="🎮 Jeux",
                value="""
                `/coinflip` - Lance une pièce
                `/8ball <question>` - Boule magique
                `/rps <choix>` - Pierre-papier-ciseaux
                `/choose <options>` - Choix aléatoire
                """,
                inline=False
            )

            embed.add_field(
                name="😄 Fun",
                value="""
                `/joke` - Blague aléatoire
                `/quote` - Citation inspirante
                `/compliment [membre]` - Compliment
                """,
                inline=False
            )

        elif category == "tools":
            embed.description = "Outils avancés pour la productivité et l'organisation"
            embed.add_field(
                name="📊 Analyse",
                value="""
                `/analyze [utilisateur]` - Analyse serveur/utilisateur
                """,
                inline=False
            )

            embed.add_field(
                name="🧹 Gestion Messages",
                value="""
                `/clean <nombre> [filtres]` - Nettoyage intelligent
                `/remind <temps> <message>` - Rappels programmés
                """,
                inline=False
            )

            embed.add_field(
                name="🗳️ Communauté",
                value="""
                `/poll <question> <options> [durée]` - Sondages avancés
                """,
                inline=False
            )

        elif category == "utils":
            embed.description = "Utilitaires pratiques et outils de monitoring"
            embed.add_field(
                name="🔧 Monitoring",
                value="""
                `/ping` - Latence du bot
                """,
                inline=False
            )

        embed.set_footer(
            text="💡 Toutes ces commandes sont aussi disponibles en version préfixée")
        return embed


async def setup(bot):
    """Fonction pour charger le cog"""
    await bot.add_cog(HelpSlash(bot))
    print("✅ Module slash/help chargé")
