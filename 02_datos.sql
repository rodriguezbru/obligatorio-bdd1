USE torneo_ucu;

INSERT INTO facultad (nombre)
VALUES
('Ingeniería y tecnologías'),
('Psicología y bienestar humano'),
('Salud'),
('Ciencias Empresariales'),
('Derecho y artes liberales');
SELECT * FROM facultad;


INSERT INTO jugador
(ci, nombre, apellido, email, fecha_nacimiento, id_facultad, tipo)
VALUES
('50000001', 'Juan', 'Perez', 'juan.perez@ejemplo.com', '2002-03-15', 1, 'grado'),
('50000002', 'Pedro', 'Gomez', 'pedro.gomez@ejemplo.com', '2001-06-20', 1, 'grado'),
('50000003', 'Lucas', 'Fernandez', 'lucas.fernandez@ejemplo.com', '2003-01-10', 1, 'grado'),
('50000004', 'Martin', 'Rodriguez', 'martin.rodriguez@ejemplo.com', '2000-09-05', 1, 'posgrado'),
('50000005', 'Diego', 'Silva', 'diego.silva@ejemplo.com', '1990-11-12', 1, 'docente'),
('50000006', 'Andres', 'Lopez', 'andres.lopez@ejemplo.com', '2002-07-18', 1, 'grado'),

('50000007', 'Mateo', 'Garcia', 'mateo.garcia@ejemplo.com', '2002-02-14', 4, 'grado'),
('50000008', 'Santiago', 'Diaz', 'santiago.diaz@ejemplo.com', '2001-04-22', 4, 'grado'),
('50000009', 'Nicolas', 'Torres', 'nicolas.torres@ejemplo.com', '2003-08-30', 4, 'grado'),
('50000010', 'Facundo', 'Ruiz', 'facundo.ruiz@ejemplo.com', '2000-12-03', 4, 'posgrado'),
('50000011', 'Bruno', 'Castro', 'bruno.castro@ejemplo.com', '1988-05-16', 4, 'funcionario'),
('50000012', 'Joaquin', 'Morales', 'joaquin.morales@ejemplo.com', '2002-10-09', 4, 'grado'),

('50000013', 'Agustin', 'Romero', 'agustin.romero@ejemplo.com', '2002-01-25', 5, 'grado'),
('50000014', 'Emiliano', 'Alvarez', 'emiliano.alvarez@ejemplo.com', '2001-03-17', 5, 'grado'),
('50000015', 'Sebastian', 'Mendez', 'sebastian.mendez@ejemplo.com', '2003-05-08', 5, 'grado'),
('50000016', 'Franco', 'Suarez', 'franco.suarez@ejemplo.com', '2000-07-11', 5, 'posgrado'),
('50000017', 'Pablo', 'Herrera', 'pablo.herrera@ejemplo.com', '1985-09-19', 5, 'docente'),
('50000018', 'Rodrigo', 'Vega', 'rodrigo.vega@ejemplo.com', '2002-11-27', 5, 'grado'),

('50000019', 'Ignacio', 'Acosta', 'ignacio.acosta@ejemplo.com', '2002-04-13', 3, 'grado'),
('50000020', 'Federico', 'Pereira', 'federico.pereira@ejemplo.com', '2001-08-07', 3, 'grado'),
('50000021', 'Gonzalo', 'Ramos', 'gonzalo.ramos@ejemplo.com', '2003-06-21', 3, 'grado'),
('50000022', 'Tomas', 'Medina', 'tomas.medina@ejemplo.com', '2000-02-28', 3, 'posgrado'),
('50000023', 'Carlos', 'Sosa', 'carlos.sosa@ejemplo.com', '1987-10-14', 3, 'funcionario'),
('50000024', 'Daniel', 'Cabrera', 'daniel.cabrera@ejemplo.com', '2002-12-06', 3, 'grado'),

('50000025', 'Maximiliano', 'Navarro', 'maximiliano.navarro@ejemplo.com', '2002-05-04', 2, 'grado'),
('50000026', 'Valentin', 'Ortega', 'valentin.ortega@ejemplo.com', '2001-07-23', 2, 'grado'),
('50000027', 'Leonardo', 'Molina', 'leonardo.molina@ejemplo.com', '2003-09-15', 2, 'grado'),
('50000028', 'Alejandro', 'Rios', 'alejandro.rios@ejemplo.com', '2000-01-18', 2, 'posgrado'),
('50000029', 'Ricardo', 'Dominguez', 'ricardo.dominguez@ejemplo.com', '1989-03-29', 2, 'docente'),
('50000030', 'Gabriel', 'Fuentes', 'gabriel.fuentes@ejemplo.com', '2002-11-02', 2, 'grado'),

