/*
This view has a row for each instance of officer activity -- being in a call,
being on duty, and/or being out of service.  Note that there could be significant
overlap here.  We'll use this to drive the officer allocation view.
*/

-- Lookup table for the different types of activity
DROP MATERIALIZED VIEW IF EXISTS officer_activity CASCADE;

CREATE MATERIALIZED VIEW officer_activity AS
    -- we only want call_units that are patrol units; for others, we don't care about
    -- how their time is allocated
  WITH
    valid_call_units AS (SELECT call_unit_id FROM call_unit WHERE is_patrol_unit = TRUE),
    directed_patrol_natures AS (SELECT nature_id FROM nature WHERE is_directed_patrol = TRUE),
    self_initiated_sources AS (SELECT call_source_id FROM call_source WHERE is_self_initiated = TRUE)
  SELECT
    ROW_NUMBER() OVER (ORDER BY start_time ASC) AS officer_activity_id,
    activity.*
  FROM (
  SELECT
    ic.call_unit_id AS call_unit_id,
    ic.start_time AS start_time,
    ic.end_time AS end_time,
    (SELECT officer_activity_type_id
     FROM officer_activity_type
     WHERE descr='IN CALL - DIRECTED PATROL') AS officer_activity_type_id,
    ic.call_id AS call_id
  FROM
    in_call ic INNER JOIN call c ON ic.call_id = c.call_id
  WHERE
    ic.start_time IS NOT NULL AND
    ic.end_time IS NOT NULL AND
    ic.end_time - ic.start_time < interval '1 day' AND
    ic.call_unit_id IN (SELECT call_unit_id FROM valid_call_units) AND
    c.nature_id IN (SELECT nature_id FROM directed_patrol_natures)
  UNION ALL
  SELECT
    ic.call_unit_id AS call_unit_id,
    ic.start_time AS start_time,
    ic.end_time AS end_time,
    (SELECT officer_activity_type_id
     FROM officer_activity_type
     WHERE descr='IN CALL - SELF INITIATED') AS officer_activity_type_id,
    ic.call_id AS call_id
  FROM
    in_call ic INNER JOIN call c ON ic.call_id = c.call_id
  WHERE
    ic.start_time IS NOT NULL AND
    ic.end_time IS NOT NULL AND
    ic.end_time - ic.start_time < interval '1 day' AND
    ic.call_unit_id IN (SELECT call_unit_id FROM valid_call_units) AND
    c.nature_id NOT IN (SELECT nature_id FROM directed_patrol_natures) AND
    c.call_source_id IN (SELECT call_source_id FROM self_initiated_sources)
  UNION ALL
    SELECT
    ic.call_unit_id AS call_unit_id,
    ic.start_time AS start_time,
    ic.end_time AS end_time,
    (SELECT officer_activity_type_id
     FROM officer_activity_type
     WHERE descr='IN CALL - CITIZEN INITIATED') AS officer_activity_type_id,
    ic.call_id AS call_id
  FROM
    in_call ic INNER JOIN call c ON ic.call_id = c.call_id
  WHERE
    ic.start_time IS NOT NULL AND
    ic.end_time IS NOT NULL AND
    ic.end_time - ic.start_time < interval '1 day' AND
    ic.call_unit_id IN (SELECT call_unit_id FROM valid_call_units) AND
    c.nature_id NOT IN (SELECT nature_id FROM directed_patrol_natures) AND
    c.call_source_id NOT IN (SELECT call_source_id FROM self_initiated_sources)
  UNION ALL
  SELECT
    oos.call_unit_id AS call_unit_id,
    oos.start_time AS start_time,
    oos.end_time AS end_time,
    (SELECT officer_activity_type_id
     FROM officer_activity_type
     WHERE descr='OUT OF SERVICE') AS officer_activity_type_id,
    NULL AS call_id
   FROM
     out_of_service oos
   WHERE
     oos.start_time IS NOT NULL AND
     oos.end_time IS NOT NULL AND
     oos.end_time - oos.start_time < interval '1 day' AND
     oos.call_unit_id IN (SELECT * FROM valid_call_units)
   UNION ALL
   -- Here, we have to account for multiple officers clocking into the
   -- same unit; this will double count them unless we only take one row
   SELECT DISTINCT ON (sh.shift_id)
     sh.call_unit_id AS call_unit_id,
     sh.in_time AS start_time,
     sh.out_time AS out_time,
     (SELECT officer_activity_type_id
     FROM officer_activity_type
     WHERE descr='ON DUTY') AS officer_activity_type_id,
     NULL AS call_id
   FROM
     shift_unit sh
   WHERE
     sh.in_time IS NOT NULL AND
     sh.out_time IS NOT NULL AND
     sh.out_time - sh.in_time < interval '1 day'
   ORDER BY
     start_time) activity;

/*
This view has a row for each instance of officer activity at each 10 minute interval.  It can be used to aggregate activity up based on discrete time intervals instead of a continuous start_time to end_time.
*/

-- temp view needed here for speed
DROP MATERIALIZED VIEW IF EXISTS time_sample CASCADE;
CREATE MATERIALIZED VIEW time_sample AS
SELECT
    -- Round times to the nearest 10 mins
    date_trunc('hour', time_) +
      INTERVAL '10 min' * ROUND(date_part('minute', time_) / 10.0)
    AS time_
FROM
    -- Generate the range of times we have in the DB
    generate_series(
        (SELECT date_trunc('minute', min(start_time)) FROM officer_activity),
        (SELECT date_trunc('minute', max(end_time)) FROM officer_activity),
        '10 minutes'
    ) AS series(time_);

CREATE UNIQUE INDEX time_sample_time
  ON time_sample(time_);

DROP MATERIALIZED VIEW IF EXISTS discrete_officer_activity CASCADE;

CREATE MATERIALIZED VIEW discrete_officer_activity AS
  SELECT
    ROW_NUMBER() OVER (ORDER BY start_time ASC) AS discrete_officer_activity_id,
    ts.time_,
    oa.call_unit_id,
    oa.officer_activity_type_id,
    oa.call_id
  FROM
    officer_activity oa,
    time_sample ts
  WHERE
    ts.time_ BETWEEN oa.start_time AND oa.end_time;

CREATE INDEX discrete_officer_activity_time
  ON discrete_officer_activity(time_);

CREATE INDEX discrete_officer_activity_time_hour
  ON discrete_officer_activity (EXTRACT(HOUR FROM time_));
