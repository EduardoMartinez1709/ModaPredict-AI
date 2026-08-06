from pathlib import Path

import pandas as pd

from src.utils.scoring import (
    agregar_modapredict_score,
    agregar_score_clima,
    agregar_score_marca,
    agregar_score_popularidad,
    agregar_score_precio,
    agregar_score_trends,
)

def main():

    ruta = Path(__file__).resolve().parent

    datos = ruta / "datos"

    catalogo = pd.read_csv(
        datos / "catalogo_features.csv"
    )

    catalogo = agregar_score_trends(
        catalogo
    )

    catalogo = agregar_score_clima(
    catalogo
)
    catalogo = agregar_score_precio(
    catalogo
)
    catalogo = agregar_score_marca(
    catalogo
)
    catalogo = agregar_score_popularidad(
    catalogo
)
    catalogo = agregar_modapredict_score(
    catalogo
)

    print()

    print("========== SCORE TRENDS ==========")

    print()
    

    print(
    catalogo[
        [
            "nombre",
            "ciudad",
            "score_tendencia_30",
            "score_clima_25",
            "score_precio_20",
            "score_marca_15",
            "score_popularidad_10",
            "modapredict_score",
            "nivel_recomendacion",
        ]
    ].head(30)
)
    
    salida = (
        datos
        / "catalogo_scoring.csv"
    )

    catalogo.to_csv(
        salida,
        index=False,
        encoding="utf-8-sig",
    )

    print()

    print(
        f"Archivo guardado:\n{salida}"
    )


if __name__ == "__main__":
    main()