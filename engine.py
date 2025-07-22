"""
Engine principal du bot Discord
"""
import discord
from discord.ext import commands
import os
import asyncio
from prefix_manager import get_prefix
from web_panel import start_web_panel, log_bot_event, update_bot_stats


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

        # Initialisation du panel web
        self.web_panel_thread = None

    async def setup_hook(self):
        """Méthode appelée lors de l'initialisation du bot"""
        import time
        start_time = time.time()
        print("Configuration du bot en cours...")

        # Chargement des commandes slash
        print("Chargement des modules slash...")
        await self.load_extension('slash.bonjour')
        await self.load_extension('slash.logs')
        await self.load_extension('slash.admin')
        await self.load_extension('slash.admin_roles')
        await self.load_extension('slash.help')

        # Chargement des commandes préfixées
        print("Chargement des modules préfixés...")
        await self.load_extension('prefixe.bonjour')
        await self.load_extension('prefixe.prefix')
        await self.load_extension('prefixe.logs')
        await self.load_extension('prefixe.admin')
        await self.load_extension('prefixe.admin_roles')
        await self.load_extension('prefixe.help')

        # Chargement du système de mentions et événements
        print("Chargement du système de mentions...")
        await self.load_extension('bot_mentions')

        # Chargement du système d'événements de logs
        print("Chargement du système de logs...")
        await self.load_extension('log_events')
        await self.load_extension('multiserver_diagnostic')

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

        # Démarrage du panel web
        print("🌐 Démarrage du panel web...")
        self.web_panel_thread = start_web_panel(
            self, host='127.0.0.1', port=8080)
        log_bot_event('SUCCESS', 'Bot configuré et panel web démarré')

    async def on_ready(self):
        """Événement déclenché quand le bot est prêt"""
        import time
        print(f'🎉 {self.user} est connecté et prêt à {time.strftime("%H:%M:%S")}!')
        print(f'Bot ID: {self.user.id}')
        print(f'🌐 Panel web accessible sur: http://127.0.0.1:8080')
        print(f'📊 Identifiants: admin / admin123')
        print('-------------------')

        # Mettre à jour les statistiques du bot
        update_bot_stats(
            connected_servers=len(self.guilds),
            total_users=len(self.users),
            status='online'
        )
        log_bot_event(
            'SUCCESS', f'Bot connecté - {len(self.guilds)} serveurs, {len(self.users)} utilisateurs')

    async def on_command_error(self, ctx, error):
        """Gestion des erreurs de commandes"""
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("❌ Commande introuvable!")
            log_bot_event('WARNING', f'Commande introuvable: {ctx.message.content}',
                          guild=ctx.guild.name if ctx.guild else 'DM',
                          user=str(ctx.author))
        else:
            print(f"Erreur: {error}")
            await ctx.send(f"❌ Une erreur s'est produite: {error}")
            log_bot_event('ERROR', f'Erreur de commande: {str(error)}',
                          command=ctx.command.name if ctx.command else 'Unknown',
                          error_type=type(error).__name__,
                          guild=ctx.guild.name if ctx.guild else 'DM',
                          user=str(ctx.author))

    async def on_command(self, ctx):
        """Événement déclenché quand une commande est utilisée"""
        log_bot_event('INFO', f'Commande utilisée: {ctx.command.name}',
                      user=str(ctx.author),
                      guild=ctx.guild.name if ctx.guild else 'DM')
        update_bot_stats(command_used=True)
