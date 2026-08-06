"""
Respuestas conversacionales de ModaPredict Advisor.

Este módulo centraliza el tono y la redacción del asistente.
No detecta intenciones ni modifica la memoria.
"""

from __future__ import annotations

from typing import Any

import pandas as pd

from app.chat.memoria import MemoriaConversacion


# ==========================================================
# FUNCIONES AUXILIARES
# ==========================================================

def formatear_moneda(
    cantidad: float | None,
) -> str:
    """Formatea una cantidad monetaria."""

    if cantidad is None:
        return "sin definir"

    return f"${float(cantidad):,.2f}"


def obtener_valor_memoria(
    memoria: MemoriaConversacion | dict[str, Any],
    campo: str,
    valor_default=None,
):
    """
    Obtiene un valor de memoria, ya sea una dataclass
    o un diccionario.
    """

    if isinstance(memoria, dict):
        return memoria.get(
            campo,
            valor_default,
        )

    return getattr(
        memoria,
        campo,
        valor_default,
    )


# ==========================================================
# SALUDOS Y CORTESÍA
# ==========================================================

def respuesta_saludo(
    perfil: str,
) -> str:
    """Saludo inicial según el perfil."""

    if perfil == "Empresa":
        return (
            "¡Hola! 👋 Soy **ModaPredict Advisor**.\n\n"
            "Puedo ayudarte a analizar categorías, marcas, "
            "ciudades, precios, inventario, tendencias y "
            "resultados del modelo.\n\n"
            "¿Qué decisión comercial te gustaría revisar?"
        )

    return (
        "¡Hola! 👋 Soy **ModaPredict Advisor**.\n\n"
        "Estoy aquí para ayudarte a descubrir qué productos "
        "podrían representar una mejor oportunidad para comenzar "
        "o fortalecer tu negocio de moda.\n\n"
        "Podemos empezar por tu ciudad, tu presupuesto o la "
        "categoría que te interesa."
    )


def respuesta_agradecimiento(
    perfil: str,
) -> str:
    """Respuesta amable ante un agradecimiento."""

    if perfil == "Empresa":
        return (
            "Con gusto. Quedo listo para continuar con otro "
            "análisis comercial, una comparación entre ciudades "
            "o la revisión de categorías."
        )

    return (
        "¡Con gusto! 😊 Cuando quieras podemos seguir comparando "
        "productos, ciudades o aprovechar mejor tu presupuesto."
    )


# ==========================================================
# PREGUNTAS PARA COMPLETAR INFORMACIÓN
# ==========================================================

def preguntar_ciudad(
    perfil: str,
) -> str:
    """Solicita la ciudad necesaria para el análisis."""

    if perfil == "Empresa":
        return (
            "Para continuar necesito definir la cobertura "
            "geográfica del análisis.\n\n"
            "¿Qué ciudad deseas revisar: **Toluca, Ciudad de "
            "México, Guadalajara, Monterrey o Cancún**?"
        )

    return (
        "¡Va! Para darte una recomendación realmente útil, "
        "primero necesito saber algo:\n\n"
        "📍 **¿En qué ciudad piensas vender?**\n\n"
        "Puedo analizar Toluca, Ciudad de México, Guadalajara, "
        "Monterrey o Cancún."
    )


def preguntar_presupuesto(
    memoria: MemoriaConversacion | dict[str, Any],
    perfil: str,
) -> str:
    """Solicita el presupuesto conservando el contexto."""

    ciudad = obtener_valor_memoria(
        memoria,
        "ciudad",
    )

    contexto = (
        f": **{ciudad}**"
        if ciudad
        else ""
    )

    if perfil == "Empresa":
        return (
            f"Ya tengo definida la ciudad{contexto}. Para estimar "
            "el alcance de la compra necesito conocer el presupuesto "
            "aproximado.\n\n"
            "¿Qué monto deseas analizar?"
        )

    return (
        f"Perfecto, ya tengo registrada la ciudad{contexto}. 👍\n\n"
        "Ahora dime aproximadamente **cuánto quieres invertir**.\n\n"
        "Por ejemplo: **$10,000**, **15 mil** o **25,000 pesos**."
    )


