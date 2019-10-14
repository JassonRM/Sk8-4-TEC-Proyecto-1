INSERT INTO metodopago (metodo, descripcion)
VALUES ('Master Card', 'Tarjeta de la marca Master Card'),
       ('Visa', 'Tarjeta de la marca Visa'),
       ('Efectivo', 'Billetes y monedas'),
       ('Puntos', 'Canje de puntos de cliente frecuente');

INSERT INTO estado (descripcion)
VALUES ('Activo'),
       ('Inactivo');

INSERT INTO estadoArticulo (nombre)
VALUES ('Bodega'),
       ('Tienda'),
       ('Vendido'),
       ('Garantía');

INSERT INTO categoria (nombre, descripcion)
VALUES ('Camiseta de hombre', 'Camisetas de diferentes estilos para hombre'),
       ('Camiseta de mujer', 'Camisetas de diferentes estilos para mujeres'),
       ('Blusas', 'Blusas de diferentes estilos para mujeres'),
       ('Calzado de hombre', 'Zapatos para hombres para hacer skate'),
       ('Calzado de mujer', 'Zapatos para mujeres para hacer skate'),
       ('Accesorios', 'Accesorios relacionados al skate');

INSERT INTO pais (nombre)
VALUES ('Costa Rica');

INSERT INTO provincia (nombre, idpais)
VALUES ('San José', 1),
       ('Alajuela', 1),
       ('Cartago', 1),
       ('Heredia', 1),
       ('Guanacaste', 1),
       ('Puntarenas', 1),
       ('Limón', 1);

INSERT INTO puesto (nombre, descripcion)
VALUES ('Administrador', 'Se encarga de administrar cada una de las sucursales'),
       ('Vendedor', 'Se encarga de vender a los clientes los productos'),
       ('Bodeguero', 'Se encarga de recibir los productos'),
       ('Jefe de bodega', 'Se encarga de administrar todos los entrantes y salientes de la bodega');

