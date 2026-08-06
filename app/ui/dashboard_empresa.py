"""
Pestaña del dashboard empresarial de ModaPredict AI.

Incluye:
- análisis ejecutivo del catálogo general;
- carga de Excel o CSV propio de una empresa;
- KPIs de inventario;
- alertas de reposición, sobrestock y margen;
- resumen ejecutivo basado en reglas de negocio.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import gradio as gr
import pandas as pd

from app.componentes import construir_encabezado_seccion
from app.dashboards import generar_dashboard_empresa
from app.empresa import analizar_archivo_empresa
from app.reportes import generar_reporte_empresa_pdf
from app.ui.utilidades import construir_tabla_html


# ==========================================================
# CONFIGURACIÓN
# ==========================================================

RUTA_PROYECTO = Path(__file__).resolve().parents[2]

RUTA_PLANTILLA_EMPRESA = (
    RUTA_PROYECTO
    / "plantillas"
    / "plantilla_inventario_empresa.xlsx"
)


# ==========================================================
# DASHBOARD GENERAL DEL CATÁLOGO
# ==========================================================

def actualizar_dashboard_empresa(
    ciudad: str,
) -> tuple[
    str,
    str,
    Any,
    Any,
    Any,
    str,
]:
    """
    Genera los elementos del dashboard ejecutivo
    usando el catálogo general de ModaPredict AI.
    """

    resultado = generar_dashboard_empresa(
        ciudad=ciudad,
    )

    tabla_html = construir_tabla_html(
        resultado["tabla_categorias"],
        mensaje_vacio=(
            "No existe información suficiente para "
            "esta cobertura geográfica."
        ),
    )

    return (
        resultado["kpis"],
        tabla_html,
        resultado["grafica_fuentes"],
        resultado["grafica_ciudades"],
        resultado["grafica_categorias"],
        resultado["resumen"],
    )


# ==========================================================
# ARCHIVO EMPRESARIAL
# ==========================================================

def obtener_ruta_archivo_subido(
    archivo: Any,
) -> str | None:
    """
    Obtiene una ruta válida desde el valor recibido
    por el componente gr.File.
    """

    if archivo is None:
        return None

    if isinstance(
        archivo,
        (
            str,
            Path,
        ),
    ):
        return str(
            archivo
        )

    if isinstance(
        archivo,
        dict,
    ):
        ruta = (
            archivo.get("path")
            or archivo.get("name")
        )

        return (
            str(ruta)
            if ruta
            else None
        )

    ruta = getattr(
        archivo,
        "name",
        None,
    )

    if ruta:
        return str(
            ruta
        )

    return None


def construir_diagnostico_archivo(
    diagnostico: dict[str, Any],
) -> str:
    """Genera un mensaje sobre la calidad del archivo."""

    filas = int(
        diagnostico.get(
            "filas",
            0,
        )
    )

    duplicados = int(
        diagnostico.get(
            "duplicados",
            0,
        )
    )

    columnas_adicionales = diagnostico.get(
        "columnas_no_reconocidas",
        [],
    )

    texto_columnas = ""

    if columnas_adicionales:
        columnas = ", ".join(
            map(
                str,
                columnas_adicionales,
            )
        )

        texto_columnas = (
            "\n\nSe conservaron columnas adicionales "
            f"no utilizadas en este análisis: `{columnas}`."
        )

    return (
        "### Archivo procesado correctamente ✅\n\n"
        f"- Registros recibidos: **{filas:,}**\n"
        f"- Filas duplicadas detectadas: **{duplicados:,}**"
        f"{texto_columnas}"
    )


def analizar_excel_empresa(
    archivo: Any,
) -> tuple[
    str,
    str,
    str,
    str,
]:
    """
    Analiza el archivo cargado por una empresa.

    Devuelve:
    - diagnóstico;
    - KPIs;
    - resumen ejecutivo;
    - tabla HTML de alertas.
    """

    ruta_archivo = obtener_ruta_archivo_subido(
        archivo
    )

    if not ruta_archivo:
        return (
            (
                "### Selecciona un archivo\n\n"
                "Carga un archivo `.xlsx`, `.xls` o `.csv` "
                "antes de ejecutar el análisis."
            ),
            "",
            "",
            construir_tabla_html(
                pd.DataFrame(),
                mensaje_vacio=(
                    "Carga un archivo empresarial para "
                    "consultar las alertas."
                ),
            ),
        )

    try:
        resultado = analizar_archivo_empresa(
            ruta_archivo
        )

        diagnostico_html = construir_diagnostico_archivo(
            resultado["diagnostico"]
        )

        tabla_alertas_html = construir_tabla_html(
            resultado["tabla_alertas"],
            mensaje_vacio=(
                "No se detectaron productos con alertas. "
                "El inventario se encuentra equilibrado "
                "según las reglas actuales."
            ),
        )

        return (
            diagnostico_html,
            resultado["kpis"],
            resultado["resumen_ejecutivo"],
            tabla_alertas_html,
        )

    except (
        FileNotFoundError,
        ValueError,
        KeyError,
        TypeError,
    ) as error:
        mensaje = str(
            error
        )

        return (
            (
                "### No fue posible analizar el archivo ⚠️\n\n"
                f"{mensaje}\n\n"
                "Revisa la plantilla y confirma que incluya "
                "las columnas obligatorias."
            ),
            "",
            "",
            construir_tabla_html(
                pd.DataFrame(),
                mensaje_vacio=(
                    "Corrige el archivo y vuelve a ejecutar "
                    "el análisis."
                ),
            ),
        )

    except Exception as error:
        return (
            (
                "### Ocurrió un error inesperado ⚠️\n\n"
                f"`{type(error).__name__}: {error}`"
            ),
            "",
            "",
            construir_tabla_html(
                pd.DataFrame(),
                mensaje_vacio=(
                    "No fue posible generar las alertas."
                ),
            ),
        )


# ==========================================================
# INTERFAZ
# ==========================================================
def generar_pdf_desde_archivo(
    archivo: Any,
    nombre_empresa: str,
) -> tuple[str | None, str]:
    """
    Analiza nuevamente el archivo y genera
    un reporte ejecutivo descargable.
    """

    ruta_archivo = obtener_ruta_archivo_subido(
        archivo
    )

    if not ruta_archivo:
        return (
            None,
            (
                "Primero carga un archivo de inventario "
                "antes de generar el reporte."
            ),
        )

    nombre_empresa = str(
        nombre_empresa or "Empresa"
    ).strip()

    try:
        resultado = analizar_archivo_empresa(
            ruta_archivo
        )

        ruta_pdf = generar_reporte_empresa_pdf(
            resumen=resultado["resumen"],
            resumen_ejecutivo=resultado[
                "resumen_ejecutivo"
            ],
            tabla_alertas=resultado[
                "tabla_alertas"
            ],
            nombre_empresa=nombre_empresa,
        )

        return (
            ruta_pdf,
            (
                "Reporte generado correctamente ✅\n\n"
                "Ya puedes descargarlo."
            ),
        )

    except Exception as error:
        return (
            None,
            (
                "No fue posible generar el reporte.\n\n"
                f"{type(error).__name__}: {error}"
            ),
        )


def construir_tab_dashboard_empresa(
    demo: gr.Blocks,
    ciudades: list[str],
) -> None:
    """
    Construye la pestaña empresarial completa,
    conecta sus eventos y carga el dashboard inicial.
    """

    with gr.Tab(
        "Dashboard Empresa",
        id="dashboard-empresa",
    ):
        gr.HTML(
            construir_encabezado_seccion(
                titulo="Visión ejecutiva del catálogo",
                subtitulo=(
                    "Analiza cobertura, categorías, fuentes "
                    "y oportunidades comerciales."
                ),
                etiqueta="Perfil empresa",
            )
        )

        # ==================================================
        # CATÁLOGO GENERAL
        # ==================================================

        with gr.Accordion(
            "Análisis del catálogo ModaPredict AI",
            open=True,
        ):
            with gr.Row():
                ciudad_empresa = gr.Dropdown(
                    choices=ciudades,
                    value=(
                        "Todas"
                        if "Todas" in ciudades
                        else ciudades[0]
                    ),
                    label="Cobertura geográfica",
                )

                boton_dashboard_empresa = gr.Button(
                    "Actualizar dashboard",
                    variant="primary",
                    elem_classes="primary-button",
                )

            kpis_empresa = gr.HTML()

            resumen_empresa = gr.Markdown()

            tabla_empresa = gr.HTML(
                value="""
                <div class="empty-state">
                    <div class="empty-icon">📊</div>

                    <h3>Preparando análisis ejecutivo</h3>

                    <p>
                        El resumen por categoría
                        aparecerá aquí.
                    </p>
                </div>
                """
            )

            with gr.Row():
                grafica_fuentes_empresa = gr.Plot(
                    label="Fuentes"
                )

                grafica_ciudades_empresa = gr.Plot(
                    label="Ciudades"
                )

            grafica_categorias_empresa = gr.Plot(
                label="Categorías"
            )

        # ==================================================
        # ARCHIVO PROPIO DE LA EMPRESA
        # ==================================================

        gr.HTML(
            construir_encabezado_seccion(
                titulo="Analiza tu propio inventario",
                subtitulo=(
                    "Carga un Excel o CSV para detectar "
                    "reposición, sobrestock, falta de movimiento "
                    "y problemas de margen."
                ),
                etiqueta="Inventario empresarial",
            )
        )

        with gr.Row():
            with gr.Column(
                scale=2,
                elem_classes="panel-premium",
            ):
                archivo_empresa = gr.File(
                    label="Archivo de inventario",
                    file_types=[
                        ".xlsx",
                        ".xls",
                        ".csv",
                    ],
                    type="filepath",
                )

                boton_analizar_empresa = gr.Button(
                    "Analizar inventario",
                    variant="primary",
                    elem_classes="primary-button",
                )

                nombre_empresa = gr.Textbox(
                    value="Empresa Demo",
                    label="Nombre de la empresa",
                    placeholder="Ejemplo: Boutique Lalo",
                )

                boton_generar_pdf = gr.Button(
                    "Generar reporte PDF",
                    variant="secondary",
                    elem_classes="secondary-button",
                )

            with gr.Column(
                scale=1,
                elem_classes="panel-premium",
            ):
                gr.HTML(
                    """
                    <div class="required-columns-box">
                        <h3>Columnas obligatorias</h3>

                        <div class="required-columns-grid">
                            <span>producto</span>
                            <span>categoria</span>
                            <span>marca</span>
                            <span>ciudad</span>
                            <span>precio_compra</span>
                            <span>precio_venta</span>
                            <span>stock</span>
                            <span>ventas_30_dias</span>
                        </div>
                    </div>
                    """
                )

                if RUTA_PLANTILLA_EMPRESA.exists():
                    gr.DownloadButton(
                        label="Descargar plantilla",
                        value=str(
                            RUTA_PLANTILLA_EMPRESA
                        ),
                        variant="secondary",
                        elem_classes="secondary-button",
                    )

                else:
                    gr.Markdown(
                        (
                            "La plantilla no está disponible en "
                            "`plantillas/plantilla_inventario_empresa.xlsx`."
                        )
                    )

        diagnostico_empresa_excel = gr.Markdown(
            value=(
                "Carga tu archivo y presiona "
                "**Analizar inventario**."
            )
        )

        estado_reporte_pdf = gr.Markdown(
            value=""
        )

        archivo_reporte_pdf = gr.File(
            label="Reporte ejecutivo PDF",
            interactive=False,
            visible=True,
        )

        kpis_empresa_excel = gr.HTML()

        resumen_empresa_excel = gr.Markdown()

        gr.HTML(
            construir_encabezado_seccion(
                titulo="Productos que requieren atención",
                subtitulo=(
                    "Alertas calculadas a partir de stock, ventas, "
                    "margen y cobertura estimada."
                ),
            )
        )

        tabla_alertas_empresa = gr.HTML(
            value="""
            <div class="empty-state">
                <div class="empty-icon">📦</div>

                <h3>Esperando un archivo</h3>

                <p>
                    Las alertas empresariales
                    aparecerán en esta sección.
                </p>
            </div>
            """
        )

        # ==================================================
        # EVENTOS
        # ==================================================

        boton_dashboard_empresa.click(
            fn=actualizar_dashboard_empresa,
            inputs=ciudad_empresa,
            outputs=[
                kpis_empresa,
                tabla_empresa,
                grafica_fuentes_empresa,
                grafica_ciudades_empresa,
                grafica_categorias_empresa,
                resumen_empresa,
            ],
        )

        boton_analizar_empresa.click(
            fn=analizar_excel_empresa,
            inputs=archivo_empresa,
            outputs=[
                diagnostico_empresa_excel,
                kpis_empresa_excel,
                resumen_empresa_excel,
                tabla_alertas_empresa,
            ],
        )

        boton_generar_pdf.click(
            fn=generar_pdf_desde_archivo,
            inputs=[
                archivo_empresa,
                nombre_empresa,
            ],
            outputs=[
                archivo_reporte_pdf,
                estado_reporte_pdf,
            ],
        )

        demo.load(
            fn=actualizar_dashboard_empresa,
            inputs=ciudad_empresa,
            outputs=[
                kpis_empresa,
                tabla_empresa,
                grafica_fuentes_empresa,
                grafica_ciudades_empresa,
                grafica_categorias_empresa,
                resumen_empresa,
            ],
            show_progress="hidden",
        )