from warehouse.scripts.dummy_data import *
from warehouse.scripts.inserts import *
from comms.init import *
from warehouse.scripts.shipments import *
import branch.scripts.CRUD
import comms.cash_desk_closing
import branch.scripts.reports as reports
import warehouse.queries.puntos_clientes as puntos


def init():
    createDummyData()
    initBranches()
    generateShipments()

def cierreDeCaja():
    # Hacer todos los cierres de caja
    comms.cash_desk_closing.updateBranchDB("Ska8-4-TEC-Alajuela", "0.0.0.0", 3306, "root", "admin")
    comms.cash_desk_closing.cierreCaja()
    comms.cash_desk_closing.updateBranchDB("Ska8-4-TEC-Cartago", "0.0.0.0", 3307, "root", "admin")
    comms.cash_desk_closing.cierreCaja()
    comms.cash_desk_closing.updateBranchDB("Ska8-4-TEC-San-Jose", "0.0.0.0", 3308, "root", "admin")
    comms.cash_desk_closing.cierreCaja()

if __name__ == "__main__":
    # init()
    # cierreDeCaja()
    # generateShipments()
    # insertEmpleado("2-0782-0951", "Jasson", "Rodriguez", "Mendez", "89719489",
    #                "jassonrm@icloud.com", '08-24-1998', "Tec", "Cartago", 407,
    #                "Administrador", "01", 850000)
    # insertPedido("Jenkins-Fields", 6, "NewSKU1", 10000, 30, "Calzado de hombre",
    #              "Ventana", 5000, 15, [1, 2])



    # branch.scripts.CRUD.updateBranchDB("Ska8-4-TEC-Alajuela", "0.0.0.0", 3306, "root", "admin")
    # puntos.updateBranchDB("Ska8-4-TEC-Alajuela", "0.0.0.0", 3306,
    #                                    "root", "admin")
    # ptscli = puntos.generatePuntosClientes()
    # print(ptscli)
    # reports.generateReports()
    # updateBranchDB("Ska8-4-TEC-Cartago", "0.0.0.0", 3307, "root", "admin")

    # # Nuevos clientes con personas nuevas
    # branch.scripts.CRUD.insertCliente("469-68-0955", "Carlos", "Rodriguez", "Mendez", "89922567", "carlosr@icloud.com", '1956-03-14', "Centro", "Alajuela", 122, "Buen cliente")
    # branch.scripts.CRUD.insertCliente("293-13-9304", "Maria", "Vasquez", "Coronado", "86304893", "marivc@icloud.com", '1973-07-08', "Los Angeles", "Cartago", 236, "Buen cliente")
    # branch.scripts.CRUD.insertCliente("345-68-0955", "Pablo", "Campos", "Rojas", "73942034", "pabloc@icloud.com", '1986-01-25', "Centro", "Alajuela", 130, "Buen cliente")
    # branch.scripts.CRUD.insertCliente("945-13-9304", "Ana", "Lopez", "Redondo", "73040293", "lopezredondoa@icloud.com", '01-24-1990', "Los Angeles", "Cartago", 237, "Buen cliente")
    #
    # # Nuevos clientes de personas ya existentes
    # branch.scripts.CRUD.insertCliente("209-47-5441", "Carlos", "Rodriguez",
    #                                   "Mendez", "89922567",
    #                                   "carlosr@icloud.com", '1956-03-14',
    #                                   "Centro", "Alajuela", 122,
    #                                   "Buen cliente")
    # branch.scripts.CRUD.insertCliente("631-15-1750", "Maria", "Vasquez",
    #                                   "Coronado", "86304893",
    #                                   "marivc@icloud.com", '1973-07-08',
    #                                   "Los Angeles", "Cartago", 236,
    #                                   "Buen cliente")
    # branch.scripts.CRUD.insertCliente("340-45-6379", "Pablo", "Campos",
    #                                   "Rojas", "73942034", "pabloc@icloud.com",
    #                                   '1986-01-25', "Centro", "Alajuela", 130,
    #                                   "Buen cliente")
    # branch.scripts.CRUD.insertCliente("750-51-5480", "Ana", "Lopez", "Redondo",
    #                                   "73040293", "lopezredondoa@icloud.com",
    #                                   '01-24-1990', "Los Angeles", "Cartago",
    #                                   237, "Buen cliente")

    # insertVenta(articulos, codigoFactura, porcentajeImpuestos, porcentajePuntos,idCliente, idEmpleado, idMetodoPago)
    # branch.scripts.CRUD.updateBranchDB("Ska8-4-TEC-Alajuela", "0.0.0.0", 3306, "root", "admin")
    # branch.scripts.CRUD.insertVenta([8583], "SA5", 0.13, 0.1, 1, 9, 2)
    # branch.scripts.CRUD.insertVenta([230, 232, 233], "SA4", 0.13, 0.1, 2, 9, 1)
    #
    # branch.scripts.CRUD.updateBranchDB("Ska8-4-TEC-Cartago", "0.0.0.0", 3307,
    #                                    "root", "admin")
    # branch.scripts.CRUD.insertVenta([96, 98, 99], "SC3", 0.13, 0.1, 3, 1, 2)
    # branch.scripts.CRUD.insertVenta([201, 202, 203], "SC4", 0.13, 0.1, 4, 6, 1)
    #
    # branch.scripts.CRUD.updateBranchDB("Ska8-4-TEC-San-Jose", "0.0.0.0", 3308,
    #                                    "root", "admin")
    # branch.scripts.CRUD.insertVenta([500, 505, 509], "SSJ3", 0.13, 0.1, 5, 2, 2)
    # branch.scripts.CRUD.insertVenta([855, 859, 869], "SSJ4", 0.13, 0.1, 6, 3, 2)
    #
    # branch.scripts.CRUD.insertPromocion(32, "Viernes negro", "2019-10-16 00:00:00", "2019-10-18 00:00:00", 25)
    # branch.scripts.CRUD.insertVenta([3016, 1135, 2149], "PROMO1", 0.13, 0.05, 2, 5, 1)

    # devolucion(idArticulo, codigoFactura, idCliente, idEmpleado, fecha)
    # devolucion(3, "DEV001", 1, 4, fecha)


