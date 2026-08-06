"""
Utilidades visuales compartidas de ModaPredict AI.
"""

from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Any

import pandas as pd


RUTA_PROYECTO = Path(__file__).resolve().parents[2]

RUTA_GRAFICAS = (
    RUTA_PROYECTO
    / "resultados"
    / "graficas"
)


def formatear_valor_tabla(
    valor: Any,
) -> str:
    """Convierte un valor a texto seguro para HTML."""

    if pd.isna(valor):
        return "—"

    if isinstance(valor, float):
        texto = (
            f"{valor:,.2f}"
            .rstrip("0")
            .rstrip(".")
        )
    else:
        texto = str(valor)

    return escape(
        texto,
        quote=True,
    )


def construir_tabla_html(
    tabla: pd.DataFrame,
    mensaje_vacio: str = (
        "No hay información disponible."
    ),
) -> str:
    """Convierte un DataFrame en una tabla HTML personalizada."""

    if tabla is None or tabla.empty:
        return f"""
        <div class="empty-state">
            <div class="empty-icon">📊</div>

            <h3>No hay información disponible</h3>

            <p>
                {escape(mensaje_vacio)}
            </p>
        </div>
        """

    encabezados = "".join(
        f"<th>{escape(str(columna))}</th>"
        for columna in tabla.columns
    )

    filas: list[str] = []

    for _, registro in tabla.iterrows():
        celdas = "".join(
            f"<td>{formatear_valor_tabla(valor)}</td>"
            for valor in registro.tolist()
        )

        filas.append(
            f"<tr>{celdas}</tr>"
        )

    return f"""
    <div class="mp-table-wrapper">
        <table class="mp-table">
            <thead>
                <tr>
                    {encabezados}
                </tr>
            </thead>

            <tbody>
                {''.join(filas)}
            </tbody>
        </table>
    </div>
    """


def obtener_ruta_grafica(
    nombre: str,
) -> str | None:
    """Devuelve la ruta de una gráfica si existe."""

    ruta = RUTA_GRAFICAS / nombre

    if not ruta.exists():
        return None

    return str(ruta)