# 🎯 Guide des Nouvelles Commandes Utiles

Le bot Discord a été enrichi avec de puissantes commandes d'outils avancés ! Voici un gui## 🚀 **Nouveaux totaux de commandes**

Le bot dispose maintenant de **35+ commandes slash** et plus de **45+ commandes préfixées** réparties dans :

- 🏠 **Base** : Salutations, aide
- ⚙️ **Configuration** : Préfixes, logs
- 🛡️ **Modération** : Ban, kick, mute, clean
- 🎭 **Rôles** : Gestion complète des rôles
- 📊 **Information** : Stats serveur/utilisateur, analyse
- 🔧 **Utilitaires** : Ping, monitoring
- 🎮 **Divertissement** : Jeux, blagues, citations
- 🔧 **Outils Avancés** : Analyse, sondages, rappels, nettoyageour les utiliser.

## 🔧 Commandes d'Outils Avancés (4 commandes principales)

### 📊 **Analyse et Monitoring**

#### `/analyze` ou `!analyze` - Analyse détaillée
**Usage slash :** `/analyze [utilisateur]`
**Usage préfixé :** `!analyze [utilisateur]`

**Exemples :**
- `/analyze` - Analyse complète du serveur (membres, sécurité, statistiques)
- `/analyze @John` - Analyse détaillée d'un utilisateur (ancienneté, rôles, permissions)
- `!analyze` - Version préfixée pour analyser le serveur

**Ce que vous obtenez :**
- 📊 Statistiques complètes (membres, bots, humains)
- 🛡️ Score de sécurité du serveur (0-4)
- 🎭 Analyse des rôles et permissions
- 📱 Statut et activité des utilisateurs

---

#### `/clean` ou `!clean` - Nettoyage intelligent des messages
**Usage slash :** `/clean <nombre> [utilisateur] [contient] [bots]`
**Usage préfixé :** `!clean <nombre> [filtres]`

**Exemples slash :**
- `/clean 20` - Supprime les 20 derniers messages
- `/clean 50 user:@John` - Supprime 50 messages de John
- `/clean 30 contains:spam` - Supprime 30 messages contenant "spam"
- `/clean 25 bots:True` - Supprime 25 messages de bots

**Exemples préfixés :**
- `!clean 20` - Supprime 20 messages
- `!clean 50 user:@John` - Supprime 50 messages de John
- `!clean 30 contains:spam` - Messages contenant "spam"
- `!clean 25 bots` - Messages de bots uniquement

**Fonctionnalités :**
- 🧹 Filtrage intelligent par utilisateur, contenu ou type
- 🛡️ Protection des messages épinglés
- ⚡ Confirmation automatique avec statistiques

---

#### `/remind` ou `!remind` - Système de rappels
**Usage :** `/remind <temps> <message>` ou `!remind <temps> <message>`

**Formats de temps supportés :**
- `s` = secondes, `m` = minutes, `h` = heures, `d` = jours, `w` = semaines
- Combinaisons possibles : `1h30m`, `2d12h`, etc.

**Exemples :**
- `/remind 30m Réunion équipe`
- `!remind 2h Prendre médicament`
- `/remind 1d Anniversaire demain`
- `!remind 1w Backup serveur`

**Fonctionnalités :**
- ⏰ Rappel en message privé + canal public
- 📅 Affichage du temps restant en temps réel
- 🎯 Maximum 30 jours de délai

---

### ️ **Interaction Communautaire**

#### `/poll` ou `!poll` - Sondages avancés
**Usage slash :** `/poll <question> <options> [durée]`
**Usage préfixé :** `!poll [durée] "question" option1,option2,option3`

**Exemples slash :**
- `/poll "Votre film préféré ?" "Action,Comédie,Horreur,Drame" 60`
- `/poll "Réunion demain ?" "Oui,Non,Peut-être"`

**Exemples préfixés :**
- `!poll "Quel framework ?" React,Vue,Angular`
- `!poll 30m "Menu ce soir ?" Pizza,Burger,Sushi,Salade`
- `!poll 2h "Sortie weekend ?" Cinéma,Restaurant,Parc,Maison`

**Fonctionnalités :**
- 🗳️ Jusqu'à 10 options maximum
- ⏰ Timer automatique (optionnel, max 1 semaine)
- 🏆 Résultats automatiques avec podium
- 📊 Calcul de pourcentages en temps réel
- 🎯 Réactions automatiques (1️⃣-🔟)

---

### 📝 **Utilitaires Texte** (Préfixé uniquement)

#### `!count` ou `!wc` - Statistiques de texte
**Usage :** `!count <texte>` ou `!wc <texte>`

**Exemples :**
- `!count Lorem ipsum dolor sit amet...`
- `!wc "Texte avec plusieurs mots et lignes"`

**Statistiques fournies :**
- 📝 Nombre de caractères (total)
- 🔤 Caractères sans espaces
- 📖 Nombre de mots
- 📄 Nombre de lignes
- 👁️ Aperçu du texte (premiers 100 caractères)

---

## 🎯 **Conseils d'utilisation**

### ⚡ **Performance**
- Les commandes `/clean` sont limitées à 100 messages maximum
- Les rappels (`/remind`) ont une limite de 30 jours
- Les sondages peuvent durer jusqu'à 1 semaine

### 🛡️ **Sécurité**
- Les mots de passe générés sont automatiquement supprimés
- Les hashes MD5/SHA1 incluent des avertissements de sécurité
- Le nettoyage de messages nécessite la permission "Gérer les messages"

### 🎨 **Interface**
- Toutes les commandes utilisent des embeds colorés
- Les résultats incluent des timestamps automatiques
- Les erreurs sont accompagnées de conseils d'utilisation

### 🔄 **Compatibilité**
- Toutes les commandes existent en version slash (`/`) et préfixe (`!`)
- Syntaxe légèrement différente entre les deux formats
- Les alias sont disponibles pour les commandes préfixées

---

## 🚀 **Nouveaux totaux de commandes**

Le bot dispose maintenant de **39 commandes slash** et plus de **50 commandes préfixées** réparties dans :

- 🏠 **Base** : Salutations, aide
- ⚙️ **Configuration** : Préfixes, logs
- 🛡️ **Modération** : Ban, kick, mute, clean
- 🎭 **Rôles** : Gestion complète des rôles
- 📊 **Information** : Stats serveur/utilisateur, analyse
- 🔧 **Utilitaires** : Ping, météo, traduction, monitoring
- 🎮 **Divertissement** : Jeux, blagues, citations
- 🔐 **Outils Avancés** : Cryptographie, sondages, rappels

**Profitez de ces nouveaux outils pour améliorer votre serveur Discord !** 🎉
