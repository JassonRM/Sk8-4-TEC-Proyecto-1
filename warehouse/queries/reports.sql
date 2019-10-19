-- Gets characteristic information about a Cliente and its points
CREATE PROCEDURE PuntosClientes()
LANGUAGE SQL
AS $$
    SELECT Cliente.IdCliente, P.Nombre, Cliente.Puntos
    FROM Cliente
             INNER JOIN Persona P ON Cliente.IdPersona = P.IdPersona
$$;