('50000031', 'Matias', 'Benitez', 'matias.benitez@ejemplo.com', '2002-08-12', 1, 'grado'),
('50000032', 'Ezequiel', 'Cardozo', 'ezequiel.cardozo@ejemplo.com', '2001-10-24', 1, 'grado'),
('50000033', 'Cristian', 'Ferreira', 'cristian.ferreira@ejemplo.com', '2003-04-16', 1, 'grado'),
('50000034', 'Adrian', 'Martinez', 'adrian.martinez@ejemplo.com', '2000-06-09', 1, 'posgrado'),
('50000035', 'Oscar', 'Gimenez', 'oscar.gimenez@ejemplo.com', '1986-12-20', 1, 'funcionario'),
('50000036', 'Damian', 'Varela', 'damian.varela@ejemplo.com', '2002-02-05', 1, 'grado');
SELECT COUNT(*) AS total_jugadores
FROM jugador;


INSERT INTO torneo
(nombre, anio, semestre, fecha_inicio, fecha_fin, estado)
VALUES
('Torneo Interfacultades Fútbol 5', 2026, 2,
 '2026-08-01', '2026-11-30', 'en curso');
SELECT * FROM torneo;


INSERT INTO equipo
(nombre, id_torneo, id_facultad, ci_capitan)
VALUES
('Ingeniería FC', 1, 1, NULL),
('Empresariales United', 1, 4, NULL),
('Derecho FC', 1, 5, NULL),
('Salud Atlético', 1, 3, NULL),
('Humanidades FC', 1, 2, NULL),
('Ingeniería B', 1, 1, NULL);
SELECT * FROM equipo;


INSERT INTO equipo_jugador_torneo
(id_equipo, ci_jugador, id_torneo, numero_camiseta)
VALUES
(1, '50000001', 1, 1),
(1, '50000002', 1, 2),
(1, '50000003', 1, 3),
(1, '50000004', 1, 4),
(1, '50000005', 1, 5),
(1, '50000006', 1, 6),

(2, '50000007', 1, 1),
(2, '50000008', 1, 2),
(2, '50000009', 1, 3),
(2, '50000010', 1, 4),
(2, '50000011', 1, 5),
(2, '50000012', 1, 6),

(3, '50000013', 1, 1),
(3, '50000014', 1, 2),
(3, '50000015', 1, 3),
(3, '50000016', 1, 4),
(3, '50000017', 1, 5),
(3, '50000018', 1, 6),

(4, '50000019', 1, 1),
(4, '50000020', 1, 2),
(4, '50000021', 1, 3),
(4, '50000022', 1, 4),
(4, '50000023', 1, 5),
(4, '50000024', 1, 6),

(5, '50000025', 1, 1),
(5, '50000026', 1, 2),
(5, '50000027', 1, 3),
(5, '50000028', 1, 4),
(5, '50000029', 1, 5),
(5, '50000030', 1, 6),

(6, '50000031', 1, 1),
(6, '50000032', 1, 2),
(6, '50000033', 1, 3),
(6, '50000034', 1, 4),
(6, '50000035', 1, 5),
(6, '50000036', 1, 6);
SELECT
    e.nombre AS equipo,
    COUNT(ejt.ci_jugador) AS cantidad_jugadores
FROM equipo e
JOIN equipo_jugador_torneo ejt
    ON e.id_equipo = ejt.id_equipo
GROUP BY e.id_equipo, e.nombre;


UPDATE equipo
SET ci_capitan = '50000001'
WHERE id_equipo = 1;

UPDATE equipo
SET ci_capitan = '50000007'
WHERE id_equipo = 2;

UPDATE equipo
SET ci_capitan = '50000013'
WHERE id_equipo = 3;

UPDATE equipo
SET ci_capitan = '50000019'
WHERE id_equipo = 4;

UPDATE equipo
SET ci_capitan = '50000025'
WHERE id_equipo = 5;

UPDATE equipo
SET ci_capitan = '50000031'
WHERE id_equipo = 6;

SELECT
    e.nombre AS equipo,
    CONCAT(j.nombre, ' ', j.apellido) AS capitan
