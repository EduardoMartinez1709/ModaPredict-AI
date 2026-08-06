"""
Generación de reportes PDF para ModaPredict AI.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import (
    ParagraphStyle,
    getSampleStyleSheet,
)
from reportlab.lib.units import cm
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


# ==========================================================
# RUTAS Y PALETA
# ==========================================================

RUTA_PROYECTO = Path(__file__).resolve().parents[1]

RUTA_REPORTES = (
    RUTA_PROYECTO
    / "resultados"
    / "reportes"
)

RUTA_LOGO = (
    RUTA_PROYECTO
    / "app"
    / "assets"
    / "logo.png"
)

NEGRO = colors.HexColor("#080808")
PANEL = colors.HexColor("#141519")
DORADO = colors.HexColor("#D6B36A")
DORADO_CLARO = colors.HexColor("#F3D995")
BLANCO = colors.HexColor("#F7F7F7")
GRIS = colors.HexColor("#D0D1D5")
GRIS_OSCURO = colors.HexColor("#303238")
ROJO = colors.HexColor("#D87373")


# ==========================================================
# ESTILOS
# ==========================================================

def construir_estilos() -> dict[str, ParagraphStyle]:
    """Construye los estilos tipográficos del reporte."""

    base = getSampleStyleSheet()

    return {
        "titulo": ParagraphStyle(
            "TituloModaPredict",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=27,
            leading=31,
            textColor=DORADO_CLARO,
            alignment=TA_CENTER,
            spaceAfter=12,
        ),
        "subtitulo": ParagraphStyle(
            "SubtituloModaPredict",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=12,
            leading=17,
            textColor=GRIS,
            alignment=TA_CENTER,
            spaceAfter=12,
        ),
        "seccion": ParagraphStyle(
            "SeccionModaPredict",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=17,
            leading=21,
            textColor=DORADO_CLARO,
            spaceBefore=12,
            spaceAfter=10,
        ),
        "texto": ParagraphStyle(
            "TextoModaPredict",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=10,
            leading=15,
            textColor=NEGRO,
            alignment=TA_LEFT,
            spaceAfter=8,
        ),
        "nota": ParagraphStyle(
            "NotaModaPredict",
            parent=base["BodyText"],
            fontName="Helvetica-Oblique",
            fontSize=8.5,
            leading=12,
            textColor=colors.HexColor("#555555"),
            alignment=TA_LEFT,
        ),
        "kpi_label": ParagraphStyle(
            "KpiLabel",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=10,
            textColor=DORADO_CLARO,
            alignment=TA_CENTER,
        ),
        "kpi_value": ParagraphStyle(
            "KpiValue",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=16,
            leading=19,
            textColor=BLANCO,
            alignment=TA_CENTER,
        ),
    }


# ==========================================================
# ELEMENTOS DEL REPORTE
# ==========================================================

def agregar_numero_pagina(
    canvas,
    documento,
) -> None:
    """Agrega pie de página y numeración."""

    canvas.saveState()

    ancho, _ = letter

    canvas.setStrokeColor(
        DORADO
    )
    canvas.setLineWidth(
        0.6
    )
    canvas.line(
        1.7 * cm,
        1.25 * cm,
        ancho - 1.7 * cm,
        1.25 * cm,
    )

    canvas.setFont(
        "Helvetica",
        8,
    )
    canvas.setFillColor(
        colors.HexColor("#555555")
    )

    canvas.drawString(
        1.7 * cm,
        0.85 * cm,
        "ModaPredict AI - Reporte ejecutivo",
    )

    canvas.drawRightString(
        ancho - 1.7 * cm,
        0.85 * cm,
        f"Página {documento.page}",
    )

    canvas.restoreState()


def construir_portada(
    estilos: dict[str, ParagraphStyle],
    nombre_empresa: str,
) -> list:
    """Construye la portada del reporte."""

    elementos: list = [
        Spacer(
            1,
            2.2 * cm,
        )
    ]

    if RUTA_LOGO.exists():
        logo = Image(
            str(RUTA_LOGO),
            width=5.3 * cm,
            height=5.3 * cm,
        )

        logo.hAlign = "CENTER"
        elementos.append(
            logo
        )
        elementos.append(
            Spacer(
                1,
                0.5 * cm,
            )
        )

    elementos.extend(
        [
            Paragraph(
                "ModaPredict AI",
                estilos["titulo"],
            ),
            Paragraph(
                "Reporte ejecutivo de inventario",
                estilos["subtitulo"],
            ),
            Spacer(
                1,
                1.1 * cm,
            ),
            Paragraph(
                f"<b>Empresa analizada:</b> {nombre_empresa}",
                estilos["subtitulo"],
            ),
            Paragraph(
                (
                    "<b>Fecha del análisis:</b> "
                    f"{datetime.now().strftime('%d/%m/%Y %H:%M')}"
                ),
                estilos["subtitulo"],
            ),
            Spacer(
                1,
                1.4 * cm,
            ),
            Paragraph(
                (
                    "Este reporte transforma información de "
                    "inventario, ventas y margen en recomendaciones "
                    "claras para apoyar la toma de decisiones."
                ),
                estilos["subtitulo"],
            ),
            PageBreak(),
        ]
    )

    return elementos


def construir_tabla_kpis(
    resumen: dict[str, Any],
    estilos: dict[str, ParagraphStyle],
) -> Table:
    """Construye las tarjetas KPI del reporte."""

    kpis = [
        (
            "PRODUCTOS ANALIZADOS",
            f"{resumen.get('productos', 0):,}",
        ),
        (
            "STOCK TOTAL",
            f"{resumen.get('stock_total', 0):,}",
        ),
        (
            "VENTAS 30 DÍAS",
            f"{resumen.get('ventas_30_dias', 0):,}",
        ),
        (
            "PRODUCTOS CON ALERTA",
            f"{resumen.get('productos_alerta', 0):,}",
        ),
        (
            "INVENTARIO A COSTO",
            (
                "$"
                f"{resumen.get('valor_inventario_costo', 0):,.2f}"
            ),
        ),
        (
            "MARGEN PROMEDIO",
            f"{resumen.get('margen_promedio_pct', 0):.1f}%",
        ),
    ]

    filas = []

    for indice in range(
        0,
        len(kpis),
        3,
    ):
        etiquetas = []
        valores = []

        for etiqueta, valor in kpis[
            indice:indice + 3
        ]:
            etiquetas.append(
                Paragraph(
                    etiqueta,
                    estilos["kpi_label"],
                )
            )

            valores.append(
                Paragraph(
                    valor,
                    estilos["kpi_value"],
                )
            )

        filas.append(
            etiquetas
        )
        filas.append(
            valores
        )

    tabla = Table(
        filas,
        colWidths=[
            5.4 * cm,
            5.4 * cm,
            5.4 * cm,
        ],
        rowHeights=[
            0.75 * cm,
            1.15 * cm,
            0.75 * cm,
            1.15 * cm,
        ],
        hAlign="CENTER",
    )

    tabla.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    PANEL,
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.8,
                    DORADO,
                ),
                (
                    "INNERGRID",
                    (0, 0),
                    (-1, -1),
                    0.35,
                    GRIS_OSCURO,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
            ]
        )
    )

    return tabla


def construir_tabla_alertas_pdf(
    tabla_alertas: pd.DataFrame,
) -> Table | Paragraph:
    """Convierte la tabla de alertas a formato PDF."""

    if (
        tabla_alertas is None
        or tabla_alertas.empty
    ):
        return Paragraph(
            (
                "No se detectaron productos con alertas "
                "según las reglas actuales."
            ),
            construir_estilos()["texto"],
        )

    columnas_deseadas = [
        "Producto",
        "Categoría",
        "Stock",
        "Ventas 30 días",
        "Margen %",
        "Estado",
    ]

    columnas = [
        columna
        for columna in columnas_deseadas
        if columna in tabla_alertas.columns
    ]

    tabla = (
        tabla_alertas[
            columnas
        ]
        .head(20)
        .copy()
    )

    encabezados = [
        Paragraph(
            f"<b>{columna}</b>",
            ParagraphStyle(
                "TablaHeader",
                fontName="Helvetica-Bold",
                fontSize=7.3,
                leading=9,
                textColor=NEGRO,
                alignment=TA_CENTER,
            ),
        )
        for columna in columnas
    ]

    filas = [
        encabezados
    ]

    estilo_celda = ParagraphStyle(
        "TablaCelda",
        fontName="Helvetica",
        fontSize=7.2,
        leading=9,
        textColor=NEGRO,
    )

    for _, fila in tabla.iterrows():
        filas.append(
            [
                Paragraph(
                    str(
                        fila.get(
                            columna,
                            "",
                        )
                    ),
                    estilo_celda,
                )
                for columna in columnas
            ]
        )

    anchos = {
        "Producto": 5.0 * cm,
        "Categoría": 2.5 * cm,
        "Stock": 1.6 * cm,
        "Ventas 30 días": 2.1 * cm,
        "Margen %": 1.8 * cm,
        "Estado": 3.2 * cm,
    }

    tabla_pdf = Table(
        filas,
        colWidths=[
            anchos.get(
                columna,
                2.5 * cm,
            )
            for columna in columnas
        ],
        repeatRows=1,
        hAlign="CENTER",
    )

    estilos_tabla = [
        (
            "BACKGROUND",
            (0, 0),
            (-1, 0),
            DORADO_CLARO,
        ),
        (
            "TEXTCOLOR",
            (0, 0),
            (-1, 0),
            NEGRO,
        ),
        (
            "GRID",
            (0, 0),
            (-1, -1),
            0.35,
            colors.HexColor("#A0A0A0"),
        ),
        (
            "VALIGN",
            (0, 0),
            (-1, -1),
            "MIDDLE",
        ),
        (
            "LEFTPADDING",
            (0, 0),
            (-1, -1),
            5,
        ),
        (
            "RIGHTPADDING",
            (0, 0),
            (-1, -1),
            5,
        ),
        (
            "TOPPADDING",
            (0, 0),
            (-1, -1),
            5,
        ),
        (
            "BOTTOMPADDING",
            (0, 0),
            (-1, -1),
            5,
        ),
    ]

    for indice in range(
        1,
        len(filas),
    ):
        fondo = (
            colors.HexColor("#F5F5F5")
            if indice % 2 == 0
            else colors.white
        )

        estilos_tabla.append(
            (
                "BACKGROUND",
                (0, indice),
                (-1, indice),
                fondo,
            )
        )

    tabla_pdf.setStyle(
        TableStyle(
            estilos_tabla
        )
    )

    return tabla_pdf


# ==========================================================
# GENERADOR PRINCIPAL
# ==========================================================

def generar_reporte_empresa_pdf(
    resumen: dict[str, Any],
    resumen_ejecutivo: str,
    tabla_alertas: pd.DataFrame,
    nombre_empresa: str = "Empresa",
) -> str:
    """
    Genera un reporte PDF empresarial.

    Devuelve la ruta del archivo creado.
    """

    RUTA_REPORTES.mkdir(
        parents=True,
        exist_ok=True,
    )

    nombre_seguro = (
        nombre_empresa.strip()
        .lower()
        .replace(
            " ",
            "_",
        )
    )

    marca_tiempo = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    ruta_salida = (
        RUTA_REPORTES
        / (
            "reporte_modapredict_"
            f"{nombre_seguro}_{marca_tiempo}.pdf"
        )
    )

    documento = SimpleDocTemplate(
        str(
            ruta_salida
        ),
        pagesize=letter,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.8 * cm,
        title="Reporte ejecutivo ModaPredict AI",
        author="ModaPredict AI",
    )

    estilos = construir_estilos()

    contenido = construir_portada(
        estilos=estilos,
        nombre_empresa=nombre_empresa,
    )

    contenido.extend(
        [
            Paragraph(
                "Resumen de indicadores",
                estilos["seccion"],
            ),
            construir_tabla_kpis(
                resumen=resumen,
                estilos=estilos,
            ),
            Spacer(
                1,
                0.7 * cm,
            ),
            Paragraph(
                "Conclusiones ejecutivas",
                estilos["seccion"],
            ),
        ]
    )

    parrafos = [
        parrafo.strip()
        for parrafo in str(
            resumen_ejecutivo
        ).split(
            "\n\n"
        )
        if parrafo.strip()
    ]

    for parrafo in parrafos:
        texto = (
            parrafo
            .replace(
                "**",
                "<b>",
                1,
            )
        )

        # El resumen viene en Markdown. Para evitar etiquetas
        # abiertas incorrectas, lo mostramos como texto normal.
        texto = parrafo.replace(
            "**",
            "",
        )

        contenido.append(
            Paragraph(
                texto,
                estilos["texto"],
            )
        )

    contenido.extend(
        [
            Spacer(
                1,
                0.35 * cm,
            ),
            Paragraph(
                "Productos que requieren atención",
                estilos["seccion"],
            ),
            construir_tabla_alertas_pdf(
                tabla_alertas
            ),
            Spacer(
                1,
                0.7 * cm,
            ),
            Paragraph(
                "Nota metodológica",
                estilos["seccion"],
            ),
            Paragraph(
                (
                    "Este análisis utiliza reglas de negocio "
                    "basadas en stock, ventas de los últimos "
                    "30 días, margen y cobertura estimada. "
                    "No constituye una garantía de ventas ni "
                    "sustituye el criterio comercial de la empresa."
                ),
                estilos["nota"],
            ),
        ]
    )

    documento.build(
        contenido,
        onFirstPage=agregar_numero_pagina,
        onLaterPages=agregar_numero_pagina,
    )

    return str(
        ruta_salida
    )