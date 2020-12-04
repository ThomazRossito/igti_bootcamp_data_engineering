SELECT  c.cod_cliente     AS `Código Cliente`,
		c.nome_cliente    AS `Nome Cliente`,
        e.cod_endereco    AS `Código Endereço`,
        e.nome_endereco	  AS `Nome Endereço`,
        e.descri_endereco AS `Descrição Endereço`
FROM Cad_Clientes.Clientes c
INNER JOIN Cad_Clientes.Endereco e
		ON c.cod_cliente = e.fk_Cliente_cod_cliente;