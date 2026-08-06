from __future__ import annotations

from typing import Any

import matplotlib.pyplot as plt
import pandas as pd

from app.servicios import (
    TIPO_CAMBIO_USD_MXN,
    convertir_mxn_a_usd,
    filtrar_catalogo,
    interpretar_oportunidad,
    obtener_recomendaciones,
    resumen_para_empresa,
    resumen_para_emprendedor,
)


# ==========================================================
# PALETA Y ESTILO VISUAL
# ==========================================================

COLOR_FONDO = "#050505"
COLOR_PANEL = "#0f1014"
COLOR_TEXTO = "#f5f5f7"
COLOR_TEXTO_SUAVE = "#c8c9ce"
COLOR_DORADO = "#d6b36a"
COLOR_DORADO_CLARO = "#f3d995"
COLOR_PLATEADO = "#bfc2c9"
COLOR_REJILLA = "#2b2d33"
COLOR_BORDE = "#3a3c42"


def aplicar_estilo_figura(
    figura,
    eje,
    titulo: str,
    xlabel: str = "",
    ylabel: str = "",
) -> None:
    """Aplica el estilo visual general de ModaPredict AI."""

    figura.patch.set_facecolor(
        COLOR_FONDO
    )

    eje.set_facecolor(
        COLOR_PANEL
    )

    eje.set_title(
        titulo,
        color=COLOR_TEXTO,
        fontsize=15,
        fontweight="bold",
        pad=16,
    )

    eje.set_xlabel(
        xlabel,
        color=COLOR_TEXTO_SUAVE,
        fontsize=11,
        labelpad=10,
    )

    eje.set_ylabel(
        ylabel,
        color=COLOR_TEXTO_SUAVE,
        fontsize=11,
        labelpad=10,
    )

    eje.tick_params(
        axis="both",
        colors=COLOR_TEXTO_SUAVE,
        labelsize=10,
    )

    eje.grid(
        axis="x",
        color=COLOR_REJILLA,
        alpha=0.55,
        linewidth=0.8,
    )

    eje.set_axisbelow(
        True
    )

    for borde in eje.spines.values():
        borde.set_color(
            COLOR_BORDE
        )
        borde.set_linewidth(
            0.8
        )


def agregar_valores_barras_horizontales(
    eje,
    decimales: int = 1,
) -> None:
    """Añade etiquetas al final de las barras horizontales."""

    for barra in eje.patches:
        ancho = barra.get_width()

        eje.text(
            ancho,
            barra.get_y() + barra.get_height() / 2,
            f" {ancho:.{decimales}f}",
            va="center",
            ha="left",
            color=COLOR_TEXTO,
            fontsize=9,
            fontweight="bold",
        )


def agregar_valores_barras_verticales(
    eje,
    decimales: int = 0,
) -> None:
    """Añade etiquetas sobre las barras verticales."""

    for barra in eje.patches:
        altura = barra.get_height()

        eje.text(
            barra.get_x() + barra.get_width() / 2,
            altura,
            f"{altura:.{decimales}f}",
            va="bottom",
            ha="center",
            color=COLOR_TEXTO,
            fontsize=9,
            fontweight="bold",
        )


# ==========================================================
# FUNCIONES GENERALES
# ==========================================================

def figura_sin_datos(
    titulo: str,
):
    """Genera una figura elegante cuando no existen datos."""

    figura, eje = plt.subplots(
        figsize=(8, 4)
    )

    aplicar_estilo_figura(
        figura=figura,
        eje=eje,
        titulo=titulo,
    )

    eje.text(
        0.5,
        0.55,
        "No hay información disponible",
        ha="center",
        va="center",
        fontsize=15,
        fontweight="bold",
        color=COLOR_TEXTO,
        transform=eje.transAxes,
    )

    eje.text(
        0.5,
        0.42,
        "Prueba con otra selección o amplía los filtros.",
        ha="center",
        va="center",
        fontsize=10,
        color=COLOR_TEXTO_SUAVE,
        transform=eje.transAxes,
    )

    eje.axis(
        "off"
    )

    figura.tight_layout()

    return figura


