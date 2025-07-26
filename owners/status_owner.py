"""
Commandes de statut réservées aux propriétaires du bot
"""
import discord
from discord.ext import commands
from core.bot_owner_manager import is_bot_owner


class StatusOwnerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="status_owner", aliases=["ststatus"], help="Commandes de statut pour propriétaires", invoke_without_command=True)
    async def status_owner_group(self, ctx):
        """Commandes de gestion des statuts réservées aux propriétaires"""
        if not is_bot_owner(ctx.author.id):
            await ctx.send("❌ Ces commandes sont réservées aux propriétaires du bot.")
            return

        embed = discord.Embed(
            title="🎛️ Commandes de Statut - Propriétaires",
            description="Contrôles avancés du système de rotation des statuts",
            color=0x3498db
        )

        embed.add_field(
            name="🎬 Contrôles",
            value="`!status_owner start` - Démarrer la rotation\n"
                  "`!status_owner stop` - Arrêter la rotation\n"
                  "`!status_owner next` - Statut suivant\n"
                  "`!status_owner interval <secondes>` - Changer l'intervalle",
            inline=False
        )

        embed.add_field(
            name="🌟 Statuts Spéciaux",
            value="`!status_owner special maintenance [durée]` - Mode maintenance\n"
                  "`!status_owner special update [durée]` - Mode mise à jour\n"
                  "`!status_owner special error [durée]` - Mode erreur\n"
                  "`!status_owner special offline [durée]` - Mode veille",
            inline=False
        )

        embed.set_footer(
            text="💡 Durée en secondes, optionnelle pour les statuts spéciaux")
        await ctx.send(embed=embed)

    @status_owner_group.command(name='start', aliases=['demarrer'])
    async def status_start(self, ctx):
        """Démarre la rotation automatique des statuts."""
        if not is_bot_owner(ctx.author.id):
            await ctx.send("❌ Cette commande est réservée aux propriétaires du bot.")
            return

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

    @status_owner_group.command(name='stop', aliases=['arreter'])
    async def status_stop(self, ctx):
        """Arrête la rotation automatique des statuts."""
        if not is_bot_owner(ctx.author.id):
            await ctx.send("❌ Cette commande est réservée aux propriétaires du bot.")
            return

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

    @status_owner_group.command(name='next', aliases=['suivant'])
    async def status_next(self, ctx):
        """Passe au statut suivant manuellement."""
        if not is_bot_owner(ctx.author.id):
            await ctx.send("❌ Cette commande est réservée aux propriétaires du bot.")
            return

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

    @status_owner_group.command(name='interval', aliases=['intervalle'])
    async def status_interval(self, ctx, seconds: int):
        """Change l'intervalle de rotation des statuts."""
        if not is_bot_owner(ctx.author.id):
            await ctx.send("❌ Cette commande est réservée aux propriétaires du bot.")
            return

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

    @status_owner_group.command(name='special', aliases=['speciale'])
    async def status_special(self, ctx, status_type: str, duration: int = 0):
        """Active un statut spécial temporaire."""
        if not is_bot_owner(ctx.author.id):
            await ctx.send("❌ Cette commande est réservée aux propriétaires du bot.")
            return

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

            await rotator.set_special_status(status_type.lower(), duration)

            duration_text = f" pendant {duration} secondes" if duration > 0 else " indéfiniment"
            embed = discord.Embed(
                title="🌟 Statut Spécial Activé",
                description=f"Statut **{status_type}** activé{duration_text}.",
                color=0xf39c12
            )

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"❌ Erreur lors de l'activation du statut spécial: {e}")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Gestion des erreurs pour les commandes de statut owner"""
        if ctx.command and ctx.command.qualified_name.startswith('status_owner'):
            if isinstance(error, commands.NotOwner):
                await ctx.send("❌ Cette commande est réservée aux propriétaires du bot.")
            elif isinstance(error, commands.MissingRequiredArgument):
                await ctx.send("❌ Argument manquant. Utilisez `!help status_owner` pour voir l'aide.")
            elif isinstance(error, commands.BadArgument):
                await ctx.send("❌ Argument invalide. Vérifiez les types attendus.")


async def setup(bot):
    await bot.add_cog(StatusOwnerCommands(bot))
