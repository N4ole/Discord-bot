# 📦 Guide d'installation - Bot Discord

## 🔧 Prérequis système

### Logiciels requis
- **Python 3.8+** (recommandé : Python 3.10+)
- **Git** pour cloner le repository
- **Éditeur de texte** (VS Code, Notepad++, etc.)

### Système d'exploitation
- ✅ Windows 10/11
- ✅ Linux (Ubuntu, Debian, CentOS)
- ✅ macOS 10.15+

## 📥 Installation étape par étape

### 1. Cloner le repository

```bash
git clone https://github.com/N4ole/Discord-bot.git
cd Discord-bot
```

### 2. Installer Python (si nécessaire)

#### Sur Windows
1. Téléchargez Python sur [python.org](https://python.org)
2. Cochez "Add Python to PATH" pendant l'installation
3. Vérifiez : `python --version`

#### Sur Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

#### Sur macOS
```bash
brew install python3
```

### 3. Créer un environnement virtuel (recommandé)

```bash
# Créer l'environnement
python -m venv discord-bot-env

# Activer l'environnement
# Sur Windows :
discord-bot-env\Scripts\activate
# Sur Linux/macOS :
source discord-bot-env/bin/activate
```

### 4. Installer les dépendances

```bash
pip install -r requirements.txt
```

Si `requirements.txt` n'existe pas, installez manuellement :
```bash
pip install discord.py flask asyncio sqlite3 requests aiohttp
```

## 🔑 Configuration Discord

### 1. Créer une application Discord

1. Allez sur [Discord Developer Portal](https://discord.com/developers/applications)
2. Cliquez "New Application"
3. Donnez un nom à votre bot
4. Allez dans l'onglet "Bot"
5. Cliquez "Add Bot"
6. Copiez le **Token** (gardez-le secret !)

### 2. Configurer les permissions

Dans l'onglet "Bot" :
- ✅ **Privileged Gateway Intents** :
  - `Presence Intent` (optionnel)
  - `Server Members Intent` (recommandé)
  - `Message Content Intent` (requis)

### 3. Inviter le bot sur votre serveur

1. Onglet "OAuth2" > "URL Generator"
2. **Scopes** : `bot` + `applications.commands`
3. **Bot Permissions** :
   - ✅ Administrator (ou permissions spécifiques)
   - ✅ Send Messages
   - ✅ Use Slash Commands
   - ✅ Manage Roles
   - ✅ Read Message History
4. Copiez l'URL générée et ouvrez-la

## ⚙️ Configuration du bot

### 1. Variables d'environnement

Créez un fichier `.env` dans le répertoire du bot :

```env
# Token du bot Discord (OBLIGATOIRE)
DISCORD_TOKEN=votre_token_ici

# Clé secrète pour Flask (OBLIGATOIRE)
FLASK_SECRET_KEY=une_cle_secrete_aleatoire_longue

# Configuration du serveur web (OPTIONNEL)
WEB_HOST=127.0.0.1
WEB_PORT=8080

# Configuration des logs (OPTIONNEL)
LOG_LEVEL=INFO
LOG_FILE=bot.log
```

### 2. Configuration des propriétaires

Éditez `bot_owners.json` pour ajouter votre ID Discord :

```json
{
  "description": "Liste des propriétaires du bot avec accès complet",
  "owners": [
    123456789012345678,
    987654321098765432
  ],
  "usage": "Ajoutez l'ID Discord des utilisateurs autorisés",
  "last_modified": "2025-07-24"
}
```

**Comment obtenir votre ID Discord :**
1. Activez le Mode Développeur (Paramètres > Avancé > Mode développeur)
2. Clic droit sur votre profil > "Copier l'ID utilisateur"

### 3. Configuration optionnelle

#### Préfixes personnalisés (`prefixes.json`)
```json
{
  "default": "!",
  "servers": {
    "123456789": "?",
    "987654321": "."
  }
}
```

#### Configuration des logs (`logs_config.json`)
```json
{
  "servers": {
    "123456789": {
      "enabled": true,
      "channel_id": 987654321,
      "events": ["member_join", "member_leave", "message_delete"]
    }
  }
}
```

## 🚀 Premier démarrage

### 1. Tester la configuration

```bash
python -c "import discord; print('Discord.py installé :', discord.__version__)"
```

### 2. Démarrer le bot

```bash
python main.py
```

### 3. Vérifications de démarrage

Le bot devrait afficher :
```
✅ Module xyz chargé
✅ Configuration terminée
🎉 [NomDuBot] est connecté et prêt !
🌐 Panel web accessible sur: http://127.0.0.1:8080
```

### 4. Tester les commandes

Sur Discord :
- `!help` - Aide générale
- `/ping` - Test de connectivité
- `!owner list` - Voir les propriétaires

### 5. Accéder à l'interface web

1. Ouvrez http://127.0.0.1:8080
2. Connectez-vous :
   - **Login** : `admin`
   - **Mot de passe** : `admin123`
3. ⚠️ **Changez immédiatement ces identifiants !**

## 🔧 Dépannage

### Erreurs courantes

#### "Token invalide"
- Vérifiez que le token est correct dans `.env`
- Assurez-vous qu'il n'y a pas d'espaces avant/après
- Régénérez le token si nécessaire

#### "Module non trouvé"
```bash
pip install --upgrade -r requirements.txt
```

#### "Permission denied"
- Vérifiez les permissions du bot sur Discord
- Assurez-vous que le bot a les intents requis

#### "Port 8080 déjà utilisé"
Changez le port dans `.env` :
```env
WEB_PORT=8081
```

### Logs de diagnostic

Consultez les logs pour identifier les problèmes :
- **Console** : Messages de démarrage
- **Interface web** : `/logs`
- **Fichiers** : `bot.log` (si configuré)

## 🔒 Sécurité

### Première configuration
1. **Changez les mots de passe par défaut** de l'interface web
2. **Gardez le token secret** - ne le partagez jamais
3. **Limitez les permissions** bot au minimum nécessaire
4. **Configurez un firewall** si le bot est accessible publiquement

### En production
- Utilisez un reverse proxy (nginx)
- Configurez HTTPS
- Utilisez un gestionnaire de processus (PM2, systemd)
- Sauvegardez régulièrement les configurations

## 📋 Checklist post-installation

- [ ] Bot connecté et répond aux commandes
- [ ] Interface web accessible
- [ ] Identifiants admin changés
- [ ] Propriétaires configurés dans `bot_owners.json`
- [ ] Permissions Discord correctes
- [ ] Logs fonctionnels
- [ ] Sauvegarde de la configuration

## 🆘 Support

Si vous rencontrez des problèmes :

1. **Consultez les logs** d'erreur
2. **Vérifiez la configuration** (token, permissions)
3. **Redémarrez le bot** complètement
4. **Consultez la documentation** complète
5. **Contactez le support** via l'interface web

---

*Guide d'installation v1.0 - Mise à jour : Juillet 2025*