FROM equipo e
JOIN jugador j
    ON e.ci_capitan = j.ci;


INSERT INTO complejo (nombre, direccion, departamento)
VALUES
('Complejo Deportivo UCU', 'Av. 8 de Octubre 2738', 'Montevideo'),
('Complejo Deportivo Central', 'Av. Italia 4500', 'Montevideo'),
('Complejo Deportivo Norte', 'Bulevar Artigas 3500', 'Montevideo');
SELECT * FROM complejo;


INSERT INTO cancha
(nombre_cancha, id_complejo, superficie, techada)
VALUES
('Cancha 1', 1, 'sintético', TRUE),
('Cancha 2', 1, 'sintético', FALSE),
('Cancha 1', 2, 'parquet', TRUE),
('Cancha 2', 2, 'sintético', FALSE),
('Cancha 1', 3, 'sintético', TRUE),
('Cancha 2', 3, 'parquet', TRUE);
SELECT * FROM cancha;


INSERT INTO turno (hora_inicio, hora_fin)
VALUES
('18:00:00', '19:00:00'),
('19:00:00', '20:00:00'),
('20:00:00', '21:00:00'),
('21:00:00', '22:00:00'),
('22:00:00', '23:00:00');
SELECT * FROM turno;


INSERT INTO partido
(id_torneo, numero_fecha, id_equipo_local, id_equipo_visitante,
 dia, id_turno, nombre_cancha, id_complejo, estado)
VALUES
(1, 1, 1, 2, '2026-10-05', 1, 'Cancha 1', 1, 'programado'),
(1, 1, 3, 4, '2026-10-05', 2, 'Cancha 1', 1, 'programado'),
(1, 1, 5, 6, '2026-10-05', 3, 'Cancha 2', 1, 'programado'),

(1, 2, 1, 3, '2026-10-12', 1, 'Cancha 1', 2, 'programado'),
(1, 2, 2, 5, '2026-10-12', 2, 'Cancha 1', 2, 'programado'),
(1, 2, 4, 6, '2026-10-12', 3, 'Cancha 2', 2, 'programado'),

(1, 3, 1, 4, '2026-10-19', 1, 'Cancha 1', 3, 'programado'),
(1, 3, 2, 6, '2026-10-19', 2, 'Cancha 1', 3, 'programado'),
(1, 3, 3, 5, '2026-10-19', 3, 'Cancha 2', 3, 'programado');
SELECT * FROM partido;



INSERT INTO planilla_partido
(id_partido, ci_jugador, id_equipo)
VALUES
(1, '50000001', 1),
(1, '50000002', 1),
(1, '50000003', 1),
(1, '50000004', 1),
(1, '50000005', 1),
(1, '50000007', 2),
(1, '50000008', 2),
(1, '50000009', 2),
(1, '50000010', 2),
(1, '50000011', 2),

(2, '50000013', 3),
(2, '50000014', 3),
(2, '50000015', 3),
(2, '50000016', 3),
(2, '50000017', 3),
(2, '50000019', 4),
(2, '50000020', 4),
(2, '50000021', 4),
(2, '50000022', 4),
(2, '50000023', 4),

(3, '50000025', 5),
(3, '50000026', 5),
(3, '50000027', 5),
(3, '50000028', 5),
(3, '50000029', 5),
(3, '50000031', 6),
(3, '50000032', 6),
(3, '50000033', 6),
(3, '50000034', 6),
(3, '50000035', 6),

(4, '50000001', 1),
(4, '50000002', 1),
(4, '50000003', 1),
(4, '50000004', 1),
(4, '50000005', 1),
(4, '50000013', 3),
(4, '50000014', 3),
(4, '50000015', 3),
(4, '50000016', 3),
(4, '50000017', 3),

(5, '50000007', 2),
(5, '50000008', 2),
(5, '50000009', 2),
(5, '50000010', 2),
(5, '50000011', 2),
(5, '50000025', 5),
(5, '50000026', 5),
(5, '50000027', 5),
(5, '50000028', 5),
(5, '50000029', 5),

(6, '50000019', 4),
(6, '50000020', 4),
(6, '50000021', 4),
(6, '50000022', 4),
(6, '50000023', 4),
(6, '50000031', 6),
(6, '50000032', 6),
(6, '50000033', 6),
(6, '50000034', 6),
(6, '50000035', 6),

