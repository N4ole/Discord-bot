# Configuration du Bot Discord

Ce dossier contient tous les fichiers de configuration du bot.

## Fichiers de configuration

### Propriétaires et permissions
- `bot_owners.json` - Liste des propriétaires du bot
- `prefixes.json` - Préfixes personnalisés par serveur

### Logs et journalisation
- `logs_config.json` - Configuration des logs par serveur
- `logs_config.example.json` - Exemple de configuration des logs

### Autres
- `package.json` - Configuration Node.js (si utilisé)

## Important

⚠️ **Ces fichiers contiennent des informations sensibles !**

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
