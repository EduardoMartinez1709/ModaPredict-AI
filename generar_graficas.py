from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


# ==========================================================
# PALETA VISUAL MODAPREDICT AI
# ==========================================================

COLOR_FONDO = "#050505"
COLOR_PANEL = "#101116"
COLOR_TEXTO = "#f5f5f7"
COLOR_TEXTO_SUAVE = "#c9cbd1"
COLOR_DORADO = "#d6b36a"
COLOR_DORADO_CLARO = "#f3d995"
COLOR_PLATEADO = "#bfc2c9"
COLOR_REJILLA = "#2b2d33"
COLOR_BORDE = "#3a3c42"
COLOR_ALERTA = "#d87373"


# ==========================================================
# ESTILO GENERAL
# ==========================================================

def aplicar_estilo(
    figura,
    eje,
    titulo: str,
    xlabel: str = "",
    ylabel: str = "",
    grid_axis: str = "x",
) -> None:
    """Aplica el estilo visual general de ModaPredict AI."""

    figura.patch.set_facecolor(
        COLOR_FONDO
    )

    eje.set_facecolor(
        COLOR_PANEL
    )

    eje.set_title(
        titulo,
        color=COLOR_TEXTO,
        fontsize=16,
        fontweight="bold",
        pad=18,
    )

    eje.set_xlabel(
        xlabel,
        color=COLOR_TEXTO_SUAVE,
        fontsize=11,
        labelpad=10,
    )

    eje.set_ylabel(
        ylabel,
        color=COLOR_TEXTO_SUAVE,
        fontsize=11,
        labelpad=10,
    )

    eje.tick_params(
        axis="both",
        colors=COLOR_TEXTO_SUAVE,
        labelsize=10,
    )

    eje.grid(
        axis=grid_axis,
        color=COLOR_REJILLA,
        alpha=0.55,
        linewidth=0.8,
    )

    eje.set_axisbelow(
        True
    )

    for borde in eje.spines.values():
        borde.set_color(
            COLOR_BORDE
        )
        borde.set_linewidth(
            0.8
        )


def agregar_valores_barras_horizontales(
    eje,
    decimales: int = 2,
) -> None:
    """Añade etiquetas al final de las barras horizontales."""

    for barra in eje.patches:
        ancho = barra.get_width()

        eje.text(
            ancho,
            barra.get_y() + barra.get_height() / 2,
            f" {ancho:.{decimales}f}",
            va="center",
            ha="left",
            color=COLOR_TEXTO,
            fontsize=9,
            fontweight="bold",
        )


def guardar_grafica(
    figura,
    ruta: Path,
) -> None:
    """Guarda una gráfica con formato uniforme."""

    figura.tight_layout(
        pad=1.6
    )

    figura.savefig(
        ruta,
        dpi=300,
        bbox_inches="tight",
        facecolor=figura.get_facecolor(),
    )

    plt.close(
        figura
    )


# ==========================================================
# GRÁFICAS
# ==========================================================

def grafica_comparacion_modelos(
    comparacion: pd.DataFrame,
    carpeta: Path,
) -> None:
    """Compara el MAE de los modelos del Experimento B."""

    datos = (
        comparacion.loc[
            comparacion["experimento"].eq("B")
        ]
        .sort_values(
            "MAE",
            ascending=True,
        )
        .copy()
    )

    figura, eje = plt.subplots(
        figsize=(10, 6)
    )

    eje.barh(
        datos["modelo"],
        datos["MAE"],
        color=COLOR_DORADO,
        edgecolor=COLOR_DORADO_CLARO,
        linewidth=0.7,
    )

    aplicar_estilo(
        figura=figura,
        eje=eje,
        titulo="Comparación de modelos — Experimento B",
        xlabel="MAE",
        ylabel="Modelo",
        grid_axis="x",
    )

    agregar_valores_barras_horizontales(
        eje,
        decimales=2,
    )

    guardar_grafica(
        figura,
        carpeta
        / "01_comparacion_modelos_mae.png",
    )


def grafica_prediccion_vs_real(
    errores: pd.DataFrame,
    carpeta: Path,
) -> None:
    """Compara las predicciones con el valor real."""

    figura, eje = plt.subplots(
        figsize=(8, 7)
    )

    eje.scatter(
        errores["valor_real"],
        errores["valor_predicho"],
        alpha=0.72,
        s=34,
        color=COLOR_DORADO,
        edgecolors=COLOR_DORADO_CLARO,
        linewidths=0.45,
    )

    minimo = min(
        errores["valor_real"].min(),
        errores["valor_predicho"].min(),
    )

    maximo = max(
        errores["valor_real"].max(),
        errores["valor_predicho"].max(),
    )

    eje.plot(
        [minimo, maximo],
        [minimo, maximo],
        linestyle="--",
        linewidth=1.8,
        color=COLOR_PLATEADO,
        label="Predicción ideal",
    )

    aplicar_estilo(
        figura=figura,
        eje=eje,
        titulo="Predicción frente al valor real",
        xlabel="ModaPredict Score real",
        ylabel="Predicción del modelo",
        grid_axis="both",
    )

    leyenda = eje.legend(
        frameon=True,
        facecolor=COLOR_PANEL,
        edgecolor=COLOR_BORDE,
    )

    for texto in leyenda.get_texts():
        texto.set_color(
            COLOR_TEXTO
        )

    guardar_grafica(
        figura,
        carpeta
        / "02_prediccion_vs_real.png",
    )


