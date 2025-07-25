# 🔧 Core Modules - Bot Discord

Ce dossier contient les modules principaux (core) du bot Discord qui gèrent les fonctionnalités essentielles.

## 📦 Modules disponibles

### 🎯 **bot_owner_manager.py**

- **Description** : Gestion centralisée des propriétaires du bot
- **Fonctions principales** :
  - `get_bot_owners()` - Récupère la liste des propriétaires
  - `add_bot_owner(user_id)` - Ajoute un propriétaire
  - `remove_bot_owner(user_id)` - Retire un propriétaire  
  - `is_bot_owner(user_id)` - Vérifie si un utilisateur est propriétaire
- **Fichier de config** : `config/bot_owners.json`

### 🏷️ **prefix_manager.py**
- Gestion des préfixes personnalisés par serveur
- Classe principale : `PrefixManager`

### 📝 **log_manager.py**
- Système de logs avancé pour le bot
- Classe principale : `LogManager`

### 🔄 **status_rotator.py**
- Rotation automatique des statuts du bot
- Classe principale : `StatusRotator`

### 🎫 **support_db.py**
- Base de données pour le système de support
- Classe principale : `SupportDB`

### 🔔 **support_notifier.py**
- Notifications Discord pour le système de support
- Module : `support_notifier`

### 💬 **bot_mentions.py**
- Gestion des mentions du bot
- Classe principale : `BotMentions`

### 📊 **log_events.py**
- Événements et logs du bot
- Classe principale : `LogEvents`

## Utilisation

Les modules core peuvent être importés de deux façons :

```python
# Import direct
from core.bot_owner_manager import get_bot_owners

# Import via __init__.py
from core import get_bot_owners
```

## Architecture

Ces modules constituent le cœur du bot et sont utilisés par :
- Le moteur principal (`engine.py`)
- L'interface web (`web_panel.py`)
- Les commandes préfixe (`prefixe/`)
- Les commandes slash (`slash/`)
- Les scripts utilitaires (`scripts/`)
