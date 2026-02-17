CREATE TABLE tracking (
    id VARCHAR(50) PRIMARY KEY
);

INSERT INTO tracking (id) VALUES ('ogAZZfxtOKUELbuJ');

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Le mot de passe à voler via l'erreur
INSERT INTO users (username, password) VALUES 
('administrator', 'postgres_error_leaks_secrets');