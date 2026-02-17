CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    stock INT DEFAULT 10,
    category VARCHAR(50)
);

INSERT INTO products (name, stock, category) VALUES
('Raspberry Pi 4', 50, 'Electronics'),
('Arduino Uno', 120, 'Electronics'),
('Breadboard', 200, 'Components'),
('Jumper Wires', 500, 'Components');