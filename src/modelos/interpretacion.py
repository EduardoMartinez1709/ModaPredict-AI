from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.inspection import permutation_importance
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

from src.modelos.entrenamiento import construir_modelos
from src.modelos.preparacion import (
    preparar_datos_experimento,
)


MODELO_PRINCIPAL = "HistGradientBoosting"
EXPERIMENTO_PRINCIPAL = "B"


def entrenar_modelo_ganador() -> dict:
    """
    Prepara el Experimento B y entrena HistGradientBoosting
    con la partición agrupada de entrenamiento y prueba.
    """

    datos = preparar_datos_experimento(
        experimento=EXPERIMENTO_PRINCIPAL
    )

    modelos = construir_modelos(
        columnas_numericas=datos[
            "columnas_numericas"
        ],
        columnas_categoricas=datos[
            "columnas_categoricas"
        ],
    )

    modelo = modelos[MODELO_PRINCIPAL]

    print(
        "\nEntrenando el modelo ganador "
        "para interpretación..."
    )

    modelo.fit(
        datos["X_train"],
        datos["y_train"],
    )

    predicciones_train = modelo.predict(
        datos["X_train"]
    )

    predicciones_test = modelo.predict(
        datos["X_test"]
    )

    return {
        "modelo": modelo,
        "datos": datos,
        "predicciones_train": predicciones_train,
        "predicciones_test": predicciones_test,
    }


def calcular_metricas_conjunto(
    y_real: pd.Series,
    y_predicha,
    conjunto: str,
) -> dict:
    """Calcula métricas para train o test."""

    mae = mean_absolute_error(
        y_real,
        y_predicha,
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_real,
            y_predicha,
        )
    )

    r2 = r2_score(
        y_real,
        y_predicha,
    )

    return {
        "conjunto": conjunto,
        "MAE": round(float(mae), 4),
        "RMSE": round(float(rmse), 4),
        "R2": round(float(r2), 4),
    }


def comparar_train_test(
    resultado_entrenamiento: dict,
) -> pd.DataFrame:
    """
    Compara el desempeño de entrenamiento y prueba
    para revisar posible sobreajuste.
    """

    datos = resultado_entrenamiento["datos"]

    metricas_train = calcular_metricas_conjunto(
        y_real=datos["y_train"],
        y_predicha=resultado_entrenamiento[
            "predicciones_train"
        ],
        conjunto="Entrenamiento",
    )

    metricas_test = calcular_metricas_conjunto(
        y_real=datos["y_test"],
        y_predicha=resultado_entrenamiento[
            "predicciones_test"
        ],
        conjunto="Prueba",
    )

    return pd.DataFrame(
        [
            metricas_train,
            metricas_test,
        ]
    )


def construir_analisis_errores(
    resultado_entrenamiento: dict,
) -> pd.DataFrame:
    """
    Construye una tabla detallada de errores en test,
    incluyendo información del producto y del contexto.
    """

    datos = resultado_entrenamiento["datos"]
    dataframe_completo = datos["dataframe_completo"]

    indices_test = datos["X_test"].index

    columnas_contexto = [
        "id_unico",
        "nombre",
        "fuente",
        "marca_normalizada",
        "categoria_normalizada",
        "categoria_general",
        "rango_precio",
        "ciudad",
        "temperatura_media",
        "nivel_tendencia",
        "modapredict_score",
    ]

    columnas_existentes = [
        columna
        for columna in columnas_contexto
        if columna in dataframe_completo.columns
    ]

    errores = (
        dataframe_completo.loc[
            indices_test,
            columnas_existentes,
        ]
        .copy()
        .reset_index(drop=True)
    )

    errores["valor_real"] = (
        datos["y_test"]
        .reset_index(drop=True)
    )

    errores["valor_predicho"] = (
        resultado_entrenamiento[
            "predicciones_test"
        ]
    )

    errores["error"] = (
        errores["valor_real"]
        - errores["valor_predicho"]
    )

    errores["error_absoluto"] = (
        errores["error"].abs()
    )

    errores["tipo_error"] = np.where(
        errores["error"] > 0,
        "Subestimación",
        np.where(
            errores["error"] < 0,
            "Sobreestimación",
            "Exacto",
        ),
    )

    return errores.sort_values(
        by="error_absoluto",
        ascending=False,
    )


def resumir_errores_por_variable(
    errores: pd.DataFrame,
    columna: str,
) -> pd.DataFrame:
    """
    Resume el error absoluto por ciudad, categoría,
    marca u otra variable categórica.
    """

    if columna not in errores.columns:
        return pd.DataFrame()

    resumen = (
        errores.groupby(
            columna,
            dropna=False,
        )
        .agg(
            registros=(
                "error_absoluto",
                "size",
            ),
            mae=(
                "error_absoluto",
                "mean",
            ),
            error_maximo=(
                "error_absoluto",
                "max",
            ),
            error_mediano=(
                "error_absoluto",
                "median",
            ),
        )
        .reset_index()
        .sort_values(
            by="mae",
            ascending=False,
        )
    )

    resumen[
        [
            "mae",
            "error_maximo",
            "error_mediano",
        ]
    ] = resumen[
        [
            "mae",
            "error_maximo",
            "error_mediano",
        ]
    ].round(4)

    return resumen


def calcular_importancia_permutacion(
    resultado_entrenamiento: dict,
    repeticiones: int = 10,
) -> pd.DataFrame:
    """
    Calcula la importancia de cada variable original.

    Una variable es importante cuando, al desordenar sus
    valores, el desempeño del modelo empeora notablemente.
    """

    modelo = resultado_entrenamiento["modelo"]
    datos = resultado_entrenamiento["datos"]

    print(
        "\nCalculando importancia por permutación..."
    )

    resultado = permutation_importance(
        estimator=modelo,
        X=datos["X_test"],
        y=datos["y_test"],
        scoring="neg_mean_absolute_error",
        n_repeats=repeticiones,
        random_state=42,
        n_jobs=-1,
    )

    importancia = pd.DataFrame(
        {
            "variable": datos[
                "X_test"
            ].columns,
            "importancia_promedio": (
                resultado.importances_mean
            ),
            "desviacion_estandar": (
                resultado.importances_std
            ),
        }
    )

    importancia[
        "importancia_promedio"
    ] = importancia[
        "importancia_promedio"
    ].round(6)

    importancia[
        "desviacion_estandar"
    ] = importancia[
        "desviacion_estandar"
    ].round(6)

    return importancia.sort_values(
        by="importancia_promedio",
        ascending=False,
    )


def generar_reporte_interpretacion(
    metricas: pd.DataFrame,
    errores: pd.DataFrame,
    importancia: pd.DataFrame,
) -> None:
    """Muestra el diagnóstico principal en terminal."""

    print(
        "\n========== TRAIN VS. TEST ==========\n"
    )

    print(
        metricas.to_string(index=False)
    )

    print(
        "\n========== MAYORES ERRORES ==========\n"
    )

    columnas_mostrar = [
        columna
        for columna in [
            "nombre",
            "ciudad",
            "categoria_normalizada",
            "valor_real",
            "valor_predicho",
            "error_absoluto",
            "tipo_error",
        ]
        if columna in errores.columns
    ]

    print(
        errores[
            columnas_mostrar
        ].head(20).to_string(
            index=False
        )
    )

    print(
        "\n========== VARIABLES MÁS IMPORTANTES ==========\n"
    )

    print(
        importancia.head(20).to_string(
            index=False
        )
    )

    print(
        "\n==============================================="
    )