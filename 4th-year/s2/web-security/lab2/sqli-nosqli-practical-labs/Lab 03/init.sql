CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(50),
    released INT DEFAULT 1
);

INSERT INTO products (name, category, released) VALUES
('HackRF One', 'Hardware', 1),
('Burp Suite Pro', 'Software', 1),
('Lock Picking Set', 'Gadgets', 1),
('Flipper Zero', 'Hardware', 1),
('OWASP Guide', 'Books', 1);