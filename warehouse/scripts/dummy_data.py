import psycopg2
from random import *
from pydbgen import pydbgen
import requests
import json

CantidadCamiones = 20
CantidadEmpleados = 15
CantidadProveedores = 10
CantidadPedidos = 30
CantidadSKUs = 500
CantidadArticulos = 15000

def createDummyData():
    # Create random generator
    gen = pydbgen.pydb()
    # Connect to an existing database and open a cursor to perform database operations
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="admin")
    cur = conn.cursor()

    # Create tables
    sql_file = open('warehouse/schema/table_creation.sql','r', encoding='utf-8')
    cur.execute(sql_file.read())

    # Create procedures
    sql_file = open('warehouse/queries/reports.sql','r', encoding='utf-8')
    cur.execute(sql_file.read())

    # Execute the inserts on each table

    # Add seeds
    sql_file = open('warehouse/schema/seeds.sql','r', encoding='utf-8')
    cur.execute(sql_file.read())

    # Fill table Camion
    placas = gen.gen_data_series(CantidadCamiones, data_type='license_plate')
    marcas = ["Freightliner", "International", "Kenworth", "Volvo", "Mercedes-Benz", "Hyundai"]
    estado = [0, 1]
    camiones = []
    for i in range(1, CantidadCamiones + 1):
        placa = placas[i-1]
        marca = choice(marcas)
        estado = randint(1, 2)
        camiones.append((i, placa, marca, estado))
    cur.executemany("INSERT INTO Camion (IdCamion, Placa, Marca, IdEstado) VALUES (%s, %s, %s, %s)", camiones)

    # Fill tables Canton and Distrito
    website = "https://ubicaciones.paginasweb.cr/provincia/"
    idcanton = 1
    cantones = []
    iddistrito = 1
    distritos = []
    for provincia in range(1, 8):
        r = requests.get(website + provincia.__str__() + "/cantones.json")
        requestCantones = r.json()
        for canton in requestCantones:
            cantones.append((idcanton, requestCantones[canton], provincia))
            r = requests.get(website + provincia.__str__() + "/canton/" + canton + "/distritos.json")
            requestsDistritos = r.json()
            for distrito in requestsDistritos:
                distritos.append((iddistrito, requestsDistritos[distrito], idcanton))
                iddistrito += 1
            idcanton += 1

    cur.executemany("INSERT INTO Canton (IdCanton, Nombre, IdProvincia) VALUES (%s, %s, %s)", cantones)
    cur.executemany("INSERT INTO Distrito (IdDistrito, Nombre, IdCanton) VALUES (%s, %s, %s)", distritos)

    # Add seeds2
    sql_file = open('warehouse/schema/seeds2.sql','r', encoding='utf-8')
    cur.execute(sql_file.read())

    # #Fill tables Empleado, Persona and Direccion
    empleados = []
    personas = []
    direcciones = []

    cur.execute("SELECT COUNT(*) FROM Sucursal")
    CantidadSucursales = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM Puesto")
    CantidadPuestos = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM Direccion")
    ContadorDireccion = cur.fetchone()[0]

    detalles1 = gen.gen_data_series(CantidadEmpleados, data_type='street_address')
    detalles2 = gen.gen_data_series(CantidadEmpleados, data_type='zipcode')
    cedulas = gen.gen_data_series(CantidadEmpleados, data_type='ssn')
    fakepersons = json.load(open("warehouse/scripts/fakepersons.json", 'r'))

    for i in range(1, CantidadEmpleados + 1):
        # Direccion
        detalle1 = detalles1[i-1]
        detalle2 = detalles2[i-1]
        distrito = randint(1, len(distritos))
        direcciones.append((ContadorDireccion + i, distrito, detalle1, detalle2))

        # Persona
        identificacion = cedulas[i-1]
        nombre = fakepersons[i-1]['Nombre']
        apellido1 = fakepersons[i-1]['Apellido1']
        apellido2 = fakepersons[i-1]['Apellido2']
        telefono = fakepersons[i-1]['Telefono']
        correo = fakepersons[i-1]['Correo']
        nacimiento = fakepersons[i-1]['FechaNacimiento']
        registro = fakepersons[i-1]['FechaRegistro']
        estado = randint(1, 2)
        personas.append((i, identificacion, nombre, apellido1, apellido2, telefono, correo, nacimiento, registro, estado, ContadorDireccion + i))

        # Empleados
        sucursal = randint(1, CantidadSucursales)
        puesto = randint(1, CantidadPuestos)
        salario = randint(400000, 1500000)
        fecha = fakepersons[i-1]['FechaRegistro']
        estado = randint(1, 2)
        empleados.append((i, i, puesto, sucursal, salario, fecha, estado))

    cur.executemany("INSERT INTO Direccion (IdDireccion, IdDistrito, Detalle1, Detalle2) VALUES (%s, %s, %s, %s)", direcciones)

    cur.executemany("INSERT INTO Persona (IdPersona, Identificacion, Nombre, Apellido1, Apellido2, Telefono, Correo, "
                    "FechaNacimiento, FechaRegistro, IdEstado, IdDireccion) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", personas)

    cur.executemany("INSERT INTO Empleado (IdEmpleado, IdPersona, IdPuesto, IdSucursal, Salario, Fecha, IdEstado) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)", empleados)


    # Fill table Proveedor
    nombres = gen.gen_data_series(CantidadProveedores, data_type='company')
    proveedores = []
    for i in range(1, CantidadProveedores + 1):
        nombre = nombres[i-1]
        estado = randint(1, 2)
        proveedores.append((i, nombre, estado))
    cur.executemany("INSERT INTO Proveedor (IdProveedor, Nombre, IdEstado) VALUES (%s, %s, %s)", proveedores)

    # Fill table Pedido
    fechas = gen.gen_data_series(CantidadPedidos, data_type='date')

    pedidos = []
    for i in range(1, CantidadPedidos + 1):
        fecha = fechas[i-1]
        proveedor = randint(1, CantidadProveedores)
        encargado = randint(1, CantidadEmpleados)
        estado = randint(1, 2)
        pedidos.append((i, fecha, proveedor, encargado))
    cur.executemany("INSERT INTO Pedido (IdPedido, Fecha, IdProveedor, IdEncargado) VALUES (%s, %s, %s, %s)", pedidos)

    # Fill table SKU
    codigos = gen.gen_data_series(CantidadSKUs, data_type='ssn')
    fechas = gen.gen_data_series(CantidadSKUs, data_type='date')
    garantias = [1, 2, 3, 12]
    detalles = ['Mostrador', 'Ventana', 'Pasillo principal', 'Pasillo de acuerdo a la categoria']

    cur.execute("SELECT COUNT(*) FROM Categoria")
    CantidadCategorias = cur.fetchone()[0]

    skus = []
    for i in range(1, CantidadSKUs + 1):
        codigo = codigos[i-1]
        categoria = randint(1, CantidadCategorias)
        estado = 1
        precio = randrange(5000, 50000, 500)
        fecha = fechas[i-1]
        garantia = choice(garantias)
        detalle = choice(detalles)
        skus.append((i, codigo, categoria, estado, precio, fecha, garantia, detalle))
    cur.executemany("INSERT INTO SKU (IdSKU, Codigo, IdCategoria, IdEstado, PrecioActual, FechaRegistro, Garantia, DetalleUbicacion)  "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", skus)

    # Fill table SucursalSKU
    sucursalSKUs = []
    for sku in range(1, CantidadSKUs):
        storeList = []
        for i in range(1, CantidadSucursales + 1):
            store = randint(1, CantidadSucursales)
            if store not in storeList:
                storeList.append(store)
                sucursalSKUs.append((sku, store))
            if random() > 0.35:
                break



    cur.executemany("INSERT INTO SucursalSKU (IdSKU, IdSucursal) VALUES  (%s, %s)", sucursalSKUs)

    # Fill table Articulo
    codigos = gen.gen_data_series(CantidadArticulos, data_type='ssn')

    articulos = []
    for i in range(1, CantidadArticulos + 1):
        sku = randint(1, len(skus))
        codigo = codigos[i-1]
        costo = randrange(500, 10000, 500)
        pedido = randint(1, CantidadPedidos)
        articulos.append((i, sku, codigo, costo, pedido, 1))
    cur.executemany("INSERT INTO Articulo (IdArticulo, IdSKU, Codigo, Costo, IdPedido, IdEstadoArticulo)  "
                    "VALUES (%s, %s, %s, %s, %s, %s)", articulos)


    # Make the changes to the database persistent
    conn.commit()

    # Close communication with the database
    cur.close()
    conn.close()

if __name__ == "__main__":
    createDummyData()