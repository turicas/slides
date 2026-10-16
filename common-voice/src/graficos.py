"""Gera os gráficos (SVG) da palestra a partir dos dados públicos do Common Voice.

Usa só a stdlib: os gráficos são barras horizontais simples e SVG escrito à mão fica nítido no projetor e não exige
matplotlib. Entradas: o JSON de `https://commonvoice.mozilla.org/api/v1/stats/languages` (números ao vivo) e os
metadados de uma versão publicada do _dataset_ (`datasets/scripted-speech/cv-corpus-*.json` do repositório
`common-voice/cv-dataset`), que trazem a proporção de gravações por gênero declarado - dado que a API não expõe.
"""

import argparse
import json
import sys
from collections.abc import Callable
from dataclasses import dataclass
from html import escape
from pathlib import Path

NOMES_PT = {
    "ab": "Abcázio",
    "be": "Bielorrusso",
    "bn": "Bengali",
    "ca": "Catalão",
    "de": "Alemão",
    "en": "Inglês",
    "eo": "Esperanto",
    "es": "Espanhol",
    "eu": "Basco",
    "fr": "Francês",
    "gl": "Galego",
    "it": "Italiano",
    "kab": "Cabila",
    "ps": "Pachto",
    "pt": "Português",
    "ro": "Romeno",
    "rw": "Kinyarwanda",
    "th": "Tailandês",
    "ug": "Uigur",
}
LINGUAS_LATINAS = ("ca", "fr", "es", "it", "gl", "pt", "ro")
LINGUAS_COMPARACAO_GENERO = ("ca", "fr", "es", "it", "gl", "pt", "en", "de")
NOMES_GENERO = {
    "male_masculine": "Masculino",
    "female_feminine": "Feminino",
    "": "Não informado",
}
# Tabela 10 (WER % no Multilingual LibriSpeech) de Radford et al. (2022), "Robust Speech Recognition via Large-Scale
# Weak Supervision", https://arxiv.org/abs/2212.04356
WHISPER_MLS = {
    "tiny": {"en": 15.7, "pt": 31.3},
    "base": {"en": 11.7, "pt": 21.9},
    "small": {"en": 8.3, "pt": 13.0},
    "medium": {"en": 6.8, "pt": 9.0},
    "large-v2": {"en": 6.2, "pt": 6.8},
}

COR_DESTAQUE = "#E00000"
COR_BARRA = "#B4B4B4"
COR_TEXTO = "#222222"
COR_TEXTO_SUAVE = "#666666"
FONTE = "Lato, 'Helvetica Neue', Arial, sans-serif"


@dataclass
class Lingua:
    codigo: str
    nome: str
    horas_validadas: float
    falantes: int
    frases: int


def formata_numero(valor: float) -> str:
    """Formata no padrão brasileiro (`1.234.567`); valores abaixo de 10 mantêm uma casa decimal."""
    if valor < 10 and valor != int(valor):
        return f"{valor:.1f}".replace(".", ",")
    return f"{round(valor):,}".replace(",", ".")


def formata_percentual(proporcao: float) -> str:
    return f"{proporcao * 100:.1f}%".replace(".", ",")


def le_generos(caminho: Path) -> dict[str, dict[str, float]]:
    """Proporção de gravações por gênero declarado, por língua (chaves como no _dataset_: `female_feminine` etc.)."""
    return {codigo: dados["splits"]["gender"] for codigo, dados in json.loads(caminho.read_text())["locales"].items()}


def le_linguas(caminho: Path) -> list[Lingua]:
    linguas = []
    for registro in json.loads(caminho.read_text()):
        if not registro["recordedHours"]:
            continue
        linguas.append(
            Lingua(
                codigo=registro["locale"],
                nome=NOMES_PT.get(registro["locale"], registro["english_name"]),
                horas_validadas=registro["validatedHours"],
                falantes=registro["speakersCount"],
                frases=registro["sentencesCount"]["currentCount"],
            )
        )
    return linguas


def abre_svg(largura: int, altura: float) -> list[str]:
    return [
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {largura} {altura}" width="{largura}" '
            f'height="{altura}" font-family="{FONTE}">'
        ),
        f'<rect width="{largura}" height="{altura}" fill="#ffffff"/>',
    ]


def titulo_svg(largura: int, titulo: str) -> str:
    return (
        f'<text x="{largura / 2}" y="36" font-size="28" fill="{COR_TEXTO}" text-anchor="middle">{escape(titulo)}</text>'
    )


