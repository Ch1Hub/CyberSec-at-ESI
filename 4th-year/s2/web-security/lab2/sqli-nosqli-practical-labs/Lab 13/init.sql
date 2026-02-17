CREATE TABLE tracking (
    id VARCHAR(50) PRIMARY KEY
);

INSERT INTO tracking (id) VALUES ('x');

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL
);

INSERT INTO users (username, password) VALUES 
('administrator', 's3cr3t_P@ssw0rd');