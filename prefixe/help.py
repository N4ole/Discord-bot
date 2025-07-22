"""
Commandes préfixées - Module help (système d'aide)
"""
import discord
from discord.ext import commands
from datetime import datetime


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
            `{0}userinfo [membre]` - Infos sur un membre
            `{0}serverinfo` - Infos sur le serveur
            """.format(ctx.prefix),
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
            text=f"Bot créé avec ❤️ • {len(self.bot.commands)} commandes préfixées")

        return embed


async def setup(bot):
    """Fonction pour charger le cog"""
    await bot.add_cog(HelpPrefixe(bot))
    print("✅ Module prefixe/help chargé")
