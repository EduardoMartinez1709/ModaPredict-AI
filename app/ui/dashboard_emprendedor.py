"""
Pestaña del dashboard para emprendedores.
"""

from __future__ import annotations

from typing import Any

import gradio as gr

from app.componentes import construir_encabezado_seccion
from app.dashboards import generar_dashboard_emprendedor
from app.servicios import construir_html_productos
from app.ui.utilidades import construir_tabla_html


def actualizar_dashboard_emprendedor(
    ciudad: str,
    presupuesto: float,
) -> tuple[
    str,
    str,
    Any,
    Any,
    str,
    str,
]:
    """
    Genera todos los elementos del dashboard
    para emprendedores.
    """

    resultado = generar_dashboard_emprendedor(
        ciudad=ciudad,
        presupuesto=presupuesto,
    )

    tabla_html = construir_tabla_html(
        resultado["tabla_oportunidades"],
        mensaje_vacio=(
            "No encontramos oportunidades con esta combinación. "
            "Prueba otra ciudad o amplía tu presupuesto."
        ),
    )

    productos_html = construir_html_productos(
        resultado["productos"]
    )

    return (
        resultado["kpis"],
        tabla_html,
        resultado["grafica_categorias"],
        resultado["grafica_precios"],
        resultado["recomendacion"],
        productos_html,
    )


def construir_tab_dashboard_emprendedor(
    demo: gr.Blocks,
    ciudades: list[str],
) -> None:
    """
    Construye el dashboard para emprendedores,
    conecta sus eventos y carga el análisis inicial.
    """

    ciudades_disponibles = [
        ciudad
        for ciudad in ciudades
        if ciudad != "Todas"
    ]

    if not ciudades_disponibles:
        raise ValueError(
            "No existen ciudades disponibles para "
            "el Dashboard Emprendedor."
        )

    ciudad_inicial = (
        "Toluca"
        if "Toluca" in ciudades_disponibles
        else ciudades_disponibles[0]
    )

    with gr.Tab(
        "Dashboard Emprendedor",
        id="dashboard-emprendedor",
    ):
        gr.HTML(
            construir_encabezado_seccion(
                titulo="Decisiones claras para comenzar",
                subtitulo=(
                    "Identifica categorías, precios y productos "
                    "que podrían representar una mejor oportunidad."
                ),
                etiqueta="Perfil emprendedor",
            )
        )

        with gr.Row():
            ciudad_emprendedor = gr.Dropdown(
                choices=ciudades_disponibles,
                value=ciudad_inicial,
                label="Ciudad de interés",
            )

            presupuesto_emprendedor = gr.Number(
                value=15000,
                minimum=0,
                label="Presupuesto disponible (MXN)",
                info=(
                    "El presupuesto se captura en pesos mexicanos. "
                    "Los precios del catálogo se convierten desde USD "
                    "usando el tipo de cambio configurado."
                ),
            )

            boton_dashboard_emprendedor = gr.Button(
                "Actualizar análisis",
                variant="primary",
                elem_classes="primary-button",
            )

        kpis_emprendedor = gr.HTML()

        recomendacion_emprendedor = gr.Markdown()

        tabla_emprendedor = gr.HTML(
            value="""
            <div class="empty-state">
                <div class="empty-icon">📊</div>

                <h3>Preparando oportunidades</h3>

                <p>
                    El análisis por categoría aparecerá aquí.
                </p>
            </div>
            """
        )

        with gr.Row():
            grafica_categorias_emprendedor = gr.Plot(
                label="Categorías"
            )

            grafica_precios_emprendedor = gr.Plot(
                label="Precios"
            )

        gr.HTML(
            construir_encabezado_seccion(
                titulo="Productos para revisar",
                subtitulo=(
                    "Opciones destacadas de acuerdo con "
                    "la ciudad y el presupuesto."
                ),
            )
        )

        productos_emprendedor = gr.HTML()

        boton_dashboard_emprendedor.click(
            fn=actualizar_dashboard_emprendedor,
            inputs=[
                ciudad_emprendedor,
                presupuesto_emprendedor,
            ],
            outputs=[
                kpis_emprendedor,
                tabla_emprendedor,
                grafica_categorias_emprendedor,
                grafica_precios_emprendedor,
                recomendacion_emprendedor,
                productos_emprendedor,
            ],
        )

        demo.load(
            fn=actualizar_dashboard_emprendedor,
            inputs=[
                ciudad_emprendedor,
                presupuesto_emprendedor,
            ],
            outputs=[
                kpis_emprendedor,
                tabla_emprendedor,
                grafica_categorias_emprendedor,
                grafica_precios_emprendedor,
                recomendacion_emprendedor,
                productos_emprendedor,
            ],
            show_progress="hidden",
        )