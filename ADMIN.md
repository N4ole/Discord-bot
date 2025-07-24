# 🛡️ Documentation Administrateurs - Bot Discord

## 👤 Rôle des administrateurs

Les administrateurs ont des permissions étendues pour :
- Gérer leur serveur spécifique
- Configurer les fonctionnalités du bot
- Accéder à l'interface web
- Modérer et administrer les utilisateurs
- Consulter les logs et statistiques

*Note : Les propriétaires ont automatiquement tous les droits d'administrateur*

## 🎮 Commandes de modération

### Gestion des membres

#### `/ban <user> [reason]`
Bannit un utilisateur du serveur.
```
/ban @user#1234 Comportement inapproprié
```

#### `/kick <user> [reason]`
Expulse un utilisateur du serveur.
```
/kick @user#1234 Spam
```

#### `/timeout <user> <duration> [reason]`
Met un utilisateur en timeout.
```
/timeout @user#1234 1h Flood
```

#### `/warn <user> <reason>`
Avertit un utilisateur (log automatique).
```
/warn @user#1234 Langue inappropriée
```

### Gestion des messages

#### `/clear <amount> [user]`
Supprime des messages.
```
/clear 10          # Supprime 10 messages
/clear 5 @user     # Supprime 5 messages de cet utilisateur
```

#### `/lock [channel]`
Verrouille un salon.
```
/lock              # Salon actuel
/lock #general     # Salon spécifique
```

#### `/unlock [channel]`
Déverrouille un salon.

### Gestion des rôles

#### `/role add <user> <role>`
Ajoute un rôle à un utilisateur.
```
/role add @user#1234 @Modérateur
```

#### `/role remove <user> <role>`
Retire un rôle d'un utilisateur.

#### `/role create <name> [color] [permissions]`
Crée un nouveau rôle.
```
/role create "Support" blue manage_messages
```

## ⚙️ Configuration du serveur

### Préfixes personnalisés

#### `!prefix set <nouveau_préfixe>`
Change le préfixe du serveur.
```
!prefix set ?
!prefix set !
```

#### `!prefix reset`
Remet le préfixe par défaut (`!`).

### Système de logs

#### `!logs setup <channel>`
Configure le salon de logs.
```
!logs setup #logs
```

#### `!logs events <event1> <event2>...`
Configure les événements à logger.
```
!logs events member_join member_leave message_delete ban
```

**Événements disponibles :**
- `member_join` - Arrivée de membres
- `member_leave` - Départ de membres
- `message_delete` - Messages supprimés
- `message_edit` - Messages modifiés
- `ban` - Bannissements
- `unban` - Débannissements
- `role_add` - Attribution de rôles
- `role_remove` - Retrait de rôles
- `channel_create` - Création de salons
- `channel_delete` - Suppression de salons

#### `!logs disable`
Désactive les logs pour ce serveur.

### Messages de bienvenue

#### `!welcome setup <channel> <message>`
Configure les messages de bienvenue.
```
!welcome setup #general "Bienvenue {user} sur notre serveur !"
```

**Variables disponibles :**
- `{user}` - Mention de l'utilisateur
- `{username}` - Nom de l'utilisateur
- `{server}` - Nom du serveur
- `{member_count}` - Nombre de membres

#### `!welcome disable`
Désactive les messages de bienvenue.

## 🌐 Interface Web d'administration

### Accès à l'interface
1. Connectez-vous sur http://127.0.0.1:8080
2. Utilisez vos identifiants administrateur
3. Naviguez vers votre serveur

### Dashboard serveur

#### Statistiques disponibles
- **Membres** : Total, en ligne, nouveaux
- **Messages** : Par jour, par salon
- **Modération** : Actions récentes
- **Activité** : Graphiques d'utilisation

#### Actions rapides
- Voir les détails du serveur
- Gérer les rôles et permissions
- Consulter les logs en temps réel
- Exporter les données

### Gestion des membres

#### Recherche et filtres
- Recherche par nom ou ID
- Filtre par rôle
- Tri par date d'arrivée
- Statut en ligne/hors ligne

#### Actions en masse
- Attribution de rôles multiple
- Messages privés groupés
- Export des listes de membres
- Statistiques détaillées

### Système de logs

#### Consultation
- **Filtres** : Par type, date, utilisateur
- **Recherche** : Texte libre dans les événements
- **Export** : CSV, JSON
- **Graphiques** : Tendances d'activité

#### Types de logs
- **Modération** : Bans, kicks, warnings
- **Messages** : Suppressions, modifications
- **Membres** : Arrivées, départs, changements de rôles
- **Serveur** : Modifications de configuration

