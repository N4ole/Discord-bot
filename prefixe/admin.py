"""
Commandes préfixées - Module admin (modération)
"""
import discord
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta
import re


class AdminPrefixe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # === COMMANDES DE BAN ===
    @commands.command(name="ban", help="Bannit un membre du serveur")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason: str = None):
        """Bannit un membre du serveur"""
        if member == ctx.author:
            await ctx.send("❌ Tu ne peux pas te bannir toi-même !")
            return

        if member.top_role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            await ctx.send("❌ Tu ne peux pas bannir quelqu'un avec un rôle égal ou supérieur au tien !")
            return

        if member.top_role >= ctx.guild.me.top_role:
            await ctx.send("❌ Je ne peux pas bannir quelqu'un avec un rôle égal ou supérieur au mien !")
            return

        reason = reason or f"Banni par {ctx.author} - Aucune raison spécifiée"

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
                            value=ctx.author.mention, inline=True)
            embed.add_field(name="📝 Raison", value=reason, inline=False)
            embed.set_thumbnail(url=member.display_avatar.url)

            await ctx.send(embed=embed)

        except discord.HTTPException as e:
            await ctx.send(f"❌ Erreur lors du bannissement: {e}")

    @commands.command(name="unban", help="Débannit un utilisateur")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def unban(self, ctx, user_id: int, *, reason: str = None):
        """Débannit un utilisateur par son ID"""
        reason = reason or f"Débanni par {ctx.author}"

        try:
            user = await self.bot.fetch_user(user_id)
            await ctx.guild.unban(user, reason=reason)

            embed = discord.Embed(
                title="🔓 Utilisateur Débanni",
                description=f"{user.mention} a été débanni du serveur",
                color=discord.Color.green(),
                timestamp=datetime.utcnow()
            )
            embed.add_field(name="👤 Utilisateur",
                            value=f"{user} (ID: {user.id})", inline=False)
            embed.add_field(name="🛡️ Modérateur",
                            value=ctx.author.mention, inline=True)
            embed.add_field(name="📝 Raison", value=reason, inline=False)
            embed.set_thumbnail(url=user.display_avatar.url)

            await ctx.send(embed=embed)

        except discord.NotFound:
            await ctx.send("❌ Utilisateur non trouvé ou pas banni")
        except discord.HTTPException as e:
            await ctx.send(f"❌ Erreur lors du débannissement: {e}")

    # === COMMANDES DE KICK ===
    @commands.command(name="kick", help="Expulse un membre du serveur")
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str = None):
        """Expulse un membre du serveur"""
        if member == ctx.author:
            await ctx.send("❌ Tu ne peux pas t'expulser toi-même !")
            return

        if member.top_role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            await ctx.send("❌ Tu ne peux pas expulser quelqu'un avec un rôle égal ou supérieur au tien !")
            return

        if member.top_role >= ctx.guild.me.top_role:
            await ctx.send("❌ Je ne peux pas expulser quelqu'un avec un rôle égal ou supérieur au mien !")
            return

        reason = reason or f"Expulsé par {ctx.author} - Aucune raison spécifiée"

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
                            value=ctx.author.mention, inline=True)
            embed.add_field(name="📝 Raison", value=reason, inline=False)
            embed.set_thumbnail(url=member.display_avatar.url)

            await ctx.send(embed=embed)

        except discord.HTTPException as e:
            await ctx.send(f"❌ Erreur lors de l'expulsion: {e}")

    # === COMMANDES DE TIMEOUT (MUTE) ===
    @commands.command(name="mute", help="Met un membre en timeout")
    @commands.guild_only()
    @commands.has_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    async def mute(self, ctx, member: discord.Member, duration: str = "10m", *, reason: str = None):
        """Met un membre en timeout"""
        if member == ctx.author:
            await ctx.send("❌ Tu ne peux pas te mute toi-même !")
            return

        if member.top_role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            await ctx.send("❌ Tu ne peux pas mute quelqu'un avec un rôle égal ou supérieur au tien !")
            return

        if member.top_role >= ctx.guild.me.top_role:
            await ctx.send("❌ Je ne peux pas mute quelqu'un avec un rôle égal ou supérieur au mien !")
            return

        # Conversion de la durée
        time_dict = {"s": 1, "m": 60, "h": 3600, "d": 86400}
        time_regex = re.compile(r'(\d+)([smhd])')
        matches = time_regex.findall(duration.lower())

        if not matches:
            await ctx.send("❌ Format de durée invalide ! Utilisez: 10s, 5m, 2h, 1d")
            return

        total_seconds = 0
        for amount, unit in matches:
            total_seconds += int(amount) * time_dict[unit]

        if total_seconds > 2419200:  # 28 jours max
            await ctx.send("❌ La durée maximale est de 28 jours !")
            return

        until = discord.utils.utcnow() + timedelta(seconds=total_seconds)
        reason = reason or f"Mute par {ctx.author}"

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
                            value=ctx.author.mention, inline=True)
            embed.add_field(name="⏰ Durée", value=duration, inline=True)
            embed.add_field(name="📅 Fin du timeout",
                            value=f"<t:{int(until.timestamp())}:R>", inline=True)
            embed.add_field(name="📝 Raison", value=reason, inline=False)
            embed.set_thumbnail(url=member.display_avatar.url)

            await ctx.send(embed=embed)

        except discord.HTTPException as e:
            await ctx.send(f"❌ Erreur lors du mute: {e}")

    @commands.command(name="unmute", help="Retire le timeout d'un membre")
    @commands.guild_only()
    @commands.has_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    async def unmute(self, ctx, member: discord.Member, *, reason: str = None):
        """Retire le timeout d'un membre"""
        if not member.is_timed_out():
            await ctx.send("❌ Ce membre n'est pas en timeout !")
            return

        reason = reason or f"Unmute par {ctx.author}"

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
                            value=ctx.author.mention, inline=True)
            embed.add_field(name="📝 Raison", value=reason, inline=False)
            embed.set_thumbnail(url=member.display_avatar.url)

            await ctx.send(embed=embed)

        except discord.HTTPException as e:
            await ctx.send(f"❌ Erreur lors de l'unmute: {e}")

    # === GESTION DES ERREURS ===
    @ban.error
    @kick.error
    @mute.error
    @unmute.error
    async def moderation_error(self, ctx, error):
        """Gestion des erreurs de modération"""
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ Tu n'as pas les permissions nécessaires pour cette commande.")
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send("❌ Je n'ai pas les permissions nécessaires pour exécuter cette commande.")
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send("❌ Membre non trouvé.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("❌ Arguments invalides. Vérifiez la syntaxe de la commande.")


async def setup(bot):
    """Fonction pour charger le cog"""
    await bot.add_cog(AdminPrefixe(bot))
    print("✅ Module prefixe/admin chargé")
