import re
import unicodedata

import pandas as pd


PALABRAS_CATEGORIA = {
    "playeras": [
        "t-shirt",
        "t shirt",
        "tee",
        "top",
        "playera",
    ],
    "camisetas": [
        "camiseta",
        "jersey",
    ],
    "blusas": [
        "blouse",
        "blusa",
    ],
    "camisas": [
        "shirt",
        "overshirt",
        "button-down",
        "button down",
        "camisa",
    ],
    "polos": [
        "polo shirt",
        "polo",
    ],
    "sudaderas": [
        "hoodie",
        "hooded",
        "sweatshirt",
        "sweat top",
        "sudadera",
    ],
    "chamarras": [
        "jacket",
        "bomber",
        "puffer",
        "parka",
        "chamarra",
    ],
    "abrigos": [
        "coat",
        "overcoat",
        "trench",
        "abrigo",
    ],
    "suéteres": [
        "sweater",
        "jumper",
        "pullover",
        "cardigan",
        "sueter",
    ],
    "jeans": [
        "jeans",
        "denim jeans",
    ],
    "pantalones cargo": [
        "cargo pants",
        "cargo trousers",
        "cargo",
    ],
    "pantalones": [
        "pants",
        "trousers",
        "slacks",
        "chinos",
        "pantalon",
    ],
    "shorts": [
        "shorts",
        "bermuda",
    ],
    "joggers": [
        "joggers",
        "jogger",
        "track pants",
        "sweatpants",
    ],
    "vestidos": [
        "dress",
        "gown",
        "vestido",
    ],
    "faldas": [
        "skirt",
        "falda",
    ],
    "leggins": [
        "leggings",
        "legging",
        "tights",
    ],

"sandalias": [
    "sandals",
    "sandal",
    "flip flops",
    "flip-flops",
    "espadrilles",
    "espadrille",
    "slides",
    "slide",
    "sliders",
    "slider",
],
"mocasines": [
    "loafers",
    "loafer",
    "drivers",
    "driver",
    "monk",
    "mules",
    "mule",
    "brogues",
    "brogue",
],
    "tenis": [
        "sneakers",
        "sneaker",
        "trainers",
        "trainer",
        "running shoes",
        "sports shoes",
        "shoe",
    ],
    "botas": [
        "boots",
        "boot",
        "ankle boots",
        "botines",
    ],
    "bolsas": [
        "bag",
        "handbag",
        "tote",
        "crossbody",
        "shoulder bag",
        "clutch",
        "bolsa",
    ],
    "gorras": [
        "cap",
        "baseball cap",
        "hat",
        "gorra",
    ],
    "accesorios": [
    "sunglasses",
    "necklace",
    "scarf",
    "socks",
],
"ropa_interior": [
    "bra",
    "thong",
    "bodysuit",
    "bikini bottoms",
],
"zuecos": [
    "clogs",
    "clog",
],
}


def normalizar_texto(texto) -> str:
    if pd.isna(texto):
        return ""

    texto = str(texto).lower().strip()

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
        r"[^a-z0-9\s\-]",
        " ",
        texto,
    )

    texto = re.sub(
        r"\s+",
        " ",
        texto,
    ).strip()

    return texto


def detectar_categoria(nombre_producto) -> str:
    nombre = normalizar_texto(nombre_producto)

    for categoria, palabras in PALABRAS_CATEGORIA.items():
        for palabra in palabras:
            palabra_normalizada = normalizar_texto(
                palabra
            )

            if palabra_normalizada in nombre:
                return categoria

    return "sin_clasificar"


def agregar_categoria_detectada(
    catalogo: pd.DataFrame,
) -> pd.DataFrame:
    catalogo_nuevo = catalogo.copy()

    catalogo_nuevo["categoria_detectada"] = (
        catalogo_nuevo["nombre"]
        .apply(detectar_categoria)
    )

    return catalogo_nuevo


def agregar_tendencias(
    catalogo: pd.DataFrame,
    resumen_tendencias: pd.DataFrame,
) -> pd.DataFrame:
    catalogo_nuevo = catalogo.copy()
    tendencias = resumen_tendencias.copy()

    tendencias["clave_categoria"] = (
        tendencias["termino"]
        .apply(normalizar_texto)
    )

    catalogo_nuevo["clave_categoria"] = (
        catalogo_nuevo["categoria_detectada"]
        .apply(normalizar_texto)
    )

    columnas_tendencias = [
        "clave_categoria",
        "interes_promedio",
        "interes_reciente",
        "crecimiento_pct",
        "tendencia",
    ]

    catalogo_nuevo = catalogo_nuevo.merge(
        tendencias[columnas_tendencias],
        how="left",
        on="clave_categoria",
    )

    catalogo_nuevo = catalogo_nuevo.drop(
        columns="clave_categoria"
    )

    catalogo_nuevo["tiene_tendencia"] = (
        catalogo_nuevo["interes_reciente"]
        .notna()
    )

    return catalogo_nuevo


def generar_reporte_clasificacion(
    catalogo: pd.DataFrame,
) -> None:
    total = len(catalogo)

    clasificados = (
        catalogo["categoria_detectada"]
        .ne("sin_clasificar")
        .sum()
    )

    vinculados = (
        catalogo["tiene_tendencia"]
        .sum()
    )

    porcentaje_clasificado = (
        clasificados / total * 100
        if total > 0
        else 0
    )

    porcentaje_vinculado = (
        vinculados / total * 100
        if total > 0
        else 0
    )

    print(
        "\n========== CLASIFICACIÓN DE PRODUCTOS ==========\n"
    )

    print(f"Productos totales: {total}")
    print(f"Productos clasificados: {clasificados}")
    print(
        f"Porcentaje clasificado: "
        f"{porcentaje_clasificado:.2f}%"
    )

    print(
        f"\nProductos vinculados con Trends: "
        f"{vinculados}"
    )

    print(
        f"Porcentaje vinculado: "
        f"{porcentaje_vinculado:.2f}%"
    )

    print("\nCategorías detectadas:")
    print(
        catalogo["categoria_detectada"]
        .value_counts()
        .head(20)
    )

    print("\nEjemplos sin clasificar:")
    print(
        catalogo.loc[
            catalogo["categoria_detectada"]
            .eq("sin_clasificar"),
            [
                "nombre",
                "fuente",
            ],
        ].head(20)
    )