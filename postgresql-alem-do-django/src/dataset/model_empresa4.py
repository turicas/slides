import django.contrib.postgres.indexes as pg_indexes
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVectorField

from . import choices


class EmpresaQuerySet(models.QuerySet):
    def search(self, term):
        qs = self

        if term:
            query = SearchQuery(term, config="pg_catalog.portuguese", search_type="websearch")
            qs = qs.annotate(search_rank=SearchRank(models.F("search_data"), query)).filter(search_data=query)
            # Overwriting `qs.query.order_by` to APPEND ordering field
            # instead of OVERWRITTING (as in `qs.order_by`). We append directly
            # (instead of using `qs.query.add_ordering` because the search rank
            # must have precedence over the other ordering.
            qs.query.order_by = tuple(["-search_rank"] + list(qs.query.order_by))
        return qs

    def order_by(self, *args, **kwargs):
        # We must force search_rank ordering, since some operations will add
        # ordering after calling `.search` (like in Django Admin)
        qs = super().order_by(*args, **kwargs)
        if "-search_rank" in qs.query.order_by and qs.query.order_by[0] != "-search_rank":
            qs.query.order_by = tuple(["-search_rank"] + [item for item in qs.query.order_by if item != "-search_rank"])
        return qs


class Empresa4(models.Model):
    objects = EmpresaQuerySet.as_manager()

    # 16 bytes:
    uuid = models.UUIDField(blank=False, null=False, primary_key=True)
    empresa_uuid = models.UUIDField(blank=False, null=False)

    # 4 bytes:
    data_situacao_cadastral = models.DateField(null=True, blank=True)
    data_inicio_atividade = models.DateField(blank=False, null=False)
    data_situacao_especial = models.DateField(blank=True, null=True)
    cnae_principal = models.IntegerField(blank=False, null=False, choices=choices.CNAE)

    # 2 bytes:
    codigo_natureza_juridica = models.SmallIntegerField(blank=False, null=False, choices=choices.NATUREZA_JURIDICA)
    codigo_qualificacao_responsavel = models.SmallIntegerField(blank=False, null=False, choices=choices.QUALIFICACAO_SOCIO)
    codigo_porte = models.SmallIntegerField(blank=False, null=False, choices=choices.PORTE)
    ente_responsavel_codigo_municipio = models.SmallIntegerField(blank=True, null=True, choices=choices.MUNICIPIO)
    codigo_situacao_cadastral = models.SmallIntegerField(blank=False, null=False, choices=choices.SITUACAO_CADASTRAL)
    codigo_motivo_situacao_cadastral = models.SmallIntegerField(blank=False, null=False, choices=choices.MOTIVO_SITUACAO_CADASTRAL)
    codigo_pais = models.SmallIntegerField(blank=True, null=True, choices=choices.PAIS)
    codigo_municipio = models.SmallIntegerField(blank=False, null=False, choices=choices.MUNICIPIO)

    # 1 byte:
    matriz = models.BooleanField(blank=False, null=False)

    # Variable length:
    capital_social = models.DecimalField(max_digits=16, decimal_places=2, blank=False, null=False)
    razao_social = models.TextField(blank=False, null=False, max_length=200)
    ente_responsavel_uf = models.TextField(blank=True, null=True, max_length=2)
    cnpj = models.TextField(blank=False, null=False, max_length=14)
    nome_fantasia = models.TextField(blank=True, null=True, max_length=63)
    cidade_exterior = models.TextField(blank=True, null=True)
    tipo_logradouro = models.TextField(blank=True, null=True, max_length=20)
    logradouro = models.TextField(blank=True, null=True, max_length=100)
    numero = models.TextField(blank=True, null=True, max_length=16)
    complemento = models.TextField(blank=True, null=True, max_length=200)
    bairro = models.TextField(blank=True, null=True, max_length=63)
    cep = models.TextField(blank=True, null=True, max_length=8)
    uf = models.TextField(blank=False, null=False, max_length=2)
    ddd_1 = models.TextField(blank=True, null=True, max_length=4)
    telefone_1 = models.TextField(blank=True, null=True, max_length=8)
    ddd_2 = models.TextField(blank=True, null=True, max_length=4)
    telefone_2 = models.TextField(blank=True, null=True, max_length=8)
    ddd_fax = models.TextField(blank=True, null=True, max_length=4)
    fax = models.TextField(blank=True, null=True, max_length=8)
    email = models.TextField(blank=True, null=True, max_length=120)
    situacao_especial = models.TextField(blank=True, null=True, max_length=20)
    # PostgreSQL-specific:
    cnae_secundaria = ArrayField(models.IntegerField(), null=True, blank=True, max_length=99)
    search_data = SearchVectorField(null=True)

    class Meta:
        index_together = (
            ("uf", "codigo_situacao_cadastral"),
        )
        indexes = (
            pg_indexes.GinIndex(fields=["search_data"]),
        )