def convertir_usd_a_mxn(
    cantidad_usd: float | None,
) -> float | None:
    """Convierte una cantidad del catálogo de USD a MXN."""

    if cantidad_usd is None:
        return None

    return float(cantidad_usd) * TIPO_CAMBIO_USD_MXN


def formatear_moneda(
    cantidad: float | None,
    moneda: str = "MXN",
) -> str:
    """Formatea una cantidad monetaria para la interfaz."""

    if cantidad is None:
        return "Sin definir"

    return f"${float(cantidad):,.2f} {moneda}"


def obtener_icono_oportunidad(
    score: float,
) -> str:
    """Devuelve un indicador visual según la oportunidad."""

    try:
        valor = float(
            score
        )
    except (TypeError, ValueError):
        valor = 0.0

    if valor >= 65:
        return "🟢"

    if valor >= 50:
        return "🟡"

    if valor >= 35:
        return "🟠"

    return "🔴"


# ==========================================================
# DASHBOARD PARA EMPRENDEDORES
# ==========================================================

def construir_kpis_emprendedor(
    ciudad: str,
    presupuesto: float | None,
) -> str:
    """Genera las tarjetas KPI del perfil Emprendedor."""

    resumen = resumen_para_emprendedor(
        ciudad=ciudad,
        presupuesto=presupuesto,
    )

    oportunidad = interpretar_oportunidad(
        score=resumen["score_promedio"],
        ciudad=ciudad,
    )

    precio_promedio_mxn = convertir_usd_a_mxn(
        resumen["precio_promedio"]
    )

    presupuesto_texto = formatear_moneda(
        presupuesto,
        moneda="MXN",
    )

    return f"""
    <div class="kpi-grid">

        <div class="kpi-card">
            <div class="kpi-label">Ciudad analizada</div>
            <div class="kpi-value">{resumen["ciudad"]}</div>
        </div>

        <div class="kpi-card">
            <div class="kpi-label">Productos disponibles</div>
            <div class="kpi-value">
                {resumen["productos_disponibles"]:,}
            </div>
        </div>

        <div class="kpi-card oportunidad-card">
            <div class="kpi-label">Oportunidad promedio</div>
            <div class="kpi-value kpi-text">
                {oportunidad["nivel"]}
            </div>
            <div class="kpi-stars">
                {oportunidad["estrellas"]}
            </div>
            <div class="kpi-subtitle">
                {oportunidad["mensaje"]}
            </div>
        </div>

        <div class="kpi-card">
            <div class="kpi-label">Categoría destacada</div>
            <div class="kpi-value kpi-text">
                {resumen["categoria_destacada"]}
            </div>
        </div>

        <div class="kpi-card">
            <div class="kpi-label">Precio promedio</div>
            <div class="kpi-value kpi-text">
                {formatear_moneda(
                    precio_promedio_mxn,
                    moneda="MXN",
                )}
            </div>
            <div class="kpi-subtitle">
                Precio original convertido desde USD
            </div>
        </div>

        <div class="kpi-card">
            <div class="kpi-label">Presupuesto</div>
            <div class="kpi-value kpi-text">
                {presupuesto_texto}
            </div>
        </div>

    </div>
    """


