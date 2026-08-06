import numpy as np
import pandas as pd


# ==========================================================
# VARIABLES TEMPORALES
# ==========================================================

def obtener_estacion(mes: int) -> str:
    """
    Asigna una estación meteorológica de referencia
    para el hemisferio norte.
    """

    if mes in [3, 4, 5]:
        return "Primavera"

    if mes in [6, 7, 8]:
        return "Verano"

    if mes in [9, 10, 11]:
        return "Otoño"

    return "Invierno"


def agregar_variables_temporales(
    catalogo: pd.DataFrame,
    fecha_referencia,
) -> pd.DataFrame:
    """Crea variables relacionadas con fecha y temporada."""

    dataframe = catalogo.copy()

    fecha = pd.to_datetime(
        fecha_referencia,
        errors="coerce",
    )

    if pd.isna(fecha):
        raise ValueError(
            "No fue posible convertir la fecha de referencia."
        )

    dataframe["fecha_referencia"] = fecha
    dataframe["anio"] = fecha.year
    dataframe["mes"] = fecha.month
    dataframe["numero_semana"] = int(
        fecha.isocalendar().week
    )
    dataframe["trimestre"] = (
        (fecha.month - 1) // 3 + 1
    )
    dataframe["estacion"] = obtener_estacion(
        fecha.month
    )

    # Referencia general para el centro de México.
    dataframe["temporada_lluvias"] = (
        fecha.month in [5, 6, 7, 8, 9, 10]
    )

    dataframe["temporada_fria"] = (
        fecha.month in [11, 12, 1, 2]
    )

    dataframe["temporada_calor"] = (
        fecha.month in [3, 4, 5, 6]
    )

    return dataframe


# ==========================================================
# VARIABLES DE TENDENCIA
# ==========================================================

def clasificar_nivel_tendencia(
    interes_reciente,
) -> str:
    """Clasifica el interés de Google Trends."""

    if pd.isna(interes_reciente):
        return "Sin información"

    if interes_reciente >= 60:
        return "Alto"

    if interes_reciente >= 30:
        return "Medio"

    return "Bajo"


def agregar_variables_tendencia(
    catalogo: pd.DataFrame,
) -> pd.DataFrame:
    """
    Crea indicadores derivados de Google Trends.

    Conserva una señal que indica si existían datos reales
    antes de reemplazar los valores nulos por cero.
    """

    dataframe = catalogo.copy()

    columnas_numericas = [
        "interes_promedio",
        "interes_reciente",
        "crecimiento_pct",
    ]

    # Convertir las columnas de Trends a números.
    for columna in columnas_numericas:
        if columna not in dataframe.columns:
            dataframe[columna] = np.nan

        dataframe[columna] = pd.to_numeric(
            dataframe[columna],
            errors="coerce",
        )

    # IMPORTANTE:
    # Registrar primero si el producto realmente tenía datos
    # de Google Trends, antes de reemplazar los NaN.
    dataframe["tiene_datos_trends"] = (
        dataframe["interes_reciente"]
        .notna()
    ).astype(int)

    # Clasificar el nivel antes de rellenar los valores nulos.
    dataframe["nivel_tendencia"] = (
        dataframe["interes_reciente"]
        .apply(clasificar_nivel_tendencia)
    )

    # Reemplazar valores numéricos faltantes por cero.
    dataframe[columnas_numericas] = (
        dataframe[columnas_numericas]
        .fillna(0)
    )

    # Si existe la columna textual original, completar sus nulos.
    if "tendencia" in dataframe.columns:
        dataframe["tendencia"] = (
            dataframe["tendencia"]
            .fillna("Sin información")
        )

    dataframe["trend_alto"] = (
        dataframe["nivel_tendencia"]
        .eq("Alto")
    ).astype(int)

    dataframe["trend_medio"] = (
        dataframe["nivel_tendencia"]
        .eq("Medio")
    ).astype(int)

    dataframe["trend_bajo"] = (
        dataframe["nivel_tendencia"]
        .eq("Bajo")
    ).astype(int)

    dataframe["trend_subiendo"] = (
        (
            dataframe["tiene_datos_trends"].eq(1)
        )
        & (
            dataframe["crecimiento_pct"].ge(10)
        )
    ).astype(int)

    dataframe["trend_bajando"] = (
        (
            dataframe["tiene_datos_trends"].eq(1)
        )
        & (
            dataframe["crecimiento_pct"].le(-10)
        )
    ).astype(int)

    dataframe["trend_estable"] = (
        (
            dataframe["tiene_datos_trends"].eq(1)
        )
        & (
            dataframe["crecimiento_pct"]
            .between(
                -10,
                10,
                inclusive="neither",
            )
        )
    ).astype(int)

    return dataframe

# ==========================================================
# VARIABLES COMERCIALES
# ==========================================================

