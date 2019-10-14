DELIMITER //
CREATE PROCEDURE EmpleadoMes(IN Mes INT, IN Año INT, OUT Nombre VARCHAR(40))
BEGIN
    SELECT P.Nombre
    FROM Factura F
             INNER JOIN Empleado E
                        ON F.IdEmpleado = E.IdEmpleado
             INNER JOIN Persona P ON E.IdPersona = P.IdPersona
    WHERE MONTH(F.Fecha) = Mes
      AND YEAR(F.Fecha) = Año
    GROUP BY F.IdEmpleado
    ORDER BY SUM(F.SubTotal) DESC
    LIMIT 1
    INTO Nombre;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE CierreCajaFacturas(IN date VARCHAR(20))
BEGIN
    SELECT F.*
    FROM Factura F
    WHERE F.Fecha = date;
END
//
DELIMITER ;


DELIMITER //
CREATE PROCEDURE CierreCajaVentas(IN date VARCHAR(20))
BEGIN
    SELECT V.*
    FROM Venta V
             INNER JOIN Factura F ON V.IdFactura = F.IdFactura
    WHERE F.Fecha = date;
END
//
DELIMITER ;


DELIMITER //
CREATE PROCEDURE CierreCajaPromociones(IN date DATETIME)
BEGIN
    SELECT P.*
    FROM Promocion P
    WHERE DATE(P.Inicio) = date; -- TODO Revisar como mejorar desempeño
END
//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE CierreCajaPromocionFactura(IN date VARCHAR(20))
BEGIN
    SELECT PF.*
    FROM PromocionFactura PF
             INNER JOIN Factura F ON PF.IdFactura = F.IdFactura
    WHERE F.Fecha = date;
END
//
DELIMITER ;


DELIMITER //
CREATE PROCEDURE GarantiaArticulo(IN IdArticulo INT)
BEGIN
    SELECT DATE_ADD(F.Fecha, INTERVAL S.Garantia MONTH)
    FROM Factura F
             INNER JOIN Venta V ON F.IdFactura = V.IdFactura
             INNER JOIN Articulo A ON V.IdArticulo = A.IdArticulo
             INNER JOIN SKU S ON A.IdSKU = S.IdSKU
    WHERE A.IdArticulo = IdArticulo;
END
//
DELIMITER ;


DELIMITER //
CREATE PROCEDURE InicioPromocion(IN Fecha DATETIME, OUT Descuento INT)
BEGIN
    SELECT Descuento FROM Promocion WHERE Inicio = Fecha;
END
//
DELIMITER ;


DELIMITER //
CREATE PROCEDURE FinPromocion(IN Fecha DATETIME, OUT Descuento INT)
BEGIN
    SELECT Descuento FROM Promocion WHERE Fin = Fecha;
END
//
DELIMITER ;


# DELIMITER //
# CREATE PROCEDURE PuntosClientes()
# BEGIN
#     SELECT C.IdCliente, P.Nombre, C.Puntos
#     FROM Cliente C
#              INNER JOIN Persona P ON C.IdPersona = P.IdPersona;
# END
# //
# DELIMITER ;


DELIMITER //
CREATE PROCEDURE ReporteProductos()
BEGIN
    SELECT EA.Nombre, COUNT(*) AS Cantidad
    FROM Articulo A
             INNER JOIN EstadoArticulo EA ON A.IdEstadoArticulo = EA.IdEstadoArticulo
    GROUP BY EA.IdEstadoArticulo
    ORDER BY Cantidad DESC;
END
//
DELIMITER ;


DELIMITER //
CREATE PROCEDURE ReporteCompras()
BEGIN
    SELECT SUM(F.SubTotal) AS Total, COUNT(*) AS CantidadAnual
    FROM Factura F
    GROUP BY YEAR(F.Fecha)
    ORDER BY CantidadAnual DESC;
END
//
DELIMITER ;


CALL GarantiaArticulo(5)