SELECT 'codigo_natureza_juridica' AS coluna, MIN(codigo_natureza_juridica) AS minimo, MAX(codigo_natureza_juridica) AS maximo FROM dataset_empresa1
UNION
SELECT 'codigo_qualificacao_responsavel' AS coluna, MIN(codigo_qualificacao_responsavel) AS minimo, MAX(codigo_qualificacao_responsavel) AS maximo FROM dataset_empresa1
UNION
SELECT 'codigo_porte' AS coluna, MIN(codigo_porte) AS minimo, MAX(codigo_porte) AS maximo FROM dataset_empresa1
UNION
SELECT 'ente_responsavel_codigo_municipio' AS coluna, MIN(ente_responsavel_codigo_municipio) AS minimo, MAX(ente_responsavel_codigo_municipio) AS maximo FROM dataset_empresa1
UNION
SELECT 'codigo_situacao_cadastral' AS coluna, MIN(codigo_situacao_cadastral) AS minimo, MAX(codigo_situacao_cadastral) AS maximo FROM dataset_empresa1
UNION
SELECT 'codigo_motivo_situacao_cadastral' AS coluna, MIN(codigo_motivo_situacao_cadastral) AS minimo, MAX(codigo_motivo_situacao_cadastral) AS maximo FROM dataset_empresa1
UNION
SELECT 'codigo_pais' AS coluna, MIN(codigo_pais) AS minimo, MAX(codigo_pais) AS maximo FROM dataset_empresa1
UNION
SELECT 'codigo_municipio' AS coluna, MIN(codigo_municipio) AS minimo, MAX(codigo_municipio) AS maximo FROM dataset_empresa1;
