"""
Funciones encargadas de extraer información del mensaje del usuario.
"""

from __future__ import annotations

import re
import unicodedata

from app.servicios import CATALOGO


# =====================================================
# CATÁLOGO
# =====================================================

CIUDADES_DISPONIBLES = sorted(
    CATALOGO["ciudad"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

CATEGORIAS_DISPONIBLES = sorted(
    CATALOGO["categoria_normalizada"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

MARCAS_DISPONIBLES = sorted(
    CATALOGO["marca_normalizada"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)


# =====================================================
# NORMALIZACIÓN
# =====================================================

def normalizar_texto(texto: str) -> str:

    texto = str(texto or "").lower().strip()

    texto = unicodedata.normalize(
        "NFKD",
        texto,
    )

    texto = "".join(
        caracter
        for caracter in texto
        if not unicodedata.combining(caracter)
    )

    texto = re.sub(
        r"[^a-z0-9$.,\s&]",
        " ",
        texto,
    )

    texto = re.sub(
        r"\s+",
        " ",
        texto,
    ).strip()

    return texto


# =====================================================
# EXTRACTORES
# =====================================================

def detectar_ciudades(
    mensaje: str,
) -> list[str]:

    texto = normalizar_texto(mensaje)

    ciudades = []

    for ciudad in CIUDADES_DISPONIBLES:

        if normalizar_texto(ciudad) in texto:

            ciudades.append(ciudad)

    return ciudades


def detectar_categoria(
    mensaje: str,
) -> str | None:

    texto = normalizar_texto(mensaje)

    for categoria in CATEGORIAS_DISPONIBLES:

        if normalizar_texto(categoria) in texto:

            return categoria

    return None


def detectar_marca(
    mensaje: str,
) -> str | None:

    texto = normalizar_texto(mensaje)

    for marca in MARCAS_DISPONIBLES:

        if normalizar_texto(marca) in texto:

            return marca

    return None


def detectar_presupuesto(
    mensaje: str,
) -> float | None:

    texto = normalizar_texto(mensaje)

    coincidencia_mil = re.search(
        r"(\d+(?:[.,]\d+)?)\s*mil",
        texto,
    )

    if coincidencia_mil:

        numero = coincidencia_mil.group(1)

        numero = numero.replace(",", ".")

        return float(numero) * 1000

    coincidencia = re.search(
        r"\$?\s*(\d[\d,]*(?:\.\d+)?)",
        texto,
    )

    if not coincidencia:

        return None

    numero = coincidencia.group(1)

    numero = numero.replace(",", "")

    try:

        return float(numero)

    except ValueError:

        return None