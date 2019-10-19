import psycopg2

def generatePuntosClientes():

    # Connect to the warehouse database and open a cursor to perform database operations
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="admin")
    warehousedb = conn.cursor()

    warehousedb.execute("SELECT Cliente.IdCliente, P.Nombre, Cliente.Puntos FROM Cliente INNER JOIN Persona P ON Cliente.IdPersona = P.IdPersona;")
    result = warehousedb.fetchall()
    conn.commit()
    warehousedb.close()
    conn.close()
    return result