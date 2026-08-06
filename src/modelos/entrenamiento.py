from __future__ import annotations

from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import (
    HistGradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler,
)


# ==========================================================
# PREPROCESAMIENTO
# ==========================================================

def construir_preprocesador(
    columnas_numericas: list[str],
    columnas_categoricas: list[str],
    salida_densa: bool = False,
) -> ColumnTransformer:
    """
    Construye el preprocesador común.

    salida_densa=False:
        Genera una matriz dispersa, útil para regresión
        lineal, Dummy y Random Forest.

    salida_densa=True:
        Genera una matriz densa, necesaria para
        HistGradientBoosting.
    """

    pipeline_numerico = Pipeline(
        steps=[
            (
                "imputacion",
                SimpleImputer(
                    strategy="median",
                ),
            ),
            (
                "escalado",
                StandardScaler(),
            ),
        ]
    )

    pipeline_categorico = Pipeline(
        steps=[
            (
                "imputacion",
                SimpleImputer(
                    strategy="most_frequent",
                ),
            ),
            (
                "onehot",
                OneHotEncoder(
                    handle_unknown="ignore",
                    sparse_output=not salida_densa,
                ),
            ),
        ]
    )

    preprocesador = ColumnTransformer(
        transformers=[
            (
                "numericas",
                pipeline_numerico,
                columnas_numericas,
            ),
            (
                "categoricas",
                pipeline_categorico,
                columnas_categoricas,
            ),
        ],
        remainder="drop",
        sparse_threshold=0.0 if salida_densa else 0.3,
    )

    return preprocesador


# ==========================================================
# MODELOS
# ==========================================================

def construir_modelos(
    columnas_numericas: list[str],
    columnas_categoricas: list[str],
) -> dict[str, Pipeline]:
    """
    Construye los modelos que se compararán.

    Modelos:
        1. Dummy Regressor
        2. Regresión Lineal
        3. Random Forest
        4. HistGradientBoosting
    """

    preprocesador_disperso = construir_preprocesador(
        columnas_numericas=columnas_numericas,
        columnas_categoricas=columnas_categoricas,
        salida_densa=False,
    )

    preprocesador_denso = construir_preprocesador(
        columnas_numericas=columnas_numericas,
        columnas_categoricas=columnas_categoricas,
        salida_densa=True,
    )

    modelos = {
        "Dummy Regressor": Pipeline(
            steps=[
                (
                    "preprocesador",
                    preprocesador_disperso,
                ),
                (
                    "modelo",
                    DummyRegressor(
                        strategy="mean",
                    ),
                ),
            ]
        ),

        "Regresión Lineal": Pipeline(
            steps=[
                (
                    "preprocesador",
                    preprocesador_disperso,
                ),
                (
                    "modelo",
                    LinearRegression(),
                ),
            ]
        ),

        "Random Forest": Pipeline(
            steps=[
                (
                    "preprocesador",
                    preprocesador_disperso,
                ),
                (
                    "modelo",
                    RandomForestRegressor(
                        n_estimators=300,
                        max_depth=None,
                        min_samples_split=2,
                        min_samples_leaf=2,
                        max_features="sqrt",
                        random_state=42,
                        n_jobs=-1,
                    ),
                ),
            ]
        ),

        "HistGradientBoosting": Pipeline(
            steps=[
                (
                    "preprocesador",
                    preprocesador_denso,
                ),
                (
                    "modelo",
                    HistGradientBoostingRegressor(
                        learning_rate=0.05,
                        max_iter=250,
                        max_leaf_nodes=31,
                        min_samples_leaf=20,
                        l2_regularization=0.1,
                        early_stopping=True,
                        random_state=42,
                    ),
                ),
            ]
        ),
    }

    return modelos