def tabla_oportunidades_emprendedor(
    ciudad: str,
    presupuesto: float | None = None,
) -> pd.DataFrame:
    """Genera la tabla principal del perfil Emprendedor."""

    presupuesto_usd = convertir_mxn_a_usd(
        presupuesto
    )

    datos = filtrar_catalogo(
        ciudad=ciudad,
        precio_maximo=presupuesto_usd,
    )

    if datos.empty:
        return pd.DataFrame(
            columns=[
                "Categoría",
                "Productos",
                "Oportunidad",
                "Precio promedio (MXN)",
                "Tendencia reciente",
            ]
        )

    tabla = (
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
            tendencia_reciente=(
                "interes_reciente",
                "mean",
            ),
        )
        .sort_values(
            "score_promedio",
            ascending=False,
        )
        .head(12)
    )

    tabla["precio_promedio"] = (
        tabla["precio_promedio"]
        .mul(TIPO_CAMBIO_USD_MXN)
        .round(2)
    )

    tabla["tendencia_reciente"] = (
        tabla["tendencia_reciente"]
        .round(2)
    )

    tabla["nivel_oportunidad"] = (
        tabla["score_promedio"]
        .apply(
            lambda valor: interpretar_oportunidad(
                valor
            )["nivel"]
        )
    )

    tabla["estrellas"] = (
        tabla["score_promedio"]
        .apply(
            lambda valor: interpretar_oportunidad(
                valor
            )["estrellas"]
        )
    )

    tabla["indicador_visual"] = (
        tabla.apply(
            lambda fila: (
                f"{obtener_icono_oportunidad(fila['score_promedio'])} "
                f"{fila['nivel_oportunidad']} "
                f"{fila['estrellas']}"
            ),
            axis=1,
        )
    )

    tabla = tabla.rename(
        columns={
            "categoria_normalizada": "Categoría",
            "productos": "Productos",
            "indicador_visual": "Oportunidad",
            "precio_promedio": "Precio promedio (MXN)",
            "tendencia_reciente": "Tendencia reciente",
        }
    )

    return tabla[
        [
            "Categoría",
            "Productos",
            "Oportunidad",
            "Precio promedio (MXN)",
            "Tendencia reciente",
        ]
    ]


def grafica_score_por_categoria_emprendedor(
    ciudad: str,
    presupuesto: float | None = None,
):
    """Grafica las categorías con mayor oportunidad."""

    presupuesto_usd = convertir_mxn_a_usd(
        presupuesto
    )

    datos = filtrar_catalogo(
        ciudad=ciudad,
        precio_maximo=presupuesto_usd,
    )

    if datos.empty:
        return figura_sin_datos(
            "Oportunidades por categoría"
        )

    tabla = (
        datos.groupby(
            "categoria_normalizada",
            as_index=False,
        )
        .agg(
            score_promedio=(
                "modapredict_score",
                "mean",
            )
        )
        .sort_values(
            "score_promedio",
            ascending=False,
        )
        .head(10)
        .sort_values(
            "score_promedio",
            ascending=True,
        )
    )

    figura, eje = plt.subplots(
        figsize=(9, 6)
    )

    eje.barh(
        tabla["categoria_normalizada"],
        tabla["score_promedio"],
        color=COLOR_DORADO,
        edgecolor=COLOR_DORADO_CLARO,
        linewidth=0.7,
    )

    aplicar_estilo_figura(
        figura=figura,
        eje=eje,
        titulo=(
            f"Categorías con mayor oportunidad en {ciudad}"
        ),
        xlabel="Nivel de oportunidad estimado",
        ylabel="Categoría",
    )

    eje.set_xlim(
        0,
        100,
    )

    agregar_valores_barras_horizontales(
        eje,
        decimales=1,
    )

    figura.tight_layout(
        pad=1.5
    )

    return figura


