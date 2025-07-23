"""
Commandes de divertissement slash pour le bot Discord
"""
import discord
from discord import app_commands
from discord.ext import commands
import random
import asyncio
from typing import Literal


class FunSlash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="coinflip", description="Lance une pièce")
    async def coinflip_slash(self, interaction: discord.Interaction):
        """Lance une pièce"""
        result = random.choice(["Pile", "Face"])
        emoji = "🪙" if result == "Pile" else "🌟"

        embed = discord.Embed(
            title="🪙 Lancer de pièce",
            description=f"{emoji} **{result}** !",
            color=discord.Color.gold()
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="8ball", description="Pose une question à la boule magique")
    @app_commands.describe(question="La question à poser")
    async def eightball_slash(self, interaction: discord.Interaction, question: str):
        """Boule magique 8-ball"""
        responses = [
            "🟢 Oui, absolument !",
            "🟢 C'est certain !",
            "🟢 Sans aucun doute !",
            "🟢 Oui, définitivement !",
            "🟢 Tu peux compter dessus !",
            "🟡 Probablement oui",
            "🟡 Les signes pointent vers oui",
            "🟡 Réessaie plus tard",
            "🟡 Difficile à dire maintenant",
            "🟡 Concentre-toi et redemande",
            "🔴 Non, absolument pas !",
            "🔴 Ma réponse est non",
            "🔴 Mes sources disent non",
            "🔴 Très douteux",
            "🔴 Ne compte pas dessus"
        ]

        response = random.choice(responses)

        embed = discord.Embed(
            title="🎱 Boule Magique",
            color=discord.Color.purple()
        )

        embed.add_field(
            name="❓ Question",
            value=question,
            inline=False
        )

        embed.add_field(
            name="🔮 Réponse",
            value=response,
            inline=False
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="choose", description="Choisit au hasard entre plusieurs options")
    @app_commands.describe(options="Les options séparées par des virgules")
    async def choose_slash(self, interaction: discord.Interaction, options: str):
        """Choisit au hasard entre plusieurs options"""
        choices = [choice.strip()
                   for choice in options.split(',') if choice.strip()]

        if len(choices) < 2:
            await interaction.response.send_message("❌ Veuillez fournir au moins 2 options séparées par des virgules!", ephemeral=True)
            return

        if len(choices) > 20:
            await interaction.response.send_message("❌ Maximum 20 options autorisées!", ephemeral=True)
            return

        chosen = random.choice(choices)

        embed = discord.Embed(
            title="🎯 Choix aléatoire",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="📝 Options",
            value="\n".join([f"• {choice}" for choice in choices]),
            inline=False
        )

        embed.add_field(
            name="🎲 Choix",
            value=f"**{chosen}**",
            inline=False
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="joke", description="Raconte une blague aléatoire")
    async def joke_slash(self, interaction: discord.Interaction):
        """Raconte une blague"""
        jokes = [
            "Pourquoi les plongeurs plongent-ils toujours en arrière et jamais en avant ? \n*Parce que sinon, ils tombent dans le bateau !* 😂",
            "Qu'est-ce qui est jaune et qui attend ? \n*Jonathan !* 🟡",
            "Que dit un escargot quand il croise une limace ? \n*'Regarde, un nudiste !'* 🐌",
            "Pourquoi les poissons n'aiment pas jouer au tennis ? \n*Parce qu'ils ont peur du filet !* 🎾",
            "Comment appelle-t-on un chat tombé dans un pot de peinture le jour de Noël ? \n*Un chat-mallow !* 🐱",
            "Que dit un informaticien quand il s'ennuie ? \n*'Je me fichier !'* 💻",
            "Pourquoi les développeurs préfèrent-ils le thé au café ? \n*Parce que le café cause trop de Java !* ☕",
            "Comment savoir qu'un développeur a des problèmes sociaux ? \n*Il utilise des espaces au lieu de tabs !* 🤓"
        ]

        joke = random.choice(jokes)

        embed = discord.Embed(
            title="😂 Blague du jour",
            description=joke,
            color=discord.Color.yellow()
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="quote", description="Affiche une citation inspirante")
    async def quote_slash(self, interaction: discord.Interaction):
        """Affiche une citation inspirante"""
        quotes = [
            ("La vie, c'est comme une bicyclette, il faut avancer pour ne pas perdre l'équilibre.", "Albert Einstein"),
            ("Le succès, c'est tomber sept fois et se relever huit.", "Proverbe japonais"),
            ("Il n'y a que deux façons de vivre sa vie : l'une en faisant comme si rien n'était un miracle, l'autre en faisant comme si tout était un miracle.", "Albert Einstein"),
            ("La meilleure façon de prédire l'avenir, c'est de le créer.", "Peter Drucker"),
            ("Ce ne sont pas les années de votre vie qui comptent, c'est la vie dans vos années.", "Abraham Lincoln"),
            ("L'imagination est plus importante que la connaissance.", "Albert Einstein"),
            ("Soyez vous-même, tous les autres sont déjà pris.", "Oscar Wilde"),
            ("Il vaut mieux allumer une bougie que de maudire les ténèbres.",
             "Proverbe chinois")
        ]

        quote, author = random.choice(quotes)

        embed = discord.Embed(
            title="💭 Citation inspirante",
            description=f"*'{quote}'*",
            color=discord.Color.blue()
        )

        embed.set_footer(text=f"— {author}")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="rps", description="Joue à pierre-papier-ciseaux")
    @app_commands.describe(choice="Votre choix")
    async def rps_slash(self, interaction: discord.Interaction, choice: Literal["pierre", "papier", "ciseaux"]):
        """Joue à pierre-papier-ciseaux"""
        choices = ["pierre", "papier", "ciseaux"]
        bot_choice = random.choice(choices)

        emojis = {
            "pierre": "🪨",
            "papier": "📄",
            "ciseaux": "✂️"
        }

        # Déterminer le gagnant
        if choice == bot_choice:
            result = "🤝 Égalité !"
            color = discord.Color.yellow()
        elif (choice == "pierre" and bot_choice == "ciseaux") or \
             (choice == "papier" and bot_choice == "pierre") or \
             (choice == "ciseaux" and bot_choice == "papier"):
            result = "🎉 Vous gagnez !"
            color = discord.Color.green()
        else:
            result = "😞 Vous perdez !"
            color = discord.Color.red()

        embed = discord.Embed(
            title="🎮 Pierre-Papier-Ciseaux",
            description=result,
            color=color
        )

        embed.add_field(
            name="Votre choix",
            value=f"{emojis[choice]} {choice.title()}",
            inline=True
        )

        embed.add_field(
            name="Mon choix",
            value=f"{emojis[bot_choice]} {bot_choice.title()}",
            inline=True
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="compliment", description="Donne un compliment à quelqu'un")
    @app_commands.describe(user="L'utilisateur à complimenter")
    async def compliment_slash(self, interaction: discord.Interaction, user: discord.Member = None):
        """Donne un compliment"""
        if user is None:
            user = interaction.user

        compliments = [
            "est une personne extraordinaire ! ✨",
            "a un sourire qui illumine la journée ! 😊",
            "est quelqu'un de très bienveillant ! 💖",
            "a un coeur en or ! 💛",
            "est une source d'inspiration ! 🌟",
            "apporte de la joie partout où il/elle va ! 🎉",
            "est quelqu'un d'unique et spécial ! 🦄",
            "a une personnalité magnifique ! 🌈",
            "est très intelligent(e) ! 🧠",
            "a beaucoup de talents ! 🎨"
        ]

        compliment = random.choice(compliments)

        embed = discord.Embed(
            title="💖 Compliment",
            description=f"{user.mention} {compliment}",
            color=discord.Color.pink()
        )

        embed.set_thumbnail(url=user.display_avatar.url)
        embed.set_footer(
            text=f"Compliment offert par {interaction.user.display_name}")

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    """Fonction pour charger le cog"""
    await bot.add_cog(FunSlash(bot))
    print("✅ Module slash/fun chargé")
