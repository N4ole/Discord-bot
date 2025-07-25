"""
Panel Web d'Administration pour le Bot Discord
Interface web sécurisée pour surveiller les logs et statistiques
"""
from collections import defaultdict
import time
from core.bot_owner_manager import get_bot_owners, is_bot_owner
import uuid
from werkzeug.utils import secure_filename
from core.support_db import SupportDB
from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
import json
import os
import sys
import uuid
import asyncio
import threading
from datetime import datetime
import concurrent.futures
import traceback
import discord
sys.path.append(os.path.dirname(__file__))

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-super-secret-key-here')

# Configuration des admins (en production, utiliser une base de données)
ADMIN_CREDENTIALS = {
    'admin': generate_password_hash('admin123'),  # Changez ce mot de passe !
    # Ajoutez d'autres admins si besoin
    'owner': generate_password_hash('securepass2025')
}

# Variable globale pour stocker l'instance du bot
bot_instance = None


def set_bot_instance(bot):
    """Définit l'instance du bot pour les notifications Discord"""
    global bot_instance
    bot_instance = bot

    # Initialiser le notificateur de support avec l'instance du bot
    try:
        from core.support_notifier import support_notifier
        support_notifier.set_bot_instance(bot)
        print("✅ Notificateur de support initialisé avec l'instance du bot")
        print(
            f"🔍 DEBUG: support_notifier.bot après config = {support_notifier.bot}")
        print(f"🔍 DEBUG: admin_user_ids = {support_notifier.admin_user_ids}")
    except ImportError:
        print("⚠️ Module de notification de support non trouvé")
    except Exception as e:
        print(f"⚠️ Erreur lors de l'initialisation du notificateur: {e}")


# Stockage des logs et statistiques en mémoire
bot_logs = []
bot_stats = {
    'start_time': None,
    'commands_used': 0,
    'errors_count': 0,
    'last_activity': None,
    'connected_servers': 0,
    'total_users': 0,
    'status': 'offline'
}

# Statistiques détaillées
detailed_stats = {
    'commands_by_hour': defaultdict(int),
    'errors_by_type': defaultdict(int),
    'server_activity': defaultdict(int),
    'daily_users': defaultdict(set)
}


class BotLogger:
    """Classe pour gérer les logs du bot"""

    @staticmethod
    def log(level, message, extra_data=None):
        """Ajoute un log avec timestamp"""
        log_entry = {
            'timestamp': datetime.now(),
            'level': level,
            'message': message,
            'extra_data': extra_data or {}
        }
        bot_logs.append(log_entry)

        # Garder seulement les 1000 derniers logs
        if len(bot_logs) > 1000:
            bot_logs.pop(0)

        # Mettre à jour les statistiques
        if level == 'ERROR':
            bot_stats['errors_count'] += 1
            if extra_data and isinstance(extra_data, dict):
                detailed_stats['errors_by_type'][extra_data.get(
                    'error_type', 'Unknown')] += 1
            else:
                detailed_stats['errors_by_type']['Unknown'] += 1

        bot_stats['last_activity'] = datetime.now()

    @staticmethod
    def update_stats(bot_instance=None):
        """Met à jour les statistiques du bot"""
        if bot_instance:
            bot_stats['connected_servers'] = len(bot_instance.guilds)
            bot_stats['total_users'] = len(bot_instance.users)
            bot_stats['status'] = 'online' if bot_instance.is_ready(
            ) else 'connecting'

        bot_stats['last_update'] = datetime.now()


# Instance globale du logger
logger = BotLogger()


@app.before_request
def require_login():
    """Vérifie l'authentification pour toutes les routes sauf login, promo et support"""
    # Routes publiques (pas d'authentification admin requise)
    public_routes = ['login', 'static', 'promo', 'index',
                     'support_home', 'support_register', 'support_login',
                     'support_logout', 'support_dashboard', 'support_ticket_new',
                     'support_ticket_view', 'support_tickets', 'support_ticket_respond']

    if request.endpoint not in public_routes and 'admin_logged_in' not in session:
        # Rediriger vers la page de login admin pour les routes admin
        if request.endpoint and not request.endpoint.startswith('support_'):
            return redirect(url_for('login'))

    # Initialiser la session de support si nécessaire
    if request.endpoint and request.endpoint.startswith('support_'):
        if 'support_session_id' not in session:
            session['support_session_id'] = str(uuid.uuid4())


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Page de connexion admin"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in ADMIN_CREDENTIALS and check_password_hash(ADMIN_CREDENTIALS[username], password):
            session['admin_logged_in'] = True
            session['admin_username'] = username
            session['login_time'] = datetime.now()
            logger.log('INFO', f'Admin {username} connecté au panel web')
            return redirect(url_for('dashboard'))
        else:
            logger.log('WARNING', f'Tentative de connexion échouée pour {username}', {
                       'ip': request.remote_addr})
            flash('Nom d\'utilisateur ou mot de passe incorrect', 'error')

    return render_template('login.html')


@app.route('/logout')
def logout():
    """Déconnexion admin"""
    username = session.get('admin_username', 'Unknown')
    session.clear()
    logger.log('INFO', f'Admin {username} déconnecté du panel web')
    return redirect(url_for('login'))


@app.route('/promo')
def promo():
    """Page publicitaire du bot"""
    return render_template('promo.html')


@app.route('/')
def index():
    """Page d'accueil - redirige vers promo ou dashboard selon l'authentification"""
    if 'admin_logged_in' in session:
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('promo'))


@app.route('/dashboard')
def dashboard():
    """Dashboard principal"""
    # Calculer l'uptime
    uptime = None
    if bot_stats['start_time']:
        try:
            uptime = datetime.now() - bot_stats['start_time']
        except TypeError:
            # Si il y a un problème de timezone, réinitialiser start_time
            bot_stats['start_time'] = datetime.now()
            uptime = timedelta(seconds=0)

    return render_template('dashboard.html',
                           stats=bot_stats,
                           uptime=uptime,
                           admin=session.get('admin_username'))


@app.route('/logs')
def logs():
    """Page des logs"""
    # Filtres
    level_filter = request.args.get('level', '')
    search_filter = request.args.get('search', '')

    filtered_logs = bot_logs.copy()

    # Appliquer les filtres
    if level_filter:
        filtered_logs = [
            log for log in filtered_logs if log['level'] == level_filter]

    if search_filter:
        filtered_logs = [
            log for log in filtered_logs if search_filter.lower() in log['message'].lower()]

    # Trier par timestamp (plus récent en premier)
    filtered_logs.sort(key=lambda x: x['timestamp'], reverse=True)

    # Pagination
    page = int(request.args.get('page', 1))
    per_page = 50
    start = (page - 1) * per_page
    end = start + per_page
    paginated_logs = filtered_logs[start:end]

    total_pages = (len(filtered_logs) + per_page - 1) // per_page

    return render_template('logs.html',
                           logs=paginated_logs,
                           current_page=page,
                           total_pages=total_pages,
                           level_filter=level_filter,
                           search_filter=search_filter,
                           admin=session.get('admin_username'))


@app.route('/stats')
def statistics():
    """Page des statistiques détaillées"""
    return render_template('stats.html',
                           stats=bot_stats,
                           detailed=detailed_stats,
                           admin=session.get('admin_username'))


