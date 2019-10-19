-- Inserts default Direcciones for sucursales
INSERT INTO Direccion (IdDistrito, Detalle1, Detalle2)
VALUES (122, 'Avenida 2', 'Frente al parque'),
       (9, 'Avenida 4', 'Frente al KFC'),
       (236, 'Calle 3', 'Frente a la iglesia');

-- Inserts values of Sucursales and their data
INSERT INTO Sucursal (Codigo, Nombre, Descripcion, IdDireccion, IdEstado)
VALUES ('01', 'Ska8-4-TEC-Alajuela', 'Tienda original', 1, 1),
       ('02', 'Ska8-4-TEC-Cartago', 'Tienda religiosa', 3, 1),
       ('03', 'Ska8-4-TEC-San-Jose', 'Tienda super ventas', 2, 2);

