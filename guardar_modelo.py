from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import joblib

from src.modelos.entrenamiento import construir_modelos
from src.modelos.preparacion import (
    cargar_dataset_scoring,
    identificar_tipos_columnas,
    seleccionar_variables,
)


EXPERIMENTO_FINAL = "B"
MODELO_FINAL = "HistGradientBoosting"


def main() -> None:
    ruta_proyecto = Path(__file__).resolve().parent

    carpeta_modelos = (
        ruta_proyecto
        / "modelos_guardados"
    )

    carpeta_modelos.mkdir(
        parents=True,
        exist_ok=True,
    )

    # ==========================================
    # PREPARAR TODO EL EXPERIMENTO B
    # ==========================================

    dataframe = cargar_dataset_scoring()

    X, y, grupos = seleccionar_variables(
        dataframe=dataframe,
        experimento=EXPERIMENTO_FINAL,
    )

    (
        columnas_numericas,
        columnas_categoricas,
    ) = identificar_tipos_columnas(X)

    modelos = construir_modelos(
        columnas_numericas=columnas_numericas,
        columnas_categoricas=columnas_categoricas,
    )

    modelo = modelos[MODELO_FINAL]

    # ==========================================
    # ENTRENAR CON TODOS LOS DATOS
    # ==========================================

    print(
        "\n========== ENTRENAMIENTO FINAL ==========\n"
    )

    print(f"Experimento: {EXPERIMENTO_FINAL}")
    print(f"Modelo: {MODELO_FINAL}")
    print(f"Registros utilizados: {len(X)}")
    print(f"Productos únicos: {grupos.nunique()}")
    print(f"Variables predictoras: {X.shape[1]}")

    print(
        "\nEntrenando modelo con todo el "
        "Experimento B..."
    )

    modelo.fit(
        X,
        y,
    )

    # ==========================================
    # GUARDAR PIPELINE
    # ==========================================

    ruta_modelo = (
        carpeta_modelos
        / "modapredict_hgb.joblib"
    )

    joblib.dump(
        modelo,
        ruta_modelo,
    )

    # ==========================================
    # GUARDAR METADATOS
    # ==========================================

    metadatos = {
        "nombre_modelo": MODELO_FINAL,
        "experimento": EXPERIMENTO_FINAL,
        "variable_objetivo": "modapredict_score",
        "registros_entrenamiento": len(X),
        "productos_unicos": int(grupos.nunique()),
        "numero_variables": X.shape[1],
        "columnas_predictoras": X.columns.tolist(),
        "columnas_numericas": columnas_numericas,
        "columnas_categoricas": columnas_categoricas,
        "fecha_entrenamiento": datetime.now().isoformat(),
        "advertencia": (
            "El modelo estima el ModaPredict Score. "
            "No predice ventas ni demanda real."
        ),
    }

    ruta_metadatos = (
        carpeta_modelos
        / "metadatos_modelo.json"
    )

    with open(
        ruta_metadatos,
        "w",
        encoding="utf-8",
    ) as archivo:
        json.dump(
            metadatos,
            archivo,
            ensure_ascii=False,
            indent=4,
        )

    print(
        "\nModelo guardado correctamente en:"
        f"\n{ruta_modelo}"
    )

    print(
        "\nMetadatos guardados en:"
        f"\n{ruta_metadatos}"
    )


if __name__ == "__main__":
    main()