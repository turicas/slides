SELECT
    CASE t.dow
        WHEN 0 THEN 'sunday'
        WHEN 1 THEN 'monday'
        WHEN 2 THEN 'tuesday'
        WHEN 3 THEN 'wednesday'
        WHEN 4 THEN 'thrusday'
        WHEN 5 THEN 'friday'
        WHEN 6 THEN 'saturday'
    END AS day_of_week,
    AVG(t.total)
FROM (
    SELECT
        EXTRACT(YEAR FROM inicio_del_viaje) AS year,
        EXTRACT(MONTH FROM inicio_del_viaje) AS month,
        EXTRACT(DAY FROM inicio_del_viaje) AS day,
        EXTRACT(DOW FROM inicio_del_viaje) AS dow,
        COUNT(*) AS total
    FROM mibici
    GROUP BY year, month, day, dow
) AS t
GROUP BY t.dow
ORDER BY dow ASC
