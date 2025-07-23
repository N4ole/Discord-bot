# 📱 Système de Notifications Discord - Documentation

## Vue d'ensemble

Le système de support Summer Bot inclut un système de notifications Discord automatiques qui envoie des messages privés à l'administrateur (naole77) chaque fois qu'un nouveau ticket de support est créé ou qu'une réponse est ajoutée.

## Configuration

### 🔧 ID Utilisateur Discord
- **Utilisateur cible** : naole77
- **ID Discord** : `702923932239527978`
- **Localisation du paramètre** : `support_notifier.py` ligne 13

### 📋 Types de notifications

#### 1. Nouveau Ticket de Support
Envoyé automatiquement quand un utilisateur crée un nouveau ticket via l'interface web.

**Contenu de la notification :**
- 📋 Sujet du ticket
- 👤 Nom d'utilisateur et email
- 🏷️ Catégorie (bug, question, suggestion, etc.)
- ⚡ Priorité (low, medium, high, urgent)
- 🆔 ID du ticket
- 📝 Description complète
- 🔗 Liens directs vers le panel admin

#### 2. Nouvelle Réponse à un Ticket
Envoyé quand un utilisateur ajoute une réponse à un ticket existant.

**Contenu de la notification :**
- 📋 Sujet du ticket original
- 👤 Utilisateur qui a répondu
- 🆔 ID du ticket
- 💬 Contenu de la nouvelle réponse
- 🔗 Lien direct vers le ticket

## 🔧 Architecture Technique

### Fichiers impliqués
1. `support_notifier.py` - Module principal des notifications
2. `support_db.py` - Intégration avec la base de données
3. `web_panel.py` - Initialisation du système
4. `main.py` - Configuration au démarrage du bot

### Flux de fonctionnement
```
Ticket créé → support_db.py → support_notifier.py → Discord API → MP à naole77
```

### Gestion asynchrone
- Les notifications utilisent des threads séparés pour ne pas bloquer l'interface web
- Gestion d'erreur robuste en cas d'échec d'envoi
- Logs détaillés pour le debugging

## 🎨 Format des Messages

### Embed Discord
- **Couleur** : Rouge-orange (#ff6b6b) pour nouveaux tickets, Bleu (#667eea) pour réponses
- **Timestamp** : Date/heure de création automatique
- **Footer** : Logo Summer Bot et nom du système
- **Champs structurés** : Informations organisées et lisibles

### Exemple de notification
```
🎫 Nouveau Ticket de Support
Un nouveau ticket a été créé sur le système de support Summer Bot

📋 Sujet: Problème avec la commande /help
👤 Utilisateur: testuser
📧 Email: user@example.com
🏷️ Catégorie: bug
⚡ Priorité: HIGH
🆔 ID du Ticket: #123

📝 Description:
La commande /help ne fonctionne pas correctement...

🔗 Actions:
[Voir le ticket dans le panel admin]
[Centre de support]
```

## 🛠️ Configuration Avancée

### Changer l'utilisateur de notification
Modifiez la ligne 13 dans `support_notifier.py` :
```python
self.admin_user_id = 702923932239527978  # Remplacez par le nouvel ID
```

### Ajouter plusieurs destinataires
```python
self.admin_user_ids = [
    702923932239527978,  # naole77
    123456789012345678   # Autre admin
]
```

### Personnaliser les messages
Modifiez les fonctions `send_new_ticket_notification` et `send_new_response_notification` dans `support_notifier.py`.

## 🧪 Tests

### Test manuel
```bash
python test_notifications.py
```

### Test via interface web
1. Accédez à `http://127.0.0.1:8080/support`
2. Créez un compte de test
3. Soumettez un nouveau ticket
4. Vérifiez la réception du MP Discord

## 🚨 Dépannage

### Problèmes courants

#### 1. Notification non reçue
- Vérifiez que le bot Discord est en ligne
- Confirmez l'ID utilisateur Discord (702923932239527978)
- Vérifiez les logs de la console pour les erreurs

#### 2. Erreur "Forbidden"
- L'utilisateur a peut-être bloqué les MPs de bots
- Vérifiez les paramètres de confidentialité Discord

#### 3. Erreur "User not found"
- Vérifiez que l'ID utilisateur est correct
- Assurez-vous que l'utilisateur partage au moins un serveur avec le bot

### Logs de debugging
```
✅ Notification envoyée à naole77 pour le ticket #123
📱 Thread de notification démarré pour le ticket #123
⚠️ Module de notification Discord non disponible
❌ Erreur lors de l'envoi de la notification: [détails]
```

## 🔮 Évolutions Futures

### Fonctionnalités prévues
- [ ] Notifications de changement de statut
- [ ] Rappels pour tickets non traités
- [ ] Notifications par webhook Discord
- [ ] Interface d'administration des notifications
- [ ] Notifications par email en complément

### Optimisations
- [ ] Cache des utilisateurs Discord
- [ ] Limitation du taux d'envoi
- [ ] Templates de messages personnalisables
- [ ] Statistiques d'envoi

---

**Note** : Ce système nécessite que le bot Summer Bot soit en ligne et connecté à Discord pour fonctionner. Les notifications sont envoyées uniquement si l'instance du bot est correctement initialisée.
