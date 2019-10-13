import mysql.connector
import psycopg2
import datetime
from pydbgen import pydbgen

fecha = datetime.datetime.now().strftime("%Y-%m-%d")

"""
Moves all new data (bills, sales and promos) from branch to warehouse 
b_cursor: branch database cursor
w_cursor: warehouse database cursor
sucursal: name of the branch that is sending data
"""


def cierreCaja(sucursal):
    branch = mysql.connector.connect(host="localhost", user="root", database="sk8", passwd="salchipapa101")
    warehouse = psycopg2.connect(dbname="sk8_warehouse", user="postgres", password="salchipapa101")
    w_cursor = warehouse.cursor()
    b_cursor = branch.cursor()

    # get branch id
    w_cursor.execute("SELECT IdSucursal FROM Sucursal WHERE Nombre = %s", (sucursal,))
    idSucursal = w_cursor.fetchone()[0]

    # move facturas from branch to warehouse
    b_cursor.callproc("CierreCajaFacturas")
    for result in b_cursor.stored_results():
        for factura in result.fetchall():
            w_cursor.execute(
                "INSERT INTO Factura (IdFacturaSucursal, Codigo, Fecha, SubTotal, Impuestos, PuntosOtorgados, IdCliente, IdEmpleado, IdMetodoPago, IdSucursal) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                factura + (idSucursal,))
    warehouse.commit()
    # move ventas from branch to warehouse
    b_cursor.callproc("CierreCajaVentas")
    for result in b_cursor.stored_results():
        for venta in result.fetchall():
            w_cursor.execute(
                "SELECT IdFactura FROM Factura WHERE IdFacturaSucursal = %s AND IdSucursal = %s",
                (venta[1], idSucursal))
            idFactura = w_cursor.fetchone()[0]
            w_cursor.execute(
                "INSERT INTO Venta (IdArticulo, IdFactura, Precio) VALUES (%s, %s, %s)",
                (venta[0], idFactura, venta[2]))

            if venta[2] < 0:  # fue devolución
                w_cursor.execute(
                    "UPDATE Articulo SET IdEstadoArticulo = %s WHERE IdArticulo = %s",
                    (4, venta[0]))
            else:
                w_cursor.execute(
                    "UPDATE Articulo SET IdEstadoArticulo = %s WHERE IdArticulo = %s",
                    (3, venta[0]))

    # move Promociones from branch to warehouse
    b_cursor.callproc("CierreCajaPromociones")
    for result in b_cursor.stored_results():
        for promocion in result.fetchall():
            w_cursor.execute(
                "INSERT INTO Promocion (IdPromocionSucursal, IdSKU, Descripcion, Inicio, Fin, Descuento, IdSucursal) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                promocion + (idSucursal,))

    # move PromocionFactura from branch to warehouse
    b_cursor.callproc("CierreCajaPromocionFactura")
    for result in b_cursor.stored_results():
        for promocionFactura in result.fetchall():
            w_cursor.execute(
                "SELECT IdFactura FROM Factura WHERE IdFacturaSucursal = %s AND IdSucursal = %s",
                (promocionFactura[1], idSucursal))
            idFactura = w_cursor.fetchone()[0]
            w_cursor.execute(
                "INSERT INTO PromocionFactura (IdPromocion, IdFactura) VALUES (%s, %s)",
                (promocionFactura[0], idFactura))

    # close connections
    warehouse.commit()
    branch.commit()
    w_cursor.close()
    b_cursor.close()
    warehouse.close()
    branch.close()


def insertCliente(identificacion, nombre, apellido1, apellido2, telefono, correo, fechaNacimiento, direccion1,
                  direccion2, distrito, descripcion):
    # Create random generator
    gen = pydbgen.pydb()

    # Connect to an existing database and open a cursor to perform database operations
    warehouse = psycopg2.connect(dbname="sk8_warehouse", user="postgres", password="salchipapa101")
    w_cursor = warehouse.cursor()

    # Check if Persona exists
    w_cursor.execute("SELECT IdPersona FROM persona where identificacion = %s", (identificacion,))
    idpersona = w_cursor.fetchone()
    if idpersona != None:
        idpersona = idpersona[0]
    else:
        # Insert Persona and Direccion
        w_cursor.execute("SELECT COUNT(*) FROM Persona")
        CantidadPersonas = w_cursor.fetchone()[0]
        w_cursor.execute("SELECT COUNT(*) FROM Direccion")
        CantidadDirecciones = w_cursor.fetchone()[0]

        w_cursor.execute("SELECT iddistrito FROM distrito where nombre = %s",
                         (distrito,))
        iddistrito = w_cursor.fetchone()[0]

        direccion = (CantidadDirecciones + 1, iddistrito, direccion1, direccion2)
        w_cursor.execute(
            "INSERT INTO Direccion (IdDireccion, IdDistrito, Detalle1, Detalle2) VALUES (%s, %s, %s, %s)",
            direccion)

        idpersona = CantidadPersonas + 1
        persona = (
            idpersona, identificacion, nombre, apellido1, apellido2, telefono, correo, fechaNacimiento, fecha, 1,
            CantidadDirecciones + 1)
        w_cursor.execute(
            "INSERT INTO Persona (IdPersona, Identificacion, Nombre, Apellido1, Apellido2, Telefono, Correo, FechaNacimiento, FechaRegistro, IdEstado, IdDireccion) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            persona)

    # Insert Empleado

    w_cursor.execute("SELECT COUNT(*) FROM Cliente")
    CantidadClientes = w_cursor.fetchone()[0]
    estado = 1
    cliente = (
        CantidadClientes + 1, idpersona, descripcion, 0, fecha, estado)
    w_cursor.execute(
        "INSERT INTO Cliente (IdCliente, IdPersona, Descripcion, Puntos, FechaRegistro, IdEstado) VALUES (%s, %s, %s, %s, %s, %s)",
        cliente)

    # Make the changes to the database persistent
    warehouse.commit()

    # Close communication with the database
    w_cursor.close()
    warehouse.close()
    return


def newPromo(idSKU, description, start, finish, discount):
    branch = mysql.connector.connect(host="localhost", user="root", database="sk8", passwd="salchipapa101")
    b_cursor = branch.cursor()
    promocion = (idSKU, description, start, finish, discount)
    b_cursor.execute(
        "INSERT INTO Promocion (IdSKU, Descripcion, Inicio, Fin, Descuento) VALUES (%s, %s, %s, %s, %s)",
        promocion)
    branch.commit()

    # close connections
    b_cursor.close()
    branch.close()


def newSale(articulos, codigoFactura, fecha, porcentajeImpuestos, porcentajePuntos,
            idCliente,
            idEmpleado,
            idMetodoPago, sucursal):
    branch = mysql.connector.connect(host="localhost", user="root", database=sucursal, passwd="salchipapa101")
    warehouse = psycopg2.connect(dbname="sk8_warehouse", user="postgres", password="salchipapa101")
    w_cursor = warehouse.cursor()
    b_cursor = branch.cursor()

    # get estadoArticulo for a sold article
    b_cursor.execute("SELECT IdEstadoArticulo FROM EstadoArticulo WHERE Nombre = %s", ('Vendido',))
    estadoVendido = b_cursor.fetchone()[0]

    # get estadoArticulo for a stock article
    b_cursor.execute("SELECT IdEstadoArticulo FROM EstadoArticulo WHERE Nombre = %s", ('Tienda',))
    estadoInventario = b_cursor.fetchone()[0]

    precioTotal = 0
    crearFactura = True
    idFactura = 0
    idArticulosVendidos = []
    idPromociones = []
    for idArticulo in articulos:
        b_cursor.execute("UPDATE Articulo SET IdEstadoArticulo = %s WHERE IdArticulo = %s AND IdEstadoArticulo = %s ",
                         (estadoVendido, idArticulo, estadoInventario))
        branch.commit()
        if b_cursor.rowcount != 0:
            if crearFactura:
                crearFactura = False
                b_cursor.execute(
                    "INSERT INTO Factura (Codigo, Fecha, IdCliente, IdEmpleado, IdMetodoPago) VALUES (%s, %s, %s, %s, %s)",
                    (codigoFactura, fecha, idCliente, idEmpleado, idMetodoPago))
                branch.commit()
                idFactura = b_cursor.lastrowid
            b_cursor.execute(
                "SELECT S.PrecioActual FROM SKU S INNER JOIN Articulo A ON S.IdSKU = A.IdSKU WHERE A.IdArticulo = %s",
                (idArticulo,))
            precio = b_cursor.fetchone()[0]
            b_cursor.execute(
                "SELECT P.Descuento, P.IdPromocion FROM  SKU S INNER JOIN Promocion P  ON  S.IdSKU = P.IdSKU INNER JOIN Articulo A ON P.IdSKU = A.IdSKU WHERE A.IdArticulo = %s AND P.Fin > CURRENT_TIMESTAMP()",
                (idArticulo,))
            promo = b_cursor.fetchone()
            descuento = 0
            if promo != None:
                descuento = promo[0]/100
                b_cursor.execute(
                    "INSERT INTO PromocionFactura (IdPromocion, IdFactura) VALUES (%s, %s)",
                    (promo[1], idFactura))
                idPromociones.append(promo[1])
            b_cursor.execute(
                "INSERT INTO Venta (IdArticulo, IdFactura, Precio) VALUES (%s, %s, %s)",
                (idArticulo, idFactura, precio * (1 - descuento)))
            branch.commit()
            idArticulosVendidos.append(idArticulo)
            precioTotal += precio * (1 - descuento)

    w_cursor.execute("SELECT Puntos FROM Cliente WHERE IdCliente = %s", (idCliente,))
    puntos = w_cursor.fetchone()[0]
    puntosObtenidos = 0
    if idMetodoPago == 4:  # puntos
        if puntos < precioTotal * (1 + porcentajeImpuestos):
            b_cursor.execute(
                "DELETE FROM Factura WHERE IdFactura = %s",
                (idFactura,))
            b_cursor.execute(
                "DELETE FROM Venta WHERE IdFactura = %s",
                (idFactura,))
            branch.commit()
            for idArticulo in idArticulosVendidos:
                b_cursor.execute(
                    "UPDATE Articulo SET IdEstadoArticulo = %s WHERE IdArticulo = %s",
                    (estadoInventario, idArticulo))
            for idPromocion in idPromociones:
                b_cursor.execute(
                    "DELETE FROM PromocionFactura WHERE IdFactura = %s",
                    (idFactura,))
            puntosObtenidos = -1 * precioTotal * (1 + porcentajeImpuestos)
    else:
        puntosObtenidos = precioTotal * porcentajePuntos

    puntos += puntosObtenidos

    w_cursor.execute("UPDATE Cliente SET Puntos = %s WHERE IdCliente = %s", (puntos, idCliente))
    b_cursor.execute(
        "UPDATE Factura SET SubTotal = %s, Impuestos = %s, PuntosOtorgados = %s  WHERE IdFactura = %s",
        (precioTotal, precioTotal * porcentajeImpuestos, puntosObtenidos, idFactura))

    # close connections
    warehouse.commit()
    branch.commit()
    w_cursor.close()
    b_cursor.close()
    warehouse.close()
    branch.close()


def devolucion(idArticulo, codigoFactura, idCliente, idEmpleado, sucursal):
    branch = mysql.connector.connect(host="localhost", user="root", database=sucursal, passwd="salchipapa101")
    b_cursor = branch.cursor()

    b_cursor.callproc("GarantiaArticulo")
    for result in b_cursor.stored_results():
        garantia = result.fetchone()
        if garantia != None:
            garantia = garantia[0]
            if fecha < garantia:
                b_cursor.execute(
                    "SELECT Precio FROM Venta INNER JOIN Articulo A ON V.IdArticulo = A.IdArticulo WHERE A.IdArticulo = %s",
                    (idArticulo,))
                precio = result.fetchone()[0]

                b_cursor.execute(
                    "INSERT INTO Factura (Codigo, Fecha, SubTotal, IdCliente, IdEmpleado, IdMetodoPago) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (codigoFactura, fecha, -1 * precio, idCliente, idEmpleado, 3))  # devolucion en efectivo
                branch.commit()
                idFactura = b_cursor.lastrowid

                b_cursor.execute(
                    "INSERT INTO Venta (IdArticulo, IdFactura, Precio) VALUES (%s, %s, %s)",
                    (idArticulo, idFactura, -1 * precio))

                b_cursor.execute(
                    "UPDATE Articulo SET IdEstadoArticulo = %s WHERE IdArticulo = %s",
                    (4, idArticulo))
    branch.commit()
    b_cursor.close()
    branch.close()


cierreCaja("Ska8-4-TEC Alajuela")

#newSale([5, 10], "VE233", fecha, 0.1, 0.3, 1, 2, 1, "sk8")

#newPromo(290, "super promo", fecha, "2028-01-19 03:14:07", 20)

# insertCliente("207970282", "Marco", "Herrera", "Valverde", "12345678", "m.hsdfasdf", "07-10-1999", "lala", "lala",
#                "San Pedro", "lala")

