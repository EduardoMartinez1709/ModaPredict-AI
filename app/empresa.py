"""
Análisis empresarial de inventario para ModaPredict AI.

Este módulo permite:
- leer archivos Excel o CSV;
- validar una plantilla empresarial;
- limpiar y normalizar datos;
- calcular indicadores de margen, inventario y rotación;
- detectar productos que requieren atención;
- generar un resumen ejecutivo para la interfaz.

La primera versión utiliza reglas de negocio sobre información
propia de la empresa. No aplica automáticamente el modelo ML,
porque un archivo empresarial sencillo no contiene necesariamente
todas las variables con las que fue entrenado.
"""

from __future__ import annotations

import re
import unicodedata
from html import escape
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


# ==========================================================
# CONFIGURACIÓN
# ==========================================================

COLUMNAS_OBLIGATORIAS = [
    "producto",
    "categoria",
    "marca",
    "ciudad",
    "precio_compra",
    "precio_venta",
    "stock",
    "ventas_30_dias",
]

COLUMNAS_OPCIONALES = [
    "id_producto",
    "proveedor",
    "descuento_pct",
    "fecha_actualizacion",
]

ALIAS_COLUMNAS = {
    "nombre": "producto",
    "nombre_producto": "producto",
    "producto_nombre": "producto",
    "tipo_producto": "categoria",
    "categoría": "categoria",
    "brand": "marca",
    "ubicacion": "ciudad",
    "ubicación": "ciudad",
    "costo": "precio_compra",
    "costo_unitario": "precio_compra",
    "precio_costo": "precio_compra",
    "precio": "precio_venta",
    "precio_actual": "precio_venta",
    "existencias": "stock",
    "inventario": "stock",
    "unidades_stock": "stock",
    "ventas": "ventas_30_dias",
    "ventas_ultimo_mes": "ventas_30_dias",
    "ventas_mes": "ventas_30_dias",
}

COLUMNAS_NUMERICAS = [
    "precio_compra",
    "precio_venta",
    "stock",
    "ventas_30_dias",
    "descuento_pct",
]

ESTADOS_PRIORIDAD = [
    "Reponer de inmediato",
    "Reponer pronto",
    "Sin movimiento",
    "Sobrestock",
    "Margen bajo",
    "Inventario equilibrado",
]


# ==========================================================
# NORMALIZACIÓN
# ==========================================================

def normalizar_texto(
    texto: Any,
) -> str:
    """Normaliza texto para comparaciones y nombres de columnas."""

    valor = str(
        texto or ""
    ).strip().lower()

    valor = unicodedata.normalize(
        "NFKD",
        valor,
    )

    valor = "".join(
        caracter
        for caracter in valor
        if not unicodedata.combining(caracter)
    )

    valor = re.sub(
        r"[^a-z0-9]+",
        "_",
        valor,
    )

    return valor.strip("_")


def normalizar_columnas(
    datos: pd.DataFrame,
) -> pd.DataFrame:
    """Normaliza encabezados y aplica alias conocidos."""

    nuevo = datos.copy()

    columnas_normalizadas = []

    for columna in nuevo.columns:
        nombre = normalizar_texto(
            columna
        )

        nombre = ALIAS_COLUMNAS.get(
            nombre,
            nombre,
        )

        columnas_normalizadas.append(
            nombre
        )

    nuevo.columns = columnas_normalizadas

    return nuevo


def convertir_numero(
    serie: pd.Series,
) -> pd.Series:
    """
    Convierte texto monetario o numérico a float.

    Acepta símbolos, espacios y separadores comunes.
    """

    texto = (
        serie.astype(str)
        .str.strip()
        .str.replace(
            r"[$€£\s]",
            "",
            regex=True,
        )
        .str.replace(
            ",",
            "",
            regex=False,
        )
    )

    return pd.to_numeric(
        texto,
        errors="coerce",
    )


# ==========================================================
# LECTURA Y VALIDACIÓN
# ==========================================================

