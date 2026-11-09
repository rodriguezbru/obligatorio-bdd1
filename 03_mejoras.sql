USE torneo_ucu;

CREATE TABLE fecha_torneo (
    id_torneo INT NOT NULL,
    numero_fecha INT NOT NULL,
    fecha_programada DATE NOT NULL,

    PRIMARY KEY (id_torneo, numero_fecha),

    FOREIGN KEY (id_torneo)
        REFERENCES torneo(id_torneo),

    CHECK (numero_fecha > 0)
);

INSERT INTO fecha_torneo
(id_torneo, numero_fecha, fecha_programada)
VALUES
(1, 1, '2026-10-05'),
(1, 2, '2026-10-12'),
(1, 3, '2026-10-19'),
(1, 4, '2026-11-09'),
(1, 5, '2026-11-16');

SELECT * FROM fecha_torneo;

ALTER TABLE partido
ADD CONSTRAINT fk_partido_fecha
FOREIGN KEY (id_torneo, numero_fecha)
REFERENCES fecha_torneo(id_torneo, numero_fecha);


CREATE TABLE historial_partido (
    id_historial INT AUTO_INCREMENT PRIMARY KEY,
    id_partido INT NOT NULL,
    dia_anterior DATE NOT NULL,
    id_turno_anterior INT NOT NULL,
    nombre_cancha_anterior VARCHAR(100) NOT NULL,
    id_complejo_anterior INT NOT NULL,
    dia_nuevo DATE NOT NULL,
    id_turno_nuevo INT NOT NULL,
    nombre_cancha_nueva VARCHAR(100) NOT NULL,
    id_complejo_nuevo INT NOT NULL,
    motivo VARCHAR(255) NOT NULL,
    fecha_cambio DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (id_partido)
        REFERENCES partido(id_partido),

    FOREIGN KEY (id_turno_anterior)
        REFERENCES turno(id_turno),

    FOREIGN KEY (id_turno_nuevo)
        REFERENCES turno(id_turno),

    FOREIGN KEY (nombre_cancha_anterior, id_complejo_anterior)
        REFERENCES cancha(nombre_cancha, id_complejo),

    FOREIGN KEY (nombre_cancha_nueva, id_complejo_nuevo)
        REFERENCES cancha(nombre_cancha, id_complejo)
);
