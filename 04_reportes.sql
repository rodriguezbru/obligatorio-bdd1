USE torneo_ucu;


SELECT
    j.ci,
    j.nombre,
    j.apellido,
    COUNT(g.id_gol) AS total_goles
FROM jugador j
JOIN gol g
    ON j.ci = g.ci_jugador
JOIN partido p
    ON g.id_partido = p.id_partido
WHERE g.autogol = FALSE
    AND p.id_torneo = 1
    AND p.estado = 'jugado'
GROUP BY j.ci, j.nombre, j.apellido
ORDER BY total_goles DESC
LIMIT 10;


SELECT
    p.id_partido,
    p.numero_fecha,
    el.nombre AS equipo_local,
    ev.nombre AS equipo_visitante,

    SUM(
        CASE
            WHEN pp.id_equipo = p.id_equipo_local
                 AND g.autogol = FALSE THEN 1
            WHEN pp.id_equipo = p.id_equipo_visitante
                 AND g.autogol = TRUE THEN 1
            ELSE 0
        END
    ) AS goles_local,

    SUM(
        CASE
            WHEN pp.id_equipo = p.id_equipo_visitante
                 AND g.autogol = FALSE THEN 1
            WHEN pp.id_equipo = p.id_equipo_local
                 AND g.autogol = TRUE THEN 1
            ELSE 0
        END
    ) AS goles_visitante

FROM partido p
JOIN equipo el
    ON p.id_equipo_local = el.id_equipo
JOIN equipo ev
    ON p.id_equipo_visitante = ev.id_equipo
LEFT JOIN gol g
    ON p.id_partido = g.id_partido
LEFT JOIN planilla_partido pp
    ON g.id_partido = pp.id_partido
    AND g.ci_jugador = pp.ci_jugador

WHERE p.id_torneo = 1
    AND p.estado = 'jugado'

GROUP BY
    p.id_partido,
    p.numero_fecha,
    el.nombre,
    ev.nombre

ORDER BY p.numero_fecha, p.id_partido;


WITH resultados AS (
    SELECT
        p.id_partido,
        p.id_equipo_local,
        p.id_equipo_visitante,

        SUM(
            CASE
                WHEN pp.id_equipo = p.id_equipo_local
                     AND g.autogol = FALSE THEN 1
                WHEN pp.id_equipo = p.id_equipo_visitante
                     AND g.autogol = TRUE THEN 1
                ELSE 0
            END
        ) AS goles_local,

        SUM(
            CASE
                WHEN pp.id_equipo = p.id_equipo_visitante
                     AND g.autogol = FALSE THEN 1
                WHEN pp.id_equipo = p.id_equipo_local
                     AND g.autogol = TRUE THEN 1
                ELSE 0
            END
        ) AS goles_visitante

    FROM partido p
    LEFT JOIN gol g
        ON p.id_partido = g.id_partido
    LEFT JOIN planilla_partido pp
        ON g.id_partido = pp.id_partido
        AND g.ci_jugador = pp.ci_jugador

    WHERE p.id_torneo = 1
        AND p.estado = 'jugado'

    GROUP BY
        p.id_partido,
        p.id_equipo_local,
        p.id_equipo_visitante
),

estadisticas AS (
    SELECT
        id_equipo_local AS id_equipo,
        goles_local AS gf,
        goles_visitante AS gc
    FROM resultados

    UNION ALL

    SELECT
        id_equipo_visitante AS id_equipo,
        goles_visitante AS gf,
        goles_local AS gc
    FROM resultados
)

SELECT
    e.nombre AS equipo,
    COUNT(s.id_equipo) AS PJ,
    SUM(CASE WHEN s.gf > s.gc THEN 1 ELSE 0 END) AS PG,
    SUM(CASE WHEN s.gf = s.gc THEN 1 ELSE 0 END) AS PE,
    SUM(CASE WHEN s.gf < s.gc THEN 1 ELSE 0 END) AS PP,
    SUM(s.gf) AS GF,
    SUM(s.gc) AS GC,
    SUM(s.gf) - SUM(s.gc) AS DG,
    SUM(
        CASE
            WHEN s.gf > s.gc THEN 3
            WHEN s.gf = s.gc THEN 1
            ELSE 0
        END
    ) AS puntos

FROM equipo e
LEFT JOIN estadisticas s
    ON e.id_equipo = s.id_equipo

WHERE e.id_torneo = 1

