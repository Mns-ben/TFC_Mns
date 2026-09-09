# ================================================================
# MODÈLES DJANGO - OBSERVATOIRE HISTORIQUE DU PROJET GRAND INGA
# Application : core
# Fichier : models.py
# ================================================================

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from typing import ClassVar


# ================================================================
# 1. MODÈLE UTILISATEUR PERSONNALISÉ
# ================================================================
class Utilisateur(AbstractUser):
    """
    Modèle utilisateur personnalisé.
    Étend AbstractUser pour ajouter le rôle et d'autres champs.
    """
    ROLE_CHOICES: ClassVar[list[tuple[str, str]]] = [
        ('administrateur', 'Administrateur'),
        ('chercheur', 'Chercheur / Analyste'),
        ('decideur', 'Décideur'),
        ('public', 'Public / Visiteur'),
    ]
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='public',
        verbose_name="Rôle"
    )
    date_creation = models.DateField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name="Biographie"
    )
    institution = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Institution"
    )
    
    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ['username']
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


# ================================================================
# 2. MODÈLE PROJET
# ================================================================
class Projet(models.Model):
    """
    Représente le projet Grand Inga dans sa globalité.
    """
    STATUT_CHOICES: ClassVar[list[tuple[str, str]]] = [
        ('etude', 'En étude'),
        ('planification', 'En planification'),
        ('suspendu', 'Suspendu'),
        ('en_cours', 'En cours'),
        ('acheve', 'Achevé'),
    ]
    
    TYPE_TURBINE_CHOICES: ClassVar[list[tuple[str, str]]] = [
        ('francis', 'Francis'),
        ('kaplan', 'Kaplan'),
        ('pelton', 'Pelton'),
        ('autre', 'Autre'),
    ]
    
    nom = models.CharField(max_length=100, verbose_name="Nom du projet")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    capacite_prevue = models.DecimalField(
        max_digits=15, decimal_places=2,
        blank=True, null=True,
        verbose_name="Capacité prévue (MW)"
    )
    investissement_estime = models.DecimalField(
        max_digits=20, decimal_places=2,
        blank=True, null=True,
        verbose_name="Investissement estimé (USD)"
    )
    statut_actuel = models.CharField(
        max_length=50, choices=STATUT_CHOICES,
        default='en_cours',
        verbose_name="Statut actuel"
    )
    date_debut_projet = models.DateField(
        blank=True, null=True,
        verbose_name="Date de début du projet"
    )
    date_fin_prevue = models.DateField(
        blank=True, null=True,
        verbose_name="Date de fin prévue"
    )
    localisation = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name="Localisation"
    )
    coordonnees_gps = models.CharField(
        max_length=50, blank=True, null=True,
        verbose_name="Coordonnées GPS"
    )
    maitre_ouvrage = models.CharField(
        max_length=200, blank=True, null=True,
        verbose_name="Maître d'ouvrage"
    )
    hauteur_chute = models.DecimalField(
        max_digits=10, decimal_places=2,
        blank=True, null=True,
        verbose_name="Hauteur de chute (m)"
    )
    nombre_turbines = models.IntegerField(
        blank=True, null=True,
        verbose_name="Nombre de turbines"
    )
    type_turbines = models.CharField(
        max_length=100, choices=TYPE_TURBINE_CHOICES,
        blank=True, null=True,
        verbose_name="Type de turbines"
    )
    
    class Meta:
        verbose_name = "Projet"
        verbose_name_plural = "Projets"
        ordering = ['nom']
    
    def __str__(self):
        return self.nom


