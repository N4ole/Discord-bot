# ⚙️ Configuration du Bot Discord

Ce dossier contient tous les fichiers de configuration du bot en format JSON.

## 📁 Fichiers de configuration

### 👑 Propriétaires et permissions

- **`bot_owners.json`** - Liste des propriétaires du bot avec leurs permissions
- **`prefixes.json`** - Préfixes personnalisés par serveur Discord

### 📝 Logs et journalisation

- **`logs_config.json`** - Configuration des logs par serveur
- **`logs_config.example.json`** - Exemple de configuration des logs

## ⚠️ Sécurité importante

**Ces fichiers contiennent des informations sensibles !**

- Ne jamais partager le contenu de `bot_owners.json`
- Sauvegarder régulièrement ces configurations
- Vérifier les permissions avant d'ajouter de nouveaux propriétaires

## 🔧 Utilisation

Ces fichiers sont automatiquement lus et mis à jour par le bot lors de son fonctionnement. Aucune intervention manuelle n'est généralement nécessaire.

- Ne partagez jamais le contenu de ces fichiers
- Vérifiez que ces fichiers sont dans votre `.gitignore`
- Faites des sauvegardes régulières

## Structure des fichiers

### bot_owners.json
```json
[
  123456789012345678,
  987654321098765432
]
```

### prefixes.json
```json
{
  "123456789012345678": "!",
  "987654321098765432": "?"
}
```

### logs_config.json
Voir `logs_config.example.json` pour un exemple de structure.
