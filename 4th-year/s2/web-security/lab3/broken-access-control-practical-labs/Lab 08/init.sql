CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'user'
);

INSERT INTO users (username, password, role) VALUES 
('administrator', 'ESI_SBA_Adm1n_P@ss_2026', 'admin'),
('djamel', 'password123', 'user'),
('amine', 'azerty', 'user');