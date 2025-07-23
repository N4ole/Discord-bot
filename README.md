# 🤖## ✨ Fonctionnalités principales

- 🏗️ **Architecture modulaire** - Commandes organisées par cat### 🔧 **Nouvelles Commandes d'Outils Avancés**
- 📊 **Analyse** : `/analyze` - Analyse détaillée serveur/utilisateur avec scoring sécurité
- 🧹 **Nettoyage** : `/clean` - Suppression intelligente de messages avec filtres
- ⏰ **Rappels** : `/remind` - Système de rappels programmables jusqu'à 30 jours
- 🗳️ **Sondages** : `/poll` - Sondages interactifs avec timer automatique et résultats
- ⚡ **Double interface** - Commandes slash (/) ET préfixées (!)
- 🌐 **Multi-serveur** - Configuration indépendante par serveur
- 📊 **Système de logs** - Surveillance complète des activités
- 🛡️ **Modération complète** - Ban, kick, mute avec gestio## 📝 Ajout de nouvelles commandes

Pour ajouter de nouvelles commandes :

1. **Commande slash** : Créez un fichier dans `slash/`
2. **Commande préfixée** : Créez un fichier dans `prefixe/`
3. Ajoutez le chargement dans `engine.py` dans la méthode `setup_hook()`

Chaque module doit avoir une fonction `setup(bot)` pour être chargé automatiquement.

## 🚀 Déploiement et Production

### 🔧 Configuration de Production
1. **Changez les identifiants par défaut** dans `web_panel.py`
2. **Utilisez un serveur WSGI** comme Gunicorn pour le panel web
3. **Configurez un reverse proxy** (Nginx) pour HTTPS
4. **Activez les logs en fichier** pour la persistance
5. **Utilisez une base de données** pour les configurations (optionnel)

### 🛡️ Sécurité
- ✅ Tokens et mots de passe dans des variables d'environnement
- ✅ Authentification obligatoire pour le panel web
- ✅ Sessions sécurisées avec timeout automatique
- ✅ Validation des permissions Discord
- ✅ Logs d'audit pour toutes les actions sensibles

### 📊 Monitoring
- ✅ Statistiques en temps réel via le panel web
- ✅ Logs détaillés de tous les événements
- ✅ Métriques de performance et d'utilisation
- ✅ Alertes automatiques en cas d'erreur

## 🆘 Dépannage et FAQ

### ❓ Problèmes Courants

**Q: Le bot ne répond pas aux commandes**
- Vérifiez que le token Discord est correct dans `.env`
- Assurez-vous que le bot a les permissions nécessaires sur le serveur
- Vérifiez que les intents sont activés (Members, Presences)

**Q: Les commandes slash n'apparaissent pas**
- Utilisez la commande `/sync` ou le bouton dans le panel web
- Attendez quelques minutes (propagation Discord)
- Vérifiez les permissions "Use Application Commands"

**Q: Le panel web ne fonctionne pas**
- Vérifiez que le port 8080 n'est pas utilisé par un autre programme
- Assurez-vous que Flask et Werkzeug sont installés
- Vérifiez la configuration dans `.env`

**Q: Erreur "Intents" au démarrage**
- Activez "Presence Intent" et "Server Members Intent" dans le Developer Portal
- Redémarrez le bot après avoir modifié les intents

**Q: Les logs ne s'affichent pas**
- Configurez d'abord un canal avec `/setlog #canal`
- Activez les logs avec `/logon`
- Vérifiez que le bot peut écrire dans le canal

### 🔧 Commandes de Diagnostic

#### Pour les Propriétaires du Bot
- `!diag` - Diagnostic complet du bot
- `!servers` - Liste des serveurs connectés
- `!stats` - Statistiques globales

#### Panel Web
- **Contrôle > Synchroniser** - Resynchronise les commandes slash
- **Contrôle > Vider le cache** - Remet à zéro les statistiques
- **Logs** - Consultation détaillée de l'historique

## � Documentation des Commandes

### 🆘 **Système d'Aide Intégré**

#### **Aide Générale**
- **Slash** : `/help` - Interface interactive avec sélection de catégories
- **Préfixe** : `!help` - Aide complète avec toutes les commandes

