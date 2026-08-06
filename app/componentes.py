"""
Componentes visuales reutilizables de ModaPredict AI.
"""

from __future__ import annotations

import base64
from html import escape
from pathlib import Path
from typing import Any

# ==========================================================
# RECURSOS VISUALES
# ==========================================================

RUTA_ASSETS = (
    Path(__file__).resolve().parent
    / "assets"
)

RUTA_LOGO = (
    RUTA_ASSETS
    / "logo_modapredict.png"
)


def obtener_logo_base64() -> str:
    """
    Convierte el logo en una imagen embebida en HTML.

    Esto permite mostrarlo dentro de Gradio sin depender
    de una URL externa.
    """

    if not RUTA_LOGO.exists():
        return ""

    contenido = base64.b64encode(
        RUTA_LOGO.read_bytes()
    ).decode("utf-8")

    return (
        "data:image/png;base64,"
        + contenido
    )
# ==========================================================
# PORTADA
# ==========================================================

def construir_portada() -> str:
    """
    Genera la portada premium de ModaPredict AI.
    """

    logo = obtener_logo_base64()

    logo_html = ""

    if logo:
        logo_html = f"""
        <div class="hero-logo-wrapper">
            <img
                class="hero-logo"
                src="{logo}"
                alt="ModaPredict AI"
            />
        </div>
        """

    return f"""
    <section id="hero">

        <div class="hero-glow hero-glow-left"></div>
        <div class="hero-glow hero-glow-right"></div>

        <div class="hero-content">

            {logo_html}

            <div id="hero-badge">
                Plataforma de inteligencia comercial
            </div>

            <h1>
                Decisiones de moda respaldadas por datos
            </h1>

            <p class="hero-description">
                Identifica productos y categorías con mayor
                oportunidad comercial mediante tendencias,
                clima, precios y Machine Learning.
            </p>

            <div class="hero-highlights">

                <div class="hero-highlight">
                    <span class="highlight-icon">◆</span>
                    Recomendaciones por ciudad
                </div>

                <div class="hero-highlight">
                    <span class="highlight-icon">◆</span>
                    Análisis para emprendedores
                </div>

                <div class="hero-highlight">
                    <span class="highlight-icon">◆</span>
                    Dashboard empresarial
                </div>

                <div class="hero-highlight">
                    <span class="highlight-icon">◆</span>
                    ModaPredict Advisor
                </div>

            </div>

        </div>

    </section>
    """


# ==========================================================
# SELECTOR DE PERFIL
# ==========================================================

def construir_bienvenida_perfil(
    perfil: str,
) -> str:
    """Genera un mensaje según el perfil elegido."""

    if perfil == "Empresa":
        return """
        <div class="profile-welcome enterprise-welcome">
            <div class="profile-icon">🏢</div>

            <div>
                <h3>Experiencia para empresas</h3>

                <p>
                    Accede a indicadores ejecutivos,
                    comparaciones por ciudad, categorías,
                    marcas y desempeño del modelo.
                </p>
            </div>
        </div>
        """

    return """
    <div class="profile-welcome entrepreneur-welcome">
        <div class="profile-icon">🚀</div>

        <div>
            <h3>Experiencia para emprendedores</h3>

            <p>
                Encuentra productos y categorías con mejor
                oportunidad comercial de forma clara,
                cercana y fácil de entender.
            </p>
        </div>
    </div>
    """


# ==========================================================
# ENCABEZADOS
# ==========================================================

def construir_encabezado_seccion(
    titulo: str,
    subtitulo: str,
    etiqueta: str | None = None,
) -> str:
    """Genera un encabezado reutilizable."""

    titulo_seguro = escape(
        str(titulo)
    )

    subtitulo_seguro = escape(
        str(subtitulo)
    )

    etiqueta_html = ""

    if etiqueta:
        etiqueta_html = f"""
        <div class="section-eyebrow">
            {escape(str(etiqueta))}
        </div>
        """

    return f"""
    <header class="section-header">
        {etiqueta_html}

        <h2 class="section-title">
            {titulo_seguro}
        </h2>

        <p class="section-subtitle">
            {subtitulo_seguro}
        </p>
    </header>
    """


