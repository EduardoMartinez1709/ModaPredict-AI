from pathlib import Path

import pandas as pd

from src.utils.feature_engineering_avanzado import (
    construir_features,
    generar_reporte_features,
)


def main():
    ruta_proyecto = Path(__file__).resolve().parent
    carpeta_datos = ruta_proyecto / "datos"

    ruta_catalogo = (
        carpeta_datos
        / "catalogo_normalizado.csv"
    )

    ruta_clima = (
        carpeta_datos
        / "externos"
        / "clima"
        / "pronostico_ciudades.csv"
    )

    if not ruta_catalogo.exists():
        raise FileNotFoundError(
            "No se encontró catalogo_normalizado.csv. "
            "Ejecuta primero normalizar_catalogo.py"
        )

    if not ruta_clima.exists():
        raise FileNotFoundError(
            "No se encontró pronostico_ciudades.csv. "
            "Ejecuta primero actualizar_clima.py"
        )

    catalogo = pd.read_csv(
        ruta_catalogo
    )

    clima = pd.read_csv(
        ruta_clima
    )

    catalogo_features = construir_features(
        catalogo=catalogo,
        clima=clima,
    )

    generar_reporte_features(
        catalogo_features
    )

    ruta_salida = (
        carpeta_datos
        / "catalogo_features.csv"
    )

    catalogo_features.to_csv(
        ruta_salida,
        index=False,
        encoding="utf-8-sig",
    )

    print(
        "\nArchivo de features guardado en:"
        f"\n{ruta_salida}"
    )


if __name__ == "__main__":
    main()