#### **Aide par Catégorie** (Slash)
- `/help category:moderation` - �️ Commandes de modération (ban, kick, mute, clean)
- `/help category:roles` - 🎭 Gestion des rôles
- `/help category:logs` - 📊 Système de logs et surveillance
- `/help category:config` - 🛠️ Configuration et préfixes
- `/help category:info` - 📋 Informations utilisateur/serveur
- `/help category:fun` - 🎮 Divertissement et jeux
- `/help category:tools` - 🔧 Outils avancés (cryptographie, sondages, rappels)
- `/help category:utils` - ⚙️ Utilitaires (ping, météo, traduction)

#### **Aide Spécifique** (Préfixe)
- `!help <commande>` - Aide détaillée d'une commande avec usage et exemples

### 📚 **Documentation Complète**
- 📄 **[AIDE_COMPLETE.md](AIDE_COMPLETE.md)** - Guide complet avec tous les détails et exemples
- � **[NOUVELLES_COMMANDES.md](NOUVELLES_COMMANDES.md)** - Guide des outils avancés récemment ajoutés

### 🔧 **Nouvelles Commandes d'Outils Avancés**
- 📊 **Analyse** : `/analyze` - Analyse détaillée serveur/utilisateur avec scoring sécurité
- 🧹 **Nettoyage** : `/clean` - Suppression intelligente de messages avec filtres
- ⏰ **Rappels** : `/remind` - Système de rappels programmables jusqu'à 30 jours
- � **Cryptographie** : `/encode`, `/decode`, `/hash` - Encodage Base64 et hashes sécurisés
- 🔒 **Sécurité** : `/password` - Générateur de mots de passe avec calcul d'entropie
- 🗳️ **Sondages** : `/poll` - Sondages interactifs avec timer automatique et résultats

### 📞 Support et Documentation
- 📚 **Aide intégrée** : `/help` ou `!help` pour l'aide interactive
- 📖 **[AIDE_COMPLETE.md](AIDE_COMPLETE.md)** - Guide complet de toutes les commandes
- 📝 **[NOUVELLES_COMMANDES.md](NOUVELLES_COMMANDES.md)** - Guide des outils avancés
- 🌐 **Panel web** - Logs et diagnostics détaillés
- 📚 Documentation Discord.py : https://discordpy.readthedocs.io/

### 🎯 Roadmap et Améliorations Futures

### ✅ **Récemment Ajouté**
- [x] 🔧 **Outils avancés** - Cryptographie, sondages, rappels, analyse
- [x] 🎮 **Commandes de divertissement** - Jeux interactifs et fun
- [x] ⚙️ **Utilitaires étendus** - Météo, traduction, informations détaillées
- [x] 🌐 **Panel web complet** - Contrôle, monitoring, gestion des serveurs
- [x] 📖 **Documentation complète** - Guides détaillés et aide interactive
- [ ] 🎵 Commandes musicales (lecture YouTube/Spotify)
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
- [ ] CI/CD avec GitHub Actionses
- 💬 **Mention interactive** - Aide automatique en mentionnant le bot
- ⚙️ **Préfixes personnalisables** - Chaque serveur peut avoir son préfixe
- 🌐 **Panel web d'administration** - Interface web sécurisée pour monitorer le bot
- 🔧 **Commandes utilitaires** - Ping, infos utilisateur/serveur, météo, traduction
- 🎮 **Commandes de divertissement** - Jeux, blagues, citations, mini-jeuxBot Multi-Fonctionnel

Un bot Discord complet développé en Python avec une architecture modulaire, supportant les commandes slash et préfixées avec système multi-serveur et panel web d'administration.

## ✨ Fonctionnalités principales

- 🏗️ **Architecture modulaire** - Commandes organisées par catégories
- ⚡ **Double interface** - Commandes slash (/) ET préfixées (!)
- 🌐 **Multi-serveur** - Configuration indépendante par serveur
- � **Système de logs** - Surveillance complète des activités
- 🛡️ **Modération complète** - Ban, kick, mute avec gestion des rôles
- 💬 **Mention interactive** - Aide automatique en mentionnant le bot
- ⚙️ **Préfixes personnalisables** - Chaque serveur peut avoir son préfixe

## �📁 Structure du projet

