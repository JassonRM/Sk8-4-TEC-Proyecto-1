-- Creates Estado and its structure
CREATE TABLE IF NOT EXISTS Estado
(
    IdEstado    SERIAL PRIMARY KEY,
    Descripcion VARCHAR(40) NOT NULL
);


-- Creates Pais and its structure
CREATE TABLE IF NOT EXISTS Pais
(
    IdPais SERIAL PRIMARY KEY,
    Nombre VARCHAR(40) NOT NULL
);


-- Creates Provincia and its structure
CREATE TABLE IF NOT EXISTS Provincia
(
    IdProvincia SERIAL PRIMARY KEY,
    Nombre      VARCHAR(40) NOT NULL,
    IdPais      INT         NOT NULL,

    FOREIGN KEY (IdPais)
        REFERENCES Pais (IdPais)
);


-- Creates Canton and its structure
CREATE TABLE IF NOT EXISTS Canton
(
    IdCanton    SERIAL PRIMARY KEY,
    Nombre      VARCHAR(40) NOT NULL,
    IdProvincia INT         NOT NULL,

    FOREIGN KEY (IdProvincia)
        REFERENCES Provincia (IdProvincia)
);


-- Creates Distrito and its structure
CREATE TABLE IF NOT EXISTS Distrito
(
    IdDistrito SERIAL PRIMARY KEY,
    Nombre     VARCHAR(40) NOT NULL,
    IdCanton   INT         NOT NULL,

    FOREIGN KEY (IdCanton)
        REFERENCES Canton (IdCanton)
);


-- Creates Direccion and its structure
CREATE TABLE IF NOT EXISTS Direccion
(
    IdDireccion SERIAL PRIMARY KEY,
    IdDistrito  INT          NOT NULL,
    Detalle1    VARCHAR(100) NOT NULL,
    Detalle2    VARCHAR(100),

    FOREIGN KEY (IdDistrito)
        REFERENCES Distrito (IdDistrito)
);


-- Creates Persona and its structure
CREATE TABLE IF NOT EXISTS Persona
(
    IdPersona       SERIAL PRIMARY KEY,
    Identificacion  VARCHAR(40) UNIQUE NOT NULL,
    Nombre          VARCHAR(40)        NOT NULL,
    Apellido1       VARCHAR(40)        NOT NULL,
    Apellido2       VARCHAR(40)        NOT NULL,
    Telefono        VARCHAR(40)        NOT NULL,
    Correo          VARCHAR(100)       NOT NULL,
    FechaNacimiento DATE               NOT NULL,
    FechaRegistro   DATE               NOT NULL,
    IdEstado        INT                NOT NULL,
    IdDireccion     INT                NOT NULL,

    FOREIGN KEY (IdEstado)
        REFERENCES Estado (IdEstado),

    FOREIGN KEY (IdDireccion)
        REFERENCES Direccion (IdDireccion)
);


-- Creates Cliente and its structure
CREATE TABLE IF NOT EXISTS Cliente
(
    IdCliente     SERIAL PRIMARY KEY,
    IdPersona     INT  NOT NULL,
    Descripcion   VARCHAR(100),
    Puntos        INT  NOT NULL,
    FechaRegistro DATE NOT NULL,
    IdEstado      INT  NOT NULL,

    FOREIGN KEY (IdPersona)
        REFERENCES Persona (IdPersona),
    FOREIGN KEY (IdEstado)
        REFERENCES Estado (IdEstado)
);


-- Creates Puesto and its structure
CREATE TABLE IF NOT EXISTS Puesto
(
    IdPuesto    SERIAL PRIMARY KEY,
    Nombre      VARCHAR(40) NOT NULL,
    Descripcion VARCHAR(100)
);


-- Creates Sucursal and its structure
CREATE TABLE IF NOT EXISTS Sucursal
(
    IdSucursal  SERIAL PRIMARY KEY,
    Codigo      VARCHAR(40) NOT NULL,
    Nombre      VARCHAR(40) NOT NULL,
    Descripcion VARCHAR(100),
    IdDireccion INT         NOT NULL,
    IdEstado    INT         NOT NULL,

    FOREIGN KEY (IdEstado)
        REFERENCES Estado (IdEstado),

    FOREIGN KEY (IdDireccion)
        REFERENCES Direccion (IdDireccion)
);