@app.route('/api/stats/charts')
def api_stats_charts():
    """API pour récupérer les données des graphiques"""
    current_hour = datetime.now().hour

    # Données pour le graphique des commandes par heure (24 dernières heures)
    commands_by_hour = []
    for i in range(24):
        hour = (current_hour - 23 + i) % 24
        commands_by_hour.append({
            'hour': f"{hour:02d}:00",
            'count': detailed_stats['commands_by_hour'].get(hour, 0)
        })

    # Données pour le graphique des erreurs par type
    errors_by_type = [
        {'type': error_type, 'count': count}
        for error_type, count in detailed_stats['errors_by_type'].items()
        if count > 0
    ]

    # Données en temps réel
    current_stats = {
        'timestamp': datetime.now().strftime('%H:%M:%S'),
        'commands': bot_stats['commands_used'],
        'errors': bot_stats['errors_count'],
        'servers': bot_stats['connected_servers'],
        'users': bot_stats['total_users'],
        'uptime': (datetime.now() - bot_stats['start_time']).total_seconds() if bot_stats['start_time'] else 0
    }

    return jsonify({
        'commands_by_hour': commands_by_hour,
        'errors_by_type': errors_by_type,
        'current_stats': current_stats,
        'success_rate': ((bot_stats['commands_used'] - bot_stats['errors_count']) / max(bot_stats['commands_used'], 1)) * 100
    })


@app.route('/api/stats')
def api_stats():
    """API pour récupérer les statistiques en temps réel"""
    try:
        uptime_seconds = 0
        if bot_stats['start_time']:
            uptime_seconds = (
                datetime.now() - bot_stats['start_time']).total_seconds()
    except TypeError:
        # Problème de timezone, réinitialiser
        bot_stats['start_time'] = datetime.now()
        uptime_seconds = 0

    return jsonify({
        'status': bot_stats['status'],
        'servers': bot_stats['connected_servers'],
        'users': bot_stats['total_users'],
        'commands': bot_stats['commands_used'],
        'errors': bot_stats['errors_count'],
        'last_activity': bot_stats['last_activity'].isoformat() if bot_stats['last_activity'] else None,
        'uptime': uptime_seconds
    })


@app.route('/api/recent_logs')
def api_recent_logs():
    """API pour récupérer les logs récents"""
    recent = bot_logs[-10:] if bot_logs else []
    return jsonify([{
        'timestamp': log['timestamp'].strftime('%H:%M:%S'),
        'level': log['level'],
        'message': log['message']
    } for log in recent])


@app.route('/control')
def control():
    """Page de contrôle du bot"""
    servers = []
    bot_stats_current = bot_stats.copy()
    uptime_str = "Non disponible"

    if bot_instance:
        # Récupérer les informations des serveurs
        for guild in bot_instance.guilds:
            server_info = {
                'id': str(guild.id),
                'name': guild.name,
                'member_count': guild.member_count,
                'role_count': len(guild.roles),
                'text_channels': len(guild.text_channels),
                'voice_channels': len(guild.voice_channels),
                'owner': str(guild.owner) if guild.owner else "Inconnu",
                'joined_at': guild.me.joined_at.replace(tzinfo=None).strftime('%d/%m/%Y') if guild.me.joined_at else "Inconnu",
                'premium_tier': guild.premium_tier,
                'icon_url': guild.icon.url if guild.icon else None,
                'is_owner': guild.owner_id == bot_instance.user.id
            }
            servers.append(server_info)

        # Calculer l'uptime
        if bot_stats['start_time']:
            try:
                uptime_delta = datetime.now() - bot_stats['start_time']
                days = uptime_delta.days
                hours, remainder = divmod(uptime_delta.seconds, 3600)
                minutes, _ = divmod(remainder, 60)

                if days > 0:
                    uptime_str = f"{days}j {hours}h {minutes}m"
                elif hours > 0:
                    uptime_str = f"{hours}h {minutes}m"
                else:
                    uptime_str = f"{minutes}m"
            except TypeError:
                # Problème de timezone
                bot_stats['start_time'] = datetime.now()
                uptime_str = "0m"

        # Mettre à jour les stats actuelles
        bot_stats_current.update({
            'servers': len(bot_instance.guilds),
            'users': len(bot_instance.users),
            'status': 'online' if bot_instance.is_ready() else 'connecting'
        })

    # Trier les serveurs par nom
    servers.sort(key=lambda x: x['name'].lower())

    return render_template('control.html',
                           servers=servers,
                           bot_stats=bot_stats_current,
                           uptime_str=uptime_str,
                           admin=session.get('admin_username'))


@app.route('/status_manager')
def status_manager():
    """Page de gestion du système de rotation des statuts"""
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))

    logger.log('INFO', 'Accès à la page de gestion des statuts', {
               'admin': session.get('admin_username')})

    status_info = get_status_rotator_info()

    # Si status_info est None, utiliser des valeurs par défaut
    if status_info is None:
        status_info = {
            'current_status': None,
            'rotation_active': False,
            'rotation_interval': 60,
            'total_statuses': 0,
            'special_statuses': ['maintenance', 'update', 'error', 'offline']
        }

    # Assurer que toutes les clés existent avec des valeurs par défaut
    status_info.setdefault('current_status', None)
    status_info.setdefault('rotation_active', False)
    status_info.setdefault('rotation_interval', 60)
    status_info.setdefault('total_statuses', 0)
    status_info.setdefault('special_statuses', [
                           'maintenance', 'update', 'error', 'offline'])

    return render_template('status_manager.html',
                           status_info=status_info,
                           admin=session.get('admin_username'))


@app.route('/api/status', methods=['GET'])
def api_status_info():
    """API pour récupérer les informations de statut en temps réel"""
    if 'admin_logged_in' not in session:
        return jsonify({'error': 'Non autorisé'}), 401

    status_info = get_status_rotator_info()
    return jsonify(status_info or {'error': 'Système de statuts non disponible'})


