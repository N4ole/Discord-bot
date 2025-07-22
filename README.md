# Discord-bot 🤖

Un bot Discord développé en Python avec une architecture multi-fichiers, supportant les commandes slash et préfixées.

## 📁 Structure du projet

```
Discord-bot/
├── main.py              # Point d'entrée principal
├── engine.py            # Moteur principal du bot
├── slash/               # Commandes slash (/)
│   ├── __init__.py
│   └── bonjour.py      # Commande slash /bonjour
├── prefixe/            # Commandes préfixées (!)
│   ├── __init__.py
│   └── bonjour.py      # Commande préfixée !bonjour
├── .env.example        # Exemple de configuration
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
pip install discord.py
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

## 📋 Commandes disponibles

### Commandes Slash
- `/bonjour` - Dit bonjour avec une belle carte embed
- `/setlog <canal>` - Définit le canal de logs (nécessite "Gérer le serveur")
- `/logon` - Active les logs (nécessite "Gérer le serveur")
- `/logoff` - Désactive les logs (nécessite "Gérer le serveur")
- `/logstatus` - Affiche le statut des logs

### Commandes Préfixées  
- `!bonjour` - Dit bonjour avec une belle carte embed
- `!prefix` - Gère le préfixe du bot pour ce serveur
  - `!prefix set <nouveau_préfixe>` - Change le préfixe (nécessite "Gérer le serveur")
  - `!prefix reset` - Remet le préfixe par défaut
  - `!prefix info` - Affiche les informations sur les préfixes
- `!setlog <canal>` - Définit le canal de logs (nécessite "Gérer le serveur")
- `!logon` - Active les logs (nécessite "Gérer le serveur")
- `!logoff` - Désactive les logs (nécessite "Gérer le serveur")
- `!logstatus` - Affiche le statut des logs

> 💡 **Note**: Le préfixe `!` peut être différent selon le serveur. Tu peux aussi mentionner le bot à la place du préfixe!

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