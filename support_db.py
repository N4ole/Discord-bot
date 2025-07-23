"""
Système de Support - Base de données SQLite
Gestion des utilisateurs et tickets de support
"""
import sqlite3
import hashlib
import secrets
import json
from datetime import datetime
import os
import threading


class SupportDB:
    def __init__(self, db_path="support.db"):
        self.db_path = db_path
        self.conn = None
        self.init_database()

    def init_database(self):
        """Initialise la base de données avec les tables nécessaires"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        # Pour avoir des résultats sous forme de dictionnaire
        self.conn.row_factory = sqlite3.Row
        cursor = self.conn.cursor()

        # Table des utilisateurs du support
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS support_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            discord_id TEXT,
            discord_username TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT 1
        )
        ''')

        # Table des tickets de support
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS support_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_number INTEGER UNIQUE NOT NULL,
            user_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            priority TEXT DEFAULT 'medium',
            subject TEXT NOT NULL,
            description TEXT NOT NULL,
            metadata TEXT,
            status TEXT DEFAULT 'open',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            discord_notified BOOLEAN DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES support_users (id)
        )
        ''')

        # Table pour gérer les compteurs séquentiels
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS support_counters (
            counter_name TEXT PRIMARY KEY,
            current_value INTEGER DEFAULT 0
        )
        ''')

        # Initialiser le compteur de tickets s'il n'existe pas
        cursor.execute('''
        INSERT OR IGNORE INTO support_counters (counter_name, current_value) 
        VALUES ('ticket_counter', 0)
        ''')

        # Table des réponses aux tickets
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS ticket_responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id INTEGER NOT NULL,
            message TEXT NOT NULL,
            is_admin BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (ticket_id) REFERENCES support_tickets (id)
        )
        ''')

        self.conn.commit()
        print("✅ Base de données initialisée avec succès")

    def hash_password(self, password):
        """Hache un mot de passe avec PBKDF2 et sel"""
        salt = secrets.token_hex(32)
        key = hashlib.pbkdf2_hmac('sha256', password.encode(
            'utf-8'), salt.encode('utf-8'), 100000)
        return salt + key.hex()

    def verify_password(self, password, hashed_password):
        """Vérifie un mot de passe"""
        salt = hashed_password[:64]
        stored_key = hashed_password[64:]
        key = hashlib.pbkdf2_hmac('sha256', password.encode(
            'utf-8'), salt.encode('utf-8'), 100000)
        return key.hex() == stored_key

    def create_user(self, username, email, password, discord_id=None, discord_username=None):
        """Crée un nouvel utilisateur"""
        try:
            password_hash = self.hash_password(password)
            cursor = self.conn.execute('''
            INSERT INTO support_users (username, email, password_hash, discord_id, discord_username)
            VALUES (?, ?, ?, ?, ?)
            ''', (username, email, password_hash, discord_id, discord_username))

            user_id = cursor.lastrowid
            self.conn.commit()
            print(f"✅ Utilisateur créé avec l'ID: {user_id}")
            return user_id
        except sqlite3.IntegrityError as e:
            print(f"❌ Erreur lors de la création d'utilisateur: {e}")
            return None
        except Exception as e:
            print(f"❌ Erreur inattendue: {e}")
            return None

    def authenticate_user(self, username_or_email, password):
        """Authentifie un utilisateur par nom d'utilisateur ou email"""
        try:
            cursor = self.conn.execute('''
            SELECT id, username, email, password_hash, discord_id, discord_username FROM support_users 
            WHERE (username = ? OR email = ?) AND is_active = 1
            ''', (username_or_email, username_or_email))

            user = cursor.fetchone()

            if user and self.verify_password(password, user['password_hash']):
                return {
                    'id': user['id'],
                    'username': user['username'],
                    'email': user['email'],
                    'discord_id': user['discord_id'],
                    'discord_username': user['discord_username']
                }
            return None
        except Exception as e:
            print(f"❌ Erreur lors de l'authentification: {e}")
            return None

    def get_next_ticket_number(self):
        """Récupère et incrémente le prochain numéro de ticket séquentiel"""
        try:
            cursor = self.conn.cursor()

            # Récupérer la valeur actuelle du compteur
            cursor.execute(
                'SELECT current_value FROM support_counters WHERE counter_name = ?', ('ticket_counter',))
            result = cursor.fetchone()

            if result:
                next_number = result['current_value'] + 1
            else:
                # Si le compteur n'existe pas, le créer
                next_number = 1
                cursor.execute('INSERT INTO support_counters (counter_name, current_value) VALUES (?, ?)',
                               ('ticket_counter', 0))

            # Mettre à jour le compteur
            cursor.execute('UPDATE support_counters SET current_value = ? WHERE counter_name = ?',
                           (next_number, 'ticket_counter'))

            self.conn.commit()
            return next_number

        except Exception as e:
            print(f"❌ Erreur lors de la récupération du numéro de ticket: {e}")
            self.conn.rollback()
            return None

    def reset_ticket_counter_if_needed(self):
        """Initialise le compteur en se basant sur les tickets existants (migration)"""
        try:
            cursor = self.conn.cursor()

            # Vérifier si la colonne ticket_number existe
            cursor.execute("PRAGMA table_info(support_tickets)")
            columns = [column[1] for column in cursor.fetchall()]

            if 'ticket_number' not in columns:
                # Ajouter la colonne ticket_number si elle n'existe pas
                cursor.execute(
                    'ALTER TABLE support_tickets ADD COLUMN ticket_number INTEGER')
                print("📋 Colonne ticket_number ajoutée à la table support_tickets")

            # Vérifier s'il y a des tickets sans numéro
            cursor.execute(
                'SELECT COUNT(*) as count FROM support_tickets WHERE ticket_number IS NULL')
            tickets_without_number = cursor.fetchone()['count']

            if tickets_without_number > 0:
                print(
                    f"🔄 Migration de {tickets_without_number} tickets sans numéro...")

                # Assigner des numéros séquentiels aux tickets existants
                cursor.execute(
                    'SELECT id FROM support_tickets WHERE ticket_number IS NULL ORDER BY created_at')
                tickets = cursor.fetchall()

                for i, ticket in enumerate(tickets, 1):
                    cursor.execute('UPDATE support_tickets SET ticket_number = ? WHERE id = ?',
                                   (i, ticket['id']))

                # Mettre à jour le compteur avec le prochain numéro disponible
                cursor.execute('UPDATE support_counters SET current_value = ? WHERE counter_name = ?',
                               (len(tickets), 'ticket_counter'))

                self.conn.commit()
                print(
                    f"✅ Migration terminée - {len(tickets)} tickets numérotés")

        except Exception as e:
            print(f"❌ Erreur lors de l'initialisation du compteur: {e}")
            self.conn.rollback()

    def create_ticket(self, user_id, category, priority, subject, description, metadata=None):
        """Crée un nouveau ticket de support avec numéro séquentiel"""
        try:
            # S'assurer que la migration est effectuée
            self.reset_ticket_counter_if_needed()

            # Obtenir le prochain numéro de ticket
            ticket_number = self.get_next_ticket_number()
            if not ticket_number:
                print("❌ Impossible d'obtenir un numéro de ticket")
                return None

            metadata_json = json.dumps(metadata) if metadata else None
            cursor = self.conn.execute('''
            INSERT INTO support_tickets (ticket_number, user_id, category, priority, subject, description, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (ticket_number, user_id, category, priority, subject, description, metadata_json))

            ticket_id = cursor.lastrowid
            self.conn.commit()
            print(
                f"✅ Ticket créé avec l'ID: {ticket_id}, Numéro: {ticket_number}")

            # Envoyer la notification Discord
            print(
                f"🔍 DEBUG: Appel de _send_discord_notification pour ticket {ticket_id}")
            self._send_discord_notification(
                ticket_id, user_id, category, priority, subject, description)

            return ticket_id
        except Exception as e:
            print(f"❌ Erreur lors de la création du ticket: {e}")
            return None

    def _send_discord_notification(self, ticket_id, user_id, category, priority, subject, description):
        """Envoie une notification Discord pour un nouveau ticket (non-bloquant)"""
        print(
            f"🔍 DEBUG: _send_discord_notification appelée pour ticket {ticket_id}")

        def notification_worker():
            print(
                f"🔍 DEBUG: notification_worker démarré pour ticket {ticket_id}")
            try:
                # Récupérer les informations de l'utilisateur et du ticket
                ticket_info = self.conn.execute('''
                    SELECT u.username, u.email, t.ticket_number 
                    FROM support_users u, support_tickets t 
                    WHERE u.id = ? AND t.id = ?
                ''', (user_id, ticket_id)).fetchone()

                print(
                    f"🔍 DEBUG: ticket_info récupéré: {dict(ticket_info) if ticket_info else None}")

                if ticket_info:
                    ticket_data = {
                        # Utiliser le numéro séquentiel
                        'ticket_id': ticket_info['ticket_number'],
                        'username': ticket_info['username'],
                        'email': ticket_info['email'],
                        'category': category,
                        'priority': priority,
                        'subject': subject,
                        'description': description
                    }

                    print(f"🔍 DEBUG: ticket_data préparé: {ticket_data}")

                    # Essayer d'envoyer la notification
                    try:
                        print("🔍 DEBUG: Import support_notifier")
                        from support_notifier import support_notifier

                        print(
                            f"🔍 DEBUG: support_notifier.bot = {support_notifier.bot}")

                        # Vérifier si le bot est disponible
                        if not support_notifier.bot:
                            print(
                                "⚠️ Bot Discord non disponible pour les notifications")
                            return

                        # Vérifier si le bot est prêt
                        if not support_notifier.bot.is_ready():
                            print("⚠️ Bot Discord pas encore prêt")
                            return

                        print(
                            "🔍 DEBUG: Bot disponible et prêt, programmation de la notification...")

                        # Programmer la notification dans la boucle du bot de manière simple
                        import asyncio

                        async def send_notification():
                            print("🔍 DEBUG: Début de send_notification")
                            try:
                                result = await support_notifier.send_new_ticket_notification(ticket_data)
                                print(
                                    f"🔍 DEBUG: Résultat notification: {result}")
                                return result
                            except Exception as e:
                                print(f"❌ Erreur dans send_notification: {e}")
                                import traceback
                                traceback.print_exc()
                                return False

                        # Utiliser call_soon_threadsafe pour programmer la tâche
                        support_notifier.bot.loop.call_soon_threadsafe(
                            lambda: asyncio.create_task(send_notification())
                        )

                        print(
                            f"📱 Notification programmée pour le ticket #{ticket_id}")

                    except ImportError:
                        print("⚠️ Module de notification Discord non disponible")
                    except Exception as e:
                        print(
                            f"⚠️ Erreur lors de l'envoi de la notification: {e}")
            except Exception as e:
                print(
                    f"⚠️ Erreur lors de la préparation de la notification: {e}")

        # Lancer la notification dans un thread séparé pour ne pas bloquer
        try:
            notification_thread = threading.Thread(
                target=notification_worker, daemon=False)  # Changé de True à False
            notification_thread.start()
            print(
                f"📱 Thread de notification démarré pour le ticket #{ticket_id}")
        except Exception as e:
            print(
                f"⚠️ Erreur lors du démarrage du thread de notification: {e}")

    def get_user_tickets(self, user_id):
        """Récupère tous les tickets d'un utilisateur"""
        try:
            cursor = self.conn.execute('''
            SELECT * FROM support_tickets 
            WHERE user_id = ? 
            ORDER BY created_at DESC
            ''', (user_id,))

            tickets = []
            for row in cursor.fetchall():
                ticket = dict(row)
                # Parser les métadonnées JSON
                if ticket['metadata']:
                    try:
                        ticket['metadata'] = json.loads(ticket['metadata'])
                    except json.JSONDecodeError:
                        ticket['metadata'] = {}
                else:
                    ticket['metadata'] = {}

                # Convertir les timestamps
                if ticket['created_at']:
                    ticket['created_at'] = datetime.fromisoformat(
                        ticket['created_at'])
                if ticket['updated_at']:
                    ticket['updated_at'] = datetime.fromisoformat(
                        ticket['updated_at'])

                tickets.append(ticket)

            return tickets
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des tickets: {e}")
            return []

    def get_all_tickets_for_admin(self):
        """Récupère tous les tickets avec les informations utilisateur pour l'admin"""
        try:
            cursor = self.conn.execute('''
            SELECT st.*, su.username, su.email, su.discord_username, su.discord_id
            FROM support_tickets st
            JOIN support_users su ON st.user_id = su.id
            ORDER BY st.ticket_number DESC
            ''')

            tickets = []
            for row in cursor.fetchall():
                ticket = dict(row)
                # Parser les métadonnées JSON
                if ticket['metadata']:
                    try:
                        ticket['metadata'] = json.loads(ticket['metadata'])
                    except json.JSONDecodeError:
                        ticket['metadata'] = {}
                else:
                    ticket['metadata'] = {}

                # Convertir les timestamps
                if ticket['created_at']:
                    ticket['created_at'] = datetime.fromisoformat(
                        ticket['created_at'])
                if ticket['updated_at']:
                    ticket['updated_at'] = datetime.fromisoformat(
                        ticket['updated_at'])

                tickets.append(ticket)

            return tickets

        except Exception as e:
            print(f"❌ Erreur lors de la récupération de tous les tickets: {e}")
            return []

    def get_ticket_by_number(self, ticket_number):
        """Récupère un ticket par son numéro séquentiel"""
        try:
            cursor = self.conn.execute('''
            SELECT st.*, su.username, su.email, su.discord_username, su.discord_id
            FROM support_tickets st
            JOIN support_users su ON st.user_id = su.id
            WHERE st.ticket_number = ?
            ''', (ticket_number,))

            row = cursor.fetchone()
            if row:
                ticket = dict(row)
                # Parser les métadonnées JSON
                if ticket['metadata']:
                    try:
                        ticket['metadata'] = json.loads(ticket['metadata'])
                    except json.JSONDecodeError:
                        ticket['metadata'] = {}
                else:
                    ticket['metadata'] = {}

                # Convertir les timestamps
                if ticket['created_at']:
                    ticket['created_at'] = datetime.fromisoformat(
                        ticket['created_at'])
                if ticket['updated_at']:
                    ticket['updated_at'] = datetime.fromisoformat(
                        ticket['updated_at'])

                return ticket

            return None

        except Exception as e:
            print(
                f"❌ Erreur lors de la récupération du ticket #{ticket_number}: {e}")
            return None

    def update_ticket_status(self, ticket_id, status):
        """Met à jour le statut d'un ticket"""
        try:
            self.conn.execute('''
            UPDATE support_tickets 
            SET status = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            ''', (status, ticket_id))

            self.conn.commit()
            print(f"✅ Statut du ticket #{ticket_id} mis à jour: {status}")
        except Exception as e:
            print(f"❌ Erreur lors de la mise à jour du statut: {e}")

    def add_ticket_response(self, ticket_id, message, is_admin=False):
        """Ajouter une réponse à un ticket"""
        try:
            cursor = self.conn.execute('''
            INSERT INTO ticket_responses (ticket_id, message, is_admin, created_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ''', (ticket_id, message, 1 if is_admin else 0))

            self.conn.commit()

            # Mettre à jour le timestamp du ticket
            self.conn.execute('''
            UPDATE support_tickets SET updated_at = CURRENT_TIMESTAMP WHERE id = ?
            ''', (ticket_id,))
            self.conn.commit()

            response_id = cursor.lastrowid
            print(f"✅ Réponse ajoutée avec l'ID: {response_id}")
            return response_id
        except Exception as e:
            print(f"❌ Erreur lors de l'ajout de la réponse: {e}")
            return None

    def get_ticket_responses(self, ticket_id):
        """Récupérer toutes les réponses d'un ticket"""
        try:
            cursor = self.conn.execute('''
            SELECT * FROM ticket_responses 
            WHERE ticket_id = ? 
            ORDER BY created_at ASC
            ''', (ticket_id,))

            responses = []
            for row in cursor.fetchall():
                response = dict(row)
                if response['created_at']:
                    response['created_at'] = datetime.fromisoformat(
                        response['created_at'])
                responses.append(response)
            return responses
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des réponses: {e}")
            return []

    def get_total_tickets(self):
        """Récupérer le nombre total de tickets"""
        try:
            cursor = self.conn.execute(
                "SELECT COUNT(*) as count FROM support_tickets")
            result = cursor.fetchone()
            return result['count']
        except Exception as e:
            print(
                f"❌ Erreur lors de la récupération du nombre total de tickets: {e}")
            return 0

    def get_resolved_tickets_count(self):
        """Récupérer le nombre de tickets résolus"""
        try:
            cursor = self.conn.execute(
                "SELECT COUNT(*) as count FROM support_tickets WHERE status = 'resolved'"
            )
            result = cursor.fetchone()
            return result['count']
        except Exception as e:
            print(
                f"❌ Erreur lors de la récupération du nombre de tickets résolus: {e}")
            return 0

    def get_active_users_count(self):
        """Récupérer le nombre d'utilisateurs actifs (ayant créé au moins un ticket)"""
        try:
            cursor = self.conn.execute(
                "SELECT COUNT(DISTINCT user_id) as count FROM support_tickets"
            )
            result = cursor.fetchone()
            return result['count']
        except Exception as e:
            print(
                f"❌ Erreur lors de la récupération du nombre d'utilisateurs actifs: {e}")
            return 0

    def get_user_by_username(self, username):
        """Récupérer un utilisateur par nom d'utilisateur"""
        try:
            cursor = self.conn.execute(
                "SELECT * FROM support_users WHERE username = ?",
                (username,)
            )
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None
        except Exception as e:
            print(
                f"❌ Erreur lors de la récupération de l'utilisateur par nom: {e}")
            return None

    def get_user_by_email(self, email):
        """Récupérer un utilisateur par email"""
        try:
            cursor = self.conn.execute(
                "SELECT * FROM support_users WHERE email = ?",
                (email,)
            )
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None
        except Exception as e:
            print(
                f"❌ Erreur lors de la récupération de l'utilisateur par email: {e}")
            return None

    def get_ticket_by_id(self, ticket_id):
        """Récupérer un ticket par son ID"""
        try:
            cursor = self.conn.execute('''
            SELECT st.*, su.username, su.email, su.discord_username, su.discord_id
            FROM support_tickets st
            JOIN support_users su ON st.user_id = su.id
            WHERE st.id = ?
            ''', (ticket_id,))

            row = cursor.fetchone()
            if row:
                ticket = dict(row)
                # Parser les métadonnées JSON
                if ticket['metadata']:
                    try:
                        ticket['metadata'] = json.loads(ticket['metadata'])
                    except json.JSONDecodeError:
                        ticket['metadata'] = {}
                else:
                    ticket['metadata'] = {}

                # Convertir les timestamps
                if ticket['created_at']:
                    ticket['created_at'] = datetime.fromisoformat(
                        ticket['created_at'])
                if ticket['updated_at']:
                    ticket['updated_at'] = datetime.fromisoformat(
                        ticket['updated_at'])

                return ticket
            return None
        except Exception as e:
            print(f"❌ Erreur lors de la récupération du ticket: {e}")
            return None

    def delete_ticket(self, ticket_id):
        """Supprime un ticket et toutes ses réponses"""
        try:
            cursor = self.conn.cursor()

            # Vérifier que le ticket existe
            cursor.execute(
                'SELECT id FROM support_tickets WHERE id = ?', (ticket_id,))
            if not cursor.fetchone():
                print(f"❌ Ticket {ticket_id} introuvable")
                return False

            # Supprimer d'abord toutes les réponses liées au ticket
            cursor.execute(
                'DELETE FROM ticket_responses WHERE ticket_id = ?', (ticket_id,))
            deleted_responses = cursor.rowcount

            # Supprimer le ticket
            cursor.execute(
                'DELETE FROM support_tickets WHERE id = ?', (ticket_id,))
            deleted_ticket = cursor.rowcount

            self.conn.commit()

            if deleted_ticket > 0:
                print(
                    f"✅ Ticket {ticket_id} supprimé avec {deleted_responses} réponse(s)")
                return True
            else:
                print(f"❌ Échec de la suppression du ticket {ticket_id}")
                return False

        except Exception as e:
            print(
                f"❌ Erreur lors de la suppression du ticket {ticket_id}: {e}")
            self.conn.rollback()
            return False

    def delete_old_tickets(self, status='closed', days_old=30):
        """Supprime les anciens tickets selon des critères"""
        try:
            cursor = self.conn.cursor()

            # Supprimer les tickets fermés de plus de X jours
            cursor.execute('''
                DELETE FROM ticket_responses 
                WHERE ticket_id IN (
                    SELECT id FROM support_tickets 
                    WHERE status = ? 
                    AND updated_at < datetime('now', '-{} days')
                )
            '''.format(days_old), (status,))

            cursor.execute('''
                DELETE FROM support_tickets 
                WHERE status = ? 
                AND updated_at < datetime('now', '-{} days')
            '''.format(days_old), (status,))

            deleted_count = cursor.rowcount
            self.conn.commit()

            print(f"✅ {deleted_count} ticket(s) ancien(s) supprimé(s)")
            return deleted_count

        except Exception as e:
            print(f"❌ Erreur lors de la suppression des anciens tickets: {e}")
            self.conn.rollback()
            return 0

    def get_tickets_for_deletion(self, status='closed', days_old=30):
        """Récupère la liste des tickets qui peuvent être supprimés"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT t.id, t.subject, t.status, t.created_at, t.updated_at,
                       u.username, u.email,
                       COUNT(r.id) as response_count
                FROM support_tickets t
                LEFT JOIN support_users u ON t.user_id = u.id
                LEFT JOIN ticket_responses r ON t.id = r.ticket_id
                WHERE t.status = ? 
                AND t.updated_at < datetime('now', '-{} days')
                GROUP BY t.id
                ORDER BY t.updated_at ASC
            '''.format(days_old), (status,))

            tickets = []
            for row in cursor.fetchall():
                ticket = dict(row)
                # Convertir les timestamps
                if ticket['created_at']:
                    ticket['created_at'] = datetime.fromisoformat(
                        ticket['created_at'].replace('Z', '+00:00'))
                if ticket['updated_at']:
                    ticket['updated_at'] = datetime.fromisoformat(
                        ticket['updated_at'].replace('Z', '+00:00'))
                tickets.append(ticket)

            return tickets

        except Exception as e:
            print(
                f"❌ Erreur lors de la récupération des tickets à supprimer: {e}")
            return []

    def close(self):
        """Fermer la connexion à la base de données"""
        if self.conn:
            self.conn.close()
            print("🔌 Connexion à la base de données fermée")


# Instance globale de la base de données
support_db = SupportDB()
