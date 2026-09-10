# ================================================================
# VUES DJANGO - OBSERVATOIRE HISTORIQUE DU PROJET GRAND INGA
# Application : core
# Fichier : views.py
# ================================================================

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import (
    ActeurForm,
    DocumentForm,
    EtapeProjetForm,
    EvenementForm,
)
from .models import (
    Acteur,
    Chronologie,
    Document,
    EtapeProjet,
    Evenement,
    ImpactActeur,
    ImpactEnvironnementalSocial,
    Projet,
)


# ================================================================
# VUE : ADMIN DASHBOARD (tableau de bord d'administration)
# ================================================================
@login_required
def admin_dashboard(request):
    """
    Tableau de bord d'administration : affiche les statistiques
    et les liens vers chaque section CRUD.
    """
    context = {
        'nb_etapes': EtapeProjet.objects.count(),
        'nb_acteurs': Acteur.objects.count(),
        'nb_evenements': Evenement.objects.count(),
        'nb_documents': Document.objects.count(),
        'nb_impacts_acteurs': ImpactActeur.objects.count(),
        'nb_impacts_es': ImpactEnvironnementalSocial.objects.count(),
        'derniers_evenements': Evenement.objects.order_by('-date_evenement')[:5],
        'dernieres_etapes': EtapeProjet.objects.order_by('-date_debut')[:5],
    }
    return render(request, 'core/admin/dashboard.html', context)
# ================================================================
# FONCTION UTILITAIRE : Récupérer le projet actif
# ================================================================
def get_projet_actif():
    """Récupère le premier projet (Grand Inga)."""
    return Projet.objects.first()


# ================================================================
# 1. VUE : DASHBOARD (Page d'accueil)
# ================================================================
def dashboard(request):
    """
    Vue principale : affiche les indicateurs clés du projet.
    """
    projet = get_projet_actif()
    
    # Indicateurs clés
    nb_etapes = EtapeProjet.objects.filter(projet=projet).count()
    nb_evenements = Evenement.objects.filter(projet=projet).count()
    nb_acteurs = Acteur.objects.count()
    nb_documents = Document.objects.filter(projet=projet).count()
    
    # Derniers événements
    derniers_evenements = Evenement.objects.filter(
        projet=projet
    ).order_by('-date_evenement')[:5]
    
    # Répartition des événements par type
    evenements_par_type = Evenement.objects.filter(
        projet=projet
    ).values('type_evenement').annotate(nb=Count('id'))
    
    # Évolution par décennie
    from django.db.models.functions import ExtractYear
    evenements_par_decennie = Evenement.objects.filter(
        projet=projet
    ).annotate(
        annee=ExtractYear('date_evenement')
    ).values('annee').annotate(nb=Count('id')).order_by('annee')
    
    context = {
        'projet': projet,
        'nb_etapes': nb_etapes,
        'nb_evenements': nb_evenements,
        'nb_acteurs': nb_acteurs,
        'nb_documents': nb_documents,
        'derniers_evenements': derniers_evenements,
        'evenements_par_type': evenements_par_type,
        'evenements_par_decennie': evenements_par_decennie,
    }
    return render(request, 'core/pages/dashboard.html', context)


