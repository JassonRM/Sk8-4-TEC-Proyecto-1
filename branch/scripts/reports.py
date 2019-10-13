import mysql.connector
import psycopg2

branch = mysql.connector.connect(
    host="localhost",
    user="root",
    database="sk8_branch",
    passwd="admin"
)

warehouse = psycopg2.connect(
    dbname="sk8_warehouse",
    user="postgres",
    password="admin"
)

warehouse_cursor = warehouse.cursor()
branch_cursor = branch.cursor()



"""
Moves all new data (bills, sales and promos) from branch to warehouse 
b_cursor: branch database cursor
w_cursor: warehouse database cursor
sucursal: name of the branch that is sending data
"""
def cierreCaja(b_cursor, w_cursor, sucursal):
    # get branch id
    w_cursor.execute("SELECT IdSucursal FROM Sucursal WHERE Nombre = %s", (sucursal,))
    idSucursal = w_cursor.fetchone()[0]

    # move facturas from branch to warehouse
    b_cursor.callproc("CierreCajaFacturas")
    for result in b_cursor.stored_results():
        for factura in result.fetchall():
            w_cursor.executemany(
                "INSERT INTO Factura (IdFacturaSucursal, Codigo, Fecha, SubTotal, Impuestos, PuntosOtorgados, IdCliente, IdEmpleado, IdMetodoPago, IdSucursal) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                factura + (idSucursal,))

    # move ventas from branch to warehouse
    b_cursor.callproc("CierreCajaVentas")
    for result in b_cursor.stored_results():
        for venta in result.fetchall():
            idFactura = w_cursor.execute(
                "SELECT IdFactura FROM Factura WHERE IdFacturaSucursal = %s AND IdSucursal = %s",
                (venta[1], idSucursal))
            w_cursor.executemany(
                "INSERT INTO Venta (IdArticulo, IdFactura, Precio) VALUES (%s, %s, %s)",
                (venta[0], idFactura, venta[2]))

    # move Promociones from branch to warehouse
    b_cursor.callproc("CierreCajaPromociones")
    for result in b_cursor.stored_results():
        for promocion in result.fetchall():
            w_cursor.executemany(
                "INSERT INTO Promocion (IdPromocionSucursal, IdSKU, Inicio, Fin, Descuento, IdSucursal) VALUES (%s, %s, %s, %s, %s, %s)",
                promocion + (idSucursal,))

    # move PromocionFactura from branch to warehouse
    b_cursor.callproc("CierreCajaPromocionFactura")
    for result in b_cursor.stored_results():
        for promocionFactura in result.fetchall():
            idFactura = w_cursor.execute(
                "SELECT IdFactura FROM Factura WHERE IdFacturaSucursal = %s AND IdSucursal = %s",
                (promocionFactura[1], idSucursal))
            w_cursor.executemany(
                "INSERT INTO PromocionFactura (IdPromocion, IdFactura) VALUES (%s, %s)",
                (promocionFactura[0], idFactura))
    warehouse.commit()
