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
    LIMIT 1
    INTO Nombre;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE CierreCajaFacturas()
BEGIN
    SELECT F.*
    FROM Factura F
    WHERE F.Fecha = CURRENT_DATE();
END
//
DELIMITER ;


DELIMITER //
CREATE PROCEDURE CierreCajaVentas()
BEGIN
    SELECT V.*
    FROM Venta V
             INNER JOIN Factura F ON V.IdFactura = F.IdFactura
    WHERE F.Fecha = CURRENT_DATE();
END
//
DELIMITER ;


DELIMITER //
CREATE PROCEDURE CierreCajaPromociones()
BEGIN
    SELECT P.*
    FROM Promocion P
    WHERE DATE(P.Inicio) = CURRENT_DATE(); -- TODO Revisar como mejorar desempeño
END
//
DELIMITER ;


DELIMITER //
CREATE PROCEDURE CierreCajaPromocionFactura()
BEGIN
    SELECT PF.*
    FROM PromocionFactura PF
             INNER JOIN Factura F ON PF.IdFactura = F.IdFactura
    WHERE F.Fecha = CURRENT_DATE();
END
//
DELIMITER ;


DELIMITER //
CREATE PROCEDURE GarantiaArticulo(IN IdArticulo VARCHAR(40), OUT Garantia DATE)
BEGIN
    SELECT DATE_ADD(F.Fecha, INTERVAL S.Garantia MONTH)
    FROM Factura F
             INNER JOIN Venta V ON F.IdFactura = V.IdFactura
             INNER JOIN Articulo A ON V.IdArticulo = A.IdArticulo
             INNER JOIN SKU S ON A.IdSKU = S.IdSKU
    WHERE A.IdArticulo = IdArticulo
    INTO Garantia;
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
             INNER JOIN Estadoarticulo EA ON A.IdEstadoArticulo = EA.Nombre
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
