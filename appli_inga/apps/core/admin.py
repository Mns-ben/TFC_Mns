# ================================================================
# INTERFACE D'ADMINISTRATION DJANGO
# Application : core
# Fichier : admin.py
# ================================================================

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    Acteur,
    ActeurEvenement,
    Chronologie,
    Document,
    EtapeProjet,
    Evenement,
    ImpactActeur,
    ImpactEnvironnementalSocial,
    Projet,
    Utilisateur,
)


# ================================================================
# 1. ADMIN : UTILISATEUR
# ================================================================
@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    """
    Administration du modèle Utilisateur personnalisé.
    Hérite de UserAdmin pour garder les fonctionnalités de base.
    """
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'institution', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'institution')
    ordering = ('username',)

    fieldsets = UserAdmin.fieldsets + (
        ('Informations complémentaires', {
            'fields': ('role', 'institution', 'bio', 'date_creation')
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations complémentaires', {
            'fields': ('role', 'institution', 'email')
        }),
    )


# ================================================================
# 2. ADMIN : PROJET
# ================================================================
@admin.register(Projet)
class ProjetAdmin(admin.ModelAdmin):
    """
    Administration du modèle Projet.
    """
    list_display = (
        'nom', 'statut_actuel', 'capacite_prevue',
        'localisation', 'maitre_ouvrage', 'date_debut_projet'
    )
    list_filter = ('statut_actuel', 'type_turbines', 'maitre_ouvrage')
    search_fields = ('nom', 'description', 'localisation', 'maitre_ouvrage')
    ordering = ('nom',)

    fieldsets = (
        ('Informations générales', {
            'fields': ('nom', 'description', 'statut_actuel')
        }),
        ('Caractéristiques techniques', {
            'fields': (
                'capacite_prevue', 'hauteur_chute',
                'nombre_turbines', 'type_turbines'
            )
        }),
        ('Localisation', {
            'fields': ('localisation', 'coordonnees_gps')
        }),
        ('Gestion et financement', {
            'fields': (
                'maitre_ouvrage', 'investissement_estime',
                'date_debut_projet', 'date_fin_prevue'
            )
        }),
    )


# ================================================================
# 3. ADMIN : ETAPE_PROJET
# ================================================================
@admin.register(EtapeProjet)
class EtapeProjetAdmin(admin.ModelAdmin):
    """
    Administration du modèle EtapeProjet.
    """
    list_display = (
        'nom', 'projet', 'date_debut', 'date_fin',
        'statut', 'responsable_etape'
    )
    list_filter = ('statut', 'projet', 'date_debut')
    search_fields = ('nom', 'description', 'responsable_etape')
    ordering = ('date_debut',)
    date_hierarchy = 'date_debut'

    fieldsets = (
        ('Informations générales', {
            'fields': ('nom', 'description', 'projet')
        }),
        ('Période', {
            'fields': ('date_debut', 'date_fin', 'statut')
        }),
        ('Détails', {
            'fields': ('objectifs', 'resultats', 'responsable_etape')
        }),
    )


# ================================================================
# 4. ADMIN : ACTEUR
# ================================================================
@admin.register(Acteur)
class ActeurAdmin(admin.ModelAdmin):
    """
    Administration du modèle Acteur.
    """
    list_display = (
        'nom', 'type_acteur', 'categorie',
        'pays', 'date_creation', 'date_disparition'
    )
    list_filter = ('type_acteur', 'categorie', 'pays')
    search_fields = ('nom', 'description', 'pays')
    ordering = ('nom',)

    fieldsets = (
        ('Informations générales', {
            'fields': ('nom', 'type_acteur', 'categorie', 'pays')
        }),
        ('Détails', {
            'fields': ('description', 'site_web')
        }),
        ('Dates', {
            'fields': ('date_creation', 'date_disparition')
        }),
    )


# ================================================================
# 5. ADMIN : IMPACT_ACTEUR
# ================================================================
@admin.register(ImpactActeur)
class ImpactActeurAdmin(admin.ModelAdmin):
    """
    Administration du modèle ImpactActeur.
    """
    list_display = (
        'acteur', 'type_impact', 'importance',
        'date_impact', 'etape'
    )
    list_filter = ('type_impact', 'importance', 'acteur', 'etape')
    search_fields = ('acteur__nom', 'description', 'consequences')
    ordering = ('-importance', 'date_impact')
    date_hierarchy = 'date_impact'

    fieldsets = (
        ('Informations générales', {
            'fields': ('acteur', 'etape', 'type_impact', 'importance')
        }),
        ('Détails', {
            'fields': ('description', 'consequences', 'date_impact')
        }),
    )


