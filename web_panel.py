"""
Panel Web d'Administration pour le Bot Discord
Interface web sécurisée pour surveiller les logs et statistiques
"""
from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
import json
import os
import threading
import time
from collections import defaultdict
import discord

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
    """Vérifie l'authentification pour toutes les routes sauf login"""
    if request.endpoint not in ['login', 'static'] and 'admin_logged_in' not in session:
        return redirect(url_for('login'))


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


@app.route('/')
def dashboard():
    """Dashboard principal"""
    # Calculer l'uptime
    uptime = None
    if bot_stats['start_time']:
        uptime = datetime.now() - bot_stats['start_time']

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
    return jsonify({
        'status': bot_stats['status'],
        'servers': bot_stats['connected_servers'],
        'users': bot_stats['total_users'],
        'commands': bot_stats['commands_used'],
        'errors': bot_stats['errors_count'],
        'last_activity': bot_stats['last_activity'].isoformat() if bot_stats['last_activity'] else None,
        'uptime': (datetime.now() - bot_stats['start_time']).total_seconds() if bot_stats['start_time'] else 0
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
                'joined_at': guild.me.joined_at.strftime('%d/%m/%Y') if guild.me.joined_at else "Inconnu",
                'premium_tier': guild.premium_tier,
                'icon_url': guild.icon.url if guild.icon else None,
                'is_owner': guild.owner_id == bot_instance.user.id
            }
            servers.append(server_info)

        # Calculer l'uptime
        if bot_stats['start_time']:
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
            'created_at': guild.created_at.strftime('%d/%m/%Y à %H:%M'),
            'joined_at': guild.me.joined_at.strftime('%d/%m/%Y à %H:%M') if guild.me.joined_at else "Inconnu",
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
            uptime_delta = datetime.now() - bot_stats['start_time']
            uptime = uptime_delta.total_seconds()
            days = uptime_delta.days
            hours, remainder = divmod(uptime_delta.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            uptime_str = f"{days}j {hours}h {minutes}m" if days > 0 else f"{hours}h {minutes}m"

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