# ================================================================
# 2. VUE : CHRONOLOGIE
# ================================================================
def chronologie(request):
    """
    Vue de la frise chronologique.
    Affiche les étapes et événements triés par date.
    """
    projet = get_projet_actif()
    
    # Filtres (optionnels)
    date_debut = request.GET.get('date_debut')
    date_fin = request.GET.get('date_fin')
    type_filtre = request.GET.get('type', 'tous')
    
    etapes = EtapeProjet.objects.filter(projet=projet)
    evenements = Evenement.objects.filter(projet=projet)
    
    # Application des filtres
    if date_debut:
        etapes = etapes.filter(date_debut__gte=date_debut)
        evenements = evenements.filter(date_evenement__gte=date_debut)
    if date_fin:
        etapes = etapes.filter(date_debut__lte=date_fin)
        evenements = evenements.filter(date_evenement__lte=date_fin)
    
    # Filtre par type
    if type_filtre == 'etapes':
        evenements = Evenement.objects.none()
    elif type_filtre == 'evenements':
        etapes = EtapeProjet.objects.none()
    
    # Fusion chronologique
    entrees = []
    for e in etapes:
        entrees.append({
            'type': 'etape',
            'titre': e.nom,
            'description': e.description,
            'date': e.date_debut,
            'date_fin': e.date_fin,
            'statut': e.statut,
            'id': e.id,
        })
    for ev in evenements:
        entrees.append({
            'type': 'evenement',
            'titre': ev.titre,
            'description': ev.description,
            'date': ev.date_evenement,
            'importance': ev.importance,
            'id': ev.id,
        })
    
    # Tri par date
    entrees.sort(key=lambda x: x['date'])
    
    context = {
        'projet': projet,
        'entrees': entrees,
        'date_debut': date_debut,
        'date_fin': date_fin,
        'type_filtre': type_filtre,
    }
    return render(request, 'core/pages/chronologie.html', context)


# ================================================================
# 3. VUE : ACTEURS (liste)
# ================================================================


# ================================================================
# 4. VUE : ACTEUR (fiche détaillée)
# ================================================================
def acteur_detail(request, acteur_id):
    """
    Vue de la fiche détaillée d'un acteur.
    """
    acteur = get_object_or_404(Acteur, id=acteur_id)
    
    # Impacts de l'acteur
    impacts = ImpactActeur.objects.filter(acteur=acteur).order_by('-importance')
    
    # Événements auxquels l'acteur a participé
    evenements = Evenement.objects.filter(acteurs=acteur).order_by('-date_evenement')
    
    # Calcul de l'impact moyen
    impact_moyen = impacts.aggregate(Avg('importance'))['importance__avg']
    
    context = {
        'acteur': acteur,
        'impacts': impacts,
        'evenements': evenements,
        'impact_moyen': impact_moyen,
        'nb_impacts': impacts.count(),
    }
    return render(request, 'core/pages/acteur_detail.html', context)


# ================================================================
# 5. VUE : EVENEMENTS (liste)
# ================================================================


# ================================================================
# 6. VUE : EVENEMENT (fiche détaillée)
# ================================================================
def evenement_detail(request, evenement_id):
    """
    Vue de la fiche détaillée d'un événement.
    """
    evenement = get_object_or_404(Evenement, id=evenement_id)
    
    # Acteurs impliqués
    acteurs_impliques = evenement.acteurs.all()
    
    # Documents associés (à filtrer si relation créée)
    documents = Document.objects.filter(projet=evenement.projet)[:5]
    
    context = {
        'evenement': evenement,
        'acteurs_impliques': acteurs_impliques,
        'documents': documents,
    }
    return render(request, 'core/pages/evenement_detail.html', context)


# ================================================================
# 7. VUE : DOCUMENTS (bibliothèque)
# ================================================================

# ================================================================
# 3. VUE : ACTEURS (avec filtres configurables)
# ================================================================
def acteurs(request):
    acteurs_list = Acteur.objects.all()
    
    type_filtre = request.GET.get('type')
    pays_filtre = request.GET.get('pays')
    recherche = request.GET.get('q')
    
    if type_filtre:
        acteurs_list = acteurs_list.filter(type_acteur=type_filtre)
    if pays_filtre:
        acteurs_list = acteurs_list.filter(pays=pays_filtre)
    if recherche:
        acteurs_list = acteurs_list.filter(
            Q(nom__icontains=recherche) |
            Q(description__icontains=recherche) |
            Q(pays__icontains=recherche)
        )
    
    pays_disponibles = Acteur.objects.values_list('pays', flat=True).distinct()
    
    # Configuration des filtres pour le partial
    filtres = [
        {
            'name': 'type',
            'label_defaut': 'Tous les types',
            'selected': type_filtre,
            'options': [
                {'value': 'gouvernement', 'label': 'Gouvernement'},
                {'value': 'entreprise_publique', 'label': 'Entreprise publique'},
                {'value': 'entreprise_privee', 'label': 'Entreprise privée'},
                {'value': 'institution_financiere', 'label': 'Institution financière'},
                {'value': 'ong', 'label': 'ONG'},
                {'value': 'organisation_internationale', 'label': 'Organisation internationale'},
                {'value': 'personnalite_politique', 'label': 'Personnalité politique'},
                {'value': 'universite', 'label': 'Université / Recherche'},
            ]
        },
        {
            'name': 'pays',
            'label_defaut': 'Tous les pays',
            'selected': pays_filtre,
            'options': [
                {'value': p, 'label': p} for p in pays_disponibles if p
            ]
        },
    ]
    
    context = {
        'acteurs': acteurs_list,
        'recherche': recherche,
        'filtres': filtres,
    }
    return render(request, 'core/pages/acteurs.html', context)


