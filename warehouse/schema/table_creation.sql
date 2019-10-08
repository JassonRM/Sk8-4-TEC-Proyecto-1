USE sk8;
CREATE TABLE IF NOT EXISTS Estado
(
    IdEstado    INT AUTO_INCREMENT PRIMARY KEY,
    Descripcion VARCHAR(40) NOT NULL
);


CREATE TABLE IF NOT EXISTS Pais
(
    IdPais INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(40) NOT NULL
);


CREATE TABLE IF NOT EXISTS Provincia
(
    IdProvincia INT AUTO_INCREMENT PRIMARY KEY,
    Nombre      VARCHAR(40) NOT NULL,
    IdPais      INT         NOT NULL,
    CONSTRAINT FkPais
        FOREIGN KEY (IdPais)
            REFERENCES Pais (IdPais)
);


CREATE TABLE IF NOT EXISTS Canton
(
    IdCanton    INT AUTO_INCREMENT PRIMARY KEY,
    Nombre      VARCHAR(40) NOT NULL,
    IdProvincia INT         NOT NULL,
    CONSTRAINT FkProvincia
        FOREIGN KEY (IdProvincia)
            REFERENCES Provincia (IdProvincia)
);


CREATE TABLE IF NOT EXISTS Distrito
(
    IdDistrito INT AUTO_INCREMENT PRIMARY KEY,
    Nombre     VARCHAR(40) NOT NULL,
    IdCanton   INT         NOT NULL,
    CONSTRAINT FkCanton
        FOREIGN KEY (IdCanton)
            REFERENCES Canton (IdCanton)
);


CREATE TABLE IF NOT EXISTS Direccion
(
    IdDireccion INT AUTO_INCREMENT PRIMARY KEY,
    IdDistrito  INT          NOT NULL,
    Detalle1    VARCHAR(100) NOT NULL,
    Detalle2    VARCHAR(100),
    CONSTRAINT FkDistrito
        FOREIGN KEY (IdDistrito)
            REFERENCES Distrito (IdDistrito)
);


CREATE TABLE IF NOT EXISTS Persona
(
    IdPersona       INT AUTO_INCREMENT PRIMARY KEY,
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
    CONSTRAINT FkEstado
        FOREIGN KEY (IdEstado)
            REFERENCES Estado (IdEstado),
    CONSTRAINT FkDireccion
        FOREIGN KEY (IdDireccion)
            REFERENCES Direccion (IdDireccion)
);


CREATE TABLE IF NOT EXISTS Cliente
(
    IdCliente   INT AUTO_INCREMENT PRIMARY KEY,
    IdPersona   INT NOT NULL,
    Descripcion VARCHAR(100),
    Puntos      INT NOT NULL,
    CONSTRAINT FkPersona
        FOREIGN KEY (IdPersona)
            REFERENCES Persona (IdPersona)
);


CREATE TABLE IF NOT EXISTS Empleado
(
    IdEmpleado  INT AUTO_INCREMENT PRIMARY KEY,
    IdPersona   INT NOT NULL,
    Descripcion VARCHAR(100),
    CONSTRAINT FkPersona
        FOREIGN KEY (IdPersona)
            REFERENCES Persona (IdPersona)
);


CREATE TABLE IF NOT EXISTS Puesto
(
    IdPuesto    INT AUTO_INCREMENT PRIMARY KEY,
    Nombre      VARCHAR(40) NOT NULL,
    Descripcion VARCHAR(100)
);


CREATE TABLE IF NOT EXISTS EmpleadoPuesto
(
    IdEmpleado INT  NOT NULL,
    IdPuesto   INT  NOT NULL,
    IdSucursal INT  NOT NULL,
    Salario    INT  NOT NULL,
    Fecha      DATE NOT NULL,
    IdEstado   INT  NOT NULL,
    CONSTRAINT FkEmpleado
        FOREIGN KEY (IdEmpleado)
            REFERENCES Empleado (IdEmpleado),
    CONSTRAINT FkPuesto
        FOREIGN KEY (IdPuesto)
            REFERENCES Puesto (IdPuesto),
    CONSTRAINT FkSucursal
        FOREIGN KEY (IdSucursal)
            REFERENCES Sucursal (IdSucursal),
    CONSTRAINT FkEstado
        FOREIGN KEY (IdEstado)
            REFERENCES Estado (IdEstado)
);