-- Creates Empleado and its structure
CREATE TABLE IF NOT EXISTS Empleado
(
    IdEmpleado SERIAL PRIMARY KEY,
    IdPersona  INT  NOT NULL,
    IdPuesto   INT  NOT NULL,
    IdSucursal INT  NOT NULL,
    Salario    INT  NOT NULL,
    Fecha      DATE NOT NULL,
    IdEstado   INT  NOT NULL,

    FOREIGN KEY (IdPuesto)
        REFERENCES Puesto (IdPuesto),

    FOREIGN KEY (IdSucursal)
        REFERENCES Sucursal (IdSucursal),

    FOREIGN KEY (IdEstado)
        REFERENCES Estado (IdEstado),

    FOREIGN KEY (IdPersona)
        REFERENCES Persona (IdPersona)
);


-- Creates Categoria and its structure
CREATE TABLE IF NOT EXISTS Categoria
(
    IdCategoria SERIAL PRIMARY KEY,
    Nombre      VARCHAR(40) NOT NULL,
    Descripcion VARCHAR(100)
);


-- Creates SKU and its structure
CREATE TABLE IF NOT EXISTS SKU
(
    IdSKU            SERIAL PRIMARY KEY,
    Codigo           VARCHAR(40) NOT NULL,
    IdCategoria      INT         NOT NULL,
    IdEstado         INT         NOT NULL,
    PrecioActual     INT         NOT NULL,
    FechaRegistro    DATE        NOT NULL,
    Garantia         INT         NOT NULL,
    DetalleUbicacion VARCHAR(100),

    FOREIGN KEY (IdCategoria)
        REFERENCES Categoria (IdCategoria),

    FOREIGN KEY (IdEstado)
        REFERENCES Estado (IdEstado)
);


-- Creates Proveedor and its structure
CREATE TABLE IF NOT EXISTS Proveedor
(
    IdProveedor SERIAL PRIMARY KEY,
    Nombre      VARCHAR(40) NOT NULL,
    IdEstado    INT         NOT NULL,

    FOREIGN KEY (IdEstado)
        REFERENCES Estado (IdEstado)
);


-- Creates Pedido and its structure
CREATE TABLE IF NOT EXISTS Pedido
(
    IdPedido    SERIAL PRIMARY KEY,
    Fecha       DATE NOT NULL,
    IdProveedor INT  NOT NULL,
    IdEncargado INT  NOT NULL,

    FOREIGN KEY (IdProveedor)
        REFERENCES Proveedor (IdProveedor),

    FOREIGN KEY (IdEncargado)
        REFERENCES Empleado (IdEmpleado)
);


-- Creates EstadoArticulo and its structure
CREATE TABLE IF NOT EXISTS EstadoArticulo
(
    IdEstadoArticulo SERIAL PRIMARY KEY,
    Nombre           VARCHAR(40)
);


-- Creates Articulo and its structure
CREATE TABLE IF NOT EXISTS Articulo
(
    IdArticulo       SERIAL PRIMARY KEY,
    IdSKU            INT         NOT NULL,
    Codigo           VARCHAR(40) NOT NULL,
    Costo            INT         NOT NULL,
    IdPedido         INT         NOT NULL,
    IdEstadoArticulo INT         NOT NULL,
    IdSucursal       INT,

    FOREIGN KEY (IdSKU)
        REFERENCES SKU (IdSKU),

    FOREIGN KEY (IdEstadoArticulo)
        REFERENCES EstadoArticulo (IdEstadoArticulo),

    FOREIGN KEY (IdSucursal)
        REFERENCES Sucursal (IdSucursal),

    FOREIGN KEY (IdPedido)
        REFERENCES Pedido (IdPedido)

);


-- Creates Sucursal and its structure
CREATE TABLE IF NOT EXISTS Sucursal
(
    IdSucursal  SERIAL PRIMARY KEY,
    Codigo      VARCHAR(40) NOT NULL,
    Nombre      VARCHAR(40) NOT NULL,
    Descripcion VARCHAR(100),
    IdDireccion INT         NOT NULL,
    IdEstado    INT         NOT NULL,

    FOREIGN KEY (IdEstado)
        REFERENCES Estado (IdEstado),

    FOREIGN KEY (IdDireccion)
        REFERENCES Direccion (IdDireccion)
);


-- Creates SucursalSKU and its structure
CREATE TABLE IF NOT EXISTS SucursalSKU
(
    IdSucursal INT NOT NULL,
    IdSKU      INT NOT NULL,

    FOREIGN KEY (IdSucursal)
        REFERENCES Sucursal (IdSucursal),

    FOREIGN KEY (IdSKU)
        REFERENCES SKU (IdSKU)
);