# ================================================================
# 5. VUE : EVENEMENTS (avec filtres configurables)
# ================================================================
def evenements(request):
    projet = get_projet_actif()
    evenements_list = Evenement.objects.filter(projet=projet)
    
    type_filtre = request.GET.get('type')
    importance_filtre = request.GET.get('importance')
    recherche = request.GET.get('q')
    
    if type_filtre:
        evenements_list = evenements_list.filter(type_evenement=type_filtre)
    if importance_filtre:
        evenements_list = evenements_list.filter(importance=importance_filtre)
    if recherche:
        evenements_list = evenements_list.filter(
            Q(titre__icontains=recherche) |
            Q(description__icontains=recherche)
        )
    
    evenements_list = evenements_list.order_by('-date_evenement')
    
    filtres = [
        {
            'name': 'type',
            'label_defaut': 'Tous les types',
            'selected': type_filtre,
            'options': [
                {'value': 'politique', 'label': 'Politique'},
                {'value': 'financier', 'label': 'Financier'},
                {'value': 'technique', 'label': 'Technique'},
                {'value': 'diplomatique', 'label': 'Diplomatique'},
                {'value': 'social', 'label': 'Social'},
                {'value': 'environnemental', 'label': 'Environnemental'},
            ]
        },
        {
            'name': 'importance',
            'label_defaut': 'Toute importance',
            'selected': importance_filtre,
            'options': [
                {'value': '1', 'label': 'Importance 1'},
                {'value': '2', 'label': 'Importance 2'},
                {'value': '3', 'label': 'Importance 3'},
                {'value': '4', 'label': 'Importance 4'},
                {'value': '5', 'label': 'Importance 5'},
            ]
        },
    ]
    
    context = {
        'evenements': evenements_list,
        'recherche': recherche,
        'filtres': filtres,
    }
    return render(request, 'core/pages/evenements.html', context)


# ================================================================
# 7. VUE : DOCUMENTS (avec filtres configurables)
# ================================================================
def documents(request):
    projet = get_projet_actif()
    documents_list = Document.objects.filter(projet=projet)
    
    type_filtre = request.GET.get('type')
    recherche = request.GET.get('q')
    
    if type_filtre:
        documents_list = documents_list.filter(type_document=type_filtre)
    if recherche:
        documents_list = documents_list.filter(
            Q(titre__icontains=recherche) |
            Q(auteur__icontains=recherche) |
            Q(resume__icontains=recherche) |
            Q(mots_cles__icontains=recherche)
        )
    
    documents_list = documents_list.order_by('-date_publication')
    
    filtres = [
        {
            'name': 'type',
            'label_defaut': 'Tous les types',
            'selected': type_filtre,
            'options': [
                {'value': 'rapport', 'label': 'Rapport'},
                {'value': 'etude', 'label': 'Étude'},
                {'value': 'archive', 'label': 'Archive'},
                {'value': 'correspondance', 'label': 'Correspondance'},
                {'value': 'contrat', 'label': 'Contrat'},
                {'value': 'article', 'label': 'Article'},
                {'value': 'these', 'label': 'Thèse / Mémoire'},
                {'value': 'communique', 'label': 'Communiqué'},
            ]
        },
    ]
    
    context = {
        'documents': documents_list,
        'recherche': recherche,
        'filtres': filtres,
    }
    return render(request, 'core/pages/documents.html', context)




