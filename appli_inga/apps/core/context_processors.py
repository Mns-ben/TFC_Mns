# ================================================================
# CONTEXT PROCESSORS
# Application : core
# Fichier : context_processors.py
# ================================================================

from .models import Projet


def projet_actif(request):
    """
    Injecte le projet actif dans tous les templates.
    Permet d'accéder à {{ projet_actif }} partout.
    """
    try:
        projet = Projet.objects.first()
    except Exception:
        projet = None
    return {'projet_actif': projet}


def site_info(request):
    """
    Injecte les informations générales du site dans tous les templates.
    """
    return {
        'site_nom': 'Observatoire Grand Inga',
        'site_description': "Observatoire historique et institutionnel du projet Grand Inga",
        'site_version': '1.0',
        'auteur': 'MUNSINGIELE LUPO',
        'annee': '2025-2026',
    }


def user_role(request):
    """
    Injecte le rôle de l'utilisateur connecté dans tous les templates.
    """
    if request.user.is_authenticated:
        return {
            'user_role': getattr(request.user, 'role', 'public'),
            'is_administrateur': getattr(request.user, 'role', '') == 'administrateur',
            'is_chercheur': getattr(request.user, 'role', '') == 'chercheur',
            'is_decideur': getattr(request.user, 'role', '') == 'decideur',
        }
    return {
        'user_role': 'public',
        'is_administrateur': False,
        'is_chercheur': False,
        'is_decideur': False,
    }