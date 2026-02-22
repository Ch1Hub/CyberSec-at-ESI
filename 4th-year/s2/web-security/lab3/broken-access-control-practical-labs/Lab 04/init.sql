CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    roleid INT DEFAULT 1
);

INSERT INTO users (username, password, email, roleid) VALUES 
('administrator', 'Sup3rS3cr3tP@ssw0rd', 'admin@esi-sba.dz', 2),
('djamel', 'password123', 'djamel@esi-sba.dz', 1),
('amine', 'azerty', 'amine@esi-sba.dz', 1);