def preguntar_categoria(
    memoria: MemoriaConversacion | dict[str, Any],
    perfil: str,
) -> str:
    """Pregunta por una categoría cuando sea necesaria."""

    ciudad = obtener_valor_memoria(
        memoria,
        "ciudad",
    )

    contexto = (
        f" en **{ciudad}**"
        if ciudad
        else ""
    )

    if perfil == "Empresa":
        return (
            f"¿Deseas analizar una categoría específica{contexto} "
            "o revisar el catálogo completo?"
        )

    return (
        f"¿Tienes alguna categoría en mente{contexto}? "
        "Por ejemplo: **playeras, pantalones, tenis, vestidos "
        "o sandalias**.\n\n"
        "También puedes decirme: **“No sé qué vender”**."
    )


def pedir_segunda_ciudad(
    primera_ciudad: str | None,
) -> str:
    """Solicita la segunda ciudad para una comparación."""

    contexto = (
        f"Ya tengo **{primera_ciudad}**. "
        if primera_ciudad
        else ""
    )

    return (
        f"{contexto}Para realizar la comparación necesito una "
        "segunda ciudad.\n\n"
        "¿Con cuál te gustaría compararla?"
    )


# ==========================================================
# RESPUESTAS DE RECOMENDACIÓN
# ==========================================================

def respuesta_recomendacion(
    datos: pd.DataFrame,
    memoria: MemoriaConversacion | dict[str, Any],
    perfil: str,
) -> str:
    """Redacta una recomendación a partir del ranking."""

    if datos is None or datos.empty:
        return (
            "No encontré productos que coincidan con la combinación "
            "actual. Podemos ampliar el presupuesto, cambiar la "
            "categoría o revisar otra ciudad."
        )

    top = datos.iloc[0]

    ciudad = str(
        top.get(
            "ciudad",
            obtener_valor_memoria(
                memoria,
                "ciudad",
                "la ciudad seleccionada",
            ),
        )
    )

    categoria = str(
        top.get(
            "categoria_normalizada",
            "la categoría analizada",
        )
    )

    producto = str(
        top.get(
            "nombre",
            "Producto destacado",
        )
    )

    precio = float(
        top.get(
            "precio_actual",
            0,
        )
        or 0
    )

    score = float(
        top.get(
            "modapredict_score",
            0,
        )
        or 0
    )

    prediccion = float(
        top.get(
            "prediccion_ml",
            0,
        )
        or 0
    )

    if perfil == "Empresa":
        return (
            f"El análisis identifica una oportunidad destacada en "
            f"**{categoria} para {ciudad}**.\n\n"
            f"El producto mejor posicionado es **{producto}**, con:\n\n"
            f"- Precio actual: **${precio:,.2f}**\n"
            f"- ModaPredict Score: **{score:.1f}**\n"
            f"- Predicción ML: **{prediccion:.1f}**\n\n"
            "Conviene revisar también las primeras opciones del "
            "ranking y complementar el resultado con margen, stock, "
            "rotación y costos logísticos."
        )

    return (
        f"¡Encontré una opción interesante! 🙌\n\n"
        f"Para **{ciudad}**, la mejor señal aparece en "
        f"**{categoria}**.\n\n"
        f"El producto mejor posicionado es:\n\n"
        f"### {producto}\n"
        f"Precio aproximado: **${precio:,.2f}**\n\n"
        "Yo lo tomaría como una de las primeras opciones para "
        "revisar, comparando también tallas, disponibilidad, envío "
        "y el margen que podrías obtener."
    )


# ==========================================================
# RESPUESTA DE PRESUPUESTO
# ==========================================================

