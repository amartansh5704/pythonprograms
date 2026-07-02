CREATE DATABASE students_db;

\c students_db

CREATE TABLE students(
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(20) NOT NULL,
    age         INTEGER NOT NULL,
    city        VARCHAR(20),
    email       VARCHAR(20) UNIQUE,
    marks       DECIMAL(5,2),
    joined_on   DATE DEFAULT CURRENT_DATE
);

INSERT INTO students (name, age, city, email, marks)
VALUES ('Rahul Sharma', 20, 'delhi', 'rr@gmail.com', 56.76);

INSERT INTO students (name, age, city, email, marks)
VALUES ('Priya', 19, 'agra', 'pp@gmail.com', 98.42);

SELECT * FROM students