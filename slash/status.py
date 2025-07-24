"""
Commandes slash pour gérer le système de rotation des statuts
"""

import discord
from discord.ext import commands
from discord import app_commands
import asyncio


class StatusCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="status_info", description="Affiche les informations sur le système de rotation des statuts")
    @app_commands.describe()
    async def status_info(self, interaction: discord.Interaction):
        """Affiche les informations sur le système de rotation des statuts."""
        if not hasattr(self.bot, 'status_rotator') or self.bot.status_rotator is None:
            await interaction.response.send_message("❌ Le système de rotation des statuts n'est pas initialisé.", ephemeral=True)
            return

        rotator = self.bot.status_rotator
        current_info = rotator.get_current_status_info()

        embed = discord.Embed(
            title="🔄 Système de Rotation des Statuts",
            description="Informations sur le système de rotation automatique",
            color=0x3498db
        )

        if current_info:
            embed.add_field(
                name="📊 Statut Actuel",
                value=f"**Nom:** {current_info['name']}\n"
                f"**Type:** {current_info['type']}\n"
                f"**État:** {current_info['status']}\n"
                f"**Position:** {current_info['index'] + 1}/{current_info['total']}",
                inline=False
            )

        embed.add_field(
            name="⚙️ Configuration",
            value=f"**Intervalle:** {rotator.rotation_interval} secondes\n"
            f"**Statuts disponibles:** {len(rotator.statuses)}\n"
            f"**Rotation active:** {'✅ Oui' if rotator.rotation_task and not rotator.rotation_task.done() else '❌ Non'}",
            inline=False
        )

        embed.add_field(
            name="🎯 Statuts Spéciaux",
            value="• 🔧 Maintenance\n• 🆕 Mise à jour\n• ⚠️ Erreur\n• 💤 Veille",
            inline=True
        )

        embed.add_field(
            name="📱 Contrôles",
            value="• `/status_start` - Démarrer\n• `/status_stop` - Arrêter\n• `/status_next` - Suivant\n• `/status_special` - Spécial",
            inline=True
        )

        embed.set_footer(
            text="💡 Seuls les propriétaires du bot peuvent contrôler le système")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="status_start", description="Démarre la rotation automatique des statuts")
    async def status_start(self, interaction: discord.Interaction):
        """Démarre la rotation automatique des statuts."""
        # Vérifier si l'utilisateur est propriétaire du bot
        # Remplacez par vos IDs
        if interaction.user.id not in [882673962778382356]:
            await interaction.response.send_message("❌ Seuls les propriétaires du bot peuvent utiliser cette commande.", ephemeral=True)
            return

        if not hasattr(self.bot, 'status_rotator') or self.bot.status_rotator is None:
            await interaction.response.send_message("❌ Le système de rotation des statuts n'est pas initialisé.", ephemeral=True)
            return

        rotator = self.bot.status_rotator

        if rotator.rotation_task and not rotator.rotation_task.done():
            await interaction.response.send_message("⚠️ La rotation des statuts est déjà active.", ephemeral=True)
            return

        rotator.start_rotation()

        embed = discord.Embed(
            title="✅ Rotation Démarrée",
            description="La rotation automatique des statuts a été démarrée avec succès.",
            color=0x2ecc71
        )
        embed.add_field(
            name="⚙️ Configuration",
            value=f"**Intervalle:** {rotator.rotation_interval} secondes\n**Statuts:** {len(rotator.statuses)} disponibles",
            inline=False
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="status_stop", description="Arrête la rotation automatique des statuts")
    async def status_stop(self, interaction: discord.Interaction):
        """Arrête la rotation automatique des statuts."""
        # Vérifier si l'utilisateur est propriétaire du bot
        # Remplacez par vos IDs
        if interaction.user.id not in [882673962778382356]:
            await interaction.response.send_message("❌ Seuls les propriétaires du bot peuvent utiliser cette commande.", ephemeral=True)
            return

        if not hasattr(self.bot, 'status_rotator') or self.bot.status_rotator is None:
            await interaction.response.send_message("❌ Le système de rotation des statuts n'est pas initialisé.", ephemeral=True)
            return

        rotator = self.bot.status_rotator
        rotator.stop_rotation()

        embed = discord.Embed(
            title="⏹️ Rotation Arrêtée",
            description="La rotation automatique des statuts a été arrêtée.",
            color=0xe74c3c
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="status_next", description="Passe au statut suivant manuellement")
    async def status_next(self, interaction: discord.Interaction):
        """Passe au statut suivant manuellement."""
        # Vérifier si l'utilisateur est propriétaire du bot
        # Remplacez par vos IDs
        if interaction.user.id not in [882673962778382356]:
            await interaction.response.send_message("❌ Seuls les propriétaires du bot peuvent utiliser cette commande.", ephemeral=True)
            return

        if not hasattr(self.bot, 'status_rotator') or self.bot.status_rotator is None:
            await interaction.response.send_message("❌ Le système de rotation des statuts n'est pas initialisé.", ephemeral=True)
            return

        rotator = self.bot.status_rotator

        try:
            await rotator._update_status()
            current_info = rotator.get_current_status_info()

            embed = discord.Embed(
                title="⏭️ Statut Suivant",
                description="Le statut a été mis à jour manuellement.",
                color=0x3498db
            )

            if current_info:
                embed.add_field(
                    name="📊 Nouveau Statut",
                    value=f"**Nom:** {current_info['name']}\n**Type:** {current_info['type']}",
                    inline=False
                )

            await interaction.response.send_message(embed=embed)

        except Exception as e:
            await interaction.response.send_message(f"❌ Erreur lors de la mise à jour du statut: {e}", ephemeral=True)

    @app_commands.command(name="status_special", description="Active un statut spécial temporaire")
    @app_commands.describe(
        type="Type de statut spécial à activer",
        duration="Durée en secondes (optionnel, 0 = permanent)"
    )
    @app_commands.choices(type=[
        app_commands.Choice(name="🔧 Maintenance", value="maintenance"),
        app_commands.Choice(name="🆕 Mise à jour", value="update"),
        app_commands.Choice(name="⚠️ Erreur", value="error"),
        app_commands.Choice(name="💤 Veille", value="offline")
    ])
    async def status_special(self, interaction: discord.Interaction, type: str, duration: int = 0):
        """Active un statut spécial temporaire."""
        # Vérifier si l'utilisateur est propriétaire du bot
        # Remplacez par vos IDs
        if interaction.user.id not in [882673962778382356]:
            await interaction.response.send_message("❌ Seuls les propriétaires du bot peuvent utiliser cette commande.", ephemeral=True)
            return

        if not hasattr(self.bot, 'status_rotator') or self.bot.status_rotator is None:
            await interaction.response.send_message("❌ Le système de rotation des statuts n'est pas initialisé.", ephemeral=True)
            return

        rotator = self.bot.status_rotator

        try:
            # Valider la durée
            if duration < 0:
                duration = 0
            elif duration > 3600:  # Maximum 1 heure
                duration = 3600

            await rotator.set_special_status(type, duration if duration > 0 else None)

            embed = discord.Embed(
                title="🌟 Statut Spécial Activé",
                description=f"Le statut spécial **{type}** a été activé.",
                color=0x9b59b6
            )

            if duration > 0:
                embed.add_field(
                    name="⏰ Durée",
                    value=f"{duration} secondes\n*La rotation normale reprendra automatiquement*",
                    inline=False
                )
            else:
                embed.add_field(
                    name="⏰ Durée",
                    value="Permanent\n*Utilisez `/status_start` pour reprendre la rotation*",
                    inline=False
                )

            await interaction.response.send_message(embed=embed)

        except Exception as e:
            await interaction.response.send_message(f"❌ Erreur lors de l'activation du statut spécial: {e}", ephemeral=True)

    @app_commands.command(name="status_interval", description="Change l'intervalle de rotation des statuts")
    @app_commands.describe(seconds="Nouvel intervalle en secondes (minimum 10)")
    async def status_interval(self, interaction: discord.Interaction, seconds: int):
        """Change l'intervalle de rotation des statuts."""
        # Vérifier si l'utilisateur est propriétaire du bot
        # Remplacez par vos IDs
        if interaction.user.id not in [882673962778382356]:
            await interaction.response.send_message("❌ Seuls les propriétaires du bot peuvent utiliser cette commande.", ephemeral=True)
            return

        if not hasattr(self.bot, 'status_rotator') or self.bot.status_rotator is None:
            await interaction.response.send_message("❌ Le système de rotation des statuts n'est pas initialisé.", ephemeral=True)
            return

        if seconds < 10:
            await interaction.response.send_message("❌ L'intervalle minimum est de 10 secondes.", ephemeral=True)
            return

        if seconds > 3600:
            await interaction.response.send_message("❌ L'intervalle maximum est de 3600 secondes (1 heure).", ephemeral=True)
            return

        rotator = self.bot.status_rotator
        old_interval = rotator.rotation_interval
        rotator.set_rotation_interval(seconds)

        embed = discord.Embed(
            title="⚙️ Intervalle Modifié",
            description="L'intervalle de rotation a été mis à jour.",
            color=0x3498db
        )
        embed.add_field(
            name="🔄 Changement",
            value=f"**Ancien:** {old_interval} secondes\n**Nouveau:** {seconds} secondes",
            inline=False
        )
        embed.add_field(
            name="💡 Note",
            value="Le changement prendra effet au prochain cycle de rotation.",
            inline=False
        )

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(StatusCommands(bot))
