CREATE OR REPLACE FUNCTION gen_random_string(_min_length INT = 3)
RETURNS VARCHAR
LANGUAGE SQL
AS '
SELECT substring(
  md5(random()::TEXT),
  0,
  _min_length + floor(random() * 10 + 1)::INT
)
';

-- First, ensure the uuid-ossp extension is available in your database
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Then, create a table with a UUID primary key
CREATE TABLE IF NOT exists huge_table_with_uuid (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    column1 VARCHAR(255) NOT NULL,
    column2 VARCHAR(255) NOT NULL,
    column3 TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

DO
$do$
BEGIN
  FOR index IN 1..60000000 LOOP
    INSERT INTO huge_table_with_uuid (column1,column2)
    SELECT gen_random_string(),
    gen_random_string();
  END LOOP;
END
$do$;

-- Then, create a table of the same size with sequentially incrementing numeric primary key

CREATE TABLE IF NOT exists huge_table_with_bigint (
    id bigint GENERATED ALWAYS AS IDENTITY
             PRIMARY KEY,
    column1 VARCHAR(255) NOT NULL,
    column2 VARCHAR(255) NOT NULL,
    column3 TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

DO
$do$
BEGIN
  FOR index IN 1..60000000 LOOP
    INSERT INTO huge_table_with_bigint (column1,column2)
    SELECT gen_random_string(),
    gen_random_string();
  END LOOP;
END
$do$;

-- Data generation statistics
--UUID: 6.1G
--Queries	4
--Updated Rows	0
--Execute time (ms)	9901680
--Fetch time (ms)	0
--Total time (ms)	9901680
--Start time	2024-08-08 14:30:54.740
--Finish time	2024-08-08 17:15:56.421
--
--bigint: 4.9G
--Queries	3
--Updated Rows	0
--Execute time (ms)	730174
--Fetch time (ms)	0
--Total time (ms)	730174
--Start time	2024-08-08 17:32:07.384
--Finish time	2024-08-08 17:44:17.560

--insert 1000000 rows, reindex;

DO
	$do$
	BEGIN
	  FOR index IN 1..1000000 LOOP
	    INSERT INTO huge_table_with_uuid (column1,column2)
	    SELECT gen_random_string(),
	    gen_random_string();
	  END LOOP;
	END
	$do$

    Start time	Fri Aug 09 17:50:04 MSK 2024
    Finish time	Fri Aug 09 17:54:12 MSK 2024

reindex index huge_table_with_uuid_pkey

    Start time	Fri Aug 09 17:57:32 MSK 2024
    Finish time	Fri Aug 09 17:59:33 MSK 2024


Query	DO
	$do$
	BEGIN
	  FOR index IN 1..1000000 LOOP
	    INSERT INTO huge_table_with_bigint (column1,column2)
	    SELECT gen_random_string(),
	    gen_random_string();
	  END LOOP;
	END
	$do$

    Start time	Fri Aug 09 18:00:38 MSK 2024
    Finish time	Fri Aug 09 18:00:49 MSK 2024

reindex index huge_table_with_bigint_pkey
    Start time	Fri Aug 09 18:01:44 MSK 2024
    Finish time	Fri Aug 09 18:02:58 MSK 2024

--pure reindex

reindex index huge_table_with_uuid_pkey
    Start time	Fri Aug 09 17:25:10 MSK 2024
    Finish time	Fri Aug 09 17:27:07 MSK 2024

reindex index huge_table_with_bigint_pkey;
    Start time	Fri Aug 09 17:36:12 MSK 2024
    Finish time	Fri Aug 09 17:37:16 MSK 2024