```
Discord-bot/
├── main.py                  # Point d'entrée principal
├── engine.py                # Moteur principal du bot
├── prefix_manager.py        # Gestion des préfixes multi-serveur
├── log_manager.py          # Système de logs
├── log_events.py           # Écouteurs d'événements
├── bot_mentions.py         # Gestion des mentions du bot
├── multiserver_diagnostic.py # Diagnostics pour le propriétaire
├── web_panel.py            # 🌐 Panel web d'administration
├── templates/              # 🎨 Templates HTML pour le panel web
│   ├── login.html         # Page de connexion
│   ├── dashboard.html     # Tableau de bord principal
│   ├── logs.html          # Interface de consultation des logs
│   └── stats.html         # Statistiques détaillées
├── slash/                  # Commandes slash (/)
│   ├── __init__.py
│   ├── bonjour.py         # Commande de salutation
│   ├── logs.py            # Configuration des logs
│   ├── admin.py           # Commandes de modération
│   ├── admin_roles.py     # Gestion des rôles
│   ├── help.py            # Système d'aide interactif
│   ├── utils.py           # 🔧 Commandes utilitaires (ping, info, météo...)
│   └── fun.py             # 🎮 Commandes de divertissement (jeux, blagues...)
├── prefixe/               # Commandes préfixées (!)
│   ├── __init__.py
│   ├── bonjour.py         # Commande de salutation
│   ├── prefix.py          # Gestion des préfixes
│   ├── logs.py            # Configuration des logs
│   ├── admin.py           # Commandes de modération
│   ├── admin_roles.py     # Gestion des rôles
│   ├── help.py            # Système d'aide détaillé
│   ├── utils.py           # 🔧 Commandes utilitaires (versions préfixées)
│   └── fun.py             # 🎮 Commandes de divertissement (versions préfixées)
├── data/                  # Données persistantes (auto-généré)
│   ├── prefixes.json      # Configuration des préfixes
│   └── logs_config.json   # Configuration des logs
├── .env                   # Variables d'environnement (à créer)
├── .env.example          # Exemple de configuration
├── .env.panel            # Configuration du panel web
└── README.md
```

## 🚀 Installation et Configuration

1. **Clonez le repository**
```bash
git clone <votre-repo>
cd Discord-bot
```

2. **Installez les dépendances**
```bash
pip install -r requirements.txt
```

3. **Configurez le token Discord**
   - Copiez `.env.example` vers `.env`
   - Remplacez `YOUR_DISCORD_BOT_TOKEN` par votre vrai token Discord
   ```bash
   cp .env.example .env
   ```

4. **Lancez le bot**
```bash
python main.py
```

## 🌐 Panel Web d'Administration

Le bot inclut un **panel web complet** pour l'administration et la surveillance !

### 🚀 **Accès au Panel**
- **URL** : http://127.0.0.1:8080 (une fois le bot lancé)
- **Identifiants par défaut** : `admin` / `admin123`
- ⚠️ **Important** : Changez les identifiants dans `web_panel.py` pour la production !

### 🎛️ **Fonctionnalités du Panel**

#### 📊 **Dashboard Principal**
- **Statistiques en temps réel** : serveurs, utilisateurs, commandes
- **Statut du bot** et temps de fonctionnement (uptime)
- **Compteurs d'erreurs** et d'activité
- **Actualisation automatique** toutes les 10 secondes

#### 📝 **Gestion des Logs**
- **Consultation complète** de l'historique
- **Filtres avancés** par niveau (INFO, SUCCESS, WARNING, ERROR)
- **Recherche textuelle** dans les messages
- **Pagination** pour une navigation fluide

#### 📈 **Statistiques Détaillées**
- **Graphiques d'utilisation** par heure sur 24h
- **Types d'erreurs** avec compteurs détaillés
- **Métriques de performance** (taux de succès, etc.)
- **Informations système** complètes

#### 🎛️ **Contrôle du Bot** (NOUVEAU !)
- **Liste complète des serveurs** avec détails (membres, canaux, rôles)
- **Quitter un serveur** avec confirmation sécurisée
- **Commandes de maintenance** :
  - 🔄 Synchroniser les commandes slash
  - 🗑️ Vider le cache
  - 📊 Mettre à jour les statistiques
  - 🔄 Recharger les modules
