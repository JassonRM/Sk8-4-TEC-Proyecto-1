import psycopg2
from pydbgen import pydbgen
import datetime

fecha = datetime.datetime.now().strftime("%Y-%m-%d")

def insertEmpleado(identificacion, nombre, apellido1, apellido2, telefono, correo, fechaNacimiento, direccion1, direccion2, iddistrito, puesto, codSucursal, salario):

    # Connect to an existing database and open a cursor to perform database operations
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="admin")
    cur = conn.cursor()

    # Check if Persona exists
    cur.execute("SELECT IdPersona FROM persona where identificacion = %s", (identificacion,))
    idpersona = cur.fetchone()
    if idpersona != None:
        idpersona = idpersona[0]
    else:
        # Insert Persona and Direccion
        cur.execute("SELECT COUNT(*) FROM Persona")
        CantidadPersonas = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM Direccion")
        CantidadDirecciones = cur.fetchone()[0]

        direccion = (CantidadDirecciones + 1, iddistrito, direccion1, direccion2)
        cur.execute(
            "INSERT INTO Direccion (IdDireccion, IdDistrito, Detalle1, Detalle2) VALUES (%s, %s, %s, %s)",
            direccion)

        idpersona = CantidadPersonas + 1
        persona = (idpersona, identificacion, nombre, apellido1, apellido2, telefono, correo, fechaNacimiento, fecha, 1, CantidadDirecciones + 1)
        cur.execute(
            "INSERT INTO Persona (IdPersona, Identificacion, Nombre, Apellido1, Apellido2, Telefono, Correo, FechaNacimiento, FechaRegistro, IdEstado, IdDireccion) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            persona)

    # Insert Empleado

    cur.execute("SELECT COUNT(*) FROM Empleado")
    CantidadEmpleados = cur.fetchone()[0]
    cur.execute("SELECT IdSucursal FROM sucursal where codigo = %s",
                (codSucursal,))
    sucursal = cur.fetchone()[0]
    cur.execute("SELECT IdPuesto FROM puesto where nombre = %s",
                (puesto,))
    puesto = cur.fetchone()[0]
    estado = 1
    empleado = (
    CantidadEmpleados + 1, idpersona, puesto, sucursal, salario, fecha, estado)
    cur.execute(
        "INSERT INTO Empleado (IdEmpleado, IdPersona, IdPuesto, IdSucursal, Salario, Fecha, IdEstado) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        empleado)

    # Make the changes to the database persistent
    conn.commit()

    # Close communication with the database
    cur.close()
    conn.close()


def insertPedido(proveedor, idempleado, codigoSKU, precioSKU, garantia, categoria, detalleUbicacion, costo, cantidad, sucursales):

    # Create random generator
    gen = pydbgen.pydb()

    # Connect to an existing database and open a cursor to perform database operations
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="admin")
    cur = conn.cursor()

    cur.execute("SELECT IdProveedor FROM proveedor where nombre = %s",
                (proveedor,))
    idproveedor = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM Pedido")
    CantidadPedidos = cur.fetchone()[0]
    idpedido = CantidadPedidos + 1
    pedido = (idpedido, fecha, idproveedor, idempleado)
    cur.execute("INSERT INTO Pedido (IdPedido, Fecha, IdProveedor, IdEncargado) VALUES (%s, %s, %s, %s)", pedido)

    cur.execute("SELECT IdSKU FROM SKU where codigo = %s", (codigoSKU,))
    idsku = cur.fetchone()
    if idsku != None:
        idsku = idsku[0]

    else:
        cur.execute("SELECT COUNT(*) FROM SKU")
        CantidadSKUs = cur.fetchone()[0]

        cur.execute("SELECT idcategoria FROM Categoria where nombre = %s", (categoria,))
        idcategoria = cur.fetchone()
        estado = 1
        idsku = CantidadSKUs + 1
        sku = (idsku, codigoSKU, idcategoria, estado, precioSKU, fecha, garantia, detalleUbicacion)
        cur.execute(
        "INSERT INTO SKU (IdSKU, Codigo, IdCategoria, IdEstado, PrecioActual, FechaRegistro, Garantia, DetalleUbicacion)  VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        sku)

        # Assign SKU to Sucursal
        sucursalSKUs = []
        for sucursal in sucursales:
            sucursalSKUs.append((idsku, sucursal))
        cur.executemany(
            "INSERT INTO SucursalSKU (IdSKU, IdSucursal) VALUES  (%s, %s)",
            sucursalSKUs)

    codigos = gen.gen_data_series(cantidad, data_type='ssn')
    cur.execute("SELECT COUNT(*) FROM Articulo")
    CantidadArticulos = cur.fetchone()[0]
    articulos = []
    for i in range(1, cantidad + 1):
        codigo = codigos[i-1]
        idArticulo = CantidadArticulos + i
        articulos.append((idArticulo, idsku, codigo, costo, idpedido, 1))
    cur.executemany(
        "INSERT INTO Articulo (IdArticulo, IdSKU, Codigo, Costo, IdPedido, IdEstadoArticulo)  VALUES (%s, %s, %s, %s, %s, %s)",
        articulos)

    # Make the changes to the database persistent
    conn.commit()

    # Close communication with the database
    cur.close()
    conn.close()

if __name__ == "__main__":
    insertEmpleado("2-07820-951", "Jasson", "R", "M", "89719489", "jassonrm@icloud.com", '08-24-1998', "Tec", "Cartago", 407, "Administrador", "01", 850000)
    # insertPedido("Benson PLC", 6, "NewSKU11", 10000, 30, "Calzado de hombre", "Ventana", 5000, 15, [1, 2])
