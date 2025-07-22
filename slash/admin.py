"""
Commandes slash - Module admin (modération)
"""
import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timedelta
import re


class AdminSlash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # === COMMANDES DE BAN ===
    @app_commands.command(name="ban", description="Bannit un membre du serveur")
    @app_commands.describe(
        member="Le membre à bannir",
        reason="La raison du bannissement"
    )
    @app_commands.guild_only()
    async def ban_slash(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        """Commande slash pour bannir un membre"""
        # Vérification des permissions
        if not interaction.user.guild_permissions.ban_members:
            embed = discord.Embed(
                title="❌ Permissions Insuffisantes",
                description="Tu as besoin de la permission `Bannir des membres` pour cette commande.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if member == interaction.user:
            await interaction.response.send_message("❌ Tu ne peux pas te bannir toi-même !", ephemeral=True)
            return

        if member.top_role >= interaction.user.top_role and interaction.user != interaction.guild.owner:
            await interaction.response.send_message("❌ Tu ne peux pas bannir quelqu'un avec un rôle égal ou supérieur au tien !", ephemeral=True)
            return

        if member.top_role >= interaction.guild.me.top_role:
            await interaction.response.send_message("❌ Je ne peux pas bannir quelqu'un avec un rôle égal ou supérieur au mien !", ephemeral=True)
            return

        reason = reason or f"Banni par {interaction.user} - Aucune raison spécifiée"

        try:
            await member.ban(reason=reason)

            embed = discord.Embed(
                title="🔨 Membre Banni",
                description=f"{member.mention} a été banni du serveur",
                color=discord.Color.red(),
                timestamp=datetime.utcnow()
            )
            embed.add_field(name="👤 Utilisateur",
                            value=f"{member} (ID: {member.id})", inline=False)
            embed.add_field(name="🛡️ Modérateur",
                            value=interaction.user.mention, inline=True)
            embed.add_field(name="📝 Raison", value=reason, inline=False)
            embed.set_thumbnail(url=member.display_avatar.url)

            await interaction.response.send_message(embed=embed)

        except discord.HTTPException as e:
            await interaction.response.send_message(f"❌ Erreur lors du bannissement: {e}", ephemeral=True)

    @app_commands.command(name="unban", description="Débannit un utilisateur")
    @app_commands.describe(
        user_id="L'ID de l'utilisateur à débannir",
        reason="La raison du débannissement"
    )
    @app_commands.guild_only()
    async def unban_slash(self, interaction: discord.Interaction, user_id: str, reason: str = None):
        """Commande slash pour débannir un utilisateur"""
        # Vérification des permissions
        if not interaction.user.guild_permissions.ban_members:
            embed = discord.Embed(
                title="❌ Permissions Insuffisantes",
                description="Tu as besoin de la permission `Bannir des membres` pour cette commande.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        try:
            user_id_int = int(user_id)
        except ValueError:
            await interaction.response.send_message("❌ ID utilisateur invalide !", ephemeral=True)
            return

        reason = reason or f"Débanni par {interaction.user}"

        try:
            user = await self.bot.fetch_user(user_id_int)
            await interaction.guild.unban(user, reason=reason)

            embed = discord.Embed(
                title="🔓 Utilisateur Débanni",
                description=f"{user.mention} a été débanni du serveur",
                color=discord.Color.green(),
                timestamp=datetime.utcnow()
            )
            embed.add_field(name="👤 Utilisateur",
                            value=f"{user} (ID: {user.id})", inline=False)
            embed.add_field(name="🛡️ Modérateur",
                            value=interaction.user.mention, inline=True)
            embed.add_field(name="📝 Raison", value=reason, inline=False)
            embed.set_thumbnail(url=user.display_avatar.url)

            await interaction.response.send_message(embed=embed)

        except discord.NotFound:
            await interaction.response.send_message("❌ Utilisateur non trouvé ou pas banni", ephemeral=True)
        except discord.HTTPException as e:
            await interaction.response.send_message(f"❌ Erreur lors du débannissement: {e}", ephemeral=True)

    # === COMMANDES DE KICK ===
    @app_commands.command(name="kick", description="Expulse un membre du serveur")
    @app_commands.describe(
        member="Le membre à expulser",
        reason="La raison de l'expulsion"
    )
    @app_commands.guild_only()
    async def kick_slash(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        """Commande slash pour expulser un membre"""
        # Vérification des permissions
        if not interaction.user.guild_permissions.kick_members:
            embed = discord.Embed(
                title="❌ Permissions Insuffisantes",
                description="Tu as besoin de la permission `Expulser des membres` pour cette commande.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if member == interaction.user:
            await interaction.response.send_message("❌ Tu ne peux pas t'expulser toi-même !", ephemeral=True)
            return

        if member.top_role >= interaction.user.top_role and interaction.user != interaction.guild.owner:
            await interaction.response.send_message("❌ Tu ne peux pas expulser quelqu'un avec un rôle égal ou supérieur au tien !", ephemeral=True)
            return

        if member.top_role >= interaction.guild.me.top_role:
            await interaction.response.send_message("❌ Je ne peux pas expulser quelqu'un avec un rôle égal ou supérieur au mien !", ephemeral=True)
            return

        reason = reason or f"Expulsé par {interaction.user} - Aucune raison spécifiée"

        try:
            await member.kick(reason=reason)

            embed = discord.Embed(
                title="👢 Membre Expulsé",
                description=f"{member.mention} a été expulsé du serveur",
                color=discord.Color.orange(),
                timestamp=datetime.utcnow()
            )
            embed.add_field(name="👤 Utilisateur",
                            value=f"{member} (ID: {member.id})", inline=False)
            embed.add_field(name="🛡️ Modérateur",
                            value=interaction.user.mention, inline=True)
            embed.add_field(name="📝 Raison", value=reason, inline=False)
            embed.set_thumbnail(url=member.display_avatar.url)

            await interaction.response.send_message(embed=embed)

        except discord.HTTPException as e:
            await interaction.response.send_message(f"❌ Erreur lors de l'expulsion: {e}", ephemeral=True)

    # === COMMANDES DE TIMEOUT (MUTE) ===
    @app_commands.command(name="mute", description="Met un membre en timeout")
    @app_commands.describe(
        member="Le membre à mute",
        duration="Durée du timeout (ex: 10m, 2h, 1d)",
        reason="La raison du mute"
    )
    @app_commands.guild_only()
    async def mute_slash(self, interaction: discord.Interaction, member: discord.Member, duration: str = "10m", reason: str = None):
        """Commande slash pour mute un membre"""
        # Vérification des permissions
        if not interaction.user.guild_permissions.moderate_members:
            embed = discord.Embed(
                title="❌ Permissions Insuffisantes",
                description="Tu as besoin de la permission `Modérer les membres` pour cette commande.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if member == interaction.user:
            await interaction.response.send_message("❌ Tu ne peux pas te mute toi-même !", ephemeral=True)
            return

        if member.top_role >= interaction.user.top_role and interaction.user != interaction.guild.owner:
            await interaction.response.send_message("❌ Tu ne peux pas mute quelqu'un avec un rôle égal ou supérieur au tien !", ephemeral=True)
            return

        if member.top_role >= interaction.guild.me.top_role:
            await interaction.response.send_message("❌ Je ne peux pas mute quelqu'un avec un rôle égal ou supérieur au mien !", ephemeral=True)
            return

        # Conversion de la durée
        time_dict = {"s": 1, "m": 60, "h": 3600, "d": 86400}
        time_regex = re.compile(r'(\d+)([smhd])')
        matches = time_regex.findall(duration.lower())

        if not matches:
            await interaction.response.send_message("❌ Format de durée invalide ! Utilisez: 10s, 5m, 2h, 1d", ephemeral=True)
            return

        total_seconds = 0
        for amount, unit in matches:
            total_seconds += int(amount) * time_dict[unit]

        if total_seconds > 2419200:  # 28 jours max
            await interaction.response.send_message("❌ La durée maximale est de 28 jours !", ephemeral=True)
            return

        until = discord.utils.utcnow() + timedelta(seconds=total_seconds)
        reason = reason or f"Mute par {interaction.user}"

        try:
            await member.edit(timed_out_until=until, reason=reason)

            embed = discord.Embed(
                title="🔇 Membre Mute",
                description=f"{member.mention} a été mis en timeout",
                color=discord.Color.yellow(),
                timestamp=datetime.utcnow()
            )
            embed.add_field(name="👤 Utilisateur",
                            value=f"{member} (ID: {member.id})", inline=False)
            embed.add_field(name="🛡️ Modérateur",
                            value=interaction.user.mention, inline=True)
            embed.add_field(name="⏰ Durée", value=duration, inline=True)
            embed.add_field(name="📅 Fin du timeout",
                            value=f"<t:{int(until.timestamp())}:R>", inline=True)
            embed.add_field(name="📝 Raison", value=reason, inline=False)
            embed.set_thumbnail(url=member.display_avatar.url)

            await interaction.response.send_message(embed=embed)

        except discord.HTTPException as e:
            await interaction.response.send_message(f"❌ Erreur lors du mute: {e}", ephemeral=True)

    @app_commands.command(name="unmute", description="Retire le timeout d'un membre")
    @app_commands.describe(
        member="Le membre à unmute",
        reason="La raison de l'unmute"
    )
    @app_commands.guild_only()
    async def unmute_slash(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        """Commande slash pour unmute un membre"""
        # Vérification des permissions
        if not interaction.user.guild_permissions.moderate_members:
            embed = discord.Embed(
                title="❌ Permissions Insuffisantes",
                description="Tu as besoin de la permission `Modérer les membres` pour cette commande.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if not member.is_timed_out():
            await interaction.response.send_message("❌ Ce membre n'est pas en timeout !", ephemeral=True)
            return

        reason = reason or f"Unmute par {interaction.user}"

        try:
            await member.edit(timed_out_until=None, reason=reason)

            embed = discord.Embed(
                title="🔊 Membre Unmute",
                description=f"{member.mention} n'est plus en timeout",
                color=discord.Color.green(),
                timestamp=datetime.utcnow()
            )
            embed.add_field(name="👤 Utilisateur",
                            value=f"{member} (ID: {member.id})", inline=False)
            embed.add_field(name="🛡️ Modérateur",
                            value=interaction.user.mention, inline=True)
            embed.add_field(name="📝 Raison", value=reason, inline=False)
            embed.set_thumbnail(url=member.display_avatar.url)

            await interaction.response.send_message(embed=embed)

        except discord.HTTPException as e:
            await interaction.response.send_message(f"❌ Erreur lors de l'unmute: {e}", ephemeral=True)


async def setup(bot):
    """Fonction pour charger le cog"""
    await bot.add_cog(AdminSlash(bot))
    print("✅ Module slash/admin chargé")
