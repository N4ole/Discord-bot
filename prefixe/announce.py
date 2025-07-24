"""
Commandes préfixées - Module d'annonces (réservé aux propriétaires du bot)
"""
from bot_owner_manager import is_bot_owner
import discord
from discord.ext import commands
import asyncio
from datetime import datetime
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


class AnnouncePrefixe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="annonce", help="Envoie une annonce à tous les propriétaires de serveurs (propriétaires du bot uniquement)")
    async def annonce(self, ctx, *, message: str = None):
        """Envoie un message privé à tous les propriétaires des serveurs où le bot est présent"""

        # Vérifier si l'utilisateur est propriétaire du bot
        if not is_bot_owner(ctx.author.id):
            await ctx.send("❌ Cette commande est réservée aux propriétaires du bot.")
            return

        if not message:
            await ctx.send("❌ Veuillez fournir un message à envoyer.\n"
                           "**Usage:** `!annonce <votre message>`")
            return

        # Message de confirmation avant envoi
        embed = discord.Embed(
            title="🔔 Confirmation d'Annonce",
            description=f"**Message à envoyer:**\n{message}",
            color=0xffa500,
            timestamp=datetime.now()
        )

        # Compter les serveurs et propriétaires uniques
        total_guilds = len(self.bot.guilds)
        unique_owners = set()

        for guild in self.bot.guilds:
            if guild.owner:
                unique_owners.add(guild.owner.id)

        embed.add_field(
            name="📊 Statistiques",
            value=f"• **Serveurs:** {total_guilds}\n"
            f"• **Propriétaires uniques:** {len(unique_owners)}",
            inline=False
        )

        embed.add_field(
            name="⚠️ Attention",
            value="Cette action enverra le message à tous les propriétaires de serveurs.\n"
                  "Réagissez avec ✅ pour confirmer ou ❌ pour annuler.",
            inline=False
        )

        embed.set_footer(
            text="Annonce Bot", icon_url=self.bot.user.avatar.url if self.bot.user.avatar else None)

        confirmation_msg = await ctx.send(embed=embed)

        # Ajouter les réactions
        await confirmation_msg.add_reaction("✅")
        await confirmation_msg.add_reaction("❌")

        def check(reaction, user):
            return (user == ctx.author and
                    str(reaction.emoji) in ["✅", "❌"] and
                    reaction.message.id == confirmation_msg.id)

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)

            if str(reaction.emoji) == "❌":
                await confirmation_msg.edit(embed=discord.Embed(
                    title="❌ Annonce Annulée",
                    description="L'envoi de l'annonce a été annulé.",
                    color=0xff0000
                ))
                return

            # Procéder à l'envoi
            await self.send_announcement(ctx, message, confirmation_msg)

        except asyncio.TimeoutError:
            await confirmation_msg.edit(embed=discord.Embed(
                title="⏰ Délai Expiré",
                description="Aucune réponse reçue. Annonce annulée.",
                color=0x808080
            ))

    async def send_announcement(self, ctx, message, confirmation_msg):
        """Envoie l'annonce à tous les propriétaires de serveurs"""

        # Mettre à jour le message de confirmation
        progress_embed = discord.Embed(
            title="📤 Envoi en Cours...",
            description="Envoi de l'annonce aux propriétaires de serveurs...",
            color=0x00ff00
        )
        await confirmation_msg.edit(embed=progress_embed)

        # Préparer l'embed de l'annonce
        announcement_embed = discord.Embed(
            title="📢 Annonce Officielle",
            description=message,
            color=0x0099ff,
            timestamp=datetime.now()
        )

        announcement_embed.add_field(
            name="🤖 Informations",
            value=f"Cette annonce concerne le bot **{self.bot.user.name}** présent sur votre serveur.",
            inline=False
        )

        announcement_embed.set_footer(
            text=f"Annonce envoyée par {ctx.author} • {self.bot.user.name}",
            icon_url=self.bot.user.avatar.url if self.bot.user.avatar else None
        )

        # Statistiques d'envoi
        sent_count = 0
        failed_count = 0
        skipped_count = 0
        processed_owners = set()

        for guild in self.bot.guilds:
            if not guild.owner:
                continue

            # Éviter d'envoyer plusieurs fois au même propriétaire
            if guild.owner.id in processed_owners:
                skipped_count += 1
                continue

            processed_owners.add(guild.owner.id)

            try:
                # Créer un embed personnalisé pour chaque propriétaire
                personal_embed = announcement_embed.copy()
                personal_embed.add_field(
                    name="🏠 Votre Serveur",
                    value=f"**{guild.name}** ({guild.member_count} membres)",
                    inline=True
                )

                await guild.owner.send(embed=personal_embed)
                sent_count += 1

                # Attendre un peu entre chaque envoi pour éviter le rate limiting
                await asyncio.sleep(1)

            except discord.Forbidden:
                # L'utilisateur a désactivé les MPs ou a bloqué le bot
                failed_count += 1
                continue
            except discord.HTTPException as e:
                # Erreur HTTP (rate limit, etc.)
                failed_count += 1
                print(f"❌ Erreur HTTP lors de l'envoi à {guild.owner}: {e}")
                continue
            except Exception as e:
                # Autres erreurs
                failed_count += 1
                print(
                    f"❌ Erreur inattendue lors de l'envoi à {guild.owner}: {e}")
                continue

        # Résultats finaux
        results_embed = discord.Embed(
            title="✅ Annonce Terminée",
            color=0x00ff00,
            timestamp=datetime.now()
        )

        results_embed.add_field(
            name="📊 Résultats",
            value=f"• **Envoyés:** {sent_count}\n"
            f"• **Échecs:** {failed_count}\n"
            f"• **Ignorés (doublons):** {skipped_count}\n"
            f"• **Total traité:** {len(processed_owners)}",
            inline=False
        )

        if failed_count > 0:
            results_embed.add_field(
                name="⚠️ Note",
                value="Certains envois ont échoué (MPs désactivés, bot bloqué, etc.)",
                inline=False
            )

        results_embed.set_footer(text="Annonce Bot")

        await confirmation_msg.edit(embed=results_embed)

        # Log de l'action
        print(
            f"📢 Annonce envoyée par {ctx.author} ({ctx.author.id}): {sent_count}/{len(processed_owners)} réussie(s)")


async def setup(bot):
    await bot.add_cog(AnnouncePrefixe(bot))
