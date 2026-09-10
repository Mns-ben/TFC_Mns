"""
Configuration des URLs principales du projet appli_inga.

Ce fichier redirige les requêtes vers :
- L'administration Django native (django-admin/)
- Les URLs de l'application core (dashboard, chronologie, etc.)
"""

from django.conf import settings
from django.conf.urls.static import static  # ✅ Import corrigé
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Administration Django native (superuser)
    path('django-admin/', admin.site.urls),

    # URLs de l'application core (dashboard, chronologie, etc.)
    path('', include('apps.core.urls')),
]

# Servir les fichiers statiques et médias en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)