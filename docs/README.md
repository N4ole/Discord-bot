# 🤖 Documentation Générale - Bot Discord

## 📋 Vue d'ensemble

Ce bot Discord offre un système complet de gestion de serveur avec interface web d'administration, système de support, et gestion multi-serveurs.

## ✨ Fonctionnalités principales

### � Commandes Discord
- **Commandes slash** : `/help`, `/ping`, `/stats`, `/fun`, etc.
- **Commandes préfixées** : `!help`, `!owner`, `!admin`, etc.
- **Gestion des rôles** : Attribution automatique et manuelle
- **Logs avancés** : Suivi des événements serveur
- **Système de préfixes** : Personnalisation par serveur

### 🌐 Interface Web
- **Dashboard administrateur** : Statistiques en temps réel
- **Gestion des serveurs** : Vue détaillée de chaque serveur
- **Système de logs** : Consultation et filtrage
- **Gestion des propriétaires** : Interface graphique
- **Panel de support** : Tickets utilisateur

### 🛠️ Outils d'administration
- **Multi-serveurs** : Gestion centralisée
- **Rotation des statuts** : Personnalisation automatique
- **Système de notifications** : Alertes Discord
- **Base de données** : SQLite intégré
- **Cache intelligent** : Optimisation des performances

## � Documentation

Cette documentation est organisée en 4 sections principales :

### 🏠 [README.md](README.md) - Documentation Générale
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
- Commandes Discord et interface web
- Administration globale et configuration avancée
- Procédures de sécurité et d'urgence

### 🛡️ [ADMIN.md](ADMIN.md) - Documentation Administrateurs
- Commandes de modération et gestion des membres
- Configuration des serveurs et système de logs
- Interface web d'administration
- Outils avancés et bonnes pratiques

## 📁 Structure du projet

```
Discord-bot/
├── main.py                 # Point d'entrée principal
├── engine.py              # Moteur du bot Discord
├── web_panel.py           # Interface web Flask
├── bot_owner_manager.py   # Gestion des propriétaires
├── config/                # 📁 Configuration
│   ├── bot_owners.json    # Configuration des propriétaires
│   ├── prefixes.json      # Configuration des préfixes
│   └── logs_config.json   # Configuration des logs
├── prefixe/               # Commandes préfixées
│   ├── owner_management.py
│   ├── admin.py
│   └── ...
├── slash/                 # Commandes slash
│   ├── admin.py
│   ├── help.py
│   └── ...
├── templates/             # Templates HTML
├── static/               # Fichiers statiques
└── docs/                 # Documentation
```

```
Discord-bot/
├── main.py                     # Point d'entrée principal
├── engine.py                   # Moteur principal du bot
├── prefix_manager.py           # Gestion des préfixes multi-serveur
├── log_manager.py             # Système de logs
├── log_events.py              # Écouteurs d'événements
├── bot_mentions.py            # Gestion des mentions du bot
├── multiserver_diagnostic.py  # Diagnostics pour le propriétaire
├── web_panel.py               # 🌐 Panel web d'administration
├── support_db.py              # 🎫 Base de données du système de support
├── support_notifier.py        # 📧 Notifications Discord pour le support
├── admin_panel.py             # 🛠️ Utilitaires d'administration
├── templates/                 # 🎨 Templates HTML
│   ├── login.html            # Page de connexion admin
│   ├── dashboard.html        # Tableau de bord principal
│   ├── logs.html             # Interface de consultation des logs
│   ├── stats.html            # Statistiques détaillées
│   ├── control.html          # Contrôle du bot
│   ├── support_*.html        # 🎫 Interface du système de support
│   └── admin_*.html          # 🛠️ Interface d'administration des tickets
├── static/                   # 📁 Fichiers statiques (CSS, JS, images)
├── slash/                    # Commandes slash (/)
│   ├── bonjour.py           # Commande de salutation
│   ├── logs.py              # Configuration des logs
│   ├── admin.py             # Commandes de modération
│   ├── admin_roles.py       # Gestion des rôles
│   ├── help.py              # Système d'aide interactif
│   ├── utils.py             # 🔧 Commandes utilitaires
│   ├── fun.py               # 🎮 Commandes de divertissement
│   ├── tools.py             # 🔧 Outils avancés
│   └── prefix.py            # Gestion des préfixes
├── prefixe/                 # Commandes préfixées (!)
│   ├── bonjour.py           # Commande de salutation
│   ├── prefix.py            # Gestion des préfixes
│   ├── logs.py              # Configuration des logs
│   ├── admin.py             # Commandes de modération
│   ├── admin_roles.py       # Gestion des rôles
│   ├── help.py              # Système d'aide détaillé
│   ├── utils.py             # 🔧 Commandes utilitaires
│   ├── fun.py               # 🎮 Commandes de divertissement
│   └── tools.py             # 🔧 Outils avancés
├── .env                     # Variables d'environnement (à créer)
├── .env.example            # Exemple de configuration
├── .env.panel              # Configuration du panel web
├── support.db              # 🎫 Base de données SQLite du support
├── scripts/                # 📁 Scripts utilitaires
├── tests/                  # 📁 Scripts de test
├── docs/                   # 📁 Documentation
└── requirements.txt        # Dépendances Python
```

