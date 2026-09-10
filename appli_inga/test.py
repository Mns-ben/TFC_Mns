
# ================================================================
# TEST DE CONNEXION À LA BASE DE DONNÉES
# Utilisation : python test_connection.py
# ================================================================

import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'appli_inga.settings')
django.setup()

from django.db import connection
from apps.core.models import (
    Projet, EtapeProjet, Acteur, Evenement,
    ImpactActeur, ImpactEnvironnementalSocial,
    Document, Chronologie,
)


def afficher_titre(titre):
    """Affiche un titre encadré."""
    print("\n" + "=" * 60)
    print(f"  {titre}")
    print("=" * 60)


def tester_connexion():
    """Vérifie que Django est bien connecté à PostgreSQL."""
    afficher_titre("1. TEST DE CONNEXION")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print(f"✅ Connecté à PostgreSQL")
            print(f"   Version : {version[:60]}...")
    except Exception as e:
        print(f"❌ Erreur de connexion : {e}")
        return False
    
    # Informations de la base
    print(f"\n   Base de données : {connection.settings_dict['NAME']}")
    print(f"   Utilisateur     : {connection.settings_dict['USER']}")
    print(f"   Hôte            : {connection.settings_dict['HOST']}")
    print(f"   Port            : {connection.settings_dict['PORT']}")
    
    return True


def tester_tables():
    """Vérifie que les tables existent."""
    afficher_titre("2. TEST DES TABLES")
    
    tables_attendues = [
        'core_projet',
        'core_etapeprojet',
        'core_acteur',
        'core_evenement',
        'core_impactacteur',
        'core_impactenvironnementalsocial',
        'core_acteurevenement',
        'core_document',
        'core_chronologie',
        'core_utilisateur',
    ]
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables_existantes = [row[0] for row in cursor.fetchall()]
    
    print(f"Tables trouvées : {len(tables_existantes)}\n")
    
    for table in tables_attendues:
        if table in tables_existantes:
            print(f"   ✅ {table}")
        else:
            print(f"   ❌ {table} (MANQUANTE)")
    
    return len(tables_existantes) > 0


def tester_donnees():
    """Compte les données dans chaque table."""
    afficher_titre("3. TEST DES DONNÉES")
    
    compteurs = [
        ('Projets', Projet.objects.count()),
        ('Étapes', EtapeProjet.objects.count()),
        ('Acteurs', Acteur.objects.count()),
        ('Événements', Evenement.objects.count()),
        ('Impacts acteurs', ImpactActeur.objects.count()),
        ('Impacts environnementaux/sociaux', ImpactEnvironnementalSocial.objects.count()),
        ('Documents', Document.objects.count()),
        ('Chronologies', Chronologie.objects.count()),
    ]
    
    total = 0
    for nom, count in compteurs:
        statut = "✅" if count > 0 else "⚠️ "
        print(f"   {statut} {nom:<35} : {count}")
        total += count
    
    print(f"\n   TOTAL : {total} lignes")
    
    if total == 0:
        print("\n   ⚠️  ATTENTION : La base est vide !")
        print("   → Lance : python manage.py populate_data")
        return False
    
    return True


def afficher_echantillon():
    """Affiche un échantillon des données."""
    afficher_titre("4. ÉCHANTILLON DES DONNÉES")
    
    # Projet
    projet = Projet.objects.first()
    if projet:
        print(f"\n📌 PROJET PRINCIPAL")
        print(f"   Nom         : {projet.nom}")
        print(f"   Capacité    : {projet.capacite_prevue} MW")
        print(f"   Statut      : {projet.get_statut_actuel_display()}")
        print(f"   Localisation: {projet.localisation}")
    
    # Étapes
    print(f"\n📌 3 PREMIÈRES ÉTAPES")
    for etape in EtapeProjet.objects.all()[:3]:
        print(f"   - {etape.nom} ({etape.date_debut.year})")
    
    # Acteurs
    print(f"\n📌 3 PREMIERS ACTEURS")
    for acteur in Acteur.objects.all()[:3]:
        print(f"   - {acteur.nom} ({acteur.get_type_acteur_display()})")
    
    # Événements
    print(f"\n📌 3 PREMIERS ÉVÉNEMENTS")
    for ev in Evenement.objects.all()[:3]:
        print(f"   - {ev.titre} ({ev.date_evenement.year})")


def tester_requetes():
    """Teste quelques requêtes SQL typiques."""
    afficher_titre("5. TEST DES REQUÊTES SQL")
    
    # Requête 1 : Frise chronologique
    from django.db.models import Count
    from django.db.models.functions import ExtractYear
    
    print("\n📊 Événements par type :")
    types = Evenement.objects.values('type_evenement').annotate(
        nb=Count('id')
    ).order_by('-nb')
    
    for t in types:
        print(f"   - {t['type_evenement']:<20} : {t['nb']}")
    
    # Requête 2 : Acteurs les plus influents
    from django.db.models import Avg
    
    print("\n📊 Acteurs les plus influents :")
    acteurs = Acteur.objects.annotate(
        nb_impacts=Count('impacts'),
        importance_moy=Avg('impacts__importance')
    ).filter(nb_impacts__gt=0).order_by('-importance_moy')[:5]
    
    if acteurs:
        for a in acteurs:
            print(f"   - {a.nom:<30} : {a.nb_impacts} impacts (moy. {a.importance_moy:.1f})")
    else:
        print("   ⚠️ Aucun impact enregistré")


def main():
    """Fonction principale."""
    print("\n" + "🔍" * 30)
    print("   TEST DE CONNEXION - OBSERVATOIRE GRAND INGA")
    print("🔍" * 30)
    
    # Test 1 : Connexion
    if not tester_connexion():
        print("\n❌ Impossible de continuer : problème de connexion")
        return
    
    # Test 2 : Tables
    tester_tables()
    
    # Test 3 : Données
    donnees_ok = tester_donnees()
    
    # Test 4 : Échantillon
    if donnees_ok:
        afficher_echantillon()
        
        # Test 5 : Requêtes
        tester_requetes()
    
    # Résumé final
    afficher_titre("RÉSUMÉ")
    if donnees_ok:
        print("\n✅ Tout est OK !")
        print("   → Tu peux lancer : python manage.py runserver")
        print("   → Ouvre : http://127.0.0.1:8000/")
    else:
        print("\n⚠️  La connexion fonctionne, mais la base est VIDE.")
        print("   → Il faut peupler les données.")


if __name__ == '__main__':
    main()