"""
Pestaña de inicio de ModaPredict AI.
"""

from __future__ import annotations

import gradio as gr

from app.componentes import (
    construir_advertencia_modelo,
    construir_encabezado_seccion,
    construir_escala_oportunidad,
    construir_explicacion_oportunidad,
)


def construir_tab_inicio(
    resumen_modelo: dict,
) -> None:
    """
    Construye la pestaña Inicio.

    Los componentes se crean directamente dentro
    del contexto de Gradio.
    """

    with gr.Tab(
        "Inicio",
        id="inicio",
    ):
        gr.HTML(
            construir_encabezado_seccion(
                titulo="Tu inteligencia comercial de moda",
                subtitulo=(
                    "Explora recomendaciones, tendencias, "
                    "dashboards y análisis respaldados por datos."
                ),
                etiqueta="ModaPredict AI",
            )
        )

        with gr.Row():
            with gr.Column(scale=1):
                gr.HTML(
                    construir_explicacion_oportunidad()
                )

            with gr.Column(scale=1):
                gr.HTML(
                    construir_escala_oportunidad()
                )

        gr.HTML(
            construir_advertencia_modelo(
                resumen_modelo["advertencia"]
            )
        )