# ================================================================
# 8. VUE : CARTE SIG
# ================================================================
def carte(request):
    """
    Vue de la carte interactive (SIG).
    """
    projet = get_projet_actif()
    
    # Données pour la carte
    etapes = EtapeProjet.objects.filter(projet=projet)
    impacts_es = ImpactEnvironnementalSocial.objects.filter(projet=projet)
    
    context = {
        'projet': projet,
        'etapes': etapes,
        'impacts_es': impacts_es,
    }
    return render(request, 'core/pages/carte.html', context)


# ================================================================
# 9. VUE : STATISTIQUES
# ================================================================
def statistiques(request):
    """
    Vue des statistiques et analyses.
    """
    projet = get_projet_actif()
    
    # Répartition des impacts par type
    impacts_par_type = ImpactActeur.objects.values(
        'type_impact'
    ).annotate(nb=Count('id'))
    
    # Acteurs les plus influents (par nombre d'impacts)
    acteurs_influents = Acteur.objects.annotate(
        nb_impacts=Count('impacts'),
        importance_moyenne=Avg('impacts__importance')
    ).filter(nb_impacts__gt=0).order_by('-importance_moyenne')[:10]
    
    # Impacts environnementaux agrégés
    impacts_env = ImpactEnvironnementalSocial.objects.filter(
        projet=projet
    ).aggregate(
        surface_totale=Sum('surface_ennoyee'),
        volume_total=Sum('volume_reservoir'),
        population_totale=Sum('population_deplacee'),
        bilan_carbone_total=Sum('bilan_carbone'),
    )
    
    # Événements par décennie
    from django.db.models.functions import ExtractYear
    evenements_decennie = Evenement.objects.filter(
        projet=projet
    ).annotate(
        annee=ExtractYear('date_evenement')
    ).values('annee').annotate(nb=Count('id')).order_by('annee')
    
    context = {
        'projet': projet,
        'impacts_par_type': impacts_par_type,
        'acteurs_influents': acteurs_influents,
        'impacts_env': impacts_env,
        'evenements_decennie': evenements_decennie,
    }
    return render(request, 'core/pages/statistiques.html', context)


# ================================================================
# 10. VUES D'ADMINISTRATION (CRUD)
# ================================================================

# ---------- CRUD ETAPES ----------
@login_required
def admin_etapes(request):
    """Liste des étapes pour l'administration."""
    etapes = EtapeProjet.objects.all().order_by('-date_debut')
    return render(request, 'core/admin/etapes_liste.html', {'etapes': etapes})


@login_required
def admin_etape_ajouter(request):
    """Ajouter une nouvelle étape."""
    if request.method == 'POST':
        form = EtapeProjetForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Étape ajoutée avec succès !")
            return redirect('admin_etapes')
    else:
        form = EtapeProjetForm()
    return render(request, 'core/admin/etape_form.html', {'form': form, 'action': 'Ajouter'})


@login_required
def admin_etape_modifier(request, etape_id):
    """Modifier une étape existante."""
    etape = get_object_or_404(EtapeProjet, id=etape_id)
    if request.method == 'POST':
        form = EtapeProjetForm(request.POST, instance=etape)
        if form.is_valid():
            form.save()
            messages.success(request, "Étape modifiée avec succès !")
            return redirect('admin_etapes')
    else:
        form = EtapeProjetForm(instance=etape)
    return render(request, 'core/admin/etape_form.html', {'form': form, 'action': 'Modifier'})


@login_required
def admin_etape_supprimer(request, etape_id):
    """Supprimer une étape."""
    etape = get_object_or_404(EtapeProjet, id=etape_id)
    if request.method == 'POST':
        etape.delete()
        messages.success(request, "Étape supprimée avec succès !")
        return redirect('admin_etapes')
    return render(request, 'core/admin/etape_confirm_delete.html', {'etape': etape})


# ---------- CRUD ACTEURS ----------
@login_required
def admin_acteurs(request):
    acteurs = Acteur.objects.all().order_by('nom')
    return render(request, 'core/admin/acteurs_liste.html', {'acteurs': acteurs})


