-- Table des produits (Affichée publiquement)
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(50)
);

INSERT INTO products (name, description, category) VALUES
('Kali Linux ISO', 'The most advanced Penetration Testing Distribution.', 'Software'),
('Parrot OS', 'Security OS for ethical hacking.', 'Software'),
('Alfa Network Adapter', 'Wi-Fi adapter with Monitor Mode support.', 'Hardware'),
('Ubertooth One', 'Open source 2.4 GHz wireless development platform.', 'Hardware');

-- Table des utilisateurs (Cachée, à exfiltrer)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL
);

INSERT INTO users (username, password) VALUES 
('administrator', 'Sup3r_S3cr3t_P@ssw0rd_Retrieved!'),
('guest', 'guest123'),
('student', 'esi-sba-2026');