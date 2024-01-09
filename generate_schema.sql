CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    "user" VARCHAR,
    book VARCHAR,
    quantity INTEGER,
    status VARCHAR,
    CONSTRAINT order_status CHECK (status IN ('pending', 'confirmed', 'rejected'))
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR,
    surname VARCHAR,
    email VARCHAR UNIQUE,
    picture VARCHAR,
    role VARCHAR,
    CONSTRAINT user_role CHECK (role IN ('admin', 'user'))
);

CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title VARCHAR,
    description VARCHAR,
    author VARCHAR,
    price FLOAT,
    cover VARCHAR,
    quantity INTEGER
);