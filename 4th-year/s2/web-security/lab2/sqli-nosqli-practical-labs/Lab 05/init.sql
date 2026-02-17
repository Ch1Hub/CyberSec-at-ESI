-- 1. Table Produits standard
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    category VARCHAR(50),
    description TEXT
);

INSERT INTO products (name, category, description) VALUES
('Oracle Database 19c', 'Software', 'Enterprise Grid Computing'),
('Java SE Subscription', 'Software', 'Long Term Support'),
('SPARC Server', 'Hardware', 'High performance processor');

-- 2. La Table cible (Nom aléatoire comme dans le Lab)
CREATE TABLE USERS_Z9Y1 (
    USERNAME_A1 VARCHAR(50),
    PASSWORD_B2 VARCHAR(50)
);

INSERT INTO USERS_Z9Y1 VALUES ('administrator', '3gg_Sh3ll_0racle_H4ck');
INSERT INTO USERS_Z9Y1 VALUES ('carlos', 'qwerty');


-- ==========================================
-- 3. SIMULATION DES TABLES SYSTÈMES ORACLE
-- ==========================================

-- A. Table DUAL (CORRIGÉ : Ajout des backticks ` ` pour éviter l'erreur MySQL)
CREATE TABLE `dual` (
    dummy VARCHAR(1)
);
INSERT INTO `dual` VALUES ('X');

-- B. Table ALL_TABLES (Liste les tables du système)
CREATE TABLE all_tables (
    owner VARCHAR(50),
    table_name VARCHAR(50)
);

-- On peuple cette table pour qu'elle contienne notre table cachée
INSERT INTO all_tables VALUES ('LAB05', 'PRODUCTS');
INSERT INTO all_tables VALUES ('LAB05', 'USERS_Z9Y1'); -- C'est celle-ci qu'on cherche !
INSERT INTO all_tables VALUES ('SYS', 'DUAL');
INSERT INTO all_tables VALUES ('SYS', 'ALL_TABLES');
INSERT INTO all_tables VALUES ('SYS', 'ALL_TAB_COLUMNS');

-- C. Table ALL_TAB_COLUMNS (Liste les colonnes)
CREATE TABLE all_tab_columns (
    owner VARCHAR(50),
    table_name VARCHAR(50),
    column_name VARCHAR(50),
    data_type VARCHAR(50)
);

-- 1. Colonnes de la table cible (Cachées)
INSERT INTO all_tab_columns VALUES ('LAB05', 'USERS_Z9Y1', 'USERNAME_A1', 'VARCHAR2');
INSERT INTO all_tab_columns VALUES ('LAB05', 'USERS_Z9Y1', 'PASSWORD_B2', 'VARCHAR2');

-- 2. Colonnes de la table publique (Pour que l'étudiant puisse vérifier)
INSERT INTO all_tab_columns VALUES ('LAB05', 'PRODUCTS', 'NAME', 'VARCHAR2');
INSERT INTO all_tab_columns VALUES ('LAB05', 'PRODUCTS', 'DESCRIPTION', 'VARCHAR2');
INSERT INTO all_tab_columns VALUES ('LAB05', 'PRODUCTS', 'CATEGORY', 'VARCHAR2');

-- 3. Colonnes des tables systèmes (Pour permettre l'introspection)
INSERT INTO all_tab_columns VALUES ('SYS', 'ALL_TABLES', 'TABLE_NAME', 'VARCHAR2');
INSERT INTO all_tab_columns VALUES ('SYS', 'ALL_TABLES', 'OWNER', 'VARCHAR2');
INSERT INTO all_tab_columns VALUES ('SYS', 'ALL_TAB_COLUMNS', 'COLUMN_NAME', 'VARCHAR2');
INSERT INTO all_tab_columns VALUES ('SYS', 'ALL_TAB_COLUMNS', 'TABLE_NAME', 'VARCHAR2');