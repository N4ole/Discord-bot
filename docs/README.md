# 🤖 Documentation Générale - Bot Discord

## 📋 Vue d'ensemble

Ce bot Discord offre un système complet de gestion de serveur avec interface web d'administration, système de support, et gestion multi-serveurs.

## ✨ Fonctionnalités principales

### 💬 Commandes Discord

- **Commandes slash** : `/help`, `/ping`, `/stats`, `/fun`, etc.
- **Commandes préfixées** : `!help`, `!owner`, `!admin`, etc.
- **Gestion des rôles** : Attribution automatique et manuelle
- **Logs avancés** : Suivi des événements serveur
- **Système de préfixes** : Personnalisation par serveur

### 🌐 Interface Web

- **Dashboard administrateur** : Statistiques en temps réel
- **Gestion des serveurs** : Vue détaillée de chaque serveur
- **Système de logs** : Consultation et filtrage
- **Panel de support** : Tickets utilisateur

### 🛠️ Outils d'administration

- **Multi-serveurs** : Gestion centralisée
- **Rotation des statuts** : Personnalisation automatique
- **Système de notifications** : Alertes Discord
- **Base de données** : SQLite intégré
- **Cache intelligent** : Optimisation des performances

## 📚 Documentation

Cette documentation est organisée en 6 sections principales :

### 🏠 [README.md](../README.md) - Documentation Générale

- Vue d'ensemble du bot et de ses fonctionnalités
- Structure du projet et configuration de base
- Guide de démarrage rapide
- Informations de sécurité et maintenance

### 📦 [INSTALLATION.md](INSTALLATION.md) - Guide d'Installation

- Prérequis système et logiciels requis
- Installation étape par étape
- Configuration Discord et variables d'environnement
- Dépannage et première utilisation

### 👑 [OWNER_MANAGEMENT.md](OWNER_MANAGEMENT.md) - Documentation Propriétaires

- Gestion de la liste des propriétaires
- Commandes Discord spéciales
- Administration globale et configuration avancée
- Procédures de sécurité et d'urgence

### 🛡️ [ADMIN.md](ADMIN.md) - Documentation Administrateurs

- Commandes de modération et gestion des membres
- Configuration des serveurs et système de logs
- Interface web d'administration
- Outils avancés et bonnes pratiques

### 🔧 [CORE_MODULES.md](CORE_MODULES.md) - Documentation des Modules Core

- Architecture et fonctionnement des modules principaux
- Système de gestion des propriétaires
- Gestionnaire de logs et d'événements
- Outils de diagnostic et de support

### ⚙️ [CONFIGURATION.md](CONFIGURATION.md) - Guide de Configuration

- Fichiers de configuration JSON
- Gestion des préfixes et des logs
- Variables d'environnement
- Personnalisation avancée

## 📁 Structure du projet

```text
Discord-bot/
├── main.py                  # Point d'entrée principal
├── engine.py                # Moteur principal du bot Discord
├── web_panel.py            # 🌐 Panel web d'administration Flask
├── start_bot.py            # Script de démarrage alternatif
├── get_my_id.py            # Utilitaire pour obtenir votre ID Discord
├── config/                 # 📁 Configuration JSON
│   ├── bot_owners.json     # Liste des propriétaires du bot
│   ├── prefixes.json       # Préfixes personnalisés par serveur
│   └── logs_config.json    # Configuration du système de logs
├── core/                   # 📁 Modules principaux
│   ├── bot_owner_manager.py   # Gestion des propriétaires
│   ├── prefix_manager.py      # Gestion des préfixes multi-serveur
│   ├── log_manager.py         # Système de logs avancé
│   ├── log_events.py          # Écouteurs d'événements Discord
│   ├── status_rotator.py      # Rotation automatique des statuts
│   ├── support_db.py          # Base de données du support
│   └── support_notifier.py    # Notifications Discord pour le support
├── slash/                  # 📁 Commandes slash (/)
│   ├── help.py             # Aide interactive avec menus
│   ├── admin.py            # Commandes de modération
│   ├── admin_roles.py      # Gestion des rôles
│   ├── tools.py            # Outils avancés (crypto, sondages, etc.)
│   ├── utils.py            # Utilitaires (info, ping, avatar, etc.)
│   ├── fun.py              # Divertissement (jeux, blagues, etc.)
│   └── prefix.py           # Gestion des préfixes
├── prefixe/                # 📁 Commandes préfixées (!)
│   ├── help.py             # Aide détaillée textuelle
│   ├── admin.py            # Modération avancée
│   ├── owner_management.py # Gestion des propriétaires (owners seulement)
│   ├── tools.py            # Outils et utilitaires étendus
│   ├── fun.py              # Divertissement et jeux
│   └── utils.py            # Informations et diagnostics
├── templates/              # 📁 Templates HTML pour le panel web
│   ├── dashboard.html      # Tableau de bord principal
│   ├── logs.html           # Interface de consultation des logs
│   ├── stats.html          # Statistiques détaillées
│   ├── control.html        # Contrôle et gestion du bot
│   ├── support_*.html      # 🎫 Interface du système de support
│   └── admin_*.html        # 🛠️ Administration des tickets
├── static/                 # 📁 Fichiers statiques (CSS, JS, images)
├── scripts/                # 📁 Scripts utilitaires
│   ├── get_my_id.py        # Obtenir votre ID Discord
│   └── multiserver_diagnostic.py  # Diagnostic multi-serveurs
├── docs/                   # 📁 Documentation complète
├── support.db              # 🗄️ Base de données SQLite du support
├── .env                    # Variables d'environnement (à créer)
├── .env.example            # Exemple de configuration
├── .env.panel              # Configuration du panel web
└── requirements.txt        # Dépendances Python
```