def leer_archivo_empresa(
    ruta_archivo: str | Path,
) -> pd.DataFrame:
    """Lee un archivo empresarial en formato XLSX, XLS o CSV."""

    ruta = Path(
        ruta_archivo
    )

    if not ruta.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo: {ruta}"
        )

    extension = ruta.suffix.lower()

    if extension in {
        ".xlsx",
        ".xls",
    }:
        libro = pd.ExcelFile(
            ruta
        )

        if not libro.sheet_names:
            raise ValueError(
                "El archivo de Excel no contiene hojas."
            )

        hoja_normalizada = {
            normalizar_texto(nombre): nombre
            for nombre in libro.sheet_names
        }

        hoja_inventario = hoja_normalizada.get(
            "inventario"
        )

        if hoja_inventario is None:
            # Si no existe una hoja llamada Inventario,
            # buscamos la primera hoja que contenga las
            # columnas obligatorias.
            for nombre_hoja in libro.sheet_names:
                muestra = pd.read_excel(
                    ruta,
                    sheet_name=nombre_hoja,
                    nrows=5,
                )

                muestra = normalizar_columnas(
                    muestra
                )

                if all(
                    columna in muestra.columns
                    for columna in COLUMNAS_OBLIGATORIAS
                ):
                    hoja_inventario = nombre_hoja
                    break

        if hoja_inventario is None:
            hojas = ", ".join(
                libro.sheet_names
            )

            raise ValueError(
                "No se encontró una hoja de inventario válida. "
                "La plantilla debe incluir una hoja llamada "
                "'Inventario' o una hoja con las columnas "
                "obligatorias. Hojas disponibles: "
                f"{hojas}"
            )

        datos = pd.read_excel(
            ruta,
            sheet_name=hoja_inventario,
        )

    elif extension == ".csv":
        datos = pd.read_csv(
            ruta
        )

    else:
        raise ValueError(
            "Formato no compatible. Utiliza XLSX, XLS o CSV."
        )

    if datos.empty:
        raise ValueError(
            "El archivo está vacío."
        )

    return normalizar_columnas(
        datos
    )


def validar_archivo_empresa(
    datos: pd.DataFrame,
) -> dict[str, Any]:
    """
    Valida estructura y calidad básica del archivo.

    Devuelve un diagnóstico; no modifica los datos.
    """

    columnas_faltantes = [
        columna
        for columna in COLUMNAS_OBLIGATORIAS
        if columna not in datos.columns
    ]

    columnas_reconocidas = [
        columna
        for columna in datos.columns
        if columna
        in (
            COLUMNAS_OBLIGATORIAS
            + COLUMNAS_OPCIONALES
        )
    ]

    columnas_no_reconocidas = [
        columna
        for columna in datos.columns
        if columna not in columnas_reconocidas
    ]

    duplicados = int(
        datos.duplicated().sum()
    )

    return {
        "es_valido": not columnas_faltantes,
        "columnas_faltantes": columnas_faltantes,
        "columnas_reconocidas": columnas_reconocidas,
        "columnas_no_reconocidas": columnas_no_reconocidas,
        "filas": int(
            len(datos)
        ),
        "duplicados": duplicados,
    }


