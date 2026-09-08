-- ================================================================
-- SCRIPT DE CRÉATION DE LA BASE DE DONNÉES
-- OBSERVATOIRE HISTORIQUE DU PROJET GRAND INGA
-- PostgreSQL 15+
-- ================================================================

-- ================================================================
-- 1. CRÉATION DES TABLES (dans l'ordre des dépendances)
-- ================================================================

-- ----- Table ROLE (pas de dépendance) -----
CREATE TABLE IF NOT EXISTS role (
    id_role             SERIAL PRIMARY KEY,
    nom                 VARCHAR(50) NOT NULL UNIQUE,
    description         TEXT
);

-- ----- Table PROJET (pas de dépendance) -----
CREATE TABLE IF NOT EXISTS projet (
    id_projet           SERIAL PRIMARY KEY,
    nom                 VARCHAR(100) NOT NULL,
    description         TEXT,
    capacite_prevue     DECIMAL(15,2),
    investissement_estime DECIMAL(20,2),
    statut_actuel       VARCHAR(50),
    date_debut_projet   DATE,
    date_fin_prevue     DATE,
    localisation        VARCHAR(255),
    coordonnees_gps     VARCHAR(50),
    maitre_ouvrage      VARCHAR(200),
    hauteur_chute       DECIMAL(10,2),
    nombre_turbines     INT,
    type_turbines       VARCHAR(100)
);

-- ----- Table ACTEUR (pas de dépendance) -----
CREATE TABLE IF NOT EXISTS acteur (
    id_acteur           SERIAL PRIMARY KEY,
    nom                 VARCHAR(100) NOT NULL,
    type_acteur         VARCHAR(50),
    categorie           VARCHAR(50),
    pays                VARCHAR(100),
    description         TEXT,
    site_web            VARCHAR(255),
    date_creation       DATE,
    date_disparition    DATE
);

-- ----- Table ETAPE_PROJET (dépend : PROJET) -----
CREATE TABLE IF NOT EXISTS etape_projet (
    id_etape            SERIAL PRIMARY KEY,
    nom                 VARCHAR(100) NOT NULL,
    description         TEXT,
    date_debut          DATE NOT NULL,
    date_fin            DATE,
    statut              VARCHAR(50),
    objectifs           TEXT,
    resultats           TEXT,
    responsable_etape   VARCHAR(200),
    id_projet           INT NOT NULL,
    
    FOREIGN KEY (id_projet) REFERENCES projet(id_projet) ON DELETE CASCADE
);

-- ----- Table EVENEMENT (dépend : PROJET) -----
CREATE TABLE IF NOT EXISTS evenement (
    id_evenement        SERIAL PRIMARY KEY,
    titre               VARCHAR(200) NOT NULL,
    description         TEXT,
    date_evenement      DATE NOT NULL,
    type_evenement      VARCHAR(50),
    importance          INT CHECK (importance BETWEEN 1 AND 5),
    source              VARCHAR(255),
    localisation        VARCHAR(255),
    id_projet           INT NOT NULL,
    
    FOREIGN KEY (id_projet) REFERENCES projet(id_projet) ON DELETE CASCADE
);

-- ----- Table DOCUMENT (dépend : PROJET) -----
CREATE TABLE IF NOT EXISTS document (
    id_document         SERIAL PRIMARY KEY,
    titre               VARCHAR(255) NOT NULL,
    type_document       VARCHAR(50),
    date_publication    DATE,
    auteur              VARCHAR(200),
    resume              TEXT,
    url                 VARCHAR(255),
    chemin_fichier      VARCHAR(255),
    mots_cles           VARCHAR(255),
    etat_conservation   VARCHAR(50),
    id_projet           INT NOT NULL,
    
    FOREIGN KEY (id_projet) REFERENCES projet(id_projet) ON DELETE CASCADE
);

-- ----- Table IMPACT_ACTEUR (dépend : ACTEUR, ETAPE_PROJET) -----
CREATE TABLE IF NOT EXISTS impact_acteur (
    id_impact_acteur    SERIAL PRIMARY KEY,
    type_impact         VARCHAR(50) NOT NULL,
    description         TEXT,
    date_impact         DATE,
    importance          INT CHECK (importance BETWEEN 1 AND 5),
    consequences        TEXT,
    id_acteur           INT NOT NULL,
    id_etape            INT,
    
    FOREIGN KEY (id_acteur) REFERENCES acteur(id_acteur) ON DELETE CASCADE,
    FOREIGN KEY (id_etape) REFERENCES etape_projet(id_etape) ON DELETE SET NULL
);

-- ----- Table IMPACT_ENVIRONNEMENTAL_SOCIAL (dépend : PROJET, ETAPE_PROJET) -----
CREATE TABLE IF NOT EXISTS impact_environnemental_social (
    id_impact_es        SERIAL PRIMARY KEY,
    type_impact         VARCHAR(50) NOT NULL,
    description         TEXT,
    date_impact         DATE,
    surface_ennoyee     DECIMAL(15,2),
    volume_reservoir    DECIMAL(15,2),
    population_deplacee INT,
    bilan_carbone       DECIMAL(15,2),
    importance          INT CHECK (importance BETWEEN 1 AND 5),
    id_projet           INT NOT NULL,
    id_etape            INT,
    
    FOREIGN KEY (id_projet) REFERENCES projet(id_projet) ON DELETE CASCADE,
    FOREIGN KEY (id_etape) REFERENCES etape_projet(id_etape) ON DELETE SET NULL
);

-- ----- Table ACTEUR_EVENEMENT (dépend : ACTEUR, EVENEMENT) -----
CREATE TABLE IF NOT EXISTS acteur_evenement (
    id_acteur_evenement SERIAL PRIMARY KEY,
    role                VARCHAR(100),
    id_acteur           INT NOT NULL,
    id_evenement        INT NOT NULL,
    
    FOREIGN KEY (id_acteur) REFERENCES acteur(id_acteur) ON DELETE CASCADE,
    FOREIGN KEY (id_evenement) REFERENCES evenement(id_evenement) ON DELETE CASCADE,
    CONSTRAINT unique_acteur_evenement UNIQUE (id_acteur, id_evenement)
);

-- ----- Table UTILISATEUR (dépend : ROLE) -----
CREATE TABLE IF NOT EXISTS utilisateur (
    id_utilisateur      SERIAL PRIMARY KEY,
    nom                 VARCHAR(100) NOT NULL,
    email               VARCHAR(100) NOT NULL UNIQUE,
    mot_de_passe        VARCHAR(255) NOT NULL,
    date_creation       DATE DEFAULT CURRENT_DATE,
    id_role             INT NOT NULL,
    
    FOREIGN KEY (id_role) REFERENCES role(id_role) ON DELETE RESTRICT
);

-- ----- Table CHRONOLOGIE (indépendante) -----
CREATE TABLE IF NOT EXISTS chronologie (
    id_chronologie      SERIAL PRIMARY KEY,
    date_debut          DATE,
    date_fin            DATE,
    description         TEXT NOT NULL,
    date_lancement_travaux DATE,
    date_mise_service   DATE,
    duree_vie           VARCHAR(50),
    type_entree         VARCHAR(50)
);

-- ================================================================
-- 2. AJOUT DES CONTRAINTES SUPPLÉMENTAIRES
-- ================================================================

-- Contrainte de dates pour ETAPE_PROJET
ALTER TABLE etape_projet ADD CONSTRAINT check_dates_etape 
    CHECK (date_debut < date_fin OR date_fin IS NULL);

-- Contrainte de dates pour CHRONOLOGIE
ALTER TABLE chronologie ADD CONSTRAINT check_dates_chrono 
    CHECK (date_debut < date_fin OR date_fin IS NULL);

-- ================================================================
-- 3. CRÉATION DES INDEX POUR OPTIMISATION
-- ================================================================

-- Index sur les clés étrangères
CREATE INDEX idx_etape_projet_id_projet ON etape_projet (id_projet);
CREATE INDEX idx_evenement_id_projet ON evenement (id_projet);
CREATE INDEX idx_document_id_projet ON document (id_projet);
CREATE INDEX idx_impact_acteur_id_acteur ON impact_acteur (id_acteur);
CREATE INDEX idx_impact_acteur_id_etape ON impact_acteur (id_etape);
CREATE INDEX idx_impact_es_id_projet ON impact_environnemental_social (id_projet);
CREATE INDEX idx_impact_es_id_etape ON impact_environnemental_social (id_etape);
CREATE INDEX idx_acteur_evenement_id_acteur ON acteur_evenement (id_acteur);
CREATE INDEX idx_acteur_evenement_id_evenement ON acteur_evenement (id_evenement);
CREATE INDEX idx_utilisateur_id_role ON utilisateur (id_role);

-- Index pour les recherches fréquentes
CREATE INDEX idx_evenement_date ON evenement (date_evenement);
CREATE INDEX idx_evenement_type ON evenement (type_evenement);
CREATE INDEX idx_acteur_nom ON acteur (nom);
CREATE INDEX idx_acteur_type ON acteur (type_acteur);
CREATE INDEX idx_etape_projet_date_debut ON etape_projet (date_debut);
CREATE INDEX idx_document_date_publication ON document (date_publication);
CREATE INDEX idx_document_mots_cles ON document USING GIN (to_tsvector('french', mots_cles));

-- ================================================================
-- 4. COMMENTAIRES SUR LES TABLES (documentation)
-- ================================================================

COMMENT ON TABLE projet IS 'Informations générales du projet Grand Inga';
COMMENT ON TABLE etape_projet IS 'Étapes historiques du projet (études, constructions, décisions)';
COMMENT ON TABLE acteur IS 'Personnes et organisations impliquées dans le projet';
COMMENT ON TABLE impact_acteur IS 'Impacts des acteurs sur l évolution du projet';
COMMENT ON TABLE impact_environnemental_social IS 'Impacts environnementaux et sociaux du projet';
COMMENT ON TABLE evenement IS 'Événements marquants du projet (accords, suspensions, annonces)';
COMMENT ON TABLE acteur_evenement IS 'Table de liaison entre acteurs et événements';
COMMENT ON TABLE document IS 'Documents, rapports, études et archives liés au projet';
COMMENT ON TABLE chronologie IS 'Frise chronologique du projet (vue synthétique)';
COMMENT ON TABLE utilisateur IS 'Utilisateurs de l observatoire';
COMMENT ON TABLE role IS 'Profils d accès des utilisateurs (RBAC)';