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

## 📝 Ajout de nouvelles commandes

Pour ajouter de nouvelles commandes :

1. **Commande slash** : Créez un fichier dans `slash/`
2. **Commande préfixée** : Créez un fichier dans `prefixe/`
3. Ajoutez le chargement dans `engine.py` si nécessaire

Chaque module doit avoir une fonction `setup(bot)` pour être chargé automatiquement.

---

Développé avec ❤️ en Python