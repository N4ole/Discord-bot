# Configuration de la Page Promo

## 🎯 Personnalisation du Lien d'Invitation

Pour que la page promo fonctionne correctement avec votre bot, vous devez modifier le lien d'invitation Discord.

### 📝 Étapes de Configuration

1. **Récupérez l'ID de votre bot** :
   - Allez sur le [Discord Developer Portal](https://discord.com/developers/applications)
   - Sélectionnez votre application/bot
   - Copiez l'ID de l'application (Client ID)

2. **Modifiez les liens dans `templates/promo.html`** :
   - Recherchez : `client_id=1397194777098981517`
   - Remplacez par : `client_id=VOTRE_BOT_CLIENT_ID`

3. **Personnalisez les permissions** (optionnel) :
   - Le lien actuel utilise `permissions=8` (Administrateur)
   - Vous pouvez générer un lien personnalisé sur le Developer Portal

### 🔗 Liens à Modifier

Dans le fichier `templates/promo.html`, modifiez ces URLs :

```html
<!-- Ligne ~71 et ~214 -->
https://discord.com/api/oauth2/authorize?client_id=VOTRE_BOT_CLIENT_ID&permissions=8&scope=bot%20applications.commands
```

### 🎨 Personnalisation Supplémentaire

#### Informations du Bot
- **Nom** : Changez "Summer Bot" par le nom de votre bot
- **Description** : Modifiez les descriptions selon vos fonctionnalités
- **Statistiques** : Ajustez les nombres (33+ commandes, etc.)

#### Liens Sociaux
- **Support Server** : Remplacez `https://discord.gg/your-support-server`
- **GitHub** : Modifiez le lien GitHub vers votre repository

#### Couleurs et Style
- **Couleurs principales** : Modifiez les gradients CSS
- **Avatar du bot** : Remplacez l'icône robot par votre logo

### 🚀 Accès à la Page

Une fois configurée, la page sera accessible à :
- **URL locale** : `http://127.0.0.1:8080/promo`
- **Production** : `https://votre-domaine.com/promo`

### 🔒 Sécurité

- La page promo est **publique** (pas d'authentification requise)
- Le panel admin reste protégé par login
- Aucune donnée sensible n'est exposée

### 📱 Fonctionnalités

- ✅ Design responsive (mobile + desktop)
- ✅ Animations au scroll
- ✅ Compteurs animés
- ✅ Navigation fluide
- ✅ SEO optimisé
- ✅ Boutons d'invitation Discord
- ✅ Lien vers le panel admin

### 🎯 Exemple de Personnalisation

```html
<!-- Changez ceci -->
<h1>Summer Bot</h1>
<p class="subtitle">Le Bot Discord Multi-Fonctionnel Ultime</p>

<!-- En ceci -->
<h1>Mon Super Bot</h1>
<p class="subtitle">Le Meilleur Bot Pour Votre Serveur</p>
```

---

**Note** : N'oubliez pas de redémarrer le serveur Flask après vos modifications !
