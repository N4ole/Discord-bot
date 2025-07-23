# 📖 Guide Complet des Commandes - Bot Discord

## 🏠 Vue d'ensemble

Ce bot Dis### ⚙️ Utilitaires

### Monitoring
- **Slash** : `/ping`
- **Préfixe** : `!ping`offre un système complet de commandes disponibles en deux formats :
- **Commandes Slash** : Tapez `/` et sélectionnez la commande
- **Commandes Préfixées** : Tapez le préfixe (par défaut `!`) suivi de la commande

---

## 🛡️ Modération

### Bannissement
- **Slash** : `/ban <membre> [raison]`
- **Préfixe** : `!ban <membre> [raison]`
- **Permission** : Bannir des membres

### Expulsion
- **Slash** : `/kick <membre> [raison]`
- **Préfixe** : `!kick <membre> [raison]`
- **Permission** : Expulser des membres

### Timeout (Mute)
- **Slash** : `/mute <membre> [durée] [raison]`
- **Préfixe** : `!mute <membre> [durée] [raison]`
- **Permission** : Modérer les membres
- **Durées supportées** : `10s`, `5m`, `2h`, `1d` (max 28 jours)

### Débannissement/Unmute
- **Slash** : `/unban <user_id>`, `/unmute <membre>`
- **Préfixe** : `!unban <user_id>`, `!unmute <membre>`

---

## 🎭 Gestion des Rôles

### Ajouter/Retirer des Rôles
- **Slash** : `/addrole <membre> <rôle>`, `/removerole <membre> <rôle>`
- **Préfixe** : `!addrole <membre> <rôle>`, `!removerole <membre> <rôle>`
- **Permission** : Gérer les rôles

### Afficher les Rôles
- **Slash** : `/roles [membre]`
- **Préfixe** : `!roles [membre]`

---

## 📊 Système de Logs

### Configuration
- **Slash** : `/setlog <canal>`, `/logon`, `/logoff`, `/logstatus`
- **Préfixe** : `!setlog <canal>`, `!logon`, `!logoff`, `!logstatus`, `!testlog`
- **Permission** : Gérer le serveur

### Événements Surveillés
- Messages (suppression, modification)
- Membres (arrivée, départ, rôles)
- Vocal (connexion, déconnexion)
- Modération (ban, unban)
- Canaux (création, suppression)

---

## 🛠️ Configuration

### Gestion des Préfixes
- **Slash** : `/prefix` (affichage uniquement)
- **Préfixe** : `!prefix`, `!prefix set <nouveau>`, `!prefix reset`
- **Permission** : Gérer le serveur

---

## 📋 Informations

### Utilisateurs
- **Slash** : `/info [membre]`, `/avatar [membre]`
- **Préfixe** : `!info [membre]`, `!avatar [membre]`

### Serveur
- **Slash** : `/server`, `/botinfo`, `/uptime`
- **Préfixe** : `!server`, `!botinfo`, `!uptime`

---

## ⚙️ Utilitaires

### Réseau et Monitoring
- **Slash** : `/ping`, `/weather <ville>`, `/translate <texte>`
- **Préfixe** : `!ping`, `!weather <ville>`, `!translate <texte>`

---

## 🎮 Divertissement

### Jeux
- **Slash** : `/coinflip`, `/8ball <question>`, `/rps <choix>`, `/choose <options>`
- **Préfixe** : `!coinflip`, `!8ball <question>`, `!rps <choix>`, `!choose <options>`

### Fun
- **Slash** : `/joke`, `/quote`, `/compliment [membre]`
- **Préfixe** : `!joke`, `!quote`, `!compliment [membre]`

---

## 🔧 Outils Avancés

### 📊 Analyse et Monitoring

#### `/analyze` ou `!analyze` - Analyse détaillée
**Usage slash :** `/analyze [utilisateur]`
**Usage préfixé :** `!analyze [utilisateur]` (aliases: `!analyse`, `!stats`)

**Fonctionnalités :**
- Analyse complète du serveur (membres, sécurité, statistiques)
- Analyse détaillée d'un utilisateur (ancienneté, rôles, permissions)
- Score de sécurité du serveur (0-4)
- Statistiques en temps réel

