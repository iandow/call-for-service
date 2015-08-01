/*
For each hour in 2014, displays the number of officers clocked in,
the number of officers out of service, and the number of officers on a call.

Helper views are used to increase performance (without this, with 1 hour granularity,
   view takes ~1200 secs to creat; with this, with 1 hour granularity,
   only a few secs)
   
For some reason, using 5 minute intervals for the time sample causes the query
execution time to explode from 3 secs to ~800secs if the time range is extended
to the end of July.  It's something about the number of records used to create the views.
We can, however, query the whole year fairly quickly (~3 secs) with 10 minute intervals.

In addition, these indices should be present:
create index shift_time_in on shift(time_in);
create index shift_time_out on shift(time_out);
create index oos_start_time on out_of_service(start_time);
create index oos_end_time on out_of_service(end_time);
create index in_call_start_time on in_call(start_time);
create index in_call_end_time on in_call(end_time);
*/

-- Time sample
DROP MATERIALIZED VIEW IF EXISTS time_sample CASCADE;
CREATE MATERIALIZED VIEW time_sample AS
SELECT * FROM
generate_series('2014-01-01 00:00'::timestamp,
                '2014-12-31 23:59'::timestamp,
                '10 minutes') AS series(time_);

CREATE UNIQUE INDEX time_sample_time
  ON time_sample(time_); 

-- On duty
DROP MATERIALIZED VIEW IF EXISTS on_duty_count CASCADE;
CREATE MATERIALIZED VIEW on_duty_count AS

SELECT
    ts.time_ AS time_,
    CASE
      WHEN d.num IS NULL THEN 0
      ELSE d.num
    END AS num
FROM
    time_sample AS ts
    LEFT JOIN (
      SELECT time_sample.time_ AS time_, COUNT(*) AS num
      FROM time_sample, shift
      WHERE (time_out-time_in) < (interval '1 day')
        AND time_sample.time_ BETWEEN time_in AND time_out 
      GROUP BY time_sample.time_
    ) AS d ON (ts.time_ = d.time_);

CREATE UNIQUE INDEX on_duty_count_time
  ON on_duty_count(time_);

-- Out of service
DROP MATERIALIZED VIEW IF EXISTS oos_count CASCADE;
CREATE MATERIALIZED VIEW oos_count AS

SELECT
    ts.time_ AS time_,
    CASE
      WHEN d.num IS NULL THEN 0
      ELSE d.num
    END AS num
FROM
    time_sample AS ts
    LEFT JOIN (
      SELECT time_sample.time_ AS time_, COUNT(*) AS num
      FROM time_sample, out_of_service
      WHERE duration < (interval '1 day')
        AND out_of_service.call_unit_id IN (SELECT DISTINCT call_unit_id FROM shift)
        AND time_sample.time_ BETWEEN start_time AND end_time 
      GROUP BY time_sample.time_
    ) AS d ON (ts.time_ = d.time_);
    
CREATE UNIQUE INDEX oos_count_time
  ON oos_count(time_);
  
-- On call
DROP MATERIALIZED VIEW IF EXISTS in_call_count CASCADE;
CREATE MATERIALIZED VIEW in_call_count AS

SELECT ts.time_,
    call.call_source_id,
    call.nature_id,
    count(*) AS num
FROM in_call,
    call,
    time_sample ts
WHERE (in_call.start_call_unit_id IN ( SELECT DISTINCT shift.call_unit_id
         FROM shift)) AND (in_call.end_call_unit_id IN ( SELECT DISTINCT shift.call_unit_id
         FROM shift)) AND ts.time_ >= in_call.start_time AND ts.time_ <= in_call.end_time AND in_call.call_id = call.call_id
GROUP BY ts.time_, call.call_source_id, call.nature_id;

-- On Directed Patrol

DROP MATERIALIZED VIEW IF EXISTS dp_count CASCADE;
CREATE MATERIALIZED VIEW dp_count AS

SELECT 
  ts.time_,
  CASE
    WHEN d.num IS NULL THEN 0
    ELSE d.num
  END AS num
FROM
  time_sample AS ts
  LEFT JOIN (
    SELECT time_, SUM(num) AS num FROM in_call_count WHERE
      in_call_count.nature_id IN (58,121)
      GROUP BY time_
  ) AS d ON (ts.time_ = d.time_);

CREATE UNIQUE INDEX dp_count_time
  ON dp_count (time_);

-- On Self-initiated Call

DROP MATERIALIZED VIEW IF EXISTS self_init_count CASCADE;
CREATE MATERIALIZED VIEW self_init_count AS

SELECT 
  ts.time_,
  CASE
    WHEN d.num IS NULL THEN 0
    ELSE d.num
  END AS num
FROM
  time_sample AS ts
  LEFT JOIN (
    SELECT time_, SUM(num) AS num FROM in_call_count WHERE
      in_call_count.call_source_id = 8 AND in_call_count.nature_id NOT IN (58,121)
      GROUP BY time_
  ) AS d ON (ts.time_ = d.time_);

CREATE UNIQUE INDEX self_init_count_time
  ON self_init_count (time_);

-- On Other-initiated Call

DROP MATERIALIZED VIEW IF EXISTS other_init_count CASCADE;
CREATE MATERIALIZED VIEW other_init_count AS

SELECT 
  ts.time_,
  CASE
    WHEN d.num IS NULL THEN 0
    ELSE d.num
  END AS num
FROM
  time_sample AS ts
  LEFT JOIN (
    SELECT time_, SUM(num) AS num FROM in_call_count WHERE
      in_call_count.call_source_id <> 8 AND in_call_count.nature_id NOT IN (58, 121)
      GROUP BY time_
  ) AS d ON (ts.time_ = d.time_);

CREATE UNIQUE INDEX other_init_count_time
  ON other_init_count(time_);

/* Main view */                

DROP MATERIALIZED VIEW IF EXISTS officer_allocation;
CREATE MATERIALIZED VIEW officer_allocation AS

SELECT d.time_ AS time_sample,
    d.num AS num_on_duty,
    o.num AS num_oos,
    dp_count.num AS num_on_dp,
    self_init_count.num AS num_self_init,
    other_init_count.num AS num_other_init
FROM on_duty_count d,
    oos_count o,
    dp_count,
    self_init_count,
    other_init_count
WHERE d.time_ = o.time_ AND d.time_ = dp_count.time_ AND
      d.time_ = self_init_count.time_ AND d.time_ = other_init_count.time_;