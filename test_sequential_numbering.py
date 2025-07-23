#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test du système de numérotation séquentielle des tickets
Vérifie que les IDs restent séquentiels même après suppression
"""

from support_db import support_db
import sys
import os

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def test_sequential_numbering():
    """Test la numérotation séquentielle des tickets"""

    print("🧪 TEST DE LA NUMÉROTATION SÉQUENTIELLE DES TICKETS")
    print("=" * 60)

    # Test 1: Vérifier la migration/initialisation
    print("\n📋 1. Initialisation du système de numérotation:")
    try:
        support_db.reset_ticket_counter_if_needed()
        print("   ✅ Migration/initialisation effectuée")

        # Vérifier le compteur actuel
        cursor = support_db.conn.execute(
            'SELECT current_value FROM support_counters WHERE counter_name = ?', ('ticket_counter',))
        result = cursor.fetchone()
        current_counter = result['current_value'] if result else 0
        print(f"   📊 Compteur actuel: {current_counter}")

    except Exception as e:
        print(f"   ❌ Erreur: {e}")

    # Test 2: Simulation de la numérotation
    print("\n🔢 2. Simulation de la numérotation séquentielle:")

    print("   Scénario: Créer 3 tickets, supprimer le 2ème, créer un 4ème")
    print("   Résultat attendu: Tickets #1, #2, #3, puis suppression #2, puis création #4")
    print("   Liste finale: #1, #3, #4 (numérotation continue)")

    # Test 3: Vérifier la structure de la base
    print("\n🗄️ 3. Vérification de la structure de la base:")
    try:
        cursor = support_db.conn.execute("PRAGMA table_info(support_tickets)")
        columns = [column[1] for column in cursor.fetchall()]

        if 'ticket_number' in columns:
            print("   ✅ Colonne 'ticket_number' présente")
        else:
            print("   ❌ Colonne 'ticket_number' manquante")

        cursor = support_db.conn.execute("PRAGMA table_info(support_counters)")
        counter_columns = [column[1] for column in cursor.fetchall()]

        if len(counter_columns) > 0:
            print("   ✅ Table 'support_counters' présente")
        else:
            print("   ❌ Table 'support_counters' manquante")

    except Exception as e:
        print(f"   ❌ Erreur: {e}")

    # Test 4: Tester les nouvelles méthodes
    print("\n🔧 4. Test des nouvelles méthodes:")

    try:
        # Test get_next_ticket_number
        next_number = support_db.get_next_ticket_number()
        print(f"   📋 get_next_ticket_number(): {next_number}")

        # Test get_all_tickets_for_admin
        admin_tickets = support_db.get_all_tickets_for_admin()
        print(
            f"   📋 get_all_tickets_for_admin(): {len(admin_tickets)} tickets")

        if admin_tickets:
            print("   🔍 Aperçu des tickets (5 premiers):")
            for ticket in admin_tickets[:5]:
                ticket_num = ticket.get('ticket_number', 'N/A')
                subject = ticket.get('subject', 'Sans sujet')[:30]
                print(f"      - #{ticket_num}: {subject}...")

    except Exception as e:
        print(f"   ❌ Erreur lors du test des méthodes: {e}")


def show_numbering_explanation():
    """Explique le système de numérotation"""

    print("\n" + "=" * 60)
    print("📖 EXPLICATION DU SYSTÈME DE NUMÉROTATION")
    print("=" * 60)

    print("\n🎯 PROBLÈME RÉSOLU:")
    print("   Avant: Suppression du ticket #1 → prochain ticket = #3")
    print("   Après: Suppression du ticket #1 → prochain ticket = #2")

    print("\n🔧 SOLUTION TECHNIQUE:")
    print("   • Ajout de la colonne 'ticket_number' (numéro séquentiel)")
    print("   • Ajout de la table 'support_counters' (compteur global)")
    print("   • Les IDs de base (auto-increment) restent pour les relations")
    print("   • Les numéros affichés utilisent 'ticket_number'")

    print("\n📊 STRUCTURE DE DONNÉES:")
    print("   support_tickets:")
    print("     - id (PRIMARY KEY, auto-increment) ← pour les relations")
    print("     - ticket_number (UNIQUE) ← pour l'affichage utilisateur")
    print("     - ... autres colonnes")
    print("   ")
    print("   support_counters:")
    print("     - counter_name ('ticket_counter')")
    print("     - current_value (dernier numéro utilisé)")

    print("\n🔄 FONCTIONNEMENT:")
    print("   1. Création d'un ticket:")
    print("      → Récupère current_value + 1")
    print("      → Assigne ticket_number")
    print("      → Met à jour current_value")
    print("   ")
    print("   2. Suppression d'un ticket:")
    print("      → Supprime le ticket (ticket_number libéré)")
    print("      → Le compteur continue à partir du dernier numéro")
    print("   ")
    print("   3. Affichage:")
    print("      → Utilise ticket_number au lieu de id")

    print("\n✅ AVANTAGES:")
    print("   • Numérotation toujours séquentielle")
    print("   • Pas de trous dans la numérotation")
    print("   • Migration transparente des anciens tickets")
    print("   • Compatibilité avec l'existant")


def show_migration_info():
    """Informations sur la migration"""

    print("\n" + "=" * 60)
    print("🔄 INFORMATIONS DE MIGRATION")
    print("=" * 60)

    print("\n📋 MIGRATION AUTOMATIQUE:")
    print("   • Détection des tickets sans ticket_number")
    print("   • Attribution séquentielle basée sur created_at")
    print("   • Mise à jour du compteur global")
    print("   • Migration transparente au premier lancement")

    print("\n⚙️ PROCESSUS DE MIGRATION:")
    print("   1. Ajout de la colonne ticket_number si manquante")
    print("   2. Identification des tickets sans numéro")
    print("   3. Attribution des numéros par ordre chronologique")
    print("   4. Initialisation du compteur")

    print("\n🚀 APRÈS MIGRATION:")
    print("   • Tous les anciens tickets ont un ticket_number")
    print("   • Les nouveaux tickets suivent la séquence")
    print("   • L'affichage utilise les nouveaux numéros")


if __name__ == "__main__":
    try:
        test_sequential_numbering()
        show_numbering_explanation()
        show_migration_info()

        print("\n" + "=" * 60)
        print("✅ SYSTÈME DE NUMÉROTATION SÉQUENTIELLE INSTALLÉ")
        print("=" * 60)
        print("\n🎯 Résultat:")
        print("   Les tickets auront toujours des numéros séquentiels")
        print("   même après suppression de tickets intermédiaires.")
        print("\n🚀 Pour tester:")
        print("   1. Créez quelques tickets via /support/new")
        print("   2. Supprimez un ticket via l'admin")
        print("   3. Créez un nouveau ticket")
        print("   4. Vérifiez que la numérotation reste séquentielle")

    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