def grafica_precios_emprendedor(
    ciudad: str,
):
    """Muestra la distribución de precios disponibles."""

    datos = filtrar_catalogo(
        ciudad=ciudad,
    )

    if datos.empty:
        return figura_sin_datos(
            "Distribución de precios"
        )

    productos_unicos = (
        datos[
            [
                "id_unico",
                "precio_actual",
            ]
        ]
        .drop_duplicates(
            subset="id_unico"
        )
        .copy()
    )

    productos_unicos["precio_mxn"] = (
        productos_unicos["precio_actual"]
        * TIPO_CAMBIO_USD_MXN
    )

    figura, eje = plt.subplots(
        figsize=(9, 5)
    )

    eje.hist(
        productos_unicos["precio_mxn"].dropna(),
        bins=25,
        color=COLOR_DORADO,
        edgecolor=COLOR_DORADO_CLARO,
        linewidth=0.6,
        alpha=0.92,
    )

    aplicar_estilo_figura(
        figura=figura,
        eje=eje,
        titulo=f"Distribución de precios en {ciudad}",
        xlabel="Precio del producto (MXN)",
        ylabel="Número de productos",
    )

    figura.tight_layout(
        pad=1.5
    )

    return figura


def recomendacion_accionable_emprendedor(
    ciudad: str,
    presupuesto: float | None,
) -> str:
    """Genera un consejo simple y cercano."""

    resumen = resumen_para_emprendedor(
        ciudad=ciudad,
        presupuesto=presupuesto,
    )

    if resumen["productos_disponibles"] == 0:
        return (
            "No encontré suficientes productos para esta "
            "selección. Probemos con otra ciudad o ampliemos "
            "los filtros."
        )

    categoria = resumen[
        "categoria_destacada"
    ]

    precio_usd = resumen[
        "precio_promedio"
    ]

    precio_mxn = convertir_usd_a_mxn(
        precio_usd
    )

    texto = (
        f"Para {ciudad}, yo empezaría revisando productos de "
        f"la categoría **{categoria}**, porque actualmente "
        f"presenta la mejor señal promedio dentro del catálogo. "
        f"El precio medio ronda los "
        f"**{formatear_moneda(precio_mxn, moneda='MXN')}**."
    )

    if (
        presupuesto is not None
        and precio_mxn is not None
        and precio_mxn > 0
    ):
        unidades = int(
            float(presupuesto)
            // precio_mxn
        )

        texto += (
            f"\n\nCon un presupuesto de "
            f"**{formatear_moneda(presupuesto, moneda='MXN')}**, "
            f"podrías tomar como referencia aproximadamente "
            f"**{unidades} piezas**, antes de considerar "
            f"envíos, impuestos y margen de ganancia."
        )

    texto += (
        "\n\nLos precios originales del catálogo están en USD "
        f"y se convierten con un tipo de cambio de referencia de "
        f"**${TIPO_CAMBIO_USD_MXN:,.2f} MXN por USD**."
        "\n\nTómalo como punto de partida: conviene revisar "
        "también disponibilidad, margen y variedad de tallas."
    )

    return texto


def generar_dashboard_emprendedor(
    ciudad: str,
    presupuesto: float | None,
) -> dict[str, Any]:
    """Construye todo el dashboard de emprendedor."""

    presupuesto_usd = convertir_mxn_a_usd(
        presupuesto
    )

    recomendaciones = obtener_recomendaciones(
        ciudad=ciudad,
        precio_maximo=presupuesto_usd,
        cantidad=10,
    )

    return {
        "kpis": construir_kpis_emprendedor(
            ciudad=ciudad,
            presupuesto=presupuesto,
        ),
        "tabla_oportunidades": (
            tabla_oportunidades_emprendedor(
                ciudad=ciudad,
                presupuesto=presupuesto,
            )
        ),
        "grafica_categorias": (
            grafica_score_por_categoria_emprendedor(
                ciudad=ciudad,
                presupuesto=presupuesto,
            )
        ),
        "grafica_precios": (
            grafica_precios_emprendedor(
                ciudad=ciudad,
            )
        ),
        "recomendacion": (
            recomendacion_accionable_emprendedor(
                ciudad=ciudad,
                presupuesto=presupuesto,
            )
        ),
        "productos": recomendaciones,
    }


# ==========================================================
# DASHBOARD PARA EMPRESAS
# ==========================================================

