"""
Gestionnaire de propriétaires basé sur SQLite
Remplace le système JSON pour plus de robustesse
"""
import sqlite3
import os
import threading
from typing import List, Union
from datetime import datetime


class BotOwnerDatabase:
    """Gestionnaire des propriétaires du bot avec SQLite"""

    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), 'config', 'bot_owners.db')

        self.db_path = db_path
        self.lock = threading.Lock()
        self.init_database()

    def init_database(self):
        """Initialize the database and create tables if they don't exist"""
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            try:
                cursor = conn.cursor()

                # Create owners table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS bot_owners (
                        user_id INTEGER PRIMARY KEY,
                        added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        added_by TEXT,
                        notes TEXT
                    )
                ''')

                # Create audit log table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS owner_audit (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        action TEXT NOT NULL,
                        user_id INTEGER NOT NULL,
                        performed_by TEXT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        details TEXT
                    )
                ''')

                conn.commit()

                # Migrate from JSON if it exists and DB is empty
                self._migrate_from_json()

            finally:
                conn.close()

    def _migrate_from_json(self):
        """Migrate existing owners from JSON file to database"""
        json_path = os.path.join(
            os.path.dirname(self.db_path), 'bot_owners.json')

        if not os.path.exists(json_path):
            return

        try:
            import json

            # Check if database is empty first
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM bot_owners')
            count = cursor.fetchone()[0]

            if count > 0:
                conn.close()
                return  # Database already has data

            # Load from JSON and migrate
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                owners = data.get('owners', [])

                for owner_id in owners:
                    cursor.execute('''
                        INSERT OR IGNORE INTO bot_owners (user_id, added_by, notes) 
                        VALUES (?, ?, ?)
                    ''', (int(owner_id), 'JSON_MIGRATION', 'Migrated from bot_owners.json'))

                    # Log the migration
                    cursor.execute('''
                        INSERT INTO owner_audit (action, user_id, performed_by, details) 
                        VALUES (?, ?, ?, ?)
                    ''', ('MIGRATE', int(owner_id), 'SYSTEM', 'Migrated from JSON file'))

                conn.commit()
                print(f"✅ Migrated {len(owners)} owners from JSON to database")

                # Backup the JSON file
                backup_path = json_path + '.backup'
                import shutil
                shutil.copy2(json_path, backup_path)
                print(f"✅ JSON file backed up to {backup_path}")

        except Exception as e:
            print(f"⚠️ Error during JSON migration: {e}")
        finally:
            conn.close()

    def get_owners(self) -> List[int]:
        """Get list of all bot owners"""
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            try:
                cursor = conn.cursor()
                cursor.execute(
                    'SELECT user_id FROM bot_owners ORDER BY added_at')
                return [row[0] for row in cursor.fetchall()]
            finally:
                conn.close()

    def is_owner(self, user_id: Union[int, str]) -> bool:
        """Check if a user is a bot owner"""
        try:
            user_id = int(user_id)
        except (ValueError, TypeError):
            return False

        with self.lock:
            conn = sqlite3.connect(self.db_path)
            try:
                cursor = conn.cursor()
                cursor.execute(
                    'SELECT 1 FROM bot_owners WHERE user_id = ?', (user_id,))
                return cursor.fetchone() is not None
            finally:
                conn.close()

    def add_owner(self, user_id: Union[int, str], added_by: str = None, notes: str = None) -> bool:
        """Add a new bot owner"""
        try:
            user_id = int(user_id)
        except (ValueError, TypeError):
            return False

        with self.lock:
            conn = sqlite3.connect(self.db_path)
            try:
                cursor = conn.cursor()

                # Check if already exists
                if self.is_owner(user_id):
                    return False

                # Add owner
                cursor.execute('''
                    INSERT INTO bot_owners (user_id, added_by, notes) 
                    VALUES (?, ?, ?)
                ''', (user_id, added_by or 'WEB_PANEL', notes))

                # Log the action
                cursor.execute('''
                    INSERT INTO owner_audit (action, user_id, performed_by, details) 
                    VALUES (?, ?, ?, ?)
                ''', ('ADD', user_id, added_by or 'WEB_PANEL', notes or 'Added via web panel'))

                conn.commit()
                print(f"✅ Owner {user_id} added to database")
                return True

            except sqlite3.Error as e:
                print(f"❌ Database error adding owner {user_id}: {e}")
                return False
            finally:
                conn.close()

    def remove_owner(self, user_id: Union[int, str], removed_by: str = None) -> bool:
        """Remove a bot owner"""
        try:
            user_id = int(user_id)
        except (ValueError, TypeError):
            return False

        with self.lock:
            conn = sqlite3.connect(self.db_path)
            try:
                cursor = conn.cursor()

                # Check if exists
                if not self.is_owner(user_id):
                    return False

                # Remove owner
                cursor.execute(
                    'DELETE FROM bot_owners WHERE user_id = ?', (user_id,))

                # Log the action
                cursor.execute('''
                    INSERT INTO owner_audit (action, user_id, performed_by, details) 
                    VALUES (?, ?, ?, ?)
                ''', ('REMOVE', user_id, removed_by or 'WEB_PANEL', 'Removed via web panel'))

                conn.commit()
                print(f"✅ Owner {user_id} removed from database")
                return True

            except sqlite3.Error as e:
                print(f"❌ Database error removing owner {user_id}: {e}")
                return False
            finally:
                conn.close()

    def get_owner_info(self, user_id: Union[int, str]) -> dict:
        """Get detailed information about an owner"""
        try:
            user_id = int(user_id)
        except (ValueError, TypeError):
            return None

        with self.lock:
            conn = sqlite3.connect(self.db_path)
            try:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT user_id, added_at, added_by, notes 
                    FROM bot_owners WHERE user_id = ?
                ''', (user_id,))

                row = cursor.fetchone()
                if row:
                    return {
                        'user_id': row[0],
                        'added_at': row[1],
                        'added_by': row[2],
                        'notes': row[3]
                    }
                return None
            finally:
                conn.close()

    def get_audit_log(self, limit: int = 100) -> List[dict]:
        """Get audit log of owner changes"""
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            try:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT action, user_id, performed_by, timestamp, details 
                    FROM owner_audit 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                ''', (limit,))

                return [{
                    'action': row[0],
                    'user_id': row[1],
                    'performed_by': row[2],
                    'timestamp': row[3],
                    'details': row[4]
                } for row in cursor.fetchall()]
            finally:
                conn.close()

    def get_stats(self) -> dict:
        """Get statistics about owners"""
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            try:
                cursor = conn.cursor()

                # Total owners
                cursor.execute('SELECT COUNT(*) FROM bot_owners')
                total_owners = cursor.fetchone()[0]

                # Recent additions (last 30 days)
                cursor.execute('''
                    SELECT COUNT(*) FROM bot_owners 
                    WHERE added_at > datetime('now', '-30 days')
                ''')
                recent_additions = cursor.fetchone()[0]

                # Total audit entries
                cursor.execute('SELECT COUNT(*) FROM owner_audit')
                total_audit_entries = cursor.fetchone()[0]

                return {
                    'total_owners': total_owners,
                    'recent_additions': recent_additions,
                    'total_audit_entries': total_audit_entries
                }
            finally:
                conn.close()


# Global instance
bot_owner_db = BotOwnerDatabase()

# Compatibility functions for existing code


def get_bot_owners() -> List[int]:
    """Compatibility function - get list of bot owners"""
    return bot_owner_db.get_owners()


def is_bot_owner(user_id: Union[int, str]) -> bool:
    """Compatibility function - check if user is bot owner"""
    return bot_owner_db.is_owner(user_id)


def add_bot_owner(user_id: Union[int, str], added_by: str = None) -> bool:
    """Compatibility function - add bot owner"""
    return bot_owner_db.add_owner(user_id, added_by)


def remove_bot_owner(user_id: Union[int, str], removed_by: str = None) -> bool:
    """Compatibility function - remove bot owner"""
    return bot_owner_db.remove_owner(user_id, removed_by)
