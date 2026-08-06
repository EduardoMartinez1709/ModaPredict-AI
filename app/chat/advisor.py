"""
Cerebro conversacional de ModaPredict Advisor.

Este módulo coordina:
- detección de intención;
- extracción de datos;
- memoria conversacional;
- validación del dominio;
- consultas al catálogo;
- generación de respuestas.
"""

from __future__ import annotations

from typing import Any

from app.chat.dominio import (
    esta_dentro_del_dominio,
    respuesta_fuera_del_dominio,
)
from app.chat.extractores import normalizar_texto
from app.chat.intenciones import detectar_intencion
from app.chat.memoria import (
    MEMORIA,
    MemoriaConversacion,
)
from app.chat.respuestas import (
    pedir_segunda_ciudad,
    preguntar_categoria,
    preguntar_ciudad,
    preguntar_presupuesto,
    respuesta_agradecimiento,
    respuesta_ayuda_general,
    respuesta_comparacion,
    respuesta_explicacion_oportunidad,
    respuesta_modelo,
    respuesta_presupuesto,
    respuesta_principiante,
    respuesta_recomendacion,
    respuesta_saludo,
)
from app.servicios import (
    comparar_ciudades,
    obtener_recomendaciones,
    resumen_para_emprendedor,
)


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

AGRADECIMIENTOS = {
    "gracias",
    "muchas gracias",
    "te agradezco",
    "perfecto gracias",
    "excelente gracias",
}

RESPUESTAS_NEGATIVAS = {
    "no",
    "ninguna",
    "ninguno",
    "no se",
    "no sé",
    "no tengo una",
    "no tengo alguna",
    "cualquiera",
    "lo que recomiendes",
}

CONTINUACIONES_BREVES = {
    "y ahora",
    "ahora",
    "y despues",
    "despues",
    "sigue",
    "continuemos",
    "continua",
    "que sigue",
    "que recomiendas",
    "dime mas",
}


def normalizar_perfil(
    perfil: str,
) -> str:
    """Normaliza el perfil recibido desde la interfaz."""

    return (
        "Empresa"
        if perfil == "Empresa"
        else "Emprendedor"
    )


def memoria_como_dict(
    memoria: MemoriaConversacion,
) -> dict[str, Any]:
    """Convierte el estado conversacional en diccionario."""

    return {
        "perfil": memoria.perfil,
        "ciudad": memoria.ciudad,
        "categoria": memoria.categoria,
        "marca": memoria.marca,
        "presupuesto": memoria.presupuesto,
        "ultima_intencion": memoria.ultima_intencion,
        "ultimo_producto": memoria.ultimo_producto,
        "ultima_respuesta": memoria.ultima_respuesta,
    }


def es_saludo(
    mensaje: str,
) -> bool:
    """Detecta saludos breves."""

    texto = normalizar_texto(mensaje)

    return any(
        texto == saludo
        or texto.startswith(f"{saludo} ")
        for saludo in SALUDOS
    )


def es_agradecimiento(
    mensaje: str,
) -> bool:
    """Detecta expresiones de agradecimiento."""

    texto = normalizar_texto(mensaje)

    return any(
        expresion in texto
        for expresion in AGRADECIMIENTOS
    )


def es_respuesta_negativa(
    mensaje: str,
) -> bool:
    """Detecta que el usuario no tiene una preferencia concreta."""

    texto = normalizar_texto(mensaje)

    return texto in {
        normalizar_texto(expresion)
        for expresion in RESPUESTAS_NEGATIVAS
    }


def es_continuacion_breve(
    mensaje: str,
) -> bool:
    """Detecta frases que dependen del contexto previo."""

    texto = normalizar_texto(mensaje)

    return texto in {
        normalizar_texto(expresion)
        for expresion in CONTINUACIONES_BREVES
    }


def guardar_y_devolver(
    memoria: MemoriaConversacion,
    respuesta: str,
) -> str:
    """Guarda la respuesta del Advisor y la devuelve."""

    memoria.ultima_respuesta = respuesta
    memoria.guardar_asistente(respuesta)

    return respuesta