# ================================================================
# 3. MODÈLE ETAPE_PROJET
# ================================================================
class EtapeProjet(models.Model):
    """
    Étapes historiques du projet (études, constructions, décisions).
    """
    STATUT_CHOICES: ClassVar[list[tuple[str, str]]] = [
        ('achevee', 'Achevée'),
        ('en_cours', 'En cours'),
        ('reportee', 'Reportée'),
        ('annulee', 'Annulée'),
    ]
    
    nom = models.CharField(max_length=100, verbose_name="Nom de l'étape")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    date_debut = models.DateField(verbose_name="Date de début")
    date_fin = models.DateField(blank=True, null=True, verbose_name="Date de fin")
    statut = models.CharField(
        max_length=50, choices=STATUT_CHOICES,
        default='en_cours',
        verbose_name="Statut"
    )
    objectifs = models.TextField(blank=True, null=True, verbose_name="Objectifs")
    resultats = models.TextField(blank=True, null=True, verbose_name="Résultats")
    responsable_etape = models.CharField(
        max_length=200, blank=True, null=True,
        verbose_name="Responsable de l'étape"
    )
    projet = models.ForeignKey(
        Projet,
        on_delete=models.CASCADE,
        related_name='etapes',
        verbose_name="Projet"
    )
    
    class Meta:
        verbose_name = "Étape du projet"
        verbose_name_plural = "Étapes du projet"
        ordering = ['date_debut']
    
    def __str__(self):
        return f"{self.nom} ({self.date_debut.year})"
    
    def get_duree(self):
        """Calcule la durée de l'étape en années."""
        if self.date_fin:
            return self.date_fin.year - self.date_debut.year
        return None


# ================================================================
# 4. MODÈLE ACTEUR
# ================================================================
class Acteur(models.Model):
    """
    Acteurs (personnes morales) impliqués dans le projet.
    """
    TYPE_CHOICES: ClassVar[list[tuple[str, str]]] = [
        ('gouvernement', 'Gouvernement'),
        ('entreprise_publique', 'Entreprise publique'),
        ('entreprise_privee', 'Entreprise privée'),
        ('institution_financiere', 'Institution financière'),
        ('ong', 'ONG'),
        ('organisation_internationale', 'Organisation internationale'),
        ('personnalite_politique', 'Personnalité politique'),
        ('universite', 'Université / Centre de recherche'),
    ]
    
    CATEGORIE_CHOICES: ClassVar[list[tuple[str, str]]] = [
        ('personne_morale', 'Personne morale'),
        ('personne_physique', 'Personne physique'),
    ]
    
    nom = models.CharField(max_length=100, verbose_name="Nom de l'acteur")
    type_acteur = models.CharField(
        max_length=50, choices=TYPE_CHOICES,
        verbose_name="Type d'acteur"
    )
    categorie = models.CharField(
        max_length=50, choices=CATEGORIE_CHOICES,
        default='personne_morale',
        verbose_name="Catégorie"
    )
    pays = models.CharField(
        max_length=100, blank=True, null=True,
        verbose_name="Pays"
    )
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    site_web = models.URLField(
        max_length=255, blank=True, null=True,
        verbose_name="Site web"
    )
    date_creation = models.DateField(
        blank=True, null=True,
        verbose_name="Date de création"
    )
    date_disparition = models.DateField(
        blank=True, null=True,
        verbose_name="Date de disparition"
    )
    
    class Meta:
        verbose_name = "Acteur"
        verbose_name_plural = "Acteurs"
        ordering = ['nom']
    
    def __str__(self):
        return self.nom


# ================================================================
# 5. MODÈLE IMPACT_ACTEUR
# ================================================================
class ImpactActeur(models.Model):
    """
    Impact spécifique d'un acteur sur le projet.
    """
    TYPE_IMPACT_CHOICES: ClassVar[list[tuple[str, str]]] = [
        ('positif', 'Positif'),
        ('negatif', 'Négatif'),
        ('neutre', 'Neutre'),
        ('decisif', 'Décisif'),
        ('bloquant', 'Bloquant'),
        ('facilitateur', 'Facilitateur'),
    ]
    
    type_impact = models.CharField(
        max_length=50, choices=TYPE_IMPACT_CHOICES,
        verbose_name="Type d'impact"
    )
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    date_impact = models.DateField(blank=True, null=True, verbose_name="Date de l'impact")
    importance = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Importance (1-5)"
    )
    consequences = models.TextField(blank=True, null=True, verbose_name="Conséquences")
    acteur = models.ForeignKey(
        Acteur,
        on_delete=models.CASCADE,
        related_name='impacts',
        verbose_name="Acteur"
    )
    etape = models.ForeignKey(
        EtapeProjet,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='impacts_acteurs',
        verbose_name="Étape concernée"
    )
    
    class Meta:
        verbose_name = "Impact d'acteur"
        verbose_name_plural = "Impacts des acteurs"
        ordering = ['-importance', 'date_impact']
    
    def __str__(self):
        return f"{self.acteur.nom} - {self.get_type_impact_display()}"
    
    def est_critique(self):
        """Vérifie si l'impact est critique (importance >= 4)."""
        return self.importance >= 4


