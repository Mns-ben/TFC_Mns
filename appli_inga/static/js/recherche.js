/* ================================================================
   OBSERVATOIRE GRAND INGA - RECHERCHE ET FILTRES
   Fichier : static/js/recherche.js
   Rôle : Filtrage dynamique des listes (acteurs, événements, documents)
   ================================================================ */

(function() {
    'use strict';

    // ============================================================
    // 1. Filtrage côté client (démonstration)
    // ============================================================
    function initClientFilter() {
        const searchInput = document.querySelector('.search-bar input[type="text"]');
        if (!searchInput) return;

        // Cibler les éléments à filtrer
        const items = document.querySelectorAll('.acteur-card, .table-wrap tbody tr');
        if (!items.length) return;

        searchInput.addEventListener('input', function() {
            const query = this.value.toLowerCase().trim();

            items.forEach(item => {
                const text = item.textContent.toLowerCase();
                if (query === '' || text.includes(query)) {
                    item.style.display = '';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    }

    // ============================================================
    // 2. Réinitialisation des filtres
    // ============================================================
    function initResetFilter() {
        const resetBtn = document.getElementById('resetFilter');
        if (!resetBtn) return;

        resetBtn.addEventListener('click', function() {
            const inputs = document.querySelectorAll('.search-bar input, .search-bar select');
            inputs.forEach(input => {
                if (input.tagName === 'SELECT') {
                    input.selectedIndex = 0;
                } else {
                    input.value = '';
                }
            });

            // Réafficher tous les éléments
            document.querySelectorAll('.acteur-card, .table-wrap tbody tr').forEach(item => {
                item.style.display = '';
            });
        });
    }

    // ============================================================
    // 3. Compteur de résultats
    // ============================================================
    function initResultCount() {
        const searchInput = document.querySelector('.search-bar input[type="text"]');
        const countContainer = document.getElementById('resultCount');
        if (!searchInput || !countContainer) return;

        searchInput.addEventListener('input', function() {
            const visibleItems = document.querySelectorAll(
                '.acteur-card:not([style*="display: none"]), .table-wrap tbody tr:not([style*="display: none"])'
            );
            countContainer.textContent = `${visibleItems.length} résultat(s)`;
        });
    }

    // ============================================================
    // INITIALISATION
    // ============================================================
    document.addEventListener('DOMContentLoaded', function() {
        initClientFilter();
        initResetFilter();
        initResultCount();

        console.log('✅ Recherche et filtres initialisés');
    });

})();