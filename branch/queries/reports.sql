USE sk8;

DELIMITER //
CREATE PROCEDURE EmpleadoMes(IN Mes INT, OUT Nombre VARCHAR(40))
BEGIN
    SELECT P.Nombre
    FROM Factura F
             INNER JOIN Empleado E
                        ON F.IdEmpleado = E.IdEmpleado
             INNER JOIN Persona P ON E.IdPersona = P.IdPersona
    WHERE MONTH(F.Fecha) = Mes
    GROUP BY F.IdEmpleado
    ORDER BY SUM(F.SubTotal) DESC
    LIMIT 1 INTO Nombre;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE GarantiaArticulo(IN CodigoArticulo VARCHAR(40), OUT Garantia DATE)
BEGIN

END //
DELIMITER ;
