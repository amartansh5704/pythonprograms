\c postgres
DROP DATABASE IF EXISTS blog_db;
CREATE DATABASE blog_db;
\c blog_db

CREATE TABLE users(
    id      SERIAL PRIMARY KEY,
    name    VARCHAR(50) NOT NULL,
    email   VARCHAR(50) UNIQUE
);

CREATE TABLE posts(
    id      SERIAL PRIMARY KEY,
    title   VARCHAR(200) NOT NULL,
    content TEXT,
    author_id   INTEGER REFERENCES users(id) ON DELETE CASCADE,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
);

CREATE TABLE comments (
    id        SERIAL PRIMARY KEY,
    post_id   INTEGER REFERENCES posts(id) ON DELETE CASCADE,
    user_id   INTEGER REFERENCES users(id) ON DELETE SET NULL,
    text      TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tags (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(30) UNIQUE NOT NULL
);

CREATE TABLE post_tags (
    post_id INTEGER REFERENCES posts(id) ON DELETE CASCADE,
    tag_id  INTEGER REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (post_id, tag_id)
);

INSERT INTO users (name, email) VALUES
('Alice', 'alice@blog.com'), ('Bob', 'bob@blog.com');

INSERT INTO posts (title, content, author_id) VALUES
('Learning PostgreSQL', 'PostgreSQL is awesome...', 1),
('Python Tips', 'Use list comprehensions...', 2);

INSERT INTO tags (name) VALUES ('Database'), ('Python'), ('Tutorial');

INSERT INTO post_tags (post_id, tag_id) VALUES (1, 1), (1, 3), (2, 2), (2, 3);

INSERT INTO comments (post_id, user_id, text) VALUES
(1, 2, 'Great article!'), (1, 1, 'Thanks Bob!'), (2, 1, 'Very helpful.');

SELECT
    p.title,
    u.name AS author,
    COUNT (DISTINCT c.id) AS comment_count,
    STRING_AGG(t.name, ', ') AS tags

FROM posts p
JOIN users u ON p.author_id = u.id
LEFT JOIN comments c ON p.id = c.post_id
LEFT JOIN post_tags pt ON p.id = pt.post_id
LEFT JOIN tags t ON pt.tag_id = t.id
GROUP BY p.id, p.title, u.name;

CREATE VIEW post_summary AS
SELECT p.id, p.title, u.name AS author,
p.created_at
FROM posts p
JOIN users u ON p.author_id = u.id;

Select * FROM post_summary;

BEGIN;
    INSERT INTO posts (title, content, author_id)
    VALUES ('OOP in Python', 'Classed and objects', 1) RETURNING id;
    INSERT INTO post_tags (post_id, tag_id) VALUES (3,2), (3,3);
COMMIT;

SELECT * FROM posts WHERE title = 'OOP in Python';
