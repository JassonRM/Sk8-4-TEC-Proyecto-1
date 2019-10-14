import mysql.connector
import psycopg2
import datetime

WAREHOUSE_DB = "postgres"
WAREHOUSE_DB_USER = "postgres"
WAREHOUSE_DB_PASSWD = "admin"

BRANCH_DB = ""
BRANCH_DB_HOST = "localhost"
BRANCH_DB_USER = "root"
BRANCH_DB_PASSWD = "admin"
BRANCH_DB_PORT = "3306"

fecha = datetime.datetime.now().strftime("%Y-%m-%d")


def updateWarehouseDB(db, user, password):
    global WAREHOUSE_DB
    global WAREHOUSE_DB_USER
    global WAREHOUSE_DB_PASSWD

    WAREHOUSE_DB = db
    WAREHOUSE_DB_USER = user
    WAREHOUSE_DB_PASSWD = password


def updateBranchDB(db, host, port, user, password):
    global BRANCH_DB
    global BRANCH_DB_HOST
    global BRANCH_DB_PORT
    global BRANCH_DB_USER
    global BRANCH_DB_PASSWD

    BRANCH_DB = db
    BRANCH_DB_HOST = host
    BRANCH_DB_PORT = port
    BRANCH_DB_USER = user
    BRANCH_DB_PASSWD = password


"""
Moves all new data (bills, sales and promos) from branch to warehouse 
b_cursor: branch database cursor
w_cursor: warehouse database cursor
sucursal: name of the branch that is sending data
"""


