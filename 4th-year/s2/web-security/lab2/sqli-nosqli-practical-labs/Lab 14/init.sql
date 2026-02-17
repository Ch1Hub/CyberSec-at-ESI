CREATE TABLE tracking (
    id VARCHAR(50) PRIMARY KEY
);

INSERT INTO tracking (id) VALUES ('x');

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Le mot de passe cible (12 caractères pour que ce soit faisable en lab)
-- "t1m3_i5_k3y!"
INSERT INTO users (username, password) VALUES 
('administrator', 't1m3_i5_k3y!');