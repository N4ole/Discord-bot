# 🤖 Discord Bot - Summer of Making

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Discord.py](https://img.shields.io/badge/Discord.py-2.3+-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discordpy.readthedocs.io)
[![Flask](https://img.shields.io/badge/Flask-2.3+-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![HTML5](https://img.shields.io/badge/HTML5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/docs/Web/CSS)
[![JavaScript](https://img.shields.io/badge/JavaScript-%23F7DF1E.svg?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/docs/Web/JavaScript)

[![VS Code](https://img.shields.io/badge/VS_Code-007ACC?style=for-the-badge&logo=visual-studio-code&logoColor=white)](https://code.visualstudio.com/)
[![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)](https://git-scm.com/)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org/)

![My hackatime](https://hackatime-badge.hackclub.com/U096RRX1LRZ/Discord-bot)



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
![My time](https://github-readme-stats.hackclub.dev/api/wakatime?username=15793&api_domain=hackatime.hackclub.com&&custom_title=Hackatime+Stats&layout=compact&cache_seconds=0&langs_count=8&theme=transparent)
