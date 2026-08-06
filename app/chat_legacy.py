from __future__ import annotations

import re
import unicodedata
from typing import Any

import pandas as pd

from app.servicios import (
    CATALOGO,
    comparar_ciudades,
    obtener_recomendaciones,
    resumen_para_empresa,
    resumen_para_emprendedor,
)


# ==========================================================
# CONFIGURACIÓN DEL DOMINIO
# ==========================================================

CIUDADES_DISPONIBLES = sorted(
    CATALOGO["ciudad"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

CATEGORIAS_DISPONIBLES = sorted(
    CATALOGO["categoria_normalizada"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

MARCAS_DISPONIBLES = sorted(
    CATALOGO["marca_normalizada"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

PALABRAS_DOMINIO = {
    "moda",
    "ropa",
    "producto",
    "productos",
    "vender",
    "venta",
    "comprar",
    "compra",
    "inventario",
    "precio",
    "precios",
    "presupuesto",
    "marca",
    "marcas",
    "categoria",
    "categorias",
    "tendencia",
    "tendencias",
    "google trends",
    "clima",
    "ciudad",
    "score",
    "modapredict",
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
}


# ==========================================================
# NORMALIZACIÓN DE TEXTO
# ==========================================================

def normalizar_texto(texto: str) -> str:
    """Convierte el texto a una forma comparable."""

    texto = str(texto or "").lower().strip()

    texto = unicodedata.normalize(
        "NFKD",
        texto,
    )

    texto = "".join(
        caracter
        for caracter in texto
        if not unicodedata.combining(caracter)
    )

    texto = re.sub(
        r"[^a-z0-9$.,\s&]",
        " ",
        texto,
    )

    texto = re.sub(
        r"\s+",
        " ",
        texto,
    ).strip()

    return texto


# ==========================================================
# VALIDACIÓN DEL ALCANCE
# ==========================================================

def esta_dentro_del_alcance(
    mensaje: str,
) -> bool:
    """
    Comprueba si la consulta pertenece al dominio
    de ModaPredict AI.
    """

    texto = normalizar_texto(mensaje)

    if not texto:
        return True

    for palabra in PALABRAS_DOMINIO:
        if normalizar_texto(palabra) in texto:
            return True

    for ciudad in CIUDADES_DISPONIBLES:
        if normalizar_texto(ciudad) in texto:
            return True

    for categoria in CATEGORIAS_DISPONIBLES:
        if normalizar_texto(categoria) in texto:
            return True

    for marca in MARCAS_DISPONIBLES:
        if normalizar_texto(marca) in texto:
            return True

    return False


def respuesta_fuera_de_alcance(
    perfil: str,
) -> str:
    """
    Devuelve una redirección amable cuando la pregunta
    no corresponde al propósito del chat.
    """

    if perfil == "Empresa":
        return (
            "Esa consulta se sale un poco del objetivo de "
            "ModaPredict AI. Este asistente está diseñado "
            "para apoyar decisiones comerciales de moda, "
            "como analizar categorías, ciudades, precios, "
            "tendencias, marcas y oportunidades de inventario.\n\n"
            "Podemos continuar con algo como:\n"
            "• comparar dos ciudades;\n"
            "• revisar las categorías con mejor score;\n"
            "• analizar marcas o rangos de precio;\n"
            "• consultar indicadores del modelo.\n\n"
            "¿Qué aspecto comercial te gustaría revisar?"
        )

    return (
        "Creo que esa pregunta se sale un poquito del objetivo "
        "de ModaPredict AI 😄\n\n"
        "Este chat está pensado para ayudarte con productos "
        "de moda, precios, tendencias, ciudades, clima y "
        "decisiones de compra.\n\n"
        "Puedo ayudarte, por ejemplo, a:\n"
        "• encontrar qué vender en Toluca;\n"
        "• comparar categorías;\n"
        "• armar opciones según tu presupuesto;\n"
        "• explicar por qué un producto tiene buen score.\n\n"
        "¿Qué te gustaría analizar?"
    )


# ==========================================================
# EXTRACCIÓN DE PARÁMETROS
# ==========================================================

def detectar_ciudades(
    mensaje: str,
) -> list[str]:
    """Encuentra ciudades mencionadas en el mensaje."""

    texto = normalizar_texto(mensaje)

    ciudades = []

    for ciudad in CIUDADES_DISPONIBLES:
        if normalizar_texto(ciudad) in texto:
            ciudades.append(ciudad)

    return ciudades


def detectar_categoria(
    mensaje: str,
) -> str | None:
    """Encuentra una categoría mencionada."""

    texto = normalizar_texto(mensaje)

    for categoria in CATEGORIAS_DISPONIBLES:
        if normalizar_texto(categoria) in texto:
            return categoria

    return None


def detectar_marca(
    mensaje: str,
) -> str | None:
    """Encuentra una marca mencionada."""

    texto = normalizar_texto(mensaje)

    for marca in MARCAS_DISPONIBLES:
        if normalizar_texto(marca) in texto:
            return marca

    return None


def detectar_presupuesto(
    mensaje: str,
) -> float | None:
    """
    Extrae una cantidad monetaria sencilla.

    Ejemplos:
        15000
        $15,000
        15 mil
    """

    texto = normalizar_texto(mensaje)

    coincidencia_mil = re.search(
        r"(\d+(?:[.,]\d+)?)\s*mil",
        texto,
    )

    if coincidencia_mil:
        numero = coincidencia_mil.group(1)
        numero = numero.replace(",", ".")
        return float(numero) * 1000

    coincidencia = re.search(
        r"\$?\s*(\d[\d,]*(?:\.\d+)?)",
        texto,
    )

    if not coincidencia:
        return None

    numero = coincidencia.group(1)
    numero = numero.replace(",", "")

    try:
        return float(numero)
    except ValueError:
        return None


# ==========================================================
# DETECCIÓN DE INTENCIÓN
# ==========================================================

def detectar_intencion(
    mensaje: str,
) -> str:
    """Clasifica la intención principal del usuario."""

    texto = normalizar_texto(mensaje)

    if any(
        expresion in texto
        for expresion in [
            "compara",
            "comparar",
            "diferencia entre",
            "que conviene mas",
            "cual es mejor",
        ]
    ):
        return "comparacion"

    if any(
        expresion in texto
        for expresion in [
            "presupuesto",
            "tengo $",
            "tengo ",
            "cuanto comprar",
            "invertir",
        ]
    ):
        return "presupuesto"

    if any(
        expresion in texto
        for expresion in [
            "por que",
            "explica",
            "score",
            "prediccion",
        ]
    ):
        return "explicacion"

    if any(
        expresion in texto
        for expresion in [
            "tendencia",
            "google trends",
            "esta de moda",
        ]
    ):
        return "tendencias"

    if any(
        expresion in texto
        for expresion in [
            "modelo",
            "mae",
            "rmse",
            "r2",
            "machine learning",
        ]
    ):
        return "modelo"

    if any(
        expresion in texto
        for expresion in [
            "que vender",
            "que comprar",
            "recomienda",
            "recomendacion",
            "me conviene",
        ]
    ):
        return "recomendacion"

    return "consulta_general"


# ==========================================================
# RESPUESTAS DE NEGOCIO
# ==========================================================

def responder_recomendacion(
    mensaje: str,
    perfil: str,
) -> str:
    ciudades = detectar_ciudades(mensaje)
    categoria = detectar_categoria(mensaje)
    marca = detectar_marca(mensaje)

    ciudad = (
        ciudades[0]
        if ciudades
        else "Todas"
    )

    datos = obtener_recomendaciones(
        ciudad=ciudad,
        categoria=categoria or "Todas",
        marca=marca or "Todas",
        cantidad=5,
    )

    if datos.empty:
        return (
            "No encontré productos que coincidan con esa "
            "combinación. Podemos probar con otra ciudad, "
            "categoría o marca."
        )

    top = datos.iloc[0]

    if perfil == "Empresa":
        return (
            f"El mejor escenario encontrado corresponde a "
            f"{top['categoria_normalizada']} en {top['ciudad']}. "
            f"El producto con mayor puntuación es "
            f"“{top['nombre']}”, con un ModaPredict Score de "
            f"{top['modapredict_score']:.1f} y una predicción "
            f"del modelo de {top['prediccion_ml']:.1f}.\n\n"
            f"También se recomienda revisar las primeras cinco "
            f"opciones del ranking para evaluar margen, stock "
            f"y capacidad de compra."
        )

    return (
        f"¡Va! Encontré una buena oportunidad en "
        f"{top['categoria_normalizada']} para {top['ciudad']}.\n\n"
        f"El producto mejor posicionado es "
        f"“{top['nombre']}”, con un score de "
        f"{top['modapredict_score']:.1f}.\n\n"
        f"Yo empezaría revisando las primeras cinco opciones "
        f"y compararía precio, margen y disponibilidad antes "
        f"de comprar."
    )


def responder_presupuesto(
    mensaje: str,
    perfil: str,
) -> str:
    ciudades = detectar_ciudades(mensaje)
    presupuesto = detectar_presupuesto(mensaje)

    ciudad = (
        ciudades[0]
        if ciudades
        else "Todas"
    )

    if presupuesto is None:
        return (
            "Claro. Dime aproximadamente cuánto quieres "
            "invertir y en qué ciudad deseas vender. "
            "Por ejemplo: “Tengo $15,000 para vender en Toluca”."
        )

    resumen = resumen_para_emprendedor(
        ciudad=ciudad,
        presupuesto=presupuesto,
    )

    categoria = resumen[
        "categoria_destacada"
    ]

    precio_promedio = resumen[
        "precio_promedio"
    ]

    if precio_promedio > 0:
        unidades_estimadas = int(
            presupuesto // precio_promedio
        )
    else:
        unidades_estimadas = 0

    if perfil == "Empresa":
        return (
            f"Con un presupuesto de ${presupuesto:,.2f}, "
            f"la categoría con mejor score promedio en "
            f"{ciudad} es {categoria}. El precio promedio del "
            f"catálogo es ${precio_promedio:,.2f}, lo que "
            f"equivale aproximadamente a {unidades_estimadas} "
            f"unidades antes de considerar logística, impuestos "
            f"y margen comercial."
        )

    return (
        f"Con ${presupuesto:,.2f}, yo pondría primero el ojo "
        f"en {categoria} para {ciudad}.\n\n"
        f"El precio promedio es de ${precio_promedio:,.2f}, "
        f"así que podrías considerar alrededor de "
        f"{unidades_estimadas} piezas como referencia.\n\n"
        f"Ojo: todavía habría que descontar envío, impuestos "
        f"y dejar espacio para tu ganancia."
    )


def responder_comparacion(
    mensaje: str,
    perfil: str,
) -> str:
    ciudades = detectar_ciudades(mensaje)
    categoria = detectar_categoria(mensaje)

    if len(ciudades) < 2:
        return (
            "Para hacer una comparación necesito dos ciudades. "
            "Por ejemplo: “Compara Toluca y Cancún para sandalias”."
        )

    tabla = comparar_ciudades(
        ciudad_1=ciudades[0],
        ciudad_2=ciudades[1],
        categoria=categoria or "Todas",
    )

    mejor = tabla.sort_values(
        "Score promedio",
        ascending=False,
    ).iloc[0]

    if perfil == "Empresa":
        return (
            f"En la comparación, {mejor['Ciudad']} presenta "
            f"el mayor score promedio ({mejor['Score promedio']:.2f}). "
            f"El precio promedio es de "
            f"${mejor['Precio promedio']:.2f} y la temperatura "
            f"media es de {mejor['Temperatura media']:.1f} °C.\n\n"
            f"Esta información debe complementarse con margen, "
            f"inventario y capacidad logística."
        )

    return (
        f"Entre {ciudades[0]} y {ciudades[1]}, la mejor señal "
        f"la tiene {mejor['Ciudad']} con un score promedio de "
        f"{mejor['Score promedio']:.2f}.\n\n"
        f"Eso no significa que debas comprar todo ahí, pero sí "
        f"que vale la pena revisar primero las opciones de esa ciudad."
    )


def responder_modelo(
    perfil: str,
) -> str:
    if perfil == "Empresa":
        return (
            "El modelo final es HistGradientBoosting, entrenado "
            "con el Experimento B. En prueba obtuvo MAE de 0.5566, "
            "RMSE de 1.2747 y R² de 0.9894. La validación cruzada "
            "agrupada obtuvo un MAE promedio de 0.4976.\n\n"
            "El modelo estima el ModaPredict Score; no predice "
            "ventas ni demanda real."
        )

    return (
        "El modelo aprende a estimar el ModaPredict Score usando "
        "precio, tendencias, marca, categoría, ciudad y clima.\n\n"
        "En promedio se equivoca cerca de medio punto, pero ojo: "
        "no está prediciendo ventas reales, sino la recomendación "
        "del sistema."
    )


# ==========================================================
# RESPUESTA PRINCIPAL
# ==========================================================

def responder_chat(
    mensaje: str,
    historial: list | None = None,
    perfil: str = "Emprendedor",
) -> str:
    """
    Respuesta central del chat especializado.

    El historial se recibe para compatibilidad con Gradio,
    aunque esta primera versión no depende de un LLM.
    """

    del historial

    perfil = (
        "Empresa"
        if perfil == "Empresa"
        else "Emprendedor"
    )

    if not esta_dentro_del_alcance(mensaje):
        return respuesta_fuera_de_alcance(
            perfil=perfil
        )

    intencion = detectar_intencion(
        mensaje
    )

    if intencion == "recomendacion":
        return responder_recomendacion(
            mensaje=mensaje,
            perfil=perfil,
        )

    if intencion == "presupuesto":
        return responder_presupuesto(
            mensaje=mensaje,
            perfil=perfil,
        )

    if intencion == "comparacion":
        return responder_comparacion(
            mensaje=mensaje,
            perfil=perfil,
        )

    if intencion == "modelo":
        return responder_modelo(
            perfil=perfil
        )

    if intencion in {
        "explicacion",
        "tendencias",
        "consulta_general",
    }:
        return (
            "Claro, te ayudo con eso. Para darte una respuesta "
            "más útil dime al menos una ciudad, categoría, marca "
            "o presupuesto.\n\n"
            "Por ejemplo:\n"
            "• ¿Qué me conviene vender en Toluca?\n"
            "• Compara playeras entre Cancún y Monterrey.\n"
            "• Tengo $10,000 para empezar."
        )

    return respuesta_fuera_de_alcance(
        perfil=perfil
    )