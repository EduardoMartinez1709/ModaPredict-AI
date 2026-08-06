from pathlib import Path

import pandas as pd

from src.modelos.entrenamiento import (
    construir_modelos,
)
from src.modelos.evaluacion import (
    construir_tabla_predicciones,
    entrenar_y_evaluar_modelos,
)
from src.modelos.preparacion import (
    generar_reporte_preparacion,
    preparar_datos_experimento,
)


def ejecutar_experimento(
    experimento: str,
    carpeta_resultados: Path,
) -> pd.DataFrame:

    print(
        f"\n\n########## EXPERIMENTO {experimento} ##########"
    )

    datos = preparar_datos_experimento(
        experimento=experimento
    )

    generar_reporte_preparacion(datos)

    modelos = construir_modelos(
        columnas_numericas=datos[
            "columnas_numericas"
        ],
        columnas_categoricas=datos[
            "columnas_categoricas"
        ],
    )

    (
        metricas,
        modelos_entrenados,
        predicciones,
    ) = entrenar_y_evaluar_modelos(
        modelos=modelos,
        X_train=datos["X_train"],
        y_train=datos["y_train"],
        X_test=datos["X_test"],
        y_test=datos["y_test"],
    )

    metricas["experimento"] = experimento
    metricas["numero_variables"] = (
        datos["X_train"].shape[1]
    )

    tabla_predicciones = (
        construir_tabla_predicciones(
            y_test=datos["y_test"],
            predicciones=predicciones,
            grupos_test=datos[
                "grupos_test"
            ],
        )
    )

    metricas.to_csv(
        carpeta_resultados
        / f"metricas_experimento_{experimento}.csv",
        index=False,
        encoding="utf-8-sig",
    )

    tabla_predicciones.to_csv(
        carpeta_resultados
        / f"predicciones_experimento_{experimento}.csv",
        index=False,
        encoding="utf-8-sig",
    )

    print(
        f"\nResultados del Experimento {experimento}:"
    )
    print(
        metricas.to_string(index=False)
    )

    return metricas


def main():
    ruta_proyecto = Path(__file__).resolve().parent

    carpeta_resultados = (
        ruta_proyecto / "resultados"
    )

    carpeta_resultados.mkdir(
        parents=True,
        exist_ok=True,
    )

    metricas_a = ejecutar_experimento(
        experimento="A",
        carpeta_resultados=carpeta_resultados,
    )

    metricas_b = ejecutar_experimento(
        experimento="B",
        carpeta_resultados=carpeta_resultados,
    )

    comparacion = pd.concat(
        [metricas_a, metricas_b],
        ignore_index=True,
    )

    comparacion = comparacion[
        [
            "experimento",
            "modelo",
            "numero_variables",
            "MAE",
            "RMSE",
            "R2",
        ]
    ].sort_values(
        ["experimento", "MAE"]
    )

    ruta_comparacion = (
        carpeta_resultados
        / "comparacion_experimentos.csv"
    )

    comparacion.to_csv(
        ruta_comparacion,
        index=False,
        encoding="utf-8-sig",
    )

    print(
        "\n========== COMPARACIÓN FINAL ==========\n"
    )

    print(
        comparacion.to_string(index=False)
    )

    print(
        f"\nArchivo generado:\n{ruta_comparacion}"
    )


if __name__ == "__main__":
    main()