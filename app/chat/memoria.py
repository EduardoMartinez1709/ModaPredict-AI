"""
Memoria conversacional de ModaPredict Advisor.

Este módulo almacena el contexto de la conversación
mientras el usuario no pulse "Limpiar conversación".
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class MemoriaConversacion:
    """
    Estado actual de la conversación.
    """

    perfil: str = "Emprendedor"

    ciudad: str | None = None

    categoria: str | None = None

    marca: str | None = None

    presupuesto: float | None = None

    ultima_intencion: str | None = None

    ultimo_producto: str | None = None

    ultima_respuesta: str | None = None

    historial: list[tuple[str, str]] = field(
        default_factory=list
    )

    # ----------------------------------------------------

    def guardar_usuario(
        self,
        mensaje: str,
    ) -> None:
        self.historial.append(
            ("usuario", mensaje)
        )

    # ----------------------------------------------------

    def guardar_asistente(
        self,
        mensaje: str,
    ) -> None:
        self.historial.append(
            ("advisor", mensaje)
        )

    # ----------------------------------------------------

    def limpiar(self) -> None:
        """
        Reinicia toda la conversación.
        """

        self.ciudad = None
        self.categoria = None
        self.marca = None
        self.presupuesto = None
        self.ultima_intencion = None
        self.ultimo_producto = None
        self.ultima_respuesta = None

        self.historial.clear()

    # ----------------------------------------------------

    def actualizar(
        self,
        **kwargs,
    ) -> None:

        for llave, valor in kwargs.items():

            if valor is None:
                continue

            if hasattr(self, llave):
                setattr(
                    self,
                    llave,
                    valor,
                )


# ======================================================
# MEMORIA GLOBAL
# ======================================================

MEMORIA = MemoriaConversacion()