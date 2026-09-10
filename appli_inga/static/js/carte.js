/* ================================================================
   OBSERVATOIRE GRAND INGA - CARTE SIG
   Fichier : static/js/carte.js
   Rôle : Initialisation de la carte ArcGIS
   ================================================================ */

(function() {
    'use strict';

    // ============================================================
    // Vérifier que le conteneur existe (page carte uniquement)
    // ============================================================
    const viewDiv = document.getElementById('viewDiv');
    if (!viewDiv) {
        console.log('ℹ️ Carte non chargée (page non-carte)');
        return;
    }

    // ============================================================
    // Chargement des modules ArcGIS
    // ============================================================
    require([
        "esri/Map",
        "esri/views/MapView",
        "esri/Graphic",
        "esri/layers/GraphicsLayer",
        "esri/geometry/Point",
        "esri/geometry/Polygon"
    ], function(Map, MapView, Graphic, GraphicsLayer, Point, Polygon) {

        // --------------------------------------------------------
        // 1. Coordonnées du site d'Inga
        // --------------------------------------------------------
        const ingaCoords = { lat: -5.5242, lon: 13.6205 };

        // --------------------------------------------------------
        // 2. Création de la carte
        // --------------------------------------------------------
        const map = new Map({
            basemap: "dark-gray-vector"
        });

        const view = new MapView({
            container: "viewDiv",
            map: map,
            center: [ingaCoords.lon, ingaCoords.lat],
            zoom: 10,
            popup: {
                dockEnabled: true,
                dockOptions: {
                    buttonEnabled: false,
                    breakpoint: false
                }
            }
        });

        // --------------------------------------------------------
        // 3. Couche graphique
        // --------------------------------------------------------
        const layer = new GraphicsLayer();
        map.add(layer);

        // --------------------------------------------------------
        // 4. Marqueur principal : Site d'Inga
        // --------------------------------------------------------
        const pointInga = new Point({
            longitude: ingaCoords.lon,
            latitude: ingaCoords.lat
        });

        layer.add(new Graphic({
            geometry: pointInga,
            symbol: {
                type: "simple-marker",
                color: [42, 107, 176],
                outline: { color: [255, 255, 255], width: 2 },
                size: 16,
                style: "circle"
            },
            attributes: { name: "Site d'Inga" },
            popupTemplate: {
                title: "Site d'Inga",
                content: "Complexe hydroélectrique<br><strong>Coordonnées :</strong> 5°31'27''S - 13°37'14''E<br>Capacité potentielle : 40 000+ MW"
            }
        }));

        // --------------------------------------------------------
        // 5. Barrages existants (Inga I et Inga II)
        // --------------------------------------------------------
        const barrages = [
            { lat: -5.5190, lon: 13.6190, nom: "Inga I", cap: "351 MW", annee: 1972 },
            { lat: -5.5280, lon: 13.6220, nom: "Inga II", cap: "1 424 MW", annee: 1982 }
        ];

        barrages.forEach(b => {
            layer.add(new Graphic({
                geometry: new Point({ longitude: b.lon, latitude: b.lat }),
                symbol: {
                    type: "simple-marker",
                    color: [42, 107, 176],
                    outline: { color: [255, 255, 255], width: 2 },
                    size: 12,
                    style: "diamond"
                },
                attributes: b,
                popupTemplate: {
                    title: "{nom}",
                    content: "Puissance : {cap}<br>Mise en service : {annee}"
                }
            }));
        });

        // --------------------------------------------------------
        // 6. Projets futurs (Grand Inga, Bundi)
        // --------------------------------------------------------
        const futurs = [
            { lat: -5.5310, lon: 13.6150, nom: "Grand Inga", cap: "39 000 MW", etat: "Projet" },
            { lat: -5.5270, lon: 13.6280, nom: "Centrale de la Bundi", cap: "39 000 MW", etat: "Projet" }
        ];

        futurs.forEach(b => {
            layer.add(new Graphic({
                geometry: new Point({ longitude: b.lon, latitude: b.lat }),
                symbol: {
                    type: "simple-marker",
                    color: [230, 126, 34],
                    outline: { color: [255, 255, 255], width: 2 },
                    size: 12,
                    style: "triangle"
                },
                attributes: b,
                popupTemplate: {
                    title: "{nom}",
                    content: "Puissance : {cap}<br>Statut : {etat}"
                }
            }));
        });

        // --------------------------------------------------------
        // 7. Zone inondée (polygone simulé)
        // --------------------------------------------------------
        const zonePoints = [
            [13.610, -5.515],
            [13.625, -5.518],
            [13.630, -5.525],
            [13.625, -5.532],
            [13.612, -5.530],
            [13.608, -5.522]
        ];

        layer.add(new Graphic({
            geometry: new Polygon({
                rings: zonePoints,
                spatialReference: { wkid: 4326 }
            }),
            symbol: {
                type: "simple-fill",
                color: [192, 57, 43, 0.25],
                outline: { color: [192, 57, 43], width: 1 }
            },
            popupTemplate: {
                title: "Zone inondée",
                content: "Surface estimée : ~1 500 km²<br>Impact : zones de forêt inondées"
            }
        }));

        // --------------------------------------------------------
        // 8. Populations déplacées
        // --------------------------------------------------------
        layer.add(new Graphic({
            geometry: new Point({ longitude: 13.600, latitude: -5.508 }),
            symbol: {
                type: "simple-marker",
                color: [39, 174, 96, 0.3],
                outline: { color: [39, 174, 96], width: 1 },
                size: 80,
                style: "circle"
            },
            popupTemplate: {
                title: "Populations déplacées",
                content: "Estimées : ~30 000 personnes<br>Communautés impactées"
            }
        }));

        // --------------------------------------------------------
        // 9. Bouton : Zoom sur Inga
        // --------------------------------------------------------
        document.getElementById('btnZoomInga')?.addEventListener('click', function() {
            view.goTo({
                center: [ingaCoords.lon, ingaCoords.lat],
                zoom: 12,
                duration: 1000
            });
        });

        // --------------------------------------------------------
        // 10. Bouton : Afficher/Masquer les barrages
        // --------------------------------------------------------
        document.getElementById('btnLayerBarrages')?.addEventListener('click', function() {
            layer.graphics.forEach(g => {
                if (g.symbol && g.symbol.style === 'diamond') {
                    g.visible = !g.visible;
                }
            });
        });

        // --------------------------------------------------------
        // 11. Bouton : Afficher/Masquer la zone inondée
        // --------------------------------------------------------
        document.getElementById('btnLayerZone')?.addEventListener('click', function() {
            layer.graphics.forEach(g => {
                if (g.geometry && g.geometry.type === 'polygon') {
                    g.visible = !g.visible;
                }
            });
        });

        // --------------------------------------------------------
        // 12. Bouton : Afficher/Masquer les populations
        // --------------------------------------------------------
        document.getElementById('btnLayerPop')?.addEventListener('click', function() {
            layer.graphics.forEach(g => {
                if (g.symbol && g.symbol.style === 'circle' && g.symbol.size === 80) {
                    g.visible = !g.visible;
                }
            });
        });

        // --------------------------------------------------------
        // 13. Exposer view globalement (pour resize)
        // --------------------------------------------------------
        window.view = view;

        // --------------------------------------------------------
        // 14. Redimensionnement
        // --------------------------------------------------------
        setTimeout(() => { view.resize(); }, 500);

        window.addEventListener('resize', function() {
            view.resize();
        });

        console.log('✅ Carte ArcGIS chargée');
    });

})();