def actualizar_memoria_desde_intencion(
    memoria: MemoriaConversacion,
    resultado: dict[str, Any],
) -> None:
    """Guarda los parámetros detectados en el mensaje actual."""

    ciudades = resultado.get("ciudades", [])

    if ciudades:
        memoria.ciudad = ciudades[0]

    categoria = resultado.get("categoria")

    if categoria:
        memoria.categoria = categoria

    marca = resultado.get("marca")

    if marca:
        memoria.marca = marca

    presupuesto = resultado.get("presupuesto")

    if presupuesto is not None:
        memoria.presupuesto = float(presupuesto)


def obtener_ciudades_comparacion(
    ciudades_actuales: list[str],
    ciudad_anterior: str | None,
) -> list[str]:
    """
    Construye las ciudades de comparación.

    Si el mensaje actual contiene dos ciudades, se usan esas dos.
    Si contiene una, se combina con la ciudad guardada cuando
    sean diferentes.
    """

    ciudades_unicas: list[str] = []

    for ciudad in ciudades_actuales:
        if ciudad not in ciudades_unicas:
            ciudades_unicas.append(ciudad)

    if len(ciudades_unicas) >= 2:
        return ciudades_unicas[:2]

    if (
        ciudad_anterior
        and ciudad_anterior not in ciudades_unicas
    ):
        ciudades_unicas.insert(0, ciudad_anterior)

    return ciudades_unicas[:2]


def contiene_datos_comerciales(
    resultado: dict[str, Any],
) -> bool:
    """Indica si el extractor encontró información útil."""

    return any(
        [
            bool(resultado.get("ciudades", [])),
            resultado.get("categoria") is not None,
            resultado.get("marca") is not None,
            resultado.get("presupuesto") is not None,
        ]
    )