def construir_kpis_empresa(
    ciudad: str = "Todas",
) -> str:
    """Genera KPIs ejecutivos para empresas."""

    resumen = resumen_para_empresa(
        ciudad=ciudad,
    )

    precio_promedio_mxn = convertir_usd_a_mxn(
        resumen["precio_promedio"]
    )

    return f"""
    <div class="kpi-grid">

        <div class="kpi-card">
            <div class="kpi-label">Productos únicos</div>
            <div class="kpi-value">
                {resumen["productos_unicos"]:,}
            </div>
        </div>

        <div class="kpi-card">
            <div class="kpi-label">Marcas analizadas</div>
            <div class="kpi-value">{resumen["marcas"]:,}</div>
        </div>

        <div class="kpi-card">
            <div class="kpi-label">Categorías</div>
            <div class="kpi-value">
                {resumen["categorias"]:,}
            </div>
        </div>

        <div class="kpi-card oportunidad-card">
            <div class="kpi-label">ModaPredict Score</div>
            <div class="kpi-value">
                {resumen["score_promedio"]:.2f}
            </div>
            <div class="kpi-subtitle">
                Indicador técnico promedio del catálogo
            </div>
        </div>

        <div class="kpi-card">
            <div class="kpi-label">Precio promedio</div>
            <div class="kpi-value kpi-text">
                {formatear_moneda(
                    precio_promedio_mxn,
                    moneda="MXN",
                )}
            </div>
        </div>

        <div class="kpi-card">
            <div class="kpi-label">Cobertura</div>
            <div class="kpi-value kpi-text">{ciudad}</div>
        </div>

    </div>
    """


def grafica_empresa_por_fuente(
    ciudad: str = "Todas",
):
    """Compara el número de productos por fuente."""

    resumen = resumen_para_empresa(
        ciudad=ciudad,
    )

    datos = resumen[
        "por_fuente"
    ]

    if datos.empty:
        return figura_sin_datos(
            "Catálogo por fuente"
        )

    figura, eje = plt.subplots(
        figsize=(8, 5)
    )

    eje.bar(
        datos["fuente"],
        datos["productos"],
        color=COLOR_DORADO,
        edgecolor=COLOR_DORADO_CLARO,
        linewidth=0.7,
    )

    aplicar_estilo_figura(
        figura=figura,
        eje=eje,
        titulo="Composición del catálogo por fuente",
        xlabel="Fuente",
        ylabel="Productos únicos",
    )

    agregar_valores_barras_verticales(
        eje,
        decimales=0,
    )

    figura.tight_layout(
        pad=1.5
    )

    return figura


def grafica_empresa_por_ciudad():
    """Compara el score promedio entre ciudades."""

    resumen = resumen_para_empresa(
        ciudad="Todas",
    )

    datos = (
        resumen["por_ciudad"]
        .sort_values(
            "score_promedio",
            ascending=True,
        )
    )

    if datos.empty:
        return figura_sin_datos(
            "Score por ciudad"
        )

    figura, eje = plt.subplots(
        figsize=(9, 6)
    )

    eje.barh(
        datos["ciudad"],
        datos["score_promedio"],
        color=COLOR_PLATEADO,
        edgecolor=COLOR_TEXTO,
        linewidth=0.5,
    )

    aplicar_estilo_figura(
        figura=figura,
        eje=eje,
        titulo="Oportunidad comercial promedio por ciudad",
        xlabel="ModaPredict Score promedio",
        ylabel="Ciudad",
    )

    eje.set_xlim(
        0,
        100,
    )

    agregar_valores_barras_horizontales(
        eje,
        decimales=1,
    )

    figura.tight_layout(
        pad=1.5
    )

    return figura


