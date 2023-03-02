#!/bin/bash

echo "
DROP VIEW IF EXISTS size_report;
CREATE VIEW size_report AS
  WITH RECURSIVE pg_inherit(inhrelid, inhparent) AS (
    SELECT
      inhrelid,
      inhparent
      FROM pg_inherits
    UNION
    SELECT
      child.inhrelid,
      parent.inhparent
    FROM pg_inherit child, pg_inherits parent
    WHERE child.inhparent = parent.inhrelid
  ),
  pg_inherit_short AS (
    SELECT *
    FROM pg_inherit
    WHERE inhparent NOT IN (SELECT inhrelid FROM pg_inherit)
  )
  SELECT
    table_schema AS schema
    , table_name AS table
    , row_estimate
    , pg_size_pretty(total_bytes) AS total_size
    , pg_size_pretty(index_bytes) AS index_size
    , pg_size_pretty(toast_bytes) AS toast_size
    , pg_size_pretty(table_bytes) AS table_size
    , ROUND(table_bytes::numeric / total_bytes::numeric, 2) AS table_size_ratio
    , ROUND(total_bytes::numeric / row_estimate::numeric, 2) AS avg_row_size
    , total_bytes
    , index_bytes
    , toast_bytes
    , table_bytes
  FROM (
    SELECT
      *,
      total_bytes - index_bytes - COALESCE(toast_bytes, 0) AS table_bytes
    FROM (
      SELECT
        c.oid
        , nspname AS table_schema
        , relname AS table_name
        , SUM(c.reltuples) OVER (partition BY parent) AS row_estimate
        , SUM(pg_total_relation_size(c.oid)) OVER (partition BY parent) AS total_bytes
        , SUM(pg_indexes_size(c.oid)) OVER (partition BY parent) AS index_bytes
        , SUM(pg_total_relation_size(reltoastrelid)) OVER (partition BY parent) AS toast_bytes
        , parent
       FROM (
         SELECT
           pg_class.oid
           , reltuples
           , relname
           , relnamespace
           , pg_class.reltoastrelid
           , COALESCE(inhparent, pg_class.oid) parent
         FROM pg_class
         LEFT JOIN pg_inherit_short
           ON inhrelid = oid
         WHERE relkind IN ('r', 'p')
       ) c
       LEFT JOIN pg_namespace n
         ON n.oid = c.relnamespace
       WHERE nspname NOT IN ('information_schema', 'pg_catalog')
    ) a
    WHERE oid = parent
  ) a
  ORDER BY total_bytes DESC;

VACUUM ANALYZE;
SELECT * FROM size_report;
" | psql $DATABASE_URL
