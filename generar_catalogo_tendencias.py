from pathlib import Path

import pandas as pd

from src.utils.feature_engineering import (
    agregar_categoria_detectada,
    agregar_tendencias,
    generar_reporte_clasificacion,
)


def main():
    ruta_proyecto = Path(__file__).resolve().parent
    carpeta_datos = ruta_proyecto / "datos"

    catalogo = pd.read_csv(
        carpeta_datos / "catalogo_maestro.csv"
    )

    resumen_tendencias = pd.read_csv(
        carpeta_datos / "resumen_tendencias.csv"
    )

    catalogo = agregar_categoria_detectada(
        catalogo
    )

    catalogo_enriquecido = agregar_tendencias(
        catalogo,
        resumen_tendencias,
    )

    generar_reporte_clasificacion(
        catalogo_enriquecido
    )

    ruta_salida = (
        carpeta_datos
        / "catalogo_con_tendencias.csv"
    )

    catalogo_enriquecido.to_csv(
        ruta_salida,
        index=False,
        encoding="utf-8-sig",
    )

    print(
        "\nArchivo guardado correctamente en:"
        f"\n{ruta_salida}"
    )


if __name__ == "__main__":
    main()