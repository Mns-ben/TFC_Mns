# ================================================================
# FILTRES PERSONNALISÉS POUR LES TEMPLATES
# Application : core
# Fichier : templatetags/custom_filters.py
# ================================================================

from django import template

register = template.Library()


# ================================================================
# 1. FILTRES DE TEXTE
# ================================================================

@register.filter
def tronquer(value, longueur=50):
    """Tronque un texte à une longueur donnée."""
    if len(str(value)) > longueur:
        return str(value)[:longueur] + "..."
    return value


@register.filter
def majuscule(value):
    """Met en majuscules."""
    return str(value).upper()


@register.filter
def initiales(value):
    """Retourne les initiales d'un nom (ex: 'Banque Mondiale' → 'BM')."""
    return ''.join([mot[0].upper() for mot in str(value).split() if mot])


# ================================================================
# 2. FILTRES DE COULEUR (pour les badges)
# ================================================================

@register.filter
def couleur_importance(importance):
    """Retourne une classe CSS selon le niveau d'importance."""
    try:
        importance = int(importance)
    except (ValueError, TypeError):
        return 'importance-1'
    return f'importance-{importance}'


@register.filter
def couleur_type_evenement(type_evenement):
    """Retourne une classe CSS pour le badge du type d'événement."""
    mapping = {
        'politique': 'badge-politique',
        'financier': 'badge-financier',
        'technique': 'badge-technique',
        'diplomatique': 'badge-diplomatique',
        'social': 'badge-social',
        'environnemental': 'badge-environnemental',
        'juridique': 'badge-politique',
    }
    return mapping.get(type_evenement, 'badge-politique')


@register.filter
def couleur_type_impact(type_impact):
    """Retourne une classe CSS pour le badge du type d'impact."""
    mapping = {
        'positif': 'badge-technique',
        'negatif': 'badge-social',
        'neutre': 'badge-politique',
        'decisif': 'badge-diplomatique',
        'bloquant': 'badge-financier',
        'facilitateur': 'badge-technique',
    }
    return mapping.get(type_impact, 'badge-politique')


# ================================================================
# 3. FILTRES DE DATE
# ================================================================

@register.filter
def annee_seule(value):
    """Retourne uniquement l'année d'une date."""
    if hasattr(value, 'year'):
        return value.year
    return value


@register.filter
def format_date_fr(value):
    """Formate une date au format JJ/MM/AAAA."""
    if hasattr(value, 'strftime'):
        return value.strftime('%d/%m/%Y')
    return value


@register.filter
def periode(date_debut, date_fin):
    """Affiche une période (ex: '1968-1972' ou '2021-présent')."""
    if date_fin:
        return f"{date_debut.year}-{date_fin.year}"
    return f"{date_debut.year}-présent"


# ================================================================
# 4. FILTRES POUR LES ÉTOILES (importance)
# ================================================================

@register.filter
def etoiles(importance):
    """Affiche des étoiles selon l'importance (1-5)."""
    try:
        n = int(importance)
    except (ValueError, TypeError):
        n = 0
    return '★' * n + '☆' * (5 - n)


# ================================================================
# 5. FILTRES POUR LES NOMBRES
# ================================================================

@register.filter
def format_milliers(value):
    """Formate un nombre avec séparateurs de milliers."""
    try:
        return f"{int(value):,}".replace(',', ' ')
    except (ValueError, TypeError):
        return value


@register.filter
def format_mw(value):
    """Formate une puissance en MW."""
    try:
        return f"{float(value):,.0f} MW".replace(',', ' ')
    except (ValueError, TypeError):
        return f"{value} MW"


# ================================================================
# 6. FILTRES POUR LES MODÈLES
# ================================================================

@register.filter
def get_type_display(obj):
    """Retourne le libellé d'un champ avec choices."""
    if hasattr(obj, 'get_type_impact_display'):
        return obj.get_type_impact_display()
    return obj


@register.filter
def get_field_value(obj, field_name):
    """Retourne la valeur d'un champ d'un objet."""
    return getattr(obj, field_name, None)


# ================================================================
# 7. FILTRES POUR LES DICT
# ================================================================

@register.filter
def get_item(dictionary, key):
    """Accède à une valeur dans un dictionnaire (pour les templates)."""
    if isinstance(dictionary, dict):
        return dictionary.get(key, 0)
    return 0


# ================================================================
# 8. FILTRES POUR LES POURCENTAGES
# ================================================================

@register.filter
def pourcentage(value, total):
    """Calcule un pourcentage."""
    try:
        return round((float(value) / float(total)) * 100, 1)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0