CREATE TABLE IF NOT EXISTS Categoria
(
    IdCategoria INT AUTO_INCREMENT PRIMARY KEY,
    Nombre      VARCHAR(40) NOT NULL,
    Descripcion VARCHAR(100)
);


CREATE TABLE IF NOT EXISTS SKU
(
    IdSKU            INT AUTO_INCREMENT PRIMARY KEY,
    Codigo           VARCHAR(40) NOT NULL,
    Nombre           VARCHAR(40) NOT NULL,
    Descripcion      VARCHAR(100),
    IdCategoria      INT         NOT NULL,
    IdEstado         INT         NOT NULL,
    PrecioActual     INT         NOT NULL,
    FechaRegistro    DATE        NOT NULL,
    FechaCaducidad   DATE        NOT NULL,
    DetalleUbicacion VARCHAR(100),
    Cantidad         INT         NOT NULL,
    CONSTRAINT FkCategoria
        FOREIGN KEY (IdCategoria)
            REFERENCES Categoria (IdCategoria),
    CONSTRAINT FkEstado
        FOREIGN KEY (IdEstado)
            REFERENCES Estado (IdEstado)
);


CREATE TABLE IF NOT EXISTS Sucursal
(
    IdSucursal  INT AUTO_INCREMENT PRIMARY KEY,
    Codigo      VARCHAR(40) NOT NULL,
    Nombre      VARCHAR(40) NOT NULL,
    Descripcion VARCHAR(100),
    IdDireccion INT         NOT NULL,
    IdEstado    INT         NOT NULL,
    CONSTRAINT FkEstado
        FOREIGN KEY (IdEstado)
            REFERENCES Estado (IdEstado),
    CONSTRAINT FkDireccion
        FOREIGN KEY (IdDireccion)
            REFERENCES Direccion (IdDireccion)
);


CREATE TABLE IF NOT EXISTS SucursalSKU
(
    IdSucursal INT NOT NULL,
    IdSKU      INT NOT NULL,
    CONSTRAINT FkSucursal
        FOREIGN KEY (IdSucursal)
            REFERENCES Sucursal (IdSucursal),
    CONSTRAINT FkSKU
        FOREIGN KEY (IdSKU)
            REFERENCES SKU (IdSKU)
);


CREATE TABLE IF NOT EXISTS Camion
(
    IdCamion    INT AUTO_INCREMENT PRIMARY KEY,
    Placa       VARCHAR(20) NOT NULL,
    Descripcion VARCHAR(100),
    IdEstado    INT         NOT NULL,
    CONSTRAINT FkEstado
        FOREIGN KEY (IdEstado)
            REFERENCES Estado (IdEstado)
);


CREATE TABLE IF NOT EXISTS Envio
(
    IdEnvio     INT AUTO_INCREMENT PRIMARY KEY,
    IdCamion    INT      NOT NULL,
    IdChofer    INT      NOT NULL,
    IdEncargado INT      NOT NULL,
    IdSucursal  INT      NOT NULL,
    Fecha       DATETIME NOT NULL,
    CONSTRAINT FkCamion
        FOREIGN KEY (IdCamion)
            REFERENCES Camion (IdCamion),
    CONSTRAINT FkChofer
        FOREIGN KEY (IdChofer)
            REFERENCES Empleado (IdEmpleado),
    CONSTRAINT FkEncargado
        FOREIGN KEY (IdEncargado)
            REFERENCES Empleado (IdEmpleado),
    CONSTRAINT FkSucursal
        FOREIGN KEY (IdSucursal)
            REFERENCES Sucursal (IdSucursal)
);


CREATE TABLE IF NOT EXISTS EnvioPaquete
(
    IdEnvio  INT NOT NULL,
    IdSKU    INT NOT NULL,
    Cantidad INT NOT NULL,
    CONSTRAINT FkEnvio
        FOREIGN KEY (IdEnvio)
            REFERENCES Envio (IdEnvio),
    CONSTRAINT FkSKU
        FOREIGN KEY (IdSKU)
            REFERENCES SKU (IdSKU)
);


