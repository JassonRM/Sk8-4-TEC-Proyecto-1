import psycopg2
from random import *
from pydbgen import pydbgen
import requests
import json

CantidadCamiones = 10
CantidadEmpleados = 15

# Create random generator
gen = pydbgen.pydb()

# Connect to an existing database and open a cursor to perform database operations
conn = psycopg2.connect(dbname="postgres", user="postgres", password="admin")
cur = conn.cursor()

# Execute the inserts on each table

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

# #Fill tables Empleado, Persona and Direccion
empleados = []
idpersona = 1
personas = []
direcciones = []

cur.execute("SELECT COUNT(*) FROM Sucursal")
CantidadSucursales = cur.fetchone()[0]

detalles1 = gen.gen_data_series(CantidadEmpleados, data_type='street_address')
detalles2 = gen.gen_data_series(CantidadEmpleados, data_type='zipcode')
cedulas = gen.gen_data_series(CantidadEmpleados, data_type='ssn')
fakepersons = json.load(open("fakepersons.json", 'r'))

for i in range(1, CantidadEmpleados + 1):
    # Direccion
    detalle1 = detalles1[i-1]
    detalle2 = detalles2[i-1]
    distrito = randint(1, len(distritos))
    direcciones.append((i, distrito, detalle1, detalle2))

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
    personas.append((i, identificacion, nombre, apellido1, apellido2, telefono, correo, nacimiento, registro, estado, i))

cur.executemany("INSERT INTO Direccion (IdDireccion, IdDistrito, Detalle1, Detalle2) VALUES (%s, %s, %s, %s)", direcciones)
cur.executemany("INSERT INTO Persona (IdPersona, Identificacion, Nombre, Apellido1, Apellido2, Telefono, Correo, FechaNacimiento, FechaRegistro, IdEstado, IdDireccion) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", personas)


# Make the changes to the database persistent
conn.commit()

# Close communication with the database
cur.close()
conn.close()
