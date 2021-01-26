
-- Database: authdb_dev

DROP DATABASE authdb_dev;

CREATE DATABASE authdb_dev
    WITH
    OWNER = auth
    ENCODING = 'UTF8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;