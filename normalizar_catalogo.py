from pathlib import Path

import pandas as pd

from src.utils.normalizacion import (
    generar_reporte_normalizacion,
    normalizar_catalogo,
)


def main():
    ruta_proyecto = Path(__file__).resolve().parent
    carpeta_datos = ruta_proyecto / "datos"

    ruta_entrada = (
        carpeta_datos
        / "catalogo_con_tendencias.csv"
    )

    if not ruta_entrada.exists():
        raise FileNotFoundError(
            "No se encontró catalogo_con_tendencias.csv. "
            "Ejecuta primero generar_catalogo_tendencias.py"
        )

    catalogo = pd.read_csv(ruta_entrada)

    catalogo_normalizado = normalizar_catalogo(
        catalogo
    )

    generar_reporte_normalizacion(
        catalogo_normalizado
    )

    ruta_salida = (
        carpeta_datos
        / "catalogo_normalizado.csv"
    )

    catalogo_normalizado.to_csv(
        ruta_salida,
        index=False,
        encoding="utf-8-sig",
    )

    print(
        "\nArchivo normalizado guardado en:"
        f"\n{ruta_salida}"
    )


if __name__ == "__main__":
    main()