@app.route('/api/status/control', methods=['POST'])
def api_status_control():
    """API pour contrôler le système de rotation des statuts"""
    if 'admin_logged_in' not in session:
        return jsonify({'error': 'Non autorisé'}), 401

    if not bot_instance or not hasattr(bot_instance, 'status_rotator') or not bot_instance.status_rotator:
        return jsonify({'error': 'Système de statuts non disponible'}), 400

    data = request.get_json()
    action = data.get('action')
    rotator = bot_instance.status_rotator

    try:
        if action == 'start':
            if rotator.rotation_task and not rotator.rotation_task.done():
                return jsonify({'error': 'Rotation déjà active'}), 400
            rotator.start_rotation()
            logger.log('INFO', 'Rotation des statuts démarrée via panel web', {
                       'admin': session.get('admin_username')})
            return jsonify({'success': True, 'message': 'Rotation démarrée'})

        elif action == 'stop':
            rotator.stop_rotation()
            logger.log('INFO', 'Rotation des statuts arrêtée via panel web', {
                       'admin': session.get('admin_username')})
            return jsonify({'success': True, 'message': 'Rotation arrêtée'})

        elif action == 'next':
            # Utiliser la méthode run_async_safe du bot
            try:
                async def update_status():
                    await rotator._update_status()

                result = bot_instance.run_async_safe(update_status())
                if result is not None:
                    logger.log('INFO', 'Statut mis à jour manuellement via panel web', {
                               'admin': session.get('admin_username')})
                    return jsonify({'success': True, 'message': 'Statut mis à jour'})
                else:
                    return jsonify({'error': 'Erreur lors de la mise à jour du statut'}), 500
            except Exception as e:
                logger.log(
                    'ERROR', f'Erreur lors de la mise à jour du statut: {e}')
                return jsonify({'error': 'Erreur lors de la mise à jour du statut'}), 500

        elif action == 'set_interval':
            interval = data.get('interval', 60)
            if interval < 10:
                interval = 10
            elif interval > 3600:
                interval = 3600
            rotator.set_rotation_interval(interval)
            logger.log('INFO', f'Intervalle de rotation changé à {interval}s via panel web', {
                       'admin': session.get('admin_username')})
            return jsonify({'success': True, 'message': f'Intervalle défini à {interval}s'})

        elif action == 'special_status':
            status_type = data.get('status_type')
            duration = data.get('duration', 0)

            if status_type not in rotator.special_statuses:
                return jsonify({'error': 'Type de statut invalide'}), 400

            # Utiliser la méthode run_async_safe du bot
            try:
                async def set_special_status():
                    await rotator.set_special_status(status_type, duration if duration > 0 else None)

                result = bot_instance.run_async_safe(set_special_status())
                if result is not None:
                    logger.log('INFO', f'Statut spécial {status_type} activé via panel web', {
                               'admin': session.get('admin_username'),
                               'duration': duration
                               })
                    return jsonify({'success': True, 'message': f'Statut {status_type} activé'})
                else:
                    return jsonify({'error': 'Erreur lors de l\'activation du statut spécial'}), 500
            except Exception as e:
                logger.log(
                    'ERROR', f'Erreur lors de l\'activation du statut spécial: {e}')
                return jsonify({'error': 'Erreur lors de l\'activation du statut spécial'}), 500

        elif action == 'clear_special_status':
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(rotator.clear_special_status())
            loop.close()

            logger.log('INFO', 'Statut spécial désactivé via panel web', {
                       'admin': session.get('admin_username')
                       })
            return jsonify({'success': True, 'message': 'Statut spécial désactivé, rotation reprise'})

        else:
            return jsonify({'error': 'Action inconnue'}), 400

    except Exception as e:
        logger.log('ERROR', f'Erreur lors du contrôle des statuts: {str(e)}', {
                   'admin': session.get('admin_username'),
                   'action': action
                   })
        return jsonify({'error': f'Erreur: {str(e)}'}), 500


