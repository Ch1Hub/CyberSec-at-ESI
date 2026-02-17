CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price VARCHAR(50),
    category VARCHAR(50),
    image VARCHAR(255),
    released INT DEFAULT 1
);

INSERT INTO products (name, description, price, category, image, released) VALUES
('ESI Hoodie', 'Official Hoodie of the CyberLab.', '$40', 'Clothing', 'https://m.media-amazon.com/images/I/71W+1a+5I+L._AC_UY1000_.jpg', 1),
('Python for Hackers', 'Best-selling book for pentesting.', '$25', 'Books', 'https://m.media-amazon.com/images/I/61f8JkI2S9L._AC_UF1000,1000_QL80_.jpg', 1),
('USB Rubber Ducky', 'Keystroke injection tool.', '$50', 'Gadgets', 'https://shop.hak5.org/cdn/shop/products/usb-rubber-ducky-deluxe_530x@2x.jpg', 1),
('Gift Card 50$', 'Perfect for students.', '$50', 'Gifts', 'https://png.pngtree.com/png-vector/20220611/ourmid/pngtree-voucher-gift-card-template-design-png-image_4989650.png', 1),
('PROTOTYPE ZERO', 'TOP SECRET FLAG: ESI-SBA{MYSQL_DOCK3R_M4ST3R}', '$9999', 'Tech', 'https://t3.ftcdn.net/jpg/02/98/53/63/360_F_298536338_P5yd7q9aKk9k8c8yG9pq3j7aKk9k8c8y.jpg', 0);