- **Informations détaillées du bot** (latence, uptime, etc.)
- **Sécurité** : Confirmation requise pour les actions critiques

### 🔐 **Sécurité du Panel**
- ✅ **Authentification obligatoire** pour toutes les pages
- ✅ **Sessions sécurisées** avec timeout automatique
- ✅ **Mots de passe hashés** (jamais stockés en clair)
- ✅ **Logs d'audit** pour toutes les actions admin
- ✅ **Confirmations** pour les actions critiques (quitter un serveur)

### 🛠️ **Utilitaires d'Administration**
Utilisez `python admin_panel.py` pour :
- Créer de nouveaux utilisateurs admin
- Générer des configurations Flask sécurisées
- Voir les statistiques du panel

## 🌐 Panel Web d'Administration

Le bot intègre un **panel web sécurisé** pour surveiller et administrer le bot à distance !

### 🚀 Accès au Panel
- **URL** : `http://127.0.0.1:8080` (démarre automatiquement avec le bot)
- **Identifiants par défaut** : `admin` / `admin123`
- **⚠️ Important** : Changez les identifiants dans `web_panel.py` pour la production !

### 📊 Fonctionnalités du Panel
- **📈 Dashboard en temps réel** - Statistiques du bot, uptime, serveurs connectés
- **📝 Consultation des logs** - Filtrage par niveau, recherche, pagination
- **📊 Statistiques détaillées** - Commandes par heure, types d'erreurs, métriques
- **🔄 Actualisation automatique** - Données mises à jour toutes les 10 secondes
- **📱 Interface responsive** - Compatible mobile et desktop
- **🔐 Authentification sécurisée** - Session avec timeout automatique

### 🛡️ Sécurité
- **Mots de passe hashés** avec Werkzeug
- **Sessions sécurisées** avec clés secrètes
- **Logs d'audit** pour toutes les connexions
- **Interface d'administration** accessible uniquement aux utilisateurs autorisés

### ⚙️ Configuration Avancée
Modifiez le fichier `.env.panel` pour personnaliser :
- Identifiants administrateurs
- Port et adresse du serveur web
- Paramètres de sécurité
- Fonctionnalités activées

## 💬 Système d'aide intégré

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
- `/ping` ou `!ping` - Affiche la latence du bot et les statistiques de connexion
- `/info [utilisateur]` ou `!info [utilisateur]` - Informations détaillées d'un utilisateur
- `/server` ou `!server` - Informations complètes du serveur (membres, canaux, rôles...)
- `/avatar [utilisateur]` ou `!avatar [utilisateur]` - Affiche l'avatar d'un utilisateur en haute résolution
- `/uptime` ou `!uptime` - Temps de fonctionnement du bot avec statistiques
- `/botinfo` ou `!botinfo` - Informations complètes du bot (version, serveurs, utilisateurs...)

#### 🌐 Utilitaires Web (slash ET préfixé)
- `/weather <ville>` ou `!weather <ville>` - Météo actuelle d'une ville
- `/translate <texte>` ou `!translate <texte>` - Traduction automatique de texte

#### 🔗 Utilitaires Préfixés Exclusifs
- `!invite` - Génère un lien d'invitation pour le bot
- `!roll [XdY]` - Lance des dés (par défaut 1d6, personnalisable ex: `!roll 2d20`)

### 🎮 Commandes de Divertissement

#### 🎯 Jeux et Hasard (slash ET préfixé)
- `/coinflip` ou `!coinflip` (alias: `!coin`) - Lance une pièce de monnaie
- `/rps <choix>` ou `!rps <choix>` (alias: `!ppc`) - Pierre-papier-ciseaux contre le bot
- `/8ball <question>` ou `!8ball <question>` (alias: `!ball`) - Pose une question à la boule magique
- `/choose <option1> <option2> ...` ou `!choose <option1> <option2> ...` (alias: `!pick`) - Choisit aléatoirement entre plusieurs options

#### 😄 Divertissement et Social (slash ET préfixé)
- `/joke` ou `!joke` - Raconte une blague aléatoire
- `/quote` ou `!quote` (alias: `!citation`) - Affiche une citation inspirante
- `/compliment [utilisateur]` ou `!compliment [utilisateur]` - Donne un compliment