## 🚀 Installation et Configuration

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

### 3. Configuration du token Discord
```bash
# Copier le fichier d'exemple
cp .env.example .env

# Éditer le fichier .env et remplacer YOUR_DISCORD_BOT_TOKEN
# par votre vrai token Discord
```

### 4. Configuration du panel web (optionnel)
```bash
# Modifier .env.panel pour personnaliser les identifiants
# Par défaut : admin / admin123
```

### 5. Lancement du bot
```bash
python main.py
```

## 🌐 Panel Web d'Administration

Le bot inclut un **panel web complet** pour l'administration et la surveillance !

### � Accès au Panel
- **URL** : http://127.0.0.1:8080 (une fois le bot lancé)
- **Identifiants par défaut** : `admin` / `admin123`
- ⚠️ **Important** : Changez les identifiants dans `.env.panel` pour la production !

### 🎛️ Fonctionnalités du Panel

#### 📊 Dashboard Principal
- **Statistiques en temps réel** : serveurs, utilisateurs, commandes
- **Statut du bot** et temps de fonctionnement (uptime)
- **Compteurs d'erreurs** et d'activité
- **Actualisation automatique** toutes les 10 secondes

#### 📝 Gestion des Logs
- **Consultation complète** de l'historique
- **Filtres avancés** par niveau (INFO, SUCCESS, WARNING, ERROR)
- **Recherche textuelle** dans les messages
- **Pagination** pour une navigation fluide

#### 📈 Statistiques Détaillées
- **Graphiques d'utilisation** par heure sur 24h
- **Types d'erreurs** avec compteurs détaillés
- **Métriques de performance** (taux de succès, etc.)
- **Informations système** complètes

#### 🎛️ Contrôle du Bot
- **Liste complète des serveurs** avec détails
- **Quitter un serveur** avec confirmation sécurisée
- **Commandes de maintenance** :
  - 🔄 Synchroniser les commandes slash
  - 🗑️ Vider le cache
  - 📊 Mettre à jour les statistiques
  - 🔄 Recharger les modules

### 🔐 Sécurité du Panel
- ✅ **Authentification obligatoire** pour toutes les pages
- ✅ **Sessions sécurisées** avec timeout automatique
- ✅ **Mots de passe hashés** (jamais stockés en clair)
- ✅ **Logs d'audit** pour toutes les actions admin
- ✅ **Confirmations** pour les actions critiques

## 🎫 Système de Support

Le bot intègre un **système de support complet** avec interface web dédiée !

### 🌟 Fonctionnalités du Support