GROUP BY e.id_equipo, e.nombre

ORDER BY puntos DESC, DG DESC, GF DESC;


SELECT
    e.nombre AS equipo,
    SUM(CASE WHEN t.color = 'amarilla' THEN 1 ELSE 0 END) AS amarillas,
    SUM(CASE WHEN t.color = 'roja' THEN 1 ELSE 0 END) AS rojas,
    SUM(CASE
        WHEN t.color = 'amarilla' THEN 1
        WHEN t.color = 'roja' THEN 3
        ELSE 0
    END) AS puntos_fair_play
FROM equipo e
LEFT JOIN partido p
    ON p.id_torneo = e.id_torneo
    AND p.estado = 'jugado'
LEFT JOIN planilla_partido pp
    ON pp.id_partido = p.id_partido
    AND pp.id_equipo = e.id_equipo
LEFT JOIN tarjeta t
    ON t.id_partido = pp.id_partido
    AND t.ci_jugador = pp.ci_jugador
WHERE e.id_torneo = 1
GROUP BY e.id_equipo, e.nombre
ORDER BY puntos_fair_play ASC, e.nombre;


SELECT
    p.numero_fecha,
    COUNT(DISTINCT p.id_partido) AS partidos_jugados,
    COUNT(g.id_gol) AS total_goles,
    ROUND(
        COUNT(g.id_gol) / COUNT(DISTINCT p.id_partido), 2
    ) AS promedio_goles
FROM partido p
LEFT JOIN gol g
    ON p.id_partido = g.id_partido
WHERE p.id_torneo = 1
    AND p.estado = 'jugado'
GROUP BY p.numero_fecha
ORDER BY p.numero_fecha;


SELECT
    p.id_torneo,
    COUNT(DISTINCT p.id_partido) AS partidos_jugados,
    COUNT(g.id_gol) AS total_goles,
    ROUND(
        COUNT(g.id_gol) / COUNT(DISTINCT p.id_partido), 2
    ) AS promedio_goles
FROM partido p
LEFT JOIN gol g
    ON p.id_partido = g.id_partido
WHERE p.id_torneo = 1
    AND p.estado = 'jugado'
GROUP BY p.id_torneo;


SELECT
    c.nombre AS complejo,
    p.nombre_cancha AS cancha,
    COUNT(p.id_partido) AS cantidad_partidos
FROM partido p
JOIN complejo c
    ON p.id_complejo = c.id_complejo
WHERE p.id_torneo = 1
    AND p.estado = 'jugado'
GROUP BY p.id_complejo, c.nombre, p.nombre_cancha
ORDER BY cantidad_partidos DESC;


SELECT
    t.hora_inicio,
    t.hora_fin,
    COUNT(p.id_partido) AS cantidad_partidos
FROM turno t
JOIN partido p
    ON t.id_turno = p.id_turno
WHERE p.id_torneo = 1
    AND p.estado = 'jugado'
GROUP BY t.id_turno, t.hora_inicio, t.hora_fin
ORDER BY cantidad_partidos DESC;


SELECT
    f.nombre AS facultad,
    j.tipo,
    COUNT(j.ci) AS cantidad_jugadores
FROM facultad f
JOIN jugador j
    ON f.id_facultad = j.id_facultad
GROUP BY f.id_facultad, f.nombre, j.tipo
ORDER BY f.nombre, j.tipo;


SELECT
    j.ci,
    j.nombre,
    j.apellido,
    e.nombre AS equipo
FROM jugador j
JOIN equipo_jugador_torneo ejt
    ON j.ci = ejt.ci_jugador
JOIN equipo e
    ON ejt.id_equipo = e.id_equipo
WHERE ejt.id_torneo = 1
    AND NOT EXISTS (
        SELECT *
        FROM planilla_partido pp
        JOIN partido p
            ON pp.id_partido = p.id_partido
        WHERE pp.ci_jugador = j.ci
            AND p.id_torneo = ejt.id_torneo
    )
ORDER BY e.nombre, j.apellido;


SELECT
    e.nombre AS equipo,
    s.motivo,
    COUNT(s.id_sancion) AS cantidad_sanciones
FROM sancion_jugador s
JOIN equipo_jugador_torneo ejt
    ON s.ci_jugador = ejt.ci_jugador
    AND s.id_torneo = ejt.id_torneo
JOIN equipo e
    ON ejt.id_equipo = e.id_equipo
