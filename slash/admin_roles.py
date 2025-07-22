"""
Commandes slash - Module admin rôles (gestion des rôles)
"""
import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime


class AdminRolesSlash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # === GESTION DES RÔLES ===
    @app_commands.command(name="addrole", description="Ajoute un rôle à un membre")
    @app_commands.describe(
        member="Le membre à qui ajouter le rôle",
        role="Le rôle à ajouter"
    )
    @app_commands.guild_only()
    async def add_role_slash(self, interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        """Commande slash pour ajouter un rôle à un membre"""
        # Vérification des permissions
        if not interaction.user.guild_permissions.manage_roles:
            embed = discord.Embed(
                title="❌ Permissions Insuffisantes",
                description="Tu as besoin de la permission `Gérer les rôles` pour cette commande.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if role >= interaction.user.top_role and interaction.user != interaction.guild.owner:
            await interaction.response.send_message("❌ Tu ne peux pas assigner un rôle égal ou supérieur au tien !", ephemeral=True)
            return

        if role >= interaction.guild.me.top_role:
            await interaction.response.send_message("❌ Je ne peux pas assigner un rôle égal ou supérieur au mien !", ephemeral=True)
            return

        if role in member.roles:
            await interaction.response.send_message(f"❌ {member.mention} a déjà le rôle {role.mention} !", ephemeral=True)
            return

        try:
            await member.add_roles(role, reason=f"Rôle ajouté par {interaction.user}")

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
                            value=interaction.user.mention, inline=True)
            embed.set_thumbnail(url=member.display_avatar.url)

            await interaction.response.send_message(embed=embed)

        except discord.HTTPException as e:
            await interaction.response.send_message(f"❌ Erreur lors de l'ajout du rôle: {e}", ephemeral=True)

    @app_commands.command(name="removerole", description="Retire un rôle d'un membre")
    @app_commands.describe(
        member="Le membre à qui retirer le rôle",
        role="Le rôle à retirer"
    )
    @app_commands.guild_only()
    async def remove_role_slash(self, interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        """Commande slash pour retirer un rôle d'un membre"""
        # Vérification des permissions
        if not interaction.user.guild_permissions.manage_roles:
            embed = discord.Embed(
                title="❌ Permissions Insuffisantes",
                description="Tu as besoin de la permission `Gérer les rôles` pour cette commande.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if role >= interaction.user.top_role and interaction.user != interaction.guild.owner:
            await interaction.response.send_message("❌ Tu ne peux pas retirer un rôle égal ou supérieur au tien !", ephemeral=True)
            return

        if role >= interaction.guild.me.top_role:
            await interaction.response.send_message("❌ Je ne peux pas retirer un rôle égal ou supérieur au mien !", ephemeral=True)
            return

        if role not in member.roles:
            await interaction.response.send_message(f"❌ {member.mention} n'a pas le rôle {role.mention} !", ephemeral=True)
            return

        try:
            await member.remove_roles(role, reason=f"Rôle retiré par {interaction.user}")

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
                            value=interaction.user.mention, inline=True)
            embed.set_thumbnail(url=member.display_avatar.url)

            await interaction.response.send_message(embed=embed)

        except discord.HTTPException as e:
            await interaction.response.send_message(f"❌ Erreur lors de la suppression du rôle: {e}", ephemeral=True)

    @app_commands.command(name="roles", description="Affiche les rôles d'un membre")
    @app_commands.describe(member="Le membre dont afficher les rôles (optionnel)")
    @app_commands.guild_only()
    async def show_roles_slash(self, interaction: discord.Interaction, member: discord.Member = None):
        """Commande slash pour afficher les rôles d'un membre"""
        member = member or interaction.user

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

        await interaction.response.send_message(embed=embed)

    # === COMMANDES D'INFORMATION ===
    @app_commands.command(name="userinfo", description="Affiche les informations d'un membre")
    @app_commands.describe(member="Le membre dont afficher les informations (optionnel)")
    @app_commands.guild_only()
    async def user_info_slash(self, interaction: discord.Interaction, member: discord.Member = None):
        """Commande slash pour afficher les informations d'un membre"""
        member = member or interaction.user

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
            sorted_members = sorted([m for m in interaction.guild.members if m.joined_at],
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
        if len(roles_text) > 1024:
            roles_text = roles_text[:1020] + "..."
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

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="serverinfo", description="Affiche les informations du serveur")
    @app_commands.guild_only()
    async def server_info_slash(self, interaction: discord.Interaction):
        """Commande slash pour afficher les informations du serveur"""
        guild = interaction.guild

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

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    """Fonction pour charger le cog"""
    await bot.add_cog(AdminRolesSlash(bot))
    print("✅ Module slash/admin_roles chargé")
