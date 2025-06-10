ALTER TABLE customers
ADD COLUMN category_id BIGINT,
ADD COLUMN category_code VARCHAR(50),
ADD COLUMN brand TEXT;

UPDATE customers d
SET
    category_id = i.category_id,
    category_code = i.category_code,
    brand = i.brand
FROM (
    SELECT DISTINCT ON (product_id)
        product_id,
        category_id,
        category_code,
        brand
    FROM (
        SELECT *,
            (CASE WHEN category_id IS NULL THEN 1 ELSE 0 END +
             CASE WHEN category_code IS NULL THEN 1 ELSE 0 END +
             CASE WHEN brand IS NULL THEN 1 ELSE 0 END) AS null_count
        FROM items
    ) sub
    ORDER BY product_id, null_count
) i
WHERE d.product_id = i.product_id;