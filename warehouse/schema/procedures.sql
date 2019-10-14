CREATE PROCEDURE CambiarEstado(IN id INT, IN estado INT)
LANGUAGE SQL
AS $$
UPDATE articulo
SET idestadoarticulo = estado
WHERE idarticulo = id
$$;

