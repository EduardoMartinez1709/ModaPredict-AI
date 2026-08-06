from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)


def calcular_metricas(
    y_real: pd.Series,
    y_predicha,
) -> dict[str, float]:
    """
    Calcula las métricas principales de regresión.
    """

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
        "MAE": round(float(mae), 4),
        "RMSE": round(float(rmse), 4),
        "R2": round(float(r2), 4),
    }


def entrenar_y_evaluar_modelos(
    modelos: dict,
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> tuple[pd.DataFrame, dict, dict]:
    """
    Entrena cada pipeline y evalúa su desempeño
    sobre el conjunto de prueba.
    """

    resultados = []
    modelos_entrenados = {}
    predicciones = {}

    for nombre, pipeline in modelos.items():
        print(
            f"\nEntrenando: {nombre}..."
        )

        pipeline.fit(
            X_train,
            y_train,
        )

        y_predicha = pipeline.predict(
            X_test
        )

        metricas = calcular_metricas(
            y_real=y_test,
            y_predicha=y_predicha,
        )

        resultados.append(
            {
                "modelo": nombre,
                **metricas,
            }
        )

        modelos_entrenados[nombre] = pipeline
        predicciones[nombre] = y_predicha

        print(
            f"MAE: {metricas['MAE']}"
        )
        print(
            f"RMSE: {metricas['RMSE']}"
        )
        print(
            f"R²: {metricas['R2']}"
        )

    tabla_resultados = pd.DataFrame(
        resultados
    ).sort_values(
        by="MAE",
        ascending=True,
    )

    return (
        tabla_resultados,
        modelos_entrenados,
        predicciones,
    )


def construir_tabla_predicciones(
    y_test: pd.Series,
    predicciones: dict,
    grupos_test: pd.Series,
) -> pd.DataFrame:
    """
    Construye una tabla con valores reales, predicciones
    y errores de cada modelo.
    """

    tabla = pd.DataFrame(
        {
            "id_unico": grupos_test.reset_index(
                drop=True
            ),
            "valor_real": y_test.reset_index(
                drop=True
            ),
        }
    )

    for nombre, valores in predicciones.items():
        nombre_columna = (
            nombre.lower()
            .replace(" ", "_")
            .replace("ó", "o")
            .replace("í", "i")
        )

        tabla[
            f"prediccion_{nombre_columna}"
        ] = valores

        tabla[
            f"error_{nombre_columna}"
        ] = (
            tabla["valor_real"]
            - tabla[
                f"prediccion_{nombre_columna}"
            ]
        ).abs()

    return tabla