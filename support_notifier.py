"""
Système de notifications Discord pour le support
Envoie des notifications en MP quand un nouveau ticket est créé
"""
import discord
import asyncio
from datetime import datetime


class SupportNotifier:
    def __init__(self, bot_instance=None):
        self.bot = bot_instance
        # Liste des IDs des administrateurs qui recevront les notifications
        self.admin_user_ids = [
            702923932239527978,  # naole77
            854382745252790272,  # Sharox_78
        ]

    def set_bot_instance(self, bot_instance):
        """Définit l'instance du bot Discord"""
        self.bot = bot_instance

    async def send_new_ticket_notification(self, ticket_data):
        """Envoie une notification pour un nouveau ticket à tous les admins"""
        print(
            f"🔍 DEBUG: Début send_new_ticket_notification pour ticket {ticket_data.get('ticket_id', 'N/A')}")

        if not self.bot:
            print("❌ Instance du bot non disponible pour les notifications")
            return False

        print(f"🔍 DEBUG: Bot disponible, is_ready: {self.bot.is_ready()}")

        success_count = 0
        total_admins = len(self.admin_user_ids)

        for admin_id in self.admin_user_ids:
            try:
                # Récupérer l'utilisateur admin
                print(
                    f"🔍 DEBUG: Tentative de récupération de l'utilisateur {admin_id}")
                admin_user = await self.bot.fetch_user(admin_id)
                if not admin_user:
                    print(
                        f"❌ Impossible de trouver l'utilisateur avec l'ID {admin_id}")
                    continue

                print(f"🔍 DEBUG: Utilisateur trouvé: {admin_user.name}")

                # Créer l'embed de notification
                embed = discord.Embed(
                    title="🎫 Nouveau Ticket de Support",
                    description=f"Un nouveau ticket a été créé sur le système de support Summer Bot",
                    color=0xff6b6b,  # Rouge-orange
                    timestamp=datetime.utcnow()
                )

                # Ajouter les détails du ticket
                embed.add_field(
                    name="📋 Sujet",
                    value=ticket_data.get('subject', 'Non spécifié')[:1024],
                    inline=False
                )

                embed.add_field(
                    name="👤 Utilisateur",
                    value=ticket_data.get('username', 'Inconnu'),
                    inline=True
                )

                embed.add_field(
                    name="📧 Email",
                    value=ticket_data.get('email', 'Non spécifié'),
                    inline=True
                )

                embed.add_field(
                    name="🏷️ Catégorie",
                    value=ticket_data.get('category', 'Autre'),
                    inline=True
                )

                embed.add_field(
                    name="⚡ Priorité",
                    value=ticket_data.get('priority', 'medium').upper(),
                    inline=True
                )

                embed.add_field(
                    name="🆔 ID du Ticket",
                    value=f"#{ticket_data.get('ticket_id', 'N/A')}",
                    inline=True
                )

                # Ajouter la description si elle existe
                if ticket_data.get('description'):
                    description = ticket_data['description']
                    if len(description) > 1000:
                        description = description[:1000] + "..."
                    embed.add_field(
                        name="📝 Description",
                        value=description,
                        inline=False
                    )

                # Ajouter le lien vers le panel admin
                embed.add_field(
                    name="🔗 Actions",
                    value="[Voir le ticket dans le panel admin](http://127.0.0.1:8080/admin/tickets)\n[Centre de support](http://127.0.0.1:8080/support)",
                    inline=False
                )

                embed.set_footer(
                    text="Summer Bot - Système de Support",
                    icon_url="https://raw.githubusercontent.com/N4ole/Discord-bot/main/static/logo-bot.jpg"
                )

                # Envoyer le message privé
                print(
                    f"🔍 DEBUG: Tentative d'envoi du message à {admin_user.name}")
                await admin_user.send(embed=embed)
                print(
                    f"✅ Notification envoyée à {admin_user.name} pour le ticket #{ticket_data.get('ticket_id')}")
                success_count += 1

            except discord.NotFound:
                print(f"❌ Utilisateur avec l'ID {admin_id} introuvable")
                continue
            except discord.Forbidden:
                print(
                    f"❌ Impossible d'envoyer un MP à l'utilisateur {admin_id}")
                continue
            except Exception as e:
                print(
                    f"❌ Erreur lors de l'envoi de la notification à {admin_id}: {e}")
                import traceback
                traceback.print_exc()
                continue

        # Retourner le succès si au moins une notification a été envoyée
        print(f"📊 Notifications envoyées: {success_count}/{total_admins}")
        return success_count > 0

    async def send_new_response_notification(self, ticket_data, response_data):
        """Envoie une notification pour une nouvelle réponse à un ticket à tous les admins"""
        if not self.bot:
            print("❌ Instance du bot non disponible pour les notifications")
            return False

        total_admins = len(self.admin_user_ids)
        success_count = 0

        print(
            f"📤 Envoi de notifications de réponse à {total_admins} admin(s)...")

        for admin_id in self.admin_user_ids:
            try:
                # Récupérer l'utilisateur admin
                admin_user = await self.bot.fetch_user(admin_id)
                if not admin_user:
                    print(
                        f"❌ Impossible de trouver l'utilisateur avec l'ID {admin_id}")
                    continue

                # Créer l'embed de notification
                embed = discord.Embed(
                    title="💬 Nouvelle Réponse au Ticket",
                    description=f"Une nouvelle réponse a été ajoutée au ticket #{ticket_data.get('ticket_id')}",
                    color=0x667eea,  # Bleu
                    timestamp=datetime.utcnow()
                )

                embed.add_field(
                    name="📋 Sujet du Ticket",
                    value=ticket_data.get('subject', 'Non spécifié')[:1024],
                    inline=False
                )

                embed.add_field(
                    name="👤 Utilisateur",
                    value=ticket_data.get('username', 'Inconnu'),
                    inline=True
                )

                embed.add_field(
                    name="🆔 ID du Ticket",
                    value=f"#{ticket_data.get('ticket_id', 'N/A')}",
                    inline=True
                )

                # Ajouter la réponse
                if response_data.get('message'):
                    message = response_data['message']
                    if len(message) > 1000:
                        message = message[:1000] + "..."
                    embed.add_field(
                        name="💬 Nouvelle Réponse",
                        value=message,
                        inline=False
                    )

                embed.add_field(
                    name="🔗 Actions",
                    value=f"[Voir le ticket](http://127.0.0.1:8080/support/ticket/{ticket_data.get('ticket_id')})\n[Panel admin](http://127.0.0.1:8080/admin/tickets)",
                    inline=False
                )

                embed.set_footer(
                    text="Summer Bot - Système de Support",
                    icon_url="https://raw.githubusercontent.com/N4ole/Discord-bot/main/static/logo-bot.jpg"
                )

                # Envoyer le message privé
                print(
                    f"🔍 DEBUG: Tentative d'envoi de notification de réponse à {admin_user.name}")
                await admin_user.send(embed=embed)
                print(
                    f"✅ Notification de réponse envoyée à {admin_user.name} pour le ticket #{ticket_data.get('ticket_id')}")
                success_count += 1

            except discord.NotFound:
                print(f"❌ Utilisateur avec l'ID {admin_id} introuvable")
                continue
            except discord.Forbidden:
                print(
                    f"❌ Impossible d'envoyer un MP à l'utilisateur {admin_id}")
                continue
            except Exception as e:
                print(
                    f"❌ Erreur lors de l'envoi de la notification de réponse à {admin_id}: {e}")
                import traceback
                traceback.print_exc()
                continue

        # Retourner le succès si au moins une notification a été envoyée
        print(
            f"📊 Notifications de réponse envoyées: {success_count}/{total_admins}")
        return success_count > 0


# Instance globale du notificateur
support_notifier = SupportNotifier()
