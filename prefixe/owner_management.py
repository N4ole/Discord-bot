"""
Commandes préfixées - Module de gestion des propriétaires (réservé aux propriétaires du bot)
"""
from bot_owner_manager import is_bot_owner, get_bot_owners, add_bot_owner, remove_bot_owner
import discord
from discord.ext import commands
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


class OwnerManagementPrefixe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="owner", help="Gestion des propriétaires du bot (propriétaires uniquement)", invoke_without_command=True)
    async def owner(self, ctx):
        """Commande principale de gestion des propriétaires"""
        if not is_bot_owner(ctx.author.id):
            await ctx.send("❌ Cette commande est réservée aux propriétaires du bot.")
            return

        await ctx.send_help('owner')

    @owner.command(name="list", help="Affiche la liste des propriétaires")
    async def owner_list(self, ctx):
        """Affiche la liste des propriétaires du bot"""
        if not is_bot_owner(ctx.author.id):
            await ctx.send("❌ Cette commande est réservée aux propriétaires du bot.")
            return

        owners = get_bot_owners()

        if not owners:
            await ctx.send("❌ Aucun propriétaire configuré.")
            return

        embed = discord.Embed(
            title="👑 Propriétaires du Bot",
            description="Liste des utilisateurs autorisés à utiliser les commandes de propriétaire",
            color=discord.Color.gold()
        )

        owner_list = []
        for i, owner_id in enumerate(owners, 1):
            try:
                user = await self.bot.fetch_user(owner_id)
                owner_list.append(f"{i}. **{user.name}** (`{user.id}`)")
            except discord.NotFound:
                owner_list.append(
                    f"{i}. **Utilisateur inconnu** (`{owner_id}`)")
            except Exception:
                owner_list.append(
                    f"{i}. **ID: {owner_id}** (impossible de récupérer les infos)")

        embed.add_field(
            name=f"📋 {len(owners)} propriétaire(s)",
            value="\n".join(
                owner_list) if owner_list else "Aucun propriétaire",
            inline=False
        )

        embed.set_footer(text=f"Demandé par {ctx.author}")
        embed.timestamp = discord.utils.utcnow()

        await ctx.send(embed=embed)

    @owner.command(name="add", help="Ajoute un propriétaire (ID Discord)")
    async def owner_add(self, ctx, user_id: int = None):
        """Ajoute un utilisateur à la liste des propriétaires"""
        if not is_bot_owner(ctx.author.id):
            await ctx.send("❌ Cette commande est réservée aux propriétaires du bot.")
            return

        if user_id is None:
            await ctx.send("❌ Veuillez spécifier l'ID Discord de l'utilisateur à ajouter.\n"
                           "Exemple: `!owner add 123456789012345678`")
            return

        # Vérifier si l'utilisateur existe
        try:
            user = await self.bot.fetch_user(user_id)
        except discord.NotFound:
            await ctx.send("❌ Utilisateur introuvable avec cet ID.")
            return
        except Exception as e:
            await ctx.send(f"❌ Erreur lors de la vérification de l'utilisateur: {str(e)}")
            return

        # Vérifier si l'utilisateur est déjà propriétaire
        if is_bot_owner(user_id):
            await ctx.send(f"⚠️ **{user.name}** (`{user_id}`) est déjà propriétaire du bot.")
            return

        # Ajouter le propriétaire
        if add_bot_owner(user_id):
            embed = discord.Embed(
                title="✅ Propriétaire Ajouté",
                description=f"**{user.name}** a été ajouté à la liste des propriétaires du bot.",
                color=discord.Color.green()
            )

            embed.add_field(
                name="👤 Utilisateur",
                value=f"{user.mention} (`{user.id}`)",
                inline=True
            )

            embed.add_field(
                name="👑 Ajouté par",
                value=ctx.author.mention,
                inline=True
            )

            embed.set_thumbnail(url=user.avatar.url if user.avatar else None)
            embed.set_footer(
                text="Cet utilisateur peut maintenant utiliser toutes les commandes de propriétaire")
            embed.timestamp = discord.utils.utcnow()

            await ctx.send(embed=embed)
            print(
                f"👑 OWNER ADD: {user.name} ({user_id}) ajouté par {ctx.author} ({ctx.author.id})")
        else:
            await ctx.send("❌ Erreur lors de l'ajout du propriétaire. Vérifiez les permissions du fichier.")

    @owner.command(name="remove", help="Supprime un propriétaire (ID Discord)")
    async def owner_remove(self, ctx, user_id: int = None):
        """Supprime un utilisateur de la liste des propriétaires"""
        if not is_bot_owner(ctx.author.id):
            await ctx.send("❌ Cette commande est réservée aux propriétaires du bot.")
            return

        if user_id is None:
            await ctx.send("❌ Veuillez spécifier l'ID Discord de l'utilisateur à supprimer.\n"
                           "Exemple: `!owner remove 123456789012345678`")
            return

        # Empêcher l'auto-suppression
        if user_id == ctx.author.id:
            await ctx.send("❌ Vous ne pouvez pas vous retirer vous-même de la liste des propriétaires.")
            return

        # Vérifier si l'utilisateur est propriétaire
        if not is_bot_owner(user_id):
            await ctx.send("⚠️ Cet utilisateur n'est pas dans la liste des propriétaires.")
            return

        # Empêcher de supprimer le dernier propriétaire
        owners = get_bot_owners()
        if len(owners) <= 1:
            await ctx.send("❌ Impossible de supprimer le dernier propriétaire. Ajoutez d'abord un autre propriétaire.")
            return

        # Récupérer les infos de l'utilisateur
        try:
            user = await self.bot.fetch_user(user_id)
            user_name = user.name
        except:
            user_name = f"ID: {user_id}"

        # Supprimer le propriétaire
        if remove_bot_owner(user_id):
            embed = discord.Embed(
                title="🗑️ Propriétaire Supprimé",
                description=f"**{user_name}** a été retiré de la liste des propriétaires du bot.",
                color=discord.Color.orange()
            )

            embed.add_field(
                name="👤 Utilisateur",
                value=f"{user_name} (`{user_id}`)",
                inline=True
            )

            embed.add_field(
                name="👑 Supprimé par",
                value=ctx.author.mention,
                inline=True
            )

            embed.set_footer(
                text="Cet utilisateur ne peut plus utiliser les commandes de propriétaire")
            embed.timestamp = discord.utils.utcnow()

            await ctx.send(embed=embed)
            print(
                f"🗑️ OWNER REMOVE: {user_name} ({user_id}) supprimé par {ctx.author} ({ctx.author.id})")
        else:
            await ctx.send("❌ Erreur lors de la suppression du propriétaire. Vérifiez les permissions du fichier.")

    @owner.command(name="check", help="Vérifie si un utilisateur est propriétaire")
    async def owner_check(self, ctx, user_id: int = None):
        """Vérifie si un utilisateur est propriétaire du bot"""
        if not is_bot_owner(ctx.author.id):
            await ctx.send("❌ Cette commande est réservée aux propriétaires du bot.")
            return

        if user_id is None:
            # Vérifier pour l'utilisateur qui tape la commande
            user_id = ctx.author.id

        # Récupérer les infos de l'utilisateur
        try:
            user = await self.bot.fetch_user(user_id)
            user_name = f"**{user.name}**"
            avatar_url = user.avatar.url if user.avatar else None
        except:
            user_name = f"**ID: {user_id}**"
            avatar_url = None

        is_owner = is_bot_owner(user_id)

        embed = discord.Embed(
            title="🔍 Vérification de Propriétaire",
            color=discord.Color.green() if is_owner else discord.Color.red()
        )

        embed.add_field(
            name="👤 Utilisateur",
            value=f"{user_name} (`{user_id}`)",
            inline=False
        )

        embed.add_field(
            name="👑 Statut",
            value="✅ **Propriétaire du bot**" if is_owner else "❌ **Pas propriétaire**",
            inline=False
        )

        if avatar_url:
            embed.set_thumbnail(url=avatar_url)

        embed.set_footer(text=f"Vérification effectuée par {ctx.author}")
        embed.timestamp = discord.utils.utcnow()

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(OwnerManagementPrefixe(bot))
