-- Primary Keys can't be empty of duplicated
CREATE TABLE IF NOT EXISTS customer(
	customer_id SERIAL PRIMARY KEY, 
	first_name VARCHAR(100),
	last_name VARCHAR(100),
	address VARCHAR(150),
	billing_info VARCHAR(150)
);

