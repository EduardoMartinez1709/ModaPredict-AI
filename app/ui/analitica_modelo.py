"""
Pestaña de analítica y transparencia del modelo.
"""

from __future__ import annotations

import gradio as gr

from app.componentes import (
    construir_advertencia_modelo,
    construir_encabezado_seccion,
    construir_metricas_modelo,
    construir_resumen_tecnico_modelo,
)
from app.ui.utilidades import obtener_ruta_grafica


def construir_tab_analitica_modelo(
    resumen_modelo: dict,
) -> None:
    """
    Construye la pestaña de analítica del modelo.
    """

    with gr.Tab(
        "Analítica del Modelo",
        id="analitica-modelo",
    ):
        gr.HTML(
            construir_encabezado_seccion(
                titulo="Transparencia del modelo",
                subtitulo=(
                    "Consulta el desempeño, las variables "
                    "más importantes y las principales "
                    "limitaciones metodológicas."
                ),
                etiqueta="Machine Learning",
            )
        )

        gr.HTML(
            construir_resumen_tecnico_modelo(
                resumen_modelo
            )
        )

        gr.HTML(
            construir_metricas_modelo()
        )

        gr.HTML(
            construir_advertencia_modelo(
                resumen_modelo["advertencia"]
            )
        )

        with gr.Row():
            gr.Image(
                value=obtener_ruta_grafica(
                    "01_comparacion_modelos_mae.png"
                ),
                label="Comparación de modelos",
                interactive=False,

            )

            gr.Image(
                value=obtener_ruta_grafica(
                    "02_prediccion_vs_real.png"
                ),
                label="Predicción frente al valor real",
                interactive=False,

            )

        with gr.Row():
            gr.Image(
                value=obtener_ruta_grafica(
                    "03_distribucion_residuos.png"
                ),
                label="Distribución de residuos",
                interactive=False,

            )

            gr.Image(
                value=obtener_ruta_grafica(
                    "04_importancia_variables.png"
                ),
                label="Importancia de variables",
                interactive=False,

            )

        with gr.Row():
            gr.Image(
                value=obtener_ruta_grafica(
                    "05_error_por_ciudad.png"
                ),
                label="Error por ciudad",
                interactive=False,

            )

            gr.Image(
                value=obtener_ruta_grafica(
                    "06_error_por_categoria.png"
                ),
                label="Error por categoría",
                interactive=False,

            )