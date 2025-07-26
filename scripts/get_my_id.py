"""
[DÉPRÉCIÉ] Utilitaire pour obtenir votre ID Discord

⚠️ ATTENTION: Ce script est maintenant DÉPRÉCIÉ !

🎉 NOUVELLE MÉTHODE (plus simple):
La commande !myid est maintenant intégrée directement dans le bot principal.

✅ Utilisez plutôt:
- Commande préfixe: !myid
- Commande slash: /myid

Ces commandes sont disponibles dès que le bot est en ligne et n'ont pas besoin
d'un script séparé.

---
Script conservé pour compatibilité uniquement.
"""
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Bot temporaire pour obtenir l'ID
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f"✅ Bot connecté : {bot.user}")
    print("📋 Pour obtenir votre ID Discord :")
    print("1. Activez le mode développeur : Discord > Paramètres > Avancé > Mode développeur")
    print("2. Clic droit sur votre profil utilisateur > 'Copier l'ID'")
    print("3. Ajoutez OWNER_ID=votre_id dans le fichier .env")
    print("\n🔍 Vous pouvez aussi envoyer la commande !myid dans un serveur où je suis présent")


@bot.command(name='myid')
async def get_my_id(ctx):
    """Commande pour obtenir votre ID Discord"""
    user_id = ctx.author.id
    await ctx.send(f"🆔 Votre ID Discord est : `{user_id}`\n"
                   f"📝 Ajoutez cette ligne dans votre fichier .env :\n"
                   f"```\nOWNER_ID={user_id}\n```")
    print(f"✅ ID Discord de {ctx.author} : {user_id}")

if __name__ == "__main__":
    token = os.getenv('DISCORD_TOKEN')
    if token:
        print("🤖 Démarrage du bot pour obtenir votre ID...")
        print("💬 Tapez !myid dans Discord pour obtenir votre ID")
        bot.run(token)
    else:
        print("❌ Token Discord non trouvé dans le fichier .env")
