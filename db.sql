CREATE TABLE `usuarios` (
  `id` INT,
  `cpf` CHAR(11),
  `nome` CHAR(50),
  `email` CHAR(30),
  `password` CHAR(12),
  `id_coleta` INT
);

CREATE TABLE `coleta` (
  `id_coleta` INT,
  `cep` CHAR(5),
  `end` VARCHAR(50),
  `num` CHAR,
  `bairro` CHAR(30),
  `cidade` CHAR(50),
  `uf` CHAR(2),
  `data_coleta` DATE,
  `hora_programada` TIME,
  `id_material` INT
);

CREATE TABLE `material` (
  `id_material` INT,
  `classificado` TINYINT
);


