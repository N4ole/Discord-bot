"""
Engine principal du bot Discord
"""
import discord
from discord.ext import commands
import os
import asyncio
from datetime import datetime
from core.prefix_manager import get_prefix
from web_panel import start_web_panel, log_bot_event, update_bot_stats
from core.status_rotator import StatusRotator


class DiscordBot(commands.Bot):
    def __init__(self):
        # Configuration des intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True  # Nécessaire pour accéder aux informations des membres
        intents.presences = True  # Nécessaire pour voir les statuts en ligne/hors ligne

        # Initialisation du bot avec le système de préfixes dynamiques
        super().__init__(
            command_prefix=get_prefix,
            intents=intents,
            help_command=None
        )

        # Initialisation du panel web et des systèmes
        self.web_panel_thread = None
        self.status_rotator = None
        self.start_time = datetime.now()  # Pour calculer l'uptime

    def run_async_safe(self, coro, timeout=5):
        """Exécute une coroutine de manière sécurisée depuis un thread synchrone"""
        try:
            import asyncio
            import concurrent.futures

            # Utiliser asyncio.run_coroutine_threadsafe pour exécuter dans le loop du bot
            if self.loop and not self.loop.is_closed():
                future = asyncio.run_coroutine_threadsafe(coro, self.loop)
                return future.result(timeout=timeout)
            else:
                return None
        except Exception as e:
            print(f"❌ Erreur lors de l'exécution async safe: {e}")
            return None

    def get_user_info_sync(self, user_id):
        """Récupère les informations d'un utilisateur de manière synchrone pour le web panel"""
        try:
            user_id = int(user_id)

            # Vérifier d'abord dans le cache des propriétaires pré-chargés
            if hasattr(self, 'owner_cache') and user_id in self.owner_cache:
                cached_user = self.owner_cache[user_id]
                return {
                    'id': user_id,
                    'name': cached_user.get('name', f'Utilisateur {user_id}'),
                    'discriminator': cached_user.get('discriminator', ''),
                    'avatar': cached_user.get('avatar'),
                    'found': True
                }

            # Essayer de trouver l'utilisateur dans le cache des utilisateurs du bot
            if hasattr(self, 'users'):
                for user in self.users:
                    if user.id == user_id:
                        avatar_url = None
                        if user.avatar:
                            avatar_url = user.avatar.url
                        return {
                            'id': user_id,
                            'name': user.display_name or user.name,
                            'discriminator': user.discriminator if user.discriminator != '0' else '',
                            'avatar': avatar_url,
                            'found': True
                        }

            # Fallback - utilisateur non trouvé
            return {
                'id': user_id,
                'name': f'Utilisateur {user_id}',
                'discriminator': '',
                'avatar': None,
                'found': False
            }
        except Exception as e:
            print(
                f"❌ Erreur lors de la récupération de l'utilisateur {user_id}: {e}")
            return {
                'id': user_id,
                'name': f'Utilisateur inconnu',
                'discriminator': '',
                'avatar': None,
                'found': False
            }

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
        await self.load_extension('slash.utils')
        await self.load_extension('slash.fun')
        await self.load_extension('slash.tools')
        await self.load_extension('slash.status')

        # Chargement des commandes préfixées
        print("Chargement des modules préfixés...")
        await self.load_extension('prefixe.bonjour')
        await self.load_extension('prefixe.prefix')
        await self.load_extension('prefixe.logs')
        await self.load_extension('prefixe.admin')
        await self.load_extension('prefixe.admin_roles')
        await self.load_extension('prefixe.help')
        await self.load_extension('prefixe.utils')
        await self.load_extension('prefixe.fun')
        await self.load_extension('prefixe.tools')
        await self.load_extension('prefixe.status')
        await self.load_extension('prefixe.announce')
        await self.load_extension('prefixe.addperm')
        await self.load_extension('prefixe.owner_management')
        print("✅ Module prefixe/announce chargé")
        print("✅ Module prefixe/addperm chargé")
        print("✅ Module prefixe/owner_management chargé")

        # Chargement du système de mentions et événements
        print("Chargement du système de mentions...")
        await self.load_extension('core.bot_mentions')

        # Chargement du système d'événements de logs
        print("Chargement du système de logs...")
        await self.load_extension('core.log_events')
        await self.load_extension('scripts.multiserver_diagnostic')

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

        # Initialisation du système de rotation des statuts
        print("🔄 Initialisation du système de rotation des statuts...")
        self.status_rotator = StatusRotator(self)

    async def on_ready(self):
        """Événement déclenché quand le bot est prêt"""
        import time
        print(f'🎉 {self.user} est connecté et prêt à {time.strftime("%H:%M:%S")}!')
        print(f'Bot ID: {self.user.id}')
        print(f'🌐 Panel web accessible sur: http://127.0.0.1:8080')
        print(f'📊 Identifiants: admin / admin123')
        print('-------------------')

        # Pré-charger les utilisateurs propriétaires pour le web panel
        await self.preload_owner_users()

        # Mettre à jour les statistiques du bot
        update_bot_stats(
            connected_servers=len(self.guilds),
            total_users=len(self.users),
            status='online'
        )
        log_bot_event(
            'SUCCESS', f'Bot connecté - {len(self.guilds)} serveurs, {len(self.users)} utilisateurs')

        # Démarrer la rotation des statuts
        if self.status_rotator:
            self.status_rotator.start_rotation()
            print("🔄 Rotation des statuts démarrée")

    async def preload_owner_users(self):
        """Pré-charge les informations des propriétaires pour le web panel"""
        try:
            from core.bot_owner_manager import get_bot_owners
            owners = get_bot_owners()
            print(
                f"🔍 Pré-chargement des informations de {len(owners)} propriétaires...")

            # Initialiser le cache s'il n'existe pas
            if not hasattr(self, 'owner_cache'):
                self.owner_cache = {}

            for owner_id in owners:
                try:
                    user = await self.fetch_user(owner_id)
                    if user:
                        # Stocker les informations dans le cache
                        avatar_url = None
                        if user.avatar:
                            avatar_url = user.avatar.url

                        self.owner_cache[owner_id] = {
                            'name': user.display_name or user.name,
                            'discriminator': user.discriminator if user.discriminator != '0' else '',
                            'avatar': avatar_url
                        }
                        print(
                            f"✅ Propriétaire pré-chargé: {user.name} ({owner_id})")
                    else:
                        print(f"⚠️ Propriétaire {owner_id} non trouvé")
                except Exception as e:
                    print(
                        f"❌ Erreur lors du pré-chargement de {owner_id}: {e}")
                    # Stocker une info basique même en cas d'erreur
                    self.owner_cache[owner_id] = {
                        'name': f'Utilisateur {owner_id}',
                        'discriminator': '',
                        'avatar': None
                    }
        except Exception as e:
            print(f"❌ Erreur lors du pré-chargement des propriétaires: {e}")

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
