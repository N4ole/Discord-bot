"""
Utilitaire de gestion des propriétaires du bot
Module centralisé pour vérifier les permissions des propriétaires
"""
import json
import os
from typing import List, Union


class BotOwnerManager:
    """Gestionnaire centralisé des propriétaires du bot"""

    def __init__(self):
        self.config_file = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 'config', 'bot_owners.json')
        self._owners_cache = None
        self._last_modified = None

    def _load_owners(self) -> List[int]:
        """Charge la liste des propriétaires depuis le fichier JSON"""
        try:
            # Vérifier si le fichier a été modifié
            current_modified = os.path.getmtime(
                self.config_file) if os.path.exists(self.config_file) else 0

            if self._owners_cache is None or current_modified != self._last_modified:
                if os.path.exists(self.config_file):
                    with open(self.config_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        self._owners_cache = [
                            int(owner_id) for owner_id in data.get('owners', [])]
                        self._last_modified = current_modified
                else:
                    # Si le fichier n'existe pas, utiliser l'owner par défaut depuis les variables d'environnement
                    default_owner = os.getenv('OWNER_ID')
                    if default_owner:
                        self._owners_cache = [int(default_owner)]
                        # Créer le fichier avec l'owner par défaut
                        self._create_default_config(int(default_owner))
                    else:
                        self._owners_cache = []

            return self._owners_cache
        except (json.JSONDecodeError, ValueError, FileNotFoundError) as e:
            print(f"⚠️ Erreur lors du chargement des propriétaires: {e}")
            # Fallback sur OWNER_ID si le JSON est corrompu
            default_owner = os.getenv('OWNER_ID')
            if default_owner:
                return [int(default_owner)]
            return []

    def _create_default_config(self, owner_id: int):
        """Crée le fichier de configuration par défaut"""
        try:
            config = {
                "owners": [owner_id],
                "description": "Liste des propriétaires autorisés du bot Discord",
                "note": "Ajoutez les IDs Discord des propriétaires dans le tableau 'owners'"
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            print(
                f"✅ Fichier de configuration des propriétaires créé: {self.config_file}")
        except Exception as e:
            print(
                f"❌ Erreur lors de la création du fichier de configuration: {e}")

    def is_owner(self, user_id: Union[int, str]) -> bool:
        """Vérifie si un utilisateur est propriétaire du bot"""
        try:
            user_id = int(user_id)
            owners = self._load_owners()
            return user_id in owners
        except (ValueError, TypeError):
            return False

    def get_owners(self) -> List[int]:
        """Retourne la liste des propriétaires"""
        return self._load_owners()

    def add_owner(self, user_id: Union[int, str]) -> bool:
        """Ajoute un propriétaire à la liste"""
        try:
            user_id = int(user_id)
            owners = self._load_owners()

            if user_id not in owners:
                owners.append(user_id)
                return self._save_owners(owners)
            return True  # Déjà dans la liste
        except (ValueError, TypeError):
            return False

    def remove_owner(self, user_id: Union[int, str]) -> bool:
        """Supprime un propriétaire de la liste"""
        try:
            user_id = int(user_id)
            owners = self._load_owners()

            if user_id in owners:
                owners.remove(user_id)
                return self._save_owners(owners)
            return True  # Pas dans la liste
        except (ValueError, TypeError):
            return False

    def _save_owners(self, owners: List[int]) -> bool:
        """Sauvegarde la liste des propriétaires"""
        try:
            config = {
                "owners": owners,
                "description": "Liste des propriétaires autorisés du bot Discord",
                "note": "Ajoutez les IDs Discord des propriétaires dans le tableau 'owners'"
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)

            # Invalider le cache
            self._owners_cache = None
            self._last_modified = None

            return True
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde des propriétaires: {e}")
            return False

    def reload(self):
        """Force le rechargement de la configuration"""
        self._owners_cache = None
        self._last_modified = None


# Instance globale
bot_owner_manager = BotOwnerManager()


def is_bot_owner(user_id: Union[int, str]) -> bool:
    """Fonction utilitaire pour vérifier si un utilisateur est propriétaire"""
    return bot_owner_manager.is_owner(user_id)


def get_bot_owners() -> List[int]:
    """Fonction utilitaire pour obtenir la liste des propriétaires"""
    return bot_owner_manager.get_owners()


def add_bot_owner(user_id: Union[int, str]) -> bool:
    """Fonction utilitaire pour ajouter un propriétaire"""
    return bot_owner_manager.add_owner(user_id)


def remove_bot_owner(user_id: Union[int, str]) -> bool:
    """Fonction utilitaire pour supprimer un propriétaire"""
    return bot_owner_manager.remove_owner(user_id)