def cierreCaja():
    # Connect to an existing database and open a cursor to perform database operations
    branch = mysql.connector.connect(host=BRANCH_DB_HOST, port=BRANCH_DB_PORT, user=BRANCH_DB_USER, database=BRANCH_DB,
                                     passwd=BRANCH_DB_PASSWD)
    warehouse = psycopg2.connect(dbname=WAREHOUSE_DB, user=WAREHOUSE_DB_USER, password=WAREHOUSE_DB_PASSWD)
    w_cursor = warehouse.cursor()
    b_cursor = branch.cursor()

    # get branch id
    w_cursor.execute("SELECT IdSucursal FROM Sucursal WHERE Nombre = %s", (BRANCH_DB,))
    idSucursal = w_cursor.fetchone()[0]

    # move facturas from branch to warehouse
    b_cursor.callproc("CierreCajaFacturas", (fecha,))
    for resultado in b_cursor.stored_results():
        for factura in resultado.fetchall():
            print("Factura")
            w_cursor.execute(
                "INSERT INTO Factura (IdFacturaSucursal, Codigo, Fecha, SubTotal, Impuestos, PuntosOtorgados, IdCliente, IdEmpleado, IdMetodoPago, IdSucursal) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                factura + (idSucursal,))
    warehouse.commit()

    # move ventas from branch to warehouse
    b_cursor.callproc("CierreCajaVentas", (fecha,))
    for resultado in b_cursor.stored_results():
        for venta in resultado.fetchall():
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
    for resultado in b_cursor.stored_results():
        for promocion in resultado.fetchall():
            print("Promocion")
            w_cursor.execute(
                "INSERT INTO Promocion (IdPromocionSucursal, IdSKU, Descripcion, Inicio, Fin, Descuento, IdSucursal) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                promocion + (idSucursal,))

    warehouse.commit()

    # move PromocionFactura from branch to warehouse
    b_cursor.callproc("CierreCajaPromocionFactura", (fecha,))
    for resultado in b_cursor.stored_results():
        for promocionFactura in resultado.fetchall():
            w_cursor.execute(
                "SELECT IdFactura FROM Factura WHERE IdFacturaSucursal = %s AND IdSucursal = %s",
                (promocionFactura[1], idSucursal))
            idFactura = w_cursor.fetchone()[0]
            w_cursor.execute(
                "INSERT INTO PromocionFactura (IdPromocion, IdFactura) VALUES (%s, %s)",
                (promocionFactura[0], idFactura))

    # make changes permanent
    warehouse.commit()
    branch.commit()

    # close connections
    w_cursor.close()
    b_cursor.close()
    warehouse.close()
    branch.close()


def insertCliente(identificacion, nombre, apellido1, apellido2, telefono, correo, fechaNacimiento, direccion1,
                  direccion2, iddistrito, descripcion):
    # Connect to an existing database and open a cursor to perform database operations
    warehouse = psycopg2.connect(dbname=WAREHOUSE_DB, user=WAREHOUSE_DB_USER, password=WAREHOUSE_DB_PASSWD)
    w_cursor = warehouse.cursor()

    w_cursor.execute("SELECT COUNT(*) FROM Persona")
    CantidadPersonas = w_cursor.fetchone()[0]
    w_cursor.execute("SELECT COUNT(*) FROM Direccion")
    CantidadDirecciones = w_cursor.fetchone()[0]

    # Check if Persona exists
    w_cursor.execute("SELECT IdPersona FROM persona where identificacion = %s", (identificacion,))
    idPersona = w_cursor.fetchone()
    if idPersona != None:
        idPersona = idPersona[0]
    else:
        # Insert Persona and Direccion
        w_cursor.execute(
            "INSERT INTO Direccion (IdDireccion, IdDistrito, Detalle1, Detalle2) VALUES (%s, %s, %s, %s)",
            (CantidadDirecciones + 1, iddistrito, direccion1, direccion2))
        warehouse.commit()
        idDireccion = CantidadDirecciones + 1
        persona = (CantidadPersonas + 1,
            identificacion, nombre, apellido1, apellido2, telefono, correo, fechaNacimiento, fecha, 1, idDireccion)
        w_cursor.execute(
            "INSERT INTO Persona (IdPersona, Identificacion, Nombre, Apellido1, Apellido2, Telefono, Correo, FechaNacimiento, FechaRegistro, IdEstado, IdDireccion) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            persona)
        warehouse.commit()
        idPersona = CantidadPersonas + 1

    # Insert Cliente
    estado = 1
    cliente = (idPersona, descripcion, 0, fecha, estado)
    w_cursor.execute(
        "INSERT INTO Cliente (IdPersona, Descripcion, Puntos, FechaRegistro, IdEstado) VALUES (%s, %s, %s, %s, %s)",
        cliente)

    # Make the changes to the database persistent
    warehouse.commit()

    # Close communication with the database
    w_cursor.close()
    warehouse.close()
    return


def insertPromocion(idSKU, descripcion, inicio, fin, descuento):
    # Connect to an existing database and open a cursor to perform database operations
    branch = mysql.connector.connect(host=BRANCH_DB_HOST, port=BRANCH_DB_PORT, user=BRANCH_DB_USER, database=BRANCH_DB,
                                     passwd=BRANCH_DB_PASSWD)
    b_cursor = branch.cursor()

    # Insert Promo
    promocion = (idSKU, descripcion, inicio, fin, descuento)
    b_cursor.execute(
        "INSERT INTO Promocion (IdSKU, Descripcion, Inicio, Fin, Descuento) VALUES (%s, %s, %s, %s, %s)",
        promocion)

    # Make the changes to the database persistent
    branch.commit()

    # close connections
    b_cursor.close()
    branch.close()


def insertVenta(articulos, codigoFactura, fecha, porcentajeImpuestos, porcentajePuntos,
                idCliente, idEmpleado, idMetodoPago):
    # Connect to an existing database and open a cursor to perform database operations
    branch = mysql.connector.connect(host=BRANCH_DB_HOST, port=BRANCH_DB_PORT, user=BRANCH_DB_USER, database=BRANCH_DB,
                                     passwd=BRANCH_DB_PASSWD)
    warehouse = psycopg2.connect(dbname=WAREHOUSE_DB, user=WAREHOUSE_DB_USER, password=WAREHOUSE_DB_PASSWD)
    w_cursor = warehouse.cursor()
    b_cursor = branch.cursor()

    # estadoArticulo for a sold article
    estadoVendido = 3

    # estadoArticulo for an article in the store
    estadoInventario = 2

    # temporary variables to avoid repeating queries
    precioTotal = 0
    crearFactura = True
    idFactura = 0
    idArticulosVendidos = []
    idPromociones = []

    for idArticulo in articulos:
        # change state of Articulo to sold
        b_cursor.execute("UPDATE Articulo SET IdEstadoArticulo = %s WHERE IdArticulo = %s AND IdEstadoArticulo = %s ",
                         (estadoVendido, idArticulo, estadoInventario))
        branch.commit()

        # check if Articulo is not sold
        if b_cursor.rowcount != 0:

            # create a new Factura
            if crearFactura:
                crearFactura = False
                b_cursor.execute(
                    "INSERT INTO Factura (Codigo, Fecha, IdCliente, IdEmpleado, IdMetodoPago) VALUES (%s, %s, %s, %s, %s)",
                    (codigoFactura, fecha, idCliente, idEmpleado, idMetodoPago))
                branch.commit()
                idFactura = b_cursor.lastrowid

            # get the price for each Articulo
            b_cursor.execute(
                "SELECT S.PrecioActual FROM SKU S INNER JOIN Articulo A ON S.IdSKU = A.IdSKU WHERE A.IdArticulo = %s",
                (idArticulo,))
            precio = b_cursor.fetchone()[0]

            # check if there are any Promociones for the Articulo
            b_cursor.execute(
                "SELECT P.Descuento, P.IdPromocion FROM  SKU S INNER JOIN Promocion P  ON  S.IdSKU = P.IdSKU INNER JOIN Articulo A ON P.IdSKU = A.IdSKU WHERE A.IdArticulo = %s AND P.Fin > CURRENT_TIMESTAMP()",
                (idArticulo,))
            promo = b_cursor.fetchone()
            descuento = 0

            # calculate discount if there is a Promocion
            if promo != None:
                descuento = promo[0] / 100
                b_cursor.execute(
                    "INSERT INTO PromocionFactura (IdPromocion, IdFactura) VALUES (%s, %s)",
                    (promo[1], idFactura))
                idPromociones.append(promo[1])

            # link Articulos to Factura
            b_cursor.execute(
                "INSERT INTO Venta (IdArticulo, IdFactura, Precio) VALUES (%s, %s, %s)",
                (idArticulo, idFactura, precio * (1 - descuento)))
            branch.commit()
            idArticulosVendidos.append(idArticulo)
            precioTotal += precio * (1 - descuento)

    # retrieve Puntos for the Cliente
    w_cursor.execute("SELECT Puntos FROM Cliente WHERE IdCliente = %s", (idCliente,))
    puntos = w_cursor.fetchone()[0]
    puntosObtenidos = 0

    # check if payment is with Puntos
    if idMetodoPago == 4:  # puntos

        # abort sale if Cliente doesn't have enough points
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

    # update Puntos for Cliente
    puntos += puntosObtenidos
    w_cursor.execute("UPDATE Cliente SET Puntos = %s WHERE IdCliente = %s", (puntos, idCliente))

    # update payment info in Factura
    b_cursor.execute(
        "UPDATE Factura SET SubTotal = %s, Impuestos = %s, PuntosOtorgados = %s  WHERE IdFactura = %s",
        (precioTotal, precioTotal * porcentajeImpuestos, puntosObtenidos, idFactura))

    # Make the changes to the database persistent
    warehouse.commit()
    branch.commit()

    # close connections
    w_cursor.close()
    b_cursor.close()
    warehouse.close()
    branch.close()


def devolucion(idArticulo, codigoFactura, idCliente, idEmpleado, fecha):
    # Connect to an existing database and open a cursor to perform database operations
    branch = mysql.connector.connect(host=BRANCH_DB_HOST, port=BRANCH_DB_PORT, user=BRANCH_DB_USER, database=BRANCH_DB,
                                     passwd=BRANCH_DB_PASSWD)
    b_cursor = branch.cursor()

    # Check Garantia date for Articulo
    b_cursor.callproc("GarantiaArticulo", (idArticulo,))
    fecha = datetime.datetime.strptime(fecha, '%Y-%m-%d').date()
    garantia = fecha
    for resultado in b_cursor.stored_results():
        garantia = resultado.fetchone()[0]

    if fecha < garantia:
        # check Precio when it was sold
        b_cursor.execute(
            "SELECT V.Precio FROM Venta V INNER JOIN Articulo A ON V.IdArticulo = A.IdArticulo WHERE A.IdArticulo = %s",
            (idArticulo,))
        precio = b_cursor.fetchone()[0]

        # create Factura for return
        b_cursor.execute(
            "INSERT INTO Factura (Codigo, Fecha, SubTotal, IdCliente, IdEmpleado, IdMetodoPago, Impuestos, PuntosOtorgados) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (codigoFactura, fecha, -1 * precio, idCliente, idEmpleado, 3, 0, 0))  # devolucion en efectivo
        branch.commit()
        idFactura = b_cursor.lastrowid

        # link Articulo and Factura with a Venta
        b_cursor.execute(
            "INSERT INTO Venta (IdArticulo, IdFactura, Precio) VALUES (%s, %s, %s)",
            (idArticulo, idFactura, -1 * precio))

        # update the state of Articulo
        b_cursor.execute(
            "UPDATE Articulo SET IdEstadoArticulo = %s WHERE IdArticulo = %s",
            (4, idArticulo))

    # Make the changes to the database persistent
    branch.commit()

    # close connections
    b_cursor.close()
    branch.close()


if __name__ == "__main__":
    updateBranchDB("Ska8-4-TEC-Alajuela", "0.0.0.0", 3306, "root", "admin")
    cierreCaja()
    updateBranchDB("Ska8-4-TEC-Cartago", "0.0.0.0", 3307, "root", "admin")
    cierreCaja()
    updateBranchDB("Ska8-4-TEC-San-Jose", "0.0.0.0", 3308, "root", "admin")
    cierreCaja()

    # Ejemplos

    # insertCliente("469-68-0955", "Carlos", "R", "M", "379832", "cal@icloud.com", '01-24-1990', "Tec", "Cartago", 34, "Buen cliente")
    # insertCliente("20390294", "Maria", "R", "M", "379832",
    #               "cal@icloud.com", '01-24-1990', "Tec", "Cartago", 35,
    #               "Buen cliente")
    # insertVenta([9, 15], "AMB123", fecha, 0.13,
    #             0.05,
    #             1, 13, 1)
    # insertPromocion(17, "Mitad de precio", "2018-11-28 00:00:00", "2020-11-28 00:00:00", 50)
    # insertVenta([20], "AMB250", fecha, 0.13,
    #             0.05,
    #             1, 13, 1)
    # devolucion(20, "DEV001", 2, 13, fecha)