# ================================================================
# 6. MODÈLE IMPACT_ENVIRONNEMENTAL_SOCIAL
# ================================================================
class ImpactEnvironnementalSocial(models.Model):
    """
    Impacts environnementaux et sociaux du projet.
    """
    TYPE_IMPACT_CHOICES: ClassVar[list[tuple[str, str]]] = [
        ('environnemental', 'Environnemental'),
        ('social', 'Social'),
        ('economique', 'Économique'),
    ]
    
    type_impact = models.CharField(
        max_length=50, choices=TYPE_IMPACT_CHOICES,
        verbose_name="Type d'impact"
    )
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    date_impact = models.DateField(blank=True, null=True, verbose_name="Date de l'impact")
    surface_ennoyee = models.DecimalField(
        max_digits=15, decimal_places=2,
        blank=True, null=True,
        verbose_name="Surface ennoyée (km²)"
    )
    volume_reservoir = models.DecimalField(
        max_digits=15, decimal_places=2,
        blank=True, null=True,
        verbose_name="Volume du réservoir (millions m³)"
    )
    population_deplacee = models.IntegerField(
        blank=True, null=True,
        verbose_name="Population déplacée (personnes)"
    )
    bilan_carbone = models.DecimalField(
        max_digits=15, decimal_places=2,
        blank=True, null=True,
        verbose_name="Bilan carbone (t CO₂)"
    )
    importance = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Importance (1-5)"
    )
    projet = models.ForeignKey(
        Projet,
        on_delete=models.CASCADE,
        related_name='impacts_environnementaux',
        verbose_name="Projet"
    )
    etape = models.ForeignKey(
        EtapeProjet,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='impacts_es',
        verbose_name="Étape concernée"
    )
    
    class Meta:
        verbose_name = "Impact environnemental et social"
        verbose_name_plural = "Impacts environnementaux et sociaux"
        ordering = ['-importance', 'date_impact']
    
    def __str__(self):
        return f"{self.get_type_impact_display()} - {self.projet.nom}"


# ================================================================
# 7. MODÈLE EVENEMENT
# ================================================================
class Evenement(models.Model):
    """
    Événements marquants de l'histoire du projet.
    """
    TYPE_EVENEMENT_CHOICES: ClassVar[list[tuple[str, str]]] = [
        ('politique', 'Politique'),
        ('financier', 'Financier'),
        ('technique', 'Technique'),
        ('diplomatique', 'Diplomatique'),
        ('social', 'Social'),
        ('environnemental', 'Environnemental'),
        ('juridique', 'Juridique'),
    ]
    
    titre = models.CharField(max_length=200, verbose_name="Titre de l'événement")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    date_evenement = models.DateField(verbose_name="Date de l'événement")
    type_evenement = models.CharField(
        max_length=50, choices=TYPE_EVENEMENT_CHOICES,
        verbose_name="Type d'événement"
    )
    importance = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Importance (1-5)"
    )
    source = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name="Source de l'information"
    )
    localisation = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name="Localisation"
    )
    projet = models.ForeignKey(
        Projet,
        on_delete=models.CASCADE,
        related_name='evenements',
        verbose_name="Projet"
    )
    acteurs = models.ManyToManyField(
        Acteur,
        through='ActeurEvenement',
        related_name='evenements',
        verbose_name="Acteurs impliqués"
    )
    
    class Meta:
        verbose_name = "Événement"
        verbose_name_plural = "Événements"
        ordering = ['-date_evenement']
    
    def __str__(self):
        return f"{self.titre} ({self.date_evenement.year})"
    
    def est_majeur(self):
        """Vérifie si l'événement est majeur (importance >= 4)."""
        return self.importance >= 4


