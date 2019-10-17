CREATE PROCEDURE CambiarEstado(IN id INT, IN estado INT)
LANGUAGE SQL
AS $$
UPDATE articulo
SET idestadoarticulo = estado
WHERE idarticulo = id
$$;


CREATE PROCEDURE PuntosClientes()
LANGUAGE SQL
AS $$
    SELECT Cliente.IdCliente, P.Nombre, Cliente.Puntos
    FROM Cliente
             INNER JOIN Persona P ON Cliente.IdPersona = P.IdPersona
$$;