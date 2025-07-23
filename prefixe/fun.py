"""
Commandes de divertissement préfixées pour le bot Discord
"""
import discord
from discord.ext import commands
import random
import asyncio


class FunPrefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="coinflip", help="Lance une pièce", aliases=["flip", "coin"])
    async def coinflip_prefix(self, ctx):
        """Lance une pièce"""
        result = random.choice(["Pile", "Face"])
        emoji = "🪙" if result == "Pile" else "🌟"

        embed = discord.Embed(
            title="🪙 Lancer de pièce",
            description=f"{emoji} **{result}** !",
            color=discord.Color.gold()
        )

        await ctx.send(embed=embed)

    @commands.command(name="8ball", help="Pose une question à la boule magique", aliases=["eightball", "8b"])
    async def eightball_prefix(self, ctx, *, question):
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

        await ctx.send(embed=embed)

    @commands.command(name="choose", help="Choisit au hasard entre plusieurs options", aliases=["pick", "select"])
    async def choose_prefix(self, ctx, *, options):
        """Choisit au hasard entre plusieurs options"""
        choices = [choice.strip()
                   for choice in options.split(',') if choice.strip()]

        if len(choices) < 2:
            await ctx.send("❌ Veuillez fournir au moins 2 options séparées par des virgules!")
            return

        if len(choices) > 20:
            await ctx.send("❌ Maximum 20 options autorisées!")
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

        await ctx.send(embed=embed)

    @commands.command(name="joke", help="Raconte une blague aléatoire", aliases=["blague"])
    async def joke_prefix(self, ctx):
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

        await ctx.send(embed=embed)

    @commands.command(name="quote", help="Affiche une citation inspirante", aliases=["citation"])
    async def quote_prefix(self, ctx):
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

        await ctx.send(embed=embed)

    @commands.command(name="rps", help="Joue à pierre-papier-ciseaux", aliases=["ppc", "rocherpapiercisuaux"])
    async def rps_prefix(self, ctx, choice=None):
        """Joue à pierre-papier-ciseaux"""
        if choice is None:
            await ctx.send("❌ Veuillez choisir: `pierre`, `papier` ou `ciseaux`")
            return

        choice = choice.lower()
        valid_choices = ["pierre", "papier",
                         "ciseaux", "rock", "paper", "scissors"]

        if choice not in valid_choices:
            await ctx.send("❌ Choix invalide ! Utilisez: `pierre`, `papier` ou `ciseaux`")
            return

        # Normaliser les choix en anglais vers français
        choice_map = {"rock": "pierre",
                      "paper": "papier", "scissors": "ciseaux"}
        choice = choice_map.get(choice, choice)

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

        await ctx.send(embed=embed)

    @commands.command(name="compliment", help="Donne un compliment à quelqu'un", aliases=["nice"])
    async def compliment_prefix(self, ctx, user: discord.Member = None):
        """Donne un compliment"""
        if user is None:
            user = ctx.author

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
            text=f"Compliment offert par {ctx.author.display_name}")

        await ctx.send(embed=embed)

    @commands.command(name="hug", help="Fait un câlin à quelqu'un", aliases=["calin"])
    async def hug_prefix(self, ctx, user: discord.Member = None):
        """Fait un câlin"""
        if user is None:
            await ctx.send("❌ Mentionnez quelqu'un à qui faire un câlin !")
            return

        if user == ctx.author:
            await ctx.send("🤗 Vous vous faites un auto-câlin ! C'est mignon !")
            return

        hug_gifs = [
            "https://media.tenor.com/images/8b0e1b3a5b3f4e9c8e2b1c0a9d8e7f6g/tenor.gif",
            "https://media.tenor.com/images/1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p/tenor.gif"
        ]

        embed = discord.Embed(
            title="🤗 Câlin !",
            description=f"{ctx.author.mention} fait un gros câlin à {user.mention} !",
            color=discord.Color.pink()
        )

        # Utilisation d'un GIF aléatoire (URLs d'exemple)
        embed.set_image(
            url="https://media1.tenor.com/images/558aded891924269ced2839b14db0e47/tenor.gif")

        await ctx.send(embed=embed)

    @commands.command(name="ascii", help="Génère de l'art ASCII", aliases=["art"])
    async def ascii_prefix(self, ctx, *, text=None):
        """Génère de l'art ASCII simple"""
        if text is None:
            await ctx.send("❌ Veuillez fournir un texte à convertir en ASCII !")
            return

        if len(text) > 10:
            await ctx.send("❌ Le texte ne doit pas dépasser 10 caractères !")
            return

        # Art ASCII simple pour démonstration
        ascii_art = f"""
```
╔══════════════════════════════════════╗
║              {text.upper():^20}              ║
╚══════════════════════════════════════╝
```"""

        embed = discord.Embed(
            title="🎨 Art ASCII",
            description=ascii_art,
            color=discord.Color.blue()
        )

        await ctx.send(embed=embed)


async def setup(bot):
    """Fonction pour charger le cog"""
    await bot.add_cog(FunPrefix(bot))
    print("✅ Module prefixe/fun chargé")
