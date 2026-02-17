CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price VARCHAR(20),
    category VARCHAR(50)
);

INSERT INTO products (name, description, price, category) VALUES
('Razer BlackWidow', 'Mechanical Gaming Keyboard', '$120', 'Accessories'),
('Logitech G Pro', 'Wireless Gaming Mouse', '$90', 'Accessories'),
('Samsung Odyssey G9', '49-inch Curved Monitor', '$1200', 'Monitors'),
('Dell UltraSharp', '4K Professional Monitor', '$700', 'Monitors'),
('Herman Miller Aeron', 'Ergonomic Chair', '$1400', 'Office');