def preparar_datos_empresa(
    datos: pd.DataFrame,
) -> pd.DataFrame:
    """Limpia los datos y calcula indicadores empresariales."""

    diagnostico = validar_archivo_empresa(
        datos
    )

    if not diagnostico["es_valido"]:
        faltantes = ", ".join(
            diagnostico["columnas_faltantes"]
        )

        raise ValueError(
            "Faltan columnas obligatorias: "
            f"{faltantes}"
        )

    nuevo = datos.copy()

    for columna in COLUMNAS_NUMERICAS:
        if columna in nuevo.columns:
            nuevo[columna] = convertir_numero(
                nuevo[columna]
            )

    columnas_texto = [
        "producto",
        "categoria",
        "marca",
        "ciudad",
    ]

    for columna in columnas_texto:
        nuevo[columna] = (
            nuevo[columna]
            .fillna("Sin información")
            .astype(str)
            .str.strip()
        )

    nuevo = nuevo.drop_duplicates(
        keep="first"
    ).copy()

    nuevo["precio_compra"] = (
        nuevo["precio_compra"]
        .fillna(0)
        .clip(lower=0)
    )

    nuevo["precio_venta"] = (
        nuevo["precio_venta"]
        .fillna(0)
        .clip(lower=0)
    )

    nuevo["stock"] = (
        nuevo["stock"]
        .fillna(0)
        .clip(lower=0)
        .round()
        .astype(int)
    )

    nuevo["ventas_30_dias"] = (
        nuevo["ventas_30_dias"]
        .fillna(0)
        .clip(lower=0)
        .round()
        .astype(int)
    )

    nuevo["margen_unitario"] = (
        nuevo["precio_venta"]
        - nuevo["precio_compra"]
    )

    nuevo["margen_pct"] = np.where(
        nuevo["precio_venta"] > 0,
        (
            nuevo["margen_unitario"]
            / nuevo["precio_venta"]
        )
        * 100,
        0,
    )

    nuevo["valor_inventario_costo"] = (
        nuevo["stock"]
        * nuevo["precio_compra"]
    )

    nuevo["valor_inventario_venta"] = (
        nuevo["stock"]
        * nuevo["precio_venta"]
    )

    nuevo["venta_diaria_estimada"] = (
        nuevo["ventas_30_dias"]
        / 30
    )

    nuevo["cobertura_dias"] = np.where(
        nuevo["venta_diaria_estimada"] > 0,
        (
            nuevo["stock"]
            / nuevo["venta_diaria_estimada"]
        ),
        np.where(
            nuevo["stock"] > 0,
            999,
            0,
        ),
    )

    nuevo["rotacion_30_dias"] = np.where(
        nuevo["stock"] > 0,
        nuevo["ventas_30_dias"]
        / nuevo["stock"],
        np.where(
            nuevo["ventas_30_dias"] > 0,
            np.inf,
            0,
        ),
    )

    nuevo["estado_inventario"] = nuevo.apply(
        clasificar_estado_producto,
        axis=1,
    )

    nuevo["prioridad"] = nuevo[
        "estado_inventario"
    ].map(
        {
            "Reponer de inmediato": 1,
            "Reponer pronto": 2,
            "Sin movimiento": 3,
            "Sobrestock": 4,
            "Margen bajo": 5,
            "Inventario equilibrado": 6,
        }
    ).fillna(99)

    return nuevo


# ==========================================================
# REGLAS DE NEGOCIO
# ==========================================================

def clasificar_estado_producto(
    fila: pd.Series,
) -> str:
    """Clasifica la situación comercial de cada producto."""

    stock = float(
        fila.get(
            "stock",
            0,
        )
    )

    ventas = float(
        fila.get(
            "ventas_30_dias",
            0,
        )
    )

    cobertura = float(
        fila.get(
            "cobertura_dias",
            0,
        )
    )

    margen_pct = float(
        fila.get(
            "margen_pct",
            0,
        )
    )

    if stock <= 0 and ventas > 0:
        return "Reponer de inmediato"

    if (
        ventas > 0
        and cobertura < 15
    ):
        return "Reponer pronto"

    if (
        stock > 0
        and ventas <= 0
    ):
        return "Sin movimiento"

    if cobertura > 90:
        return "Sobrestock"

    if margen_pct < 20:
        return "Margen bajo"

    return "Inventario equilibrado"


# ==========================================================
# INDICADORES Y TABLAS
# ==========================================================

