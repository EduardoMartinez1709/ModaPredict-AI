"""
Control del dominio conversacional de ModaPredict AI.

Este módulo determina si un mensaje pertenece al alcance
del proyecto y genera una redirección amable cuando el
usuario pregunta sobre temas ajenos.
"""

from __future__ import annotations

from app.chat.extractores import (
    CATEGORIAS_DISPONIBLES,
    CIUDADES_DISPONIBLES,
    MARCAS_DISPONIBLES,
    normalizar_texto,
)


# ==========================================================
# VOCABULARIO DEL PROYECTO
# ==========================================================

PALABRAS_DOMINIO = {
    "moda",
    "ropa",
    "prenda",
    "prendas",
    "producto",
    "productos",
    "vender",
    "venta",
    "ventas",
    "comprar",
    "compra",
    "compras",
    "inventario",
    "stock",
    "precio",
    "precios",
    "presupuesto",
    "inversion",
    "invertir",
    "marca",
    "marcas",
    "categoria",
    "categorias",
    "tendencia",
    "tendencias",
    "google trends",
    "clima",
    "temperatura",
    "ciudad",
    "score",
    "modapredict",
    "oportunidad",
    "oportunidades",
    "recomendacion",
    "recomendaciones",
    "emprendedor",
    "empresa",
    "catalogo",
    "asos",
    "h&m",
    "modelo",
    "prediccion",
    "machine learning",
    "mae",
    "rmse",
    "r2",
    "dashboard",
    "margen",
    "rotacion",
    "proveedor",
    "distribuidora",
    "negocio",
    "comercial",
}


SALUDOS = {
    "hola",
    "holaa",
    "holaaa",
    "buenos dias",
    "buenas tardes",
    "buenas noches",
    "que tal",
    "hey",
    "ola",
}


DESPEDIDAS_Y_CORTESIA = {
    "gracias",
    "muchas gracias",
    "perfecto",
    "vale",
    "va",
    "vavava",
    "ok",
    "entendido",
    "listo",
    "adios",
    "hasta luego",
}


# ==========================================================
# VALIDACIÓN
# ==========================================================

def es_saludo_o_cortesia(
    mensaje: str,
) -> bool:
    """
    Permite saludos, agradecimientos y expresiones breves,
    aunque no contengan vocabulario comercial.
    """

    texto = normalizar_texto(mensaje)

    if not texto:
        return True

    expresiones = SALUDOS | DESPEDIDAS_Y_CORTESIA

    return any(
        texto == expresion
        or texto.startswith(f"{expresion} ")
        for expresion in expresiones
    )


def esta_dentro_del_dominio(
    mensaje: str,
    memoria: dict | None = None,
) -> bool:
    """
    Determina si el mensaje pertenece al alcance de
    ModaPredict AI.

    La memoria permite aceptar respuestas breves como:
    "Toluca", "15 mil" o "tenis", cuando el Advisor
    está esperando completar una consulta.
    """

    texto = normalizar_texto(mensaje)

    if not texto:
        return True

    if es_saludo_o_cortesia(mensaje):
        return True

    memoria = memoria or {}

    # Si existe una conversación activa, permitimos respuestas
    # cortas para completar ciudad, presupuesto o categoría.
    if memoria.get("esperando_dato"):
        return True

    if any(
        normalizar_texto(palabra) in texto
        for palabra in PALABRAS_DOMINIO
    ):
        return True

    if any(
        normalizar_texto(ciudad) in texto
        for ciudad in CIUDADES_DISPONIBLES
    ):
        return True

    if any(
        normalizar_texto(categoria) in texto
        for categoria in CATEGORIAS_DISPONIBLES
    ):
        return True

    if any(
        normalizar_texto(marca) in texto
        for marca in MARCAS_DISPONIBLES
    ):
        return True

    return False


# ==========================================================
# REDIRECCIÓN AMABLE
# ==========================================================

def respuesta_fuera_del_dominio(
    perfil: str = "Emprendedor",
    memoria: dict | None = None,
) -> str:
    """
    Redirige la conversación sin responder el tema ajeno.
    """

    memoria = memoria or {}

    ciudad = memoria.get("ciudad")
    categoria = memoria.get("categoria")

    sugerencia_contextual = ""

    if ciudad and categoria:
        sugerencia_contextual = (
            f"\n\nPodemos retomar el análisis de "
            f"**{categoria} en {ciudad}**."
        )
    elif ciudad:
        sugerencia_contextual = (
            f"\n\nPodemos continuar revisando oportunidades "
            f"para **{ciudad}**."
        )
    elif categoria:
        sugerencia_contextual = (
            f"\n\nPodemos seguir analizando la categoría "
            f"**{categoria}**."
        )

    if perfil == "Empresa":
        return (
            "Esa consulta se sale un poco del propósito de "
            "**ModaPredict Advisor** 🙂\n\n"
            "Mi función es apoyar decisiones comerciales de moda: "
            "inventario, categorías, ciudades, marcas, precios, "
            "tendencias, clima y desempeño del modelo."
            f"{sugerencia_contextual}\n\n"
            "También puedes pedirme que compare ciudades o que "
            "identifique las categorías con mejor oportunidad."
        )

    return (
        "Jajaja 😄, esa pregunta se sale un poquito de mi "
        "especialidad.\n\n"
        "Estoy aquí para ayudarte a decidir **qué vender, dónde "
        "venderlo y cómo aprovechar mejor tu presupuesto**, "
        "utilizando los datos de ModaPredict AI."
        f"{sugerencia_contextual}\n\n"
        "Podemos empezar con algo como: "
        "**“Tengo $15,000 para vender en Toluca”**."
    )