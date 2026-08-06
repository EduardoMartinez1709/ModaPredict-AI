from __future__ import annotations

import gradio as gr

from app.componentes import (
    construir_bienvenida_perfil,
    construir_ejemplos_chat,
    construir_encabezado_seccion,
    construir_pie_pagina,
    construir_portada,
)
from app.estilos import CSS_PERSONALIZADO
from app.servicios import (
    obtener_opciones_interfaz,
    obtener_resumen_modelo,
)
from app.ui import (
    construir_tab_analitica_modelo,
    construir_tab_chat,
    construir_tab_dashboard_emprendedor,
    construir_tab_dashboard_empresa,
    construir_tab_inicio,
    construir_tab_recomendador,
)


# ==========================================================
# CONFIGURACIÓN GENERAL
# ==========================================================

OPCIONES = obtener_opciones_interfaz()
RESUMEN_MODELO = obtener_resumen_modelo()

CIUDADES = OPCIONES["ciudades"]
CATEGORIAS = OPCIONES["categorias"]
MARCAS = OPCIONES["marcas"]
FUENTES = OPCIONES["fuentes"]

PRECIO_MAXIMO_CATALOGO = max(
    1.0,
    float(
        OPCIONES["precio_maximo"]
    ),
)


# ==========================================================
# PERFIL GLOBAL
# ==========================================================

def actualizar_perfil(
    perfil: str,
) -> tuple[str, str]:
    """
    Actualiza la bienvenida y los ejemplos del chat
    según el perfil seleccionado.
    """

    perfil = (
        "Empresa"
        if perfil == "Empresa"
        else "Emprendedor"
    )

    bienvenida = construir_bienvenida_perfil(
        perfil
    )

    ejemplos = construir_ejemplos_chat(
        perfil
    )

    return bienvenida, ejemplos


# ==========================================================
# CONSTRUCCIÓN DE LA APP
# ==========================================================

def construir_app() -> gr.Blocks:
    """
    Construye la aplicación modular de ModaPredict AI.
    """

    tema = gr.themes.Base(
        primary_hue="amber",
        secondary_hue="slate",
        neutral_hue="slate",
    )

    with gr.Blocks(
        title="ModaPredict AI",
        theme=tema,
        css=CSS_PERSONALIZADO,
        analytics_enabled=False,
        fill_width=True,
    ) as demo:

        # ==================================================
        # PORTADA
        # ==================================================

        gr.HTML(
            construir_portada()
        )

        gr.HTML(
            construir_encabezado_seccion(
                titulo="Elige tu experiencia",
                subtitulo=(
                    "Personalizaremos la forma de mostrarte "
                    "recomendaciones, indicadores y análisis."
                ),
                etiqueta="Comienza aquí",
            )
        )

        perfil_global = gr.Radio(
            choices=[
                "Emprendedor",
                "Empresa",
            ],
            value="Emprendedor",
            label="¿Cómo usarás ModaPredict AI?",
            info=(
                "El perfil modifica el lenguaje y el "
                "nivel de detalle de la plataforma."
            ),
        )

        bienvenida_perfil = gr.HTML(
            construir_bienvenida_perfil(
                "Emprendedor"
            )
        )

        # ==================================================
        # PESTAÑAS
        # ==================================================

        with gr.Tabs():

            construir_tab_inicio(
                resumen_modelo=RESUMEN_MODELO,
            )

            construir_tab_recomendador(
                perfil_global=perfil_global,
                ciudades=CIUDADES,
                categorias=CATEGORIAS,
                marcas=MARCAS,
                fuentes=FUENTES,
                precio_maximo_catalogo=PRECIO_MAXIMO_CATALOGO,
            )

            ejemplos_chat = construir_tab_chat(
                perfil_global=perfil_global,
            )

            construir_tab_dashboard_emprendedor(
                demo=demo,
                ciudades=CIUDADES,
            )

            construir_tab_dashboard_empresa(
                demo=demo,
                ciudades=CIUDADES,
            )

            construir_tab_analitica_modelo(
                resumen_modelo=RESUMEN_MODELO,
            )

        gr.HTML(
            construir_pie_pagina()
        )

        # ==================================================
        # EVENTOS GLOBALES
        # ==================================================

        perfil_global.change(
            fn=actualizar_perfil,
            inputs=perfil_global,
            outputs=[
                bienvenida_perfil,
                ejemplos_chat,
            ],
            show_progress="hidden",
        )

    return demo


APP = construir_app()