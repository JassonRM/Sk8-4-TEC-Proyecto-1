# Gets the amount of Articulos in each state
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


# Gets all the money sold (without taxes) and the amount of Ventas per year
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