CREATE TABLE IF NOT EXISTS PedidoPaquete
(
    IdPedido INT NOT NULL,
    IdSKU    INT NOT NULL,
    Cantidad INT NOT NULL,
    Costo    INT NOT NULL,
    CONSTRAINT FkPedido
        FOREIGN KEY (IdPedido)
            REFERENCES Pedido (IdPedido),
    CONSTRAINT FkSKU
        FOREIGN KEY (IdSKU)
            REFERENCES SKU (IdSKU)
);


CREATE TABLE IF NOT EXISTS Proveedor
(
    IdProveedor INT AUTO_INCREMENT PRIMARY KEY,
    Nombre      VARCHAR(40) NOT NULL,
    Descripcion VARCHAR(100),
    IdEstado    INT         NOT NULL,
    CONSTRAINT FkEstado
        FOREIGN KEY (IdEstado)
            REFERENCES Estado (IdEstado)
);


CREATE TABLE IF NOT EXISTS Pedido
(
    IdPedido    INT AUTO_INCREMENT PRIMARY KEY,
    Fecha       DATE NOT NULL,
    Descripcion VARCHAR(100),
    IdProveedor INT  NOT NULL,
    IdEncargado INT  NOT NULL,
    CONSTRAINT FkProveedor
        FOREIGN KEY (IdProveedor)
            REFERENCES Proveedor (IdProveedor),
    CONSTRAINT FkEncargado
        FOREIGN KEY (IdEncargado)
            REFERENCES Empleado (IdEmpleado)
);


CREATE TABLE IF NOT EXISTS MetodoPago
(
    IdMetodoPago INT AUTO_INCREMENT PRIMARY KEY,
    Metodo       VARCHAR(40) NOT NULL,
    Descripcion  VARCHAR(100)
);


CREATE TABLE IF NOT EXISTS Promocion
(
    IdPromocion INT AUTO_INCREMENT PRIMARY KEY,
    IdSKU       INT      NOT NULL,
    Inicio      DATETIME NOT NULL,
    Fin         DATETIME NOT NULL,
    Descuento   INT      NOT NULL,
    CONSTRAINT FkSKU
        FOREIGN KEY (IdSKU)
            REFERENCES SKU (IdSKU)
);


CREATE TABLE IF NOT EXISTS Factura
(
    IdFactura       INT AUTO_INCREMENT PRIMARY KEY,
    Codigo          VARCHAR(40) NOT NULL,
    Fecha           DATE        NOT NULL,
    SubTotal        INT         NOT NULL,
    Impuestos       INT         NOT NULL,
    PuntosOtorgados INT         NOT NULL,
    Garantia        INT         NOT NULL,
    IdSucursal      INT         NOT NULL,
    IdCliente       INT         NOT NULL,
    IdEmpleado      INT         NOT NULL,
    IdMetodoPago    INT         NOT NULL,
    CONSTRAINT FkSucursal
        FOREIGN KEY (IdSucursal)
            REFERENCES Sucursal (IdSucursal),
    CONSTRAINT FkCliente
        FOREIGN KEY (IdCliente)
            REFERENCES Cliente (IdCliente),
    CONSTRAINT FkEmpleado
        FOREIGN KEY (IdEmpleado)
            REFERENCES Empleado (IdEmpleado),
    CONSTRAINT FkMetodoPago
        FOREIGN KEY (IdMetodoPago)
            REFERENCES MetodoPago (IdMetodoPago)
);

CREATE TABLE IF NOT EXISTS PromocionFactura
(
    IdPromocion INT NOT NULL,
    IdFactura   INT NOT NULL,
    CONSTRAINT FkPromocion
        FOREIGN KEY (IdPromocion)
            REFERENCES Promocion (IdPromocion),
    CONSTRAINT FkFactura
        FOREIGN KEY (IdFactura)
            REFERENCES Factura (IdFactura)
);

CREATE TABLE IF NOT EXISTS Venta
(
    IdSKU     INT NOT NULL,
    IdFactura INT NOT NULL,
    Cantidad  INT NOT NULL,
    Precio    INT NOT NULL,
    CONSTRAINT FkSKU
        FOREIGN KEY (IdSKU)
            REFERENCES SKU (IdSKu),
    CONSTRAINT FkFactura
        FOREIGN KEY (IdFactura)
            REFERENCES Factura (IdFactura)
);