def respuesta_presupuesto(
    resumen: dict[str, Any],
    presupuesto: float,
    perfil: str,
) -> str:
    """Redacta un análisis sencillo del presupuesto."""

    ciudad = resumen.get(
        "ciudad",
        "la ciudad seleccionada",
    )

    categoria = resumen.get(
        "categoria_destacada",
        "Sin información",
    )

    precio_promedio = float(
        resumen.get(
            "precio_promedio",
            0,
        )
        or 0
    )

    unidades = (
        int(
            presupuesto // precio_promedio
        )
        if precio_promedio > 0
        else 0
    )

    if perfil == "Empresa":
        return (
            f"Para **{ciudad}**, el presupuesto analizado es de "
            f"**{formatear_moneda(presupuesto)}**.\n\n"
            f"La categoría con mejor señal promedio es "
            f"**{categoria}**, con un precio unitario promedio de "
            f"**{formatear_moneda(precio_promedio)}**.\n\n"
            f"Como referencia, el monto equivaldría a alrededor de "
            f"**{unidades} unidades**, antes de considerar impuestos, "
            "logística, descuentos por volumen y margen comercial."
        )

    return (
        f"Perfecto 👍 Con un presupuesto de "
        f"**{formatear_moneda(presupuesto)}** para **{ciudad}**, "
        f"yo pondría primero el ojo en **{categoria}**.\n\n"
        f"El precio promedio ronda los "
        f"**{formatear_moneda(precio_promedio)}**, así que podrías "
        f"tomar como referencia unas **{unidades} piezas**.\n\n"
        "No significa que debas comprar todas iguales. Lo más sano "
        "sería dividir el presupuesto entre varios modelos, tallas "
        "y precios, dejando una parte para envío y margen."
    )


# ==========================================================
# COMPARACIÓN DE CIUDADES
# ==========================================================

def respuesta_comparacion(
    tabla: pd.DataFrame,
    perfil: str,
) -> str:
    """Resume la comparación entre dos ciudades."""

    if tabla is None or tabla.empty:
        return (
            "No encontré suficiente información para realizar "
            "la comparación solicitada."
        )

    ordenada = tabla.sort_values(
        "Score promedio",
        ascending=False,
    )

    mejor = ordenada.iloc[0]

    ciudad_mejor = mejor["Ciudad"]
    score = float(
        mejor["Score promedio"]
    )

    precio = float(
        mejor["Precio promedio"]
    )

    temperatura = mejor.get(
        "Temperatura media",
    )

    temperatura_texto = ""

    if pd.notna(temperatura):
        temperatura_texto = (
            f" y una temperatura media de "
            f"**{float(temperatura):.1f} °C**"
        )

    ciudades = tabla[
        "Ciudad"
    ].astype(str).tolist()

    comparadas = " y ".join(
        ciudades
    )

    if perfil == "Empresa":
        return (
            f"En la comparación entre **{comparadas}**, "
            f"**{ciudad_mejor}** presenta la mejor señal comercial, "
            f"con un ModaPredict Score promedio de **{score:.2f}**.\n\n"
            f"El precio promedio es de **${precio:,.2f}**"
            f"{temperatura_texto}.\n\n"
            "La decisión final debe complementarse con rotación, "
            "costos logísticos, margen y disponibilidad regional."
        )

    return (
        f"Entre **{comparadas}**, la mejor señal la tiene "
        f"**{ciudad_mejor}**. 🙌\n\n"
        f"Su oportunidad promedio es de **{score:.2f}** y el precio "
        f"medio de los productos es de **${precio:,.2f}**"
        f"{temperatura_texto}.\n\n"
        "Yo empezaría revisando esa ciudad, aunque conviene comparar "
        "también costos de envío y el tipo de cliente al que quieres llegar."
    )


# ==========================================================
# PRINCIPIANTES
# ==========================================================

