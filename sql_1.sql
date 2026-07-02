CREATE DATABASE lib;

\c lib;

DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS borrowed_books;
DROP TABLE IF EXISTS members;

CREATE TABLE members(
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(25) NOT NULL,
    phone           VARCHAR(15) NOT NULL UNIQUE,
    email           VARCHAR(50) NOT NULL UNIQUE,
    membership_type VARCHAR(20) NOT NULL DEFAULT 'regular',
    join_date       DATE DEFAULT CURRENT_DATE,
    is_active       BOOLEAN DEFAULT TRUE
);

CREATE TABLE books(
    id              SERIAL PRIMARY KEY,
    title           VARCHAR(100) NOT NULL,
    author          VARCHAR(100) NOT NULL,
    genre           VARCHAR(50) NOT NULL,
    total_copies    INT NOT NULL DEFAULT 1,
    available_copies INT NOT NULL DEFAULT 1,
    price           DECIMAL(10, 2)
);

CREATE TABLE borrowed_books(
    id              SERIAL PRIMARY KEY,
    member_id       INTEGER REFERENCES members(id),
    book_id         INTEGER REFERENCES books(id),
    borrowed_date   DATE DEFAULT CURRENT_DATE,
    return_date     DATE,
    is_returned     BOOLEAN DEFAULT FALSE
);

INSERT INTO members(name, email, phone, membership_type) VALUES
('John Doe', 'john.doe@example.com', '1234567890', 'regular');
INSERT INTO members(name, email, phone, membership_type) VALUES
('Jane Smith', 'jane.smith@example.com', '0987654321', 'premium');
INSERT INTO members(name, email, phone, membership_type) VALUES
('Alice Johnson', 'alice.johnson@example.com', '1112223333', 'regular');
INSERT INTO members(name, email, phone, membership_type) VALUES
('Bob Brown', 'bob.brown@example.com', '4445556666', 'premium');

INSERT INTO books(title, author, genre, total_copies, available_copies, price) VALUES
('The Great Gatsby', 'F. Scott Fitzgerald', 'Classic', 5, 5, 10.99);
INSERT INTO books(title, author, genre, total_copies, available_copies, price) VALUES
('1984', 'George Orwell', 'Dystopian', 3, 3, 8.99);
INSERT INTO books(title, author, genre, total_copies, available_copies, price) VALUES
('To Kill a Mockingbird', 'Harper Lee', 'Classic', 4, 4, 9.99);
INSERT INTO books(title, author, genre, total_copies, available_copies, price) VALUES
('1984', 'George Orwell', 'Dystopian', 3, 3, 8.99);
INSERT INTO books(title, author, genre, total_copies, available_copies, price) VALUES
('To Kill a Mockingbird', 'Harper Lee', 'Classic', 4, 4, 9.99);
INSERT INTO books(title, author, genre, total_copies, available_copies, price) VALUES

INSERT INTO borrowed_books(member_id, book_id, borrowed_date, return_date, is_returned) VALUES
(1, 1, '2026-01-01', '2026-01-02', FALSE);
INSERT INTO borrowed_books(member_id, book_id, borrowed_date, return_date, is_returned) VALUES
(2, 2, '2026-01-01', '2026-01-02', TRUE);
INSERT INTO borrowed_books(member_id, book_id, borrowed_date, return_date, is_returned) VALUES
(3, 3, '2026-01-01', '2026-01-02', FALSE);
INSERT INTO borrowed_books(member_id, book_id, borrowed_date, return_date, is_returned) VALUES
(4, 4, '2026-01-01', '2026-01-02', TRUE);
INSERT INTO borrowed_books(member_id, book_id, borrowed_date, return_date, is_returned) VALUES
(5, 5, '2026-01-01', '2026-01-02', FALSE);


SELECT * FROM members;
SELECT * FROM books;

SELECT
members.name AS member_name,
books.title AS book_title,
books.author,
borrowed_books.borrowed_date,

FROM borrowed_books
INNER JOIN members ON borrowed_books.member_id = members.id
INNER JOIN books ON borrowed_books.book_id = books.id;
WHERE borrowed_books.is_returned = FALSE;

SELECT title, author, genre, available_copies FROM books WHERE available_copies > 0 ORDER BY genre;

SELECT members.name, COUNT(borrowed_books.id) AS total_borrowed_books FROM members
LEFT JOIN borrowed_books ON members.id = borrowed_books.member_id
GROUP BY members.name
ORDER BY total_borrowed_books DESC;

-- most popular books
SELECT books.title, books.author, COUNT(borrowed_books.id) AS times_borrowed FROM books
LEFT JOIN borrowed_books ON books.id = borrowed_books.book_id
GROUP BY books.title, books.author
ORDER BY times_borrowed DESC;

-- premium members and their borrowed books
SELECT members.name, members.membership, books.title FROM members
INNER JOIN borrowed_books ON members.id = borrowed_books.member_id
INNER JOIN books ON books.id = borrowed_books.book_id
WHERE members.membership_type = 'premium'
AND borrowed_books.is_returned = FALSE;

