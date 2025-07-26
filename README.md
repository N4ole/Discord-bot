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
# 1. Installation des dépendances
pip install -r requirements.txt

# 2. Configuration initiale (OBLIGATOIRE)
cp .env.example .env
# Éditer .env avec votre token Discord et votre ID utilisateur

# 3. Lancement
python main.py
```

## ⚙️ Configuration initiale requise

Avant de lancer le bot, vous devez créer **3 fichiers essentiels** :

### 1. 📄 Fichier `.env` (Configuration Discord)

```bash
# Copiez le fichier exemple
cp .env.example .env

# Éditez .env et remplacez :
DISCORD_TOKEN=YOUR_DISCORD_BOT_TOKEN    # Token de votre bot Discord
OWNER_ID=YOUR_DISCORD_USER_ID           # Votre ID utilisateur Discord
```

**🔗 Comment obtenir ces informations :**

- **Token Discord** :
  1. Allez sur <https://discord.com/developers/applications>
  2. Créez une nouvelle application ou sélectionnez la vôtre
  3. Section "Bot" → "Token" → "Copy"
  
- **Votre ID Discord** :
  1. Discord → Paramètres → Avancé → Mode développeur (ON)
  2. Clic droit sur votre profil → "Copier l'ID"
  3. **Ou utilisez la commande `!myid` dans Discord** (plus facile !)

### 2. 🌐 Fichier `.env.panel` (Configuration Panel Web)

Créez ce fichier à la racine avec le contenu suivant :

```bash
# Copiez le fichier exemple
cp .env.panel.example .env.panel

# Ou créez-le manuellement avec ce contenu :
```

```bash
# Configuration du Panel Web d'Administration

# Identifiants administrateurs (changez-les !)
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123

# 🌐 Configuration du serveur web
WEB_HOST=0.0.0.0
WEB_PORT=8080

# 🔐 Sécurité (optionnel)
SECRET_KEY=your-secret-key-here

# Configuration avancée
LOG_RETENTION_DAYS=7
MAX_LOGS_IN_MEMORY=1000
AUTO_REFRESH_INTERVAL=10

# Sécurité
ENABLE_IP_WHITELIST=false
ALLOWED_IPS=127.0.0.1,::1

# Fonctionnalités
ENABLE_COMMAND_TRACKING=true
ENABLE_ERROR_TRACKING=true
ENABLE_PERFORMANCE_METRICS=true

```

### 3. 🗄️ Base de données `support.db`

La base de données sera **créée automatiquement** au premier lancement du bot.

- ✅ **Aucune action requise** - Le bot l'initialise tout seul
- 📍 **Emplacement** : `support.db` (à la racine)
- 🔒 **Sécurité** : Fichier local uniquement (non synchronisé sur GitHub)

### ⚠️ Notes importantes

- 🔐 **Sécurité** : Ne **JAMAIS** commiter les fichiers `.env`, `.env.panel` ou `support.db`
- 🔑 **Mots de passe** : Changez les identifiants par défaut du panel web
- 💾 **Sauvegarde** : Pensez à sauvegarder `support.db` pour ne pas perdre vos données
- 🌐 **Accès web** : Le panel sera accessible sur <http://127.0.0.1:8080> après démarrage

## 📚 Documentation complète

- **[📖 Documentation générale](docs/README.md)** - Vue d'ensemble complète
- **[⚙️ Installation](docs/INSTALLATION.md)** - Guide d'installation détaillé  
- **[👑 Gestion des propriétaires](docs/OWNER_MANAGEMENT.md)** - Configuration des propriétaires
- **[🛡️ Administration](docs/ADMIN.md)** - Commandes et fonctionnalités admin

## 🏗️ Structure du projet

```text
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

- **Interface web** : <http://127.0.0.1:8080> (après démarrage)
- **Documentation** : [docs/README.md](docs/README.md)
- **Architecture** : [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md)

---
![My time](https://github-readme-stats.hackclub.dev/api/wakatime?username=15793&api_domain=hackatime.hackclub.com&&custom_title=Hackatime+Stats&layout=compact&cache_seconds=0&langs_count=8&theme=transparent)