---

### 🧹 Gestion des Messages

#### `/clean` ou `!clean` - Nettoyage intelligent
**Usage slash :** `/clean <nombre> [utilisateur] [contient] [bots]`
**Usage préfixé :** `!clean <nombre> [filtres]` (aliases: `!purge`, `!clear`)

**Exemples :**
- `/clean 20` - Supprime 20 messages
- `/clean 50 user:@John` - Supprime 50 messages de John
- `/clean 30 contains:spam` - Messages contenant "spam"
- `!clean 25 bots` - Messages de bots uniquement

**Fonctionnalités :**
- Filtrage intelligent par utilisateur, contenu ou type
- Protection des messages épinglés
- Confirmation automatique avec statistiques
- **Permission requise** : Gérer les messages

---

#### `/remind` ou `!remind` - Système de rappels
**Usage :** `/remind <temps> <message>` ou `!remind <temps> <message>`
**Aliases préfixe :** `!reminder`, `!rappel`

**Formats de temps :**
- `s` = secondes, `m` = minutes, `h` = heures, `d` = jours, `w` = semaines
- Combinaisons : `1h30m`, `2d12h`, etc.

**Exemples :**
- `/remind 30m Réunion équipe`
- `!remind 2h Prendre médicament`
- `/remind 1d Anniversaire demain`

**Fonctionnalités :**
- Rappel en message privé + canal public
- Affichage du temps restant
- Maximum 30 jours de délai

---

### ️ Interaction Communautaire

#### `/poll` ou `!poll` - Sondages avancés
**Usage slash :** `/poll <question> <options> [durée]`
**Usage préfixé :** `!poll [durée] "question" option1,option2,option3` (aliases: `!sondage`, `!vote`)

**Exemples :**
- `/poll "Votre film préféré ?" "Action,Comédie,Horreur" 60`
- `!poll 30m "Menu ce soir ?" Pizza,Burger,Sushi`

**Fonctionnalités :**
- Jusqu'à 10 options maximum
- Timer automatique (optionnel, max 1 semaine)
- Résultats automatiques avec podium
- Calcul de pourcentages en temps réel
- Réactions automatiques (1️⃣-🔟)

---

### 📝 Utilitaires Texte (Préfixé uniquement)

#### `!count` ou `!wc` - Statistiques de texte
**Usage :** `!count <texte>` ou `!wc <texte>`

**Statistiques fournies :**
- Nombre de caractères (total et sans espaces)
- Nombre de mots
- Nombre de lignes
- Aperçu du texte

---

## 💡 Conseils d'utilisation

### ⚡ Performance
- Les commandes `/clean` sont limitées à 100 messages maximum
- Les rappels (`/remind`) ont une limite de 30 jours
- Les sondages peuvent durer jusqu'à 1 semaine

### 🛡️ Sécurité
- Les mots de passe générés sont automatiquement supprimés
- Les hashes MD5/SHA1 incluent des avertissements de sécurité
- Le nettoyage de messages nécessite la permission "Gérer les messages"

### 🎨 Interface
- Toutes les commandes utilisent des embeds colorés
- Les résultats incluent des timestamps automatiques
- Les erreurs sont accompagnées de conseils d'utilisation

### 🔄 Compatibilité
- Toutes les commandes existent en version slash (`/`) et préfixe (`!`)
- Syntaxe légèrement différente entre les deux formats
- Les aliases sont disponibles pour les commandes préfixées

---

## 🚀 Statistiques

Le bot dispose maintenant de :
- **39+ commandes slash**
- **50+ commandes préfixées**
- **9 catégories** de fonctionnalités
- **Support multilingue** (français/anglais)
- **Interface web** d'administration
- **Système de logs** complet
- **Monitoring** en temps réel

---

## 📞 Support

Pour obtenir de l'aide :
- Utilisez `/help` ou `!help` pour l'aide générale
- Utilisez `/help <catégorie>` pour une aide spécifique
- Mentionnez le bot pour une aide rapide
- Consultez ce guide pour les détails complets

**Profitez de toutes ces fonctionnalités pour améliorer votre serveur Discord !** 🎉
