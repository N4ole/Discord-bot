"""
Système de rotation du statut d'activité du bot Discord.
Fait défiler automatiquement différents statuts pour garder le bot dynamique.
"""

import discord
import asyncio
import random
import logging
from datetime import datetime

# Configuration du logger pour le status rotator
logger = logging.getLogger('status_rotator')


class StatusRotator:
    def __init__(self, bot):
        self.bot = bot
        self.current_status_index = 0
        self.rotation_task = None
        self.rotation_interval = 60  # Changement toutes les 60 secondes

        # Liste des statuts disponibles avec différents types d'activité
        self.statuses = [
            # Statuts de base
            {"type": discord.ActivityType.watching,
                "name": "les serveurs", "status": discord.Status.online},
            {"type": discord.ActivityType.listening,
                "name": "vos commandes", "status": discord.Status.online},
            {"type": discord.ActivityType.playing,
                "name": "avec les modérateurs", "status": discord.Status.online},

            # Statuts informatifs
            {"type": discord.ActivityType.watching,
                "name": "{guild_count} serveurs", "status": discord.Status.online},
            {"type": discord.ActivityType.listening,
                "name": "{user_count} utilisateurs", "status": discord.Status.online},
            {"type": discord.ActivityType.playing,
                "name": "Tape /help pour l'aide", "status": discord.Status.online},

            # Statuts fonctionnels
            {"type": discord.ActivityType.watching,
                "name": "les logs du serveur", "status": discord.Status.online},
            {"type": discord.ActivityType.listening,
                "name": "les mentions @Summer", "status": discord.Status.online},
            {"type": discord.ActivityType.playing,
                "name": "le modérateur parfait", "status": discord.Status.online},

            # Statuts avec commandes
            {"type": discord.ActivityType.watching,
                "name": "!help | /help", "status": discord.Status.online},
            {"type": discord.ActivityType.listening,
                "name": "les commandes slash", "status": discord.Status.online},
            {"type": discord.ActivityType.playing,
                "name": "avec les permissions", "status": discord.Status.online},

            # Statuts d'outils
            {"type": discord.ActivityType.watching,
                "name": "les analyses /analyze", "status": discord.Status.online},
            {"type": discord.ActivityType.listening,
                "name": "les sondages /poll", "status": discord.Status.online},
            {"type": discord.ActivityType.playing,
                "name": "avec les rappels", "status": discord.Status.online},

            # Statuts de divertissement
            {"type": discord.ActivityType.playing,
                "name": "pierre-papier-ciseaux", "status": discord.Status.online},
            {"type": discord.ActivityType.watching,
                "name": "les blagues /joke", "status": discord.Status.online},
            {"type": discord.ActivityType.listening,
                "name": "vos questions 8ball", "status": discord.Status.online},

            # Statuts temporels
            {"type": discord.ActivityType.watching,
                "name": "l'heure: {time}", "status": discord.Status.online},
            {"type": discord.ActivityType.listening,
                "name": "depuis {uptime}", "status": discord.Status.online},

            # Statuts spéciaux (rares)
            {"type": discord.ActivityType.playing,
                "name": "🤖 Mode IA activé", "status": discord.Status.idle},
            {"type": discord.ActivityType.watching,
                "name": "🛡️ Sécurité maximale", "status": discord.Status.dnd},
            {"type": discord.ActivityType.listening,
                "name": "🔧 Panel web actif", "status": discord.Status.online},
        ]

        # Statuts spéciaux pour certaines occasions
        self.special_statuses = {
            "maintenance": {"type": discord.ActivityType.playing, "name": "🔧 Maintenance en cours", "status": discord.Status.idle},
            "update": {"type": discord.ActivityType.watching, "name": "🆕 Mise à jour disponible", "status": discord.Status.idle},
            "error": {"type": discord.ActivityType.playing, "name": "⚠️ Erreur détectée", "status": discord.Status.dnd},
            "offline": {"type": discord.ActivityType.playing, "name": "💤 Mode veille", "status": discord.Status.idle},
        }

    def start_rotation(self):
        """Démarre la rotation automatique des statuts."""
        if self.rotation_task is None or self.rotation_task.done():
            self.rotation_task = asyncio.create_task(self._rotation_loop())
            print("✅ Rotation des statuts démarrée")

    def stop_rotation(self):
        """Arrête la rotation des statuts."""
        if self.rotation_task and not self.rotation_task.done():
            self.rotation_task.cancel()
            print("🛑 Rotation des statuts arrêtée")

    async def _rotation_loop(self):
        """Boucle principale de rotation des statuts."""
        try:
            while True:
                await self._update_status()
                await asyncio.sleep(self.rotation_interval)
        except asyncio.CancelledError:
            print("🔄 Tâche de rotation annulée")
        except Exception as e:
            print(f"❌ Erreur dans la rotation: {e}")

    async def _update_status(self):
        """Met à jour le statut du bot avec le prochain statut dans la rotation."""
        try:
            # Choisir le statut suivant
            if self.current_status_index >= len(self.statuses):
                self.current_status_index = 0
                # Mélanger la liste de temps en temps pour plus de variété
                if random.randint(1, 5) == 1:  # 20% de chance
                    random.shuffle(self.statuses)

            status_config = self.statuses[self.current_status_index]

            # Formater le nom du statut avec des données dynamiques
            formatted_name = await self._format_status_name(status_config["name"])

            # Créer l'activité
            activity = discord.Activity(
                type=status_config["type"],
                name=formatted_name
            )

            # Mettre à jour le statut
            await self.bot.change_presence(
                activity=activity,
                status=status_config["status"]
            )

            self.current_status_index += 1

            # Log du changement (optionnel, peut être commenté pour réduire le spam)
            # self.log_manager.log("DEBUG", "Status Rotator", f"Statut mis à jour: {formatted_name}")

        except Exception as e:
            print(f"❌ Erreur lors de la mise à jour du statut: {e}")

    async def _format_status_name(self, name_template):
        """Formate le nom du statut avec des données dynamiques."""
        try:
            # Compter les serveurs et utilisateurs
            guild_count = len(self.bot.guilds)
            user_count = sum(
                guild.member_count for guild in self.bot.guilds if guild.member_count)

            # Calculer l'uptime
            if hasattr(self.bot, 'start_time'):
                uptime_seconds = (
                    datetime.now() - self.bot.start_time).total_seconds()
                if uptime_seconds < 3600:  # Moins d'une heure
                    uptime = f"{int(uptime_seconds // 60)}min"
                elif uptime_seconds < 86400:  # Moins d'un jour
                    uptime = f"{int(uptime_seconds // 3600)}h"
                else:  # Plus d'un jour
                    uptime = f"{int(uptime_seconds // 86400)}j"
            else:
                uptime = "???"

            # Heure actuelle
            current_time = datetime.now().strftime("%H:%M")

            # Remplacer les placeholders
            formatted_name = name_template.format(
                guild_count=guild_count,
                user_count=user_count,
                uptime=uptime,
                time=current_time
            )

            return formatted_name

        except Exception as e:
            print(f"⚠️ Erreur de formatage du statut: {e}")
            return name_template  # Retourner le template original en cas d'erreur

    async def set_special_status(self, status_type, duration=None):
        """Définit un statut spécial temporaire."""
        if status_type not in self.special_statuses:
            print(f"⚠️ Statut spécial inconnu: {status_type}")
            return

        # Arrêter la rotation temporairement
        self.stop_rotation()

        try:
            special = self.special_statuses[status_type]
            activity = discord.Activity(
                type=special["type"],
                name=special["name"]
            )

            await self.bot.change_presence(
                activity=activity,
                status=special["status"]
            )

            print(f"🔧 Statut spécial activé: {status_type}")

            # Si une durée est spécifiée, revenir à la rotation normale après
            if duration:
                await asyncio.sleep(duration)
                self.start_rotation()

        except Exception as e:
            print(f"❌ Erreur lors de la définition du statut spécial: {e}")
            # Redémarrer la rotation en cas d'erreur
            self.start_rotation()

    async def clear_special_status(self):
        """Désactive le statut spécial et reprend la rotation normale."""
        try:
            print("🔄 Désactivation du statut spécial et reprise de la rotation...")

            # Reprendre la rotation normale
            self.start_rotation()

            # Optionnel: mettre à jour immédiatement le statut
            await self._update_status()

            print("✅ Statut spécial désactivé, rotation normale reprise")

        except Exception as e:
            print(f"❌ Erreur lors de la désactivation du statut spécial: {e}")

    def set_rotation_interval(self, seconds):
        """Change l'intervalle de rotation."""
        if seconds < 10:  # Minimum 10 secondes pour éviter le spam
            seconds = 10

        self.rotation_interval = seconds
        print(f"⏱️ Intervalle de rotation défini à {seconds} secondes")

    def add_custom_status(self, activity_type, name, status=discord.Status.online):
        """Ajoute un statut personnalisé à la rotation."""
        custom_status = {
            "type": activity_type,
            "name": name,
            "status": status
        }
        self.statuses.append(custom_status)
        print(f"➕ Statut personnalisé ajouté: {name}")

    def remove_status_by_name(self, name):
        """Supprime un statut de la rotation par son nom."""
        original_count = len(self.statuses)
        self.statuses = [s for s in self.statuses if s["name"] != name]
        removed_count = original_count - len(self.statuses)

        if removed_count > 0:
            print(f"➖ Statut supprimé: {name}")
        else:
            print(f"⚠️ Statut non trouvé pour suppression: {name}")

    def get_current_status_info(self):
        """Retourne des informations sur le statut actuel."""
        if self.current_status_index > 0 and self.current_status_index <= len(self.statuses):
            current = self.statuses[self.current_status_index - 1]
            return {
                "name": current["name"],
                "type": current["type"].name,
                "status": current["status"].name,
                "index": self.current_status_index - 1,
                "total": len(self.statuses)
            }
        elif len(self.statuses) > 0:
            # Si nous sommes au début (index 0) ou si pas encore démarré, retourner le premier statut
            current = self.statuses[0]
            return {
                "name": current["name"],
                "type": current["type"].name,
                "status": current["status"].name,
                "index": 0,
                "total": len(self.statuses)
            }
        return None

    def get_status_list(self):
        """Retourne la liste de tous les statuts disponibles."""
        return [
            {
                "index": i,
                "name": status["name"],
                "type": status["type"].name,
                "status": status["status"].name
            }
            for i, status in enumerate(self.statuses)
        ]
