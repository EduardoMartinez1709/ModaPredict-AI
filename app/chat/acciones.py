"""
Acciones que puede realizar el asesor de ModaPredict AI.
Aquí NO se interpreta el mensaje.
Aquí únicamente se ejecuta la acción solicitada.
"""

from __future__ import annotations

from app.dashboards import (
    generar_dashboard_emprendedor,
    generar_dashboard_empresa,
)


# ==========================================================
# RECOMENDACIONES
# ==========================================================

def recomendar_productos(
    ciudad: str,
    presupuesto: float | None = None,
):
    """
    Devuelve el dashboard del emprendedor.
    """

    return generar_dashboard_emprendedor(
        ciudad=ciudad,
        presupuesto=presupuesto,
    )


# ==========================================================
# DASHBOARD EMPRESA
# ==========================================================

def dashboard_empresa(
    ciudad: str = "Todas",
):
    """
    Dashboard ejecutivo.
    """

    return generar_dashboard_empresa(
        ciudad=ciudad
    )


# ==========================================================
# EXPLICAR SCORE
# ==========================================================

def explicar_oportunidad() -> str:

    return (
        "La oportunidad comercial representa el potencial que "
        "tiene un producto para venderse en una ciudad. "
        "Se calcula utilizando tendencias, clima, precio, "
        "marca y un modelo de Machine Learning."
    )


# ==========================================================
# AYUDA PARA PRINCIPIANTES
# ==========================================================

def ayuda_principiante() -> str:

    return (
        "Si vas comenzando, te recomiendo elegir una ciudad, "
        "definir un presupuesto y revisar primero las categorías "
        "con mayor oportunidad comercial antes de comprar inventario."
    )


# ==========================================================
# COMPARAR
# ==========================================================

def comparar(
    ciudad1,
    ciudad2,
):
    """
    Aquí después construiremos la comparación
    entre ciudades.
    """

    return (
        f"Compararemos {ciudad1} contra {ciudad2} "
        "en una siguiente versión."
    )