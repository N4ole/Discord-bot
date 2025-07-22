"""
Commandes préfixées - Module bonjour
"""
import discord
from discord.ext import commands


class BonjourPrefixe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="bonjour", help="Dit bonjour avec une commande préfixée")
    async def bonjour_prefixe(self, ctx):
        """Commande préfixée pour dire bonjour (usage: !bonjour)"""
        user = ctx.author

        # Création d'un embed pour une réponse plus jolie
        embed = discord.Embed(
            title="👋 Salut !",
            description=f"Bonjour {user.mention} ! Ravi de te voir !",
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.set_footer(
            text=f"Commande préfixée exécutée par {user.display_name} 🚀")

        await ctx.send(embed=embed)


async def setup(bot):
    """Fonction pour charger le cog"""
    await bot.add_cog(BonjourPrefixe(bot))
    print("✅ Module prefixe/bonjour chargé")
