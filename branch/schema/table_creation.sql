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

    FOREIGN KEY (IdPais)
        REFERENCES Pais (IdPais)
);


CREATE TABLE IF NOT EXISTS Canton
(
    IdCanton    INT AUTO_INCREMENT PRIMARY KEY,
    Nombre      VARCHAR(40) NOT NULL,
    IdProvincia INT         NOT NULL,

    FOREIGN KEY (IdProvincia)
        REFERENCES Provincia (IdProvincia)
);


CREATE TABLE IF NOT EXISTS Distrito
(
    IdDistrito INT AUTO_INCREMENT PRIMARY KEY,
    Nombre     VARCHAR(40) NOT NULL,
    IdCanton   INT         NOT NULL,

    FOREIGN KEY (IdCanton)
        REFERENCES Canton (IdCanton)
);


CREATE TABLE IF NOT EXISTS Direccion
(
    IdDireccion INT AUTO_INCREMENT PRIMARY KEY,
    IdDistrito  INT          NOT NULL,
    Detalle1    VARCHAR(100) NOT NULL,
    Detalle2    VARCHAR(100),

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

    FOREIGN KEY (IdEstado)
        REFERENCES Estado (IdEstado),

    FOREIGN KEY (IdDireccion)
        REFERENCES Direccion (IdDireccion)
);


CREATE TABLE IF NOT EXISTS Puesto
(
    IdPuesto    INT AUTO_INCREMENT PRIMARY KEY,
    Nombre      VARCHAR(40) NOT NULL,
    Descripcion VARCHAR(100)
);


CREATE TABLE IF NOT EXISTS Empleado
(
    IdEmpleado INT AUTO_INCREMENT PRIMARY KEY,
    IdPersona  INT  NOT NULL,
    IdPuesto   INT  NOT NULL,
    Salario    INT  NOT NULL,
    Fecha      DATE NOT NULL,
    IdEstado   INT  NOT NULL,

    FOREIGN KEY (IdPuesto)
        REFERENCES Puesto (IdPuesto),

    FOREIGN KEY (IdEstado)
        REFERENCES Estado (IdEstado),

    FOREIGN KEY (IdPersona)
        REFERENCES Persona (IdPersona)
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


CREATE TABLE IF NOT EXISTS EstadoArticulo
(
    IdEstadoArticulo INT AUTO_INCREMENT PRIMARY KEY,
    Nombre           VARCHAR(40)
);

CREATE TABLE IF NOT EXISTS Articulo
(
    IdArticulo       INT AUTO_INCREMENT PRIMARY KEY,
    IdSKU            INT         NOT NULL,
    Codigo           VARCHAR(40) NOT NULL,
    IdEstadoArticulo INT         NOT NULL,

    FOREIGN KEY (IdSKU)
        REFERENCES SKU (IdSKU),

    FOREIGN KEY (IdEstadoArticulo)
        REFERENCES EstadoArticulo (IdEstadoArticulo)

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
    IdSKU       INT          NOT NULL,
    Descripcion VARCHAR(100) NOT NULL,
    Inicio      DATETIME     NOT NULL,
    Fin         DATETIME     NOT NULL,
    Descuento   INT          NOT NULL,

    FOREIGN KEY (IdSKU)
        REFERENCES SKU (IdSKU)
);


CREATE TABLE IF NOT EXISTS Factura
(
    IdFactura       INT AUTO_INCREMENT PRIMARY KEY,
    Codigo          VARCHAR(40) NOT NULL,
    Fecha           DATE        NOT NULL,
    SubTotal        INT,
    Impuestos       INT,
    PuntosOtorgados INT,
    IdCliente       INT         NOT NULL,
    IdEmpleado      INT         NOT NULL,
    IdMetodoPago    INT         NOT NULL,

    FOREIGN KEY (IdEmpleado)
        REFERENCES Empleado (IdEmpleado),

    FOREIGN KEY (IdMetodoPago)
        REFERENCES MetodoPago (IdMetodoPago)
);

CREATE TABLE IF NOT EXISTS PromocionFactura
(
    IdPromocion INT NOT NULL,
    IdFactura   INT NOT NULL,

    FOREIGN KEY (IdPromocion)
        REFERENCES Promocion (IdPromocion),

    FOREIGN KEY (IdFactura)
        REFERENCES Factura (IdFactura)
);

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
