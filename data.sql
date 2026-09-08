-- ================================================================
-- PEUPLEMENT DE LA BASE DE DONNÉES
-- DONNÉES HISTORIQUES DU PROJET GRAND INGA
-- ================================================================

-- ----- Insertion du projet -----
INSERT INTO projet (
    nom, description, capacite_prevue, investissement_estime, 
    statut_actuel, date_debut_projet, date_fin_prevue,
    localisation, coordonnees_gps, maitre_ouvrage,
    hauteur_chute, nombre_turbines, type_turbines
) VALUES (
    'Grand Inga',
    'Mégaprojet hydroélectrique sur le fleuve Congo, en RDC',
    39000,
    80000000000,
    'En projet',
    '1925-01-01',
    NULL,
    'Site d''Inga, Kongo Central, RDC',
    '-5.5242, 13.6205',
    'Gouvernement congolais',
    155,
    NULL,
    'Francis'
);

-- ----- Insertion des étapes -----
INSERT INTO etape_projet (nom, description, date_debut, date_fin, statut, objectifs, resultats, responsable_etape, id_projet) VALUES
('Plan Van Deuren', 'Présentation du plan de 7 barrages par le colonel Pierre Van Deuren au roi Albert Ier', '1925-01-01', '1928-12-31', 'achevée', 'Faire du Congo belge la première puissance énergétique d''Afrique', 'Plan non réalisé en raison de la crise de 1929', 'Pierre Van Deuren', 1),
('Construction Inga I', 'Construction du premier barrage sur le site d''Inga', '1968-01-01', '1972-12-31', 'achevée', 'Fournir de l''électricité à l''industrie et aux mines', '351 MW installés', 'Régime Mobutu', 1),
('Construction Inga II', 'Construction du deuxième barrage sur le site d''Inga', '1974-01-01', '1982-12-31', 'achevée', 'Augmenter la capacité de production', '1 424 MW installés', 'Régime Mobutu', 1),
('Engagement Afrique du Sud', 'L''Afrique du Sud s''engage à acheter la moitié de la production', '2013-01-01', '2013-12-31', 'achevée', 'Garantir la viabilité financière du projet', 'Engagement signé', 'Afrique du Sud', 1),
('Suspension Banque mondiale', 'La Banque mondiale suspend son financement', '2016-01-01', '2016-12-31', 'achevée', 'Désaccord avec le gouvernement congolais', 'Financement suspendu', 'Banque mondiale', 1),
('Désignation Three Gorges', 'Le géant chinois Three Gorges Corporation est désigné mandataire', '2017-06-01', '2017-12-31', 'achevée', 'Piloter le projet', 'Three Gorges désignée', 'Three Gorges Corporation', 1),
('Désignation Fortescue', 'Le groupe australien Fortescue Metals Group est désigné', '2021-06-01', NULL, 'en cours', 'Réaliser le projet en PPP', 'Fortescue désignée', 'Fortescue Metals Group', 1);

-- ----- Insertion des acteurs -----
INSERT INTO acteur (nom, type_acteur, categorie, pays, description, date_creation) VALUES
('Pierre Van Deuren', 'Personnalité politique', 'Personne physique', 'Belgique', 'Colonel belge, initiateur du premier plan pour le site d''Inga en 1925', NULL),
('Mobutu Sese Seko', 'Personnalité politique', 'Personne physique', 'RDC', 'Président de la RDC, initiateur de la construction d''Inga I et II', NULL),
('SNEL', 'Entreprise publique', 'Personne morale', 'RDC', 'Société Nationale d''Électricité, gestionnaire des barrages d''Inga I et II', '1970-01-01'),
('Banque mondiale', 'Institution financière', 'Personne morale', 'International', 'Institution financière internationale, financeur du projet', '1944-01-01'),
('Three Gorges Corporation', 'Entreprise', 'Personne morale', 'Chine', 'Gestionnaire du barrage des Trois-Gorges, mandataire du Grand Inga', '1993-01-01'),
('Fortescue Metals Group', 'Entreprise', 'Personne morale', 'Australie', 'Groupe minier australien, mandataire du Grand Inga depuis 2021', '2003-01-01');

-- ----- Insertion des événements -----
INSERT INTO evenement (titre, description, date_evenement, type_evenement, importance, source, id_projet) VALUES
('Plan Van Deuren présenté au roi Albert Ier', 'Le colonel Pierre Van Deuren présente un plan ambitieux de 7 barrages sur le site d''Inga', '1925-01-01', 'politique', 5, 'Archives coloniales belges', 1),
('Mise en service d''Inga I', 'Le premier barrage d''Inga entre en service avec une capacité de 351 MW', '1972-12-31', 'technique', 4, 'Rapports SNEL', 1),
('Mise en service d''Inga II', 'Le deuxième barrage d''Inga entre en service avec une capacité de 1 424 MW', '1982-12-31', 'technique', 4, 'Rapports SNEL', 1),
('Engagement de l''Afrique du Sud', 'L''Afrique du Sud s''engage à acheter plus de la moitié de la production du Grand Inga', '2013-01-01', 'diplomatique', 5, 'Presse internationale', 1),
('Suspension du financement de la Banque mondiale', 'La Banque mondiale suspend son financement en raison de désaccords avec le gouvernement congolais', '2016-01-01', 'financier', 5, 'Banque mondiale', 1),
('Désignation de Three Gorges Corporation', 'Three Gorges Corporation est désignée mandataire du projet', '2017-06-01', 'politique', 4, 'Presse internationale', 1),
('Désignation de Fortescue Metals Group', 'Fortescue Metals Group est désignée pour réaliser le projet en PPP', '2021-06-01', 'politique', 4, 'Presse internationale', 1);