@app.route('/control/server/<int:server_id>')
def server_details(server_id):
    """Page de détails d'un serveur spécifique"""
    logger.log('INFO', f'Accès à la page détails du serveur {server_id}', {
               'admin': session.get('admin_username')})

    if not bot_instance:
        flash('Bot non connecté', 'error')
        logger.log(
            'ERROR', 'Bot non connecté lors de l\'accès aux détails du serveur')
        return redirect(url_for('control'))

    guild = bot_instance.get_guild(server_id)
    if not guild:
        flash('Serveur non trouvé', 'error')
        logger.log('WARNING', f'Serveur {server_id} non trouvé')
        return redirect(url_for('control'))

    try:
        # Informations générales du serveur
        # Note: Pour la détection précise des membres en ligne, le bot doit avoir l'intent PRESENCE et MEMBERS
        online_count = 0
        active_count = 0  # En ligne, absent, ne pas déranger

        try:
            # Compter les différents statuts
            for member in guild.members:
                if member.status == discord.Status.online:
                    online_count += 1
                    active_count += 1
                elif member.status in [discord.Status.idle, discord.Status.dnd]:
                    active_count += 1
        except Exception as e:
            # Si on ne peut pas accéder aux statuts (intents manquants), utiliser une estimation
            logger.log(
                'WARNING', f'Impossible de récupérer les statuts des membres: {str(e)}')
            # Estimation: ~5% en ligne
            online_count = max(1, guild.member_count // 20)
            # Estimation: ~10% actifs
            active_count = max(1, guild.member_count // 10)

        server_info = {
            'id': str(guild.id),
            'name': guild.name,
            'description': guild.description or "Aucune description",
            'member_count': guild.member_count,
            'online_members': online_count,
            'active_members': active_count,
            'role_count': len(guild.roles),
            'text_channels': len(guild.text_channels),
            'voice_channels': len(guild.voice_channels),
            'category_count': len(guild.categories),
            'emoji_count': len(guild.emojis),
            'sticker_count': len(guild.stickers),
            'owner': {
                'name': str(guild.owner) if guild.owner else "Inconnu",
                'id': guild.owner_id,
                'avatar': guild.owner.avatar.url if guild.owner and guild.owner.avatar else None
            },
            'created_at': guild.created_at.replace(tzinfo=None).strftime('%d/%m/%Y à %H:%M') if guild.created_at else "Inconnu",
            'joined_at': guild.me.joined_at.replace(tzinfo=None).strftime('%d/%m/%Y à %H:%M') if guild.me.joined_at else "Inconnu",
            'premium_tier': guild.premium_tier,
            'premium_subscribers': guild.premium_subscription_count or 0,
            'boost_level': guild.premium_tier,
            'verification_level': str(guild.verification_level).replace('_', ' ').title(),
            'explicit_content_filter': str(guild.explicit_content_filter).replace('_', ' ').title(),
            'default_notifications': str(guild.default_notifications).replace('_', ' ').title(),
            'icon_url': guild.icon.url if guild.icon else None,
            'banner_url': guild.banner.url if guild.banner else None,
            'splash_url': guild.splash.url if guild.splash else None,
            'is_large': guild.large,
            'max_members': guild.max_members,
            'max_presences': guild.max_presences,
            'mfa_level': guild.mfa_level,
            'preferred_locale': guild.preferred_locale
        }

        # Permissions du bot dans ce serveur
        bot_permissions = guild.me.guild_permissions
        permissions_list = [
            ('Administrateur', bot_permissions.administrator),
            ('Gérer le serveur', bot_permissions.manage_guild),
            ('Gérer les rôles', bot_permissions.manage_roles),
            ('Gérer les salons', bot_permissions.manage_channels),
            ('Expulser des membres', bot_permissions.kick_members),
            ('Bannir des membres', bot_permissions.ban_members),
            ('Voir les logs d\'audit', bot_permissions.view_audit_log),
            ('Envoyer des messages', bot_permissions.send_messages),
            ('Gérer les messages', bot_permissions.manage_messages),
            ('Utiliser des commandes slash',
             bot_permissions.use_application_commands),
            ('Se connecter aux salons vocaux', bot_permissions.connect),
            ('Parler dans les salons vocaux', bot_permissions.speak)
        ]

        # Informations sur les rôles (top 10 par nombre de membres)
        roles_info = []
        for role in sorted(guild.roles, key=lambda r: len(r.members), reverse=True)[:10]:
            if role.name != "@everyone":
                roles_info.append({
                    'name': role.name,
                    'id': role.id,
                    'member_count': len(role.members),
                    'color': str(role.color) if role.color != discord.Color.default() else '#99AAB5',
                    'position': role.position,
                    'mentionable': role.mentionable,
                    'hoisted': role.hoist,
                    'managed': role.managed
                })

        # Informations sur les salons (par catégorie)
        channels_info = {
            'categories': [],
            'text_channels': [],
            'voice_channels': []
        }

        for category in guild.categories:
            channels_info['categories'].append({
                'name': category.name,
                'id': category.id,
                'position': category.position,
                'channel_count': len(category.channels)
            })

        for channel in guild.text_channels:
            channels_info['text_channels'].append({
                'name': channel.name,
                'id': channel.id,
                'category': channel.category.name if channel.category else "Sans catégorie",
                'topic': channel.topic or "Aucun sujet",
                'position': channel.position,
                'nsfw': channel.nsfw,
                'slowmode': channel.slowmode_delay
            })

        for channel in guild.voice_channels:
            channels_info['voice_channels'].append({
                'name': channel.name,
                'id': channel.id,
                'category': channel.category.name if channel.category else "Sans catégorie",
                'user_limit': channel.user_limit or "Illimité",
                'bitrate': channel.bitrate,
                'connected_members': len(channel.members)
            })

        # Statistiques d'activité (depuis les logs)
        activity_stats = {
            'total_logs': 0,
            'recent_activity': [],
            'command_usage': 0
        }

        # Filtrer les logs pour ce serveur
        server_logs = [log for log in bot_logs if log.get(
            'extra_data', {}).get('guild_id') == server_id]
        activity_stats['total_logs'] = len(server_logs)
        activity_stats['recent_activity'] = server_logs[-5:] if server_logs else []

        return render_template('server_details.html',
                               server=server_info,
                               permissions=permissions_list,
                               roles=roles_info,
                               channels=channels_info,
                               activity=activity_stats,
                               admin=session.get('admin_username'))

    except Exception as e:
        logger.log(
            'ERROR', f'Erreur lors de la récupération des détails du serveur {server_id}: {str(e)}')
        flash(
            f'Erreur lors de la récupération des détails du serveur: {str(e)}', 'error')
        return redirect(url_for('control'))


@app.route('/control/leave_server', methods=['POST'])
def leave_server():
    """API pour faire quitter le bot d'un serveur"""
    try:
        data = request.json
        server_id = int(data.get('server_id'))
        confirmation = data.get('confirmation', '').strip()

        logger.log(
            'INFO', f'Tentative de sortie du serveur {server_id} par {session.get("admin_username")}')

        if confirmation != 'CONFIRMER':
            return jsonify({'success': False, 'message': 'Confirmation requise'})

        if not bot_instance:
            return jsonify({'success': False, 'message': 'Bot non connecté'})

        # Trouver le serveur
        guild = bot_instance.get_guild(server_id)
        if not guild:
            return jsonify({'success': False, 'message': 'Serveur non trouvé'})

        guild_name = guild.name
        logger.log('INFO', f'Serveur trouvé: {guild_name} (ID: {server_id})')

        # Programmer la tâche pour quitter le serveur
        import asyncio
        import concurrent.futures

        def leave_guild_sync():
            """Fonction synchrone pour gérer la sortie de serveur"""
            try:
                # Utiliser asyncio.run_coroutine_threadsafe pour exécuter dans l'event loop du bot
                loop = bot_instance.loop
                if loop and loop.is_running():
                    # Créer une tâche dans l'event loop du bot
                    future = asyncio.run_coroutine_threadsafe(
                        guild.leave(), loop)
                    # Attendre le résultat avec un timeout
                    future.result(timeout=10)
                    return True
                else:
                    # Si le loop n'est pas disponible, essayer avec un nouveau loop
                    asyncio.run(guild.leave())
                    return True
            except Exception as e:
                logger.log(
                    'ERROR', f'Erreur lors de la sortie du serveur {guild_name}: {str(e)}')
                return False

        # Exécuter dans un thread séparé pour éviter de bloquer Flask
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(leave_guild_sync)
            try:
                success = future.result(timeout=15)  # Timeout de 15 secondes
            except concurrent.futures.TimeoutError:
                logger.log(
                    'ERROR', f'Timeout lors de la sortie du serveur {guild_name}')
                return jsonify({'success': False, 'message': 'Timeout lors de la sortie du serveur'})

        if success:
            logger.log('WARNING', f'Bot quitté du serveur: {guild_name}',
                       {'admin': session.get('admin_username'), 'server_id': server_id})
            return jsonify({'success': True, 'message': f'Quitté le serveur {guild_name}'})
        else:
            return jsonify({'success': False, 'message': 'Erreur lors de la sortie du serveur'})

    except ValueError:
        return jsonify({'success': False, 'message': 'ID de serveur invalide'})
    except Exception as e:
        logger.log('ERROR', f'Erreur API leave_server: {str(e)}')
        return jsonify({'success': False, 'message': f'Erreur inattendue: {str(e)}'})


@app.route('/control/bot_command', methods=['POST'])
def bot_command():
    """API pour exécuter des commandes sur le bot"""
    try:
        data = request.json
        command = data.get('command')

        if not bot_instance:
            return jsonify({'success': False, 'message': 'Bot non connecté'})

        admin_user = session.get('admin_username')

        if command == 'sync':
            # Synchroniser les commandes slash
            import asyncio

            async def sync_commands():
                try:
                    synced = await bot_instance.tree.sync()
                    return len(synced)
                except Exception as e:
                    return str(e)

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(sync_commands())
            loop.close()

            if isinstance(result, int):
                logger.log('SUCCESS', f'{result} commandes slash synchronisées',
                           {'admin': admin_user})
                return jsonify({'success': True, 'message': f'{result} commandes synchronisées'})
            else:
                logger.log('ERROR', f'Erreur sync commandes: {result}',
                           {'admin': admin_user})
                return jsonify({'success': False, 'message': f'Erreur: {result}'})

        elif command == 'reload_modules':
            logger.log('INFO', 'Rechargement des modules demandé',
                       {'admin': admin_user})
            return jsonify({'success': True, 'message': 'Rechargement des modules initié'})

        elif command == 'clear_cache':
            # Vider les caches internes
            detailed_stats['commands_by_hour'].clear()
            detailed_stats['errors_by_type'].clear()
            detailed_stats['server_activity'].clear()
            detailed_stats['daily_users'].clear()

            logger.log('INFO', 'Cache vidé', {'admin': admin_user})
            return jsonify({'success': True, 'message': 'Cache vidé avec succès'})

        elif command == 'sync_commands':
            # Même que 'sync' mais avec un nom différent
            return bot_command_sync()

        elif command == 'update_stats':
            # Mettre à jour les statistiques
            if bot_instance:
                update_bot_stats(
                    connected_servers=len(bot_instance.guilds),
                    total_users=len(bot_instance.users),
                    status='online' if bot_instance.is_ready() else 'connecting'
                )
            logger.log('INFO', 'Statistiques mises à jour',
                       {'admin': admin_user})
            return jsonify({'success': True, 'message': 'Statistiques mises à jour'})

        else:
            return jsonify({'success': False, 'message': 'Commande inconnue'})

    except Exception as e:
        logger.log('ERROR', f'Erreur API bot_command: {str(e)}')
        return jsonify({'success': False, 'message': str(e)})


@app.route('/api/bot_info')
def api_bot_info():
    """API pour récupérer les informations détaillées du bot"""
    if not bot_instance:
        return jsonify({'error': 'Bot non connecté'})

    try:
        uptime = 0
        uptime_str = "Non disponible"
        if bot_stats['start_time']:
            try:
                uptime_delta = datetime.now() - bot_stats['start_time']
                uptime = uptime_delta.total_seconds()
                days = uptime_delta.days
                hours, remainder = divmod(uptime_delta.seconds, 3600)
                minutes, _ = divmod(remainder, 60)
                uptime_str = f"{days}j {hours}h {minutes}m" if days > 0 else f"{hours}h {minutes}m"
            except TypeError:
                # Problème de timezone
                bot_stats['start_time'] = datetime.now()
                uptime = 0
                uptime_str = "Redémarré"

        return jsonify({
            'name': bot_instance.user.name,
            'id': bot_instance.user.id,
            'discriminator': bot_instance.user.discriminator,
            'avatar': bot_instance.user.avatar.url if bot_instance.user.avatar else None,
            'guild_count': len(bot_instance.guilds),
            'user_count': len(bot_instance.users),
            'command_count': bot_stats['commands_used'],
            'latency': round(bot_instance.latency * 1000, 2),
            'start_time': bot_stats['start_time'].strftime('%d/%m/%Y %H:%M:%S') if bot_stats['start_time'] else 'Inconnu',
            'uptime': uptime_str,
            'last_activity': bot_stats['last_activity'].strftime('%d/%m/%Y %H:%M:%S') if bot_stats['last_activity'] else 'Aucune'
        })

    except Exception as e:
        return jsonify({'error': str(e)})


def bot_command_sync():
    """Fonction helper pour synchroniser les commandes"""
    try:
        if not bot_instance:
            return jsonify({'success': False, 'message': 'Bot non connecté'})

        import asyncio

        async def sync_commands():
            try:
                synced = await bot_instance.tree.sync()
                return len(synced)
            except Exception as e:
                return str(e)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(sync_commands())
        loop.close()

        if isinstance(result, int):
            logger.log('SUCCESS', f'{result} commandes slash synchronisées')
            return jsonify({'success': True, 'message': f'{result} commandes synchronisées'})
        else:
            logger.log('ERROR', f'Erreur sync commandes: {result}')
            return jsonify({'success': False, 'message': f'Erreur: {result}'})

    except Exception as e:
        logger.log('ERROR', f'Erreur bot_command_sync: {str(e)}')
        return jsonify({'success': False, 'message': str(e)})


def start_web_panel(bot_instance_param=None, host='127.0.0.1', port=8080):
    """Démarre le panel web dans un thread séparé"""
    global bot_instance
    bot_instance = bot_instance_param
    bot_stats['start_time'] = datetime.now()

    if bot_instance:
        logger.update_stats(bot_instance)

    logger.log('INFO', f'Panel web démarré sur http://{host}:{port}')

    # Démarrer Flask dans un thread séparé
    def run_flask():
        app.run(host=host, port=port, debug=False, use_reloader=False)

    web_thread = threading.Thread(target=run_flask)
    web_thread.daemon = True
    web_thread.start()

    return web_thread

# Fonction pour être utilisée par le bot Discord


def log_bot_event(level, message, **kwargs):
    """Interface pour que le bot Discord puisse logger des événements"""
    logger.log(level, message, kwargs)


def update_bot_stats(**kwargs):
    """Interface pour mettre à jour les statistiques du bot"""
    for key, value in kwargs.items():
        if key in bot_stats:
            bot_stats[key] = value

    # Incrémenter le compteur de commandes
    if 'command_used' in kwargs:
        bot_stats['commands_used'] += 1
        current_hour = datetime.now().hour
        detailed_stats['commands_by_hour'][current_hour] += 1


def get_status_rotator_info():
    """Récupère les informations du système de rotation des statuts"""
    print(f"🔍 DEBUG get_status_rotator_info: bot_instance = {bot_instance}")

    if not bot_instance or not hasattr(bot_instance, 'status_rotator'):
        print(f"🔍 DEBUG: pas de bot_instance ou pas d'attribut status_rotator")
        return None

    rotator = bot_instance.status_rotator
    print(f"🔍 DEBUG: rotator = {rotator}")

    if not rotator:
        print(f"🔍 DEBUG: rotator est None")
        return None

    try:
        print(f"🔍 DEBUG: tentative d'appel get_current_status_info()")
        current_info = rotator.get_current_status_info()
        print(f"🔍 DEBUG: current_info = {current_info}")

        rotation_active = rotator.rotation_task and not rotator.rotation_task.done()
        print(f"🔍 DEBUG: rotation_active = {rotation_active}")

        result = {
            'current_status': current_info,
            'rotation_active': rotation_active,
            'rotation_interval': rotator.rotation_interval,
            'total_statuses': len(rotator.statuses),
            'special_statuses': list(rotator.special_statuses.keys())
        }
        print(f"🔍 DEBUG: result = {result}")
        return result
    except Exception as e:
        print(f"❌ ERROR get_status_rotator_info: {str(e)}")
        import traceback
        traceback.print_exc()
        return {'error': str(e)}


# ===============================================
# SYSTÈME DE SUPPORT - ROUTES PUBLIQUES
# ===============================================

# Importer le système de support

# Initialiser la base de données de support
support_db = SupportDB()


@app.route('/test-notifier')
def test_notifier():
    """Route de test pour vérifier l'état du notificateur"""
    try:
        from core.support_notifier import support_notifier
        status = {
            'bot_configured': support_notifier.bot is not None,
            'bot_ready': support_notifier.bot.is_ready() if support_notifier.bot else False,
            'admin_user_ids': support_notifier.admin_user_ids,
            'bot_type': str(type(support_notifier.bot)) if support_notifier.bot else None
        }
        return f"""
        <h1>Test Notificateur</h1>
        <ul>
            <li>Bot configuré: {status['bot_configured']}</li>
            <li>Bot prêt: {status['bot_ready']}</li>
            <li>Admin User IDs: {status['admin_user_ids']}</li>
            <li>Type du bot: {status['bot_type']}</li>
        </ul>
        """
    except Exception as e:
        return f"Erreur: {e}"


@app.route('/support')
def support_home():
    """Page d'accueil du support (publique)"""
    # Statistiques publiques
    stats = {
        'total_tickets': support_db.get_total_tickets(),
        'resolved_tickets': support_db.get_resolved_tickets_count(),
        'active_users': support_db.get_active_users_count(),
        'avg_response_time': '< 24h'  # Statique pour le moment
    }

    return render_template('support_home.html', stats=stats)


@app.route('/support/register', methods=['GET', 'POST'])
def support_register():
    """Inscription au système de support"""
    if request.method == 'POST':
        try:
            username = request.form.get('username', '').strip()
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')
            confirm_password = request.form.get('confirm_password', '')
            discord_username = request.form.get('discord_username', '').strip()
            discord_id = request.form.get('discord_id', '').strip()

            # Validation
            if not username or not email or not password:
                flash('Veuillez remplir tous les champs obligatoires.', 'error')
                return render_template('support_register.html')

            if password != confirm_password:
                flash('Les mots de passe ne correspondent pas.', 'error')
                return render_template('support_register.html')

            if len(password) < 6:
                flash('Le mot de passe doit contenir au moins 6 caractères.', 'error')
                return render_template('support_register.html')

            # Vérifier si l'utilisateur existe déjà
            if support_db.get_user_by_username(username):
                flash('Ce nom d\'utilisateur est déjà pris.', 'error')
                return render_template('support_register.html')

            if support_db.get_user_by_email(email):
                flash('Cette adresse email est déjà utilisée.', 'error')
                return render_template('support_register.html')

            # Créer l'utilisateur
            user_id = support_db.create_user(
                username=username,
                email=email,
                password=password,
                discord_username=discord_username if discord_username else None,
                discord_id=discord_id if discord_id else None
            )

            if user_id:
                flash(
                    'Compte créé avec succès ! Vous pouvez maintenant vous connecter.', 'success')
                return redirect(url_for('support_login'))
            else:
                flash(
                    'Erreur lors de la création du compte. Veuillez réessayer.', 'error')

        except Exception as e:
            flash(f'Erreur lors de l\'inscription : {str(e)}', 'error')
            logger.log('ERROR', f'Erreur inscription support: {str(e)}')

    return render_template('support_register.html')


@app.route('/support/login', methods=['GET', 'POST'])
def support_login():
    """Connexion au système de support"""
    if request.method == 'POST':
        try:
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '')
            remember_me = request.form.get('remember_me') == '1'

            if not username or not password:
                flash('Veuillez remplir tous les champs.', 'error')
                return render_template('support_login.html')

            # Authentification (peut être username ou email)
            user = support_db.authenticate_user(username, password)

            if user:
                # Connexion réussie
                session['support_user'] = {
                    'id': user['id'],
                    'username': user['username'],
                    'email': user['email'],
                    'discord_username': user['discord_username'],
                    'discord_id': user['discord_id']
                }

                if remember_me:
                    session.permanent = True
                    app.permanent_session_lifetime = timedelta(days=30)

                flash(f'Bienvenue, {user["username"]} !', 'success')
                return redirect(url_for('support_dashboard'))
            else:
                flash('Nom d\'utilisateur/email ou mot de passe incorrect.', 'error')

        except Exception as e:
            flash(f'Erreur lors de la connexion : {str(e)}', 'error')
            logger.log('ERROR', f'Erreur connexion support: {str(e)}')

    return render_template('support_login.html')


@app.route('/support/logout')
def support_logout():
    """Déconnexion du système de support"""
    if 'support_user' in session:
        username = session['support_user']['username']
        session.pop('support_user', None)
        flash(f'À bientôt, {username} !', 'info')

    return redirect(url_for('support_home'))


@app.route('/support/dashboard')
def support_dashboard():
    """Tableau de bord utilisateur du support"""
    if 'support_user' not in session:
        return redirect(url_for('support_login'))

    user_id = session['support_user']['id']

    # Statistiques utilisateur
    user_tickets = support_db.get_user_tickets(user_id)
    stats = {
        'total_tickets': len(user_tickets),
        'open_tickets': len([t for t in user_tickets if t['status'] in ['open', 'in_progress']]),
        'resolved_tickets': len([t for t in user_tickets if t['status'] == 'resolved']),
        'pending_responses': len([t for t in user_tickets if t['status'] == 'waiting_user'])
    }

    # Tickets récents (5 derniers)
    recent_tickets = user_tickets[:5]

    # Notifications (placeholder)
    notifications = []

    return render_template('support_dashboard.html',
                           stats=stats,
                           recent_tickets=recent_tickets,
                           notifications=notifications)


@app.route('/support/ticket/new', methods=['GET', 'POST'])
def support_ticket_new():
    """Créer un nouveau ticket de support"""
    if 'support_user' not in session:
        return redirect(url_for('support_login'))

    if request.method == 'POST':
        try:
            user_id = session['support_user']['id']

            # Récupérer les données du formulaire
            category = request.form.get('category', '').strip()
            priority = request.form.get('priority', 'medium')
            subject = request.form.get('subject', '').strip()
            description = request.form.get('description', '').strip()
            steps_to_reproduce = request.form.get(
                'steps_to_reproduce', '').strip()
            server_id = request.form.get('server_id', '').strip()
            command_used = request.form.get('command_used', '').strip()
            error_message = request.form.get('error_message', '').strip()
            urgent_contact = request.form.get('urgent_contact') == '1'
            email_notifications = request.form.get(
                'email_notifications') == '1'

            # Validation
            if not category or not subject or not description:
                flash('Veuillez remplir tous les champs obligatoires.', 'error')
                return render_template('support_ticket_new.html')

            if len(description) < 20:
                flash('La description doit contenir au moins 20 caractères.', 'error')
                return render_template('support_ticket_new.html')

            # Préparer les métadonnées
            metadata = {
                'steps_to_reproduce': steps_to_reproduce,
                'server_id': server_id,
                'command_used': command_used,
                'error_message': error_message,
                'urgent_contact': urgent_contact,
                'email_notifications': email_notifications
            }

            # Créer le ticket
            ticket_id = support_db.create_ticket(
                user_id=user_id,
                category=category,
                priority=priority,
                subject=subject,
                description=description,
                metadata=metadata
            )

            if ticket_id:
                # TODO: Envoyer notification Discord à l'admin
                logger.log('INFO', f'Nouveau ticket créé: #{ticket_id}', {
                    'user': session['support_user']['username'],
                    'category': category,
                    'priority': priority
                })

                flash(
                    f'Ticket #{ticket_id} créé avec succès ! Nous vous répondrons dans les plus brefs délais.', 'success')
                return redirect(url_for('support_ticket_view', ticket_id=ticket_id))
            else:
                flash(
                    'Erreur lors de la création du ticket. Veuillez réessayer.', 'error')

        except Exception as e:
            flash(f'Erreur lors de la création du ticket : {str(e)}', 'error')
            logger.log('ERROR', f'Erreur création ticket: {str(e)}')

    return render_template('support_ticket_new.html')


@app.route('/support/ticket/<int:ticket_id>')
def support_ticket_view(ticket_id):
    """Voir un ticket spécifique"""
    if 'support_user' not in session:
        return redirect(url_for('support_login'))

    user_id = session['support_user']['id']

    # Récupérer le ticket
    ticket = support_db.get_ticket_by_id(ticket_id)

    if not ticket or ticket['user_id'] != user_id:
        flash('Ticket non trouvé ou accès non autorisé.', 'error')
        return redirect(url_for('support_dashboard'))

    # Récupérer les réponses
    responses = support_db.get_ticket_responses(ticket_id)

    return render_template('support_ticket_view.html',
                           ticket=ticket,
                           responses=responses)

# Fonction utilitaire pour les templates


@app.template_filter('timeago')
def timeago_filter(dt):
    """Filtre pour afficher le temps relatif"""
    if isinstance(dt, str):
        try:
            dt = datetime.fromisoformat(dt.replace('Z', '+00:00'))
        except:
            return dt

    now = datetime.now()
    if dt.tzinfo:
        now = now.replace(tzinfo=dt.tzinfo)

    diff = now - dt

    if diff.days > 0:
        return f"il y a {diff.days} jour{'s' if diff.days > 1 else ''}"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"il y a {hours} heure{'s' if hours > 1 else ''}"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"il y a {minutes} minute{'s' if minutes > 1 else ''}"
    else:
        return "à l'instant"


@app.route('/support/tickets')
def support_tickets():
    """Liste de tous les tickets de l'utilisateur"""
    if 'support_user' not in session:
        return redirect(url_for('support_login'))

    user_id = session['support_user']['id']

    # Filtres
    status_filter = request.args.get('status', '')
    priority_filter = request.args.get('priority', '')
    category_filter = request.args.get('category', '')
    search_filter = request.args.get('search', '')

    # Récupérer tous les tickets de l'utilisateur
    all_tickets = support_db.get_user_tickets(user_id)

    # Appliquer les filtres
    filtered_tickets = all_tickets

    if status_filter:
        filtered_tickets = [
            t for t in filtered_tickets if t['status'] == status_filter]

    if priority_filter:
        filtered_tickets = [
            t for t in filtered_tickets if t['priority'] == priority_filter]

    if category_filter:
        filtered_tickets = [
            t for t in filtered_tickets if t['category'] == category_filter]

    if search_filter:
        filtered_tickets = [t for t in filtered_tickets
                            if search_filter.lower() in t['subject'].lower()]

    # Statistiques
    total_tickets = len(all_tickets)
    open_tickets = len([t for t in all_tickets if t['status'] == 'open'])
    in_progress_tickets = len(
        [t for t in all_tickets if t['status'] == 'in_progress'])
    resolved_tickets = len(
        [t for t in all_tickets if t['status'] == 'resolved'])

    return render_template('support_tickets.html',
                           tickets=filtered_tickets,
                           total_tickets=total_tickets,
                           open_tickets=open_tickets,
                           in_progress_tickets=in_progress_tickets,
                           resolved_tickets=resolved_tickets)


@app.route('/support/ticket/<int:ticket_id>/respond', methods=['POST'])
def support_ticket_respond(ticket_id):
    """Ajouter une réponse à un ticket"""
    if 'support_user' not in session:
        return redirect(url_for('support_login'))

    user_id = session['support_user']['id']

    # Vérifier que le ticket appartient à l'utilisateur
    ticket = support_db.get_ticket_by_id(ticket_id)
    if not ticket or ticket['user_id'] != user_id:
        flash('Ticket non trouvé ou accès non autorisé.', 'error')
        return redirect(url_for('support_dashboard'))

    try:
        message = request.form.get('message', '').strip()
        mark_resolved = request.form.get('mark_resolved') == '1'

        if not message:
            flash('Veuillez saisir une réponse.', 'error')
            return redirect(url_for('support_ticket_view', ticket_id=ticket_id))

        # Ajouter la réponse
        response_id = support_db.add_ticket_response(
            ticket_id=ticket_id,
            message=message,
            is_admin=False
        )

        if response_id:
            # Mettre à jour le statut si demandé
            if mark_resolved:
                support_db.update_ticket_status(ticket_id, 'resolved')
                flash(
                    'Votre réponse a été ajoutée et le ticket marqué comme résolu.', 'success')
            else:
                # Remettre en attente de réponse admin
                support_db.update_ticket_status(ticket_id, 'waiting_admin')
                flash(
                    'Votre réponse a été ajoutée. Notre équipe vous répondra bientôt.', 'success')

            logger.log('INFO', f'Réponse ajoutée au ticket #{ticket_id}', {
                'user': session['support_user']['username'],
                'resolved': mark_resolved
            })
        else:
            flash('Erreur lors de l\'ajout de la réponse.', 'error')

    except Exception as e:
        flash(f'Erreur lors de l\'ajout de la réponse : {str(e)}', 'error')
        logger.log('ERROR', f'Erreur ajout réponse ticket: {str(e)}')

    return redirect(url_for('support_ticket_view', ticket_id=ticket_id))

# ===============================================
# ROUTES D'ADMINISTRATION DES NOTIFICATIONS
# ===============================================


@app.route('/admin/notifications')
def admin_notifications():
    """Interface d'administration des notifications Discord"""
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))

    try:
        from core.support_notifier import support_notifier

        # Vérifier le statut du système de notifications
        notification_status = {
            'bot_connected': bot_instance is not None,
            'notifier_ready': support_notifier.bot is not None,
            'admin_user_ids': support_notifier.admin_user_ids,
            'last_notification': None  # TODO: implémenter le suivi
        }

        return render_template('admin_notifications.html',
                               status=notification_status,
                               logs=bot_logs[-50:])  # Derniers 50 logs
    except ImportError:
        flash('Module de notifications non disponible', 'error')
        return redirect(url_for('admin'))
    except Exception as e:
        flash(
            f'Erreur lors du chargement des notifications: {str(e)}', 'error')
        return redirect(url_for('admin'))