def generar_resumen_empresa(
    datos: pd.DataFrame,
) -> dict[str, Any]:
    """Calcula los principales indicadores empresariales."""

    if datos.empty:
        return {
            "productos": 0,
            "stock_total": 0,
            "ventas_30_dias": 0,
            "valor_inventario_costo": 0,
            "valor_inventario_venta": 0,
            "margen_promedio_pct": 0,
            "productos_alerta": 0,
            "ciudades": 0,
        }

    estados_alerta = {
        "Reponer de inmediato",
        "Reponer pronto",
        "Sin movimiento",
        "Sobrestock",
        "Margen bajo",
    }

    productos_alerta = datos[
        "estado_inventario"
    ].isin(
        estados_alerta
    )

    return {
        "productos": int(
            len(datos)
        ),
        "stock_total": int(
            datos["stock"].sum()
        ),
        "ventas_30_dias": int(
            datos["ventas_30_dias"].sum()
        ),
        "valor_inventario_costo": round(
            float(
                datos[
                    "valor_inventario_costo"
                ].sum()
            ),
            2,
        ),
        "valor_inventario_venta": round(
            float(
                datos[
                    "valor_inventario_venta"
                ].sum()
            ),
            2,
        ),
        "margen_promedio_pct": round(
            float(
                datos["margen_pct"].mean()
            ),
            2,
        ),
        "productos_alerta": int(
            productos_alerta.sum()
        ),
        "ciudades": int(
            datos["ciudad"].nunique()
        ),
    }


def construir_kpis_empresa_excel(
    resumen: dict[str, Any],
) -> str:
    """Construye KPIs HTML para el análisis del Excel."""

    return f"""
    <div class="kpi-grid">

        <div class="kpi-card">
            <div class="kpi-label">Productos analizados</div>
            <div class="kpi-value">{resumen["productos"]:,}</div>
        </div>

        <div class="kpi-card">
            <div class="kpi-label">Stock total</div>
            <div class="kpi-value">{resumen["stock_total"]:,}</div>
        </div>

        <div class="kpi-card">
            <div class="kpi-label">Ventas últimos 30 días</div>
            <div class="kpi-value">{resumen["ventas_30_dias"]:,}</div>
        </div>

        <div class="kpi-card oportunidad-card">
            <div class="kpi-label">Productos con alerta</div>
            <div class="kpi-value">{resumen["productos_alerta"]:,}</div>
            <div class="kpi-subtitle">
                Reposición, baja rotación, sobrestock o margen bajo
            </div>
        </div>

        <div class="kpi-card">
            <div class="kpi-label">Inventario a costo</div>
            <div class="kpi-value kpi-text">
                ${resumen["valor_inventario_costo"]:,.2f}
            </div>
        </div>

        <div class="kpi-card">
            <div class="kpi-label">Margen promedio</div>
            <div class="kpi-value kpi-text">
                {resumen["margen_promedio_pct"]:.1f}%
            </div>
        </div>

    </div>
    """


def construir_tabla_alertas(
    datos: pd.DataFrame,
    limite: int = 25,
) -> pd.DataFrame:
    """Devuelve los productos que requieren mayor atención."""

    columnas = [
        "Producto",
        "Categoría",
        "Marca",
        "Ciudad",
        "Stock",
        "Ventas 30 días",
        "Margen %",
        "Cobertura días",
        "Estado",
    ]

    if datos.empty:
        return pd.DataFrame(
            columns=columnas
        )

    alertas = datos.loc[
        datos["estado_inventario"]
        .ne("Inventario equilibrado")
    ].copy()

    if alertas.empty:
        return pd.DataFrame(
            columns=columnas
        )

    alertas = (
        alertas.sort_values(
            [
                "prioridad",
                "ventas_30_dias",
                "stock",
            ],
            ascending=[
                True,
                False,
                False,
            ],
        )
        .head(
            max(
                1,
                int(limite),
            )
        )
    )

    tabla = alertas[
        [
            "producto",
            "categoria",
            "marca",
            "ciudad",
            "stock",
            "ventas_30_dias",
            "margen_pct",
            "cobertura_dias",
            "estado_inventario",
        ]
    ].copy()

    tabla["margen_pct"] = (
        tabla["margen_pct"]
        .round(1)
    )

    tabla["cobertura_dias"] = (
        tabla["cobertura_dias"]
        .replace(
            999,
            np.nan,
        )
        .round(1)
    )

    return tabla.rename(
        columns={
            "producto": "Producto",
            "categoria": "Categoría",
            "marca": "Marca",
            "ciudad": "Ciudad",
            "stock": "Stock",
            "ventas_30_dias": "Ventas 30 días",
            "margen_pct": "Margen %",
            "cobertura_dias": "Cobertura días",
            "estado_inventario": "Estado",
        }
    )


