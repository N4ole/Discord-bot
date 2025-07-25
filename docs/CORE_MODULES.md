# Core Modules - Bot Discord

Ce dossier contient les modules principaux (core) du bot Discord.

## Modules disponibles

### 🎯 **bot_owner_manager.py**
- Gestion centralisée des propriétaires du bot
- Fonctions : `get_bot_owners()`, `add_bot_owner()`, `remove_bot_owner()`, `is_bot_owner()`

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