def grafica_empresa_categorias(
    ciudad: str = "Todas",
):
    """Muestra las categorías con mayor score promedio."""

    resumen = resumen_para_empresa(
        ciudad=ciudad,
    )

    datos = (
        resumen["por_categoria"]
        .head(12)
        .sort_values(
            "score_promedio",
            ascending=True,
        )
    )

    if datos.empty:
        return figura_sin_datos(
            "Score por categoría"
        )

    figura, eje = plt.subplots(
        figsize=(10, 7)
    )

    eje.barh(
        datos["categoria_normalizada"],
        datos["score_promedio"],
        color=COLOR_DORADO,
        edgecolor=COLOR_DORADO_CLARO,
        linewidth=0.7,
    )

    aplicar_estilo_figura(
        figura=figura,
        eje=eje,
        titulo=f"Categorías con mayor score — {ciudad}",
        xlabel="ModaPredict Score promedio",
        ylabel="Categoría",
    )

    eje.set_xlim(
        0,
        100,
    )

    agregar_valores_barras_horizontales(
        eje,
        decimales=1,
    )

    figura.tight_layout(
        pad=1.5
    )

    return figura


def tabla_empresa_categorias(
    ciudad: str = "Todas",
) -> pd.DataFrame:
    """Genera la tabla ejecutiva por categoría."""

    resumen = resumen_para_empresa(
        ciudad=ciudad,
    )

    tabla = resumen[
        "por_categoria"
    ].copy()

    if tabla.empty:
        return pd.DataFrame(
            columns=[
                "Categoría",
                "Productos",
                "Score promedio",
                "Precio promedio (MXN)",
            ]
        )

    tabla["score_promedio"] = (
        tabla["score_promedio"]
        .round(2)
    )

    tabla["precio_promedio"] = (
        tabla["precio_promedio"]
        .mul(TIPO_CAMBIO_USD_MXN)
        .round(2)
    )

    return tabla.rename(
        columns={
            "categoria_normalizada": "Categoría",
            "productos": "Productos",
            "score_promedio": "Score promedio",
            "precio_promedio": "Precio promedio (MXN)",
        }
    )


def resumen_ejecutivo_empresa(
    ciudad: str = "Todas",
) -> str:
    """Redacta una conclusión ejecutiva."""

    resumen = resumen_para_empresa(
        ciudad=ciudad,
    )

    categorias = resumen[
        "por_categoria"
    ]

    ciudades = resumen[
        "por_ciudad"
    ]

    if categorias.empty:
        return (
            "No existe información suficiente para construir "
            "el resumen ejecutivo."
        )

    mejor_categoria = categorias.iloc[0]

    mejor_ciudad = (
        ciudades.iloc[0]
        if not ciudades.empty
        else None
    )

    texto = (
        f"La categoría con mejor score promedio es "
        f"**{mejor_categoria['categoria_normalizada']}**, "
        f"con una puntuación media de "
        f"**{mejor_categoria['score_promedio']:.2f}**."
    )

    if mejor_ciudad is not None:
        texto += (
            f"\n\nLa ciudad con la mejor señal general es "
            f"**{mejor_ciudad['ciudad']}**, con un score "
            f"promedio de "
            f"**{mejor_ciudad['score_promedio']:.2f}**."
        )

    texto += (
        "\n\nAntes de modificar inventario o volumen de compra, "
        "se recomienda complementar el análisis con margen, "
        "rotación histórica, costos logísticos y disponibilidad."
    )

    return texto


def generar_dashboard_empresa(
    ciudad: str = "Todas",
) -> dict[str, Any]:
    """Construye el dashboard completo para empresa."""

    return {
        "kpis": construir_kpis_empresa(
            ciudad=ciudad,
        ),
        "tabla_categorias": (
            tabla_empresa_categorias(
                ciudad=ciudad,
            )
        ),
        "grafica_fuentes": (
            grafica_empresa_por_fuente(
                ciudad=ciudad,
            )
        ),
        "grafica_ciudades": (
            grafica_empresa_por_ciudad()
        ),
        "grafica_categorias": (
            grafica_empresa_categorias(
                ciudad=ciudad,
            )
        ),
        "resumen": (
            resumen_ejecutivo_empresa(
                ciudad=ciudad,
            )
        ),
    }