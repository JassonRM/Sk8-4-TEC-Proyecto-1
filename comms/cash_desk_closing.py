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
