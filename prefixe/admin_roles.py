"""
Commandes préfixées - Module admin rôles (gestion des rôles)
"""
import discord
from discord.ext import commands
from datetime import datetime


class AdminRolesPrefixe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # === GESTION DES RÔLES ===
    @commands.command(name="addrole", help="Ajoute un rôle à un membre")
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def add_role(self, ctx, member: discord.Member, *, role: discord.Role):
        """Ajoute un rôle à un membre"""
        if role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            await ctx.send("❌ Tu ne peux pas assigner un rôle égal ou supérieur au tien !")
            return

        if role >= ctx.guild.me.top_role:
            await ctx.send("❌ Je ne peux pas assigner un rôle égal ou supérieur au mien !")
            return

        if role in member.roles:
            await ctx.send(f"❌ {member.mention} a déjà le rôle {role.mention} !")
            return

        try:
            await member.add_roles(role, reason=f"Rôle ajouté par {ctx.author}")

            embed = discord.Embed(
                title="➕ Rôle Ajouté",
                description=f"Le rôle {role.mention} a été ajouté à {member.mention}",
                color=discord.Color.green(),
                timestamp=datetime.utcnow()
            )
            embed.add_field(name="👤 Utilisateur",
                            value=f"{member} (ID: {member.id})", inline=True)
            embed.add_field(
                name="🎭 Rôle", value=f"{role.mention} (ID: {role.id})", inline=True)
            embed.add_field(name="🛡️ Modérateur",
                            value=ctx.author.mention, inline=True)
            embed.set_thumbnail(url=member.display_avatar.url)

            await ctx.send(embed=embed)

        except discord.HTTPException as e:
            await ctx.send(f"❌ Erreur lors de l'ajout du rôle: {e}")

    @commands.command(name="removerole", help="Retire un rôle d'un membre")
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def remove_role(self, ctx, member: discord.Member, *, role: discord.Role):
        """Retire un rôle d'un membre"""
        if role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            await ctx.send("❌ Tu ne peux pas retirer un rôle égal ou supérieur au tien !")
            return

        if role >= ctx.guild.me.top_role:
            await ctx.send("❌ Je ne peux pas retirer un rôle égal ou supérieur au mien !")
            return

        if role not in member.roles:
            await ctx.send(f"❌ {member.mention} n'a pas le rôle {role.mention} !")
            return

        try:
            await member.remove_roles(role, reason=f"Rôle retiré par {ctx.author}")

            embed = discord.Embed(
                title="➖ Rôle Retiré",
                description=f"Le rôle {role.mention} a été retiré de {member.mention}",
                color=discord.Color.orange(),
                timestamp=datetime.utcnow()
            )
            embed.add_field(name="👤 Utilisateur",
                            value=f"{member} (ID: {member.id})", inline=True)
            embed.add_field(
                name="🎭 Rôle", value=f"{role.mention} (ID: {role.id})", inline=True)
            embed.add_field(name="🛡️ Modérateur",
                            value=ctx.author.mention, inline=True)
            embed.set_thumbnail(url=member.display_avatar.url)

            await ctx.send(embed=embed)

        except discord.HTTPException as e:
            await ctx.send(f"❌ Erreur lors de la suppression du rôle: {e}")

    @commands.command(name="roles", help="Affiche les rôles d'un membre")
    @commands.guild_only()
    async def show_roles(self, ctx, member: discord.Member = None):
        """Affiche les rôles d'un membre"""
        member = member or ctx.author

        roles = [role.mention for role in member.roles[1:]]  # Exclut @everyone

        if not roles:
            roles_text = "Aucun rôle"
        else:
            roles_text = ", ".join(roles)

        embed = discord.Embed(
            title=f"🎭 Rôles de {member.display_name}",
            description=roles_text,
            color=member.color if member.color != discord.Color.default() else discord.Color.blue(),
            timestamp=datetime.utcnow()
        )

        embed.add_field(name="👤 Utilisateur",
                        value=f"{member} (ID: {member.id})", inline=True)
        embed.add_field(name="📊 Nombre de rôles", value=str(
            len(member.roles) - 1), inline=True)
        embed.add_field(name="🎯 Rôle le plus haut",
                        value=member.top_role.mention, inline=True)
        embed.set_thumbnail(url=member.display_avatar.url)

        await ctx.send(embed=embed)

    # === COMMANDES D'INFORMATION ===
    @commands.command(name="userinfo", help="Affiche les informations d'un membre")
    @commands.guild_only()
    async def user_info(self, ctx, member: discord.Member = None):
        """Affiche les informations détaillées d'un membre"""
        member = member or ctx.author

        # Calcul du temps sur le serveur
        joined_ago = (datetime.utcnow() - member.joined_at.replace(tzinfo=None)
                      ).days if member.joined_at else "Inconnu"
        created_ago = (datetime.utcnow() -
                       member.created_at.replace(tzinfo=None)).days

        embed = discord.Embed(
            title=f"📋 Informations de {member.display_name}",
            color=member.color if member.color != discord.Color.default() else discord.Color.blue(),
            timestamp=datetime.utcnow()
        )

        embed.set_thumbnail(url=member.display_avatar.url)

        # Informations de base
        embed.add_field(name="👤 Nom complet", value=str(member), inline=True)
        embed.add_field(name="🆔 ID", value=member.id, inline=True)
        embed.add_field(
            name="🤖 Bot", value="Oui" if member.bot else "Non", inline=True)

        # Dates
        embed.add_field(name="📅 Compte créé",
                        value=f"<t:{int(member.created_at.timestamp())}:R>", inline=True)
        if member.joined_at:
            embed.add_field(
                name="📅 A rejoint", value=f"<t:{int(member.joined_at.timestamp())}:R>", inline=True)

        # Position du membre (calculée de façon sécurisée)
        try:
            sorted_members = sorted([m for m in ctx.guild.members if m.joined_at],
                                    key=lambda m: m.joined_at)
            member_position = sorted_members.index(member) + 1
            embed.add_field(name="📊 Membre n°", value=str(
                member_position), inline=True)
        except (ValueError, AttributeError):
            # Si on ne peut pas calculer la position, on l'ignore
            pass

        # Rôles
        roles = [role.mention for role in member.roles[1:]]
        roles_text = ", ".join(roles) if roles else "Aucun rôle"
        embed.add_field(name="🎭 Rôles", value=roles_text, inline=False)

        # Permissions notables
        notable_perms = []
        if member.guild_permissions.administrator:
            notable_perms.append("Administrateur")
        elif member.guild_permissions.manage_guild:
            notable_perms.append("Gérer le serveur")
        elif member.guild_permissions.manage_messages:
            notable_perms.append("Gérer les messages")
        elif member.guild_permissions.kick_members:
            notable_perms.append("Expulser")
        elif member.guild_permissions.ban_members:
            notable_perms.append("Bannir")

        if notable_perms:
            embed.add_field(name="🛡️ Permissions notables",
                            value=", ".join(notable_perms), inline=False)

        await ctx.send(embed=embed)

    @commands.command(name="serverinfo", help="Affiche les informations du serveur")
    @commands.guild_only()
    async def server_info(self, ctx):
        """Affiche les informations du serveur"""
        guild = ctx.guild

        embed = discord.Embed(
            title=f"🏰 Informations de {guild.name}",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )

        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        # Informations de base
        embed.add_field(name="👑 Propriétaire",
                        value=guild.owner.mention if guild.owner else "Inconnu", inline=True)
        embed.add_field(name="🆔 ID", value=guild.id, inline=True)
        embed.add_field(
            name="📅 Créé le", value=f"<t:{int(guild.created_at.timestamp())}:R>", inline=True)

        # Statistiques
        embed.add_field(name="👥 Membres",
                        value=f"{guild.member_count}", inline=True)
        embed.add_field(name="📝 Canaux texte", value=len(
            guild.text_channels), inline=True)
        embed.add_field(name="🔊 Canaux vocaux", value=len(
            guild.voice_channels), inline=True)

        embed.add_field(name="🎭 Rôles", value=len(guild.roles), inline=True)
        embed.add_field(name="😀 Emojis", value=len(guild.emojis), inline=True)
        embed.add_field(
            name="🚀 Boosts", value=f"{guild.premium_subscription_count} (Niveau {guild.premium_tier})", inline=True)

        # Niveau de vérification
        verification_levels = {
            discord.VerificationLevel.none: "Aucune",
            discord.VerificationLevel.low: "Faible",
            discord.VerificationLevel.medium: "Moyenne",
            discord.VerificationLevel.high: "Haute",
            discord.VerificationLevel.highest: "Très haute"
        }
        embed.add_field(name="🔒 Niveau de vérification", value=verification_levels.get(
            guild.verification_level, "Inconnu"), inline=True)

        await ctx.send(embed=embed)

    # === GESTION DES ERREURS ===
    @add_role.error
    @remove_role.error
    async def role_management_error(self, ctx, error):
        """Gestion des erreurs de gestion des rôles"""
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ Tu n'as pas la permission de gérer les rôles.")
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send("❌ Je n'ai pas la permission de gérer les rôles.")
        elif isinstance(error, commands.RoleNotFound):
            await ctx.send("❌ Rôle non trouvé.")
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send("❌ Membre non trouvé.")


async def setup(bot):
    """Fonction pour charger le cog"""
    await bot.add_cog(AdminRolesPrefixe(bot))
    print("✅ Module prefixe/admin_roles chargé")
