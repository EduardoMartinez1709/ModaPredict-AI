from pathlib import Path

import pandas as pd


def cargar_datos() -> tuple[pd.DataFrame, pd.DataFrame]:
    ruta_proyecto = Path(__file__).resolve().parents[2]
    carpeta_datos = ruta_proyecto / "datos"

    catalogo = pd.read_csv(
        carpeta_datos / "catalogo_maestro.csv"
    )

    tendencias = pd.read_csv(
        carpeta_datos / "google_trends.csv"
    )

    return catalogo, tendencias


def transformar_trends_formato_largo(
    tendencias: pd.DataFrame,
) -> pd.DataFrame:
    """
    Convierte Google Trends de muchas columnas
    a tres columnas: fecha, termino e interes.
    """

    primera_columna = tendencias.columns[0]

    tendencias = tendencias.rename(
        columns={primera_columna: "fecha"}
    )

    tendencias_largas = tendencias.melt(
        id_vars="fecha",
        var_name="termino",
        value_name="interes",
    )

    tendencias_largas["fecha"] = pd.to_datetime(
        tendencias_largas["fecha"],
        errors="coerce",
    )

    tendencias_largas["interes"] = pd.to_numeric(
        tendencias_largas["interes"],
        errors="coerce",
    )

    return tendencias_largas


def generar_resumen_tendencias(
    tendencias_largas: pd.DataFrame,
) -> pd.DataFrame:
    """
    Resume el interés promedio, reciente y crecimiento
    de cada término.
    """

    registros = []

    for termino, grupo in tendencias_largas.groupby("termino"):
        grupo = grupo.sort_values("fecha").dropna(
            subset=["interes"]
        )

        if grupo.empty:
            continue

        interes_promedio = grupo["interes"].mean()

        ultimas_4 = grupo.tail(4)["interes"].mean()
        primeras_4 = grupo.head(4)["interes"].mean()

        if primeras_4 > 0:
            crecimiento = (
                (ultimas_4 - primeras_4)
                / primeras_4
                * 100
            )
        else:
            crecimiento = 0

        if crecimiento >= 10:
            estado = "Creciente"
        elif crecimiento <= -10:
            estado = "Descendente"
        else:
            estado = "Estable"

        registros.append(
            {
                "termino": termino,
                "interes_promedio": round(
                    interes_promedio,
                    2,
                ),
                "interes_reciente": round(
                    ultimas_4,
                    2,
                ),
                "crecimiento_pct": round(
                    crecimiento,
                    2,
                ),
                "tendencia": estado,
            }
        )

    resumen = pd.DataFrame(registros)

    return resumen.sort_values(
        by="interes_reciente",
        ascending=False,
    )


def generar_perfil_catalogo(
    catalogo: pd.DataFrame,
) -> None:
    print("\n========== PERFIL DEL CATÁLOGO ==========\n")

    print(f"Productos: {len(catalogo)}")
    print(f"Columnas: {catalogo.shape[1]}")

    print("\nProductos por fuente:")
    print(catalogo["fuente"].value_counts())

    print("\nMarcas diferentes:")
    print(catalogo["marca"].nunique())

    print("\nTop 10 marcas:")
    print(catalogo["marca"].value_counts().head(10))

    print("\nTop 10 colores:")
    print(catalogo["color"].value_counts().head(10))

    precios = pd.to_numeric(
        catalogo["precio_actual"],
        errors="coerce",
    )

    print("\nResumen de precios:")
    print(f"Promedio: ${precios.mean():.2f}")
    print(f"Mínimo: ${precios.min():.2f}")
    print(f"Máximo: ${precios.max():.2f}")

    print("\nValores nulos:")
    nulos = catalogo.isna().sum()
    print(nulos[nulos > 0].sort_values(ascending=False))

    print("\nIDs únicos duplicados:")
    print(catalogo["id_unico"].duplicated().sum())


def guardar_resultados(
    tendencias_largas: pd.DataFrame,
    resumen_tendencias: pd.DataFrame,
) -> None:
    ruta_proyecto = Path(__file__).resolve().parents[2]
    carpeta_datos = ruta_proyecto / "datos"

    tendencias_largas.to_csv(
        carpeta_datos / "google_trends_largo.csv",
        index=False,
        encoding="utf-8-sig",
    )

    resumen_tendencias.to_csv(
        carpeta_datos / "resumen_tendencias.csv",
        index=False,
        encoding="utf-8-sig",
    )