"""
Engine principal du bot Discord
"""
import discord
from discord.ext import commands
import os
import asyncio
from prefix_manager import get_prefix


class DiscordBot(commands.Bot):
    def __init__(self):
        # Configuration des intents
        intents = discord.Intents.default()
        intents.message_content = True

        # Initialisation du bot avec le système de préfixes dynamiques
        super().__init__(
            command_prefix=get_prefix,
            intents=intents,
            help_command=None
        )

    async def setup_hook(self):
        """Méthode appelée lors de l'initialisation du bot"""
        import time
        start_time = time.time()
        print("Configuration du bot en cours...")

        # Chargement des commandes slash
        print("Chargement des modules slash...")
        await self.load_extension('slash.bonjour')
        await self.load_extension('slash.logs')

        # Chargement des commandes préfixées
        print("Chargement des modules préfixés...")
        await self.load_extension('prefixe.bonjour')
        await self.load_extension('prefixe.prefix')
        await self.load_extension('prefixe.logs')
        
        # Chargement du système d'événements de logs
        print("Chargement du système de logs...")
        await self.load_extension('log_events')

        # Synchronisation des commandes slash
        print("Synchronisation des commandes slash...")
        try:
            sync_start = time.time()
            synced = await self.tree.sync()
            sync_end = time.time()
            print(
                f"{len(synced)} commande(s) slash synchronisée(s) en {sync_end - sync_start:.2f}s")
        except Exception as e:
            print(f"Erreur lors de la synchronisation: {e}")

        end_time = time.time()
        print(f"Configuration terminée en {end_time - start_time:.2f}s")

    async def on_ready(self):
        """Événement déclenché quand le bot est prêt"""
        import time
        print(f'🎉 {self.user} est connecté et prêt à {time.strftime("%H:%M:%S")}!')
        print(f'Bot ID: {self.user.id}')
        print('-------------------')

    async def on_command_error(self, ctx, error):
        """Gestion des erreurs de commandes"""
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("❌ Commande introuvable!")
        else:
            print(f"Erreur: {error}")
            await ctx.send(f"❌ Une erreur s'est produite: {error}")
