#!/bin/bash

echo "
SELECT c.relname, a.attname, t.typname, t.typalign, t.typlen
FROM pg_class AS c
JOIN pg_attribute AS a ON a.attrelid = c.oid
JOIN pg_type AS t ON t.oid = a.atttypid
WHERE c.relname LIKE 'dataset_%' AND a.attnum >= 0
ORDER BY c.relname;
" | python manage.py dbshell
