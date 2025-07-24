# 🤖 Discord Bot - Summer of Making

Un bot Discord complet avec interface web d'administration et système de support intégré.

## 🚀 Démarrage rapide

```bash
# Installation des dépendances
pip install -r requirements.txt

# Configuration (voir docs/INSTALLATION.md)
cp .env.example .env
# Éditer .env avec votre token Discord

# Lancement
python main.py
```

## 📚 Documentation complète

- **[📖 Documentation générale](docs/README.md)** - Vue d'ensemble complète
- **[⚙️ Installation](docs/INSTALLATION.md)** - Guide d'installation détaillé  
- **[👑 Gestion des propriétaires](docs/OWNER_MANAGEMENT.md)** - Configuration des propriétaires
- **[🛡️ Administration](docs/ADMIN.md)** - Commandes et fonctionnalités admin

## 🏗️ Structure du projet

```
Discord-bot/
├── 📁 config/          # Configuration JSON
├── 📁 docs/            # Documentation complète
├── 📁 prefixe/         # Commandes avec préfixe
├── 📁 scripts/         # Scripts utilitaires
├── 📁 slash/           # Commandes slash
├── 📁 tests/           # Scripts de test
├── 📁 templates/       # Templates HTML
├── 🐍 main.py          # Point d'entrée
├── 🐍 engine.py        # Moteur du bot
└── 🐍 web_panel.py     # Interface web
```

## ✨ Fonctionnalités principales

- 🎮 **Commandes Discord** - Préfixe et slash
- 🌐 **Interface web** - Dashboard d'administration
- 🎫 **Système de support** - Tickets utilisateurs
- 📊 **Statistiques** - Monitoring en temps réel
- 🔧 **Multi-serveurs** - Gestion centralisée

## 🔗 Liens rapides

- **Interface web** : http://127.0.0.1:8080 (après démarrage)
- **Documentation** : [docs/README.md](docs/README.md)
- **Architecture** : [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md)

---
**Développé avec ❤️ pour la communauté Discord**