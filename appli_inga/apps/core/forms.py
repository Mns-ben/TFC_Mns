# ================================================================
# FORMULAIRES DJANGO - OBSERVATOIRE HISTORIQUE DU PROJET GRAND INGA
# Application : core
# Fichier : forms.py
# ================================================================

from typing import ClassVar

from django import forms
from django.core.exceptions import ValidationError

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
# STYLES COMMUNS POUR LES FORMULAIRES
# ================================================================
# Classes CSS appliquées à tous les champs
INPUT_CLASS = 'form-control'
SELECT_CLASS = 'form-select'
TEXTAREA_CLASS = 'form-control'
CHECKBOX_CLASS = 'form-check-input'


# ================================================================
# 1. FORMULAIRE : PROJET
# ================================================================
class ProjetForm(forms.ModelForm):
    """
    Formulaire pour l'ajout et la modification d'un projet.
    """
    class Meta:
        model = Projet
        fields: ClassVar[list[str]] = [
            'nom', 'description', 'capacite_prevue', 'investissement_estime',
            'statut_actuel', 'date_debut_projet', 'date_fin_prevue',
            'localisation', 'coordonnees_gps', 'maitre_ouvrage',
            'hauteur_chute', 'nombre_turbines', 'type_turbines'
        ]
        widgets: ClassVar[dict] = {
            'nom': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Ex: Grand Inga'}),
            'description': forms.Textarea(attrs={'class': TEXTAREA_CLASS, 'rows': 4}),
            'capacite_prevue': forms.NumberInput(attrs={'class': INPUT_CLASS, 'step': '0.01'}),
            'investissement_estime': forms.NumberInput(attrs={'class': INPUT_CLASS, 'step': '0.01'}),
            'statut_actuel': forms.Select(attrs={'class': SELECT_CLASS}),
            'date_debut_projet': forms.DateInput(attrs={'class': INPUT_CLASS, 'type': 'date'}),
            'date_fin_prevue': forms.DateInput(attrs={'class': INPUT_CLASS, 'type': 'date'}),
            'localisation': forms.TextInput(attrs={'class': INPUT_CLASS}),
            'coordonnees_gps': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': '-5.5242, 13.6205'}),
            'maitre_ouvrage': forms.TextInput(attrs={'class': INPUT_CLASS}),
            'hauteur_chute': forms.NumberInput(attrs={'class': INPUT_CLASS, 'step': '0.01'}),
            'nombre_turbines': forms.NumberInput(attrs={'class': INPUT_CLASS}),
            'type_turbines': forms.Select(attrs={'class': SELECT_CLASS}),
        }
        labels: ClassVar[dict[str, str]] = {
            'nom': 'Nom du projet',
            'description': 'Description',
            'capacite_prevue': 'Capacité prévue (MW)',
            'investissement_estime': 'Investissement estimé (USD)',
            'statut_actuel': 'Statut actuel',
            'date_debut_projet': 'Date de début du projet',
            'date_fin_prevue': 'Date de fin prévue',
            'localisation': 'Localisation',
            'coordonnees_gps': 'Coordonnées GPS',
            'maitre_ouvrage': "Maître d'ouvrage",
            'hauteur_chute': 'Hauteur de chute (m)',
            'nombre_turbines': 'Nombre de turbines',
            'type_turbines': 'Type de turbines',
        }

    def clean(self):
        cleaned_data = super().clean()
        date_debut = cleaned_data.get('date_debut_projet')
        date_fin = cleaned_data.get('date_fin_prevue')
        
        if date_debut and date_fin and date_debut > date_fin:
            raise ValidationError(
                "La date de début doit être antérieure à la date de fin prévue."
            )
        return cleaned_data


