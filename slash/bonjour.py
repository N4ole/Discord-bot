"""
Commandes slash - Module bonjour
"""
import discord
from discord import app_commands
from discord.ext import commands


class BonjourSlash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="bonjour", description="Dit bonjour avec une commande slash")
    async def bonjour_slash(self, interaction: discord.Interaction):
        """Commande slash pour dire bonjour"""
        user = interaction.user

        # Création d'un embed pour une réponse plus jolie
        embed = discord.Embed(
            title="👋 Salut !",
            description=f"Bonjour {user.mention} ! Comment ça va ?",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.set_footer(text="Commande slash exécutée avec succès ✨")

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    """Fonction pour charger le cog"""
    await bot.add_cog(BonjourSlash(bot))
    print("✅ Module slash/bonjour chargé")
