"""
Pestaña conversacional de ModaPredict Advisor.
"""

from __future__ import annotations

import gradio as gr

from app.chat import (
    limpiar_memoria_chat,
    responder_chat,
)
from app.componentes import (
    construir_aviso_chat,
    construir_ejemplos_chat,
    construir_encabezado_seccion,
)


def enviar_mensaje_chat(
    mensaje: str,
    historial: list[dict] | None,
    perfil: str,
) -> tuple[str, list[dict]]:
    """
    Procesa un mensaje y actualiza el historial visible.
    """

    historial = historial or []

    mensaje = str(
        mensaje or ""
    ).strip()

    if not mensaje:
        return "", historial

    respuesta = responder_chat(
        mensaje=mensaje,
        historial=historial,
        perfil=perfil,
    )

    nuevo_historial = [
        *historial,
        {
            "role": "user",
            "content": mensaje,
        },
        {
            "role": "assistant",
            "content": respuesta,
        },
    ]

    return "", nuevo_historial


def limpiar_chat() -> tuple[str, list[dict]]:
    """
    Limpia la conversación visible y la memoria interna.
    """

    limpiar_memoria_chat()

    mensaje_bienvenida = {
        "role": "assistant",
        "content": (
            "¡Hola! Soy **ModaPredict Advisor** 👋\n\n"
            "La conversación anterior fue eliminada y "
            "podemos comenzar un análisis nuevo.\n\n"
            "Puedes decirme tu ciudad, presupuesto o qué "
            "tipo de productos te interesa vender."
        ),
    }

    return "", [mensaje_bienvenida]


def construir_tab_chat(
    perfil_global: gr.Radio,
) -> gr.HTML:
    """
    Construye la pestaña del Advisor y conecta sus eventos.

    Devuelve el componente de ejemplos para que pueda
    actualizarse al cambiar el perfil global.
    """

    with gr.Tab(
        "ModaPredict Advisor",
        id="chat",
    ):
        gr.HTML(
            construir_encabezado_seccion(
                titulo="ModaPredict Advisor",
                subtitulo=(
                    "Tu asesor especializado en decisiones "
                    "comerciales de moda."
                ),
                etiqueta="Chat conversacional",
            )
        )

        gr.HTML(
            construir_aviso_chat()
        )

        ejemplos_chat = gr.HTML(
            construir_ejemplos_chat(
                "Emprendedor"
            )
        )

        chatbot = gr.Chatbot(
            value=[
                {
                    "role": "assistant",
                    "content": (
                        "¡Hola! Soy **ModaPredict Advisor** 👋\n\n"
                        "Puedo ayudarte con productos, presupuestos, "
                        "tendencias, ciudades, clima y decisiones "
                        "comerciales de moda.\n\n"
                        "¿Qué te gustaría analizar?"
                    ),
                }
            ],
            label="Conversación",
            height=360,
            show_label=False,
            elem_classes="chatbot",
        )

        with gr.Row():
            mensaje_chat = gr.Textbox(
                placeholder=(
                    "Ejemplo: Tengo $15,000 para vender "
                    "ropa en Toluca..."
                ),
                label="Escribe tu pregunta",
                lines=2,
                scale=5,
            )

            boton_enviar = gr.Button(
                "Enviar",
                variant="primary",
                scale=1,
                elem_classes="primary-button",
            )

        boton_limpiar = gr.Button(
            "Limpiar conversación",
            variant="secondary",
            elem_classes="secondary-button",
        )

        boton_enviar.click(
            fn=enviar_mensaje_chat,
            inputs=[
                mensaje_chat,
                chatbot,
                perfil_global,
            ],
            outputs=[
                mensaje_chat,
                chatbot,
            ],
        )

        mensaje_chat.submit(
            fn=enviar_mensaje_chat,
            inputs=[
                mensaje_chat,
                chatbot,
                perfil_global,
            ],
            outputs=[
                mensaje_chat,
                chatbot,
            ],
        )

        boton_limpiar.click(
            fn=limpiar_chat,
            inputs=[],
            outputs=[
                mensaje_chat,
                chatbot,
            ],
            show_progress="hidden",
        )

    return ejemplos_chat