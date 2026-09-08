-- ================================================================
-- REQUÊTES SQL POUR L'OBSERVATOIRE HISTORIQUE
-- Projet Grand Inga
-- Auteur : MUNSINGIELE LUPO
-- Version : 1.0
-- ================================================================

-- ================================================================
-- 1. REQUÊTES D'INTERROGATION TYPIQUES
-- ================================================================

-- -----------------------------------------------------------------
-- 1.1 Frise chronologique complète du projet
-- -----------------------------------------------------------------
-- Description : Visualiser l'ensemble des étapes et événements triés par date
-- Utilisation : Interface "Frise chronologique"
-- -----------------------------------------------------------------

SELECT 
    'etape' AS type,
    nom AS titre,
    description,
    date_debut,
    date_fin,
    statut
FROM etape_projet
WHERE id_projet = 1

UNION ALL

SELECT 
    'evenement' AS type,
    titre,
    description,
    date_evenement,
    NULL AS date_fin,
    NULL AS statut
FROM evenement
WHERE id_projet = 1

ORDER BY date_debut NULLS LAST;


-- -----------------------------------------------------------------
-- 1.2 Acteurs ayant eu un impact critique (importance >= 4)
-- -----------------------------------------------------------------
-- Description : Identifier les acteurs les plus influents sur le projet
-- Utilisation : Analyse des acteurs clés
-- -----------------------------------------------------------------

SELECT 
    a.nom,
    a.type_acteur,
    a.pays,
    ia.type_impact,
    ia.description,
    ia.importance,
    ia.date_impact
FROM acteur a
JOIN impact_acteur ia ON a.id_acteur = ia.id_acteur
WHERE ia.importance >= 4
ORDER BY ia.importance DESC, ia.date_impact;


-- -----------------------------------------------------------------
-- 1.3 Événements par période (ex: 1970-1990)
-- -----------------------------------------------------------------
-- Description : Filtrer les événements sur une période donnée
-- Utilisation : Recherche chronologique
-- -----------------------------------------------------------------

SELECT 
    titre,
    description,
    date_evenement,
    type_evenement,
    importance,
    source
FROM evenement
WHERE id_projet = 1
    AND date_evenement BETWEEN '1970-01-01' AND '1990-12-31'
ORDER BY date_evenement;


-- -----------------------------------------------------------------
-- 1.4 Synthèse des impacts environnementaux et sociaux
-- -----------------------------------------------------------------
-- Description : Agréger les impacts environnementaux par type
-- Utilisation : Tableau de bord environnemental
-- -----------------------------------------------------------------

SELECT 
    type_impact,
    SUM(surface_ennoyee) AS surface_totale_ennoyee,
    SUM(volume_reservoir) AS volume_total_reservoir,
    SUM(population_deplacee) AS population_totale_deplacee,
    AVG(importance) AS importance_moyenne
FROM impact_environnemental_social
WHERE id_projet = 1
GROUP BY type_impact
ORDER BY importance_moyenne DESC;


-- -----------------------------------------------------------------
-- 1.5 Recherche de documents par mots-clés (full-text)
-- -----------------------------------------------------------------
-- Description : Recherche plein texte sur les mots-clés des documents
-- Utilisation : Bibliothèque documentaire
-- -----------------------------------------------------------------

SELECT 
    titre,
    auteur,
    date_publication,
    resume,
    mots_cles,
    etat_conservation
FROM document
WHERE id_projet = 1
    AND to_tsvector('french', mots_cles) @@ to_tsquery('french', 'financement & barrage')
ORDER BY date_publication DESC;


-- -----------------------------------------------------------------
-- 1.6 Acteurs et leurs rôles dans les événements
-- -----------------------------------------------------------------
-- Description : Visualiser les relations acteurs-événements
-- Utilisation : Analyse des réseaux d'acteurs
-- -----------------------------------------------------------------

SELECT 
    e.titre AS evenement,
    e.date_evenement,
    a.nom AS acteur,
    ae.role
FROM evenement e
JOIN acteur_evenement ae ON e.id_evenement = ae.id_evenement
JOIN acteur a ON ae.id_acteur = a.id_acteur
WHERE e.id_projet = 1
ORDER BY e.date_evenement;