# ==========================================================
# BLOQUES INFORMATIVOS
# ==========================================================

def construir_explicacion_oportunidad() -> str:
    """
    Explica de manera sencilla qué significa
    la oportunidad comercial.
    """

    return """
    <div class="info-box">
        <div class="info-icon">💡</div>

        <div>
            <h4>¿Qué significa oportunidad comercial?</h4>

            <p>
                Es una estimación del potencial que tiene
                un producto o categoría dentro del catálogo.
                Considera tendencias, clima, precio, marca,
                representatividad y el análisis del modelo.
            </p>

            <p class="info-note">
                No representa ventas garantizadas. Úsala como
                apoyo para comparar opciones antes de comprar.
            </p>
        </div>
    </div>
    """


def construir_escala_oportunidad() -> str:
    """Muestra la escala visual para emprendedores."""

    return """
    <div class="opportunity-scale">
        <div class="scale-item">
            <span class="scale-dot scale-excellent"></span>
            <div>
                <strong>Excelente oportunidad</strong>
                <small>★★★★★ · Prioridad muy alta</small>
            </div>
        </div>

        <div class="scale-item">
            <span class="scale-dot scale-good"></span>
            <div>
                <strong>Buena oportunidad</strong>
                <small>★★★★☆ · Vale la pena revisarla</small>
            </div>
        </div>

        <div class="scale-item">
            <span class="scale-dot scale-medium"></span>
            <div>
                <strong>Oportunidad moderada</strong>
                <small>★★★☆☆ · Comparar antes de decidir</small>
            </div>
        </div>

        <div class="scale-item">
            <span class="scale-dot scale-limited"></span>
            <div>
                <strong>Oportunidad limitada</strong>
                <small>★★☆☆☆ · No es prioridad</small>
            </div>
        </div>

        <div class="scale-item">
            <span class="scale-dot scale-low"></span>
            <div>
                <strong>Baja oportunidad</strong>
                <small>★☆☆☆☆ · Conviene revisar alternativas</small>
            </div>
        </div>
    </div>
    """


# ==========================================================
# ADVERTENCIAS
# ==========================================================

def construir_advertencia_modelo(
    advertencia: str,
) -> str:
    """Muestra la limitación principal del modelo."""

    return f"""
    <div class="warning-box">
        <div class="warning-icon">⚠️</div>

        <div>
            <h4>Importante</h4>

            <p>
                {escape(str(advertencia))}
            </p>

            <p>
                Las recomendaciones deben complementarse con
                margen, disponibilidad, inventario, logística
                y conocimiento del mercado.
            </p>
        </div>
    </div>
    """


def construir_aviso_chat() -> str:
    """Explica claramente el alcance del chat."""

    return """
    <div class="chat-scope-box">
        <div class="chat-scope-icon">💬</div>

        <div>
            <h4>Chat especializado en ModaPredict AI</h4>

            <p>
                Puedes preguntar sobre productos, precios,
                categorías, marcas, ciudades, clima,
                tendencias, presupuestos, recomendaciones
                y métricas del proyecto.
            </p>

            <p class="chat-scope-note">
                Para mantener respuestas útiles, el chat
                redirigirá amablemente cualquier tema que
                no esté relacionado con ModaPredict AI.
            </p>
        </div>
    </div>
    """


# ==========================================================
# ESTADOS VACÍOS
# ==========================================================

def construir_estado_vacio(
    titulo: str = "No encontramos resultados",
    mensaje: str = (
        "Prueba cambiando los filtros o ampliando "
        "el rango de precio."
    ),
) -> str:
    """Genera un estado vacío amigable."""

    return f"""
    <div class="empty-state">
        <div class="empty-icon">🔍</div>

        <h3>
            {escape(str(titulo))}
        </h3>

        <p>
            {escape(str(mensaje))}
        </p>
    </div>
    """


# ==========================================================
# RESUMEN TÉCNICO PARA EMPRESA
# ==========================================================

