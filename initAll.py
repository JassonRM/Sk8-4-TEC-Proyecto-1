from warehouse.scripts.dummy_data import *
from warehouse.scripts.inserts import *
from comms.init import *
from comms.shipments import *
from branch.scripts.CRUD import *

# createDummyData()
# initBranches()
insertEmpleado("2-07820-951", "Jasson", "R", "M", "89719489",
               "jassonrm@icloud.com", '08-24-1998', "Tec", "Cartago", 407,
               "Administrador", "01", 850000)
insertPedido("Murphy LLC", 6, "NewSKU11", 10000, 30, "Calzado de hombre",
             "Ventana", 5000, 15, [1, 2])

