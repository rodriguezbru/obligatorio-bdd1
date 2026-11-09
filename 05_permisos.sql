
CREATE USER IF NOT EXISTS 'admin_torneo'@'localhost'
IDENTIFIED BY 'CAMBIAR_CLAVE_ADMIN';

CREATE USER IF NOT EXISTS 'planillero_torneo'@'localhost'
IDENTIFIED BY 'CAMBIAR_CLAVE_PLANILLERO';

CREATE USER IF NOT EXISTS 'consulta_torneo'@'localhost'
IDENTIFIED BY 'CAMBIAR_CLAVE_CONSULTA';


GRANT SELECT, INSERT, UPDATE, DELETE
ON torneo_ucu.*
TO 'admin_torneo'@'localhost';


GRANT SELECT ON torneo_ucu.facultad TO 'planillero_torneo'@'localhost';
GRANT SELECT ON torneo_ucu.jugador TO 'planillero_torneo'@'localhost';
GRANT SELECT ON torneo_ucu.torneo TO 'planillero_torneo'@'localhost';
GRANT SELECT ON torneo_ucu.equipo TO 'planillero_torneo'@'localhost';
GRANT SELECT ON torneo_ucu.equipo_jugador_torneo TO 'planillero_torneo'@'localhost';
GRANT SELECT ON torneo_ucu.complejo TO 'planillero_torneo'@'localhost';
GRANT SELECT ON torneo_ucu.cancha TO 'planillero_torneo'@'localhost';
GRANT SELECT ON torneo_ucu.turno TO 'planillero_torneo'@'localhost';
GRANT SELECT ON torneo_ucu.partido TO 'planillero_torneo'@'localhost';
GRANT SELECT ON torneo_ucu.planilla_partido TO 'planillero_torneo'@'localhost';
GRANT SELECT ON torneo_ucu.gol TO 'planillero_torneo'@'localhost';
GRANT SELECT ON torneo_ucu.tarjeta TO 'planillero_torneo'@'localhost';
GRANT SELECT ON torneo_ucu.sancion_jugador TO 'planillero_torneo'@'localhost';
GRANT SELECT ON torneo_ucu.fecha_torneo TO 'planillero_torneo'@'localhost';
GRANT SELECT ON torneo_ucu.historial_partido TO 'planillero_torneo'@'localhost';

GRANT INSERT, DELETE
ON torneo_ucu.planilla_partido
TO 'planillero_torneo'@'localhost';

GRANT INSERT, UPDATE, DELETE
ON torneo_ucu.gol
TO 'planillero_torneo'@'localhost';

GRANT INSERT
ON torneo_ucu.tarjeta
TO 'planillero_torneo'@'localhost';

GRANT INSERT
ON torneo_ucu.sancion_jugador
TO 'planillero_torneo'@'localhost';


GRANT SELECT
ON torneo_ucu.login
TO 'consulta_torneo'@'localhost';

GRANT SELECT ON torneo_ucu.torneo TO 'consulta_torneo'@'localhost';
GRANT SELECT ON torneo_ucu.equipo TO 'consulta_torneo'@'localhost';
GRANT SELECT ON torneo_ucu.partido TO 'consulta_torneo'@'localhost';
GRANT SELECT ON torneo_ucu.turno TO 'consulta_torneo'@'localhost';
GRANT SELECT ON torneo_ucu.planilla_partido TO 'consulta_torneo'@'localhost';
GRANT SELECT ON torneo_ucu.gol TO 'consulta_torneo'@'localhost';
