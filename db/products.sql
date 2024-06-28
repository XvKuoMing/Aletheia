CREATE TABLE IF NOT EXISTS products (
shop VARCHAR(255) NOT NULL,
name VARCHAR(255) NOT NULL,
volume NUMERIC DEFAULT NULL,
volume_unit VARCHAR(50) DEFAULT NULL,
price INTEGER NOT NULL,
price_unit VARCHAR(50) NOT NULL,
description TEXT DEFAULT NULL,
img TEXT NOT NULL,
PRIMARY KEY (shop, name)
);


CREATE TABLE IF NOT EXISTS coming_products (
name VARCHAR(255) NOT NULL,
datetime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
PRIMARY KEY(name)
);

CREATE OR REPLACE FUNCTION read_and_delete()
RETURNS TABLE(product VARCHAR(255))
AS $function$
#VARIABLE_CONFLICT USE_COLUMN
BEGIN
	RETURN QUERY
	WITH fetched AS
	(
		DELETE FROM coming_products
		WHERE
		name IN (
			SELECT name FROM coming_products
			ORDER BY datetime DESC
			LIMIT 30
		)
		RETURNING name
	)
	SELECT name FROM fetched;
END; $function$
LANGUAGE plpgsql;
