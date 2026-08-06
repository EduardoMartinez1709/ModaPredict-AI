# ==========================================================
# MODAPREDICT AI — SISTEMA DE DISEÑO
# ==========================================================

CSS_PERSONALIZADO = """
/* ========================================================
   VARIABLES VISUALES
   ======================================================== */

:root {
    --mp-black: #050506;
    --mp-black-soft: #0b0c0f;
    --mp-surface: #111217;
    --mp-surface-light: #17191f;
    --mp-surface-hover: #1d2027;

    --mp-gold: #d6b36a;
    --mp-gold-light: #f2d89b;
    --mp-gold-dark: #9c7939;

    --mp-silver: #d7d9de;
    --mp-silver-dark: #8e929b;

    --mp-white: #f7f7f8;
    --mp-text: #eeeeef;
    --mp-text-soft: #a7a9b0;
    --mp-text-muted: #70737b;

    --mp-border: rgba(214, 179, 106, 0.18);
    --mp-border-soft: rgba(255, 255, 255, 0.08);

    --mp-success: #61c795;
    --mp-warning: #e7bd5a;
    --mp-danger: #d76a6a;

    --mp-radius-small: 12px;
    --mp-radius-medium: 18px;
    --mp-radius-large: 28px;

    --mp-shadow:
        0 18px 55px rgba(0, 0, 0, 0.38);

    --mp-shadow-gold:
        0 15px 45px rgba(214, 179, 106, 0.12);
}


/* ========================================================
   CONTENEDOR PRINCIPAL
   ======================================================== */

html,
body {
    background: var(--mp-black) !important;
}

.gradio-container {
    max-width: 1500px !important;
    margin: 0 auto !important;
    padding: 24px !important;

    color: var(--mp-text) !important;

    background:
        radial-gradient(
            circle at 15% 5%,
            rgba(214, 179, 106, 0.08),
            transparent 24%
        ),
        radial-gradient(
            circle at 88% 8%,
            rgba(215, 217, 222, 0.05),
            transparent 20%
        ),
        linear-gradient(
            180deg,
            #050506 0%,
            #090a0d 55%,
            #050506 100%
        ) !important;

    font-family:
        Inter,
        ui-sans-serif,
        system-ui,
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif !important;
}


/* ========================================================
   PORTADA
   ======================================================== */

#hero {
    position: relative;
    min-height: 650px;

    display: flex;
    align-items: center;
    justify-content: center;

    padding: 55px 40px;
    margin-bottom: 30px;

    overflow: hidden;

    border: 1px solid var(--mp-border);
    border-radius: 34px;

    background:
        linear-gradient(
            145deg,
            rgba(17, 18, 23, 0.98),
            rgba(5, 5, 6, 0.98)
        );

    box-shadow:
        0 30px 90px rgba(0, 0, 0, 0.55),
        inset 0 1px 0 rgba(255, 255, 255, 0.05);
}

.hero-content {
    position: relative;
    z-index: 2;

    width: 100%;
    max-width: 980px;

    text-align: center;
}

.hero-logo-wrapper {
    display: flex;
    justify-content: center;

    margin-bottom: 16px;
}

.hero-logo {
    width: min(360px, 75vw);
    height: auto;

    object-fit: contain;

    filter:
        drop-shadow(
            0 18px 35px rgba(0, 0, 0, 0.7)
        );

    animation:
        logoEntrance 1.1s ease-out both,
        logoGlow 4s ease-in-out infinite;
}

#hero-badge {
    display: inline-flex;
    align-items: center;

    padding: 9px 17px;
    margin-bottom: 22px;

    border: 1px solid rgba(214, 179, 106, 0.32);
    border-radius: 999px;

    background:
        rgba(214, 179, 106, 0.08);

    color: var(--mp-gold-light);

    font-size: 12px;
    font-weight: 800;

    letter-spacing: 1.4px;
    text-transform: uppercase;
}

#hero h1 {
    max-width: 850px;
    margin: 0 auto 20px;

    color: var(--mp-white);

    font-size: clamp(38px, 5vw, 68px);
    line-height: 1.03;
    font-weight: 800;

    letter-spacing: -2px;

    background:
        linear-gradient(
            90deg,
            var(--mp-gold-light),
            var(--mp-white),
            var(--mp-silver)
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-description {
    max-width: 760px;
    margin: 0 auto;

    color: var(--mp-text-soft);

    font-size: 18px;
    line-height: 1.75;
}

.hero-highlights {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;

    gap: 12px;

    margin-top: 30px;
}

.hero-highlight {
    display: inline-flex;
    align-items: center;

    gap: 8px;

    padding: 10px 14px;

    border: 1px solid var(--mp-border-soft);
    border-radius: 999px;

    background:
        rgba(255, 255, 255, 0.035);

    color: var(--mp-silver);

    font-size: 13px;
    font-weight: 600;
}

.highlight-icon {
    color: var(--mp-gold);
    font-size: 9px;
}

.hero-glow {
    position: absolute;

    width: 430px;
    height: 430px;

    border-radius: 50%;

    filter: blur(100px);
    opacity: 0.13;

    pointer-events: none;
}

.hero-glow-left {
    left: -160px;
    top: -180px;

    background: var(--mp-gold);
}

.hero-glow-right {
    right: -180px;
    bottom: -210px;

    background: var(--mp-silver);
}


/* ========================================================
   ANIMACIONES
   ======================================================== */

@keyframes logoEntrance {
    from {
        opacity: 0;
        transform:
            translateY(20px)
            scale(0.94);
    }

    to {
        opacity: 1;
        transform:
            translateY(0)
            scale(1);
    }
}

@keyframes logoGlow {
    0%,
    100% {
        filter:
            drop-shadow(
                0 15px 30px rgba(0, 0, 0, 0.65)
            );
    }

    50% {
        filter:
            drop-shadow(
                0 18px 38px rgba(214, 179, 106, 0.20)
            );
    }
}

@keyframes fadeUp {
    from {
        opacity: 0;
        transform: translateY(14px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}


/* ========================================================
   ENCABEZADOS
   ======================================================== */

.section-header {
    margin: 10px 0 22px;

    animation: fadeUp 0.55s ease-out both;
}

.section-eyebrow {
    margin-bottom: 7px;

    color: var(--mp-gold);

    font-size: 11px;
    font-weight: 800;

    letter-spacing: 1.5px;
    text-transform: uppercase;
}

.section-title {
    margin: 0 0 8px;

    color: var(--mp-white);

    font-size: clamp(27px, 3vw, 39px);
    line-height: 1.1;
    font-weight: 800;

    letter-spacing: -1px;
}

.section-subtitle {
    max-width: 760px;

    margin: 0;

    color: var(--mp-text-soft);

    font-size: 15px;
    line-height: 1.65;
}


/* ========================================================
   PANELES
   ======================================================== */

.panel-premium,
.block,
.form {
    border: 1px solid var(--mp-border-soft) !important;
    border-radius: var(--mp-radius-large) !important;

    background:
        linear-gradient(
            145deg,
            rgba(23, 25, 31, 0.96),
            rgba(14, 15, 19, 0.96)
        ) !important;

    box-shadow: var(--mp-shadow) !important;
}


/* ========================================================
   SELECTOR DE PERFIL
   ======================================================== */

.profile-welcome {
    display: flex;
    align-items: center;

    gap: 18px;

    padding: 22px;

    border: 1px solid var(--mp-border);
    border-radius: var(--mp-radius-medium);

    background:
        linear-gradient(
            135deg,
            rgba(214, 179, 106, 0.08),
            rgba(255, 255, 255, 0.02)
        );

    box-shadow: var(--mp-shadow-gold);
}

.profile-icon {
    display: flex;
    align-items: center;
    justify-content: center;

    min-width: 54px;
    height: 54px;

    border: 1px solid var(--mp-border);
    border-radius: 16px;

    background: rgba(214, 179, 106, 0.08);

    font-size: 25px;
}

.profile-welcome h3 {
    margin: 0 0 5px;

    color: var(--mp-white);

    font-size: 18px;
}

.profile-welcome p {
    margin: 0;

    color: var(--mp-text-soft);

    font-size: 14px;
    line-height: 1.55;
}


/* ========================================================
   KPIs
   ======================================================== */

.kpi-grid {
    display: grid;

    grid-template-columns:
        repeat(auto-fit, minmax(190px, 1fr));

    gap: 15px;

    margin: 18px 0 25px;
}

.kpi-card {
    position: relative;

    min-height: 140px;

    padding: 20px;

    overflow: hidden;

    border: 1px solid var(--mp-border-soft);
    border-radius: var(--mp-radius-medium);

    background:
        linear-gradient(
            145deg,
            rgba(24, 26, 32, 0.96),
            rgba(13, 14, 18, 0.96)
        );

    box-shadow:
        0 15px 40px rgba(0, 0, 0, 0.30);

    transition:
        transform 0.25s ease,
        border-color 0.25s ease,
        box-shadow 0.25s ease;
}

.kpi-card:hover {
    transform: translateY(-4px);

    border-color:
        rgba(214, 179, 106, 0.35);

    box-shadow:
        0 20px 48px rgba(0, 0, 0, 0.42);
}

.kpi-label {
    color: var(--mp-text-muted);

    font-size: 11px;
    font-weight: 800;

    letter-spacing: 1px;
    text-transform: uppercase;
}

.kpi-value {
    margin-top: 10px;

    color: var(--mp-white);

    font-size: 29px;
    line-height: 1.05;
    font-weight: 800;

    letter-spacing: -0.8px;
}

.kpi-text {
    font-size: 21px;
    line-height: 1.2;
}

.kpi-stars {
    margin-top: 10px;

    color: var(--mp-gold-light);

    font-size: 22px;
    letter-spacing: 3px;
}

.kpi-subtitle {
    margin-top: 9px;

    color: var(--mp-text-soft);

    font-size: 12px;
    line-height: 1.5;
}

.oportunidad-card {
    border-color:
        rgba(214, 179, 106, 0.28);

    background:
        radial-gradient(
            circle at top right,
            rgba(214, 179, 106, 0.13),
            transparent 40%
        ),
        linear-gradient(
            145deg,
            #19191c,
            #0d0e11
        );
}


/* ========================================================
   OPORTUNIDAD COMERCIAL
   ======================================================== */

.opportunity-box {
    margin-top: 15px;
    padding: 16px;

    border: 1px solid var(--mp-border-soft);
    border-radius: var(--mp-radius-small);

    background: rgba(255, 255, 255, 0.025);
}

.opportunity-level {
    color: var(--mp-white);

    font-size: 17px;
    font-weight: 800;
}

.opportunity-stars {
    margin: 5px 0;

    color: var(--mp-gold-light);

    font-size: 20px;
    letter-spacing: 3px;
}

.opportunity-message {
    color: var(--mp-text-soft);

    font-size: 12px;
    line-height: 1.5;
}

.oportunidad-excelente {
    border-color: rgba(97, 199, 149, 0.4);
}

.oportunidad-buena {
    border-color: rgba(214, 179, 106, 0.42);
}

.oportunidad-moderada {
    border-color: rgba(231, 189, 90, 0.34);
}

.oportunidad-limitada,
.oportunidad-baja {
    border-color: rgba(215, 106, 106, 0.30);
}


/* ========================================================
   TARJETAS DE PRODUCTOS
   ======================================================== */

.products-grid {
    display: grid;

    grid-template-columns:
        repeat(auto-fit, minmax(270px, 1fr));

    gap: 20px;
}

.product-card {
    overflow: hidden;

    border: 1px solid var(--mp-border-soft);
    border-radius: 22px;

    background:
        linear-gradient(
            145deg,
            rgba(24, 26, 32, 0.98),
            rgba(11, 12, 15, 0.98)
        );

    box-shadow:
        0 20px 55px rgba(0, 0, 0, 0.40);

    transition:
        transform 0.28s ease,
        border-color 0.28s ease,
        box-shadow 0.28s ease;
}

.product-card:hover {
    transform: translateY(-7px);

    border-color:
        rgba(214, 179, 106, 0.38);

    box-shadow:
        0 26px 65px rgba(0, 0, 0, 0.52);
}

.product-image {
    width: 100%;
    height: 290px;

    object-fit: cover;

    background: var(--mp-surface-light);
}

.product-body {
    padding: 20px;
}

.product-category {
    color: var(--mp-gold);

    font-size: 10px;
    font-weight: 800;

    letter-spacing: 1.1px;
    text-transform: uppercase;
}

.product-title {
    margin: 9px 0 7px;

    color: var(--mp-white);

    font-size: 17px;
    line-height: 1.35;
}

.product-meta {
    margin: 0 0 12px;

    color: var(--mp-text-soft);

    font-size: 12px;
}

.product-explanation {
    margin-top: 13px;

    color: var(--mp-text-soft);

    font-size: 12px;
    line-height: 1.55;
}

.product-link {
    display: inline-flex;

    margin-top: 14px;

    color: var(--mp-gold-light) !important;

    font-size: 13px;
    font-weight: 800;

    text-decoration: none !important;
}

.product-link:hover {
    color: var(--mp-white) !important;
}


/* ========================================================
   BLOQUES INFORMATIVOS
   ======================================================== */

.info-box,
.warning-box,
.chat-scope-box {
    display: flex;

    gap: 16px;

    padding: 20px;
    margin: 16px 0;

    border: 1px solid var(--mp-border-soft);
    border-radius: var(--mp-radius-medium);

    background:
        rgba(255, 255, 255, 0.025);
}

.info-box {
    border-color: rgba(214, 179, 106, 0.24);
}

.warning-box {
    border-color: rgba(231, 189, 90, 0.27);
}

.chat-scope-box {
    border-color: rgba(215, 217, 222, 0.20);
}

.info-icon,
.warning-icon,
.chat-scope-icon {
    font-size: 25px;
}

.info-box h4,
.warning-box h4,
.chat-scope-box h4 {
    margin: 0 0 6px;

    color: var(--mp-white);
}

.info-box p,
.warning-box p,
.chat-scope-box p {
    margin: 0 0 5px;

    color: var(--mp-text-soft);

    font-size: 13px;
    line-height: 1.55;
}

.info-note,
.chat-scope-note {
    color: var(--mp-text-muted) !important;

    font-size: 11px !important;
}


/* ========================================================
   ESCALA DE OPORTUNIDAD
   ======================================================== */

.opportunity-scale {
    display: grid;

    grid-template-columns:
        repeat(auto-fit, minmax(210px, 1fr));

    gap: 10px;
}

.scale-item {
    display: flex;
    align-items: center;

    gap: 11px;

    padding: 13px;

    border: 1px solid var(--mp-border-soft);
    border-radius: 14px;

    background: rgba(255, 255, 255, 0.025);
}

.scale-item strong {
    display: block;

    color: var(--mp-white);

    font-size: 12px;
}

.scale-item small {
    color: var(--mp-text-muted);

    font-size: 10px;
}

.scale-dot {
    width: 11px;
    height: 11px;

    border-radius: 50%;
}

.scale-excellent {
    background: #61c795;
}

.scale-good {
    background: var(--mp-gold);
}

.scale-medium {
    background: var(--mp-warning);
}

.scale-limited {
    background: #de885e;
}

.scale-low {
    background: var(--mp-danger);
}


/* ========================================================
   BOTONES
   ======================================================== */

button.primary,
.primary-button {
    min-height: 48px !important;

    border: none !important;
    border-radius: 14px !important;

    background:
        linear-gradient(
            110deg,
            var(--mp-gold-dark),
            var(--mp-gold-light),
            var(--mp-gold)
        ) !important;

    color: #080808 !important;

    font-weight: 900 !important;

    box-shadow:
        0 12px 28px rgba(214, 179, 106, 0.18) !important;

    transition:
        transform 0.20s ease,
        box-shadow 0.20s ease !important;
}

button.primary:hover,
.primary-button:hover {
    transform: translateY(-2px);

    box-shadow:
        0 16px 34px rgba(214, 179, 106, 0.28) !important;
}

.secondary-button,
button.secondary {
    min-height: 48px !important;

    border:
        1px solid var(--mp-border) !important;

    border-radius: 14px !important;

    background:
        rgba(255, 255, 255, 0.025) !important;

    color: var(--mp-white) !important;

    font-weight: 800 !important;
}


/* ========================================================
   CAMPOS Y SELECTORES
   ======================================================== */

input,
textarea,
select {
    border-color:
        var(--mp-border-soft) !important;

    border-radius:
        var(--mp-radius-small) !important;

    background:
        rgba(8, 9, 12, 0.95) !important;

    color:
        var(--mp-text) !important;
}

input:focus,
textarea:focus,
select:focus {
    border-color:
        rgba(214, 179, 106, 0.55) !important;

    box-shadow:
        0 0 0 3px rgba(214, 179, 106, 0.08) !important;
}

label,
.label-wrap {
    color:
        var(--mp-silver) !important;
}


/* ========================================================
   CHAT
   ======================================================== */

.chatbot {
    border:
        1px solid var(--mp-border-soft) !important;

    border-radius:
        var(--mp-radius-large) !important;

    background:
        rgba(8, 9, 12, 0.88) !important;
}

.message.user {
    border:
        1px solid rgba(214, 179, 106, 0.28) !important;

    background:
        linear-gradient(
            135deg,
            rgba(214, 179, 106, 0.14),
            rgba(214, 179, 106, 0.06)
        ) !important;

    color: var(--mp-white) !important;
}

.message.bot {
    border:
        1px solid var(--mp-border-soft) !important;

    background:
        rgba(255, 255, 255, 0.035) !important;

    color: var(--mp-text) !important;
}

.prompt-examples {
    margin-top: 14px;
}

.prompt-examples-title {
    color: var(--mp-text-soft);

    font-size: 12px;
    font-weight: 700;
}

.prompt-examples-grid {
    display: grid;

    grid-template-columns:
        repeat(auto-fit, minmax(220px, 1fr));

    gap: 9px;
}

.prompt-example {
    padding: 11px 13px;

    border:
        1px solid var(--mp-border-soft);

    border-radius: 12px;

    background:
        rgba(255, 255, 255, 0.025);

    color:
        var(--mp-silver);

    font-size: 11px;
}


/* ========================================================
   MÉTRICAS TÉCNICAS
   ======================================================== */

.technical-grid,
.metrics-grid {
    display: grid;

    grid-template-columns:
        repeat(auto-fit, minmax(180px, 1fr));

    gap: 13px;
}

.technical-card,
.metric-card {
    padding: 18px;

    border: 1px solid var(--mp-border-soft);
    border-radius: 16px;

    background:
        linear-gradient(
            145deg,
            rgba(24, 26, 32, 0.96),
            rgba(13, 14, 18, 0.96)
        );
}

.technical-card span,
.metric-label {
    display: block;

    color: var(--mp-text-muted);

    font-size: 10px;
    font-weight: 800;

    letter-spacing: 0.9px;
    text-transform: uppercase;
}

.technical-card strong,
.metric-value {
    display: block;

    margin-top: 7px;

    color: var(--mp-white);

    font-size: 22px;
    font-weight: 800;
}

.metric-card small {
    color: var(--mp-text-muted);

    font-size: 10px;
}


/* ========================================================
   TABLAS
   ======================================================== */

table {
    color: var(--mp-text) !important;

    background: transparent !important;
}

thead {
    background:
        rgba(214, 179, 106, 0.08) !important;
}

th {
    color:
        var(--mp-gold-light) !important;

    font-size: 11px !important;
}

td {
    border-color:
        var(--mp-border-soft) !important;
}


/* ========================================================
   ESTADO VACÍO
   ======================================================== */

.empty-state {
    padding: 45px 25px;

    text-align: center;

    border:
        1px dashed var(--mp-border);

    border-radius:
        var(--mp-radius-large);

    background:
        rgba(255, 255, 255, 0.02);
}

.empty-icon {
    margin-bottom: 10px;

    font-size: 34px;
}

.empty-state h3 {
    color: var(--mp-white);
}

.empty-state p {
    color: var(--mp-text-soft);
}


/* ========================================================
   PIE DE PÁGINA
   ======================================================== */

.app-footer {
    display: flex;
    align-items: center;
    justify-content: space-between;

    gap: 25px;

    margin-top: 45px;
    padding: 25px 5px 12px;

    border-top:
        1px solid var(--mp-border-soft);
}

.footer-brand {
    display: flex;
    align-items: center;

    gap: 13px;
}

.footer-logo {
    width: 66px;
    height: 66px;

    object-fit: contain;

    border-radius: 13px;
}

.footer-brand strong {
    display: block;

    color: var(--mp-white);

    font-size: 14px;
}

.footer-brand span {
    color: var(--mp-gold);

    font-size: 9px;

    letter-spacing: 1.3px;
    text-transform: uppercase;
}

.footer-description {
    max-width: 520px;

    text-align: right;
}

.footer-description p {
    margin: 0 0 5px;

    color: var(--mp-text-soft);

    font-size: 11px;
}

.footer-description small {
    color: var(--mp-text-muted);

    font-size: 9px;
}


/* ========================================================
   OCULTAR ELEMENTOS DE GRADIO
   ======================================================== */

footer:not(.app-footer) {
    display: none !important;
}


/* ========================================================
   RESPONSIVE
   ======================================================== */

@media (max-width: 850px) {

    .gradio-container {
        padding: 13px !important;
    }

    #hero {
        min-height: auto;

        padding: 38px 18px;

        border-radius: 25px;
    }

    #hero h1 {
        letter-spacing: -1px;
    }

    .hero-description {
        font-size: 15px;
    }

    .hero-highlights {
        flex-direction: column;
        align-items: center;
    }

    .kpi-grid {
        grid-template-columns:
            repeat(2, minmax(0, 1fr));
    }

    .app-footer {
        flex-direction: column;

        align-items: flex-start;
    }

    .footer-description {
        text-align: left;
    }
}


@media (max-width: 520px) {

    .kpi-grid {
        grid-template-columns: 1fr;
    }

    .products-grid {
        grid-template-columns: 1fr;
    }

    .hero-logo {
        width: 85vw;
    }

    .profile-welcome {
        align-items: flex-start;
    }
}


/* ========================================================
   AJUSTES FINALES — FONDO NEGRO TOTAL Y TEXTO BLANCO
   Compatibilidad reforzada con Gradio 6
   ======================================================== */

:root {
    color-scheme: dark;
    --body-background-fill: #000000;
    --body-background-fill-dark: #000000;
    --body-text-color: #ffffff;
    --body-text-color-dark: #ffffff;
    --block-background-fill: #0b0b0d;
    --block-background-fill-dark: #0b0b0d;
    --block-label-text-color: #ffffff;
    --block-label-text-color-dark: #ffffff;
    --block-title-text-color: #ffffff;
    --block-title-text-color-dark: #ffffff;
    --input-background-fill: #050505;
    --input-background-fill-dark: #050505;
    --input-placeholder-color: #8f9299;
    --input-placeholder-color-dark: #8f9299;
}

html, body, #root, gradio-app, .gradio-container, main, .app, .contain, .wrap {
    background: #000000 !important;
    color: #ffffff !important;
}

html, body, #root, gradio-app {
    width: 100% !important;
    min-height: 100% !important;
    margin: 0 !important;
}

body { overflow-x: hidden; }

.gradio-container {
    width: 100% !important;
    max-width: none !important;
    min-height: 100vh !important;
    margin: 0 !important;
    padding: 26px clamp(16px, 4vw, 52px) !important;
    background:
        radial-gradient(circle at 16% 4%, rgba(214,179,106,.08), transparent 23%),
        radial-gradient(circle at 86% 8%, rgba(230,231,234,.045), transparent 20%),
        #000000 !important;
}

.gradio-container h1, .gradio-container h2, .gradio-container h3,
.gradio-container h4, .gradio-container h5, .gradio-container h6,
.gradio-container p, .gradio-container li, .gradio-container strong,
.gradio-container small, .gradio-container label, .gradio-container .prose,
.gradio-container .markdown, .gradio-container .markdown p,
.gradio-container .markdown h1, .gradio-container .markdown h2,
.gradio-container .markdown h3, .gradio-container .markdown h4 {
    color: #ffffff !important;
}

.section-subtitle, .hero-description, .profile-welcome p,
.info-box p, .warning-box p, .chat-scope-box p, .product-meta,
.product-explanation, .kpi-subtitle, .opportunity-message,
.footer-description p { color: #d2d3d7 !important; }

.section-eyebrow, .highlight-icon, .product-category,
.footer-brand span, .product-link { color: var(--mp-gold) !important; }

.gradio-container .row, .gradio-container .column, .gradio-container .tabs,
.gradio-container .tabitem { background-color: transparent !important; }

.gradio-container .block, .gradio-container .form, .panel-premium {
    background: linear-gradient(145deg, rgba(17,18,22,.98), rgba(7,7,9,.98)) !important;
    border-color: rgba(255,255,255,.11) !important;
}

.gradio-container .tab-nav, .gradio-container [role="tablist"] {
    background: #000000 !important;
    border-bottom: 1px solid rgba(255,255,255,.13) !important;
}

.gradio-container button[role="tab"] {
    background: transparent !important;
    color: #d2d3d7 !important;
    border-bottom: 2px solid transparent !important;
}
.gradio-container button[role="tab"]:hover { color: #ffffff !important; }
.gradio-container button[role="tab"][aria-selected="true"] {
    color: var(--mp-gold-light) !important;
    border-bottom-color: var(--mp-gold) !important;
}

.gradio-container .wrap label, .gradio-container .radio-group label,
.gradio-container .checkbox-group label {
    background: #101115 !important;
    color: #ffffff !important;
    border: 1px solid rgba(255,255,255,.13) !important;
    border-radius: 10px !important;
}
.gradio-container .wrap label:hover, .gradio-container .radio-group label:hover {
    background: #17181d !important;
    border-color: rgba(214,179,106,.42) !important;
}
.gradio-container input[type="radio"], .gradio-container input[type="checkbox"] {
    accent-color: var(--mp-gold) !important;
}

.gradio-container input, .gradio-container textarea, .gradio-container select {
    background: #050505 !important;
    color: #ffffff !important;
    border-color: rgba(255,255,255,.13) !important;
}
.gradio-container input::placeholder, .gradio-container textarea::placeholder {
    color: #8f9299 !important;
}
.gradio-container label, .gradio-container .label-wrap,
.gradio-container .label-wrap span, .gradio-container .info {
    color: #d2d3d7 !important;
}

.chatbot, .gradio-container .chatbot { background: #050505 !important; }
.message.user, .gradio-container .message.user {
    background: linear-gradient(135deg, rgba(214,179,106,.15), rgba(214,179,106,.07)) !important;
    color: #ffffff !important;
}
.message.bot, .gradio-container .message.bot {
    background: #111216 !important;
    color: #ffffff !important;
}
.message.user *, .message.bot * { color: #ffffff !important; }

.gradio-container table, .gradio-container .table-wrap,
.gradio-container .dataframe, .gradio-container [data-testid="dataframe"] {
    background: #050505 !important;
    color: #ffffff !important;
}
.gradio-container thead, .gradio-container th {
    background: rgba(214,179,106,.10) !important;
    color: var(--mp-gold-light) !important;
}
.gradio-container tbody, .gradio-container tr, .gradio-container td {
    background: #0b0b0d !important;
    color: #ffffff !important;
    border-color: rgba(255,255,255,.10) !important;
}
.gradio-container tr:hover td { background: #15161a !important; }

.gradio-container details, .gradio-container .accordion, .gradio-container summary {
    background: #0b0b0d !important;
    color: #ffffff !important;
    border-color: rgba(255,255,255,.11) !important;
}

.gradio-container > footer, footer:not(.app-footer), .gradio-container .built-with {
    display: none !important;
}

@media (max-width: 850px) { .gradio-container { padding: 14px !important; } }
@media (max-width: 520px) { .gradio-container { padding: 9px !important; } }

/* ==========================================================
   MODAPREDICT AI
   OVERRIDES VISUALES (GRADIO 6)
========================================================== */

/* ---------- Dropdowns ---------- */

.gr-dropdown,
.gradio-dropdown,
[data-testid="dropdown"]{
    background:#111111 !important;
    border:1px solid #3d3d3d !important;
    border-radius:12px !important;
    color:white !important;
}

.gr-dropdown *{
    color:white !important;
}

.gradio-dropdown *{
    color:white !important;
}

.gr-dropdown input{
    color:white !important;
}

.gradio-dropdown input{
    color:white !important;
}

.gr-dropdown ul{
    background:#171717 !important;
}

.gr-dropdown li{
    color:white !important;
}

.gr-dropdown li:hover{
    background:#d4af37 !important;
    color:black !important;
}

/* ---------- Inputs ---------- */

textarea,
input,
.gr-textbox{
    background:#111111 !important;
    color:white !important;

    border-radius:12px !important;
    border:1px solid #3b3b3b !important;

    transition:.25s;
}

textarea:focus,
input:focus{

    border-color:#d4af37 !important;

    box-shadow:
        0 0 10px rgba(212,175,55,.25) !important;
}

/* ---------- Botones ---------- */

button{

    transition:.25s;

}

button:hover{

    transform:translateY(-2px);

    box-shadow:

        0 8px 25px rgba(212,175,55,.18);

}

/* ---------- Accordion ---------- */

.gr-accordion{

    border-radius:18px !important;

    overflow:hidden;

}

/* ---------- Scroll ---------- */

::-webkit-scrollbar{

    width:10px;

    height:10px;

}

::-webkit-scrollbar-track{

    background:#111;

}

::-webkit-scrollbar-thumb{

    background:#d4af37;

    border-radius:100px;

}

::-webkit-scrollbar-thumb:hover{

    background:#f0d472;

}

/* ---------- Chat ---------- */

.message{

    border-radius:18px !important;

    padding:18px !important;

}

.message.user{

    background:#302611 !important;

    border:1px solid #6b5322;

}

.message.bot{

    background:#161616 !important;

    border:1px solid #2e2e2e;

}

/* ---------- Tarjetas ---------- */

.card,
.kpi-card{

    transition:.25s;

}

.card:hover,
.kpi-card:hover{

    transform:translateY(-3px);

    box-shadow:

        0 10px 30px rgba(0,0,0,.35);

}

/* ---------- DataFrame ---------- */

[data-testid="dataframe"]{

    border-radius:18px !important;

    overflow:hidden;

}

/* ---------- AG GRID ---------- */

.ag-root-wrapper{

    border:none !important;

    border-radius:18px !important;

    overflow:hidden;

}

.ag-theme-alpine{

    --ag-background-color:#171717;

    --ag-foreground-color:white;

    --ag-header-background-color:#1f1f1f;

    --ag-header-foreground-color:#d4af37;

    --ag-row-hover-color:#232323;

    --ag-selected-row-background-color:#2f2f2f;

    --ag-border-color:#2b2b2b;

    --ag-odd-row-background-color:#181818;

    --ag-font-size:14px;

}

.ag-header-cell{

    font-weight:700 !important;

}

.ag-row{

    transition:.15s;

}

.ag-row:hover{

    background:#232323 !important;

}

/* ---------- Tabs ---------- */

.tab-nav button{

    transition:.2s;

}

.tab-nav button:hover{

    color:#d4af37 !important;

}

/* ==========================================================
   DROPDOWNS — MENÚ BLANCO CON TEXTO NEGRO
   ========================================================== */

/* Panel flotante donde aparecen las opciones */
.gradio-container [role="listbox"],
.gradio-container ul[role="listbox"],
.gradio-container div[role="listbox"],
body > div[role="listbox"] {
    background: #ffffff !important;
    color: #111111 !important;

    border: 1px solid #d7d7d7 !important;
    border-radius: 10px !important;

    box-shadow:
        0 14px 35px rgba(0, 0, 0, 0.35) !important;
}

/* Cada opción del menú */
.gradio-container [role="option"],
.gradio-container li[role="option"],
body > div [role="option"] {
    background: #ffffff !important;
    color: #111111 !important;

    font-weight: 600 !important;
}

/* Todo el texto interno de las opciones */
.gradio-container [role="option"] *,
.gradio-container li[role="option"] *,
body > div [role="option"] * {
    color: #111111 !important;
}

/* Opción seleccionada */
.gradio-container [role="option"][aria-selected="true"],
.gradio-container li[role="option"][aria-selected="true"],
body > div [role="option"][aria-selected="true"] {
    background: #f0dfb7 !important;
    color: #111111 !important;
}

/* Al pasar el cursor */
.gradio-container [role="option"]:hover,
.gradio-container li[role="option"]:hover,
body > div [role="option"]:hover {
    background: #d6b36a !important;
    color: #080808 !important;
}

/* Campo cerrado: permanece oscuro */
.gradio-container [data-testid="dropdown"] input,
.gradio-container .gr-dropdown input {
    background: #050505 !important;
    color: #ffffff !important;
}


/* ==========================================================
   ESTADO INICIAL DEL RECOMENDADOR
   ========================================================== */

.recommender-empty-state {
    min-height: 390px;

    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;

    margin-top: 15px;

    border-style: solid;

    background:
        radial-gradient(
            circle at center,
            rgba(214, 179, 106, 0.07),
            transparent 50%
        ),
        #080809;
}

.recommender-empty-state h3 {
    margin: 8px 0;

    color: #ffffff !important;
}

.recommender-empty-state p {
    max-width: 460px;

    color: #cfd0d4 !important;

    text-align: center;
    line-height: 1.7;
}

/* ==========================================================
   TABLAS / DATAFRAME — ESTILO LIMPIO MODAPREDICT
   ========================================================== */

/* Contenedor principal */
.gradio-container [data-testid="dataframe"],
.gradio-container .dataframe,
.gradio-container .table-wrap {
    overflow: hidden !important;

    border: 1px solid rgba(214, 179, 106, 0.24) !important;
    border-radius: 18px !important;

    background: #0b0b0d !important;

    box-shadow:
        0 18px 45px rgba(0, 0, 0, 0.35) !important;
}

/* Tabla completa */
.gradio-container [data-testid="dataframe"] table,
.gradio-container .dataframe table {
    width: 100% !important;

    border-collapse: collapse !important;
    border-spacing: 0 !important;

    background: #0b0b0d !important;

    color: #f5f5f7 !important;

    font-family:
        Inter,
        ui-sans-serif,
        system-ui,
        sans-serif !important;

    font-size: 14px !important;
}

/* Encabezado */
.gradio-container [data-testid="dataframe"] thead,
.gradio-container [data-testid="dataframe"] thead tr,
.gradio-container [data-testid="dataframe"] th {
    background:
        linear-gradient(
            180deg,
            #1b1b1f,
            #121216
        ) !important;

    color: #f3d995 !important;
}

/* Celdas de encabezado */
.gradio-container [data-testid="dataframe"] th {
    padding: 14px 16px !important;

    border-right:
        1px solid rgba(255, 255, 255, 0.08) !important;

    border-bottom:
        1px solid rgba(214, 179, 106, 0.26) !important;

    font-size: 12px !important;
    font-weight: 800 !important;

    letter-spacing: 0.35px !important;
    text-transform: none !important;

    white-space: nowrap !important;
}

/* Filas */
.gradio-container [data-testid="dataframe"] tbody tr {
    background: #0d0d10 !important;

    transition:
        background 0.18s ease !important;
}

/* Filas alternadas */
.gradio-container [data-testid="dataframe"] tbody tr:nth-child(even) {
    background: #121216 !important;
}

/* Hover */
.gradio-container [data-testid="dataframe"] tbody tr:hover {
    background: #1a1813 !important;
}

/* Celdas */
.gradio-container [data-testid="dataframe"] td {
    padding: 12px 16px !important;

    border-right:
        1px solid rgba(255, 255, 255, 0.055) !important;

    border-bottom:
        1px solid rgba(255, 255, 255, 0.07) !important;

    background: transparent !important;

    color: #f5f5f7 !important;

    vertical-align: middle !important;
}

/* Elimina los bloques negros internos */
.gradio-container [data-testid="dataframe"] td *,
.gradio-container [data-testid="dataframe"] th *,
.gradio-container .dataframe td *,
.gradio-container .dataframe th * {
    background: transparent !important;

    color: inherit !important;

    box-shadow: none !important;

    text-decoration: none !important;
}

/* Texto dentro de inputs/celdas editables */
.gradio-container [data-testid="dataframe"] input,
.gradio-container [data-testid="dataframe"] textarea {
    width: 100% !important;

    padding: 0 !important;

    border: none !important;

    background: transparent !important;

    color: #f5f5f7 !important;

    font: inherit !important;

    box-shadow: none !important;
}

/* Última columna sin borde derecho */
.gradio-container [data-testid="dataframe"] th:last-child,
.gradio-container [data-testid="dataframe"] td:last-child {
    border-right: none !important;
}

/* Última fila sin borde inferior */
.gradio-container [data-testid="dataframe"] tbody tr:last-child td {
    border-bottom: none !important;
}

/* Scroll horizontal */
.gradio-container [data-testid="dataframe"] .table-wrap,
.gradio-container [data-testid="dataframe"] > div {
    background: #0b0b0d !important;
}

/* Números */
.gradio-container [data-testid="dataframe"] td:nth-child(2),
.gradio-container [data-testid="dataframe"] td:nth-child(4),
.gradio-container [data-testid="dataframe"] td:nth-child(5) {
    font-variant-numeric: tabular-nums !important;
}

/* ==========================================================
   TABLAS HTML MODAPREDICT
   ========================================================== */

.mp-table-wrapper {
    width: 100%;
    overflow-x: auto;

    margin: 18px 0 26px;

    border: 1px solid rgba(214, 179, 106, 0.25);
    border-radius: 20px;

    background: #0b0b0d;

    box-shadow:
        0 18px 48px rgba(0, 0, 0, 0.42);
}

.mp-table {
    width: 100%;
    min-width: 850px;

    border-collapse: collapse;

    background: #0b0b0d;

    color: #f5f5f7;

    font-family:
        Inter,
        ui-sans-serif,
        system-ui,
        sans-serif;
}

.mp-table thead {
    background:
        linear-gradient(
            180deg,
            #1c1c20,
            #121216
        );
}

.mp-table th {
    padding: 16px 18px;

    border-bottom:
        1px solid rgba(214, 179, 106, 0.28);

    color: #f3d995 !important;

    text-align: left;

    font-size: 12px;
    font-weight: 800;

    letter-spacing: 0.35px;

    white-space: nowrap;
}

.mp-table td {
    padding: 14px 18px;

    border-bottom:
        1px solid rgba(255, 255, 255, 0.07);

    color: #f5f5f7 !important;

    font-size: 14px;
    line-height: 1.45;

    background: transparent !important;
}

.mp-table tbody tr {
    background: #0c0c0f;

    transition:
        background 0.18s ease,
        transform 0.18s ease;
}

.mp-table tbody tr:nth-child(even) {
    background: #121216;
}

.mp-table tbody tr:hover {
    background: #1b1812;
}

.mp-table tbody tr:last-child td {
    border-bottom: none;
}

.mp-table td:nth-child(2),
.mp-table td:nth-child(4),
.mp-table td:nth-child(5) {
    font-variant-numeric: tabular-nums;
}

/* ==========================================================
   COLUMNAS OBLIGATORIAS — EMPRESA
   ========================================================== */

.required-columns-box {
    padding: 20px;

    border: 1px solid rgba(214, 179, 106, 0.22);
    border-radius: 18px;

    background: #111216;
}

.required-columns-box h3 {
    margin: 0 0 16px;

    color: #ffffff !important;

    font-size: 18px;
    font-weight: 800;
}

.required-columns-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 10px;
}

.required-columns-grid span {
    display: block;

    padding: 10px 12px;

    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 10px;

    background: #09090b;

    color: #f3d995 !important;

    font-family: monospace;
    font-size: 13px;
    font-weight: 700;
}

"""