@app.route('/admin/test-notification', methods=['POST'])
def admin_test_notification():
    """Test d'envoi de notification Discord"""
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))

    try:
        from core.support_notifier import support_notifier

        # Données de test
        test_ticket_data = {
            'ticket_id': 'TEST',
            'username': 'Admin Test',
            'email': 'admin@test.com',
            'category': 'test',
            'priority': 'medium',
            'subject': 'Test de notification Discord',
            'description': 'Ceci est un test manuel du système de notifications Discord depuis le panel d\'administration.'
        }

        # Programmer l'envoi de la notification de test
        import threading

        def send_test_notification():
            try:
                import asyncio
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(
                    support_notifier.send_new_ticket_notification(
                        test_ticket_data)
                )
                loop.close()

                if result:
                    logger.log(
                        'SUCCESS', 'Test de notification Discord réussi')
                else:
                    logger.log(
                        'ERROR', 'Échec du test de notification Discord')
            except Exception as e:
                logger.log('ERROR', f'Erreur test notification: {str(e)}')

        test_thread = threading.Thread(
            target=send_test_notification, daemon=True)
        test_thread.start()

        flash(
            'Test de notification Discord programmé. Vérifiez vos messages privés.', 'info')
        logger.log('INFO', 'Test de notification Discord lancé par admin')

    except ImportError:
        flash('Module de notifications non disponible', 'error')
    except Exception as e:
        flash(f'Erreur lors du test: {str(e)}', 'error')
        logger.log('ERROR', f'Erreur test notification admin: {str(e)}')

    return redirect(url_for('admin_notifications'))

