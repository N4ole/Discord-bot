"""
Commandes préfixées pour gérer le système de rotation des statuts
"""

import discord
from discord.ext import commands


class StatusPrefixCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='status', aliases=['statut'], invoke_without_command=True)
    async def status_group(self, ctx):
        """Groupe de commandes pour gérer le système de rotation des statuts."""
        if not hasattr(self.bot, 'status_rotator') or self.bot.status_rotator is None:
            await ctx.send("❌ Le système de rotation des statuts n'est pas initialisé.")
            return

        rotator = self.bot.status_rotator
        current_info = rotator.get_current_status_info()

        embed = discord.Embed(
            title="🔄 Système de Rotation des Statuts",
            description="Utilisez `!status help` pour voir toutes les commandes disponibles",
            color=0x3498db
        )

        if current_info:
            embed.add_field(
                name="📊 Statut Actuel",
                value=f"**{current_info['name']}** ({current_info['type']})\n"
                f"Position: {current_info['index'] + 1}/{current_info['total']}",
                inline=False
            )

        embed.add_field(
            name="⚙️ Configuration",
            value=f"Intervalle: {rotator.rotation_interval}s | "
            f"Statuts: {len(rotator.statuses)} | "
            f"État: {'🟢 Actif' if rotator.rotation_task and not rotator.rotation_task.done() else '🔴 Arrêté'}",
            inline=False
        )

        await ctx.send(embed=embed)

    @status_group.command(name='help', aliases=['aide'])
    async def status_help(self, ctx):
        """Affiche l'aide pour les commandes de statut."""
        embed = discord.Embed(
            title="📖 Aide - Commandes de Statut",
            description="Toutes les commandes pour gérer le système de rotation des statuts",
            color=0x3498db
        )

        embed.add_field(
            name="📊 Informations",
            value="`!status` - Informations générales\n"
                  "`!status list` - Liste des statuts\n"
                  "`!status current` - Statut actuel",
            inline=False
        )

        embed.add_field(
            name="🎛️ Contrôles (Propriétaires uniquement)",
            value="`!status start` - Démarrer la rotation\n"
                  "`!status stop` - Arrêter la rotation\n"
                  "`!status next` - Statut suivant\n"
                  "`!status interval <secondes>` - Changer l'intervalle",
            inline=False
        )

        embed.add_field(
            name="🌟 Statuts Spéciaux (Propriétaires uniquement)",
            value="`!status special maintenance [durée]` - Mode maintenance\n"
                  "`!status special update [durée]` - Mode mise à jour\n"
                  "`!status special error [durée]` - Mode erreur\n"
                  "`!status special offline [durée]` - Mode veille",
            inline=False
        )

        embed.set_footer(
            text="💡 Durée en secondes, optionnelle pour les statuts spéciaux")

        await ctx.send(embed=embed)

    @status_group.command(name='info', aliases=['information'])
    async def status_info(self, ctx):
        """Affiche les informations détaillées sur le système de statuts."""
        if not hasattr(self.bot, 'status_rotator') or self.bot.status_rotator is None:
            await ctx.send("❌ Le système de rotation des statuts n'est pas initialisé.")
            return

        rotator = self.bot.status_rotator
        current_info = rotator.get_current_status_info()

        embed = discord.Embed(
            title="🔄 Informations Détaillées - Rotation des Statuts",
            color=0x3498db
        )

        if current_info:
            embed.add_field(
                name="📊 Statut Actuel",
                value=f"**Nom:** {current_info['name']}\n"
                f"**Type:** {current_info['type']}\n"
                f"**État:** {current_info['status']}\n"
                f"**Position:** {current_info['index'] + 1}/{current_info['total']}",
                inline=True
            )

        embed.add_field(
            name="⚙️ Configuration",
            value=f"**Intervalle:** {rotator.rotation_interval} secondes\n"
            f"**Statuts disponibles:** {len(rotator.statuses)}\n"
            f"**Rotation active:** {'✅ Oui' if rotator.rotation_task and not rotator.rotation_task.done() else '❌ Non'}",
            inline=True
        )

        embed.add_field(
            name="🎯 Statuts Spéciaux Disponibles",
            value="🔧 **maintenance** - Mode maintenance\n"
                  "🆕 **update** - Mode mise à jour\n"
                  "⚠️ **error** - Mode erreur\n"
                  "💤 **offline** - Mode veille",
            inline=False
        )

        await ctx.send(embed=embed)

    @status_group.command(name='list', aliases=['liste'])
    async def status_list(self, ctx, page: int = 1):
        """Affiche la liste des statuts disponibles."""
        if not hasattr(self.bot, 'status_rotator') or self.bot.status_rotator is None:
            await ctx.send("❌ Le système de rotation des statuts n'est pas initialisé.")
            return

        rotator = self.bot.status_rotator
        status_list = rotator.get_status_list()

        # Pagination
        per_page = 10
        total_pages = (len(status_list) + per_page - 1) // per_page

        if page < 1 or page > total_pages:
            await ctx.send(f"❌ Page invalide. Utilisez une page entre 1 et {total_pages}.")
            return

        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        page_statuses = status_list[start_idx:end_idx]

        embed = discord.Embed(
            title=f"📋 Liste des Statuts - Page {page}/{total_pages}",
            description=f"Total: {len(status_list)} statuts disponibles",
            color=0x3498db
        )

        for status in page_statuses:
            type_emoji = {
                'playing': '🎮',
                'watching': '👀',
                'listening': '🎵',
                'streaming': '📺',
                'custom': '✨'
            }.get(status['type'], '❓')

            embed.add_field(
                name=f"{type_emoji} #{status['index'] + 1}",
                value=f"**{status['name']}**\n{status['type']} • {status['status']}",
                inline=True
            )

        if total_pages > 1:
            embed.set_footer(
                text=f"Utilisez !status list <page> pour naviguer • Page {page}/{total_pages}")

        await ctx.send(embed=embed)

    @status_group.command(name='current', aliases=['actuel'])
    async def status_current(self, ctx):
        """Affiche le statut actuellement actif."""
        if not hasattr(self.bot, 'status_rotator') or self.bot.status_rotator is None:
            await ctx.send("❌ Le système de rotation des statuts n'est pas initialisé.")
            return

        rotator = self.bot.status_rotator
        current_info = rotator.get_current_status_info()

        if not current_info:
            await ctx.send("ℹ️ Aucun statut n'est actuellement actif.")
            return

        embed = discord.Embed(
            title="📊 Statut Actuel",
            color=0x2ecc71
        )

        type_emoji = {
            'playing': '🎮',
            'watching': '👀',
            'listening': '🎵',
            'streaming': '📺',
            'custom': '✨'
        }.get(current_info['type'], '❓')

        embed.add_field(
            name=f"{type_emoji} {current_info['type'].title()}",
            value=f"**{current_info['name']}**",
            inline=False
        )

        embed.add_field(
            name="📍 Position",
            value=f"{current_info['index'] + 1}/{current_info['total']}",
            inline=True
        )

        embed.add_field(
            name="🌐 État",
            value=current_info['status'].title(),
            inline=True
        )

        await ctx.send(embed=embed)

    @status_group.command(name='start', aliases=['demarrer'])
    @commands.is_owner()
    async def status_start(self, ctx):
        """Démarre la rotation automatique des statuts."""
        if not hasattr(self.bot, 'status_rotator') or self.bot.status_rotator is None:
            await ctx.send("❌ Le système de rotation des statuts n'est pas initialisé.")
            return

        rotator = self.bot.status_rotator

        if rotator.rotation_task and not rotator.rotation_task.done():
            await ctx.send("⚠️ La rotation des statuts est déjà active.")
            return

        rotator.start_rotation()

        embed = discord.Embed(
            title="✅ Rotation Démarrée",
            description=f"La rotation automatique a été démarrée avec un intervalle de {rotator.rotation_interval} secondes.",
            color=0x2ecc71
        )

        await ctx.send(embed=embed)

    @status_group.command(name='stop', aliases=['arreter'])
    @commands.is_owner()
    async def status_stop(self, ctx):
        """Arrête la rotation automatique des statuts."""
        if not hasattr(self.bot, 'status_rotator') or self.bot.status_rotator is None:
            await ctx.send("❌ Le système de rotation des statuts n'est pas initialisé.")
            return

        rotator = self.bot.status_rotator
        rotator.stop_rotation()

        embed = discord.Embed(
            title="⏹️ Rotation Arrêtée",
            description="La rotation automatique des statuts a été arrêtée.",
            color=0xe74c3c
        )

        await ctx.send(embed=embed)

    @status_group.command(name='next', aliases=['suivant'])
    @commands.is_owner()
    async def status_next(self, ctx):
        """Passe au statut suivant manuellement."""
        if not hasattr(self.bot, 'status_rotator') or self.bot.status_rotator is None:
            await ctx.send("❌ Le système de rotation des statuts n'est pas initialisé.")
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
                    value=f"**{current_info['name']}** ({current_info['type']})",
                    inline=False
                )

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"❌ Erreur lors de la mise à jour du statut: {e}")

    @status_group.command(name='interval', aliases=['intervalle'])
    @commands.is_owner()
    async def status_interval(self, ctx, seconds: int):
        """Change l'intervalle de rotation des statuts."""
        if not hasattr(self.bot, 'status_rotator') or self.bot.status_rotator is None:
            await ctx.send("❌ Le système de rotation des statuts n'est pas initialisé.")
            return

        if seconds < 10:
            await ctx.send("❌ L'intervalle minimum est de 10 secondes.")
            return

        if seconds > 3600:
            await ctx.send("❌ L'intervalle maximum est de 3600 secondes (1 heure).")
            return

        rotator = self.bot.status_rotator
        old_interval = rotator.rotation_interval
        rotator.set_rotation_interval(seconds)

        embed = discord.Embed(
            title="⚙️ Intervalle Modifié",
            description=f"Intervalle changé de {old_interval}s à {seconds}s",
            color=0x3498db
        )

        await ctx.send(embed=embed)

    @status_group.command(name='special', aliases=['speciale'])
    @commands.is_owner()
    async def status_special(self, ctx, status_type: str, duration: int = 0):
        """Active un statut spécial temporaire."""
        if not hasattr(self.bot, 'status_rotator') or self.bot.status_rotator is None:
            await ctx.send("❌ Le système de rotation des statuts n'est pas initialisé.")
            return

        valid_types = ['maintenance', 'update', 'error', 'offline']
        if status_type.lower() not in valid_types:
            await ctx.send(f"❌ Type de statut invalide. Types disponibles: {', '.join(valid_types)}")
            return

        rotator = self.bot.status_rotator

        try:
            if duration < 0:
                duration = 0
            elif duration > 3600:
                duration = 3600

            await rotator.set_special_status(status_type.lower(), duration if duration > 0 else None)

            embed = discord.Embed(
                title="🌟 Statut Spécial Activé",
                description=f"Le statut spécial **{status_type}** a été activé.",
                color=0x9b59b6
            )

            if duration > 0:
                embed.add_field(
                    name="⏰ Durée",
                    value=f"{duration} secondes",
                    inline=True
                )
            else:
                embed.add_field(
                    name="⏰ Durée",
                    value="Permanent",
                    inline=True
                )

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"❌ Erreur: {e}")

    @status_start.error
    @status_stop.error
    @status_next.error
    @status_interval.error
    @status_special.error
    async def status_owner_error(self, ctx, error):
        """Gère les erreurs des commandes réservées aux propriétaires."""
        if isinstance(error, commands.NotOwner):
            await ctx.send("❌ Seuls les propriétaires du bot peuvent utiliser cette commande.")


async def setup(bot):
    await bot.add_cog(StatusPrefixCommands(bot))