def construir_resumen_ejecutivo(
    datos: pd.DataFrame,
    resumen: dict[str, Any],
) -> str:
    """Genera recomendaciones ejecutivas a partir del archivo."""

    if datos.empty:
        return (
            "No fue posible construir el análisis porque "
            "el archivo no contiene registros válidos."
        )

    conteo_estados = (
        datos["estado_inventario"]
        .value_counts()
        .to_dict()
    )

    reponer = (
        conteo_estados.get(
            "Reponer de inmediato",
            0,
        )
        + conteo_estados.get(
            "Reponer pronto",
            0,
        )
    )

    sin_movimiento = conteo_estados.get(
        "Sin movimiento",
        0,
    )

    sobrestock = conteo_estados.get(
        "Sobrestock",
        0,
    )

    margen_bajo = conteo_estados.get(
        "Margen bajo",
        0,
    )

    categorias = (
        datos.groupby(
            "categoria",
            as_index=False,
        )
        .agg(
            ventas=(
                "ventas_30_dias",
                "sum",
            ),
            margen_promedio=(
                "margen_pct",
                "mean",
            ),
        )
        .sort_values(
            "ventas",
            ascending=False,
        )
    )

    categoria_lider = (
        categorias.iloc[0]["categoria"]
        if not categorias.empty
        else "Sin información"
    )

    recomendaciones = [
        (
            f"Se analizaron **{resumen['productos']:,} productos** "
            f"con un inventario total de "
            f"**{resumen['stock_total']:,} unidades**."
        ),
        (
            f"La categoría con más ventas en los últimos 30 días "
            f"es **{categoria_lider}**."
        ),
    ]

    if reponer:
        recomendaciones.append(
            f"Hay **{reponer} productos** que requieren "
            "reposición inmediata o próxima."
        )

    if sin_movimiento:
        recomendaciones.append(
            f"Se detectaron **{sin_movimiento} productos sin "
            "movimiento**; conviene revisar promociones, precio "
            "o continuidad en el catálogo."
        )

    if sobrestock:
        recomendaciones.append(
            f"Existen **{sobrestock} productos con sobrestock**; "
            "pueden priorizarse en liquidaciones o campañas."
        )

    if margen_bajo:
        recomendaciones.append(
            f"Hay **{margen_bajo} productos con margen inferior "
            "al 20%**; conviene negociar costo o ajustar precio."
        )

    recomendaciones.append(
        "Estas conclusiones provienen de reglas de inventario, "
        "ventas y margen. No representan todavía una predicción "
        "del modelo ML de ModaPredict AI."
    )

    return "\n\n".join(
        recomendaciones
    )


# ==========================================================
# ORQUESTADOR
# ==========================================================

def analizar_archivo_empresa(
    ruta_archivo: str | Path,
) -> dict[str, Any]:
    """
    Ejecuta el flujo completo de análisis empresarial.

    Retorna elementos listos para conectar con Gradio.
    """

    datos_originales = leer_archivo_empresa(
        ruta_archivo
    )

    diagnostico = validar_archivo_empresa(
        datos_originales
    )

    datos = preparar_datos_empresa(
        datos_originales
    )

    resumen = generar_resumen_empresa(
        datos
    )

    return {
        "diagnostico": diagnostico,
        "datos_procesados": datos,
        "resumen": resumen,
        "kpis": construir_kpis_empresa_excel(
            resumen
        ),
        "tabla_alertas": construir_tabla_alertas(
            datos
        ),
        "resumen_ejecutivo": construir_resumen_ejecutivo(
            datos=datos,
            resumen=resumen,
        ),
    }