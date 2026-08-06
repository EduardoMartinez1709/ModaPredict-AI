from pathlib import Path

import pandas as pd
from sklearn.model_selection import GroupShuffleSplit


# ==========================================================
# COLUMNAS DEL EXPERIMENTO
# ==========================================================

VARIABLE_OBJETIVO = "modapredict_score"
COLUMNA_GRUPO = "id_unico"


COLUMNAS_EXCLUIDAS = [
    # Objetivo y salidas derivadas.
    "modapredict_score",
    "nivel_recomendacion",
    "explicacion_score",

    # Componentes directos del score.
    "score_trends",
    "score_clima",
    "score_precio",
    "score_marca",
    "score_popularidad",
    "score_tendencia_30",
    "score_clima_25",
    "score_precio_20",
    "score_marca_15",
    "score_popularidad_10",

    # Identificadores.
    "id_producto",
    "id_unico",

    # Texto libre y URLs.
    "nombre",
    "url_producto",
    "url_imagen",

    # Columnas originales conservadas como respaldo.
    "marca_original",
    "color_original",
    "categoria_original",

    # Posibles columnas redundantes o no útiles
    # para este primer experimento.
    "tallas_disponibles",
]

COLUMNAS_DERIVADAS_REGLAS = [
    # Variables de tendencia ya transformadas.
    "nivel_tendencia",
    "trend_alto",
    "trend_medio",
    "trend_bajo",
    "trend_subiendo",
    "trend_bajando",
    "trend_estable",

    # Variables climáticas creadas por reglas.
    "compatibilidad_clima",
    "clima_favorable",
    "clima_desfavorable",

    # Variables comerciales derivadas.
    "rango_precio",
    "precio_normalizado",
    "precio_economico",
    "precio_medio",
    "precio_premium",
    "precio_lujo",

    # Variables de marca derivadas.
    "tipo_marca",
    "marca_propia",
    "marca_externa",

    # Representatividad construida desde el catálogo.
    "frecuencia_categoria",
    "representatividad_categoria",

    # Variables binarias climáticas derivadas.
    "clima_frio",
    "clima_templado",
    "clima_caluroso",
    "riesgo_lluvia",
    "viento_fuerte",

    # Refinamiento de redundancias.
    "marca",
    "categoria",
    "latitud",
    "longitud",
]



def cargar_dataset_scoring(
    ruta_proyecto: Path | None = None,
) -> pd.DataFrame:
    """
    Carga el dataset final generado por el motor de scoring.
    """

    if ruta_proyecto is None:
        ruta_proyecto = Path(__file__).resolve().parents[2]

    ruta_archivo = (
        ruta_proyecto
        / "datos"
        / "catalogo_scoring.csv"
    )

    if not ruta_archivo.exists():
        raise FileNotFoundError(
            "No se encontró datos/catalogo_scoring.csv. "
            "Ejecuta primero generar_scoring.py"
        )

    dataframe = pd.read_csv(ruta_archivo)

    return dataframe


def validar_dataset(
    dataframe: pd.DataFrame,
) -> None:
    """
    Comprueba que existan las columnas esenciales.
    """

    columnas_requeridas = [
        VARIABLE_OBJETIVO,
        COLUMNA_GRUPO,
    ]

    faltantes = [
        columna
        for columna in columnas_requeridas
        if columna not in dataframe.columns
    ]

    if faltantes:
        raise ValueError(
            "Faltan columnas esenciales: "
            + ", ".join(faltantes)
        )

    if dataframe[VARIABLE_OBJETIVO].isna().any():
        raise ValueError(
            "La variable objetivo contiene valores nulos."
        )

    if dataframe[COLUMNA_GRUPO].isna().any():
        raise ValueError(
            "La columna id_unico contiene valores nulos."
        )


def seleccionar_variables(
    dataframe: pd.DataFrame,
    experimento: str = "A",
) -> tuple[
    pd.DataFrame,
    pd.Series,
    pd.Series,
]:
    """
    Construye X, y y grupos.

    Experimento A:
        Conserva las variables derivadas del sistema experto.

    Experimento B:
        Excluye variables que reconstruyen directamente
        las reglas del ModaPredict Score.
    """

    validar_dataset(dataframe)

    columnas_excluir = list(
        COLUMNAS_EXCLUIDAS
    )

    if experimento.upper() == "B":
        columnas_excluir.extend(
            COLUMNAS_DERIVADAS_REGLAS
        )

    columnas_disponibles = [
        columna
        for columna in dataframe.columns
        if columna not in columnas_excluir
    ]

    if VARIABLE_OBJETIVO in columnas_disponibles:
        columnas_disponibles.remove(
            VARIABLE_OBJETIVO
        )

    if COLUMNA_GRUPO in columnas_disponibles:
        columnas_disponibles.remove(
            COLUMNA_GRUPO
        )

    X = dataframe[
        columnas_disponibles
    ].copy()

    y = pd.to_numeric(
        dataframe[VARIABLE_OBJETIVO],
        errors="coerce",
    )

    grupos = dataframe[
        COLUMNA_GRUPO
    ].astype(str)

    return X, y, grupos


