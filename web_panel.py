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

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-super-secret-key-here')

# Configuration des admins (en production, utiliser une base de données)
ADMIN_CREDENTIALS = {
    'admin': generate_password_hash('admin123'),  # Changez ce mot de passe !
    # Ajoutez d'autres admins si besoin
    'owner': generate_password_hash('securepass2025')
}

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
            detailed_stats['errors_by_type'][extra_data.get(
                'error_type', 'Unknown')] += 1

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


def start_web_panel(bot_instance=None, host='127.0.0.1', port=8080):
    """Démarre le panel web dans un thread séparé"""
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
