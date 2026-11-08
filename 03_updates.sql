
USE torneo_ucu;

UPDATE login
SET contrasena = SHA2('ClavePruebaAdmin2026', 256)
WHERE correo = 'admin@ucu.edu.uy';

UPDATE login
SET contrasena = SHA2('ClavePruebaPlan2026', 256)
WHERE correo = 'planillero@ucu.edu.uy';

SELECT correo, rol, LENGTH(contrasena) AS largo_hash
FROM login;