# ================================================================
# 8. MODÈLE ACTEUR_EVENEMENT (table de liaison N,N)
# ================================================================
class ActeurEvenement(models.Model):
    """
    Table de liaison entre les acteurs et les événements.
    """
    ROLE_CHOICES: ClassVar[list[tuple[str, str]]] = [
        ('initiateur', 'Initiateur'),
        ('participant', 'Participant'),
        ('opposant', 'Opposant'),
        ('beneficiaire', 'Bénéficiaire'),
        ('observateur', 'Observateur'),
        ('victime', 'Victime'),
    ]
    
    acteur = models.ForeignKey(
        Acteur,
        on_delete=models.CASCADE,
        verbose_name="Acteur"
    )
    evenement = models.ForeignKey(
        Evenement,
        on_delete=models.CASCADE,
        verbose_name="Événement"
    )
    role = models.CharField(
        max_length=100, choices=ROLE_CHOICES,
        blank=True, null=True,
        verbose_name="Rôle dans l'événement"
    )
    
    class Meta:
        verbose_name = "Liaison acteur-événement"
        verbose_name_plural = "Liaisons acteurs-événements"
        unique_together = ('acteur', 'evenement')
    
    def __str__(self):
        return f"{self.acteur.nom} - {self.evenement.titre}"


# ================================================================
# 9. MODÈLE DOCUMENT
# ================================================================
class Document(models.Model):
    """
    Documents, rapports, études et archives liés au projet.
    """
    TYPE_DOCUMENT_CHOICES: ClassVar[list[tuple[str, str]]] = [
        ('rapport', 'Rapport'),
        ('etude', 'Étude'),
        ('archive', 'Archive'),
        ('correspondance', 'Correspondance'),
        ('contrat', 'Contrat'),
        ('article', 'Article'),
        ('these', 'Thèse / Mémoire'),
        ('communique', 'Communiqué de presse'),
    ]
    
    ETAT_CONSERVATION_CHOICES: ClassVar[list[tuple[str, str]]] = [
        ('bon', 'Bon'),
        ('moyen', 'Moyen'),
        ('mauvais', 'Mauvais'),
        ('inconnu', 'Inconnu'),
    ]
    
    titre = models.CharField(max_length=255, verbose_name="Titre du document")
    type_document = models.CharField(
        max_length=50, choices=TYPE_DOCUMENT_CHOICES,
        verbose_name="Type de document"
    )
    date_publication = models.DateField(
        blank=True, null=True,
        verbose_name="Date de publication"
    )
    auteur = models.CharField(
        max_length=200, blank=True, null=True,
        verbose_name="Auteur"
    )
    resume = models.TextField(blank=True, null=True, verbose_name="Résumé")
    url = models.URLField(
        max_length=255, blank=True, null=True,
        verbose_name="URL"
    )
    fichier = models.FileField(
        upload_to='documents/',
        blank=True, null=True,
        verbose_name="Fichier"
    )
    mots_cles = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name="Mots-clés"
    )
    etat_conservation = models.CharField(
        max_length=50, choices=ETAT_CONSERVATION_CHOICES,
        default='inconnu',
        verbose_name="État de conservation"
    )
    projet = models.ForeignKey(
        Projet,
        on_delete=models.CASCADE,
        related_name='documents',
        verbose_name="Projet"
    )
    
    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"
        ordering = ['-date_publication']
    
    def __str__(self):
        return self.titre


# ================================================================
# 10. MODÈLE CHRONOLOGIE
# ================================================================
class Chronologie(models.Model):
    """
    Frise chronologique du projet (vue agrégée).
    """
    TYPE_ENTREE_CHOICES: ClassVar[list[tuple[str, str]]] = [
        ('etape', 'Étape'),
        ('evenement', 'Événement'),
        ('impact', 'Impact'),
        ('decision', 'Décision'),
    ]
    
    date_debut = models.DateField(blank=True, null=True, verbose_name="Date de début")
    date_fin = models.DateField(blank=True, null=True, verbose_name="Date de fin")
    description = models.TextField(verbose_name="Description")
    date_lancement_travaux = models.DateField(
        blank=True, null=True,
        verbose_name="Date de lancement des travaux"
    )
    date_mise_service = models.DateField(
        blank=True, null=True,
        verbose_name="Date de mise en service commerciale (COD)"
    )
    duree_vie = models.CharField(
        max_length=50, blank=True, null=True,
        verbose_name="Durée de vie"
    )
    type_entree = models.CharField(
        max_length=50, choices=TYPE_ENTREE_CHOICES,
        verbose_name="Type d'entrée"
    )
    
    class Meta:
        verbose_name = "Chronologie"
        verbose_name_plural = "Chronologies"
        ordering = ['date_debut']
    
    def __str__(self):
        return f"{self.description[:50]} ({self.date_debut})"
    
    def get_duree(self):
        """Calcule la durée en années."""
        if self.date_fin and self.date_debut:
            return self.date_fin.year - self.date_debut.year
        return None