def agregar_variables_comerciales(
    catalogo: pd.DataFrame,
) -> pd.DataFrame:
    """Genera indicadores de precio y tipo de marca."""

    dataframe = catalogo.copy()

    dataframe["precio_actual"] = pd.to_numeric(
        dataframe["precio_actual"],
        errors="coerce",
    )

    precio_minimo = dataframe[
        "precio_actual"
    ].min()

    precio_maximo = dataframe[
        "precio_actual"
    ].max()

    diferencia = precio_maximo - precio_minimo

    if diferencia > 0:
        dataframe["precio_normalizado"] = (
            dataframe["precio_actual"]
            - precio_minimo
        ) / diferencia
    else:
        dataframe["precio_normalizado"] = 0.0

    dataframe["marca_propia"] = (
        dataframe["tipo_marca"]
        .eq("Propia")
    ).astype(int)

    dataframe["marca_externa"] = (
        dataframe["tipo_marca"]
        .eq("Externa")
    ).astype(int)

    dataframe["precio_economico"] = (
        dataframe["rango_precio"]
        .eq("Económico")
    ).astype(int)

    dataframe["precio_medio"] = (
        dataframe["rango_precio"]
        .eq("Medio")
    ).astype(int)

    dataframe["precio_premium"] = (
        dataframe["rango_precio"]
        .eq("Premium")
    ).astype(int)

    dataframe["precio_lujo"] = (
        dataframe["rango_precio"]
        .eq("Lujo")
    ).astype(int)

    return dataframe


# ==========================================================
# RESUMEN DEL CLIMA
# ==========================================================

def preparar_resumen_clima(
    clima: pd.DataFrame,
    dias_analisis: int = 7,
) -> pd.DataFrame:
    """
    Resume los próximos días de clima para cada ciudad.
    """

    dataframe = clima.copy()

    dataframe["fecha"] = pd.to_datetime(
        dataframe["fecha"],
        errors="coerce",
    )

    columnas_numericas = [
        "temperatura_max",
        "temperatura_min",
        "precipitacion_mm",
        "lluvia_mm",
        "viento_max_kmh",
    ]

    for columna in columnas_numericas:
        dataframe[columna] = pd.to_numeric(
            dataframe[columna],
            errors="coerce",
        )

    dataframe = dataframe.sort_values(
        ["ciudad", "fecha"]
    )

    dataframe = (
        dataframe.groupby(
            "ciudad",
            group_keys=False,
        )
        .head(dias_analisis)
    )

    resumen = (
        dataframe.groupby(
            [
                "ciudad",
                "estado",
                "latitud",
                "longitud",
            ],
            as_index=False,
        )
        .agg(
            fecha_inicio=("fecha", "min"),
            fecha_fin=("fecha", "max"),
            temperatura_max_promedio=(
                "temperatura_max",
                "mean",
            ),
            temperatura_min_promedio=(
                "temperatura_min",
                "mean",
            ),
            precipitacion_acumulada=(
                "precipitacion_mm",
                "sum",
            ),
            lluvia_acumulada=(
                "lluvia_mm",
                "sum",
            ),
            viento_max_promedio=(
                "viento_max_kmh",
                "mean",
            ),
        )
    )

    resumen["temperatura_media"] = (
        resumen["temperatura_max_promedio"]
        + resumen["temperatura_min_promedio"]
    ) / 2

    resumen["clima_frio"] = (
        resumen["temperatura_media"] < 16
    ).astype(int)

    resumen["clima_templado"] = (
        resumen["temperatura_media"]
        .between(16, 24)
    ).astype(int)

    resumen["clima_caluroso"] = (
        resumen["temperatura_media"] > 24
    ).astype(int)

    resumen["riesgo_lluvia"] = (
        resumen["lluvia_acumulada"] >= 10
    ).astype(int)

    resumen["viento_fuerte"] = (
        resumen["viento_max_promedio"] >= 25
    ).astype(int)

    return resumen


# ==========================================================
# CRUCE CATÁLOGO + CIUDADES
# ==========================================================

def cruzar_catalogo_con_clima(
    catalogo: pd.DataFrame,
    resumen_clima: pd.DataFrame,
) -> pd.DataFrame:
    """
    Crea una versión del catálogo para cada ciudad.

    769 productos x 5 ciudades = 3,845 escenarios.
    """

    catalogo_nuevo = catalogo.copy()
    clima_nuevo = resumen_clima.copy()

    catalogo_nuevo["_clave_cruce"] = 1
    clima_nuevo["_clave_cruce"] = 1

    resultado = catalogo_nuevo.merge(
        clima_nuevo,
        how="inner",
        on="_clave_cruce",
    )

    resultado = resultado.drop(
        columns="_clave_cruce"
    )

    return resultado


# ==========================================================
# COMPATIBILIDAD ENTRE PRODUCTO Y CLIMA
# ==========================================================