# ===============================================
# ADMINISTRATION DES TICKETS DE SUPPORT
# ===============================================


@app.route('/admin/tickets')
def admin_tickets():
    """Interface d'administration pour gérer tous les tickets de support"""
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))

    try:
        from core.support_db import support_db

        # Récupérer tous les tickets avec les informations utilisateur
        tickets = support_db.get_all_tickets_for_admin()

        # Statistiques des tickets
        stats = {
            'total': len(tickets),
            'open': len([t for t in tickets if t['status'] == 'open']),
            'waiting_admin': len([t for t in tickets if t['status'] == 'waiting_admin']),
            'resolved': len([t for t in tickets if t['status'] == 'resolved']),
            'closed': len([t for t in tickets if t['status'] == 'closed'])
        }

        return render_template('admin_tickets.html',
                               tickets=tickets,
                               stats=stats,
                               admin=session.get('admin_username'))

    except Exception as e:
        flash(f'Erreur lors du chargement des tickets: {str(e)}', 'error')
        logger.log('ERROR', f'Erreur admin tickets: {str(e)}')
        return redirect(url_for('dashboard'))


@app.route('/admin/ticket/<int:ticket_id>')
def admin_ticket_view(ticket_id):
    """Vue détaillée d'un ticket pour l'admin avec possibilité de répondre"""
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))

    try:
        support_db = SupportDB()

        # Récupérer le ticket avec les informations utilisateur
        ticket = support_db.get_ticket_by_id(ticket_id)
        if not ticket:
            flash('Ticket non trouvé.', 'error')
            return redirect(url_for('admin_tickets'))

        # Récupérer les réponses du ticket
        responses = support_db.get_ticket_responses(ticket_id)

        return render_template('admin_ticket_view.html',
                               ticket=ticket,
                               responses=responses,
                               admin=session.get('admin_username'))

    except Exception as e:
        flash(f'Erreur lors du chargement du ticket: {str(e)}', 'error')
        logger.log('ERROR', f'Erreur admin ticket view: {str(e)}')
        return redirect(url_for('admin_tickets'))


