# Di## ✨ Fonctionnalités principales

- 🏗️ **Architecture modulaire** - Commandes organisées par catégories
- ⚡ **Double interface** - Commandes slash (/) ET préfixées (!)
- 🌐 **Multi-serveur** - Configuration indépendante par serveur
- 📊 **Système de logs** - Surveillance complète des activités
- 🛡️ **Modération complète** - Ban, kick, mute avec gestion des rôles
- 💬 **Mention interactive** - Aide automatique en mentionnant le bot
- ⚙️ **Préfixes personnalisables** - Chaque serveur peut avoir son préfixe
- 🌐 **Panel web d'administration** - Interface web sécurisée pour monitorer le bot 🤖

Un bot Discord développé en Python avec une architecture multi-fichiers, supportant les commandes slash et préfixées avec système multi-serveur.

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
│   └── help.py            # Système d'aide interactif
├── prefixe/               # Commandes préfixées (!)
│   ├── __init__.py
│   ├── bonjour.py         # Commande de salutation
│   ├── prefix.py          # Gestion des préfixes
│   ├── logs.py            # Configuration des logs
│   ├── admin.py           # Commandes de modération
│   ├── admin_roles.py     # Gestion des rôles
│   └── help.py            # Système d'aide détaillé
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
pip install discord.py python-dotenv flask werkzeug
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