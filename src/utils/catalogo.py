from pathlib import Path

import pandas as pd


COLUMNAS_MAESTRAS = [
    "id_producto",
    "nombre",
    "marca",
    "color",
    "precio_actual",
    "precio_anterior",
    "precio_minimo",
    "precio_maximo",
    "moneda",
    "categoria",
    "es_nuevo",
    "en_descuento",
    "promocion",
    "venta_rapida",
    "disponibilidad",
    "proximamente",
    "en_linea",
    "tallas_disponibles",
    "cantidad_tallas",
    "stock_total_api",
    "url_producto",
    "url_imagen",
    "fuente",
]


def preparar_catalogo_asos(df_asos: pd.DataFrame) -> pd.DataFrame:
    """Adapta las columnas de ASOS al formato maestro."""

    catalogo_asos = df_asos.copy()

    catalogo_asos["precio_minimo"] = pd.NA
    catalogo_asos["precio_maximo"] = pd.NA
    catalogo_asos["categoria"] = pd.NA
    catalogo_asos["disponibilidad"] = pd.NA
    catalogo_asos["proximamente"] = pd.NA
    catalogo_asos["en_linea"] = pd.NA
    catalogo_asos["tallas_disponibles"] = pd.NA
    catalogo_asos["cantidad_tallas"] = pd.NA
    catalogo_asos["stock_total_api"] = pd.NA
    catalogo_asos["fuente"] = "ASOS"

    return catalogo_asos.reindex(columns=COLUMNAS_MAESTRAS)


def preparar_catalogo_hm(df_hm: pd.DataFrame) -> pd.DataFrame:
    """Adapta las columnas de H&M al formato maestro."""

    catalogo_hm = df_hm.copy()

    catalogo_hm["precio_anterior"] = pd.NA
    catalogo_hm["en_descuento"] = pd.NA
    catalogo_hm["promocion"] = pd.NA
    catalogo_hm["venta_rapida"] = pd.NA

    return catalogo_hm.reindex(columns=COLUMNAS_MAESTRAS)


def unir_catalogos(
    df_asos: pd.DataFrame,
    df_hm: pd.DataFrame,
) -> pd.DataFrame:
    """Une los catálogos de ASOS y H&M."""

    asos_preparado = preparar_catalogo_asos(df_asos)
    hm_preparado = preparar_catalogo_hm(df_hm)

    catalogo_maestro = pd.concat(
        [asos_preparado, hm_preparado],
        ignore_index=True,
    )

    catalogo_maestro["id_unico"] = (
        catalogo_maestro["fuente"].astype(str)
        + "_"
        + catalogo_maestro["id_producto"].astype(str)
    )

    columnas_finales = [
        "id_unico",
        *COLUMNAS_MAESTRAS,
    ]

    return catalogo_maestro[columnas_finales]


def guardar_catalogo_maestro(
    dataframe: pd.DataFrame,
) -> Path:
    """Guarda el catálogo unificado en formato CSV."""

    ruta_proyecto = Path(__file__).resolve().parents[2]
    carpeta_datos = ruta_proyecto / "datos"
    carpeta_datos.mkdir(exist_ok=True)

    ruta_archivo = carpeta_datos / "catalogo_maestro.csv"

    dataframe.to_csv(
        ruta_archivo,
        index=False,
        encoding="utf-8-sig",
    )

    print(
        "Catálogo maestro guardado correctamente en:"
        f" {ruta_archivo}"
    )

    return ruta_archivo