(7, '50000001', 1),
(7, '50000002', 1),
(7, '50000003', 1),
(7, '50000004', 1),
(7, '50000005', 1),
(7, '50000019', 4),
(7, '50000020', 4),
(7, '50000021', 4),
(7, '50000022', 4),
(7, '50000023', 4),

(8, '50000007', 2),
(8, '50000008', 2),
(8, '50000009', 2),
(8, '50000010', 2),
(8, '50000011', 2),
(8, '50000031', 6),
(8, '50000032', 6),
(8, '50000033', 6),
(8, '50000034', 6),
(8, '50000035', 6),

(9, '50000013', 3),
(9, '50000014', 3),
(9, '50000015', 3),
(9, '50000016', 3),
(9, '50000017', 3),
(9, '50000025', 5),
(9, '50000026', 5),
(9, '50000027', 5),
(9, '50000028', 5),
(9, '50000029', 5);
SELECT COUNT(*) AS total_planillas
FROM planilla_partido;

INSERT INTO gol
(id_partido, ci_jugador, minuto, autogol)
VALUES
(1, '50000001', 12, FALSE),
(1, '50000002', 28, FALSE),
(1, '50000007', 35, FALSE),

(2, '50000013', 10, FALSE),
(2, '50000019', 20, FALSE),
(2, '50000014', 32, FALSE),
(2, '50000020', 40, FALSE),

(3, '50000025', 15, FALSE),
(3, '50000026', 30, FALSE),

(4, '50000001', 8, FALSE),
(4, '50000003', 22, FALSE),
(4, '50000013', 36, FALSE),

(5, '50000007', 14, FALSE),
(5, '50000008', 29, FALSE),
(5, '50000025', 38, FALSE),

(6, '50000019', 11, TRUE),
(6, '50000031', 25, FALSE),
(6, '50000032', 41, FALSE),

(7, '50000001', 9, FALSE),
(7, '50000002', 18, FALSE),
(7, '50000019', 33, FALSE),

(8, '50000007', 13, FALSE),
(8, '50000031', 27, FALSE),
(8, '50000008', 39, FALSE),

(9, '50000013', 17, FALSE),
(9, '50000025', 31, FALSE);
SELECT COUNT(*) AS total_goles
FROM gol;


INSERT INTO tarjeta
(id_partido, ci_jugador, minuto, color)
VALUES
(1, '50000002', 20, 'amarilla'),
(1, '50000008', 32, 'amarilla'),

(2, '50000015', 18, 'amarilla'),
(2, '50000021', 35, 'amarilla'),

(3, '50000026', 25, 'amarilla'),
(3, '50000033', 38, 'roja'),

(4, '50000002', 15, 'amarilla'),
(4, '50000016', 30, 'amarilla'),

(5, '50000009', 22, 'amarilla'),
(5, '50000027', 37, 'roja'),

(6, '50000022', 17, 'amarilla'),
(6, '50000034', 33, 'amarilla'),

(7, '50000002', 12, 'amarilla'),
(7, '50000020', 28, 'amarilla'),

(8, '50000010', 19, 'amarilla'),
(8, '50000035', 36, 'amarilla'),

(9, '50000015', 14, 'amarilla'),
(9, '50000028', 31, 'amarilla');
SELECT COUNT(*) AS total_tarjetas
FROM tarjeta;


DELETE FROM planilla_partido
WHERE id_partido = 6
AND ci_jugador = '50000033';

DELETE FROM planilla_partido
WHERE id_partido = 9
AND ci_jugador = '50000027';


INSERT INTO sancion_jugador
(ci_jugador, id_torneo, motivo, numero_fecha_inicio, cantidad_fechas)
VALUES
('50000033', 1, 'roja', 2, 1),
('50000027', 1, 'roja', 3, 1),
('50000002', 1, 'acumulación de amarillas', 4, 1),
('50000016', 1, 'disciplinaria', 4, 2);

SELECT * FROM sancion_jugador;


INSERT INTO login (correo, contrasena, rol)
VALUES
('admin@ucu.edu.uy', 'TEMPORAL_ADMIN', 'administrador'),
('planillero@ucu.edu.uy', 'TEMPORAL_PLANILLERO', 'planillero');

SELECT correo, rol
FROM login;


UPDATE partido
SET estado = 'jugado'
WHERE id_partido BETWEEN 1 AND 9;

SELECT id_partido, numero_fecha, estado
FROM partido
ORDER BY id_partido;