#### 🎨 Divertissement Préfixé Exclusif
- `!hug <utilisateur>` - Faire un câlin virtuel à quelqu'un
- `!ascii <texte>` - Génère de l'art ASCII simple

### 🔧 Commandes d'Outils Avancés

#### 📊 Analyse et Monitoring (slash ET préfixé)
- `/analyze [utilisateur]` ou `!analyze [utilisateur]` - Analyse détaillée d'un serveur ou utilisateur
- `/clean <nombre> [filtres]` ou `!clean <nombre> [filtres]` - Nettoyage avancé des messages avec filtres
- `/remind <temps> <message>` ou `!remind <temps> <message>` - Système de rappels programmés

#### 🔐 Sécurité et Cryptographie (slash ET préfixé)
- `/encode <texte>` ou `!encode <texte>` - Encode du texte en base64
- `/decode <texte>` ou `!decode <texte>` - Décode du texte base64
- `/hash <algorithme> <texte>` ou `!hash <algorithme> <texte>` - Génère des hashes (MD5, SHA1, SHA256, SHA512)
- `/password [longueur] [options]` ou `!password [longueur] [options]` - Génère des mots de passe sécurisés

#### 🗳️ Interaction Communautaire (slash ET préfixé)
- `/poll <question> <options> [durée]` ou `!poll [durée] "question" option1,option2...` - Sondages avancés avec timer

#### 📝 Utilitaires Texte Préfixés Exclusifs
- `!count <texte>` (alias: `!wc`) - Compte caractères, mots et lignes dans un texte

### ⚙️ Configuration

#### 🏷️ Gestion des Préfixes (préfixé uniquement)
- `!prefix` - Gère le préfixe du bot pour ce serveur
  - `!prefix set <nouveau_préfixe>` - Change le préfixe (nécessite "Gérer le serveur")
  - `!prefix reset` - Remet le préfixe par défaut
  - `!prefix info` - Affiche les informations sur les préfixes

#### 📊 Système de Logs (slash ET préfixé)
- `/setlog <canal>` ou `!setlog <canal>` - Définit le canal de logs (nécessite "Gérer le serveur")
- `/logon` ou `!logon` - Active les logs (nécessite "Gérer le serveur")  
- `/logoff` ou `!logoff` - Désactive les logs (nécessite "Gérer le serveur")
- `/logstatus` ou `!logstatus` - Affiche le statut des logs

#### 🛡️ Commandes de Modération (slash ET préfixé)
- `/ban <membre> [raison]` ou `!ban <membre> [raison]` - Bannit un membre (nécessite "Bannir des membres")
- `/unban <user_id> [raison]` ou `!unban <user_id> [raison]` - Débannit un utilisateur (nécessite "Bannir des membres")
- `/kick <membre> [raison]` ou `!kick <membre> [raison]` - Expulse un membre (nécessite "Expulser des membres")
- `/mute <membre> [durée] [raison]` ou `!mute <membre> [durée] [raison]` - Met un membre en timeout (nécessite "Modérer les membres")
- `/unmute <membre> [raison]` ou `!unmute <membre> [raison]` - Retire le timeout (nécessite "Modérer les membres")

#### 🎭 Gestion des Rôles (slash ET préfixé)
- `/addrole <membre> <rôle>` ou `!addrole <membre> <rôle>` - Ajoute un rôle à un membre (nécessite "Gérer les rôles")
- `/removerole <membre> <rôle>` ou `!removerole <membre> <rôle>` - Retire un rôle d'un membre (nécessite "Gérer les rôles")

#### � Informations (slash ET préfixé)
- `/roles [membre]` ou `!roles [membre]` - Affiche les rôles d'un membre
- `/userinfo [membre]` ou `!userinfo [membre]` - Affiche les informations d'un membre
- `/serverinfo` ou `!serverinfo` - Affiche les informations du serveur

> 💡 **Note**: Le préfixe `!` peut être différent selon le serveur. Tu peux aussi mentionner le bot (`@BotName`) pour obtenir de l'aide !

## 🛠️ Comment créer votre bot Discord