# ==========================================================
# COMPATIBILIDAD ENTRE PRODUCTO Y CLIMA
# ==========================================================

PRODUCTOS_FRIO = {
    "sudaderas",
    "chamarras",
    "abrigos",
    "sueteres",
    "jeans",
    "pantalones",
    "pantalones cargo",
    "botas",
}

PRODUCTOS_CALOR = {
    "playeras",
    "camisetas",
    "blusas",
    "camisas",
    "polos",
    "vestidos",
    "shorts",
    "faldas",
    "sandalias",
}

PRODUCTOS_LLUVIA = {
    "chamarras",
    "botas",
}

PRODUCTOS_DESFAVORABLES_FRIO = {
    "sandalias",
    "shorts",
    "vestidos",
}

PRODUCTOS_DESFAVORABLES_CALOR = {
    "abrigos",
    "chamarras",
    "sudaderas",
    "sueteres",
}


def calcular_compatibilidad_clima(
    fila: pd.Series,
) -> float:
    """
    Calcula una compatibilidad climática entre 0 y 1
    usando la categoría específica del producto.
    """

    compatibilidad = 0.5

    categoria = str(
        fila.get("categoria_normalizada", "")
    ).strip().lower()

    if (
        fila.get("clima_frio", 0) == 1
        and categoria in PRODUCTOS_FRIO
    ):
        compatibilidad += 0.3

    if (
        fila.get("clima_caluroso", 0) == 1
        and categoria in PRODUCTOS_CALOR
    ):
        compatibilidad += 0.3

    if (
        fila.get("riesgo_lluvia", 0) == 1
        and categoria in PRODUCTOS_LLUVIA
    ):
        compatibilidad += 0.2

    if (
        fila.get("clima_frio", 0) == 1
        and categoria in PRODUCTOS_DESFAVORABLES_FRIO
    ):
        compatibilidad -= 0.3

    if (
        fila.get("clima_caluroso", 0) == 1
        and categoria in PRODUCTOS_DESFAVORABLES_CALOR
    ):
        compatibilidad -= 0.3

    return round(
        max(0.0, min(1.0, compatibilidad)),
        2,
    )

def agregar_compatibilidad_clima(
    catalogo: pd.DataFrame,
) -> pd.DataFrame:
    """Agrega variables de compatibilidad climática."""

    dataframe = catalogo.copy()

    dataframe["compatibilidad_clima"] = (
        dataframe.apply(
            calcular_compatibilidad_clima,
            axis=1,
        )
    )

    dataframe["clima_favorable"] = (
        dataframe["compatibilidad_clima"]
        .ge(0.7)
    ).astype(int)

    dataframe["clima_desfavorable"] = (
        dataframe["compatibilidad_clima"]
        .le(0.3)
    ).astype(int)

    return dataframe


# ==========================================================
# PIPELINE COMPLETO DE FEATURES
# ==========================================================

def construir_features(
    catalogo: pd.DataFrame,
    clima: pd.DataFrame,
) -> pd.DataFrame:
    """
    Ejecuta todas las transformaciones de esta etapa.
    """

    resumen_clima = preparar_resumen_clima(
        clima=clima,
        dias_analisis=7,
    )

    fecha_referencia = resumen_clima[
        "fecha_inicio"
    ].min()

    dataframe = agregar_variables_temporales(
        catalogo,
        fecha_referencia,
    )

    dataframe = agregar_variables_tendencia(
        dataframe
    )

    dataframe = agregar_variables_comerciales(
        dataframe
    )

    dataframe = cruzar_catalogo_con_clima(
        dataframe,
        resumen_clima,
    )

    dataframe = agregar_compatibilidad_clima(
        dataframe
    )

    return dataframe


# ==========================================================
# REPORTE
# ==========================================================

def generar_reporte_features(
    dataframe: pd.DataFrame,
) -> None:
    """Muestra un diagnóstico del dataset generado."""

    print(
        "\n========== INGENIERÍA DE VARIABLES ==========\n"
    )

    print(f"Escenarios generados: {len(dataframe)}")
    print(f"Columnas totales: {dataframe.shape[1]}")

    print("\nEscenarios por ciudad:")
    print(
        dataframe["ciudad"]
        .value_counts()
    )

    print("\nNiveles de tendencia:")
    print(
        dataframe["nivel_tendencia"]
        .value_counts(dropna=False)
    )

    print("\nCompatibilidad climática:")
    print(
        dataframe["compatibilidad_clima"]
        .describe()
    )

    print("\nProductos con clima favorable:")
    print(
        dataframe["clima_favorable"]
        .sum()
    )

    print("\nTemperatura media por ciudad:")
    print(
        dataframe.groupby("ciudad")[
            "temperatura_media"
        ]
        .first()
        .round(2)
        .sort_values()
    )

    print(
        "\n=============================================="
    )