@app.route('/admin/ticket/<int:ticket_id>/respond', methods=['POST'])
def admin_ticket_respond(ticket_id):
    """Ajouter une réponse admin à un ticket"""
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))

    try:
        support_db = SupportDB()
        message = request.form.get('message', '').strip()
        new_status = request.form.get('status', 'waiting_user')

        if not message:
            flash('Veuillez saisir une réponse.', 'error')
            return redirect(url_for('admin_ticket_view', ticket_id=ticket_id))

        # Ajouter la réponse admin
        response_id = support_db.add_ticket_response(
            ticket_id=ticket_id,
            message=message,
            is_admin=True
        )

        if response_id:
            # Mettre à jour le statut du ticket
            support_db.update_ticket_status(ticket_id, new_status)

            flash('Votre réponse a été ajoutée avec succès.', 'success')
            logger.log('INFO', f'Réponse admin ajoutée au ticket #{ticket_id}', {
                'admin': session['admin_username'],
                'new_status': new_status
            })

            # TODO: Envoyer une notification à l'utilisateur (email ou Discord)

        else:
            flash('Erreur lors de l\'ajout de la réponse.', 'error')

    except Exception as e:
        flash(f'Erreur lors de l\'ajout de la réponse: {str(e)}', 'error')
        logger.log('ERROR', f'Erreur admin réponse: {str(e)}')

    return redirect(url_for('admin_ticket_view', ticket_id=ticket_id))


