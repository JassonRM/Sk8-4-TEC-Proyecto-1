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
        host="localhost",
        port="3306",
        user="root",
        database="Ska8-4-TEC-Alajuela",
        passwd="admin"
    )
    branch1db = branch1.cursor()

    # Connect to the store 2 database and open a cursor to perform database operations
    branch2 = mysql.connector.connect(
        host="0.0.0.0",
        port="3307",
        user="root",
        database="Ska8-4-TEC-Cartago",
        passwd="admin"
    )
    branch2db = branch2.cursor()

    # Connect to the store 3 database and open a cursor to perform database operations
    branch3 = mysql.connector.connect(
        host="0.0.0.0",
        port="3308",
        user="root",
        database="Ska8-4-TEC-San-Jose",
        passwd="admin"
    )
    branch3db = branch3.cursor()

    branchList = [branch1, branch2, branch3]
    cursorList = [branch1db, branch2db, branch3db]


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
        # Create tables
        sql_file = open('branch/schema/table_creation.sql', 'r', encoding='utf-8')
        queries = sql_file.read().split(';')
        for query in queries:
            if query != None:
                cursorList[i].execute(query)

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

        # Direccion
        warehousedb.execute("SELECT D.* FROM Direccion D INNER JOIN Persona P on D.iddireccion = P.iddireccion "
                            "INNER JOIN Empleado E on P.idpersona = E.idpersona WHERE E.idsucursal = %s", (i+1,))
        direcciones = warehousedb.fetchall()

        cursorList[i].executemany(
            "INSERT INTO Direccion (IdDireccion, IdDistrito, Detalle1, Detalle2) VALUES (%s, %s, %s, %s)",
            direcciones)

        # Persona
        warehousedb.execute("SELECT P.* FROM Persona P INNER JOIN Empleado E on P.idpersona = E.idpersona WHERE E.idsucursal = %s", (i+1,))
        personas = warehousedb.fetchall()

        cursorList[i].executemany(
            "INSERT INTO Persona (IdPersona, Identificacion, Nombre, Apellido1, Apellido2, Telefono, Correo, FechaNacimiento,"
            " FechaRegistro, IdEstado, IdDireccion) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            personas)

        # Empleado
        warehousedb.execute(
            "SELECT IdEmpleado, IdPersona, IdPuesto, Salario, Fecha, IdEstado FROM Empleado WHERE IdSucursal = %s",
            (i+1,))
        empleados = warehousedb.fetchall()

        cursorList[i].executemany(
            "INSERT INTO Empleado (IdEmpleado, IdPersona, IdPuesto, Salario, Fecha, IdEstado) VALUES (%s, %s, %s, %s, %s, %s)",
            empleados)

        # SKUs
        warehousedb.execute("SELECT sku.* FROM sku INNER JOIN sucursalsku s on sku.idsku = s.idsku WHERE idsucursal = %s "
                            "AND idestado = 1", (i+1,))
        skus = warehousedb.fetchall()
        cursorList[i].executemany("INSERT INTO SKU (IdSKU, Codigo, IdCategoria, IdEstado, PrecioActual, FechaRegistro, "
                                  "Garantia, DetalleUbicacion)  VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", skus)

        branchList[i].commit()
        cursorList[i].close()
        branchList[i].close()


    # Close communication with the database
    warehousedb.close()
    conn.close()


if __name__ == "__main__":
    initBranches()