-- Creates Camion and its structure
CREATE TABLE IF NOT EXISTS Camion
(
    IdCamion SERIAL PRIMARY KEY,
    Placa    VARCHAR(20) NOT NULL,
    Marca    VARCHAR(100),
    IdEstado INT         NOT NULL,

    FOREIGN KEY (IdEstado)
        REFERENCES Estado (IdEstado)
);


-- Creates Envio and its structure
CREATE TABLE IF NOT EXISTS Envio
(
    IdEnvio     SERIAL PRIMARY KEY,
    IdCamion    INT  NOT NULL,
    IdEncargado INT  NOT NULL,
    IdSucursal  INT  NOT NULL,
    Fecha       DATE NOT NULL,

    FOREIGN KEY (IdCamion)
        REFERENCES Camion (IdCamion),

    FOREIGN KEY (IdEncargado)
        REFERENCES Empleado (IdEmpleado),

    FOREIGN KEY (IdSucursal)
        REFERENCES Sucursal (IdSucursal)
);


-- Creates EnvioPaquete and its structure
CREATE TABLE IF NOT EXISTS EnvioPaquete
(
    IdEnvio    INT NOT NULL,
    IdArticulo INT NOT NULL,

    FOREIGN KEY (IdEnvio)
        REFERENCES Envio (IdEnvio),

    FOREIGN KEY (IdArticulo)
        REFERENCES Articulo (IdArticulo)
);


-- Creates MetodoPago and its structure
CREATE TABLE IF NOT EXISTS MetodoPago
(
    IdMetodoPago SERIAL PRIMARY KEY,
    Metodo       VARCHAR(40) NOT NULL,
    Descripcion  VARCHAR(100)
);


-- Creates Promocion and its structure
CREATE TABLE IF NOT EXISTS Promocion
(
    IdPromocion         SERIAL PRIMARY KEY,
    IdPromocionSucursal INT          NOT NULL,
    IdSucursal          INT          NOT NULL,
    IdSKU               INT          NOT NULL,
    Descripcion         VARCHAR(100) NOT NULL,
    Inicio              TIMESTAMP    NOT NULL,
    Fin                 TIMESTAMP    NOT NULL,
    Descuento           INT          NOT NULL,

    FOREIGN KEY (IdSucursal)
        REFERENCES Sucursal (IdSucursal),

    FOREIGN KEY (IdSKU)
        REFERENCES SKU (IdSKU)
);


-- Creates Factura and its structure
CREATE TABLE IF NOT EXISTS Factura
(
    IdFactura         SERIAL PRIMARY KEY,
    IdFacturaSucursal INT         NOT NULL,
    Codigo            VARCHAR(40) NOT NULL,
    Fecha             DATE        NOT NULL,
    SubTotal          INT         NOT NULL,
    Impuestos         INT         NOT NULL,
    PuntosOtorgados   INT         NOT NULL,
    IdSucursal        INT         NOT NULL,
    IdCliente         INT         NOT NULL,
    IdEmpleado        INT         NOT NULL,
    IdMetodoPago      INT         NOT NULL,

    FOREIGN KEY (IdSucursal)
        REFERENCES Sucursal (IdSucursal),

    FOREIGN KEY (IdCliente)
        REFERENCES Cliente (IdCliente),

    FOREIGN KEY (IdEmpleado)
        REFERENCES Empleado (IdEmpleado),

    FOREIGN KEY (IdMetodoPago)
        REFERENCES MetodoPago (IdMetodoPago)
);


-- Creates PromocionFactura and its structure
CREATE TABLE IF NOT EXISTS PromocionFactura
(
    IdPromocion INT NOT NULL,
    IdFactura   INT NOT NULL,

    FOREIGN KEY (IdPromocion)
        REFERENCES Promocion (IdPromocion),

    FOREIGN KEY (IdFactura)
        REFERENCES Factura (IdFactura)
);


-- Creates Venta and its structure
CREATE TABLE IF NOT EXISTS Venta
(
    IdArticulo INT NOT NULL,
    IdFactura  INT NOT NULL,
    Precio     INT NOT NULL,

    FOREIGN KEY (IdArticulo)
        REFERENCES Articulo (IdArticulo),

    FOREIGN KEY (IdFactura)
        REFERENCES Factura (IdFactura)
);
