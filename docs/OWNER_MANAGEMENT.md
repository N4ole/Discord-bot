# 👑 Documentation Propriétaires - Bot Discord

## 🔑 Rôle des propriétaires

Les propriétaires du bot ont un **accès complet** à toutes les fonctionnalités et peuvent :
- Gérer la liste des propriétaires
- Administrer tous les serveurs où le bot est présent
- Accéder à l'interface web complète
- Modifier les configurations globales
- Superviser le système de support

## 🎯 Gestion des propriétaires

### Configuration centralisée (`bot_owners.json`)

```json
{
  "description": "Liste des propriétaires du bot avec accès complet",
  "owners": [
    702923932239527978,
    854382745252790272
  ],
  "usage": "Ajoutez l'ID Discord des utilisateurs autorisés",
  "last_modified": "2025-07-24"
}
```
    "description": "Liste des propriétaires autorisés du bot Discord",
    "note": "Ajoutez les IDs Discord des propriétaires dans le tableau 'owners'"
}
```

## 🎯 Fonctionnalités

### Commandes Discord

| Commande | Description | Exemple |
|----------|-------------|---------|
| `!owner list` | Affiche la liste des propriétaires | `!owner list` |
| `!owner add <ID>` | Ajoute un propriétaire | `!owner add 123456789012345678` |
| `!owner remove <ID>` | Supprime un propriétaire | `!owner remove 123456789012345678` |
| `!owner check [ID]` | Vérifie si un utilisateur est propriétaire | `!owner check` |

### Interface Web

- **URL :** `http://127.0.0.1:8080/owner_management`
- **Fonctionnalités :**
  - Visualisation des propriétaires avec avatars
  - Ajout/suppression en temps réel
  - Vérifications de sécurité
  - API REST intégrée

### API REST

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/api/owners` | GET | Récupère la liste des propriétaires |
| `/api/owner/add` | POST | Ajoute un propriétaire |
| `/api/owner/remove` | POST | Supprime un propriétaire |

## 🔒 Sécurités

1. **Protection contre la suppression du dernier propriétaire**
2. **Vérification de l'existence des utilisateurs Discord**
3. **Cache intelligent avec rechargement automatique**
4. **Fallback sur OWNER_ID en cas d'erreur**
5. **Logs détaillés de toutes les modifications**

## 🚀 Utilisation

### Ajouter un propriétaire via Discord
```
!owner add 123456789012345678
```

### Ajouter un propriétaire via interface web
1. Se connecter à l'interface admin
2. Aller sur "👑 Propriétaires"
3. Saisir l'ID Discord dans le formulaire
4. Cliquer sur "Ajouter"

### Modification manuelle du fichier JSON
```json
{
    "owners": [
        702923932239527978,
        123456789012345678,
        987654321098765432
    ]
}
```

Le système détecte automatiquement les changements de fichier !

## 📝 Logs

Toutes les modifications sont enregistrées :
```
👑 OWNER ADD: Username (123456789012345678) ajouté par Admin (702923932239527978)
🗑️ OWNER REMOVE: Username (123456789012345678) supprimé par Admin (702923932239527978)
```

## 🔧 Commandes qui utilisent le système

- `!annonce` - Envoi d'annonces aux propriétaires de serveurs
- `!addperm` - Création de rôles administrateur
- `!remperm` - Suppression de rôles administrateur
- Et toutes les autres commandes avec vérification de propriétaire

## 🔄 Cache et Performance

- **Cache intelligent** : Rechargement uniquement si le fichier change
- **Performance** : Vérification O(1) grâce au cache en mémoire
- **Fiabilité** : Fallback automatique en cas d'erreur

## 🌍 Navigation Web

Le lien "👑 Propriétaires" est disponible dans toutes les pages d'administration :
- Dashboard
- Logs  
- Statistiques
- Contrôle
- Gestion des statuts

## ⚠️ Notes importantes

1. **IDs Discord** : Utilisez des IDs numériques Discord (17-19 chiffres)
2. **Permissions** : Seuls les propriétaires peuvent modifier la liste
3. **Sauvegarde** : Le fichier JSON est automatiquement sauvegardé
4. **Redémarrage** : Aucun redémarrage requis pour les modifications

## 📞 Support

En cas de problème :
1. Vérifiez les logs du bot
2. Vérifiez la syntaxe du fichier JSON
3. Utilisez `!owner check` pour tester
4. Consultez l'interface web pour le diagnostic