1. Allez sur [Discord Developer Portal](https://discord.com/developers/applications)
2. Créez une nouvelle application
3. Allez dans la section "Bot"
4. Créez un bot et copiez le token
5. Invitez le bot sur votre serveur avec les bonnes permissions

## 🔧 Fonctionnalités

- ✅ Architecture modulaire avec des cogs
- ✅ Support des commandes slash modernes
- ✅ Support des commandes préfixées classiques
- ✅ **Préfixes personnalisés par serveur**
- ✅ **Système de logs complet**
- ✅ **🛡️ Commandes d'administration complètes**
- ✅ **🎭 Gestion avancée des rôles**
- ✅ **📊 Commandes d'information détaillées**
- ✅ **🔧 Utilitaires complets** (météo, traduction, infos système)
- ✅ **🎮 Divertissement interactif** (jeux, blagues, citations)
- ✅ **🌐 Panel web d'administration**
- ✅ **⚡ Monitoring en temps réel**
- ✅ Gestion d'erreurs robuste
- ✅ Embeds Discord élégants
- ✅ Chargement automatique des modules
- ✅ Support multi-serveurs complet
- ✅ **🎭 Gestion avancée des rôles**
- ✅ **📊 Commandes d'information**
- ✅ Gestion d'erreurs
- ✅ Embeds Discord élégants
- ✅ Chargement automatique des modules

## 🎯 Gestion des Préfixes

Le bot supporte des **préfixes personnalisés par serveur** ! 

### Configuration
- **Préfixe par défaut**: `!`
- **Mention**: Tu peux toujours utiliser `@BotName` comme préfixe
- **Persistance**: Les préfixes sont sauvegardés automatiquement

### Règles pour les préfixes
- Maximum 5 caractères
- Caractères interdits: `@` `#` `` ` `` `\` `/`
- Pas d'espaces uniquement

### Permissions requises
- Seuls les membres avec la permission "Gérer le serveur" peuvent changer le préfixe

## � Système de Logs

Le bot dispose d'un **système de logs complet** qui surveille automatiquement toutes les activités du serveur !

### 🎯 Configuration rapide
1. **Définir le canal** : `/setlog #logs` ou `!setlog #logs`
2. **Activer** : `/logon` ou `!logon`
3. **Vérifier** : `/logstatus` ou `!logstatus`

### 📋 Événements surveillés
- **💬 Messages** : Suppression, modification
- **👥 Membres** : Arrivée, départ, changements de rôles
- **🔊 Vocal** : Connexion, déconnexion, changement de canal
- **🔨 Modération** : Bannissements, débannissements
- **📝 Canaux** : Création, suppression
- **🎭 Rôles** : Attribution, retrait

### 🎨 Fonctionnalités avancées
- **Embeds colorés** selon le type d'événement
- **Timestamps** automatiques
- **Informations détaillées** (IDs, liens, contexte)
- **✨ Configuration par serveur** indépendante
- **🌐 Support multi-serveurs** natif
- **Sauvegarde automatique** des paramètres

### 🌐 Multi-Serveurs
Le bot peut être utilisé simultanément sur **plusieurs serveurs Discord** avec des configurations complètement **indépendantes** :

- **🏠 Configuration unique** : Chaque serveur a ses propres paramètres (canal de logs, activation/désactivation)
- **📊 Isolation complète** : Les logs d'un serveur n'interfèrent jamais avec ceux d'un autre
- **⚡ Performance optimisée** : Un seul bot peut gérer des dizaines de serveurs
- **🔧 Gestion centralisée** : Commandes de diagnostic pour les propriétaires du bot

**Exemple de configuration multi-serveurs :**
```json
{
  "serveur_A_id": {"channel_id": 123, "enabled": true},
  "serveur_B_id": {"channel_id": 456, "enabled": false},
  "serveur_C_id": {"channel_id": 789, "enabled": true}
}
```

### 🔒 Sécurité
- Seuls les membres avec "Gérer le serveur" peuvent configurer les logs
- Pas de logs pour les actions de bots (évite le spam)
- Gestion d'erreurs robuste

## �📝 Ajout de nouvelles commandes

Pour ajouter de nouvelles commandes :

1. **Commande slash** : Créez un fichier dans `slash/`
2. **Commande préfixée** : Créez un fichier dans `prefixe/`
3. Ajoutez le chargement dans `engine.py` si nécessaire

Chaque module doit avoir une fonction `setup(bot)` pour être chargé automatiquement.

---

Développé avec ❤️ en Python