## 🚀 Démarrage rapide

### 1. Prérequis

- Python 3.8 ou plus récent
- Un bot Discord créé sur le [Discord Developer Portal](https://discord.com/developers/applications)

### 2. Installation

```bash
# Cloner le repository
git clone <votre-repo>
cd Discord-bot

# Installer les dépendances
pip install -r requirements.txt
```

### 3. Configuration

```bash
# Copier le fichier d'exemple
cp .env.example .env

# Éditer le fichier .env avec votre token Discord
# DISCORD_TOKEN=votre_token_ici
# OWNER_ID=votre_id_discord
```

### 4. Lancement

```bash
python main.py
```

## 🌐 Panel Web d'Administration

Le bot inclut un **panel web complet** pour l'administration et la surveillance.

### 🔗 Accès

- **URL** : <http://127.0.0.1:8080> (une fois le bot lancé)
- **Identifiants par défaut** : `admin` / `admin123`
- ⚠️ **Important** : Changez les identifiants dans `.env.panel` pour la production

### 🎛️ Fonctionnalités

- **Dashboard en temps réel** : Statistiques, uptime, erreurs
- **Gestion des logs** : Consultation, filtres, recherche
- **Contrôle du bot** : Gestion des serveurs, maintenance
- **Système de support** : Interface utilisateur pour tickets

## 🎫 Système de Support

Interface complète pour la gestion des tickets utilisateur.

### 🌟 Fonctionnalités

- **Inscription/Connexion** sécurisée des utilisateurs
- **Création de tickets** avec catégorisation et priorités
- **Système de réponses** entre utilisateurs et administrateurs
- **Gestion administrative** avec nettoyage automatique
- **Notifications Discord** vers les administrateurs

### 🚀 Accès

- **Utilisateurs** : <http://127.0.0.1:8080/support>
- **Administrateurs** : <http://127.0.0.1:8080/admin>

## 💡 Système d'aide intégré

### 3 façons d'obtenir de l'aide

1. **💬 Mentionnez le bot** : `@BotName` - Aide rapide interactive
2. **⚡ Commande slash** : `/help` - Menu d'aide avec catégories
3. **📝 Commande préfixée** : `!help [commande]` - Aide détaillée

## 🔧 Support et Assistance

- 📚 **Documentation complète** dans le dossier `docs/`
- 🌐 **Panel web** pour les logs et diagnostics
- 🎫 **Système de support** intégré
- 📞 **Discord.py Documentation** : <https://discordpy.readthedocs.io/>

## 🛡️ Sécurité

- ✅ **Authentification** obligatoire pour le panel web
- ✅ **Sessions sécurisées** avec timeout automatique
- ✅ **Mots de passe hashés** (jamais stockés en clair)
- ✅ **Validation des permissions** Discord
- ✅ **Logs d'audit** pour toutes les actions sensibles

---

*Développé avec ❤️ pour la communauté Discord - Utilise Discord.py 2.3.0+ et Flask*