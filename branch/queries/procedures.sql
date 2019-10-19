# Gets characteristic data for the Empleado with more sales in the
# specified Mes and Año
DELIMITER //
CREATE PROCEDURE EmpleadoMes(IN Mes INT, IN Año INT)
BEGIN
    SELECT P.Nombre, P.Apellido1, P.Apellido2, E.IdEmpleado
    FROM Factura F
             INNER JOIN Empleado E
                        ON F.IdEmpleado = E.IdEmpleado
             INNER JOIN Persona P ON E.IdPersona = P.IdPersona
    WHERE MONTH(F.Fecha) = Mes
      AND YEAR(F.Fecha) = Año
    GROUP BY F.IdEmpleado
    ORDER BY SUM(F.SubTotal) DESC
    LIMIT 1;
END //
DELIMITER ;


# Gets all Facturas created in the specified date
DELIMITER //
CREATE PROCEDURE CierreCajaFacturas(IN date VARCHAR(20))
BEGIN
    SELECT F.*
    FROM Factura F
    WHERE F.Fecha = date;
END
//
DELIMITER ;


# Gets all Ventas created in the specified date

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


# Gets all Promociones created in the specified date
DELIMITER //
CREATE PROCEDURE CierreCajaPromociones()
BEGIN
    SELECT P.*
    FROM Promocion P
    WHERE DATE(P.Inicio) = CURRENT_DATE(); -- TODO Revisar como mejorar desempeño
END
//
DELIMITER ;


# Gets all PromocionFactura elements created in the specified date
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


# Gets the date in which Garantia expires for a specific Articulo
DELIMITER //
CREATE PROCEDURE GarantiaArticulo(IN IdArticulo INT)
BEGIN
    SELECT DATE_ADD(F.Fecha, INTERVAL S.Garantia MONTH) AS Garantía
    FROM Factura F
             INNER JOIN Venta V ON F.IdFactura = V.IdFactura
             INNER JOIN Articulo A ON V.IdArticulo = A.IdArticulo
             INNER JOIN SKU S ON A.IdSKU = S.IdSKU
    WHERE A.IdArticulo = IdArticulo;
END
//
DELIMITER ;


# Gets all Promociones that started in the specified date
DELIMITER //
CREATE PROCEDURE InicioPromocion(IN Fecha DATETIME)
BEGIN
    SELECT P.IdPromocion, P.Descripcion, P.Descuento FROM Promocion P WHERE Inicio = Fecha;
END
//
DELIMITER ;


# Gets all Promociones that end in the specified date
DELIMITER //
CREATE PROCEDURE FinPromocion(IN Fecha DATETIME)
BEGIN
    SELECT P.IdPromocion, P.Descripcion, P.Descuento FROM Promocion P WHERE Fin = Fecha;
END
//
DELIMITER ;