# 🎫 Système de Support Summer Bot

## Vue d'ensemble

Le système de support de Summer Bot est une solution complète permettant aux utilisateurs de créer des comptes, soumettre des tickets de support, et recevoir de l'aide via une interface web moderne.

## Fonctionnalités Principales

### 🔐 Authentification Utilisateur
- **Inscription sécurisée** avec validation des données
- **Connexion** avec nom d'utilisateur ou email
- **Hachage des mots de passe** avec PBKDF2 et sel
- **Sessions sécurisées** avec option "Se souvenir de moi"
- **Intégration Discord optionnelle** (nom d'utilisateur et ID)

### 🎫 Gestion des Tickets
- **Création de tickets** avec catégorisation et priorités
- **Métadonnées avancées** (ID serveur, commande utilisée, message d'erreur)
- **Système de réponses** entre utilisateurs et administrateurs
- **Statuts multiples** : ouvert, en cours, en attente, résolu, fermé
- **Priorités configurables** : faible, moyenne, haute, urgente

### 🎨 Interface Utilisateur
- **Design moderne** avec thème Discord
- **Responsive** pour mobile et desktop
- **Navigation intuitive** avec tableaux de bord
- **Filtres et recherche** pour les tickets
- **Notifications en temps réel**
- **Auto-sauvegarde** des brouillons

## Architecture Technique

### 📊 Base de Données SQLite

#### Table `support_users`
```sql
- id (PRIMARY KEY)
- username (UNIQUE)
- email (UNIQUE) 
- password_hash
- salt
- discord_username
- discord_id
- created_at
```

#### Table `support_tickets`
```sql
- id (PRIMARY KEY)
- user_id (FOREIGN KEY)
- category
- priority
- subject
- description
- metadata (JSON)
- status
- created_at
- updated_at
- discord_notified
```

#### Table `ticket_responses`
```sql
- id (PRIMARY KEY)
- ticket_id (FOREIGN KEY)
- message
- is_admin (BOOLEAN)
- created_at
```

### 🌐 Routes Web

#### Routes Publiques (sans authentification admin)
- `GET /support` - Page d'accueil du support
- `GET|POST /support/register` - Inscription utilisateur
- `GET|POST /support/login` - Connexion utilisateur
- `GET /support/logout` - Déconnexion
- `GET /support/dashboard` - Tableau de bord utilisateur
- `GET|POST /support/ticket/new` - Création de ticket
- `GET /support/ticket/<id>` - Vue détaillée d'un ticket
- `GET /support/tickets` - Liste des tickets utilisateur
- `POST /support/ticket/<id>/respond` - Réponse à un ticket

## Utilisation

### 🚀 Démarrage

1. **Installer les dépendances** (si pas déjà fait)
   ```bash
   pip install flask sqlite3 hashlib secrets
   ```

2. **Lancer le serveur web**
   ```bash
   python web_panel.py
   ```

3. **Accéder au support**
   - Page d'accueil : `http://127.0.0.1:8080/support`
   - Page promotionnelle : `http://127.0.0.1:8080/promo`

### 👤 Workflow Utilisateur

1. **Inscription** : `/support/register`
   - Nom d'utilisateur unique
   - Adresse email valide
   - Mot de passe sécurisé (min. 6 caractères)
   - Informations Discord optionnelles

2. **Connexion** : `/support/login`
   - Username ou email + mot de passe
   - Option "Se souvenir de moi"

3. **Création de ticket** : `/support/ticket/new`
   - Catégorie du problème
   - Niveau de priorité
   - Description détaillée
   - Informations techniques (serveur, commande, erreur)
   - Pièces jointes (prévu pour futur développement)

4. **Suivi** : `/support/dashboard` ou `/support/tickets`
   - Vue d'ensemble des tickets
   - Filtres par statut, priorité, catégorie
   - Recherche dans les titres
   - Notifications de nouvelles réponses

### 🛠️ Administration

Les fonctionnalités d'administration seront développées dans une prochaine phase et incluront :
- Dashboard admin pour voir tous les tickets
- Système de réponse aux tickets
- Notifications Discord automatiques
- Statistiques avancées
- Gestion des utilisateurs

## Tests et Validation

### 🧪 Test du Système
```bash
python test_support.py
```

Ce script teste :
- Création et authentification d'utilisateurs
- Création et récupération de tickets
- Système de réponses
- Mise à jour des statuts
- Récupération des statistiques

### ✅ Validation de Sécurité

- **Mots de passe** : Hachage PBKDF2 avec sel aléatoire
- **Sessions** : Identifiants uniques et chiffrés
- **Validation** : Côté client et serveur
- **Accès** : Contrôle strict des permissions utilisateur
- **SQL Injection** : Protection via requêtes préparées

## Configuration

### 🔧 Variables d'environnement
```python
# Dans web_panel.py
FLASK_SECRET_KEY = 'your-super-secret-key-here'  # À changer en production
```

### 📧 Notifications Discord (À développer)
```python
# Configuration future pour les notifications
DISCORD_ADMIN_USER_ID = "your-discord-user-id"
DISCORD_SUPPORT_CHANNEL_ID = "support-channel-id"
```

## Intégration avec le Bot Discord

### 🤖 Notifications Automatiques
Le système est conçu pour s'intégrer avec le bot Discord et envoyer des notifications automatiques :

1. **Nouveau ticket** → Message privé à l'administrateur
2. **Réponse utilisateur** → Notification dans le canal support
3. **Ticket résolu** → Confirmation à l'utilisateur

### 📨 Commandes Support (À développer)
```python
# Commandes slash prévues
/support_stats    # Statistiques des tickets
/support_user     # Informations utilisateur
/support_respond  # Répondre directement depuis Discord
```

## Structure des Fichiers

```
Discord-bot/
├── support_db.py           # Gestion base de données
├── web_panel.py           # Routes Flask (modifié)
├── test_support.py        # Tests du système
├── templates/
│   ├── support_base.html          # Template de base
│   ├── support_home.html          # Page d'accueil
│   ├── support_register.html      # Inscription
│   ├── support_login.html         # Connexion
│   ├── support_dashboard.html     # Tableau de bord
│   ├── support_ticket_new.html    # Nouveau ticket
│   ├── support_ticket_view.html   # Vue ticket
│   └── support_tickets.html       # Liste tickets
└── static/
    └── logo-bot.jpg       # Logo intégré
```

## Évolutions Futures

### 🚀 Phase 2 - Administration
- Dashboard administrateur complet
- Système de notifications Discord
- Gestion en masse des tickets
- Templates de réponses

### 🚀 Phase 3 - Avancées
- Upload de fichiers/screenshots
- Système de tags personnalisés
- Escalade automatique des tickets urgents
- Intégration complète avec les commandes bot
- API REST pour développeurs tiers

### 🚀 Phase 4 - Intelligence
- Suggestions automatiques de solutions
- Analyse sentiment des tickets
- Détection automatique de problèmes récurrents
- Chatbot d'assistance première ligne

## Maintenance et Monitoring

### 📊 Logs et Debug
- Tous les événements sont loggés via le système existant
- Erreurs tracées avec contexte utilisateur
- Statistiques d'utilisation automatiques

### 🔄 Sauvegardes
- Base SQLite automatiquement sauvegardée
- Export JSON des données disponible
- Restauration rapide en cas de problème

---

**Développé avec ❤️ pour la communauté Summer Bot**
*Système de support v1.0 - Janvier 2025*
