"""
Commandes préfixées - Module help (système d'aide)
"""
from bot_owner_manager import is_bot_owner
import discord
from discord.ext import commands
from datetime import datetime
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


class HelpPrefixe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", help="Affiche l'aide du bot")
    async def help_command(self, ctx, *, command: str = None):
        """Affiche l'aide générale ou spécifique à une commande"""
        if command:
            # Aide spécifique à une commande
            cmd = self.bot.get_command(command)
            if cmd:
                embed = discord.Embed(
                    title=f"📖 Aide - {cmd.name}",
                    description=cmd.help or "Aucune description disponible",
                    color=discord.Color.blue(),
                    timestamp=datetime.utcnow()
                )

                embed.add_field(
                    name="📝 Usage",
                    value=f"`{ctx.prefix}{cmd.name} {cmd.signature}`",
                    inline=False
                )

                if cmd.aliases:
                    embed.add_field(
                        name="🔄 Aliases",
                        value=", ".join(
                            [f"`{alias}`" for alias in cmd.aliases]),
                        inline=False
                    )

                await ctx.send(embed=embed)
            else:
                await ctx.send(f"❌ Commande `{command}` introuvable.")
        else:
            # Aide générale
            embed = await self.create_main_help_embed(ctx)
            await ctx.send(embed=embed)

    async def create_main_help_embed(self, ctx):
        """Crée l'embed d'aide principal"""
        embed = discord.Embed(
            title="🤖 Aide du Bot Discord",
            description=f"Voici toutes les commandes disponibles. Préfixe actuel: `{ctx.prefix}`",
            color=discord.Color.gold(),
            timestamp=datetime.utcnow()
        )

        embed.set_thumbnail(url=self.bot.user.display_avatar.url)

        # Commandes générales
        embed.add_field(
            name="💬 Commandes Générales",
            value="""
            `{0}help` - Affiche cette aide
            `{0}bonjour` - Dit bonjour
            """.format(ctx.prefix),
            inline=False
        )

        # Gestion des préfixes
        embed.add_field(
            name="🛠️ Gestion du Préfixe",
            value="""
            `{0}prefix` - Gère le préfixe du bot
            `{0}prefix set <nouveau>` - Change le préfixe (Gérer le serveur)
            `{0}prefix reset` - Remet le préfixe par défaut
            `{0}prefix info` - Infos sur les préfixes
            """.format(ctx.prefix),
            inline=False
        )

        # Système de logs
        embed.add_field(
            name="📊 Système de Logs",
            value="""
            `{0}setlog <canal>` - Définit le canal de logs (Gérer le serveur)
            `{0}logon` - Active les logs (Gérer le serveur)
            `{0}logoff` - Désactive les logs (Gérer le serveur)
            `{0}logstatus` - Statut des logs
            `{0}testlog` - Test le système de logs (Gérer le serveur)
            """.format(ctx.prefix),
            inline=False
        )

        # Modération
        embed.add_field(
            name="🛡️ Modération",
            value="""
            `{0}ban <membre> [raison]` - Bannit un membre (Bannir)
            `{0}unban <user_id> [raison]` - Débannit (Bannir)
            `{0}kick <membre> [raison]` - Expulse un membre (Expulser)
            `{0}mute <membre> [durée] [raison]` - Mute (Modérer)
            `{0}unmute <membre> [raison]` - Unmute (Modérer)
            """.format(ctx.prefix),
            inline=False
        )

        # Gestion des rôles
        embed.add_field(
            name="🎭 Gestion des Rôles",
            value="""
            `{0}addrole <membre> <rôle>` - Ajoute un rôle (Gérer les rôles)
            `{0}removerole <membre> <rôle>` - Retire un rôle (Gérer les rôles)
            `{0}roles [membre]` - Affiche les rôles
            """.format(ctx.prefix),
            inline=False
        )

        # Informations
        embed.add_field(
            name="📋 Informations",
            value="""
            `{0}info [membre]` - Infos sur un membre
            `{0}server` - Infos sur le serveur
            `{0}avatar [membre]` - Avatar d'un utilisateur
            `{0}uptime` - Temps de fonctionnement du bot
            `{0}botinfo` - Informations détaillées du bot
            """.format(ctx.prefix),
            inline=False
        )

        # Utilitaires
        embed.add_field(
            name="⚙️ Utilitaires",
            value="""
            `{0}ping` - Latence du bot
            """.format(ctx.prefix),
            inline=False
        )

        # Divertissement
        embed.add_field(
            name="🎮 Divertissement",
            value="""
            `{0}coinflip` - Lance une pièce
            `{0}8ball <question>` - Boule magique
            `{0}rps <choix>` - Pierre-papier-ciseaux
            `{0}choose <options>` - Choix aléatoire
            `{0}joke` - Blague aléatoire
            `{0}quote` - Citation inspirante
            `{0}compliment [membre]` - Compliment
            """.format(ctx.prefix),
            inline=False
        )

        # Outils avancés
        embed.add_field(
            name="🔧 Outils Avancés",
            value="""
            `{0}analyze [utilisateur]` - Analyse serveur/utilisateur
            `{0}clean <nombre> [filtres]` - Nettoyage intelligent
            `{0}remind <temps> <message>` - Rappels programmés
            `{0}poll [durée] "question" options` - Sondages avancés
            `{0}count <texte>` - Statistiques de texte
            """.format(ctx.prefix),
            inline=False
        )

        # Commandes propriétaires (seulement visible par les propriétaires)
        if is_bot_owner(ctx.author.id):
            embed.add_field(
                name="👑 Commandes Propriétaires",
                value=f"""
                `{ctx.prefix}annonce <message>` - Envoie une annonce à tous les propriétaires de serveurs
                """,
                inline=False
            )

        # Footer avec infos utiles
        embed.add_field(
            name="💡 Infos Utiles",
            value=f"""
            • Tu peux aussi me mentionner: {self.bot.user.mention}
            • Commandes slash disponibles: tapez `/`
            • Les permissions sont indiquées entre parenthèses
            • Usage: `{ctx.prefix}help <commande>` pour plus de détails
            """,
            inline=False
        )

        embed.set_footer(
            text=f"Bot créé avec ❤️ • {len(self.bot.commands)} commandes préfixées • {len([cmd for cmd in self.bot.tree.walk_commands()])} commandes slash")

        return embed


async def setup(bot):
    """Fonction pour charger le cog"""
    await bot.add_cog(HelpPrefixe(bot))
    print("✅ Module prefixe/help chargé")