# ================================================================
# 6. ADMIN : IMPACT_ENVIRONNEMENTAL_SOCIAL
# ================================================================
@admin.register(ImpactEnvironnementalSocial)
class ImpactEnvironnementalSocialAdmin(admin.ModelAdmin):
    """
    Administration du modèle ImpactEnvironnementalSocial.
    """
    list_display = (
        'get_type_impact_display', 'projet', 'importance',
        'surface_ennoyee', 'population_deplacee', 'date_impact'
    )
    list_filter = ('type_impact', 'importance', 'projet')
    search_fields = ('description',)
    ordering = ('-importance', 'date_impact')
    date_hierarchy = 'date_impact'

    fieldsets = (
        ('Informations générales', {
            'fields': ('projet', 'etape', 'type_impact', 'importance', 'date_impact')
        }),
        ('Indicateurs environnementaux', {
            'fields': ('surface_ennoyee', 'volume_reservoir', 'bilan_carbone')
        }),
        ('Indicateurs sociaux', {
            'fields': ('population_deplacee',)
        }),
        ('Description', {
            'fields': ('description',)
        }),
    )


# ================================================================
# 7. ADMIN : ACTEUR_EVENEMENT (table de liaison)
# ================================================================
@admin.register(ActeurEvenement)
class ActeurEvenementAdmin(admin.ModelAdmin):
    """
    Administration de la table de liaison Acteur-Evenement.
    """
    list_display = ('acteur', 'evenement', 'role')
    list_filter = ('role', 'acteur', 'evenement')
    search_fields = ('acteur__nom', 'evenement__titre')
    ordering = ('acteur', 'evenement')

    fieldsets = (
        ('Liaison', {
            'fields': ('acteur', 'evenement', 'role')
        }),
    )


# ================================================================
# 8. ADMIN : INLINE pour Evenement ↔ Acteur
# ================================================================
class ActeurEvenementInline(admin.TabularInline):
    """
    Inline pour gérer les acteurs d'un événement.
    Nécessaire car la relation M2M utilise through='ActeurEvenement'.
    """
    model = ActeurEvenement
    extra = 1
    autocomplete_fields = ['acteur']
    verbose_name = "Acteur impliqué"
    verbose_name_plural = "Acteurs impliqués"


# ================================================================
# 9. ADMIN : EVENEMENT
# ================================================================
@admin.register(Evenement)
class EvenementAdmin(admin.ModelAdmin):
    """
    Administration du modèle Evenement.
    """
    list_display = (
        'titre', 'date_evenement', 'type_evenement',
        'importance', 'projet', 'localisation'
    )
    list_filter = ('type_evenement', 'importance', 'projet')
    search_fields = ('titre', 'description', 'source', 'localisation')
    ordering = ('-date_evenement',)
    date_hierarchy = 'date_evenement'

    # ✅ Utilisation d'un inline au lieu de filter_horizontal
    inlines = [ActeurEvenementInline]

    fieldsets = (
        ('Informations générales', {
            'fields': ('titre', 'description', 'projet')
        }),
        ('Classification', {
            'fields': ('type_evenement', 'importance', 'date_evenement')
        }),
        ('Sources et localisation', {
            'fields': ('source', 'localisation')
        }),
        # ⚠️ On retire 'acteurs' de fieldsets : géré par l'inline
    )


# ================================================================
# 10. ADMIN : DOCUMENT
# ================================================================
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """
    Administration du modèle Document.
    """
    list_display = (
        'titre', 'type_document', 'auteur',
        'date_publication', 'etat_conservation', 'projet'
    )
    list_filter = ('type_document', 'etat_conservation', 'projet')
    search_fields = ('titre', 'auteur', 'resume', 'mots_cles')
    ordering = ('-date_publication',)
    date_hierarchy = 'date_publication'

    fieldsets = (
        ('Informations générales', {
            'fields': ('titre', 'type_document', 'projet', 'auteur')
        }),
        ('Publication', {
            'fields': ('date_publication', 'etat_conservation')
        }),
        ('Contenu', {
            'fields': ('resume', 'mots_cles')
        }),
        ('Fichiers et liens', {
            'fields': ('url', 'fichier')
        }),
    )


# ================================================================
# 11. ADMIN : CHRONOLOGIE
# ================================================================
@admin.register(Chronologie)
class ChronologieAdmin(admin.ModelAdmin):
    """
    Administration du modèle Chronologie.
    """
    list_display = (
        'description_courte', 'date_debut', 'date_fin',
        'type_entree', 'date_mise_service', 'duree_vie'
    )
    list_filter = ('type_entree', 'date_debut')
    search_fields = ('description',)
    ordering = ('date_debut',)
    date_hierarchy = 'date_debut'

    fieldsets = (
        ('Période', {
            'fields': ('date_debut', 'date_fin', 'type_entree')
        }),
        ('Description', {
            'fields': ('description',)
        }),
        ('Jalons importants', {
            'fields': ('date_lancement_travaux', 'date_mise_service', 'duree_vie')
        }),
    )

    def description_courte(self, obj):
        """Affiche une description tronquée pour la liste."""
        if len(obj.description) > 60:
            return obj.description[:60] + "..."
        return obj.description
    description_courte.short_description = "Description"


# ================================================================
# CONFIGURATION GLOBALE DE L'ADMINISTRATION
# ================================================================

admin.site.site_header = "Observatoire Grand Inga - Administration"
admin.site.site_title = "Observatoire Grand Inga"
admin.site.index_title = "Tableau de bord administrateur"