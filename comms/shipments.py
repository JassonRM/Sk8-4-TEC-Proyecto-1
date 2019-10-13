import psycopg2
from pydbgen import pydbgen
import datetime
import mysql.connector
from random import *

fecha = datetime.datetime.now().strftime("%Y-%m-%d")

def generateShipments():
    # Create random generator
    gen = pydbgen.pydb()

    # Connect to the warehouse database and open a cursor to perform database operations
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="admin")
    warehousedb = conn.cursor()


    # Connect to the store 1 database and open a cursor to perform database operations
    branch1 = mysql.connector.connect(
        host="0.0.0.0",
        port="3306",
        user="root",
        passwd="admin"
    )
    branch1db = branch1.cursor()

    # # Connect to the store 2 database and open a cursor to perform database operations
    # branch2 = mysql.connector.connect(
    #     host="0.0.0.0",
    #     port="3307",
    #     user="root",
    #     passwd="admin"
    # )
    # branch2db = branch2.cursor()
    #
    # # Connect to the store 3 database and open a cursor to perform database operations
    # branch3 = mysql.connector.connect(
    #     host="0.0.0.0",
    #     port="3308",
    #     user="root",
    #     passwd="admin"
    # )
    # branch3db = branch3.cursor()

    branchList = [branch1]
    cursorList = [branch1db]

    # Generate shipments with a truck

    warehousedb.execute("SELECT COUNT(*) FROM Sucursal")
    CantidadEnvios = warehousedb.fetchone()[0]

    warehousedb.execute("SELECT IdCamion FROM camion where idestado = %s",
                (1,))
    camionesDisponibles = warehousedb.fetchall()
    camiones = choices(camionesDisponibles, k=CantidadEnvios)

    warehousedb.execute("SELECT COUNT(*) FROM Empleado")
    CantidadEmpleados = warehousedb.fetchone()[0]

    warehousedb.execute("SELECT COUNT(*) FROM Envio")
    EnviosPrevios = warehousedb.fetchone()[0]

    envios = []
    for i in range(1, CantidadEnvios + 1):
        idEnvio = EnviosPrevios + i
        camion = camiones[i-1][0]
        encargado = randint(1, CantidadEmpleados)
        envios.append((idEnvio, camion, encargado, i, fecha))
    warehousedb.executemany(
        "INSERT INTO Envio (IdEnvio, IdCamion, IdEncargado, IdSucursal, Fecha) VALUES (%s, %s, %s, %s, %s)",
        envios)

    warehousedb.execute("SELECT IdSKU FROM SKU WHERE IdEstado = 1")
    skus = warehousedb.fetchall()

    for sku in skus:
        id = sku[0]
        warehousedb.execute("SELECT IdSucursal FROM SucursalSKU WHERE IdSKU = %s", (id,))
        storelist = warehousedb.fetchall()
        warehousedb.execute("SELECT IdArticulo FROM Articulo WHERE idestadoarticulo = 1 AND IdSKU = %s", (id,))
        itemlist = warehousedb.fetchall()

        if itemlist != []:
            storeNeeds = []
            for store in storelist:
                storeId = store[0]
                warehousedb.execute("SELECT COUNT(*) FROM Articulo WHERE IdSKU = %s AND idsucursal = %s AND IdEstadoArticulo = 2", (id, storeId))
                stock = warehousedb.fetchone()[0]
                if stock < 5:
                    storeNeeds.append(store)
            if len(itemlist) > len(storeNeeds) * 6:
                ammount = 6
            else:
                ammount = len(itemlist) // len(storeNeeds)

            for store in storeNeeds:
                articulos = itemlist[0:ammount]
                itemlist = itemlist[ammount:]
                for articulo in articulos:
                    id = articulo[0]
                    warehousedb.execute("UPDATE Articulo SET IdEstadoArticulo = 2, IdSucursal = %s WHERE IdArticulo = %s", (store, id))
                    warehousedb.execute("INSERT INTO EnvioPaquete (IdEnvio, IdArticulo) VALUES (%s, %s)", (EnviosPrevios + store[0], id))

    # Fragmentation


    for i in range(0, len(branchList)):
        cursorList[i].execute("USE sk8;")
        # SKUs
        warehousedb.execute("SELECT sku.* FROM sku INNER JOIN sucursalsku s on sku.idsku = s.idsku WHERE idsucursal = %s AND fecharegistro = %s", (i+1,fecha))
        skus = warehousedb.fetchall()
        cursorList[i].executemany("INSERT INTO SKU (IdSKU, Codigo, IdCategoria, IdEstado, PrecioActual, FechaRegistro, Garantia, DetalleUbicacion)  VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", skus)

        # Articulos
        warehousedb.execute("SELECT a.IdArticulo, a.IdSKU, a.Codigo, a.IdEstadoArticulo FROM articulo a INNER JOIN enviopaquete e on a.idarticulo = e.idarticulo INNER JOIN envio e2 on e.idenvio = e2.idenvio WHERE e2.idsucursal = %s AND e2.fecha = %s",
            (i+1, fecha))
        articulos = warehousedb.fetchall()
        cursorList[i].executemany("INSERT INTO Articulo (IdArticulo, IdSKU, Codigo, IdEstadoArticulo) VALUES (%s, %s, %s, %s)",
                                  articulos)

        branchList[i].commit()
        cursorList[i].close()
        branchList[i].close()


    # Make the changes to the database persistent
    conn.commit()

    # Close communication with the database
    warehousedb.close()
    conn.close()

if __name__ == "__main__":
    generateShipments()