import psycopg2
from pydbgen import pydbgen
import datetime
import mysql.connector
from random import *

fecha = datetime.datetime.now().strftime("%Y-%m-%d")

def initBranches():
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


    # Insert Pais, Provincia, Canton, Distrito
    # Paises
    warehousedb.execute("SELECT * FROM Pais")
    paises = warehousedb.fetchall()

    # Provincias
    warehousedb.execute("SELECT * FROM Provincia")
    provincias = warehousedb.fetchall()

    # Cantones
    warehousedb.execute("SELECT * FROM Canton")
    cantones = warehousedb.fetchall()

    # Distritos
    warehousedb.execute("SELECT * FROM Distrito")
    distritos = warehousedb.fetchall()

    # Categorias
    warehousedb.execute("SELECT * FROM Categoria")
    categorias = warehousedb.fetchall()

    # Estado
    warehousedb.execute("SELECT * FROM Estado")
    estados = warehousedb.fetchall()

    # Estado articulo
    warehousedb.execute("SELECT * FROM EstadoArticulo")
    estadosArticulo = warehousedb.fetchall()

    # Puestos
    warehousedb.execute("SELECT * FROM Puesto")
    puestos = warehousedb.fetchall()

    # Metodo de pago
    warehousedb.execute("SELECT * FROM MetodoPago")
    metodos = warehousedb.fetchall()

    for i in range(0, len(branchList)):
        cursorList[i].execute("USE sk8;")
        cursorList[i].executemany("INSERT INTO Pais (IdPais, Nombre) VALUES (%s, %s)",
                                  paises)
        cursorList[i].executemany("INSERT INTO Provincia (IdProvincia, Nombre, IdPais) VALUES (%s, %s, %s)",
                                  provincias)
        cursorList[i].executemany("INSERT INTO Canton (IdCanton, Nombre, IdProvincia) VALUES (%s, %s, %s)",
                          cantones)
        cursorList[i].executemany("INSERT INTO Distrito (IdDistrito, Nombre, IdCanton) VALUES (%s, %s, %s)",
                          distritos)
        cursorList[i].executemany("INSERT INTO Categoria (IdCategoria, Nombre, Descripcion) VALUES (%s, %s, %s)",
            categorias)
        cursorList[i].executemany("INSERT INTO Estado (IdEstado, Descripcion) VALUES (%s, %s)",
            estados)
        cursorList[i].executemany("INSERT INTO EstadoArticulo (IdEstadoArticulo, Nombre) VALUES (%s, %s)",
            estadosArticulo)
        cursorList[i].executemany("INSERT INTO Puesto (IdPuesto, Nombre, Descripcion) VALUES (%s, %s, %s)",
            puestos)
        cursorList[i].executemany("INSERT INTO MetodoPago (IdMetodoPago, Metodo, Descripcion) VALUES (%s, %s, %s)",
            metodos)

        # SKUs
        warehousedb.execute("SELECT sku.* FROM sku INNER JOIN sucursalsku s on sku.idsku = s.idsku WHERE idsucursal = %s", (i+1,))
        skus = warehousedb.fetchall()
        cursorList[i].executemany("INSERT INTO SKU (IdSKU, Codigo, IdCategoria, IdEstado, PrecioActual, FechaRegistro, Garantia, DetalleUbicacion)  VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", skus)

        branchList[i].commit()
        cursorList[i].close()
        branchList[i].close()


    # Close communication with the database
    warehousedb.close()
    conn.close()


if __name__ == "__main__":
    initBranches()