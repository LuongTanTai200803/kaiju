-- CREATE TABLE user (
--     id CHAR(36) NOT NULL PRIMARY KEY DEFAULT (UUID()),
--     name VARCHAR(100) NOT NULL,
--     age INT NOT NULL
-- );
-- INSERT INTO user (id, name, age)
-- VALUES  ("a1b","Nguyen Van A","20"),
--         ("a2b","Nguyen Van B","30"),
--         ("a3b","Luong Tan Tai","21");

-- SELECT * FROM users WHERE id = 'a1b';

-- CREATE TABLE user1 (
--     id CHAR(36) NOT NULL PRIMARY KEY DEFAULT (UUID()),
--     name VARCHAR(100) NOT NULL,
--     age INT NOT NULL
-- );
-- INSERT INTO user1 (id, name, age)
-- VALUES  ("11111111","Nguyen Van A","20");

-- CREATE TABLE user2 (
--     id CHAR(36) NOT NULL PRIMARY KEY DEFAULT (UUID()),
--     name VARCHAR(100) NOT NULL,
--     age INT NOT NULL
-- );
-- INSERT INTO user2 (id, name, age)
-- VALUES  ("2222222","Nguyen Van A","20");
CREATE TABLE 'farm'(
    id VARCHAR(128) NOT NULL,
    name VARCHAR(128) NOT NULL,
    address VARCHAR(256) DEFAULT NULL,
    created_at datetime NOT NULL,
    updated_at datetime NOT NULL
)
