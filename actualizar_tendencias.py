from pathlib import Path
import time

import pandas as pd
from pytrends.request import TrendReq


# ==========================
# TÉRMINOS A CONSULTAR
# ==========================

GRUPOS_TERMINOS = [

[
"playeras",
"camisetas",
"blusas",
"camisas",
"polos",
],
[
"sudaderas",
"hoodies",
"chamarras",
"abrigos",
"suéteres",
],
[
"jeans",
"pantalones",
"pantalones cargo",
"shorts",
"joggers",
],
[
"vestidos",
"faldas",
"leggins",
"tenis",
"botas",
],
[
"bolsas",
"gorras",
"streetwear",
"oversize",
"ropa vintage",
],
]


# ==========================
# GOOGLE TRENDS
# ==========================

def obtener_tendencias(terminos):

    pytrends = TrendReq(
        hl="es-MX",
        tz=360,
    )

    pytrends.build_payload(
        terminos,
        cat=0,
        timeframe="today 12-m",
        geo="MX",
        gprop="",
    )

    tendencias = pytrends.interest_over_time()

    if "isPartial" in tendencias.columns:
        tendencias = tendencias.drop(
            columns=["isPartial"]
        )

    return tendencias


# ==========================
# GUARDAR CSV
# ==========================

def guardar_tendencias(df):

    ruta = (
        Path(__file__).resolve().parent
        / "datos"
        / "google_trends.csv"
    )

    df.to_csv(
        ruta,
        index=True,
        encoding="utf-8-sig",
    )

    return ruta


# ==========================
# MAIN
# ==========================

def main():

    print("\n========== GOOGLE TRENDS ==========\n")

    resultados = []

    for numero_grupo, terminos in enumerate(
        GRUPOS_TERMINOS,
        start=1,
    ):

        print(
            f"Consultando grupo {numero_grupo}: "
            f"{', '.join(terminos)}"
        )

        tendencias = obtener_tendencias(
            terminos
        )

        resultados.append(
            tendencias
        )

        time.sleep(5)

    tendencias_finales = pd.concat(
        resultados,
        axis=1,
    )

    tendencias_finales = (
        tendencias_finales.loc[
            :,
            ~tendencias_finales.columns.duplicated(),
        ]
    )

    print("\nVista previa:\n")
    print(tendencias_finales.head())

    ruta = guardar_tendencias(
        tendencias_finales
    )

    print(
        f"\nRegistros obtenidos: {len(tendencias_finales)}"
    )

    print(f"Archivo guardado en:\n{ruta}")


if __name__ == "__main__":
    main()