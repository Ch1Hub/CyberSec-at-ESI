-- Table Products
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(50)
);

INSERT INTO products (name, category) VALUES
('Gaming Mouse', 'Accessories'),
('Mechanical Keyboard', 'Accessories'),
('24 inch Monitor', 'Electronics'),
('HDMI Cable', 'Electronics');

-- Table Users (Cible)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL
);

INSERT INTO users (username, password) VALUES 
('administrator', 'Complex_P@ss_With_C0ncat!'),
('carlos', 'sierra');