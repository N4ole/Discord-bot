# Structure du Projet - Bot Discord

## Architecture du projet

```
Discord-bot/
├── 📁 config/              # Fichiers de configuration
│   ├── bot_owners.json     # Liste des propriétaires
│   ├── prefixes.json       # Préfixes par serveur
│   ├── logs_config.json    # Configuration des logs
│   └── ...
├── 📁 docs/                # Documentation
│   ├── README.md           # Documentation générale
│   ├── INSTALLATION.md     # Guide d'installation
│   ├── OWNER_MANAGEMENT.md # Gestion des propriétaires
│   └── ADMIN.md           # Documentation admin
├── 📁 prefixe/            # Commandes avec préfixe
│   ├── admin.py           # Commandes admin
│   ├── fun.py             # Commandes fun
│   └── ...
├── 📁 scripts/            # Scripts utilitaires
│   ├── admin_panel.py     # Panel d'administration
│   ├── get_my_id.py       # Obtenir son ID Discord
│   └── ...
├── 📁 slash/              # Commandes slash
│   ├── admin.py           # Commandes slash admin
│   ├── fun.py             # Commandes slash fun
│   └── ...
├── 📁 static/             # Fichiers statiques web
├── 📁 templates/          # Templates HTML
├── 📁 tests/              # Scripts de test
│   ├── test_support.py    # Tests du support
│   ├── test_owner_web.py  # Tests interface web
│   └── ...
├── 🐍 main.py             # Point d'entrée principal
├── 🐍 engine.py           # Moteur du bot
├── 🐍 web_panel.py        # Interface web d'administration
├── 🐍 support_db.py       # Base de données support
└── 📋 requirements.txt    # Dépendances Python
```

## Fichiers principaux

- **main.py** : Point d'entrée du bot
- **engine.py** : Core du bot Discord
- **web_panel.py** : Interface web d'administration
- **start_bot.py** : Script de démarrage

## Modules de gestion

- **bot_owner_manager.py** : Gestion des propriétaires
- **prefix_manager.py** : Gestion des préfixes
- **log_manager.py** : Gestion des logs
- **support_db.py** : Base de données support
- **status_rotator.py** : Rotation des statuts

## Commandes

Le bot supporte deux types de commandes :
- **Commandes préfixe** (dossier `prefixe/`)
- **Commandes slash** (dossier `slash/`)

## Tests et utilitaires

- **tests/** : Scripts de test pour valider le fonctionnement
- **scripts/** : Utilitaires d'administration et de diagnostic
