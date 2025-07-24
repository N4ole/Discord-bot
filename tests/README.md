# Tests du Bot Discord

Ce dossier contient tous les scripts de test pour le bot Discord.

## Scripts de test disponibles

### Tests des notifications
- `test_notifications.py` - Test des notifications Discord
- `test_notifier_direct.py` - Test direct du système de notification

### Tests du système de support
- `test_support.py` - Test du système de support
- `test_ticket_deletion.py` - Test de suppression des tickets
- `test_web_ticket.py` - Test des tickets via l'interface web

### Tests de l'interface web
- `test_owner_web.py` - Test de l'interface web des propriétaires
- `test_web_direct.py` - Test direct de l'interface web
- `test_user_fetch.py` - Test de récupération des utilisateurs Discord

### Tests d'administration
- `test_multi_admin.py` - Test de gestion multi-administrateurs
- `test_sequential_numbering.py` - Test de numérotation séquentielle

## Utilisation

Pour exécuter un test, utilisez :
```bash
python tests/nom_du_test.py
```

## Prérequis

Assurez-vous que votre environnement est configuré et que le bot est démarré avant d'exécuter les tests.
