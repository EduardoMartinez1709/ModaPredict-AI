from __future__ import annotations

import json
import os
from html import escape
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd


# ==========================================================
# RUTAS DEL PROYECTO
# ==========================================================

RUTA_PROYECTO = Path(__file__).resolve().parents[1]

RUTA_CATALOGO = (
    RUTA_PROYECTO
    / "datos"
    / "catalogo_scoring.csv"
)

RUTA_MODELO = (
    RUTA_PROYECTO
    / "modelos_guardados"
    / "modapredict_hgb.joblib"
)

RUTA_METADATOS = (
    RUTA_PROYECTO
    / "modelos_guardados"
    / "metadatos_modelo.json"
)

RUTA_RESULTADOS = (
    RUTA_PROYECTO
    / "resultados"
)

MONEDA_BASE = "USD"
MONEDA_PRESUPUESTO = "MXN"

# Tipo de cambio de referencia configurable.
# Puedes modificarlo sin tocar el código:
# export MODAPREDICT_USD_MXN=18.50
TIPO_CAMBIO_USD_MXN = float(
    os.getenv(
        "MODAPREDICT_USD_MXN",
        "18.00",
    )
)


def convertir_mxn_a_usd(
    cantidad_mxn: float | None,
) -> float | None:
    """
    Convierte un presupuesto expresado en MXN a USD.

    El catálogo utiliza USD, mientras que la interfaz del
    emprendedor trabaja con presupuestos en pesos mexicanos.
    """

    if cantidad_mxn is None:
        return None

    cantidad = max(
        0.0,
        float(cantidad_mxn),
    )

    if TIPO_CAMBIO_USD_MXN <= 0:
        raise ValueError(
            "TIPO_CAMBIO_USD_MXN debe ser mayor que cero."
        )

    return cantidad / TIPO_CAMBIO_USD_MXN


def formatear_moneda(
    cantidad: float | None,
    moneda: str = MONEDA_BASE,
) -> str:
    """Formatea una cantidad monetaria de manera consistente."""

    if cantidad is None:
        return "Sin definir"

    return f"${float(cantidad):,.2f} {moneda}"


# ==========================================================
# CARGA Y VALIDACIÓN DE RECURSOS
# ==========================================================

def cargar_metadatos() -> dict[str, Any]:
    """Carga los metadatos del modelo final."""

    if not RUTA_METADATOS.exists():
        raise FileNotFoundError(
            "No se encontró modelos_guardados/"
            "metadatos_modelo.json."
        )

    with open(
        RUTA_METADATOS,
        "r",
        encoding="utf-8",
    ) as archivo:
        return json.load(archivo)


def cargar_modelo():
    """Carga el pipeline completo de Machine Learning."""

    if not RUTA_MODELO.exists():
        raise FileNotFoundError(
            "No se encontró modelos_guardados/"
            "modapredict_hgb.joblib."
        )

    return joblib.load(RUTA_MODELO)


def cargar_catalogo() -> pd.DataFrame:
    """Carga el catálogo final con features y scoring."""

    if not RUTA_CATALOGO.exists():
        raise FileNotFoundError(
            "No se encontró datos/catalogo_scoring.csv. "
            "Ejecuta primero generar_scoring.py."
        )

    catalogo = pd.read_csv(RUTA_CATALOGO)

    columnas_requeridas = [
        "id_unico",
        "nombre",
        "marca_normalizada",
        "categoria_normalizada",
        "ciudad",
        "precio_actual",
        "modapredict_score",
        "nivel_recomendacion",
        "explicacion_score",
        "fuente",
    ]

    faltantes = [
        columna
        for columna in columnas_requeridas
        if columna not in catalogo.columns
    ]

    if faltantes:
        raise ValueError(
            "El catálogo no contiene las columnas requeridas: "
            + ", ".join(faltantes)
        )

    catalogo["precio_actual"] = pd.to_numeric(
        catalogo["precio_actual"],
        errors="coerce",
    )

    catalogo["modapredict_score"] = pd.to_numeric(
        catalogo["modapredict_score"],
        errors="coerce",
    )

    columnas_numericas_opcionales = [
        "interes_reciente",
        "temperatura_media",
        "prediccion_ml",
    ]

    for columna in columnas_numericas_opcionales:
        if columna in catalogo.columns:
            catalogo[columna] = pd.to_numeric(
                catalogo[columna],
                errors="coerce",
            )

    catalogo = catalogo.dropna(
        subset=[
            "id_unico",
            "nombre",
            "ciudad",
            "precio_actual",
            "modapredict_score",
        ]
    ).copy()

    return catalogo


