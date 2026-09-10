/* ================================================================
   OBSERVATOIRE GRAND INGA - SCRIPT PRINCIPAL
   Fichier : static/js/main.js
   Rôle : Interactions générales (frise, acteurs, liens, messages)
   ================================================================ */

(function() {
    'use strict';

    // ============================================================
    // 1. FRISE CHRONOLOGIQUE : clic sur un point
    // ============================================================
    function initFrise() {
        const points = document.querySelectorAll('.frise-point');
        if (!points.length) return;

        points.forEach(point => {
            point.addEventListener('click', function() {
                const titre = this.querySelector('.titre')?.textContent || 'Événement';
                const annee = this.querySelector('.annee')?.textContent || '';
                const id = this.dataset.id;
                const type = this.dataset.type;

                // Afficher un message (à remplacer par une modale plus tard)
                alert(`Détails : ${titre} (${annee})\nType : ${type}`);
                
                // Optionnel : rediriger vers une page de détail
                // if (id && type === 'evenement') {
                //     window.location.href = `/evenements/${id}/`;
                // }
            });
        });
    }

    // ============================================================
    // 2. CARTES ACTEURS : clic pour voir la fiche
    // ============================================================
    function initActeurs() {
        const cards = document.querySelectorAll('.acteur-card');
        if (!cards.length) return;

        cards.forEach(card => {
            card.addEventListener('click', function() {
                const id = this.dataset.id;
                const nom = this.querySelector('.nom')?.textContent || 'Acteur';
                
                // Rediriger vers la fiche détaillée
                if (id) {
                    window.location.href = `/acteurs/${id}/`;
                } else {
                    alert(`Fiche détaillée de : ${nom}`);
                }
            });
        });
    }

    // ============================================================
    // 3. LIENS DANS LES TABLEAUX
    // ============================================================
   // ============================================================
// 3. LIENS DANS LES TABLEAUX
// ============================================================
function initTableLinks() {
    const links = document.querySelectorAll('.table-wrap .link');
    if (!links.length) return;

    links.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            // Si le lien a un vrai href (autre que "#"), on le laisse passer
            if (href && href !== '#' && href !== '') {
                // Ne pas bloquer, le navigateur suit le lien
                return;
            }
            
            // Sinon, on bloque
            e.preventDefault();
            const action = this.dataset.action || 'Action non définie';
            alert(action);
        });
    });
}
    // ============================================================
    // 4. BOUTONS GÉNÉRIQUES (non spécifiques à la carte)
    // ============================================================
    function initButtons() {
        const buttons = document.querySelectorAll('.btn:not(.btn-no-alert)');
        if (!buttons.length) return;

        buttons.forEach(btn => {
            // Ignorer les boutons de la carte (gérés par carte.js)
            if (btn.closest('.carte-controls')) return;
            // Ignorer les liens normaux
            if (btn.tagName === 'A') return;

            btn.addEventListener('click', function(e) {
                // Si le bouton a un type submit, laisser faire
                if (this.type === 'submit') return;
                
                // Sinon, comportement par défaut
                const action = this.dataset.action;
                if (action === 'export-pdf') {
                    e.preventDefault();
                    alert('Export PDF en cours de développement...');
                } else if (action === 'export-csv') {
                    e.preventDefault();
                    alert('Export CSV en cours de développement...');
                } else if (action) {
                    e.preventDefault();
                    alert(`Action : ${action}`);
                }
            });
        });
    }

    // ============================================================
    // 5. MESSAGES DJANGO (auto-dismiss après 5 secondes)
    // ============================================================
    function initMessages() {
        const messages = document.querySelectorAll('.alert, .messages .alert');
        if (!messages.length) return;

        messages.forEach(msg => {
            setTimeout(() => {
                msg.style.transition = 'opacity 0.5s';
                msg.style.opacity = '0';
                setTimeout(() => msg.remove(), 500);
            }, 5000);
        });
    }

    // ============================================================
    // 6. RECHERCHE : soumission automatique
    // ============================================================
    function initSearchInputs() {
        const searchInputs = document.querySelectorAll('.search-bar input[type="text"]');
        if (!searchInputs.length) return;

        searchInputs.forEach(input => {
            input.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    this.closest('form')?.submit();
                }
            });
        });
    }

    // ============================================================
    // 7. FILTRES : soumission automatique au changement
    // ============================================================
    function initFilters() {
        const selects = document.querySelectorAll('.search-bar select, .frise-filters select');
        if (!selects.length) return;

        selects.forEach(select => {
            select.addEventListener('change', function() {
                // Si dans un formulaire, le soumettre
                const form = this.closest('form');
                if (form) {
                    form.submit();
                }
            });
        });
    }

    // ============================================================
    // 8. NAVIGATION : mise en surbrillance de l'onglet actif
    // ============================================================
    function initActiveNav() {
        const currentPath = window.location.pathname;
        const navLinks = document.querySelectorAll('.app-nav a');
        
        navLinks.forEach(link => {
            const href = link.getAttribute('href');
            if (href && currentPath === href) {
                link.classList.add('active');
            } else if (href && href !== '/' && currentPath.startsWith(href)) {
                link.classList.add('active');
            }
        });
    }

    // ============================================================
    // INITIALISATION GÉNÉRALE
    // ============================================================
    document.addEventListener('DOMContentLoaded', function() {
        initFrise();
        initActeurs();
        initTableLinks();
        initButtons();
        initMessages();
        initSearchInputs();
        initFilters();
        initActiveNav();
        
        console.log('✅ Observatoire Grand Inga - main.js chargé');
    });

})();