WHERE s.id_torneo = 1
GROUP BY e.id_equipo, e.nombre, s.motivo
ORDER BY e.nombre, s.motivo;


SELECT
    estado,
    COUNT(*) AS cantidad_partidos,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*)
         FROM partido
         WHERE id_torneo = 1), 2
    ) AS porcentaje
FROM partido
WHERE id_torneo = 1
GROUP BY estado
ORDER BY cantidad_partidos DESC;


SELECT
    p.numero_fecha AS fecha,
    el.nombre AS equipo_local,
    ev.nombre AS equipo_visitante,
    SUM(CASE
        WHEN pp.id_equipo = p.id_equipo_local AND g.autogol = FALSE THEN 1
        WHEN pp.id_equipo = p.id_equipo_visitante AND g.autogol = TRUE THEN 1
        ELSE 0
    END) AS goles_local,
    SUM(CASE
        WHEN pp.id_equipo = p.id_equipo_visitante AND g.autogol = FALSE THEN 1
        WHEN pp.id_equipo = p.id_equipo_local AND g.autogol = TRUE THEN 1
        ELSE 0
    END) AS goles_visitante
FROM partido p
JOIN equipo el ON p.id_equipo_local = el.id_equipo
JOIN equipo ev ON p.id_equipo_visitante = ev.id_equipo
LEFT JOIN gol g ON p.id_partido = g.id_partido
LEFT JOIN planilla_partido pp
    ON g.id_partido = pp.id_partido
    AND g.ci_jugador = pp.ci_jugador
WHERE p.id_torneo = 1
    AND p.estado = 'jugado'
GROUP BY p.id_partido, p.numero_fecha, el.nombre, ev.nombre
ORDER BY p.numero_fecha, p.id_partido;


WITH resultados AS (
    SELECT
        p.id_equipo_local,
        p.id_equipo_visitante,
        SUM(CASE
            WHEN pp.id_equipo = p.id_equipo_local AND g.autogol = FALSE THEN 1
            WHEN pp.id_equipo = p.id_equipo_visitante AND g.autogol = TRUE THEN 1
            ELSE 0
        END) AS goles_local,
        SUM(CASE
            WHEN pp.id_equipo = p.id_equipo_visitante AND g.autogol = FALSE THEN 1
            WHEN pp.id_equipo = p.id_equipo_local AND g.autogol = TRUE THEN 1
            ELSE 0
        END) AS goles_visitante
    FROM partido p
    LEFT JOIN gol g ON p.id_partido = g.id_partido
    LEFT JOIN planilla_partido pp
        ON g.id_partido = pp.id_partido
        AND g.ci_jugador = pp.ci_jugador
    WHERE p.id_torneo = 1 AND p.estado = 'jugado'
    GROUP BY p.id_partido, p.id_equipo_local, p.id_equipo_visitante
)
SELECT e.nombre AS equipo
FROM equipo e
JOIN resultados r
    ON e.id_equipo = r.id_equipo_local
    OR e.id_equipo = r.id_equipo_visitante
GROUP BY e.id_equipo, e.nombre
HAVING SUM(CASE
    WHEN e.id_equipo = r.id_equipo_local
        AND r.goles_local < r.goles_visitante THEN 1
    WHEN e.id_equipo = r.id_equipo_visitante
        AND r.goles_visitante < r.goles_local THEN 1
    ELSE 0
END) = 0;


SELECT
    e.nombre AS equipo,
    COUNT(p.id_partido) AS partidos_jugados
FROM equipo e
JOIN partido p
    ON e.id_equipo = p.id_equipo_local
    OR e.id_equipo = p.id_equipo_visitante
WHERE p.id_torneo = 1
    AND p.estado = 'jugado'
GROUP BY e.id_equipo, e.nombre
ORDER BY partidos_jugados DESC;


SELECT
    j.ci,
    j.nombre,
    j.apellido,
    SUM(CASE WHEN t.color = 'amarilla' THEN 1 ELSE 0 END) AS amarillas,
    SUM(CASE WHEN t.color = 'roja' THEN 1 ELSE 0 END) AS rojas,
    COUNT(*) AS total_tarjetas
FROM jugador j
JOIN tarjeta t ON j.ci = t.ci_jugador
JOIN partido p ON t.id_partido = p.id_partido
WHERE p.id_torneo = 1
    AND p.estado = 'jugado'
GROUP BY j.ci, j.nombre, j.apellido
ORDER BY total_tarjetas DESC, rojas DESC;

