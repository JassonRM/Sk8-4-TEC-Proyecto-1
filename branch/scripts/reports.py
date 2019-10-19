import mysql.connector
import csv
import datetime

BRANCH_DB = ""
BRANCH_DB_HOST = "localhost"
BRANCH_DB_USER = "root"
BRANCH_DB_PASSWD = "admin"
BRANCH_DB_PORT = "3306"


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

def generateReports():
    # Connect to an existing database and open a cursor to perform database operations
    branch = mysql.connector.connect(host=BRANCH_DB_HOST, port=BRANCH_DB_PORT, user=BRANCH_DB_USER, database=BRANCH_DB,
                                     passwd=BRANCH_DB_PASSWD)
    b_cursor = branch.cursor()

    # create csv file
    fileName = 'reporte_productos-' + str(datetime.datetime.now()) +  '.csv'
    c = csv.writer(open(fileName, 'w'))

    # fetch data
    b_cursor.callproc("ReporteProductos")
    # write
    for resultado in b_cursor.stored_results():
        for x in resultado.fetchall():
            c.writerow(x)

    # create csv file
    fileName = 'reporte_compras-' + str(datetime.datetime.now()) + '.csv'
    c = csv.writer(open(fileName, 'w'))

    #fetch data
    b_cursor.callproc("ReporteCompras")
    # write
    for resultado in b_cursor.stored_results():
        for x in resultado.fetchall():
            c.writerow(x)


