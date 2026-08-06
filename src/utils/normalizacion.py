import re
import unicodedata

import pandas as pd


# ==========================================================
# FUNCIONES GENERALES
# ==========================================================

def normalizar_texto(texto) -> str:
    """Limpia espacios, acentos y diferencias de mayúsculas."""

    if pd.isna(texto):
        return ""

    texto = str(texto).strip().lower()

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
        r"\s+",
        " ",
        texto,
    ).strip()

    return texto


# ==========================================================
# NORMALIZACIÓN DE MARCAS
# ==========================================================

MAPEO_MARCAS = {
    "asos design": "ASOS DESIGN",
    "adidas performance": "Adidas",
    "adidas originals": "Adidas",
    "adidas": "Adidas",
    "nike": "Nike",
    "reebok": "Reebok",
    "hugo red": "HUGO",
    "hugo blue": "HUGO",
    "hugo": "HUGO",
    "mango": "Mango",
    "keen": "Keen",
    "h&m": "H&M",
    "seqwl": "SEQWL",
    "allsaints": "AllSaints",
    "jack & jones": "Jack & Jones",
    "tommy jeans": "Tommy Jeans",
    "walk london": "Walk London",
}


def normalizar_marca(marca) -> str:
    """Estandariza los nombres de las marcas."""

    marca_limpia = normalizar_texto(marca)

    if not marca_limpia:
        return "Sin marca"

    if marca_limpia in MAPEO_MARCAS:
        return MAPEO_MARCAS[marca_limpia]

    return str(marca).strip().title()


def identificar_tipo_marca(
    marca_normalizada: str,
    fuente: str,
) -> str:
    """
    Distingue marcas propias de marcas externas.

    ASOS DESIGN es marca propia de ASOS.
    H&M es marca propia de H&M.
    """

    fuente_limpia = normalizar_texto(fuente)
    marca_limpia = normalizar_texto(
        marca_normalizada
    )

    if (
        fuente_limpia == "asos"
        and marca_limpia == "asos design"
    ):
        return "Propia"

    if (
        fuente_limpia == "h&m"
        and marca_limpia == "h&m"
    ):
        return "Propia"

    return "Externa"


# ==========================================================
# NORMALIZACIÓN DE COLORES
# ==========================================================

MAPEO_COLORES = {
    "black": "Negro",
    "white": "Blanco",
    "brown": "Café",
    "beige": "Beige",
    "cream": "Crema",
    "ivory": "Marfil",
    "gray": "Gris",
    "grey": "Gris",
    "charcoal": "Gris oscuro",
    "green": "Verde",
    "khaki": "Caqui",
    "olive": "Oliva",
    "teal": "Verde azulado",
    "red": "Rojo",
    "burgundy": "Vino",
    "blue": "Azul",
    "navy": "Azul marino",
    "denim": "Azul",
    "yellow": "Amarillo",
    "orange": "Naranja",
    "pink": "Rosa",
    "purple": "Morado",
    "taupe": "Topo",
    "stone": "Piedra",
    "tan": "Camel",
    "camel": "Camel",
    "multi": "Multicolor",
    "silver": "Plateado",
    "gold": "Dorado",
}


def normalizar_color(color) -> str:
    """Agrupa variantes de color en nombres estandarizados."""

    color_limpio = normalizar_texto(color)

    if not color_limpio:
        return "Sin especificar"

    # Los colores compuestos o estampados múltiples
    # se priorizan como multicolor.
    if "multi" in color_limpio:
        return "Multicolor"

    for palabra, color_normalizado in (
        MAPEO_COLORES.items()
    ):
        if palabra in color_limpio:
            return color_normalizado

    return str(color).strip().title()


# ==========================================================
# NORMALIZACIÓN DE CATEGORÍAS
# ==========================================================

MAPEO_CATEGORIAS_GENERALES = {
    "playeras": "Parte superior",
    "camisetas": "Parte superior",
    "blusas": "Parte superior",
    "camisas": "Parte superior",
    "polos": "Parte superior",

    "sudaderas": "Abrigos y capas",
    "chamarras": "Abrigos y capas",
    "abrigos": "Abrigos y capas",
    "sueteres": "Abrigos y capas",

    "zuecos": "Calzado",
    "accesorios": "Accesorios",
    "ropa_interior": "Ropa interior",

    "jeans": "Parte inferior",
    "pantalones cargo": "Parte inferior",
    "pantalones": "Parte inferior",
    "shorts": "Parte inferior",
    "joggers": "Parte inferior",
    "faldas": "Parte inferior",
    "leggins": "Parte inferior",

    "vestidos": "Vestidos",

    "tenis": "Calzado",
    "botas": "Calzado",
    "sandalias": "Calzado",
    "mocasines": "Calzado",

    "bolsas": "Accesorios",
    "gorras": "Accesorios",

    "sin_clasificar": "Sin clasificar",
}


def normalizar_categoria(categoria) -> str:
    """Estandariza el nombre de la categoría detectada."""

    categoria_limpia = normalizar_texto(
        categoria
    )

    if not categoria_limpia:
        return "sin_clasificar"

    return categoria_limpia


def obtener_categoria_general(
    categoria_normalizada: str,
) -> str:
    """Agrupa categorías específicas en grupos generales."""

    return MAPEO_CATEGORIAS_GENERALES.get(
        categoria_normalizada,
        "Otra",
    )


