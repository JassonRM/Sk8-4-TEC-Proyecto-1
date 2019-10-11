import psycopg2
from random import *
from pydbgen import pydbgen



# Connect to an existing database
conn = psycopg2.connect(dbname="postgres", user="postgres", password="admin")

# Open a cursor to perform database operations
cur = conn.cursor()

# Pass data to fill a query placeholders and let Psycopg perform
# the correct conversion (no more SQL injections!)
cur.execute("INSERT INTO Pais (num, data) VALUES (%s, %s)", (100, "abc'def"))


# Make the changes to the database persistent
conn.commit()

# Close communication with the database
cur.close()
conn.close()