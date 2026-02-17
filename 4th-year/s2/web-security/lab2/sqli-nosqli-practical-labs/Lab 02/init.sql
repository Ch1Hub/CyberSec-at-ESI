CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    role VARCHAR(20) DEFAULT 'user'
);

-- Insertion des utilisateurs
INSERT INTO users (username, password, email, role) VALUES 
('administrator', 'Sup3r_C0mpl3x_P@ssw0rd_Th@t_Y0u_W1ll_N3v3r_Gu3ss', 'admin@esi-sba.dz', 'admin'),
('djamel', 'password123', 'djamel@student.dz', 'user'),
('karim', 'azerty', 'karim@student.dz', 'user');