def svg_barras(
    linhas: list[tuple[str, float, bool] | None],
    titulo: str,
    nota: str,
    formatador: Callable[[float], str] = formata_numero,
) -> str:
    """Barras horizontais; cada linha é `(rótulo, valor, destaque)` e `None` vira uma linha de reticências."""
    largura, margem_esquerda, margem_direita = 960, 230, 130
    altura_linha, espaco, topo = 34, 8, 64
    altura = topo + len(linhas) * (altura_linha + espaco) + 50
    maximo = max(linha[1] for linha in linhas if linha is not None)
    largura_util = largura - margem_esquerda - margem_direita
    partes = [
        *abre_svg(largura, altura),
        titulo_svg(largura, titulo),
    ]
    for indice, linha in enumerate(linhas):
        y = topo + indice * (altura_linha + espaco)
        meio = y + altura_linha / 2 + 7
        if linha is None:
            partes.append(
                f'<text x="{margem_esquerda - 14}" y="{meio}" font-size="22" fill="{COR_TEXTO_SUAVE}" '
                'text-anchor="end">...</text>'
            )
            continue
        rotulo, valor, destaque = linha
        largura_barra = max(2, largura_util * valor / maximo)
        cor = COR_DESTAQUE if destaque else COR_BARRA
        peso = "bold" if destaque else "normal"
        partes.append(
            f'<text x="{margem_esquerda - 14}" y="{meio}" font-size="21" font-weight="{peso}" fill="{COR_TEXTO}" '
            f'text-anchor="end">{escape(rotulo)}</text>'
        )
        partes.append(
            f'<rect x="{margem_esquerda}" y="{y}" width="{largura_barra:.1f}" height="{altura_linha}" rx="3" '
            f'fill="{cor}"><title>{escape(rotulo)}: {formatador(valor)}</title></rect>'
        )
        partes.append(
            f'<text x="{margem_esquerda + largura_barra + 10:.1f}" y="{meio}" font-size="20" font-weight="{peso}" '
            f'fill="{COR_TEXTO if destaque else COR_TEXTO_SUAVE}">{formatador(valor)}</text>'
        )
    partes.append(
        f'<text x="{largura / 2}" y="{altura - 16}" font-size="15" fill="{COR_TEXTO_SUAVE}" '
        f'text-anchor="middle">{escape(nota)}</text>'
    )
    partes.append("</svg>")
    return "\n".join(partes)


def ranking(linguas: list[Lingua], campo: str, quantidade_topo: int) -> list[tuple[str, float, bool] | None]:
    """Top N + Português com sua posição (se Português já estiver no top N, não repete)."""
    ordenadas = sorted(linguas, key=lambda lingua: -getattr(lingua, campo))
    linhas: list[tuple[str, float, bool] | None] = []
    for posicao, lingua in enumerate(ordenadas, start=1):
        rotulo = f"{posicao}º {lingua.nome}"
        if posicao <= quantidade_topo:
            linhas.append((rotulo, getattr(lingua, campo), lingua.codigo == "pt"))
        elif lingua.codigo == "pt":
            linhas.append(None)
            linhas.append((rotulo, getattr(lingua, campo), True))
            break
    return linhas


