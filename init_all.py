from warehouse.scripts.dummy_data import *
from warehouse.scripts.inserts import *
from comms.init import *
from warehouse.scripts.shipments import *
from branch.scripts.CRUD import *

def init():
    createDummyData()
    initBranches()
    # generateShipments()

def cierreDeCaja():
    # Hacer todos los cierres de caja
    updateBranchDB("Ska8-4-TEC-Alajuela", "0.0.0.0", 3306, "root", "admin")
    cierreCaja()
    updateBranchDB("Ska8-4-TEC-Cartago", "0.0.0.0", 3307, "root", "admin")
    cierreCaja()
    updateBranchDB("Ska8-4-TEC-San-Jose", "0.0.0.0", 3308, "root", "admin")
    cierreCaja()

if __name__ == "__main__":
    init()
    # cierreDeCaja()
    # insertEmpleado("2-07820-951", "Jasson", "R", "M", "89719489",
    #                "jassonrm@icloud.com", '08-24-1998', "Tec", "Cartago", 407,
    #                "Administrador", "01", 850000)
    # insertPedido("Jensen-Sexton", 6, "NewSKU11", 10000, 30, "Calzado de hombre",
    #              "Ventana", 5000, 15, [1, 2])
    # generateShipments()

    # updateBranchDB("Ska8-4-TEC-Alajuela", "0.0.0.0", 3306, "root", "admin")
    # updateBranchDB("Ska8-4-TEC-Cartago", "0.0.0.0", 3307, "root", "admin")
    # insertCliente("469-68-0955", "Carlos", "R", "M", "379832", "cal@icloud.com", '01-24-1990', "Tec", "Cartago", 34, "Buen cliente")
    # insertCliente("20390294", "Maria", "R", "M", "379832", "cal@icloud.com", '01-24-1990', "Tec", "Cartago", 35, "Buen cliente")

    # # insertVenta(articulos, codigoFactura, fecha, porcentajeImpuestos, porcentajePuntos,idCliente, idEmpleado, idMetodoPago)
    # insertVenta([1634], "CANJE175", fecha, 0.13, 0.05, 1, 4, 4)
    # insertPromocion(1, "Viernes negro", "2019-10-17 00:00:00", "2020-11-28 00:00:00", 70)
    # insertVenta([5269], "AMB251", fecha, 0.13, 0.05, 1, 3, 1)

    # devolucion(idArticulo, codigoFactura, idCliente, idEmpleado, fecha)
    # devolucion(3, "DEV001", 1, 4, fecha)


