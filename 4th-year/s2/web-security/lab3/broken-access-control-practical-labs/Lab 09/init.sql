CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

INSERT INTO users (username, password) VALUES 
('administrator', 'Sup3rS3cr3tP@ssw0rd'),
('djamel', 'P@ssw0rd_Dj4m3l_2026'),
('amine', 'azerty');