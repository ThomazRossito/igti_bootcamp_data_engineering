CREATE TABLE Cad_Clientes.Clientes(
	cod_cliente INT PRIMARY KEY,
    nome_cliente VARCHAR(100) 
);

CREATE TABLE Cad_Clientes.Endereco(
	cod_endereco INT PRIMARY KEY,
    nome_endereco VARCHAR(100),
    descri_endereco VARCHAR(200),
    fk_Cliente_cod_cliente INTEGER
);

ALTER TABLE Cad_Clientes.Endereco
ADD CONSTRAINT fk_Endereco
	FOREIGN KEY (fk_Cliente_cod_cliente)
	REFERENCES Cad_Clientes.Clientes (cod_cliente)
    ON DELETE RESTRICT;