def preparar_catalogo_con_predicciones(
    catalogo: pd.DataFrame,
    modelo,
    metadatos: dict[str, Any],
) -> pd.DataFrame:
    """
    Agrega la predicción del modelo ML y la diferencia
    frente al sistema experto.
    """

    nuevo = catalogo.copy()

    columnas_predictoras = metadatos.get(
        "columnas_predictoras",
        [],
    )

    faltantes = [
        columna
        for columna in columnas_predictoras
        if columna not in nuevo.columns
    ]

    if faltantes:
        raise ValueError(
            "Faltan variables necesarias para el modelo: "
            + ", ".join(faltantes)
        )

    nuevo["prediccion_ml"] = modelo.predict(
        nuevo[columnas_predictoras]
    )

    nuevo["prediccion_ml"] = (
        pd.to_numeric(
            nuevo["prediccion_ml"],
            errors="coerce",
        )
        .clip(0, 100)
        .round(2)
    )

    nuevo["diferencia_modelo"] = (
        nuevo["modapredict_score"]
        - nuevo["prediccion_ml"]
    ).abs().round(2)

    return nuevo


METADATOS = cargar_metadatos()
MODELO = cargar_modelo()
CATALOGO = preparar_catalogo_con_predicciones(
    catalogo=cargar_catalogo(),
    modelo=MODELO,
    metadatos=METADATOS,
)


# ==========================================================
# OPCIONES PARA LA INTERFAZ
# ==========================================================

