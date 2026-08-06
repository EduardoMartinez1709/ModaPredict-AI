from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.model_selection import GroupKFold

from src.modelos.entrenamiento import construir_modelos
from src.modelos.preparacion import (
    cargar_dataset_scoring,
    identificar_tipos_columnas,
    seleccionar_variables,
)


NUMERO_FOLDS = 5
EXPERIMENTO_PRINCIPAL = "B"
MODELO_PRINCIPAL = "HistGradientBoosting"


def preparar_datos_validacion() -> dict:
    """
    Prepara X, y y grupos utilizando las reglas
    del Experimento B.
    """

    dataframe = cargar_dataset_scoring()

    X, y, grupos = seleccionar_variables(
        dataframe=dataframe,
        experimento=EXPERIMENTO_PRINCIPAL,
    )

    (
        columnas_numericas,
        columnas_categoricas,
    ) = identificar_tipos_columnas(X)

    return {
        "X": X,
        "y": y,
        "grupos": grupos,
        "columnas_numericas": columnas_numericas,
        "columnas_categoricas": columnas_categoricas,
    }


def calcular_metricas_fold(
    y_real: pd.Series,
    y_predicha,
) -> dict[str, float]:
    """
    Calcula MAE, RMSE y R² para un fold.
    """

    errores = (
        y_real.to_numpy()
        - np.asarray(y_predicha)
    )

    mae = np.mean(
        np.abs(errores)
    )

    rmse = np.sqrt(
        np.mean(
            errores ** 2
        )
    )

    suma_residuos = np.sum(
        errores ** 2
    )

    suma_total = np.sum(
        (
            y_real.to_numpy()
            - y_real.mean()
        ) ** 2
    )

    if suma_total == 0:
        r2 = 0.0
    else:
        r2 = 1 - (
            suma_residuos
            / suma_total
        )

    return {
        "MAE": float(mae),
        "RMSE": float(rmse),
        "R2": float(r2),
    }


def ejecutar_validacion_cruzada(
    numero_folds: int = NUMERO_FOLDS,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Ejecuta GroupKFold con HistGradientBoosting.

    Todos los escenarios de un mismo producto permanecen
    juntos en entrenamiento o validación.
    """

    datos = preparar_datos_validacion()

    X = datos["X"]
    y = datos["y"]
    grupos = datos["grupos"]

    modelos = construir_modelos(
        columnas_numericas=datos[
            "columnas_numericas"
        ],
        columnas_categoricas=datos[
            "columnas_categoricas"
        ],
    )

    modelo = modelos[
        MODELO_PRINCIPAL
    ]

    divisor = GroupKFold(
        n_splits=numero_folds
    )

    resultados = []

    print(
        "\n========== VALIDACIÓN CRUZADA AGRUPADA ==========\n"
    )

    print(
        f"Experimento: {EXPERIMENTO_PRINCIPAL}"
    )
    print(
        f"Modelo: {MODELO_PRINCIPAL}"
    )
    print(
        f"Número de folds: {numero_folds}"
    )
    print(
        f"Productos únicos: {grupos.nunique()}"
    )

    for numero_fold, (
        indices_train,
        indices_validacion,
    ) in enumerate(
        divisor.split(
            X,
            y,
            groups=grupos,
        ),
        start=1,
    ):
        X_train = X.iloc[
            indices_train
        ].copy()

        X_validacion = X.iloc[
            indices_validacion
        ].copy()

        y_train = y.iloc[
            indices_train
        ].copy()

        y_validacion = y.iloc[
            indices_validacion
        ].copy()

        grupos_train = grupos.iloc[
            indices_train
        ]

        grupos_validacion = grupos.iloc[
            indices_validacion
        ]

        productos_compartidos = set(
            grupos_train.unique()
        ).intersection(
            set(
                grupos_validacion.unique()
            )
        )

        if productos_compartidos:
            raise ValueError(
                f"Se detectó fuga de productos "
                f"en el fold {numero_fold}."
            )

        print(
            f"\nEntrenando fold "
            f"{numero_fold}/{numero_folds}..."
        )

        modelo.fit(
            X_train,
            y_train,
        )

        predicciones = modelo.predict(
            X_validacion
        )

        metricas = calcular_metricas_fold(
            y_real=y_validacion,
            y_predicha=predicciones,
        )

        resultados.append(
            {
                "fold": numero_fold,
                "registros_train": len(
                    X_train
                ),
                "registros_validacion": len(
                    X_validacion
                ),
                "productos_train": (
                    grupos_train.nunique()
                ),
                "productos_validacion": (
                    grupos_validacion.nunique()
                ),
                "productos_compartidos": len(
                    productos_compartidos
                ),
                "MAE": round(
                    metricas["MAE"],
                    4,
                ),
                "RMSE": round(
                    metricas["RMSE"],
                    4,
                ),
                "R2": round(
                    metricas["R2"],
                    4,
                ),
            }
        )

        print(
            f"MAE: {metricas['MAE']:.4f}"
        )
        print(
            f"RMSE: {metricas['RMSE']:.4f}"
        )
        print(
            f"R²: {metricas['R2']:.4f}"
        )

    resultados_folds = pd.DataFrame(
        resultados
    )

    resumen = pd.DataFrame(
        {
            "metrica": [
                "MAE",
                "RMSE",
                "R2",
            ],
            "promedio": [
                resultados_folds[
                    "MAE"
                ].mean(),
                resultados_folds[
                    "RMSE"
                ].mean(),
                resultados_folds[
                    "R2"
                ].mean(),
            ],
            "desviacion_estandar": [
                resultados_folds[
                    "MAE"
                ].std(),
                resultados_folds[
                    "RMSE"
                ].std(),
                resultados_folds[
                    "R2"
                ].std(),
            ],
            "minimo": [
                resultados_folds[
                    "MAE"
                ].min(),
                resultados_folds[
                    "RMSE"
                ].min(),
                resultados_folds[
                    "R2"
                ].min(),
            ],
            "maximo": [
                resultados_folds[
                    "MAE"
                ].max(),
                resultados_folds[
                    "RMSE"
                ].max(),
                resultados_folds[
                    "R2"
                ].max(),
            ],
        }
    )

    columnas_numericas = [
        "promedio",
        "desviacion_estandar",
        "minimo",
        "maximo",
    ]

    resumen[columnas_numericas] = (
        resumen[columnas_numericas]
        .round(4)
    )

    return resultados_folds, resumen


def generar_reporte_validacion(
    resultados_folds: pd.DataFrame,
    resumen: pd.DataFrame,
) -> None:
    """
    Muestra los resultados individuales y el resumen.
    """

    print(
        "\n========== RESULTADOS POR FOLD ==========\n"
    )

    print(
        resultados_folds.to_string(
            index=False
        )
    )

    print(
        "\n========== RESUMEN DE VALIDACIÓN ==========\n"
    )

    print(
        resumen.to_string(
            index=False
        )
    )

    print(
        "\nProductos compartidos en todos los folds:"
    )

    print(
        resultados_folds[
            "productos_compartidos"
        ].sum()
    )

    print(
        "\n=========================================="
    )