-- -----------------------------------------------------------------
-- 1.7 Statistiques générales du projet
-- -----------------------------------------------------------------
-- Description : Vue d'ensemble des données du projet
-- Utilisation : Dashboard principal
-- -----------------------------------------------------------------

SELECT 
    (SELECT COUNT(*) FROM etape_projet WHERE id_projet = 1) AS nb_etapes,
    (SELECT COUNT(*) FROM evenement WHERE id_projet = 1) AS nb_evenements,
    (SELECT COUNT(*) FROM acteur) AS nb_acteurs,
    (SELECT COUNT(*) FROM document WHERE id_projet = 1) AS nb_documents,
    (SELECT COUNT(*) FROM impact_acteur) AS nb_impacts_acteurs,
    (SELECT COUNT(*) FROM impact_environnemental_social WHERE id_projet = 1) AS nb_impacts_es;


-- -----------------------------------------------------------------
-- 1.8 Top 5 des événements les plus importants
-- -----------------------------------------------------------------
-- Description : Identifier les événements majeurs
-- Utilisation : Points clés du projet
-- -----------------------------------------------------------------

SELECT 
    titre,
    date_evenement,
    type_evenement,
    importance,
    source
FROM evenement
WHERE id_projet = 1
ORDER BY importance DESC
LIMIT 5;


-- -----------------------------------------------------------------
-- 1.9 Acteurs par pays
-- -----------------------------------------------------------------
-- Description : Répartition géographique des acteurs
-- Utilisation : Analyse géopolitique
-- -----------------------------------------------------------------

SELECT 
    pays,
    type_acteur,
    COUNT(*) AS nb_acteurs
FROM acteur
GROUP BY pays, type_acteur
ORDER BY pays, nb_acteurs DESC;


-- -----------------------------------------------------------------
-- 1.10 Liste des documents par type
-- -----------------------------------------------------------------
-- Description : Inventaire documentaire
-- Utilisation : Gestion des archives
-- -----------------------------------------------------------------

SELECT 
    type_document,
    COUNT(*) AS nb_documents,
    MIN(date_publication) AS plus_ancien,
    MAX(date_publication) AS plus_recent
FROM document
WHERE id_projet = 1
GROUP BY type_document
ORDER BY nb_documents DESC;


-- ================================================================
-- 2. REQUÊTES DE VALIDATION ET TESTS D'INTÉGRITÉ
-- ================================================================

-- -----------------------------------------------------------------
-- 2.1 Test : Vérification des contraintes de dates
-- -----------------------------------------------------------------
-- Vérifie que date_debut < date_fin pour les étapes
-- Résultat attendu : 0 ligne
-- -----------------------------------------------------------------

SELECT id_etape, nom, date_debut, date_fin
FROM etape_projet
WHERE date_fin IS NOT NULL AND date_debut >= date_fin;


-- -----------------------------------------------------------------
-- 2.2 Test : Vérification des contraintes d'importance
-- -----------------------------------------------------------------
-- Vérifie que importance est entre 1 et 5 pour les événements
-- Résultat attendu : 0 ligne
-- -----------------------------------------------------------------

SELECT id_evenement, titre, importance
FROM evenement
WHERE importance NOT BETWEEN 1 AND 5;


-- -----------------------------------------------------------------
-- 2.3 Test : Vérification des clés étrangères
-- -----------------------------------------------------------------
-- Vérifie que toutes les étapes ont un projet valide
-- Résultat attendu : 0 ligne
-- -----------------------------------------------------------------

SELECT id_etape, id_projet
FROM etape_projet
WHERE id_projet NOT IN (SELECT id_projet FROM projet);


-- -----------------------------------------------------------------
-- 2.4 Test : Vérification de l'unicité des emails
-- -----------------------------------------------------------------
-- Vérifie que les emails des utilisateurs sont uniques
-- Résultat attendu : 0 ligne
-- -----------------------------------------------------------------

SELECT email, COUNT(*)
FROM utilisateur
GROUP BY email
HAVING COUNT(*) > 1;


-- -----------------------------------------------------------------
-- 2.5 Test : Vérification des références d'acteurs
-- -----------------------------------------------------------------
-- Vérifie que les impacts d'acteurs référencent des acteurs valides
-- Résultat attendu : 0 ligne
-- -----------------------------------------------------------------

