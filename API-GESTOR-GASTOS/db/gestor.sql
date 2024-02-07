DROP DATABASE IF EXISTS personal_finances;
CREATE DATABASE personal_finances DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE personal_finances;

CREATE TABLE users(
    user_id CHAR(30) PRIMARY KEY,
    full_name VARCHAR(80) NOT NULL,
    mail VARCHAR(100) UNIQUE NOT NULL,
    passhash VARCHAR(140) NOT NULL,
    user_role ENUM('admin','user'),
    user_status TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE category(
    category_id SMALLINT(3) AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(50),
    category_description VARCHAR(120),
    category_status TINYINT(1) DEFAULT 1
);

CREATE TABLE transactions(
    transactions_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id CHAR(30),
    category_id SMALLINT(3),
    amount FLOAT(10,2) NOT NULL,
    t_description VARCHAR(120),
    t_type ENUM('revenue','expenses'),
    t_date DATE,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (category_id) REFERENCES category(category_id)
);

CREATE TABLE tokens(
    token VARCHAR(180) PRIMARY KEY,
    user_id CHAR(30),
    token_status TINYINT(1) DEFAULT 1,
    token_created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

INSERT INTO `users` (`user_id`, `full_name`, `mail`, `passhash`, `user_role`, `user_status`, `created_at`, `updated_at`) VALUES ('', 'Winder Alexander Roman Semprun', 'winderroman3131@gmail.com', '827ccb0eea8a706c4c34a16891f84e7b', 'admin', '1', current_timestamp(), current_timestamp());