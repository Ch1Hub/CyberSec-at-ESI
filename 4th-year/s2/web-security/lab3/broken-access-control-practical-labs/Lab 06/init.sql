CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    guid VARCHAR(36) NOT NULL UNIQUE,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    api_key VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    author_guid VARCHAR(36) NOT NULL
);

-- Insertion des utilisateurs avec des GUID (UUID)
INSERT INTO users (guid, username, password, api_key) VALUES 
('a1b2c3d4-e5f6-7890-1234-adminadminad', 'administrator', 'Sup3rS3cr3tP@ssw0rd', 'ADMIN-KEY-9999999999'),
('d41d8cd9-8f00-3204-a980-0998ecf8427e', 'djamel', 'password123', 'ESI-SBA{UNPR3D1CT4BL3_ID0R_M4ST3R}'),
('e99a18c4-2300-4b95-8b32-8419b48c1a63', 'amine', 'azerty', 'USER-KEY-1234567890');

-- Insertion des articles de blog
INSERT INTO posts (title, content, author_guid) VALUES 
('Welcome to ESI SBA CyberLab', 'This is our new cybersecurity platform. Have fun learning!', 'a1b2c3d4-e5f6-7890-1234-adminadminad'),
('My first day learning Web Security', 'Today I learned about SQL injections. It was mind-blowing!', 'e99a18c4-2300-4b95-8b32-8419b48c1a63'),
('Why Access Control is critical', 'Broken access control is number one on the OWASP Top 10. We must secure our endpoints.', 'd41d8cd9-8f00-3204-a980-0998ecf8427e');