def grafica_distribucion_errores(
    errores: pd.DataFrame,
    carpeta: Path,
) -> None:
    """Muestra la distribución de los residuos."""

    figura, eje = plt.subplots(
        figsize=(9, 6)
    )

    eje.hist(
        errores["error"].dropna(),
        bins=30,
        color=COLOR_DORADO,
        edgecolor=COLOR_DORADO_CLARO,
        linewidth=0.65,
        alpha=0.92,
    )

    eje.axvline(
        0,
        linestyle="--",
        linewidth=1.8,
        color=COLOR_PLATEADO,
        label="Error cero",
    )

    aplicar_estilo(
        figura=figura,
        eje=eje,
        titulo="Distribución de residuos",
        xlabel="Error: valor real - predicción",
        ylabel="Frecuencia",
        grid_axis="y",
    )

    leyenda = eje.legend(
        frameon=True,
        facecolor=COLOR_PANEL,
        edgecolor=COLOR_BORDE,
    )

    for texto in leyenda.get_texts():
        texto.set_color(
            COLOR_TEXTO
        )

    guardar_grafica(
        figura,
        carpeta
        / "03_distribucion_residuos.png",
    )


def grafica_importancia_variables(
    importancia: pd.DataFrame,
    carpeta: Path,
) -> None:
    """Grafica las 15 variables con mayor importancia."""

    datos = (
        importancia.head(15)
        .sort_values(
            "importancia_promedio",
            ascending=True,
        )
        .copy()
    )

    figura, eje = plt.subplots(
        figsize=(10, 7)
    )

    eje.barh(
        datos["variable"],
        datos["importancia_promedio"],
        color=COLOR_PLATEADO,
        edgecolor=COLOR_TEXTO,
        linewidth=0.5,
    )

    aplicar_estilo(
        figura=figura,
        eje=eje,
        titulo="Importancia de variables por permutación",
        xlabel="Aumento promedio del MAE al permutar",
        ylabel="Variable",
        grid_axis="x",
    )

    agregar_valores_barras_horizontales(
        eje,
        decimales=2,
    )

    guardar_grafica(
        figura,
        carpeta
        / "04_importancia_variables.png",
    )


def grafica_errores_ciudad(
    errores_ciudad: pd.DataFrame,
    carpeta: Path,
) -> None:
    """Compara el MAE por ciudad."""

    datos = (
        errores_ciudad.sort_values(
            "mae",
            ascending=True,
        )
        .copy()
    )

    figura, eje = plt.subplots(
        figsize=(9, 6)
    )

    eje.barh(
        datos["ciudad"],
        datos["mae"],
        color=COLOR_DORADO,
        edgecolor=COLOR_DORADO_CLARO,
        linewidth=0.7,
    )

    aplicar_estilo(
        figura=figura,
        eje=eje,
        titulo="Error promedio por ciudad",
        xlabel="MAE",
        ylabel="Ciudad",
        grid_axis="x",
    )

    agregar_valores_barras_horizontales(
        eje,
        decimales=2,
    )

    guardar_grafica(
        figura,
        carpeta
        / "05_error_por_ciudad.png",
    )


def grafica_errores_categoria(
    errores_categoria: pd.DataFrame,
    carpeta: Path,
) -> None:
    """Muestra las categorías con mayor MAE."""

    datos = (
        errores_categoria
        .sort_values(
            "mae",
            ascending=False,
        )
        .head(12)
        .sort_values(
            "mae",
            ascending=True,
        )
        .copy()
    )

    figura, eje = plt.subplots(
        figsize=(10, 7)
    )

    eje.barh(
        datos["categoria_normalizada"],
        datos["mae"],
        color=COLOR_ALERTA,
        edgecolor="#f0a2a2",
        linewidth=0.7,
    )

    aplicar_estilo(
        figura=figura,
        eje=eje,
        titulo="Categorías con mayor error promedio",
        xlabel="MAE",
        ylabel="Categoría",
        grid_axis="x",
    )

    agregar_valores_barras_horizontales(
        eje,
        decimales=2,
    )

    guardar_grafica(
        figura,
        carpeta
        / "06_error_por_categoria.png",
    )


# ==========================================================
# EJECUCIÓN
# ==========================================================

def main() -> None:
    """Genera todas las gráficas técnicas del proyecto."""

    ruta_proyecto = Path(
        __file__
    ).resolve().parent

    carpeta_resultados = (
        ruta_proyecto
        / "resultados"
    )

    carpeta_graficas = (
        carpeta_resultados
        / "graficas"
    )

    carpeta_graficas.mkdir(
        parents=True,
        exist_ok=True,
    )

    comparacion = pd.read_csv(
        carpeta_resultados
        / "comparacion_experimentos.csv"
    )

    errores = pd.read_csv(
        carpeta_resultados
        / "analisis_errores_test.csv"
    )

    importancia = pd.read_csv(
        carpeta_resultados
        / "importancia_variables.csv"
    )

    errores_ciudad = pd.read_csv(
        carpeta_resultados
        / "errores_por_ciudad.csv"
    )

    errores_categoria = pd.read_csv(
        carpeta_resultados
        / "errores_por_categoria.csv"
    )

    grafica_comparacion_modelos(
        comparacion,
        carpeta_graficas,
    )

    grafica_prediccion_vs_real(
        errores,
        carpeta_graficas,
    )

    grafica_distribucion_errores(
        errores,
        carpeta_graficas,
    )

    grafica_importancia_variables(
        importancia,
        carpeta_graficas,
    )

    grafica_errores_ciudad(
        errores_ciudad,
        carpeta_graficas,
    )

    grafica_errores_categoria(
        errores_categoria,
        carpeta_graficas,
    )

    print(
        "\nGráficas guardadas correctamente en:"
        f"\n{carpeta_graficas}"
    )


if __name__ == "__main__":
    main()