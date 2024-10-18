DROP TABLE IF EXISTS empresa_norte;
CREATE TABLE empresa_norte AS
  SELECT
    e.uuid,
    c.uuid AS empresa_uuid,
    c.razao_social,
    c.codigo_natureza_juridica,
    c.codigo_qualificacao_responsavel,
    c.capital_social,
    c.codigo_porte,
    c.ente_responsavel_uf,
    c.ente_responsavel_codigo_municipio,
    e.cnpj,
    e.matriz,
    e.nome_fantasia,
    e.codigo_situacao_cadastral,
    e.data_situacao_cadastral,
    e.codigo_motivo_situacao_cadastral,
    e.cidade_exterior,
    e.codigo_pais,
    e.data_inicio_atividade,
    e.cnae_principal,
    e.cnae_secundaria,
    e.tipo_logradouro,
    e.logradouro,
    e.numero,
    e.complemento,
    e.bairro,
    e.cep,
    e.uf,
    e.codigo_municipio,
    e.ddd_1,
    e.telefone_1,
    e.ddd_2,
    e.telefone_2,
    e.ddd_fax,
    e.fax,
    e.email,
    e.situacao_especial,
    e.data_situacao_especial
  FROM estabelecimento AS e
    LEFT JOIN empresa AS c
      ON e.empresa_uuid = c.uuid
  WHERE e.uf IN ('AC', 'AP', 'AM', 'PA', 'RO', 'RR', 'TO');
