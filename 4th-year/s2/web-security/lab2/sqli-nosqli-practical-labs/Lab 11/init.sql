CREATE TABLE IF NOT EXISTS tracking (
    id VARCHAR(50) PRIMARY KEY
);

INSERT INTO tracking (id) VALUES ('xyz');

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Mot de passe de l'admin (20 caractères alphanumériques comme dans le lab)
INSERT INTO users (username, password) VALUES 
('administrator', 'j98b23c71a32f5e8d90z');

-- SUPPRIMÉ : La table DUAL existe déjà dans MySQL, pas besoin de la créer !
-- CREATE TABLE IF NOT EXISTS dual ...