@login_required
def admin_acteur_ajouter(request):
    if request.method == 'POST':
        form = ActeurForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Acteur ajouté avec succès !")
            return redirect('admin_acteurs')
    else:
        form = ActeurForm()
    return render(request, 'core/admin/acteur_form.html', {'form': form, 'action': 'Ajouter'})


@login_required
def admin_acteur_modifier(request, acteur_id):
    acteur = get_object_or_404(Acteur, id=acteur_id)
    if request.method == 'POST':
        form = ActeurForm(request.POST, instance=acteur)
        if form.is_valid():
            form.save()
            messages.success(request, "Acteur modifié avec succès !")
            return redirect('admin_acteurs')
    else:
        form = ActeurForm(instance=acteur)
    return render(request, 'core/admin/acteur_form.html', {'form': form, 'action': 'Modifier'})


@login_required
def admin_acteur_supprimer(request, acteur_id):
    acteur = get_object_or_404(Acteur, id=acteur_id)
    if request.method == 'POST':
        acteur.delete()
        messages.success(request, "Acteur supprimé avec succès !")
        return redirect('admin_acteurs')
    return render(request, 'core/admin/acteur_confirm_delete.html', {'acteur': acteur})


# ---------- CRUD EVENEMENTS ----------
@login_required
def admin_evenements(request):
    evenements = Evenement.objects.all().order_by('-date_evenement')
    return render(request, 'core/admin/evenements_liste.html', {'evenements': evenements})


@login_required
def admin_evenement_ajouter(request):
    if request.method == 'POST':
        form = EvenementForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Événement ajouté avec succès !")
            return redirect('admin_evenements')
    else:
        form = EvenementForm()
    return render(request, 'core/admin/evenement_form.html', {'form': form, 'action': 'Ajouter'})


@login_required
def admin_evenement_modifier(request, evenement_id):
    evenement = get_object_or_404(Evenement, id=evenement_id)
    if request.method == 'POST':
        form = EvenementForm(request.POST, instance=evenement)
        if form.is_valid():
            form.save()
            messages.success(request, "Événement modifié avec succès !")
            return redirect('admin_evenements')
    else:
        form = EvenementForm(instance=evenement)
    return render(request, 'core/admin/evenement_form.html', {'form': form, 'action': 'Modifier'})


@login_required
def admin_evenement_supprimer(request, evenement_id):
    evenement = get_object_or_404(Evenement, id=evenement_id)
    if request.method == 'POST':
        evenement.delete()
        messages.success(request, "Événement supprimé avec succès !")
        return redirect('admin_evenements')
    return render(request, 'core/admin/evenement_confirm_delete.html', {'evenement': evenement})


# ---------- CRUD DOCUMENTS ----------
@login_required
def admin_documents(request):
    documents = Document.objects.all().order_by('-date_publication')
    return render(request, 'core/admin/documents_liste.html', {'documents': documents})


@login_required
def admin_document_ajouter(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Document ajouté avec succès !")
            return redirect('admin_documents')
    else:
        form = DocumentForm()
    return render(request, 'core/admin/document_form.html', {'form': form, 'action': 'Ajouter'})


@login_required
def admin_document_modifier(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            messages.success(request, "Document modifié avec succès !")
            return redirect('admin_documents')
    else:
        form = DocumentForm(instance=document)
    return render(request, 'core/admin/document_form.html', {'form': form, 'action': 'Modifier'})


@login_required
def admin_document_supprimer(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    if request.method == 'POST':
        document.delete()
        messages.success(request, "Document supprimé avec succès !")
        return redirect('admin_documents')
    return render(request, 'core/admin/document_confirm_delete.html', {'document': document})


# ================================================================
# 11. VUES D'AUTHENTIFICATION
# ================================================================
def login_view(request):
    """Page de connexion."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Bienvenue {user.username} !")
            return redirect('dashboard')
        else:
            messages.error(request, "Identifiants incorrects.")
    return render(request, 'registration/login.html')


def logout_view(request):
    """Déconnexion."""
    logout(request)
    messages.success(request, "Vous êtes déconnecté.")
    return redirect('dashboard')


def register_view(request):
    """Inscription d'un nouvel utilisateur."""
    from django.contrib.auth.forms import UserCreationForm
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Compte créé avec succès !")
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})