"""
Clasificador de intenciones del usuario.
"""

from __future__ import annotations

from app.chat.extractores import (
    detectar_categoria,
    detectar_ciudades,
    detectar_marca,
    detectar_presupuesto,
    normalizar_texto,
)


# ==========================================================
# PALABRAS CLAVE
# ==========================================================

INTENCIONES = {

    "recomendar": [
        "que vender",
        "qué vender",
        "recomiend",
        "conviene",
        "oportunidad",
        "producto",
        "categoria",
        "categoría",
    ],

    "comparar": [
        "compar",
        "vs",
        "contra",
        "mejor",
    ],

    "precio": [
        "precio",
        "cost",
        "barato",
        "caro",
        "invert",
        "presupuesto",
    ],

    "explicar": [
        "por que",
        "por qué",
        "score",
        "prediccion",
        "predicción",
        "modelo",
        "ml",
        "machine learning",
    ],

    "principiante": [
        "estoy empezando",
        "soy nuevo",
        "no se que vender",
        "no sé qué vender",
        "quiero emprender",
        "quiero iniciar",
        "primera vez",
    ],

    "empresa": [
        "empresa",
        "inventario",
        "compras",
        "analisis",
        "análisis",
        "dashboard",
    ],
}


# ==========================================================
# CLASIFICADOR
# ==========================================================

def detectar_intencion(
    mensaje: str,
) -> dict:

    texto = normalizar_texto(mensaje)

    resultado = {

        "tipo": "general",

        "ciudades": detectar_ciudades(
            mensaje
        ),

        "categoria": detectar_categoria(
            mensaje
        ),

        "marca": detectar_marca(
            mensaje
        ),

        "presupuesto": detectar_presupuesto(
            mensaje
        ),
    }

    for nombre, palabras in INTENCIONES.items():

        for palabra in palabras:

            if normalizar_texto(
                palabra
            ) in texto:

                resultado["tipo"] = nombre

                return resultado

    if resultado["presupuesto"] is not None:

        resultado["tipo"] = "presupuesto"

    return resultado