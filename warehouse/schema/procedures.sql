CREATE PROCEDURE CambiarEstado(IN id INT, IN estado INT)
LANGUAGE SQL
AS $$
UPDATE articulo
SET idestado = estado
WHERE idarticulo = id
$$;