SELECT id_impact_acteur, id_acteur
FROM impact_acteur
WHERE id_acteur NOT IN (SELECT id_acteur FROM acteur);


-- -----------------------------------------------------------------
-- 2.6 Test : Vérification des acteurs impliqués dans les événements
-- -----------------------------------------------------------------
-- Vérifie que les liens acteur-événement sont valides
-- Résultat attendu : 0 ligne
-- -----------------------------------------------------------------

SELECT id_acteur_evenement, id_acteur, id_evenement
FROM acteur_evenement
WHERE id_acteur NOT IN (SELECT id_acteur FROM acteur)
   OR id_evenement NOT IN (SELECT id_evenement FROM evenement);


-- ================================================================
-- 3. REQUÊTES COMPLÉMENTAIRES
-- ================================================================

-- -----------------------------------------------------------------
-- 3.1 Acteurs ayant eu plusieurs impacts
-- -----------------------------------------------------------------
-- Description : Identifier les acteurs les plus actifs
-- -----------------------------------------------------------------

SELECT 
    a.nom,
    COUNT(ia.id_impact_acteur) AS nb_impacts,
    AVG(ia.importance) AS importance_moyenne
FROM acteur a
JOIN impact_acteur ia ON a.id_acteur = ia.id_acteur
GROUP BY a.id_acteur, a.nom
HAVING COUNT(ia.id_impact_acteur) >= 2
ORDER BY nb_impacts DESC;


-- -----------------------------------------------------------------
-- 3.2 Chronologie des étapes et événements (format synthétique)
-- -----------------------------------------------------------------
-- Description : Vue synthétique pour l'affichage
-- -----------------------------------------------------------------

SELECT 
    date_debut AS date,
    '📌 ' || nom AS description
FROM etape_projet
WHERE id_projet = 1

UNION ALL

SELECT 
    date_evenement AS date,
    '⚡ ' || titre AS description
FROM evenement
WHERE id_projet = 1

ORDER BY date;


-- -----------------------------------------------------------------
-- 3.3 Documents récents (5 derniers)
-- -----------------------------------------------------------------
-- Description : Derniers documents ajoutés
-- -----------------------------------------------------------------

SELECT 
    titre,
    auteur,
    date_publication,
    type_document
FROM document
WHERE id_projet = 1
ORDER BY date_publication DESC
LIMIT 5;


-- ================================================================
-- 4. REQUÊTES POUR LE TABLEAU DE BORD
-- ================================================================

-- -----------------------------------------------------------------
-- 4.1 Indicateurs clés du projet
-- -----------------------------------------------------------------

SELECT 
    'Capacité prévue' AS indicateur,
    capacite_prevue || ' MW' AS valeur
FROM projet
WHERE id_projet = 1

UNION ALL

SELECT 
    'Investissement estimé',
    '$ ' || TO_CHAR(investissement_estime, 'FM9,999,999,999')
FROM projet
WHERE id_projet = 1

UNION ALL

SELECT 
    'Statut actuel',
    statut_actuel
FROM projet
WHERE id_projet = 1

UNION ALL

SELECT 
    'Nombre d''étapes',
    COUNT(*)::TEXT
FROM etape_projet
WHERE id_projet = 1

UNION ALL

SELECT 
    'Nombre d''événements',
    COUNT(*)::TEXT
FROM evenement
WHERE id_projet = 1;


-- -----------------------------------------------------------------
-- 4.2 Répartition des événements par type
-- -----------------------------------------------------------------
-- Description : Graphique pour le dashboard
-- -----------------------------------------------------------------

SELECT 
    type_evenement,
    COUNT(*) AS nombre,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS pourcentage
FROM evenement
WHERE id_projet = 1
GROUP BY type_evenement
ORDER BY nombre DESC;


-- -----------------------------------------------------------------
-- 4.3 Évolution temporelle des événements (par décennie)
-- -----------------------------------------------------------------
-- Description : Histogramme pour le dashboard
-- -----------------------------------------------------------------

SELECT 
    EXTRACT(YEAR FROM date_evenement) / 10 * 10 AS decennie,
    COUNT(*) AS nb_evenements
FROM evenement
WHERE id_projet = 1
GROUP BY decennie
ORDER BY decennie;


-- ================================================================
-- FIN DU FICHIER
-- ================================================================