## 🔧 Outils d'administration avancés

### Commandes de diagnostic

#### `!info server`
Informations détaillées du serveur.

#### `!info user <user>`
Informations détaillées d'un utilisateur.
```
!info user @user#1234
```

#### `!stats server`
Statistiques d'activité du serveur.

### Gestion des autorisations

#### `!permissions check <user> [channel]`
Vérifie les permissions d'un utilisateur.
```
!permissions check @user#1234 #general
```

#### `!permissions role <role>`
Affiche les permissions d'un rôle.

### Maintenance

#### `!sync`
Synchronise les commandes slash (propriétaires uniquement).

#### `!reload modules`
Recharge les modules du bot (propriétaires uniquement).

## 📊 Rapports et analytics

### Rapports automatiques

#### Rapport hebdomadaire
- Nouveaux membres
- Messages postés
- Actions de modération
- Tendances d'activité

#### Alertes automatiques
- Pics d'activité inhabituelle
- Tentatives de spam
- Comportements suspects
- Erreurs système

### Export de données

#### Formats disponibles
- **CSV** : Compatible Excel
- **JSON** : Pour développeurs
- **PDF** : Rapports formatés

#### Données exportables
- Liste des membres
- Historique des messages
- Logs de modération
- Statistiques d'activité

## 🔒 Sécurité et bonnes pratiques

### Gestion des permissions

#### Principe du moindre privilège
- Donnez uniquement les permissions nécessaires
- Révisez régulièrement les rôles
- Limitez le nombre d'administrateurs

#### Hiérarchie des rôles
```
Bot → Propriétaires → Administrateurs → Modérateurs → Membres
```

### Surveillance

#### Points à surveiller
- **Activité inhabituelle** : Pics de messages, connexions
- **Actions de modération** : Fréquence, efficacité
- **Erreurs système** : Logs d'erreur, dysfonctionnements
- **Permissions** : Changements non autorisés

#### Alertes recommandées
- Bannissements multiples
- Suppressions de messages en masse
- Changements de permissions importantes
- Tentatives d'accès non autorisées

## 🆘 Dépannage pour administrateurs

### Problèmes courants

#### "Bot ne répond pas"
1. Vérifiez que le bot est en ligne
2. Contrôlez les permissions dans le salon
3. Testez avec une commande simple (`!ping`)
4. Contactez un propriétaire si nécessaire

#### "Commandes non fonctionnelles"
1. Vérifiez le préfixe du serveur (`!prefix`)
2. Confirmez les permissions du bot
3. Essayez les commandes slash (`/help`)

#### "Logs ne fonctionnent pas"
1. Vérifiez la configuration (`!logs status`)
2. Contrôlez les permissions du salon de logs
3. Reconfigurez si nécessaire (`!logs setup`)

### Restauration de configuration

#### Sauvegarde préventive
Exportez régulièrement :
- Configuration des rôles
- Paramètres de logs
- Listes de membres importantes

#### Restauration d'urgence
En cas de problème majeur :
1. Contactez immédiatement un propriétaire
2. Documentez le problème avec captures d'écran
3. Évitez les modifications supplémentaires
4. Utilisez l'interface web pour diagnostiquer

## 📋 Checklist administrateur

### Configuration initiale
- [ ] Rôles et permissions configurés
- [ ] Salon de logs créé et configuré
- [ ] Messages de bienvenue configurés
- [ ] Préfixe défini si nécessaire
- [ ] Tests des commandes de modération

### Maintenance régulière
- [ ] Vérification des logs (quotidien)
- [ ] Révision des rôles (hebdomadaire)
- [ ] Nettoyage des messages (si nécessaire)
- [ ] Mise à jour des configurations
- [ ] Formation des nouveaux modérateurs

### Sécurité
- [ ] Audit des permissions
- [ ] Surveillance des activités suspectes
- [ ] Vérification des alertes système
- [ ] Mise à jour des mots de passe
- [ ] Sauvegarde des configurations

## 📞 Support administrateur

### Ressources disponibles
- **Interface web** : Dashboard et logs
- **Documentation complète** : `/help` dans Discord
- **Support technique** : Ticket via interface web
- **Formation** : Guides dans l'interface web

### Contacts d'urgence
1. **Propriétaires** : Contact direct via Discord
2. **Support technique** : Ticket prioritaire
3. **Communauté** : Canal support du serveur

---

*Documentation Administrateurs v1.0 - Mise à jour : Juillet 2025*
