\c postgres
DROP DATABASE IF EXISTS company_db;
CREATE DATABASE company_db;
\c company_db;

CREATE TABLE departments(
    id     SERIAL PRIMARY KEY,
    name   VARCHAR(255) NOT NULL UNIQUE,
    budget DECIMAL(12,2)
);

CREATE TABLE employees(
    id     SERIAL PRIMARY KEY,
    name   VARCHAR(50) NOT NULL,
    email  VARCHAR(255) NOT NULL UNIQUE,
    salary DECIMAL(12,2) CHECK (salary > 0),
    dept_id INT REFERENCES departments(id),
    joined_date DATE DEFAULT CURRENT_DATE
);

INSERT INTO departments (name, budget) VALUES
('Engineering', 5000000), ('Marketing', 2000000), ('HR', 1500000);

INSERT INTO employees (name, email, salary, dept_id) VALUES
('Rahul Sharma', 'rahul@co.com', 85000, 1),
('Priya Patel',  'priya@co.com', 92000, 1),
('Amit Verma',   'amit@co.com',  65000, 2),
('Sneha Gupta',  'sneha@co.com', 70000, 3),
('Rohan Das',    'rohan@co.com', 88000, 1);

SELECT e.name, e.salary, d.name AS department_name
FROM employees e
JOIN departments d ON e.dept_id = d.id;

-- Average salary of each department
SELECT d.name, ROUND(AVG(e.salary), 2) AS avg_salary, COUNT(e.id) AS employee_count
FROM departments d
LEFT JOIN employees e ON d.id = e.dept_id
GROUP BY d.name;

-- Department with average salary > 80000
SELECT d.name, ROUND(AVG(e.salary), 2) AS avg_salary
FROM departments d
JOIN employees e ON d.id = e.dept_id
GROUP BY d.name 
HAVING AVG(e.salary) > 80000;

SELECT DISTINCT ON (d.name)
    d.name as department, e.name, e.salary
FROM employees e 
JOIN departments d ON e.dept_id = d.id
ORDER BY d.name, e.salary DESC;