def obtener_opciones_interfaz() -> dict[str, Any]:
    """Obtiene los valores disponibles para los filtros."""

    ciudades = sorted(
        CATALOGO["ciudad"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    categorias = sorted(
        CATALOGO["categoria_normalizada"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    marcas = sorted(
        CATALOGO["marca_normalizada"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    fuentes = sorted(
        CATALOGO["fuente"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    precio_maximo = float(
        CATALOGO["precio_actual"].max()
    )

    return {
        "ciudades": ["Todas", *ciudades],
        "categorias": ["Todas", *categorias],
        "marcas": ["Todas", *marcas],
        "fuentes": ["Todas", *fuentes],
        "precio_maximo": precio_maximo,
        "moneda": MONEDA_BASE,
    }


# ==========================================================
# FILTROS Y RECOMENDACIONES
# ==========================================================

def filtrar_catalogo(
    ciudad: str = "Todas",
    categoria: str = "Todas",
    marca: str = "Todas",
    fuente: str = "Todas",
    precio_minimo: float = 0,
    precio_maximo: float | None = None,
) -> pd.DataFrame:
    """Aplica filtros generales al catálogo."""

    datos = CATALOGO.copy()

    if ciudad and ciudad != "Todas":
        datos = datos.loc[
            datos["ciudad"].eq(ciudad)
        ]

    if categoria and categoria != "Todas":
        datos = datos.loc[
            datos["categoria_normalizada"].eq(
                categoria
            )
        ]

    if marca and marca != "Todas":
        datos = datos.loc[
            datos["marca_normalizada"].eq(marca)
        ]

    if fuente and fuente != "Todas":
        datos = datos.loc[
            datos["fuente"].eq(fuente)
        ]

    datos = datos.loc[
        datos["precio_actual"].ge(
            float(precio_minimo or 0)
        )
    ]

    if precio_maximo is not None:
        datos = datos.loc[
            datos["precio_actual"].le(
                float(precio_maximo)
            )
        ]

    return datos.copy()


def obtener_recomendaciones(
    ciudad: str = "Todas",
    categoria: str = "Todas",
    marca: str = "Todas",
    fuente: str = "Todas",
    precio_minimo: float = 0,
    precio_maximo: float | None = None,
    cantidad: int = 10,
) -> pd.DataFrame:
    """
    Devuelve los productos mejor posicionados después
    de aplicar los filtros.
    """

    datos = filtrar_catalogo(
        ciudad=ciudad,
        categoria=categoria,
        marca=marca,
        fuente=fuente,
        precio_minimo=precio_minimo,
        precio_maximo=precio_maximo,
    )

    if datos.empty:
        return datos

    cantidad = max(
        1,
        min(int(cantidad), 30),
    )

    # Si se seleccionan todas las ciudades, conservamos
    # únicamente el mejor escenario de cada producto.
    datos = (
        datos.sort_values(
            by=[
                "modapredict_score",
                "prediccion_ml",
                "precio_actual",
            ],
            ascending=[
                False,
                False,
                True,
            ],
        )
        .drop_duplicates(
            subset="id_unico",
            keep="first",
        )
        .head(cantidad)
        .copy()
    )

    return datos


# ==========================================================
# CONSULTAS PARA EMPRENDEDORES
# ==========================================================

def resumen_para_emprendedor(
    ciudad: str,
    presupuesto: float | None = None,
) -> dict[str, Any]:
    """
    Resume las mejores oportunidades para un emprendedor.
    """

    datos = filtrar_catalogo(
        ciudad=ciudad,
    )

    if datos.empty:
        return {
            "ciudad": ciudad,
            "productos_disponibles": 0,
            "score_promedio": 0,
            "categoria_destacada": "Sin información",
            "precio_promedio": 0,
            "productos_sugeridos": pd.DataFrame(),
        }

    por_categoria = (
        datos.groupby(
            "categoria_normalizada",
            as_index=False,
        )
        .agg(
            score_promedio=(
                "modapredict_score",
                "mean",
            ),
            precio_promedio=(
                "precio_actual",
                "mean",
            ),
            productos=(
                "id_unico",
                "nunique",
            ),
        )
        .sort_values(
            "score_promedio",
            ascending=False,
        )
    )

    categoria_destacada = (
        por_categoria.iloc[0][
            "categoria_normalizada"
        ]
    )

    presupuesto_usd = convertir_mxn_a_usd(
        presupuesto
    )

    sugeridos = obtener_recomendaciones(
        ciudad=ciudad,
        precio_maximo=presupuesto_usd,
        cantidad=10,
    )

    return {
        "ciudad": ciudad,
        "productos_disponibles": int(
            datos["id_unico"].nunique()
        ),
        "score_promedio": round(
            float(datos["modapredict_score"].mean()),
            2,
        ),
        "categoria_destacada": categoria_destacada,
        "precio_promedio": round(
            float(datos["precio_actual"].mean()),
            2,
        ),
        "productos_sugeridos": sugeridos,
        "presupuesto_mxn": (
            float(presupuesto)
            if presupuesto is not None
            else None
        ),
        "presupuesto_usd": (
            round(float(presupuesto_usd), 2)
            if presupuesto_usd is not None
            else None
        ),
        "tipo_cambio_usd_mxn": TIPO_CAMBIO_USD_MXN,
        "moneda_catalogo": MONEDA_BASE,
        "moneda_presupuesto": MONEDA_PRESUPUESTO,
    }


# ==========================================================
# CONSULTAS PARA EMPRESAS
# ==========================================================

def resumen_para_empresa(
    ciudad: str = "Todas",
) -> dict[str, Any]:
    """Genera KPIs ejecutivos para empresas."""

    datos = filtrar_catalogo(
        ciudad=ciudad,
    )

    if datos.empty:
        return {
            "productos_unicos": 0,
            "marcas": 0,
            "categorias": 0,
            "score_promedio": 0,
            "precio_promedio": 0,
            "por_fuente": pd.DataFrame(),
            "por_categoria": pd.DataFrame(),
            "por_ciudad": pd.DataFrame(),
        }

    por_fuente = (
        datos.groupby(
            "fuente",
            as_index=False,
        )
        .agg(
            productos=(
                "id_unico",
                "nunique",
            ),
            score_promedio=(
                "modapredict_score",
                "mean",
            ),
            precio_promedio=(
                "precio_actual",
                "mean",
            ),
        )
    )

    por_categoria = (
        datos.groupby(
            "categoria_normalizada",
            as_index=False,
        )
        .agg(
            productos=(
                "id_unico",
                "nunique",
            ),
            score_promedio=(
                "modapredict_score",
                "mean",
            ),
            precio_promedio=(
                "precio_actual",
                "mean",
            ),
        )
        .sort_values(
            "score_promedio",
            ascending=False,
        )
    )

    por_ciudad = (
        datos.groupby(
            "ciudad",
            as_index=False,
        )
        .agg(
            productos=(
                "id_unico",
                "nunique",
            ),
            score_promedio=(
                "modapredict_score",
                "mean",
            ),
            prediccion_promedio=(
                "prediccion_ml",
                "mean",
            ),
        )
        .sort_values(
            "score_promedio",
            ascending=False,
        )
    )

    return {
        "productos_unicos": int(
            datos["id_unico"].nunique()
        ),
        "marcas": int(
            datos["marca_normalizada"].nunique()
        ),
        "categorias": int(
            datos[
                "categoria_normalizada"
            ].nunique()
        ),
        "score_promedio": round(
            float(datos["modapredict_score"].mean()),
            2,
        ),
        "precio_promedio": round(
            float(datos["precio_actual"].mean()),
            2,
        ),
        "por_fuente": por_fuente,
        "por_categoria": por_categoria,
        "por_ciudad": por_ciudad,
    }


# ==========================================================
# COMPARACIONES
# ==========================================================

def comparar_ciudades(
    ciudad_1: str,
    ciudad_2: str,
    categoria: str = "Todas",
) -> pd.DataFrame:
    """Compara dos ciudades para una categoría."""

    resultados = []

    for ciudad in [ciudad_1, ciudad_2]:
        datos = filtrar_catalogo(
            ciudad=ciudad,
            categoria=categoria,
        )

        if datos.empty:
            resultados.append(
                {
                    "Ciudad": ciudad,
                    "Productos": 0,
                    "Score promedio": 0,
                    "Predicción ML": 0,
                    "Precio promedio": 0,
                    "Temperatura media": np.nan,
                }
            )
            continue

        resultados.append(
            {
                "Ciudad": ciudad,
                "Productos": int(
                    datos["id_unico"].nunique()
                ),
                "Score promedio": round(
                    float(
                        datos[
                            "modapredict_score"
                        ].mean()
                    ),
                    2,
                ),
                "Predicción ML": round(
                    float(
                        datos[
                            "prediccion_ml"
                        ].mean()
                    ),
                    2,
                ),
                "Precio promedio": round(
                    float(
                        datos[
                            "precio_actual"
                        ].mean()
                    ),
                    2,
                ),
                "Temperatura media": (
                    round(
                        float(
                            datos["temperatura_media"].mean()
                        ),
                        2,
                    )
                    if (
                        "temperatura_media" in datos.columns
                        and datos["temperatura_media"].notna().any()
                    )
                    else np.nan
                ),
            }
        )

    return pd.DataFrame(resultados)


def obtener_detalle_producto(
    id_unico: str,
    ciudad: str | None = None,
) -> pd.Series | None:
    """Busca un producto específico."""

    datos = CATALOGO.loc[
        CATALOGO["id_unico"]
        .astype(str)
        .eq(str(id_unico))
    ]

    if ciudad:
        datos = datos.loc[
            datos["ciudad"].eq(ciudad)
        ]

    if datos.empty:
        return None

    return datos.sort_values(
        "modapredict_score",
        ascending=False,
    ).iloc[0]


# ==========================================================
# INTERPRETACIÓN DE OPORTUNIDAD
# ==========================================================

def interpretar_oportunidad(
    score: float,
    ciudad: str | None = None,
) -> dict[str, str]:
    """
    Traduce el ModaPredict Score a una lectura sencilla
    para usuarios no técnicos.

    No modifica el score ni el modelo.
    Solo cambia la forma de comunicar el resultado.
    """

    try:
        valor = float(score)
    except (TypeError, ValueError):
        valor = 0.0

    valor = max(
        0.0,
        min(100.0, valor),
    )

    if valor >= 80:
        nivel = "Excelente oportunidad"
        estrellas = "★★★★★"
        mensaje = "Muy recomendable para considerar."
        clase_css = "oportunidad-excelente"

    elif valor >= 65:
        nivel = "Buena oportunidad"
        estrellas = "★★★★☆"
        mensaje = "Vale la pena revisarlo como una opción prioritaria."
        clase_css = "oportunidad-buena"

    elif valor >= 50:
        nivel = "Oportunidad moderada"
        estrellas = "★★★☆☆"
        mensaje = "Puede funcionar, pero conviene comparar otras opciones."
        clase_css = "oportunidad-moderada"

    elif valor >= 35:
        nivel = "Oportunidad limitada"
        estrellas = "★★☆☆☆"
        mensaje = "No sería de las primeras opciones para invertir."
        clase_css = "oportunidad-limitada"

    else:
        nivel = "Baja oportunidad"
        estrellas = "★☆☆☆☆"
        mensaje = "Por ahora no parece una opción prioritaria."
        clase_css = "oportunidad-baja"

    if ciudad and ciudad != "Todas":
        if valor >= 65:
            mensaje = (
                f"{mensaje.rstrip('.')} para vender en {ciudad}."
            )
        else:
            mensaje = (
                f"{mensaje.rstrip('.')} en {ciudad}."
            )

    return {
        "nivel": nivel,
        "estrellas": estrellas,
        "mensaje": mensaje,
        "clase_css": clase_css,
        "score_formateado": f"{valor:.1f}",
    }


# ==========================================================
# FORMATO PARA INTERFAZ
# ==========================================================

def construir_tabla_recomendaciones(
    datos: pd.DataFrame,
) -> pd.DataFrame:
    """Crea una tabla limpia para mostrar en Gradio."""

    if datos.empty:
        return pd.DataFrame(
            columns=[
                "Producto",
                "Marca",
                "Categoría",
                "Ciudad",
                "Precio",
                "Score experto",
                "Predicción ML",
                "Nivel",
            ]
        )

    tabla = datos[
        [
            "nombre",
            "marca_normalizada",
            "categoria_normalizada",
            "ciudad",
            "precio_actual",
            "modapredict_score",
            "prediccion_ml",
            "nivel_recomendacion",
        ]
    ].copy()

    tabla["precio_actual"] = (
        pd.to_numeric(
            tabla["precio_actual"],
            errors="coerce",
        )
        .round(2)
    )

    tabla["modapredict_score"] = (
        pd.to_numeric(
            tabla["modapredict_score"],
            errors="coerce",
        )
        .round(2)
    )

    tabla["prediccion_ml"] = (
        pd.to_numeric(
            tabla["prediccion_ml"],
            errors="coerce",
        )
        .round(2)
    )

    return tabla.rename(
        columns={
            "nombre": "Producto",
            "marca_normalizada": "Marca",
            "categoria_normalizada": "Categoría",
            "ciudad": "Ciudad",
            "precio_actual": f"Precio ({MONEDA_BASE})",
            "modapredict_score": "Score experto",
            "prediccion_ml": "Predicción ML",
            "nivel_recomendacion": "Nivel",
        }
    )


def construir_html_productos(
    datos: pd.DataFrame,
) -> str:
    """Construye tarjetas visuales seguras para los productos."""

    if datos.empty:
        return """
        <div class="empty-state">
            <h3>No encontramos productos con esos filtros</h3>
            <p>
                Prueba cambiando la categoría, la ciudad
                o ampliando tu presupuesto.
            </p>
        </div>
        """

    tarjetas = []

    for _, fila in datos.iterrows():
        nombre = escape(
            str(fila.get("nombre", "Producto"))
        )

        marca = escape(
            str(
                fila.get(
                    "marca_normalizada",
                    "Sin marca",
                )
            )
        )

        categoria = escape(
            str(
                fila.get(
                    "categoria_normalizada",
                    "Sin categoría",
                )
            )
        )

        ciudad = escape(
            str(fila.get("ciudad", ""))
        )

        explicacion = escape(
            str(
                fila.get(
                    "explicacion_score",
                    "",
                )
            )
        )

        imagen_original = str(
            fila.get(
                "url_imagen",
                "",
            )
            or ""
        ).strip()

        enlace_original = str(
            fila.get(
                "url_producto",
                "#",
            )
            or "#"
        ).strip()

        imagen = escape(
            imagen_original,
            quote=True,
        )

        enlace = escape(
            enlace_original,
            quote=True,
        )

        precio = float(
            fila.get("precio_actual", 0) or 0
        )

        score = float(
            fila.get(
                "modapredict_score",
                0,
            ) or 0
        )
        oportunidad = interpretar_oportunidad(
            score=score,
            ciudad=ciudad,
)
        prediccion = float(
            fila.get(
                "prediccion_ml",
                0,
            ) or 0
        )

        nivel = escape(
            str(
                fila.get(
                    "nivel_recomendacion",
                    "",
                )
            )
        )

        imagen_html = ""

        if imagen_original:
            imagen_html = f"""
                <img
                    class="product-image"
                    src="{imagen}"
                    alt="{nombre}"
                    loading="lazy"
                />
            """

        enlace_html = ""

        if enlace_original and enlace_original != "#":
            enlace_html = f"""
                <a
                    class="product-link"
                    href="{enlace}"
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    Ver producto →
                </a>
            """

        tarjetas.append(
            f"""
            <article class="product-card">
                {imagen_html}

                <div class="product-body">
                    <span class="product-category">
                        {categoria} · {ciudad}
                    </span>

                    <h3 class="product-title">
                        {nombre}
                    </h3>

                    <p class="product-meta">
                        {marca} · ${precio:,.2f} {MONEDA_BASE}
                    </p>

                    <div class="
                        opportunity-box
                        {oportunidad["clase_css"]}
                    ">
                        <div class="opportunity-level">
                            {oportunidad["nivel"]}
                        </div>

                        <div class="opportunity-stars">
                            {oportunidad["estrellas"]}
                        </div>

                        <div class="opportunity-message">
                            {oportunidad["mensaje"]}
                        </div>
                    </div>

                    <p class="product-explanation">
                        {explicacion}
                    </p>

                    {enlace_html}
                </div>
            </article>
            """
        )

    return f"""
    <div class="products-grid">
        {''.join(tarjetas)}
    </div>
    """


# ==========================================================
# INFORMACIÓN DEL MODELO
# ==========================================================

def obtener_resumen_modelo() -> dict[str, Any]:
    """Devuelve información segura del modelo desplegado."""

    return {
        "modelo": METADATOS.get(
            "nombre_modelo",
            "HistGradientBoosting",
        ),
        "experimento": METADATOS.get(
            "experimento",
            "B",
        ),
        "variable_objetivo": METADATOS.get(
            "variable_objetivo",
            "modapredict_score",
        ),
        "registros": METADATOS.get(
            "registros_entrenamiento",
            0,
        ),
        "productos": METADATOS.get(
            "productos_unicos",
            0,
        ),
        "variables": METADATOS.get(
            "numero_variables",
            0,
        ),
        "advertencia": METADATOS.get(
            "advertencia",
            (
                "El modelo estima el ModaPredict Score. "
                "No predice ventas reales."
            ),
        ),
    }