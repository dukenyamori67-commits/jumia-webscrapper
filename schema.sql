CREATE TABLE jumia_phones (
    id SERIAL PRIMARY KEY,
    product_name TEXT,
    price TEXT,
    rating TEXT,
    product_link TEXT
);

SELECT *
FROM jumia_phones