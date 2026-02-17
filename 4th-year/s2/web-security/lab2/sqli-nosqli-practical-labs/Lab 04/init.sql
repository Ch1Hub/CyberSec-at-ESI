CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(50),
    description TEXT
);

INSERT INTO products (name, category, description) VALUES
('Flipper Zero', 'Hardware', 'Multi-tool device for geeks'),
('Wi-Fi Pineapple', 'Hardware', 'Rogue Access Point'),
('Burp Suite Pro', 'Software', 'Web Vulnerability Scanner'),
('Metasploit', 'Software', 'Penetration Testing Framework');

-- 🚨 LA CIBLE : Table avec un nom aléatoire pour obliger le mapping
CREATE TABLE IF NOT EXISTS users_x9d2k (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username_u8s1 VARCHAR(50) NOT NULL,  -- Colonne aussi avec nom aléatoire
    password_p4w9 VARCHAR(255) NOT NULL
);

INSERT INTO users_x9d2k (username_u8s1, password_p4w9) VALUES 
('administrator', 'P@ssw0rd_Y0u_F0und_M3!'),
('wiener', 'peter');