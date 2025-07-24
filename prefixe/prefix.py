"""
Commandes préfixées - Module préfixe (gestion des préfixes)
"""
import discord
from discord.ext import commands
from core.prefix_manager import prefix_manager


class PrefixeCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="prefix", help="Gère le préfixe du bot pour ce serveur", invoke_without_command=True)
    @commands.guild_only()
    async def prefix_group(self, ctx):
        """Commande principale pour la gestion des préfixes"""
        if ctx.guild:
            current_prefix = prefix_manager.get_prefix(ctx.guild.id)

            embed = discord.Embed(
                title="🛠️ Gestion du Préfixe",
                description=f"Préfixe actuel pour ce serveur: `{current_prefix}`",
                color=discord.Color.blue()
            )

            embed.add_field(
                name="📝 Commandes disponibles:",
                value=f"""
                `{current_prefix}prefix set <nouveau_préfixe>` - Change le préfixe
                `{current_prefix}prefix reset` - Remet le préfixe par défaut
                `{current_prefix}prefix info` - Affiche les informations
                """,
                inline=False
            )

            embed.add_field(
                name="ℹ️ Note:",
                value="Tu peux aussi me mentionner comme préfixe !",
                inline=False
            )

            await ctx.send(embed=embed)

    @prefix_group.command(name="set", help="Change le préfixe pour ce serveur")
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def prefix_set(self, ctx, *, new_prefix: str):
        """Change le préfixe pour le serveur actuel"""
        success, message = prefix_manager.set_prefix(ctx.guild.id, new_prefix)

        if success:
            embed = discord.Embed(
                title="✅ Préfixe Modifié",
                description=message,
                color=discord.Color.green()
            )
            embed.add_field(
                name="💡 Conseil",
                value=f"Teste avec: `{new_prefix}bonjour`",
                inline=False
            )
        else:
            embed = discord.Embed(
                title="❌ Erreur",
                description=message,
                color=discord.Color.red()
            )

        await ctx.send(embed=embed)

    @prefix_group.command(name="reset", help="Remet le préfixe par défaut")
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def prefix_reset(self, ctx):
        """Remet le préfixe par défaut pour le serveur"""
        success, message = prefix_manager.reset_prefix(ctx.guild.id)

        if success:
            embed = discord.Embed(
                title="🔄 Préfixe Remis à Zéro",
                description=message,
                color=discord.Color.green()
            )
        else:
            embed = discord.Embed(
                title="❌ Erreur",
                description="Impossible de remettre le préfixe par défaut",
                color=discord.Color.red()
            )

        await ctx.send(embed=embed)

    @prefix_group.command(name="info", help="Affiche les informations sur les préfixes")
    @commands.guild_only()
    async def prefix_info(self, ctx):
        """Affiche des informations sur le système de préfixes"""
        current_prefix = prefix_manager.get_prefix(ctx.guild.id)

        embed = discord.Embed(
            title="📊 Informations sur les Préfixes",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="🎯 Préfixe actuel",
            value=f"`{current_prefix}`",
            inline=True
        )

        embed.add_field(
            name="🏠 Préfixe par défaut",
            value=f"`{prefix_manager.default_prefix}`",
            inline=True
        )

        embed.add_field(
            name="🤖 Mention",
            value=f"{self.bot.user.mention}",
            inline=True
        )

        embed.add_field(
            name="⚙️ Règles",
            value="""
            • Maximum 5 caractères
            • Pas de: @ # ` \\ /
            • Pas d'espaces vides
            """,
            inline=False
        )

        await ctx.send(embed=embed)

    @prefix_set.error
    async def prefix_set_error(self, ctx, error):
        """Gestion des erreurs pour la commande prefix set"""
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="❌ Permissions Insuffisantes",
                description="Tu as besoin de la permission `Gérer le serveur` pour changer le préfixe.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            current_prefix = prefix_manager.get_prefix(ctx.guild.id)
            embed = discord.Embed(
                title="❌ Argument Manquant",
                description=f"Usage: `{current_prefix}prefix set <nouveau_préfixe>`",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)


async def setup(bot):
    """Fonction pour charger le cog"""
    await bot.add_cog(PrefixeCommands(bot))
    print("✅ Module prefixe/prefix chargé")
