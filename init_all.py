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
    # insertEmpleado("2-07820-951", "Jasson", "R", "M", "89719489",
    #                "jassonrm@icloud.com", '08-24-1998', "Tec", "Cartago", 407,
    #                "Administrador", "01", 850000)
    # insertPedido("Jensen-Sexton", 6, "NewSKU11", 10000, 30, "Calzado de hombre",
    #              "Ventana", 5000, 15, [1, 2])
    # generateShipments()


    # branch.scripts.CRUD.updateBranchDB("Ska8-4-TEC-Alajuela", "0.0.0.0", 3306, "root", "admin")
    puntos.updateBranchDB("Ska8-4-TEC-Alajuela", "0.0.0.0", 3306,
                                       "root", "admin")
    ptscli = puntos.generatePuntosClientes()
    print(ptscli)
    # reports.generateReports()
    # updateBranchDB("Ska8-4-TEC-Cartago", "0.0.0.0", 3307, "root", "admin")
    # branch.scripts.CRUD.insertCliente("469-68-0955", "Carlos", "R", "M", "379832", "cal@icloud.com", '01-24-1990', "Tec", "Cartago", 34, "Buen cliente")
    # branch.scripts.CRUD.insertCliente("20390294", "Maria", "R", "M", "379832", "cal@icloud.com", '01-24-1990', "Tec", "Cartago", 35, "Buen cliente")

    # insertVenta(articulos, codigoFactura, porcentajeImpuestos, porcentajePuntos,idCliente, idEmpleado, idMetodoPago)
    # branch.scripts.CRUD.insertVenta([2680], "CANJE", 0.13, 0.05, 2, 3, 4)
    # branch.scripts.CRUD.insertPromocion(17, "Viernes negro", "2019-10-19 00:00:00", "2020-11-28 00:00:00", 45)
    # branch.scripts.CRUD.insertVenta([354, 14, 717], "AMB251", 0.13, 0.05, 2, 5, 1)

    # devolucion(idArticulo, codigoFactura, idCliente, idEmpleado, fecha)
    # devolucion(3, "DEV001", 1, 4, fecha)