# ==========================================================
# NORMALIZACIÓN DE PRECIOS
# ==========================================================

def clasificar_rango_precio(precio) -> str:
    """Clasifica el precio en cuatro segmentos."""

    if pd.isna(precio):
        return "Sin precio"

    if precio < 30:
        return "Económico"

    if precio < 80:
        return "Medio"

    if precio < 150:
        return "Premium"

    return "Lujo"


# ==========================================================
# NORMALIZACIÓN COMPLETA
# ==========================================================

def normalizar_catalogo(
    catalogo: pd.DataFrame,
) -> pd.DataFrame:
    """
    Conserva los datos originales y crea columnas
    normalizadas para análisis posteriores.
    """

    catalogo_normalizado = catalogo.copy()

    columnas_requeridas = [
        "marca",
        "color",
        "fuente",
        "precio_actual",
    ]

    columnas_faltantes = [
        columna
        for columna in columnas_requeridas
        if columna not in catalogo_normalizado.columns
    ]

    if columnas_faltantes:
        raise ValueError(
            "Faltan columnas requeridas en el catálogo: "
            + ", ".join(columnas_faltantes)
        )

    # ------------------------------------------------------
    # CONSERVAR VALORES ORIGINALES
    # ------------------------------------------------------

    catalogo_normalizado["marca_original"] = (
        catalogo_normalizado["marca"]
    )

    catalogo_normalizado["color_original"] = (
        catalogo_normalizado["color"]
    )

    if (
        "categoria_detectada"
        in catalogo_normalizado.columns
    ):
        catalogo_normalizado["categoria_original"] = (
            catalogo_normalizado[
                "categoria_detectada"
            ]
        )
    else:
        catalogo_normalizado["categoria_original"] = (
            "sin_clasificar"
        )

    # ------------------------------------------------------
    # MARCAS
    # ------------------------------------------------------

    catalogo_normalizado["marca_normalizada"] = (
        catalogo_normalizado["marca_original"]
        .apply(normalizar_marca)
    )

    catalogo_normalizado["tipo_marca"] = (
        catalogo_normalizado.apply(
            lambda fila: identificar_tipo_marca(
                fila["marca_normalizada"],
                fila["fuente"],
            ),
            axis=1,
        )
    )

    # ------------------------------------------------------
    # COLORES
    # ------------------------------------------------------

    catalogo_normalizado["color_normalizado"] = (
        catalogo_normalizado["color_original"]
        .apply(normalizar_color)
    )

    # ------------------------------------------------------
    # CATEGORÍAS
    # ------------------------------------------------------

    catalogo_normalizado[
        "categoria_normalizada"
    ] = (
        catalogo_normalizado["categoria_original"]
        .apply(normalizar_categoria)
    )

    catalogo_normalizado["categoria_general"] = (
        catalogo_normalizado[
            "categoria_normalizada"
        ]
        .apply(obtener_categoria_general)
    )

    # ------------------------------------------------------
    # PRECIOS
    # ------------------------------------------------------

    catalogo_normalizado["precio_actual"] = (
        pd.to_numeric(
            catalogo_normalizado[
                "precio_actual"
            ],
            errors="coerce",
        )
    )

    catalogo_normalizado["rango_precio"] = (
        catalogo_normalizado["precio_actual"]
        .apply(clasificar_rango_precio)
    )

    return catalogo_normalizado


# ==========================================================
# REPORTE DE NORMALIZACIÓN
# ==========================================================

def generar_reporte_normalizacion(
    catalogo: pd.DataFrame,
) -> None:
    """Muestra un diagnóstico de la normalización."""

    print(
        "\n========== NORMALIZACIÓN DE DATOS ==========\n"
    )

    print(f"Productos procesados: {len(catalogo)}")

    print("\nTipos de marca:")
    print(
        catalogo["tipo_marca"]
        .value_counts(dropna=False)
    )

    print("\nMarcas normalizadas principales:")
    print(
        catalogo["marca_normalizada"]
        .value_counts(dropna=False)
        .head(15)
    )

    print("\nColores normalizados principales:")
    print(
        catalogo["color_normalizado"]
        .value_counts(dropna=False)
        .head(15)
    )

    print("\nCategorías generales:")
    print(
        catalogo["categoria_general"]
        .value_counts(dropna=False)
    )

    print("\nRangos de precio:")
    print(
        catalogo["rango_precio"]
        .value_counts(dropna=False)
    )

    cantidad_sin_clasificar = (
        catalogo["categoria_normalizada"]
        .eq("sin_clasificar")
        .sum()
    )

    print("\nProductos sin clasificar:")
    print(cantidad_sin_clasificar)

    print("\nEjemplos sin clasificar:")
    print(
        catalogo.loc[
            catalogo[
                "categoria_normalizada"
            ].eq("sin_clasificar"),
            [
                "nombre",
                "fuente",
                "categoria_original",
            ],
        ].head(30)
    )

    print("\nEjemplos clasificados como Otra:")
    print(
        catalogo.loc[
            catalogo["categoria_general"].eq(
                "Otra"
            ),
            [
                "nombre",
                "fuente",
                "categoria_normalizada",
            ],
        ].head(20)
    )

    print(
        "\n============================================"
    )