#### � Gestion des Utilisateurs
- **Inscription sécurisée** avec validation des données
- **Connexion** avec nom d'utilisateur ou email
- **Intégration Discord** (nom d'utilisateur et ID)
- **Sessions sécurisées** avec option "Se souvenir de moi"

#### 🎫 Gestion des Tickets
- **Création de tickets** avec catégorisation et priorités
- **Métadonnées avancées** (ID serveur, commande utilisée, erreurs)
- **Système de réponses** entre utilisateurs et administrateurs
- **Statuts multiples** : ouvert, en cours, en attente, résolu, fermé
- **Priorités configurables** : faible, moyenne, haute, urgente
- **Numérotation séquentielle** : Les tickets gardent une numérotation continue même après suppression

#### 🧹 Gestion Administrative
- **Suppression individuelle** de tickets avec confirmation
- **Nettoyage en masse** avec critères automatiques :
  - Tickets fermés depuis plus de 30 jours
  - Tickets résolus depuis plus de 90 jours
  - Tickets inactifs depuis plus de 6 mois
- **Interface d'administration** pour gérer tous les tickets
- **Notifications Discord** automatiques vers les admins

### 🚀 Accès au Support
- **URL utilisateur** : http://127.0.0.1:8080/support
- **URL admin** : http://127.0.0.1:8080/admin (nécessite connexion admin)

##  Système d'aide intégré

### 🚀 3 façons d'obtenir de l'aide

1. **💬 Mentionnez le bot** : `@BotName` - Aide rapide interactive
2. **⚡ Commande slash** : `/help` - Menu d'aide avec catégories
3. **📝 Commande préfixée** : `!help [commande]` - Aide détaillée

### ✨ Fonctionnalités d'aide
- **🎯 Aide contextuelle** - Adaptée au serveur et aux permissions
- **📂 Catégories organisées** - Modération, rôles, logs, configuration
- **🔍 Aide spécifique** - `!help ban` pour des détails sur une commande
- **🎨 Interface élégante** - Embeds colorés et interactifs

## 📋 Commandes disponibles

### 💡 Aide et Information
- `/help` - **Menu d'aide interactif** avec catégories
- `!help [commande]` - **Aide détaillée** pour une commande spécifique
- **@BotName** - **Aide rapide** en mentionnant le bot

### 🎉 Commandes de Base
- `/bonjour` ou `!bonjour` - Dit bonjour avec une belle carte embed

### 🔧 Commandes Utilitaires

#### 📊 Informations (slash ET préfixé)
- `/ping` ou `!ping` - Latence du bot et statistiques de connexion
- `/info [utilisateur]` ou `!info [utilisateur]` - Informations détaillées d'un utilisateur
- `/server` ou `!server` - Informations complètes du serveur
- `/avatar [utilisateur]` ou `!avatar [utilisateur]` - Avatar en haute résolution
- `/uptime` ou `!uptime` - Temps de fonctionnement du bot
- `/botinfo` ou `!botinfo` - Informations complètes du bot

#### 🌐 Utilitaires Web (slash ET préfixé)
- `/weather <ville>` ou `!weather <ville>` - Météo actuelle d'une ville
- `/translate <texte>` ou `!translate <texte>` - Traduction automatique

#### 🔗 Utilitaires Préfixés Exclusifs
- `!invite` - Génère un lien d'invitation pour le bot
- `!roll [XdY]` - Lance des dés (ex: `!roll 2d20`)

### 🎮 Commandes de Divertissement

#### 🎯 Jeux et Hasard (slash ET préfixé)
- `/coinflip` ou `!coinflip` - Lance une pièce de monnaie
- `/rps <choix>` ou `!rps <choix>` - Pierre-papier-ciseaux contre le bot
- `/8ball <question>` ou `!8ball <question>` - Boule magique
- `/choose <options>` ou `!choose <options>` - Choisit aléatoirement

#### 😄 Divertissement et Social (slash ET préfixé)
- `/joke` ou `!joke` - Raconte une blague aléatoire
- `/quote` ou `!quote` - Affiche une citation inspirante
- `/compliment [utilisateur]` ou `!compliment [utilisateur]` - Donne un compliment

#### 🎨 Divertissement Préfixé Exclusif
- `!hug <utilisateur>` - Faire un câlin virtuel
- `!ascii <texte>` - Génère de l'art ASCII simple

### 🔧 Commandes d'Outils Avancés

#### 📊 Analyse et Monitoring (slash ET préfixé)
- `/analyze [utilisateur]` ou `!analyze [utilisateur]` - Analyse détaillée avec scoring sécurité
- `/clean <nombre> [filtres]` ou `!clean <nombre> [filtres]` - Nettoyage avancé des messages
- `/remind <temps> <message>` ou `!remind <temps> <message>` - Système de rappels programmés

#### 🔐 Sécurité et Cryptographie (slash ET préfixé)
- `/encode <texte>` ou `!encode <texte>` - Encode du texte en base64
- `/decode <texte>` ou `!decode <texte>` - Décode du texte base64
- `/hash <algorithme> <texte>` ou `!hash <algorithme> <texte>` - Génère des hashes sécurisés
- `/password [longueur] [options]` ou `!password [longueur] [options]` - Génère des mots de passe

#### 🗳️ Interaction Communautaire (slash ET préfixé)
- `/poll <question> <options> [durée]` ou `!poll [durée] "question" options` - Sondages avancés

#### 📝 Utilitaires Texte Préfixés Exclusifs
- `!count <texte>` - Compte caractères, mots et lignes

### ⚙️ Configuration

#### 🏷️ Gestion des Préfixes (préfixé uniquement)
- `!prefix` - Gère le préfixe du bot pour ce serveur
  - `!prefix set <nouveau_préfixe>` - Change le préfixe
  - `!prefix reset` - Remet le préfixe par défaut
  - `!prefix info` - Affiche les informations

#### 📊 Système de Logs (slash ET préfixé)
- `/setlog <canal>` ou `!setlog <canal>` - Définit le canal de logs
- `/logon` ou `!logon` - Active les logs
- `/logoff` ou `!logoff` - Désactive les logs
- `/logstatus` ou `!logstatus` - Affiche le statut des logs

#### 🛡️ Commandes de Modération (slash ET préfixé)
- `/ban <membre> [raison]` ou `!ban <membre> [raison]` - Bannit un membre
- `/unban <user_id> [raison]` ou `!unban <user_id> [raison]` - Débannit un utilisateur
- `/kick <membre> [raison]` ou `!kick <membre> [raison]` - Expulse un membre
- `/mute <membre> [durée] [raison]` ou `!mute <membre> [durée] [raison]` - Met en timeout
- `/unmute <membre> [raison]` ou `!unmute <membre> [raison]` - Retire le timeout

#### 🎭 Gestion des Rôles (slash ET préfixé)
- `/addrole <membre> <rôle>` ou `!addrole <membre> <rôle>` - Ajoute un rôle
- `/removerole <membre> <rôle>` ou `!removerole <membre> <rôle>` - Retire un rôle
- `/roles [membre]` ou `!roles [membre]` - Affiche les rôles
- `/userinfo [membre]` ou `!userinfo [membre]` - Informations d'un membre
- `/serverinfo` ou `!serverinfo` - Informations du serveur

## � Fonctionnalités Avancées

### 🎯 Gestion des Préfixes
- **Préfixe par défaut** : `!`
- **Mention** : Tu peux toujours utiliser `@BotName` comme préfixe
- **Personnalisation** : Chaque serveur peut avoir son préfixe unique
- **Persistance** : Les préfixes sont sauvegardés automatiquement

### 📊 Système de Logs
Le bot dispose d'un **système de logs complet** qui surveille automatiquement :

#### 🎯 Configuration rapide
1. **Définir le canal** : `/setlog #logs` ou `!setlog #logs`
2. **Activer** : `/logon` ou `!logon`
3. **Vérifier** : `/logstatus` ou `!logstatus`

#### � Événements surveillés
- **💬 Messages** : Suppression, modification
- **👥 Membres** : Arrivée, départ, changements de rôles
- **🔊 Vocal** : Connexion, déconnexion, changement de canal
- **🔨 Modération** : Bannissements, débannissements
- **📝 Canaux** : Création, suppression
- **🎭 Rôles** : Attribution, retrait

### 🌐 Support Multi-Serveurs
Le bot peut être utilisé simultanément sur **plusieurs serveurs Discord** :
- **🏠 Configuration unique** : Chaque serveur a ses propres paramètres
- **� Isolation complète** : Les configurations ne s'interfèrent pas
- **⚡ Performance optimisée** : Un seul bot pour plusieurs serveurs
- **🔧 Gestion centralisée** : Commandes de diagnostic pour les propriétaires

## � Déploiement et Production

### 🔧 Configuration de Production
1. **Changez les identifiants par défaut** dans `.env.panel`
2. **Utilisez un serveur WSGI** comme Gunicorn pour le panel web
3. **Configurez un reverse proxy** (Nginx) pour HTTPS
4. **Activez les logs en fichier** pour la persistance
5. **Sauvegardez régulièrement** la base de données SQLite

### 🛡️ Sécurité
- ✅ Tokens et mots de passe dans des variables d'environnement
- ✅ Authentification obligatoire pour le panel web
- ✅ Sessions sécurisées avec timeout automatique
- ✅ Validation des permissions Discord
- ✅ Logs d'audit pour toutes les actions sensibles
- ✅ Hachage sécurisé des mots de passe utilisateurs

### 📊 Monitoring
- ✅ Statistiques en temps réel via le panel web
- ✅ Logs détaillés de tous les événements
- ✅ Métriques de performance et d'utilisation
- ✅ Alertes automatiques en cas d'erreur
- ✅ Système de support intégré pour les utilisateurs

## 🆘 Dépannage et FAQ

### ❓ Problèmes Courants

**Q: Le bot ne répond pas aux commandes**
- Vérifiez que le token Discord est correct dans `.env`
- Assurez-vous que le bot a les permissions nécessaires
- Vérifiez que les intents sont activés (Members, Presences)

**Q: Les commandes slash n'apparaissent pas**
- Utilisez `/sync` ou le bouton dans le panel web
- Attendez quelques minutes (propagation Discord)
- Vérifiez les permissions "Use Application Commands"

**Q: Le panel web ne fonctionne pas**
- Vérifiez que le port 8080 n'est pas utilisé
- Assurez-vous que Flask et Werkzeug sont installés
- Vérifiez la configuration dans `.env.panel`

**Q: Le système de support ne fonctionne pas**
- Vérifiez que la base de données `support.db` est accessible
- Assurez-vous que les templates HTML sont présents
- Vérifiez les logs du panel web pour les erreurs

### 🔧 Commandes de Diagnostic

#### Pour les Propriétaires du Bot
- `!diag` - Diagnostic complet du bot
- `!servers` - Liste des serveurs connectés
- `!stats` - Statistiques globales

#### Panel Web
- **Contrôle > Synchroniser** - Resynchronise les commandes slash
- **Contrôle > Vider le cache** - Remet à zéro les statistiques
- **Logs** - Consultation détaillée de l'historique

## �️ Développement

### 📝 Ajout de nouvelles commandes
1. **Commande slash** : Créez un fichier dans `slash/`
2. **Commande préfixée** : Créez un fichier dans `prefixe/`
3. Ajoutez le chargement dans `engine.py` si nécessaire

Chaque module doit avoir une fonction `setup(bot)` pour être chargé automatiquement.

### 🗃️ Structure de la Base de Données

#### Tables Principales
- `support_users` - Comptes utilisateurs du système de support
- `support_tickets` - Tickets de support avec métadonnées
- `support_responses` - Réponses aux tickets
- `support_counters` - Compteurs pour la numérotation séquentielle

#### Migration Automatique
Le système détecte automatiquement les nouvelles colonnes et effectue les migrations nécessaires.

## 🎯 Roadmap et Améliorations Futures

### ✅ Récemment Ajouté
- [x] 🔧 **Outils avancés** - Cryptographie, sondages, rappels, analyse
- [x] 🎮 **Commandes de divertissement** - Jeux interactifs et fun
- [x] ⚙️ **Utilitaires étendus** - Météo, traduction, informations détaillées
- [x] 🌐 **Panel web complet** - Contrôle, monitoring, gestion des serveurs
- [x] 🎫 **Système de support** - Interface utilisateur complète avec gestion admin
- [x] 🔢 **Numérotation séquentielle** - Tickets numérotés en continu
- [x] 🧹 **Système de nettoyage** - Suppression automatique des anciens tickets

### 🔮 À Venir
- [ ] � Commandes musicales (lecture YouTube/Spotify)
- [ ] 🎲 Système de niveaux et XP
- [ ] 🏆 Système d'achievements
- [ ] 📊 Statistiques avancées des utilisateurs
- [ ] 🤖 Commandes d'IA (ChatGPT integration)
- [ ] 📱 API REST complète
- [ ] 🌍 Support multilingue
- [ ] 📦 Système de plugins

### 🔧 Améliorations Techniques
- [ ] Migration vers PostgreSQL/MongoDB
- [ ] Système de cache Redis
- [ ] Interface web React/Vue.js
- [ ] Tests automatisés complets
- [ ] Docker containerization
- [ ] CI/CD avec GitHub Actions

## 🛠️ Comment créer votre bot Discord

1. Allez sur [Discord Developer Portal](https://discord.com/developers/applications)
2. Créez une nouvelle application
3. Allez dans la section "Bot"
4. Créez un bot et copiez le token
5. Invitez le bot sur votre serveur avec les bonnes permissions
6. Activez les intents nécessaires (Presence Intent, Server Members Intent)

### � Permissions requises
- Lire les messages
- Envoyer des messages
- Gérer les messages
- Utiliser les commandes slash
- Gérer les rôles (pour les commandes de modération)
- Bannir des membres (pour les commandes de modération)
- Expulser des membres (pour les commandes de modération)

## 📞 Support et Documentation

- 📚 **Aide intégrée** : `/help` ou `!help` pour l'aide interactive
- 🌐 **Panel web** - Logs et diagnostics détaillés
- 🎫 **Système de support** - Interface utilisateur pour signaler des problèmes
- 📚 **Documentation Discord.py** : https://discordpy.readthedocs.io/

---

**Développé avec ❤️ en Python**

*Ce bot utilise Discord.py 2.3.0+ et Flask pour une expérience moderne et complète.*