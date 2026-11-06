CREATE DATABASE torneo_ucu;
USE torneo_ucu;

CREATE TABLE facultad (
    id_facultad INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE
);


CREATE TABLE jugador (
    ci VARCHAR(20) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    fecha_nacimiento DATE NOT NULL,
    id_facultad INT NOT NULL,
    tipo ENUM('grado', 'posgrado', 'docente', 'funcionario') NOT NULL,

    FOREIGN KEY (id_facultad)
        REFERENCES facultad(id_facultad)
);


CREATE TABLE torneo (
    id_torneo INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    anio INT NOT NULL,
    semestre INT NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    estado ENUM('inscripción', 'en curso', 'finalizado') NOT NULL,

    UNIQUE (anio, semestre),
    CHECK (semestre IN (1, 2)),
    CHECK (fecha_fin >= fecha_inicio)
);


CREATE TABLE equipo (
    id_equipo INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    id_torneo INT NOT NULL,
    id_facultad INT NOT NULL,
    ci_capitan VARCHAR(20),

    FOREIGN KEY (id_torneo)
        REFERENCES torneo(id_torneo),

    FOREIGN KEY (id_facultad)
        REFERENCES facultad(id_facultad),

    FOREIGN KEY (ci_capitan)
        REFERENCES jugador(ci),

    UNIQUE (nombre, id_torneo),
    UNIQUE (id_equipo, id_torneo)
);


CREATE TABLE equipo_jugador_torneo (
    id_equipo INT NOT NULL,
    ci_jugador VARCHAR(20) NOT NULL,
    id_torneo INT NOT NULL,
    numero_camiseta INT NOT NULL,

    PRIMARY KEY (id_equipo, ci_jugador, id_torneo),

    FOREIGN KEY (id_equipo, id_torneo)
        REFERENCES equipo(id_equipo, id_torneo),

    FOREIGN KEY (ci_jugador)
        REFERENCES jugador(ci),

    UNIQUE (ci_jugador, id_torneo),
    UNIQUE (id_equipo, numero_camiseta),

    CHECK (numero_camiseta BETWEEN 1 AND 99)
);


CREATE TABLE complejo (
    id_complejo INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(200) NOT NULL,
    departamento VARCHAR(100) NOT NULL
);


CREATE TABLE cancha (
    nombre_cancha VARCHAR(100) NOT NULL,
    id_complejo INT NOT NULL,
    superficie ENUM('sintético', 'parquet') NOT NULL,
    techada BOOLEAN NOT NULL,

    PRIMARY KEY (nombre_cancha, id_complejo),

    FOREIGN KEY (id_complejo)
        REFERENCES complejo(id_complejo)
);


CREATE TABLE turno (
    id_turno INT AUTO_INCREMENT PRIMARY KEY,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,

    UNIQUE (hora_inicio, hora_fin),
    CHECK (hora_fin > hora_inicio),
    CHECK (hora_inicio >= '18:00:00'),
    CHECK (hora_fin <= '23:00:00'),
    CHECK (TIME_TO_SEC(hora_fin) - TIME_TO_SEC(hora_inicio) = 3600)
);


CREATE TABLE partido (
    id_partido INT AUTO_INCREMENT PRIMARY KEY,
    id_torneo INT NOT NULL,
    numero_fecha INT NOT NULL,
    id_equipo_local INT NOT NULL,
    id_equipo_visitante INT NOT NULL,
    dia DATE NOT NULL,
    id_turno INT NOT NULL,
    nombre_cancha VARCHAR(100) NOT NULL,
    id_complejo INT NOT NULL,
    estado ENUM('programado', 'jugado', 'postergado', 'cancelado') NOT NULL DEFAULT 'programado',

    FOREIGN KEY (id_torneo)
        REFERENCES torneo(id_torneo),

    FOREIGN KEY (id_equipo_local, id_torneo)
        REFERENCES equipo(id_equipo, id_torneo),

    FOREIGN KEY (id_equipo_visitante, id_torneo)
        REFERENCES equipo(id_equipo, id_torneo),

    FOREIGN KEY (id_turno)
        REFERENCES turno(id_turno),

    FOREIGN KEY (nombre_cancha, id_complejo)
        REFERENCES cancha(nombre_cancha, id_complejo),

    CHECK (numero_fecha > 0),
    CHECK (id_equipo_local <> id_equipo_visitante)
);


CREATE TABLE planilla_partido (
    id_partido INT NOT NULL,
    ci_jugador VARCHAR(20) NOT NULL,
    id_equipo INT NOT NULL,

    PRIMARY KEY (id_partido, ci_jugador),

    FOREIGN KEY (id_partido)
        REFERENCES partido(id_partido),

    FOREIGN KEY (ci_jugador)
        REFERENCES jugador(ci),

    FOREIGN KEY (id_equipo)
        REFERENCES equipo(id_equipo)
);


CREATE TABLE gol (
    id_gol INT AUTO_INCREMENT PRIMARY KEY,
    id_partido INT NOT NULL,
    ci_jugador VARCHAR(20) NOT NULL,
    minuto INT NOT NULL,
    autogol BOOLEAN NOT NULL DEFAULT FALSE,

    FOREIGN KEY (id_partido, ci_jugador)
        REFERENCES planilla_partido(id_partido, ci_jugador),

    CHECK (minuto >= 0)
);


CREATE TABLE tarjeta (
    id_tarjeta INT AUTO_INCREMENT PRIMARY KEY,
    id_partido INT NOT NULL,
    ci_jugador VARCHAR(20) NOT NULL,
    minuto INT NOT NULL,
    color ENUM('amarilla', 'roja') NOT NULL,

    FOREIGN KEY (id_partido, ci_jugador)
        REFERENCES planilla_partido(id_partido, ci_jugador),

    CHECK (minuto >= 0)
);


CREATE TABLE sancion_jugador (
    id_sancion INT AUTO_INCREMENT PRIMARY KEY,
    ci_jugador VARCHAR(20) NOT NULL,
    id_torneo INT NOT NULL,
    motivo ENUM('roja', 'acumulación de amarillas', 'disciplinaria') NOT NULL,
    numero_fecha_inicio INT NOT NULL,
    cantidad_fechas INT NOT NULL,

    FOREIGN KEY (ci_jugador)
        REFERENCES jugador(ci),

    FOREIGN KEY (id_torneo)
        REFERENCES torneo(id_torneo),

    CHECK (numero_fecha_inicio > 0),
    CHECK (cantidad_fechas > 0)
);


CREATE TABLE login (
    correo VARCHAR(150) PRIMARY KEY,
    contrasena VARCHAR(255) NOT NULL,
    rol ENUM('administrador', 'planillero') NOT NULL
);


USE torneo_ucu;

SHOW TABLES;

