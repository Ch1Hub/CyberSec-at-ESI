CREATE TABLE IF NOT EXISTS tracking (
    id VARCHAR(50) PRIMARY KEY
);

-- Un ID de tracking valide que l'utilisateur recevra
INSERT INTO tracking (id) VALUES ('auth_8f93j2k');

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Le mot de passe est en minuscules/chiffres pour faciliter le Brute Force
INSERT INTO users (username, password) VALUES 
('administrator', '7b439c21');