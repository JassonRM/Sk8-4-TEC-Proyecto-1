INSERT INTO metodopago (metodo, descripcion)
VALUES
       ('Master Card', 'Tarjeta de la marca Master Card'),
       ('Visa', 'Tarjeta de la marca Visa'),
       ('Efectivo', 'Billetes y monedas'),
       ('Puntos', 'Canje de puntos de cliente frecuente');

INSERT INTO estado (descripcion)
VALUES
       ('Disponible'),
       ('Vendido'),
       ('Garantía');

INSERT INTO categoria (nombre, descripcion)
VALUES
       ('Camiseta de hombre', 'Camisetas de diferentes estilos para hombre'),
       ('Camiseta de hombre', 'Camisetas de diferentes estilos para mujeres'),
       ('Blusas', 'Blusas de diferentes estilos para mujeres'),
       ('Calzado de hombre', 'Zapatos para hombres para hacer skate'),
       ('Calzado de mujer', 'Zapatos para mujeres para hacer skate'),
       ('Accesorios', 'Accesorios relacionados al skate');

INSERT INTO pais (nombre)
VALUES ('Costa Rica');

INSERT INTO provincia (nombre, idpais)
VALUES
    ('San José', 1),
    ('Alajuela', 1),
    ('Cartago', 1);

INSERT INTO canton (nombre, idprovincia)
VALUES
    ('San José', 1),
    ('Alajuela', 2),
    ('Cartago', 3);

INSERT INTO distrito (nombre, idcanton)
VALUES
    ('Pavas', 1),
    ('Alajuela', 2),
    ('Oriental', 3);


INSERT INTO direccion (iddistrito, detalle1, detalle2)
VALUES
    (2, 'Avenida 2', 'Frente al parque'),
    (1, 'Avenida 4', 'Frente al KFC'),
    (3, 'Calle 3', 'Frente a la iglesia');

INSERT INTO sucursal (codigo, nombre, descripcion, iddireccion, idestado)
VALUES
       ('01', 'Ska8-4-TEC Alajuela', 'Tienda original', 1, 1),
       ('02', 'Ska8-4-TEC Cartago', 'Tienda religiosa', 3, 1),
       ('03', 'Ska8-4-TEC San José', 'Tienda super ventas', 2, 2);

INSERT INTO puesto (nombre, descripcion) VALUES
('Administrador', 'Se encarga de administrar cada una de las sucursales'),
('Vendedor', 'Se encarga de vender a los clientes los productos'),
('Bodeguero', 'Se encarga de recibir los productos'),
('Jefe de bodega', 'Se encarga de administrar todos los entrantes y salientes de la bodega');