def construir_resumen_tecnico_modelo(
    resumen: dict[str, Any],
) -> str:
    """Construye una ficha técnica del modelo."""

    modelo = escape(
        str(
            resumen.get(
                "modelo",
                "HistGradientBoosting",
            )
        )
    )

    experimento = escape(
        str(
            resumen.get(
                "experimento",
                "B",
            )
        )
    )

    registros = int(
        resumen.get(
            "registros",
            0,
        )
    )

    productos = int(
        resumen.get(
            "productos",
            0,
        )
    )

    variables = int(
        resumen.get(
            "variables",
            0,
        )
    )

    return f"""
    <div class="technical-grid">
        <div class="technical-card">
            <span>Modelo final</span>
            <strong>{modelo}</strong>
        </div>

        <div class="technical-card">
            <span>Experimento</span>
            <strong>{experimento}</strong>
        </div>

        <div class="technical-card">
            <span>Registros</span>
            <strong>{registros:,}</strong>
        </div>

        <div class="technical-card">
            <span>Productos únicos</span>
            <strong>{productos:,}</strong>
        </div>

        <div class="technical-card">
            <span>Variables predictoras</span>
            <strong>{variables:,}</strong>
        </div>
    </div>
    """


def construir_metricas_modelo() -> str:
    """Muestra las métricas finales validadas."""

    return """
    <div class="metrics-grid">
        <div class="metric-card">
            <span class="metric-label">MAE de prueba</span>
            <strong class="metric-value">0.5576</strong>
            <small>Error absoluto promedio</small>
        </div>

        <div class="metric-card">
            <span class="metric-label">RMSE de prueba</span>
            <strong class="metric-value">1.2641</strong>
            <small>Penaliza errores grandes</small>
        </div>

        <div class="metric-card">
            <span class="metric-label">R² de prueba</span>
            <strong class="metric-value">0.9895</strong>
            <small>Variabilidad explicada</small>
        </div>

        <div class="metric-card">
            <span class="metric-label">MAE validación</span>
            <strong class="metric-value">0.5029</strong>
            <small>Promedio de cinco folds</small>
        </div>
    </div>
    """


# ==========================================================
# EJEMPLOS PARA EL CHAT
# ==========================================================

def construir_ejemplos_chat(
    perfil: str,
) -> str:
    """Muestra preguntas sugeridas según el perfil."""

    if perfil == "Empresa":
        ejemplos = [
            "Compara Toluca y Cancún para sandalias.",
            "¿Qué categorías tienen mejor oportunidad?",
            "Explícame las métricas del modelo.",
            "¿Qué ciudad presenta la mejor señal comercial?",
        ]
    else:
        ejemplos = [
            "¿Qué me conviene vender en Toluca?",
            "Tengo $15,000 para empezar.",
            "Compara playeras entre Cancún y Monterrey.",
            "¿Por qué recomiendas este producto?",
        ]

    elementos = "".join(
        f"""
        <div class="prompt-example">
            {escape(ejemplo)}
        </div>
        """
        for ejemplo in ejemplos
    )

    return f"""
    <div class="prompt-examples">
        <p class="prompt-examples-title">
            Puedes preguntarme:
        </p>

        <div class="prompt-examples-grid">
            {elementos}
        </div>
    </div>
    """


# ==========================================================
# PIE DE PÁGINA
# ==========================================================

def construir_pie_pagina() -> str:
    """
    Genera el pie de página oficial.
    """

    logo = obtener_logo_base64()

    logo_html = ""

    if logo:
        logo_html = f"""
        <img
            class="footer-logo"
            src="{logo}"
            alt="ModaPredict AI"
        />
        """

    return f"""
    <footer class="app-footer">

        <div class="footer-brand">
            {logo_html}

            <div>
                <strong>ModaPredict AI</strong>

                <span>
                    Data · Trends · Decisions
                </span>
            </div>
        </div>

        <div class="footer-description">
            <p>
                Plataforma desarrollada con información de
                catálogo, Google Trends, clima, reglas de
                negocio y Machine Learning.
            </p>

            <small>
                Las recomendaciones son orientativas y no
                representan una garantía de ventas.
            </small>
        </div>

    </footer>
    """