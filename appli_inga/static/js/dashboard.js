/* ================================================================
   OBSERVATOIRE GRAND INGA - DASHBOARD
   Fichier : static/js/dashboard.js
   Rôle : Animations et interactions du tableau de bord
   ================================================================ */

(function() {
    'use strict';

    const statsGrid = document.getElementById('statsGrid');
    if (!statsGrid) return;

    // ============================================================
    // 1. Animation d'apparition des statistiques
    // ============================================================
    function animateStats() {
        const cards = document.querySelectorAll('.stat-card');
        cards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                card.style.transition = 'opacity 0.4s, transform 0.4s';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, index * 100);
        });
    }

    // ============================================================
    // 2. Animation des barres de graphiques
    // ============================================================
    function animateCharts() {
        const bars = document.querySelectorAll('.chart-box .bar');
        bars.forEach((bar, index) => {
            const finalHeight = bar.style.height;
            bar.style.height = '0px';
            
            setTimeout(() => {
                bar.style.transition = 'height 0.6s ease-out';
                bar.style.height = finalHeight;
            }, index * 80);
        });
    }

    // ============================================================
    // 3. Compteur animé pour les nombres
    // ============================================================
    function animateCounters() {
        const numbers = document.querySelectorAll('.stat-card .number');
        numbers.forEach(num => {
            const target = parseInt(num.textContent, 10);
            if (isNaN(target)) return;
            
            let current = 0;
            const increment = Math.ceil(target / 20);
            const timer = setInterval(() => {
                current += increment;
                if (current >= target) {
                    current = target;
                    clearInterval(timer);
                }
                num.textContent = current;
            }, 30);
        });
    }

    // ============================================================
    // INITIALISATION
    // ============================================================
    document.addEventListener('DOMContentLoaded', function() {
        setTimeout(() => {
            animateStats();
            animateCharts();
            animateCounters();
        }, 200);

        console.log('✅ Dashboard animé');
    });

})();