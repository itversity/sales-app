CREATE DATABASE sales_db;
CREATE USER sales_user WITH ENCRYPTED PASSWORD 'itversity';
ALTER DATABASE sales_db OWNER TO sales_user;
COMMIT;