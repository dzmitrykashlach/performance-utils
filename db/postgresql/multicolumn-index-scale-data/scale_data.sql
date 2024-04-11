/*
   Case description
 
   https://use-the-index-luke.com/sql/testing-scalability/data-volume
   https://use-the-index-luke.com/sql/example-schema/postgresql/performance-testing-scalability

   set up data

   1) indexes-1 with scale_slow index
   2) indexes-2 with scale_fast index
 */

CREATE TABLE scale_data (
   section NUMERIC NOT NULL,
   id1     NUMERIC NOT NULL,
   id2     NUMERIC NOT NULL
);

INSERT INTO scale_data
SELECT sections.*, gen.*
     , CEIL(RANDOM()*100) 
  FROM GENERATE_SERIES(1, 300)     sections,
       GENERATE_SERIES(1, 900000) gen
 WHERE gen <= sections * 3000;
 
explain analyze  SELECT count(*)
FROM scale_data
WHERE section = 300
AND id2 = 2

-- testing function
CREATE OR REPLACE FUNCTION test_scalability
   (sql_txt VARCHAR(2000), n INT)
   RETURNS SETOF RECORD AS
$$
DECLARE
   tim   INTERVAL[300];
   rec   INT[300];
   strt  TIMESTAMP;
   v_rec RECORD;
   iter  INT;
   sec   INT;
   cnt   INT;
   rnd   INT;
BEGIN
   FOR iter  IN 0..n LOOP
      FOR sec IN 0..300 LOOP
         IF iter = 0 THEN
           tim[sec] := 0;
           rec[sec] := 0;
         END IF;
         rnd  := CEIL(RANDOM() * 100);
         strt := CLOCK_TIMESTAMP();

         EXECUTE 'select count(*) from (' || sql_txt || ') tbl'
            INTO cnt
           USING sec, rnd;

         tim[sec] := tim[sec] + CLOCK_TIMESTAMP() - strt;
         rec[sec] := rec[sec] + cnt;

         IF iter = n THEN
            SELECT INTO v_rec sec, tim[sec], rec[sec];
            RETURN NEXT v_rec;
         END IF;
      END LOOP;
   END LOOP;

   RETURN;
END;
$$ LANGUAGE plpgsql;

explain analyze SELECT *
  FROM test_scalability('SELECT * '
                      ||  'FROM scale_data '
                      || 'WHERE section=$1 '
                      ||   'AND id2=$2', 10)
       AS (sec INT, seconds INTERVAL, cnt_rows INT);


-- create slow index
CREATE INDEX scale_slow ON scale_data (section, id1, id2);
ALTER TABLE scale_data CLUSTER ON scale_slow;
CLUSTER scale_data;

-- create fast index
CREATE INDEX scale_fast ON scale_data (section, id2, id1);
ALTER TABLE scale_data CLUSTER ON scale_fast;
CLUSTER scale_data;