def respuesta_principiante(
    memoria: MemoriaConversacion | dict[str, Any],
) -> str:
    """Guía inicial para una persona que comienza."""

    ciudad = obtener_valor_memoria(
        memoria,
        "ciudad",
    )

    presupuesto = obtener_valor_memoria(
        memoria,
        "presupuesto",
    )

    conocidos = []

    if ciudad:
        conocidos.append(
            f"ciudad: **{ciudad}**"
        )

    if presupuesto:
        conocidos.append(
            f"presupuesto: **{formatear_moneda(presupuesto)}**"
        )

    contexto = ""

    if conocidos:
        contexto = (
            "\n\nPor ahora tengo registrado: "
            + " · ".join(conocidos)
            + "."
        )

    return (
        "¡Qué padre que quieras comenzar! 🚀\n\n"
        "No necesitas decidir todo de inmediato. Para construir "
        "una recomendación útil vamos a definir tres cosas:\n\n"
        "1. La ciudad donde piensas vender.\n"
        "2. El presupuesto disponible.\n"
        "3. Las categorías que podrían funcionar mejor."
        f"{contexto}\n\n"
        "Yo te iré guiando paso a paso."
    )


# ==========================================================
# EXPLICACIÓN DEL MODELO
# ==========================================================

def respuesta_modelo(
    perfil: str,
) -> str:
    """Explica qué hace y qué no hace el modelo."""

    if perfil == "Empresa":
        return (
            "El modelo final de ModaPredict AI es "
            "**HistGradientBoosting**, entrenado con el Experimento B.\n\n"
            "Resultados principales:\n\n"
            "- MAE de prueba: **0.5576**\n"
            "- RMSE de prueba: **1.2641**\n"
            "- R² de prueba: **0.9895**\n"
            "- MAE promedio en validación cruzada: **0.5029**\n\n"
            "El modelo estima el **ModaPredict Score**. No predice "
            "ventas reales, demanda futura ni utilidad financiera."
        )

    return (
        "El modelo analiza señales como precio, tendencias, marca, "
        "categoría, ciudad y clima para estimar la oportunidad de "
        "cada producto.\n\n"
        "En términos sencillos: ayuda a ordenar opciones y detectar "
        "cuáles parecen más atractivas dentro del catálogo.\n\n"
        "Ojo: no garantiza ventas ni predice exactamente cuánto "
        "dinero ganarás."
    )


def respuesta_explicacion_oportunidad(
    perfil: str,
) -> str:
    """Explica el indicador principal de la plataforma."""

    if perfil == "Empresa":
        return (
            "El **ModaPredict Score** es un indicador compuesto que "
            "resume señales de tendencia, clima, precio, características "
            "del producto y reglas comerciales. La predicción ML estima "
            "ese mismo indicador mediante el modelo entrenado.\n\n"
            "Debe interpretarse como una herramienta de priorización, "
            "no como una probabilidad de venta."
        )

    return (
        "La **oportunidad comercial** es una forma sencilla de mostrar "
        "qué tan atractiva parece una opción dentro del catálogo.\n\n"
        "Considera tendencias, clima, precio, marca y análisis con "
        "Machine Learning.\n\n"
        "Mientras mejor sea la valoración, más sentido tiene revisar "
        "ese producto antes que otros; aun así, no significa que las "
        "ventas estén garantizadas."
    )


# ==========================================================
# RESPUESTAS GENERALES
# ==========================================================

def respuesta_ayuda_general(
    perfil: str,
) -> str:
    """Ofrece opciones cuando la intención no es clara."""

    if perfil == "Empresa":
        return (
            "Puedo ayudarte con alguno de estos análisis:\n\n"
            "- Comparar dos ciudades.\n"
            "- Identificar categorías con mejor score.\n"
            "- Revisar marcas, precios o cobertura.\n"
            "- Explicar el modelo y sus métricas.\n"
            "- Analizar oportunidades de inventario.\n\n"
            "¿Cuál deseas realizar?"
        )

    return (
        "Claro, vamos paso a paso 😊\n\n"
        "Puedo ayudarte a:\n\n"
        "- Encontrar qué vender en una ciudad.\n"
        "- Organizar opciones según tu presupuesto.\n"
        "- Comparar dos ciudades.\n"
        "- Revisar una categoría o marca.\n"
        "- Explicarte por qué una opción es recomendable.\n\n"
        "Puedes comenzar diciéndome: "
        "**“Quiero vender ropa en Toluca”**."
    )