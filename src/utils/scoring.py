import pandas as pd


# ==========================================================
# SCORE POR TENDENCIA
# ==========================================================

def calcular_score_trends(
    fila: pd.Series,
) -> int:
    """
    Calcula la puntuación basada en Google Trends.

    Máximo:
        40 puntos
    """

    score = 0

    nivel = fila.get(
        "nivel_tendencia",
        "Sin información",
    )

    if nivel == "Alto":
        score += 30

    elif nivel == "Medio":
        score += 20

    elif nivel == "Bajo":
        score += 10

    crecimiento = fila.get(
        "crecimiento_pct",
        0,
    )

    if pd.isna(crecimiento):
        crecimiento = 0

    if crecimiento >= 20:
        score += 10

    elif crecimiento >= 10:
        score += 5

    elif crecimiento <= -20:
        score -= 10

    elif crecimiento <= -10:
        score -= 5

    return max(score, 0)

# ==========================================================
# APLICAR SCORE
# ==========================================================

def agregar_score_trends(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:

    nuevo = dataframe.copy()

    nuevo["score_trends"] = (
        nuevo.apply(
            calcular_score_trends,
            axis=1,
        )
    )

    return nuevo

# ==========================================================
# SCORE POR CLIMA
# ==========================================================

def calcular_score_clima(
    fila: pd.Series,
) -> int:
    """
    Calcula la puntuación según la compatibilidad
    entre el producto y el clima de la ciudad.

    Máximo:
        30 puntos
    """

    compatibilidad = fila.get(
        "compatibilidad_clima",
        0.5,
    )

    if pd.isna(compatibilidad):
        compatibilidad = 0.5

    if compatibilidad >= 0.9:
        return 30

    if compatibilidad >= 0.7:
        return 25

    if compatibilidad >= 0.5:
        return 15

    if compatibilidad >= 0.3:
        return 5

    return 0


def agregar_score_clima(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """Agrega la puntuación climática al catálogo."""

    nuevo = dataframe.copy()

    nuevo["score_clima"] = (
        nuevo.apply(
            calcular_score_clima,
            axis=1,
        )
    )

    return nuevo

# ==========================================================
# SCORE POR PRECIO
# ==========================================================

def calcular_score_precio(
    fila: pd.Series,
) -> int:
    """
    Calcula la puntuación basada en el rango de precio.

    Máximo:
        20 puntos
    """

    rango = fila.get(
        "rango_precio",
        "",
    )

    if rango == "Económico":
        return 20

    if rango == "Medio":
        return 18

    if rango == "Premium":
        return 13

    if rango == "Lujo":
        return 8

    return 0


def agregar_score_precio(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:

    nuevo = dataframe.copy()

    nuevo["score_precio"] = (
        nuevo.apply(
            calcular_score_precio,
            axis=1,
        )
    )

    return nuevo

# ==========================================================
# SCORE POR MARCA
# ==========================================================

MARCAS_RECONOCIDAS = {
    "Nike": 15,
    "Adidas": 15,
    "Calvin Klein": 13,
    "HUGO": 13,
    "Tommy Jeans": 12,
    "AllSaints": 12,
    "Mango": 11,
    "Reebok": 11,
    "Jack & Jones": 10,
}


def calcular_score_marca(
    fila: pd.Series,
) -> int:
    """
    Calcula la puntuación comercial de la marca.

    Máximo:
        15 puntos
    """

    marca = fila.get(
        "marca_normalizada",
        "",
    )

    tipo_marca = fila.get(
        "tipo_marca",
        "",
    )

    # Las marcas propias reciben una puntuación alta
    # por su control comercial y diferenciación.
    if tipo_marca == "Propia":
        return 15

    # Las marcas externas reconocidas usan el ranking.
    if marca in MARCAS_RECONOCIDAS:
        return MARCAS_RECONOCIDAS[marca]

    # Resto de marcas externas.
    return 8


def agregar_score_marca(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """Agrega la puntuación de marca."""

    nuevo = dataframe.copy()

    nuevo["score_marca"] = (
        nuevo.apply(
            calcular_score_marca,
            axis=1,
        )
    )

    return nuevo

# ==========================================================
# SCORE DE REPRESENTATIVIDAD DEL CATÁLOGO
# ==========================================================

def agregar_score_popularidad(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calcula la representatividad relativa de cada categoría
    dentro del catálogo.

    Importante:
    Este indicador no representa ventas ni demanda real.
    Solo mide la presencia de la categoría en el catálogo.

    Máximo:
        10 puntos
    """

    nuevo = dataframe.copy()

    columna_categoria = "categoria_normalizada"

    if columna_categoria not in nuevo.columns:
        raise ValueError(
            "No se encontró la columna "
            "'categoria_normalizada'."
        )

    # Como cada producto aparece una vez por ciudad,
    # contamos productos únicos para evitar duplicaciones.
    if "id_unico" in nuevo.columns:
        productos_unicos = (
            nuevo[
                [
                    "id_unico",
                    columna_categoria,
                ]
            ]
            .drop_duplicates(
                subset="id_unico"
            )
        )
    else:
        productos_unicos = (
            nuevo[
                [
                    "nombre",
                    columna_categoria,
                ]
            ]
            .drop_duplicates()
        )

    frecuencia_categorias = (
        productos_unicos[
            columna_categoria
        ]
        .value_counts()
    )

    frecuencia_maxima = (
        frecuencia_categorias.max()
    )

    if pd.isna(frecuencia_maxima) or frecuencia_maxima == 0:
        nuevo["frecuencia_categoria"] = 0
        nuevo["representatividad_categoria"] = 0.0
        nuevo["score_popularidad"] = 0

        return nuevo

    nuevo["frecuencia_categoria"] = (
        nuevo[columna_categoria]
        .map(frecuencia_categorias)
        .fillna(0)
        .astype(int)
    )

    nuevo["representatividad_categoria"] = (
        nuevo["frecuencia_categoria"]
        / frecuencia_maxima
    ).round(4)

    nuevo["score_popularidad"] = (
        nuevo["representatividad_categoria"]
        * 10
    ).round().astype(int)

    return nuevo


# ==========================================================
# SCORE FINAL MODAPREDICT
# ==========================================================

def reescalar_score(
    valor,
    maximo_original: float,
    maximo_nuevo: float,
) -> float:
    """
    Reescala una puntuación desde su máximo original
    hacia un nuevo máximo.
    """

    if pd.isna(valor):
        return 0.0

    if maximo_original <= 0:
        return 0.0

    valor_reescalado = (
        float(valor)
        / maximo_original
        * maximo_nuevo
    )

    return round(
        max(0.0, min(maximo_nuevo, valor_reescalado)),
        2,
    )


def generar_explicacion_score(
    fila: pd.Series,
) -> str:
    """
    Genera una explicación clara del ModaPredict Score.
    """

    explicaciones = []

    # Tendencia
    if fila.get("tiene_datos_trends", 0) == 0:
        explicaciones.append(
            "Sin información suficiente de Google Trends"
        )
    else:
        nivel = fila.get(
            "nivel_tendencia",
            "Sin información",
        )

        crecimiento = fila.get(
            "crecimiento_pct",
            0,
        )

        explicaciones.append(
            f"Nivel de tendencia: {str(nivel).lower()} "
            f"({crecimiento:.1f}% de crecimiento)"
        )

    # Clima
    compatibilidad = fila.get(
        "compatibilidad_clima",
        0.5,
    )

    ciudad = fila.get(
        "ciudad",
        "la ciudad seleccionada",
    )

    if compatibilidad >= 0.7:
        explicaciones.append(
            f"Clima favorable para {ciudad}"
        )
    elif compatibilidad <= 0.3:
        explicaciones.append(
            f"Clima poco favorable para {ciudad}"
        )
    else:
        explicaciones.append(
            f"Compatibilidad climática media para {ciudad}"
        )

    # Precio
    rango_precio = fila.get(
        "rango_precio",
        "Sin precio",
    )

    explicaciones.append(
        f"Precio clasificado como {str(rango_precio).lower()}"
    )

    # Marca
    marca = fila.get(
        "marca_normalizada",
        "Sin marca",
    )

    tipo_marca = fila.get(
        "tipo_marca",
        "Externa",
    )

    if tipo_marca == "Propia":
        explicaciones.append(
            f"{marca} es una marca propia"
        )
    else:
        explicaciones.append(
            f"{marca} es una marca externa"
        )

    # Representatividad
    frecuencia = fila.get(
        "frecuencia_categoria",
        0,
    )

    categoria = fila.get(
        "categoria_normalizada",
        "sin categoría",
    )

    explicaciones.append(
        f"La categoría {categoria} tiene "
        f"{int(frecuencia)} productos en el catálogo"
    )

    return ". ".join(explicaciones) + "."


def agregar_modapredict_score(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Reescala los componentes y calcula el score final
    entre 0 y 100.
    """

    nuevo = dataframe.copy()

    columnas_requeridas = [
        "score_trends",
        "score_clima",
        "score_precio",
        "score_marca",
        "score_popularidad",
    ]

    faltantes = [
        columna
        for columna in columnas_requeridas
        if columna not in nuevo.columns
    ]

    if faltantes:
        raise ValueError(
            "Faltan componentes del score: "
            + ", ".join(faltantes)
        )

    # Reescalado según la estructura acordada.
    nuevo["score_tendencia_30"] = (
        nuevo["score_trends"]
        .apply(
            lambda valor: reescalar_score(
                valor,
                maximo_original=40,
                maximo_nuevo=30,
            )
        )
    )

    nuevo["score_clima_25"] = (
        nuevo["score_clima"]
        .apply(
            lambda valor: reescalar_score(
                valor,
                maximo_original=30,
                maximo_nuevo=25,
            )
        )
    )

    nuevo["score_precio_20"] = pd.to_numeric(
        nuevo["score_precio"],
        errors="coerce",
    ).fillna(0).clip(0, 20)

    nuevo["score_marca_15"] = pd.to_numeric(
        nuevo["score_marca"],
        errors="coerce",
    ).fillna(0).clip(0, 15)

    nuevo["score_popularidad_10"] = pd.to_numeric(
        nuevo["score_popularidad"],
        errors="coerce",
    ).fillna(0).clip(0, 10)

    nuevo["modapredict_score"] = (
        nuevo["score_tendencia_30"]
        + nuevo["score_clima_25"]
        + nuevo["score_precio_20"]
        + nuevo["score_marca_15"]
        + nuevo["score_popularidad_10"]
    ).round(2)

    nuevo["nivel_recomendacion"] = pd.cut(
        nuevo["modapredict_score"],
        bins=[
            -0.01,
            39.99,
            59.99,
            79.99,
            100,
        ],
        labels=[
            "Baja",
            "Moderada",
            "Alta",
            "Muy alta",
        ],
    ).astype(str)

    nuevo["explicacion_score"] = (
        nuevo.apply(
            generar_explicacion_score,
            axis=1,
        )
    )

    return nuevo