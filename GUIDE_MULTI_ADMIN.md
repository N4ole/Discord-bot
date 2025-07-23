# 🔔 Guide du Système de Notifications Multi-Admin

## 📋 Vue d'ensemble

Le système de notifications du Summer Bot permet maintenant d'envoyer des alertes à **plusieurs administrateurs** simultanément lorsqu'un nouveau ticket de support est créé ou qu'une réponse est ajoutée.

## 🎯 Réponse à votre question

> **"Si je voulais ajouter une personne pour recevoir les notifications du bot, où dois-je le mettre ?"**

**Réponse :** Dans le fichier `support_notifier.py`, ligne 10-11, vous devez modifier la liste `admin_user_ids`.

## 🔧 Configuration Actuelle

```python
# Dans support_notifier.py, ligne 10-11
admin_user_ids = [702923932239527978]  # naole77 uniquement
```

## ➕ Comment Ajouter un Nouvel Admin

### Étape 1 : Obtenir l'ID Discord
1. Activez le **mode développeur** dans Discord :
   - `Paramètres utilisateur` → `Avancé` → `Mode développeur` ✅
2. Faites un clic droit sur l'utilisateur → `Copier l'ID`
3. L'ID ressemble à : `123456789012345678` (18 chiffres)

### Étape 2 : Modifier le Code
Ouvrez `support_notifier.py` et modifiez la ligne 10-11 :

```python
# Avant (1 admin)
admin_user_ids = [702923932239527978]

# Après (2 admins)
admin_user_ids = [
    702923932239527978,  # naole77
    123456789012345678   # Nouvel admin
]

# Après (3 admins)
admin_user_ids = [
    702923932239527978,  # naole77
    123456789012345678,  # Admin 2  
    987654321098765432   # Admin 3
]
```

### Étape 3 : Redémarrer le Bot
```bash
# Arrêter le bot actuel (Ctrl+C)
# Puis relancer
python main.py
```

## 🔍 Comment ça Fonctionne

### Notifications de Nouveaux Tickets
Quand un utilisateur crée un ticket via `/support/new`, **tous les admins** dans la liste reçoivent :
- ✉️ Un message privé Discord
- 📋 Un embed avec les détails du ticket
- 🔗 Des liens vers le panel admin

### Notifications de Réponses
Quand une réponse est ajoutée à un ticket, **tous les admins** reçoivent :
- 💬 Une notification de nouvelle réponse
- 📋 Le contenu de la réponse
- 🔗 Des liens pour voir le ticket

## ✅ Avantages du Multi-Admin

1. **🔄 Redondance** : Si un admin n'est pas disponible
2. **⚡ Réactivité** : Plus de personnes peuvent répondre rapidement
3. **📊 Répartition** : Charge de travail partagée
4. **🔔 Alertes** : Aucun ticket ne passe inaperçu

## ⚠️ Prérequis

### Pour Chaque Nouvel Admin :
- ✅ Doit autoriser les MPs de membres du serveur
- ✅ Le bot doit pouvoir lui envoyer des MPs
- ✅ Doit avoir accès au panel admin (optionnel mais recommandé)

## 🧪 Test du Système

Pour tester si le système fonctionne :

```bash
python test_multi_admin.py
```

## 📊 Statistiques de Livraison

Le système affiche des logs détaillés :
```
📤 Envoi de notifications à 3 admin(s)...
✅ Notification envoyée à naole77 pour le ticket #123
✅ Notification envoyée à Admin2 pour le ticket #123
❌ Impossible d'envoyer un MP à l'utilisateur 987654321098765432
📊 Notifications envoyées: 2/3
```

## 🔧 Localisation Exacte

**Fichier :** `support_notifier.py`  
**Ligne :** 10-11  
**Variable :** `admin_user_ids`

```python
class SupportNotifier:
    def __init__(self):
        self.bot = None
        # 👇 MODIFIER ICI 👇
        self.admin_user_ids = [702923932239527978]  # ← Ajouter les IDs ici
        # 👆 MODIFIER ICI 👆
```

## 📝 Exemple Complet

```python
# Configuration pour une équipe de 4 admins
admin_user_ids = [
    702923932239527978,  # naole77 (Admin principal)
    111222333444555666,  # Alice (Admin technique)
    777888999000111222,  # Bob (Admin communauté) 
    333444555666777888   # Carol (Admin support)
]
```

## 🚀 Déploiement

1. Modifiez `support_notifier.py`
2. Redémarrez le bot
3. Testez en créant un ticket via `/support/new`
4. Vérifiez que tous les admins reçoivent la notification

---

**✨ Le système est maintenant prêt pour supporter plusieurs administrateurs !**