# ================================================================
# 2. FORMULAIRE : ETAPE_PROJET
# ================================================================
class EtapeProjetForm(forms.ModelForm):
    """
    Formulaire pour l'ajout et la modification d'une étape.
    """
    class Meta:
        model = EtapeProjet
        fields: ClassVar[list[str]] = [
            'nom', 'description', 'date_debut', 'date_fin',
            'statut', 'objectifs', 'resultats', 'responsable_etape', 'projet'
        ]
        widgets: ClassVar[dict] = {
            'nom': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Ex: Construction Inga I'}),
            'description': forms.Textarea(attrs={'class': TEXTAREA_CLASS, 'rows': 3}),
            'date_debut': forms.DateInput(attrs={'class': INPUT_CLASS, 'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'class': INPUT_CLASS, 'type': 'date'}),
            'statut': forms.Select(attrs={'class': SELECT_CLASS}),
            'objectifs': forms.Textarea(attrs={'class': TEXTAREA_CLASS, 'rows': 3}),
            'resultats': forms.Textarea(attrs={'class': TEXTAREA_CLASS, 'rows': 3}),
            'responsable_etape': forms.TextInput(attrs={'class': INPUT_CLASS}),
            'projet': forms.Select(attrs={'class': SELECT_CLASS}),
        }
        labels: ClassVar[dict] = {
            'nom': "Nom de l'étape",
            'description': 'Description',
            'date_debut': 'Date de début',
            'date_fin': 'Date de fin',
            'statut': 'Statut',
            'objectifs': 'Objectifs',
            'resultats': 'Résultats',
            'responsable_etape': "Responsable de l'étape",
            'projet': 'Projet associé',
        }

    def clean(self):
        cleaned_data = super().clean()
        date_debut = cleaned_data.get('date_debut')
        date_fin = cleaned_data.get('date_fin')
        
        if date_debut and date_fin and date_debut >= date_fin:
            raise ValidationError(
                "La date de début doit être strictement antérieure à la date de fin."
            )
        return cleaned_data


# ================================================================
# 3. FORMULAIRE : ACTEUR
# ================================================================
class ActeurForm(forms.ModelForm):
    """
    Formulaire pour l'ajout et la modification d'un acteur.
    """
    class Meta:
        model = Acteur
        fields: ClassVar[list[str]] = [
            'nom', 'type_acteur', 'categorie', 'pays',
            'description', 'site_web', 'date_creation', 'date_disparition'
        ]
        widgets: ClassVar[dict] = {
            'nom': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Ex: Banque mondiale'}),
            'type_acteur': forms.Select(attrs={'class': SELECT_CLASS}),
            'categorie': forms.Select(attrs={'class': SELECT_CLASS}),
            'pays': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Ex: RDC'}),
            'description': forms.Textarea(attrs={'class': TEXTAREA_CLASS, 'rows': 4}),
            'site_web': forms.URLInput(attrs={'class': INPUT_CLASS, 'placeholder': 'https://...'}),
            'date_creation': forms.DateInput(attrs={'class': INPUT_CLASS, 'type': 'date'}),
            'date_disparition': forms.DateInput(attrs={'class': INPUT_CLASS, 'type': 'date'}),
        }
        labels: ClassVar[dict] = {
            'nom': "Nom de l'acteur",
            'type_acteur': "Type d'acteur",
            'categorie': 'Catégorie',
            'pays': 'Pays',
            'description': 'Description',
            'site_web': 'Site web',
            'date_creation': 'Date de création',
            'date_disparition': 'Date de disparition',
        }

    def clean(self):
        cleaned_data = super().clean()
        date_creation = cleaned_data.get('date_creation')
        date_disparition = cleaned_data.get('date_disparition')
        
        if date_creation and date_disparition and date_creation > date_disparition:
            raise ValidationError(
                "La date de création doit être antérieure à la date de disparition."
            )
        return cleaned_data


# ================================================================
# 4. FORMULAIRE : IMPACT_ACTEUR
# ================================================================
class ImpactActeurForm(forms.ModelForm):
    """
    Formulaire pour l'ajout et la modification d'un impact d'acteur.
    """
    class Meta:
        model = ImpactActeur
        fields: ClassVar[list[str]] = [
            'acteur', 'etape', 'type_impact', 'importance',
            'description', 'consequences', 'date_impact'
        ]
        widgets: ClassVar[dict] = {
            'acteur': forms.Select(attrs={'class': SELECT_CLASS}),
            'etape': forms.Select(attrs={'class': SELECT_CLASS}),
            'type_impact': forms.Select(attrs={'class': SELECT_CLASS}),
            'importance': forms.NumberInput(attrs={'class': INPUT_CLASS, 'min': 1, 'max': 5}),
            'description': forms.Textarea(attrs={'class': TEXTAREA_CLASS, 'rows': 3}),
            'consequences': forms.Textarea(attrs={'class': TEXTAREA_CLASS, 'rows': 3}),
            'date_impact': forms.DateInput(attrs={'class': INPUT_CLASS, 'type': 'date'}),
        }
        labels: ClassVar[dict] = {
            'acteur': 'Acteur',
            'etape': 'Étape concernée',
            'type_impact': "Type d'impact",
            'importance': 'Importance (1 à 5)',
            'description': 'Description',
            'consequences': 'Conséquences',
            'date_impact': "Date de l'impact",
        }

    def clean_importance(self):
        importance = self.cleaned_data.get('importance')
        if importance is not None and (importance < 1 or importance > 5):
            raise ValidationError("L'importance doit être comprise entre 1 et 5.")
        return importance


# ================================================================
# 5. FORMULAIRE : IMPACT_ENVIRONNEMENTAL_SOCIAL
# ================================================================
class ImpactEnvironnementalSocialForm(forms.ModelForm):
    """
    Formulaire pour l'ajout et la modification d'un impact environnemental/social.
    """
    class Meta:
        model = ImpactEnvironnementalSocial
        fields: ClassVar[list[str]] = [
            'projet', 'etape', 'type_impact', 'importance',
            'surface_ennoyee', 'volume_reservoir', 'population_deplacee',
            'bilan_carbone', 'description', 'date_impact'
        ]
        widgets: ClassVar = {
            'projet': forms.Select(attrs={'class': SELECT_CLASS}),
            'etape': forms.Select(attrs={'class': SELECT_CLASS}),
            'type_impact': forms.Select(attrs={'class': SELECT_CLASS}),
            'importance': forms.NumberInput(attrs={'class': INPUT_CLASS, 'min': 1, 'max': 5}),
            'surface_ennoyee': forms.NumberInput(attrs={'class': INPUT_CLASS, 'step': '0.01'}),
            'volume_reservoir': forms.NumberInput(attrs={'class': INPUT_CLASS, 'step': '0.01'}),
            'population_deplacee': forms.NumberInput(attrs={'class': INPUT_CLASS}),
            'bilan_carbone': forms.NumberInput(attrs={'class': INPUT_CLASS, 'step': '0.01'}),
            'description': forms.Textarea(attrs={'class': TEXTAREA_CLASS, 'rows': 3}),
            'date_impact': forms.DateInput(attrs={'class': INPUT_CLASS, 'type': 'date'}),
        }
        labels: ClassVar[dict[str, str]] = {
            'projet': 'Projet',
            'etape': 'Étape concernée',
            'type_impact': "Type d'impact",
            'importance': 'Importance (1 à 5)',
            'surface_ennoyee': 'Surface ennoyée (km²)',
            'volume_reservoir': 'Volume du réservoir (millions m³)',
            'population_deplacee': 'Population déplacée (personnes)',
            'bilan_carbone': 'Bilan carbone (t CO₂)',
            'description': 'Description',
            'date_impact': "Date de l'impact",
        }


# ================================================================
# 6. FORMULAIRE : EVENEMENT
# ================================================================
class EvenementForm(forms.ModelForm):
    """
    Formulaire pour l'ajout et la modification d'un événement.
    """
    class Meta:
        model = Evenement
        fields = (
            'titre', 'description', 'date_evenement', 'type_evenement',
            'importance', 'source', 'localisation', 'projet', 'acteurs'
        )
        widgets: ClassVar[dict[str, forms.Widget]] = {
            'titre': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': "Ex: Signature de l'accord"}),
            'description': forms.Textarea(attrs={'class': TEXTAREA_CLASS, 'rows': 4}),
            'date_evenement': forms.DateInput(attrs={'class': INPUT_CLASS, 'type': 'date'}),
            'type_evenement': forms.Select(attrs={'class': SELECT_CLASS}),
            'importance': forms.NumberInput(attrs={'class': INPUT_CLASS, 'min': 1, 'max': 5}),
            'source': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Ex: Le Monde'}),
            'localisation': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Ex: Kinshasa'}),
            'projet': forms.Select(attrs={'class': SELECT_CLASS}),
            'acteurs': forms.SelectMultiple(attrs={'class': SELECT_CLASS, 'size': 5}),
        }
        labels: ClassVar[dict[str, str]] = {
            'titre': "Titre de l'événement",
            'description': 'Description',
            'date_evenement': "Date de l'événement",
            'type_evenement': "Type d'événement",
            'importance': 'Importance (1 à 5)',
            'source': "Source de l'information",
            'localisation': 'Localisation',
            'projet': 'Projet associé',
            'acteurs': 'Acteurs impliqués',
        }

    def clean_importance(self):
        importance = self.cleaned_data.get('importance')
        if importance is not None and (importance < 1 or importance > 5):
            raise ValidationError("L'importance doit être comprise entre 1 et 5.")
        return importance


# ================================================================
# 7. FORMULAIRE : ACTEUR_EVENEMENT
# ================================================================
class ActeurEvenementForm(forms.ModelForm):
    """
    Formulaire pour l'ajout d'un lien acteur-événement.
    """
    class Meta:
        model = ActeurEvenement
        fields: ClassVar[list[str]] = ['evenement', 'role']
        widgets: ClassVar[dict[str, forms.Widget]] = {
            'acteur': forms.Select(attrs={'class': SELECT_CLASS}),
            'evenement': forms.Select(attrs={'class': SELECT_CLASS}),
            'role': forms.Select(attrs={'class': SELECT_CLASS}),
        }
        labels: ClassVar[dict[str, str]] = {
            'acteur': 'Acteur',
            'evenement': 'Événement',
            'role': "Rôle de l'acteur",
        }


# ================================================================
# 8. FORMULAIRE : DOCUMENT
# ================================================================
class DocumentForm(forms.ModelForm):
    """
    Formulaire pour l'ajout et la modification d'un document.
    """
    class Meta:
        model = Document
        fields: ClassVar[list[str]] = [
            'titre', 'type_document', 'projet', 'auteur',
            'date_publication', 'etat_conservation',
            'resume', 'mots_cles', 'url', 'fichier'
        ]
        widgets: ClassVar[dict] = {
            'titre': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Ex: Rapport de construction Inga I'}),
            'type_document': forms.Select(attrs={'class': SELECT_CLASS}),
            'projet': forms.Select(attrs={'class': SELECT_CLASS}),
            'auteur': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Ex: SNEL'}),
            'date_publication': forms.DateInput(attrs={'class': INPUT_CLASS, 'type': 'date'}),
            'etat_conservation': forms.Select(attrs={'class': SELECT_CLASS}),
            'resume': forms.Textarea(attrs={'class': TEXTAREA_CLASS, 'rows': 4}),
            'mots_cles': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Ex: financement, barrage'}),
            'url': forms.URLInput(attrs={'class': INPUT_CLASS, 'placeholder': 'https://...'}),
            'fichier': forms.FileInput(attrs={'class': INPUT_CLASS}),
        }
        labels: ClassVar[dict[str, str]] = {
            'titre': 'Titre du document',
            'type_document': 'Type de document',
            'projet': 'Projet associé',
            'auteur': 'Auteur',
            'date_publication': 'Date de publication',
            'etat_conservation': 'État de conservation',
            'resume': 'Résumé',
            'mots_cles': 'Mots-clés',
            'url': 'URL',
            'fichier': 'Fichier (PDF, DOCX)',
        }


# ================================================================
# 9. FORMULAIRE : CHRONOLOGIE
# ================================================================
class ChronologieForm(forms.ModelForm):
    """
    Formulaire pour l'ajout et la modification d'une entrée chronologique.
    """
    class Meta:
        model = Chronologie
        fields: ClassVar[list[str]] = [
            'date_debut', 'date_fin', 'description', 'type_entree',
            'date_lancement_travaux', 'date_mise_service', 'duree_vie'
        ]
        widgets: ClassVar[dict[str, forms.Widget]] = {
            'date_debut': forms.DateInput(attrs={'class': INPUT_CLASS, 'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'class': INPUT_CLASS, 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': TEXTAREA_CLASS, 'rows': 3}),
            'type_entree': forms.Select(attrs={'class': SELECT_CLASS}),
            'date_lancement_travaux': forms.DateInput(attrs={'class': INPUT_CLASS, 'type': 'date'}),
            'date_mise_service': forms.DateInput(attrs={'class': INPUT_CLASS, 'type': 'date'}),
            'duree_vie': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Ex: 50 ans'}),
        }
        labels: ClassVar[dict[str, str]] = {
            'date_debut': 'Date de début',
            'date_fin': 'Date de fin',
            'description': 'Description',
            'type_entree': "Type d'entrée",
            'date_lancement_travaux': 'Date de lancement des travaux',
            'date_mise_service': 'Date de mise en service commerciale (COD)',
            'duree_vie': 'Durée de vie',
        }

    def clean(self):
        cleaned_data = super().clean()
        date_debut = cleaned_data.get('date_debut')
        date_fin = cleaned_data.get('date_fin')
        
        if date_debut and date_fin and date_debut > date_fin:
            raise ValidationError(
                "La date de début doit être antérieure à la date de fin."
            )
        return cleaned_data


# ================================================================
# 10. FORMULAIRE : UTILISATEUR (inscription)
# ================================================================
class UtilisateurForm(forms.ModelForm):
    """
    Formulaire d'inscription d'un utilisateur personnalisé.
    """
    password1 = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={'class': INPUT_CLASS}),
        min_length=8,
        help_text="Minimum 8 caractères."
    )
    password2 = forms.CharField(
        label='Confirmation du mot de passe',
        widget=forms.PasswordInput(attrs={'class': INPUT_CLASS}),
    )
    
    class Meta:
        model = Utilisateur
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'institution')
        widgets: ClassVar[dict[str, forms.Widget]] = {
            'username': forms.TextInput(attrs={'class': INPUT_CLASS}),
            'email': forms.EmailInput(attrs={'class': INPUT_CLASS}),
            'first_name': forms.TextInput(attrs={'class': INPUT_CLASS}),
            'last_name': forms.TextInput(attrs={'class': INPUT_CLASS}),
            'role': forms.Select(attrs={'class': SELECT_CLASS}),
            'institution': forms.TextInput(attrs={'class': INPUT_CLASS}),
        }
        labels: ClassVar[dict[str, str]] = {
            'username': "Nom d'utilisateur",
            'email': 'Email',
            'first_name': 'Prénom',
            'last_name': 'Nom',
            'role': 'Rôle',
            'institution': 'Institution',
        }
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise ValidationError("Les deux mots de passe ne correspondent pas.")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user