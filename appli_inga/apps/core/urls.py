# ================================================================
# ROUTES DE L'APPLICATION CORE
# Application : core
# Fichier : urls.py
# ================================================================

from django.urls import path

from . import views

urlpatterns = [
    # ================================================================
    # PAGES PUBLIQUES (Consultation)
    # ================================================================
    path('', views.dashboard, name='dashboard'),
    path('chronologie/', views.chronologie, name='chronologie'),
    path('acteurs/', views.acteurs, name='acteurs'),
    path('acteurs/<int:acteur_id>/', views.acteur_detail, name='acteur_detail'),
    path('evenements/', views.evenements, name='evenements'),
    path('evenements/<int:evenement_id>/', views.evenement_detail, name='evenement_detail'),
    path('documents/', views.documents, name='documents'),
    path('carte/', views.carte, name='carte'),
    path('statistiques/', views.statistiques, name='statistiques'),

    # ================================================================
    # AUTHENTIFICATION
    # ================================================================
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

        # ⚠️ ADMINISTRATION - C'est ICI que ça doit être ⚠️
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    path('admin/etapes/', views.admin_etapes, name='admin_etapes'),
    path('admin/etapes/ajouter/', views.admin_etape_ajouter, name='admin_etape_ajouter'),
    path('admin/etapes/<int:etape_id>/modifier/', views.admin_etape_modifier, name='admin_etape_modifier'),
    path('admin/etapes/<int:etape_id>/supprimer/', views.admin_etape_supprimer, name='admin_etape_supprimer'),
    
    path('admin/acteurs/', views.admin_acteurs, name='admin_acteurs'),
    path('admin/acteurs/ajouter/', views.admin_acteur_ajouter, name='admin_acteur_ajouter'),
    path('admin/acteurs/<int:acteur_id>/modifier/', views.admin_acteur_modifier, name='admin_acteur_modifier'),
    path('admin/acteurs/<int:acteur_id>/supprimer/', views.admin_acteur_supprimer, name='admin_acteur_supprimer'),
    
    path('admin/evenements/', views.admin_evenements, name='admin_evenements'),
    path('admin/evenements/ajouter/', views.admin_evenement_ajouter, name='admin_evenement_ajouter'),
    path('admin/evenements/<int:evenement_id>/modifier/', views.admin_evenement_modifier, name='admin_evenement_modifier'),
    path('admin/evenements/<int:evenement_id>/supprimer/', views.admin_evenement_supprimer, name='admin_evenement_supprimer'),
    
    path('admin/documents/', views.admin_documents, name='admin_documents'),
    path('admin/documents/ajouter/', views.admin_document_ajouter, name='admin_document_ajouter'),
    path('admin/documents/<int:document_id>/modifier/', views.admin_document_modifier, name='admin_document_modifier'),
    path('admin/documents/<int:document_id>/supprimer/', views.admin_document_supprimer, name='admin_document_supprimer'),
]
