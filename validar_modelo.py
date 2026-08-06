from pathlib import Path

from src.modelos.validacion_cruzada import (
    ejecutar_validacion_cruzada,
    generar_reporte_validacion,
)


def main():
    ruta_proyecto = Path(__file__).resolve().parent

    carpeta_resultados = (
        ruta_proyecto
        / "resultados"
    )

    carpeta_resultados.mkdir(
        parents=True,
        exist_ok=True,
    )

    (
        resultados_folds,
        resumen,
    ) = ejecutar_validacion_cruzada(
        numero_folds=5
    )

    generar_reporte_validacion(
        resultados_folds,
        resumen,
    )

    ruta_folds = (
        carpeta_resultados
        / "validacion_cruzada_folds.csv"
    )

    ruta_resumen = (
        carpeta_resultados
        / "validacion_cruzada_resumen.csv"
    )

    resultados_folds.to_csv(
        ruta_folds,
        index=False,
        encoding="utf-8-sig",
    )

    resumen.to_csv(
        ruta_resumen,
        index=False,
        encoding="utf-8-sig",
    )

    print(
        "\nArchivos generados:"
    )
    print(
        f"- {ruta_folds}"
    )
    print(
        f"- {ruta_resumen}"
    )


if __name__ == "__main__":
    main()