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
            "INSERT INTO Persona (IdPersona, Identificacion, Nombre, Apellido1, Apellido2, Telefono, Correo, "
            "FechaNacimiento, FechaRegistro, IdEstado, IdDireccion) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
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


def insertVenta(articulos, codigoFactura, porcentajeImpuestos, porcentajePuntos,
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
    idPromociones = []
    idArticulosDisponibles = []
    precios = []
    precioTotal  = 0

    # get articulos that can actually be sold, their prices and promos
    for idArticulo in articulos:

        b_cursor.execute("SELECT A.IdArticulo, S.PrecioActual FROM SKU S INNER JOIN Articulo A ON S.IdSKU = A.IdSKU "
                         "WHERE A.IdArticulo = %s AND IdEstadoArticulo = %s", (idArticulo, estadoInventario))

        articulo = b_cursor.fetchone()
        if  articulo == None:
            break

        idArticulosDisponibles.append(articulo[0])
        precio = articulo[1]
        precios.append(precio)

        #get promociones for Articulo
        b_cursor.execute(
            "SELECT P.Descuento, P.IdPromocion FROM  SKU S INNER JOIN Promocion P  ON  S.IdSKU = P.IdSKU "
            "INNER JOIN Articulo A ON P.IdSKU = A.IdSKU WHERE A.IdArticulo = %s AND P.Fin > %s LIMIT 1",
            (idArticulo, fecha))
        promo = b_cursor.fetchone()

        #calculate total price
        if promo != None:
            idPromociones.append(promo[1])
            precioTotal += (1 - promo[0]/100) * precio
        else:
            precioTotal += precio

    if len(idArticulosDisponibles) == 0:
        return

    # calculate points
    puntosObtenidos = precioTotal * porcentajePuntos


    w_cursor.execute("SELECT Puntos FROM Cliente WHERE IdCliente = %s", (idCliente,))
    puntosCliente = w_cursor.fetchone()[0]

    if idMetodoPago == 4:  # puntos
        puntosObtenidos = -1 * precioTotal
        # abort sale if Cliente doesn't have enough points
        if puntosCliente < precioTotal * (1 + porcentajeImpuestos):
            return

    b_cursor.execute(
            "INSERT INTO Factura (Codigo, Fecha, SubTotal, Impuestos, PuntosOtorgados, IdCliente, IdEmpleado, IdMetodoPago)"
            " VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (codigoFactura, fecha, precioTotal, precioTotal * porcentajeImpuestos, puntosObtenidos, idCliente, idEmpleado, idMetodoPago))

    branch.commit()

    b_cursor.execute("SELECT COUNT(*) FROM Factura")
    idFactura = b_cursor.fetchone()[0]

    # change state of Articulo to vendido
    for idArticulo in idArticulosDisponibles:
        b_cursor.execute("UPDATE Articulo SET IdEstadoArticulo = %s WHERE IdArticulo = %s",
                         (estadoVendido, idArticulo))

    for promo in idPromociones:
        b_cursor.execute(
            "INSERT INTO PromocionFactura (IdPromocion, IdFactura) VALUES (%s, %s)",
            (promo, idFactura))

    i = 0
    for precio in precios:
        b_cursor.execute(
            "INSERT INTO Venta (IdArticulo, IdFactura, Precio) VALUES (%s, %s, %s)",
            (idArticulosDisponibles[i], idFactura, precio))
        i += 1

        # update Puntos for Cliente
    puntosCliente += puntosObtenidos
    w_cursor.execute("UPDATE Cliente SET Puntos = %s WHERE IdCliente = %s", (puntosCliente, idCliente))

    # Make the changes to the database persistent
    warehouse.commit()
    branch.commit()

    # close connections
    w_cursor.close()
    b_cursor.close()
    warehouse.close()
    branch.close()


def devolucion(idArticulo, codigoFactura, idCliente, idEmpleado):
    # Connect to an existing database and open a cursor to perform database operations
    branch = mysql.connector.connect(host=BRANCH_DB_HOST, port=BRANCH_DB_PORT, user=BRANCH_DB_USER, database=BRANCH_DB,
                                     passwd=BRANCH_DB_PASSWD)
    b_cursor = branch.cursor()

    # Check Garantia date for Articulo
    b_cursor.callproc("GarantiaArticulo", (idArticulo,))
    date = datetime.datetime.strptime(fecha, '%Y-%m-%d').date()
    garantia = date
    for resultado in b_cursor.stored_results():
        garantia = resultado.fetchone()[0]

    if date < garantia:
        # check Precio when it was sold
        b_cursor.execute(
            "SELECT V.Precio FROM Venta V INNER JOIN Articulo A ON V.IdArticulo = A.IdArticulo WHERE A.IdArticulo = %s",
            (idArticulo,))
        precio = b_cursor.fetchone()[0]

        # create Factura for return
        b_cursor.execute(
            "INSERT INTO Factura (Codigo, Fecha, SubTotal, IdCliente, IdEmpleado, IdMetodoPago, Impuestos, PuntosOtorgados) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
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
    # cierreCaja()
    # updateBranchDB("Ska8-4-TEC-Cartago", "0.0.0.0", 3307, "root", "admin")
    # cierreCaja()
    # updateBranchDB("Ska8-4-TEC-San-Jose", "0.0.0.0", 3308, "root", "admin")
    # cierreCaja()

    # Ejemplos

    # insertCliente("469-68-0955", "Carlos", "R", "M", "379832", "cal@icloud.com", '01-24-1990', "Tec", "Cartago", 34, "Buen cliente")
    # insertCliente("20390294", "Maria", "R", "M", "379832",
    #               "cal@icloud.com", '01-24-1990', "Tec", "Cartago", 35,
    #               "Buen cliente")
    # insertVenta([9, 15], "AMB123", fecha, 0.13,
    #             0.05,
    #             1, 13, 1)
    # insertPromocion(17, "Mitad de precio", "2019-10-13 00:00:00", "2020-11-28 00:00:00", 50)
    insertVenta([20], "AMB250", fecha, 0.13,
                0.05,
                1, 13, 1)
    # devolucion(20, "DEV001", 2, 13, fecha)