def identificar_tipos_columnas(
    X: pd.DataFrame,
) -> tuple[list[str], list[str]]:
    """
    Separa columnas numéricas y categóricas.
    """

    columnas_numericas = (
        X.select_dtypes(
            include=[
                "number",
                "bool",
            ]
        )
        .columns
        .tolist()
    )

    columnas_categoricas = [
        columna
        for columna in X.columns
        if columna not in columnas_numericas
    ]

    return (
        columnas_numericas,
        columnas_categoricas,
    )


def dividir_train_test_por_producto(
    X: pd.DataFrame,
    y: pd.Series,
    grupos: pd.Series,
    test_size: float = 0.20,
    random_state: int = 42,
) -> dict:
    """
    Divide entrenamiento y prueba sin mezclar escenarios
    del mismo producto entre ambos conjuntos.
    """

    divisor = GroupShuffleSplit(
        n_splits=1,
        test_size=test_size,
        random_state=random_state,
    )

    indices_train, indices_test = next(
        divisor.split(
            X,
            y,
            groups=grupos,
        )
    )

    X_train = X.iloc[
        indices_train
    ].copy()

    X_test = X.iloc[
        indices_test
    ].copy()

    y_train = y.iloc[
        indices_train
    ].copy()

    y_test = y.iloc[
        indices_test
    ].copy()

    grupos_train = grupos.iloc[
        indices_train
    ].copy()

    grupos_test = grupos.iloc[
        indices_test
    ].copy()

    return {
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
        "grupos_train": grupos_train,
        "grupos_test": grupos_test,
    }


def preparar_datos_experimento(
    experimento: str = "A",
) -> dict:
    """
    Prepara los datos del Experimento A o B.
    """

    experimento = experimento.upper()

    if experimento not in {"A", "B"}:
        raise ValueError(
            "El experimento debe ser 'A' o 'B'."
        )

    dataframe = cargar_dataset_scoring()

    X, y, grupos = seleccionar_variables(
        dataframe=dataframe,
        experimento=experimento,
    )

    (
        columnas_numericas,
        columnas_categoricas,
    ) = identificar_tipos_columnas(X)

    particion = dividir_train_test_por_producto(
        X=X,
        y=y,
        grupos=grupos,
    )

    particion["columnas_numericas"] = (
        columnas_numericas
    )

    particion["columnas_categoricas"] = (
        columnas_categoricas
    )

    particion["dataframe_completo"] = dataframe
    particion["experimento"] = experimento

    return particion


def generar_reporte_preparacion(
    datos: dict,
) -> None:
    """
    Muestra un diagnóstico de la separación de datos
    para el experimento A o B.
    """

    X_train = datos["X_train"]
    X_test = datos["X_test"]
    grupos_train = datos["grupos_train"]
    grupos_test = datos["grupos_test"]

    productos_train = set(
        grupos_train.unique()
    )

    productos_test = set(
        grupos_test.unique()
    )

    productos_compartidos = (
        productos_train.intersection(
            productos_test
        )
    )

    experimento = datos.get(
        "experimento",
        "A",
    )

    print(
        "\n========== PREPARACIÓN DEL EXPERIMENTO ==========\n"
    )

    print(
        f"Experimento: {experimento}"
    )

    print(
        f"\nRegistros de entrenamiento: "
        f"{len(X_train)}"
    )

    print(
        f"Registros de prueba: "
        f"{len(X_test)}"
    )

    print(
        f"Productos únicos en entrenamiento: "
        f"{len(productos_train)}"
    )

    print(
        f"Productos únicos en prueba: "
        f"{len(productos_test)}"
    )

    print(
        f"Productos compartidos entre train y test: "
        f"{len(productos_compartidos)}"
    )

    print(
        f"\nVariables numéricas: "
        f"{len(datos['columnas_numericas'])}"
    )

    print(
        f"Variables categóricas: "
        f"{len(datos['columnas_categoricas'])}"
    )

    print(
        f"Total de variables predictoras: "
        f"{X_train.shape[1]}"
    )

    print(
        "\nDistribución de la variable objetivo "
        "en entrenamiento:"
    )

    print(
        datos["y_train"].describe()
    )

    print(
        "\nDistribución de la variable objetivo "
        "en prueba:"
    )

    print(
        datos["y_test"].describe()
    )

    print(
        "\n================================================"
    )