class ModaPredictAdvisor:
    """Orquestador central del sistema conversacional."""

    def __init__(
        self,
        memoria: MemoriaConversacion | None = None,
    ) -> None:
        self.memoria = (
            memoria
            if memoria is not None
            else MEMORIA
        )

    def limpiar(self) -> None:
        """Reinicia completamente la conversación."""

        self.memoria.limpiar()

    def responder(
        self,
        mensaje: str,
        perfil: str = "Emprendedor",
        historial: list | None = None,
    ) -> str:
        """
        Procesa el mensaje y genera una respuesta
        conservando el contexto de la sesión.
        """

        del historial

        mensaje = str(mensaje or "").strip()
        perfil = normalizar_perfil(perfil)
        self.memoria.perfil = perfil

        if not mensaje:
            return guardar_y_devolver(
                self.memoria,
                respuesta_ayuda_general(perfil),
            )

        self.memoria.guardar_usuario(mensaje)

        if es_saludo(mensaje):
            return guardar_y_devolver(
                self.memoria,
                respuesta_saludo(perfil),
            )

        if es_agradecimiento(mensaje):
            return guardar_y_devolver(
                self.memoria,
                respuesta_agradecimiento(perfil),
            )

        # 1. Detectar la intención antes de validar el dominio.
        ciudad_anterior = self.memoria.ciudad
        intencion_anterior = self.memoria.ultima_intencion
        resultado = detectar_intencion(mensaje)

        intencion_detectada = resultado.get(
            "tipo",
            "general",
        )

        tiene_dato_comercial = contiene_datos_comerciales(
            resultado
        )

        respuesta_negativa = es_respuesta_negativa(
            mensaje
        )

        continuacion_breve = es_continuacion_breve(
            mensaje
        )

        memoria_dict = memoria_como_dict(
            self.memoria
        )

        es_continuacion_valida = (
            intencion_anterior is not None
            and (
                tiene_dato_comercial
                or respuesta_negativa
                or continuacion_breve
            )
        )

        if (
            not tiene_dato_comercial
            and not es_continuacion_valida
            and not esta_dentro_del_dominio(
                mensaje=mensaje,
                memoria=memoria_dict,
            )
        ):
            return guardar_y_devolver(
                self.memoria,
                respuesta_fuera_del_dominio(
                    perfil=perfil,
                    memoria=memoria_dict,
                ),
            )

        ciudades_mensaje = resultado.get(
            "ciudades",
            [],
        )

        ciudades_comparacion = obtener_ciudades_comparacion(
            ciudades_actuales=ciudades_mensaje,
            ciudad_anterior=ciudad_anterior,
        )

        actualizar_memoria_desde_intencion(
            memoria=self.memoria,
            resultado=resultado,
        )

        # 3. Conservar la intención anterior únicamente cuando
        # el nuevo mensaje realmente completa el contexto.
        intencion = intencion_detectada

        if (
            intencion_detectada == "general"
            and intencion_anterior
            and (
                tiene_dato_comercial
                or respuesta_negativa
                or continuacion_breve
            )
        ):
            intencion = intencion_anterior

        # Si el Advisor estaba reuniendo datos para recomendar,
        # recibir el presupuesto debe continuar esa recomendación.
        if (
            intencion_anterior in {
                "recomendar",
                "principiante",
            }
            and intencion_detectada
            in {
                "presupuesto",
                "precio",
            }
            and resultado.get("presupuesto") is not None
        ):
            intencion = intencion_anterior

        self.memoria.ultima_intencion = intencion

        if intencion == "explicar":
            texto = normalizar_texto(mensaje)

            if any(
                palabra in texto
                for palabra in [
                    "modelo",
                    "machine learning",
                    "mae",
                    "rmse",
                    "r2",
                    "prediccion",
                ]
            ):
                respuesta = respuesta_modelo(perfil)
            else:
                respuesta = respuesta_explicacion_oportunidad(
                    perfil
                )

            return guardar_y_devolver(
                self.memoria,
                respuesta,
            )

        if intencion == "comparar":
            if len(ciudades_comparacion) < 2:
                primera_ciudad = (
                    ciudades_comparacion[0]
                    if ciudades_comparacion
                    else self.memoria.ciudad
                )

                self.memoria.ultima_intencion = "comparar"

                return guardar_y_devolver(
                    self.memoria,
                    pedir_segunda_ciudad(
                        primera_ciudad
                    ),
                )

            ciudad_1 = ciudades_comparacion[0]
            ciudad_2 = ciudades_comparacion[1]

            tabla = comparar_ciudades(
                ciudad_1=ciudad_1,
                ciudad_2=ciudad_2,
                categoria=(
                    self.memoria.categoria
                    or "Todas"
                ),
            )

            respuesta = respuesta_comparacion(
                tabla=tabla,
                perfil=perfil,
            )

            return guardar_y_devolver(
                self.memoria,
                respuesta,
            )

        if intencion == "principiante":
            respuesta_inicial = respuesta_principiante(
                self.memoria
            )

            if not self.memoria.ciudad:
                self.memoria.ultima_intencion = (
                    "principiante"
                )

                respuesta = (
                    respuesta_inicial
                    + "\n\n"
                    + preguntar_ciudad(perfil)
                )

                return guardar_y_devolver(
                    self.memoria,
                    respuesta,
                )

            if self.memoria.presupuesto is None:
                self.memoria.ultima_intencion = (
                    "principiante"
                )

                respuesta = (
                    respuesta_inicial
                    + "\n\n"
                    + preguntar_presupuesto(
                        memoria=self.memoria,
                        perfil=perfil,
                    )
                )

                return guardar_y_devolver(
                    self.memoria,
                    respuesta,
                )

            resumen = resumen_para_emprendedor(
                ciudad=self.memoria.ciudad,
                presupuesto=self.memoria.presupuesto,
            )

            respuesta = respuesta_presupuesto(
                resumen=resumen,
                presupuesto=self.memoria.presupuesto,
                perfil=perfil,
            )

            return guardar_y_devolver(
                self.memoria,
                respuesta,
            )

        if intencion in {
            "precio",
            "presupuesto",
        }:
            if self.memoria.presupuesto is None:
                self.memoria.ultima_intencion = (
                    "presupuesto"
                )

                return guardar_y_devolver(
                    self.memoria,
                    preguntar_presupuesto(
                        memoria=self.memoria,
                        perfil=perfil,
                    ),
                )

            if not self.memoria.ciudad:
                self.memoria.ultima_intencion = (
                    "presupuesto"
                )

                return guardar_y_devolver(
                    self.memoria,
                    preguntar_ciudad(perfil),
                )

            resumen = resumen_para_emprendedor(
                ciudad=self.memoria.ciudad,
                presupuesto=self.memoria.presupuesto,
            )

            respuesta = respuesta_presupuesto(
                resumen=resumen,
                presupuesto=self.memoria.presupuesto,
                perfil=perfil,
            )

            return guardar_y_devolver(
                self.memoria,
                respuesta,
            )

        if intencion == "recomendar":
            if not self.memoria.ciudad:
                self.memoria.ultima_intencion = (
                    "recomendar"
                )

                return guardar_y_devolver(
                    self.memoria,
                    preguntar_ciudad(perfil),
                )

            # 2. Preguntar presupuesto antes de recomendar.
            if self.memoria.presupuesto is None:
                self.memoria.ultima_intencion = (
                    "recomendar"
                )

                return guardar_y_devolver(
                    self.memoria,
                    preguntar_presupuesto(
                        memoria=self.memoria,
                        perfil=perfil,
                    ),
                )

            if respuesta_negativa:
                self.memoria.categoria = None

            datos = obtener_recomendaciones(
                ciudad=self.memoria.ciudad,
                categoria=(
                    self.memoria.categoria
                    or "Todas"
                ),
                marca=(
                    self.memoria.marca
                    or "Todas"
                ),
                cantidad=5,
            )

            if (
                datos is not None
                and not datos.empty
            ):
                self.memoria.ultimo_producto = str(
                    datos.iloc[0].get(
                        "nombre",
                        "",
                    )
                )

            respuesta = respuesta_recomendacion(
                datos=datos,
                memoria=self.memoria,
                perfil=perfil,
            )

            return guardar_y_devolver(
                self.memoria,
                respuesta,
            )

        if (
            self.memoria.ciudad
            and self.memoria.presupuesto is not None
        ):
            resumen = resumen_para_emprendedor(
                ciudad=self.memoria.ciudad,
                presupuesto=self.memoria.presupuesto,
            )

            respuesta = respuesta_presupuesto(
                resumen=resumen,
                presupuesto=self.memoria.presupuesto,
                perfil=perfil,
            )

            return guardar_y_devolver(
                self.memoria,
                respuesta,
            )

        if not self.memoria.ciudad:
            self.memoria.ultima_intencion = "recomendar"

            return guardar_y_devolver(
                self.memoria,
                preguntar_ciudad(perfil),
            )

        if self.memoria.presupuesto is None:
            self.memoria.ultima_intencion = "presupuesto"

            return guardar_y_devolver(
                self.memoria,
                preguntar_presupuesto(
                    memoria=self.memoria,
                    perfil=perfil,
                ),
            )

        if self.memoria.categoria is None:
            return guardar_y_devolver(
                self.memoria,
                preguntar_categoria(
                    memoria=self.memoria,
                    perfil=perfil,
                ),
            )

        return guardar_y_devolver(
            self.memoria,
            respuesta_ayuda_general(perfil),
        )


ADVISOR = ModaPredictAdvisor()


def responder_chat(
    mensaje: str,
    historial: list | None = None,
    perfil: str = "Emprendedor",
) -> str:
    """Punto de entrada compatible con Gradio."""

    return ADVISOR.responder(
        mensaje=mensaje,
        perfil=perfil,
        historial=historial,
    )


def limpiar_memoria_chat() -> None:
    """Reinicia la memoria del Advisor."""

    ADVISOR.limpiar()