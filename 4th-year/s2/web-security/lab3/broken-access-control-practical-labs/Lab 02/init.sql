CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    role VARCHAR(20) DEFAULT 'user'
);

INSERT INTO users (username, role) VALUES 
('administrator', 'admin'),
('djamel', 'user'),
('karim', 'user'),
('amine', 'user');