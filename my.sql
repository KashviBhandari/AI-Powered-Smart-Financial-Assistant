create database  finance_db;
use finance_db;
SHOW TABLES;
CREATE TABLE personal_finance(

    id INT AUTO_INCREMENT PRIMARY KEY,

    salary FLOAT,

    total_expense FLOAT,

    savings FLOAT,

    emi FLOAT,

    financial_health VARCHAR(100),

    prediction FLOAT

);
