CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    api_key VARCHAR(100) NOT NULL
);

INSERT INTO users (username, password, api_key) VALUES 
('administrator', 'Sup3rS3cr3tP@ssw0rd', 'ADMIN-KEY-9999999999'),
('djamel', 'password123', 'ESI-SBA{R3D1R3CT_B0DY_L34K_M4ST3R}'),
('amine', 'azerty', 'USER-KEY-1234567890');