def svg_whisper() -> str:
    """Barras agrupadas (Inglês x Português) de WER por tamanho de modelo do Whisper."""
    largura, altura = 960, 600
    margem_esquerda, margem_inferior, topo = 70, 110, 90
    base = altura - margem_inferior
    maximo = 35
    altura_util = base - topo
    largura_grupo = (largura - margem_esquerda - 30) / len(WHISPER_MLS)
    largura_barra = 62
    cores = {"en": COR_BARRA, "pt": COR_DESTAQUE}
    partes = [
        *abre_svg(largura, altura),
        titulo_svg(largura, "Whisper: % de palavras erradas (menor = melhor)"),
    ]
    for legenda_x, (lingua, nome) in zip((340, 520), (("en", "Inglês"), ("pt", "Português"))):
        partes.append(f'<rect x="{legenda_x}" y="54" width="22" height="22" rx="3" fill="{cores[lingua]}"/>')
        partes.append(f'<text x="{legenda_x + 30}" y="72" font-size="20" fill="{COR_TEXTO}">{nome}</text>')
    for linha_grade in (10, 20, 30):
        y = base - altura_util * linha_grade / maximo
        partes.append(
            f'<line x1="{margem_esquerda}" x2="{largura - 30}" y1="{y:.1f}" y2="{y:.1f}" stroke="#e6e6e6" stroke-width="1"/>'
        )
        partes.append(
            f'<text x="{margem_esquerda - 10}" y="{y + 6:.1f}" font-size="16" fill="{COR_TEXTO_SUAVE}" '
            f'text-anchor="end">{linha_grade}%</text>'
        )
    partes.append(
        f'<line x1="{margem_esquerda}" x2="{largura - 30}" y1="{base}" y2="{base}" stroke="{COR_TEXTO_SUAVE}" stroke-width="1"/>'
    )
    for indice, (modelo, valores) in enumerate(WHISPER_MLS.items()):
        centro = margem_esquerda + largura_grupo * (indice + 0.5)
        for deslocamento, lingua in ((-largura_barra - 2, "en"), (2, "pt")):
            valor = valores[lingua]
            valor_formatado = f"{valor:.1f}".replace(".", ",")
            altura_barra = altura_util * valor / maximo
            x = centro + deslocamento
            partes.append(
                f'<rect x="{x:.1f}" y="{base - altura_barra:.1f}" width="{largura_barra}" height="{altura_barra:.1f}" '
                f'rx="3" fill="{cores[lingua]}"><title>{modelo} ({lingua}): {valor_formatado}%</title></rect>'
            )
            peso = "bold" if lingua == "pt" else "normal"
            partes.append(
                f'<text x="{x + largura_barra / 2:.1f}" y="{base - altura_barra - 8:.1f}" font-size="18" '
                f'font-weight="{peso}" fill="{COR_TEXTO}" text-anchor="middle">{valor_formatado}</text>'
            )
        partes.append(
            f'<text x="{centro:.1f}" y="{base + 30}" font-size="21" fill="{COR_TEXTO}" text-anchor="middle">{modelo}</text>'
        )
    partes.append(
        f'<text x="{margem_esquerda + largura_grupo / 2:.1f}" y="{base + 54}" font-size="15" fill="{COR_TEXTO_SUAVE}" '
        'text-anchor="middle">menor/mais rápido</text>'
    )
    partes.append(
        f'<text x="{margem_esquerda + largura_grupo * 4.5:.1f}" y="{base + 54}" font-size="15" '
        f'fill="{COR_TEXTO_SUAVE}" text-anchor="middle">maior/mais pesado</text>'
    )
    partes.append(
        f'<text x="{largura / 2}" y="{altura - 14}" font-size="15" fill="{COR_TEXTO_SUAVE}" text-anchor="middle">'
        "Fonte: Radford et al. (2022), arxiv.org/abs/2212.04356 - Tabela 10 (Multilingual LibriSpeech)</text>"
    )
    partes.append("</svg>")
    return "\n".join(partes)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("entrada", type=Path, help="JSON de /api/v1/stats/languages")
    parser.add_argument("saida", type=Path, help="Pasta onde os SVGs serão salvos")
    parser.add_argument("--data", required=True, help="Data da coleta (YYYY-MM-DD), exibida nas notas")
    parser.add_argument("--metadados", type=Path, required=True, help="JSON `cv-corpus-*.json` do cv-dataset")
    parser.add_argument("--versao", required=True, help="Versão do dataset dos metadados (ex: 27.0)")
    args = parser.parse_args()

    linguas = le_linguas(args.entrada)
    generos = le_generos(args.metadados)
    nota = f"Fonte: API do Common Voice (commonvoice.mozilla.org), coletado em {args.data}"
    nota_genero = f"Fonte: Common Voice Scripted Speech {args.versao} (github.com/common-voice/cv-dataset)"
    feminino = {codigo: generos[codigo].get("female_feminine", 0) for codigo in LINGUAS_COMPARACAO_GENERO}
    graficos = {
        "ranking-horas.svg": svg_barras(ranking(linguas, "horas_validadas", 10), "Horas validadas", nota),
        "ranking-falantes.svg": svg_barras(ranking(linguas, "falantes", 10), "Pessoas que contribuíram", nota),
        "ranking-frases.svg": svg_barras(ranking(linguas, "frases", 10), "Frases disponíveis para gravar", nota),
        "latinas-horas.svg": svg_barras(
            [
                (lingua.nome, lingua.horas_validadas, lingua.codigo == "pt")
                for lingua in sorted(linguas, key=lambda lingua: -lingua.horas_validadas)
                if lingua.codigo in LINGUAS_LATINAS
            ],
            "Línguas latinas: horas validadas",
            nota,
        ),
        "whisper-ingles-portugues.svg": svg_whisper(),
        "genero-portugues.svg": svg_barras(
            [
                (nome, generos["pt"].get(chave, 0), chave == "female_feminine")
                for chave, nome in sorted(NOMES_GENERO.items(), key=lambda item: -generos["pt"].get(item[0], 0))
            ],
            "Português: gravações por gênero declarado",
            nota_genero,
            formatador=formata_percentual,
        ),
        "genero-feminino.svg": svg_barras(
            [
                (NOMES_PT[codigo], proporcao, codigo == "pt")
                for codigo, proporcao in sorted(feminino.items(), key=lambda item: -item[1])
            ],
            "Gravações com voz feminina declarada",
            nota_genero,
            formatador=formata_percentual,
        ),
    }
    args.saida.mkdir(parents=True, exist_ok=True)
    for nome, conteudo in graficos.items():
        (args.saida / nome).write_text(conteudo)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
