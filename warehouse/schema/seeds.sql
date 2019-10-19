-- Inserts some default MetodoPago for a purchase
INSERT INTO MetodoPago (Metodo, Descripcion)
VALUES ('Master Card', 'Tarjeta de la marca Master Card'),
       ('Visa', 'Tarjeta de la marca Visa'),
       ('Efectivo', 'Billetes y monedas'),
       ('Puntos', 'Canje de puntos de cliente frecuente');


-- Inserts default Estado
INSERT INTO Estado (Descripcion)
VALUES ('Activo'),
       ('Inactivo');


-- Inserts default states for the Articulo
INSERT INTO EstadoArticulo (Nombre)
VALUES ('Bodega'),
       ('Tienda'),
       ('Vendido'),
       ('Garantía');


-- Inserts default Categorías for Articulos
INSERT INTO Categoria (Nombre, Descripcion)
VALUES ('Camiseta de hombre', 'Camisetas de diferentes estilos para hombre'),
       ('Camiseta de mujer', 'Camisetas de diferentes estilos para mujeres'),
       ('Blusas', 'Blusas de diferentes estilos para mujeres'),
       ('Calzado de hombre', 'Zapatos para hombres para hacer skate'),
       ('Calzado de mujer', 'Zapatos para mujeres para hacer skate'),
       ('Accesorios', 'Accesorios relacionados al skate');


-- Inserts default Pais
INSERT INTO Pais (Nombre)
VALUES ('Costa Rica');


-- Inserts all Provincias in Costa Rica
INSERT INTO Provincia (Nombre, IdPais)
VALUES ('San José', 1),
       ('Alajuela', 1),
       ('Cartago', 1),
       ('Heredia', 1),
       ('Guanacaste', 1),
       ('Puntarenas', 1),
       ('Limón', 1);


-- Inserts Puestos for the Sucursal
INSERT INTO Puesto (Nombre, Descripcion)
VALUES ('Administrador', 'Se encarga de administrar cada una de las sucursales'),
       ('Vendedor', 'Se encarga de vender a los clientes los productos'),
       ('Bodeguero', 'Se encarga de recibir los productos'),
       ('Jefe de bodega', 'Se encarga de administrar todos los entrantes y salientes de la bodega');

