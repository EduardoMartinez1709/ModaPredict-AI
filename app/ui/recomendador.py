"""
Pestaña del recomendador comercial de ModaPredict AI.
"""

from __future__ import annotations

import gradio as gr
import pandas as pd

from app.componentes import construir_encabezado_seccion
from app.servicios import (
    construir_html_productos,
    construir_tabla_recomendaciones,
    obtener_recomendaciones,
)


def ejecutar_recomendador(
    perfil: str,
    ciudad: str,
    categoria: str,
    marca: str,
    fuente: str,
    precio_minimo: float,
    precio_maximo: float,
    cantidad: int,
) -> tuple[str, pd.DataFrame, str]:
    """
    Filtra el catálogo y genera las recomendaciones
    de acuerdo con el perfil seleccionado.
    """

    datos = obtener_recomendaciones(
        ciudad=ciudad,
        categoria=categoria,
        marca=marca,
        fuente=fuente,
        precio_minimo=precio_minimo,
        precio_maximo=precio_maximo,
        cantidad=cantidad,
    )

    productos_html = construir_html_productos(
        datos
    )

    tabla = construir_tabla_recomendaciones(
        datos
    )

    if datos.empty:
        resumen = (
            "No encontramos productos con esa combinación. "
            "Prueba ampliando el precio máximo o cambiando "
            "la categoría, marca o ciudad."
        )

        return (
            productos_html,
            tabla,
            resumen,
        )

    mejor = datos.iloc[0]

    if perfil == "Empresa":
        resumen = (
            f"Se encontraron **{len(datos)} productos**. "
            f"El mejor posicionado es "
            f"**{mejor['nombre']}**, con ModaPredict Score de "
            f"**{mejor['modapredict_score']:.2f}** y predicción "
            f"ML de **{mejor['prediccion_ml']:.2f}**.\n\n"
            "Antes de tomar una decisión de inventario, revisa "
            "margen, disponibilidad, logística y rotación."
        )

    else:
        resumen = (
            f"Encontré **{len(datos)} opciones** que pueden "
            f"interesarte. Yo empezaría revisando "
            f"**{mejor['nombre']}**, porque es el producto mejor "
            f"posicionado con los filtros seleccionados.\n\n"
            "Compara su precio, tallas y disponibilidad antes "
            "de tomar una decisión."
        )

    return (
        productos_html,
        tabla,
        resumen,
    )


def construir_tab_recomendador(
    perfil_global: gr.Radio,
    ciudades: list[str],
    categorias: list[str],
    marcas: list[str],
    fuentes: list[str],
    precio_maximo_catalogo: float,
) -> None:
    """
    Construye la pestaña completa del recomendador
    y conecta sus eventos.
    """

    with gr.Tab(
        "Recomendador",
        id="recomendador",
    ):
        gr.HTML(
            construir_encabezado_seccion(
                titulo="Encuentra oportunidades",
                subtitulo=(
                    "Filtra el catálogo y descubre los productos "
                    "mejor posicionados para cada ciudad."
                ),
                etiqueta="Recomendador comercial",
            )
        )

        with gr.Row():
            with gr.Column(
                scale=1,
                elem_classes="panel-premium",
            ):
                filtro_ciudad = gr.Dropdown(
                    choices=ciudades,
                    value=(
                        "Toluca"
                        if "Toluca" in ciudades
                        else ciudades[0]
                    ),
                    label="Ciudad",
                )

                filtro_categoria = gr.Dropdown(
                    choices=categorias,
                    value=(
                        "Todas"
                        if "Todas" in categorias
                        else categorias[0]
                    ),
                    label="Categoría",
                )

                filtro_marca = gr.Dropdown(
                    choices=marcas,
                    value=(
                        "Todas"
                        if "Todas" in marcas
                        else marcas[0]
                    ),
                    label="Marca",
                )

                filtro_fuente = gr.Dropdown(
                    choices=fuentes,
                    value=(
                        "Todas"
                        if "Todas" in fuentes
                        else fuentes[0]
                    ),
                    label="Fuente",
                )

                filtro_precio_minimo = gr.Number(
                    value=0,
                    minimum=0,
                    label="Precio mínimo por producto",
                    info="Precio del catálogo expresado en USD.",
                )

                filtro_precio_maximo = gr.Number(
                    value=precio_maximo_catalogo,
                    minimum=0,
                    label="Precio máximo por producto",
                    info="Precio del catálogo expresado en USD.",
                )

                filtro_cantidad = gr.Slider(
                    minimum=1,
                    maximum=20,
                    value=8,
                    step=1,
                    label="Número de recomendaciones",
                )

                boton_recomendar = gr.Button(
                    "Analizar oportunidades",
                    variant="primary",
                    elem_classes="primary-button",
                )

            with gr.Column(scale=2):
                resumen_recomendador = gr.Markdown(
                    value=(
                        "Configura los filtros y presiona "
                        "**Analizar oportunidades**."
                    )
                )

                productos_recomendados = gr.HTML(
                    value="""
                    <div class="empty-state recommender-empty-state">
                        <div class="empty-icon">✨</div>

                        <h3>Tu análisis aparecerá aquí</h3>

                        <p>
                            Selecciona una ciudad, categoría,
                            marca y rango de precio. Después
                            presiona
                            <strong>
                                Analizar oportunidades
                            </strong>.
                        </p>
                    </div>
                    """
                )

        with gr.Accordion(
            "Ver tabla técnica",
            open=False,
        ):
            tabla_recomendaciones = gr.Dataframe(
                interactive=False,
                wrap=True,
                label="Productos recomendados",
            )

        boton_recomendar.click(
            fn=ejecutar_recomendador,
            inputs=[
                perfil_global,
                filtro_ciudad,
                filtro_categoria,
                filtro_marca,
                filtro_fuente,
                filtro_precio_minimo,
                filtro_precio_maximo,
                filtro_cantidad,
            ],
            outputs=[
                productos_recomendados,
                tabla_recomendaciones,
                resumen_recomendador,
            ],
        )