@app.route('/admin/ticket/<int:ticket_id>/status', methods=['POST'])
def admin_ticket_status(ticket_id):
    """Changer le statut d'un ticket"""
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))

    try:
        support_db = SupportDB()
        new_status = request.form.get('status')

        if new_status in ['open', 'waiting_admin', 'waiting_user', 'resolved', 'closed']:
            support_db.update_ticket_status(ticket_id, new_status)
            flash(f'Statut du ticket mis à jour : {new_status}', 'success')
            logger.log('INFO', f'Statut ticket #{ticket_id} changé', {
                'admin': session['admin_username'],
                'new_status': new_status
            })
        else:
            flash('Statut invalide.', 'error')

    except Exception as e:
        flash(f'Erreur lors du changement de statut: {str(e)}', 'error')
        logger.log('ERROR', f'Erreur changement statut: {str(e)}')

    return redirect(url_for('admin_ticket_view', ticket_id=ticket_id))


@app.route('/admin/ticket/<int:ticket_id>/delete', methods=['POST'])
def admin_ticket_delete(ticket_id):
    """Supprimer un ticket spécifique"""
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))

    try:
        from core.support_db import support_db

        # Vérifier que le ticket existe
        ticket = support_db.get_ticket_by_id(ticket_id)
        if not ticket:
            flash('Ticket introuvable.', 'error')
            return redirect(url_for('admin_tickets'))

        # Supprimer le ticket
        if support_db.delete_ticket(ticket_id):
            flash(
                f'Ticket #{ticket_id} "{ticket["subject"]}" supprimé avec succès.', 'success')
            logger.log('WARNING', f'Ticket #{ticket_id} supprimé', {
                'admin': session['admin_username'],
                'ticket_subject': ticket['subject']
            })
        else:
            flash('Erreur lors de la suppression du ticket.', 'error')

    except Exception as e:
        flash(f'Erreur lors de la suppression: {str(e)}', 'error')
        logger.log(
            'ERROR', f'Erreur suppression ticket #{ticket_id}: {str(e)}')

    return redirect(url_for('admin_tickets'))


@app.route('/admin/tickets/cleanup')
def admin_tickets_cleanup():
    """Page de nettoyage des anciens tickets"""
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))

    try:
        from core.support_db import support_db

        # Récupérer les tickets qui peuvent être supprimés
        old_tickets = support_db.get_tickets_for_deletion(
            status='closed', days_old=30)
        very_old_tickets = support_db.get_tickets_for_deletion(
            status='resolved', days_old=90)

        return render_template('admin_tickets_cleanup.html',
                               old_closed_tickets=old_tickets,
                               old_resolved_tickets=very_old_tickets,
                               stats={
                                   'old_closed_count': len(old_tickets),
                                   'old_resolved_count': len(very_old_tickets)
                               })

    except Exception as e:
        flash(f'Erreur lors du chargement: {str(e)}', 'error')
        logger.log('ERROR', f'Erreur cleanup page: {str(e)}')
        return redirect(url_for('admin_tickets'))


@app.route('/admin/tickets/cleanup/execute', methods=['POST'])
def admin_tickets_cleanup_execute():
    """Exécuter le nettoyage des anciens tickets"""
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))

    try:
        from core.support_db import support_db

        cleanup_type = request.form.get('cleanup_type')

        if cleanup_type == 'closed_30':
            # Supprimer les tickets fermés de plus de 30 jours
            deleted_count = support_db.delete_old_tickets(
                status='closed', days_old=30)
            flash(
                f'{deleted_count} ticket(s) fermé(s) de plus de 30 jours supprimé(s).', 'success')

        elif cleanup_type == 'resolved_90':
            # Supprimer les tickets résolus de plus de 90 jours
            deleted_count = support_db.delete_old_tickets(
                status='resolved', days_old=90)
            flash(
                f'{deleted_count} ticket(s) résolu(s) de plus de 90 jours supprimé(s).', 'success')

        elif cleanup_type == 'all_old':
            # Supprimer tous les anciens tickets
            deleted_closed = support_db.delete_old_tickets(
                status='closed', days_old=30)
            deleted_resolved = support_db.delete_old_tickets(
                status='resolved', days_old=90)
            total_deleted = deleted_closed + deleted_resolved
            flash(f'{total_deleted} ancien(s) ticket(s) supprimé(s) ({deleted_closed} fermés, {deleted_resolved} résolus).', 'success')

        else:
            flash('Type de nettoyage invalide.', 'error')

        logger.log('WARNING', f'Nettoyage des tickets exécuté', {
            'admin': session['admin_username'],
            'type': cleanup_type
        })

    except Exception as e:
        flash(f'Erreur lors du nettoyage: {str(e)}', 'error')
        logger.log('ERROR', f'Erreur cleanup execute: {str(e)}')

    return redirect(url_for('admin_tickets_cleanup'))


# ===============================================
# FIN DU SYSTÈME DE SUPPORT
# ===============================================


if __name__ == '__main__':
    # Test du panel web
    print("🌐 Démarrage du panel web de test...")
    start_web_panel(host='127.0.0.1', port=8080)

    # Ajouter quelques logs de test
    logger.log('INFO', 'Panel web démarré')
    logger.log('SUCCESS', 'Bot connecté à Discord')
    logger.log('WARNING', 'Tentative de commande non autorisée')
    logger.log('ERROR', 'Erreur de connexion à la base de données',
               {'error_type': 'DatabaseError'})

    print("Panel web accessible sur: http://127.0.0.1:8080")
    print("Identifiants par défaut: admin / admin123")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🔴 Arrêt du panel web")
