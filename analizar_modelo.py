from pathlib import Path

from src.modelos.interpretacion import (
    calcular_importancia_permutacion,
    comparar_train_test,
    construir_analisis_errores,
    entrenar_modelo_ganador,
    generar_reporte_interpretacion,
    resumir_errores_por_variable,
)


def main():
    ruta_proyecto = Path(__file__).resolve().parent

    carpeta_resultados = (
        ruta_proyecto / "resultados"
    )

    carpeta_resultados.mkdir(
        parents=True,
        exist_ok=True,
    )

    # ==========================================
    # ENTRENAR MODELO GANADOR
    # ==========================================

    resultado = entrenar_modelo_ganador()

    # ==========================================
    # TRAIN VS. TEST
    # ==========================================

    metricas = comparar_train_test(
        resultado
    )

    # ==========================================
    # ANÁLISIS DE ERRORES
    # ==========================================

    errores = construir_analisis_errores(
        resultado
    )

    errores_ciudad = resumir_errores_por_variable(
        errores,
        "ciudad",
    )

    errores_categoria = (
        resumir_errores_por_variable(
            errores,
            "categoria_normalizada",
        )
    )

    errores_marca = resumir_errores_por_variable(
        errores,
        "marca_normalizada",
    )

    # ==========================================
    # IMPORTANCIA DE VARIABLES
    # ==========================================

    importancia = calcular_importancia_permutacion(
        resultado_entrenamiento=resultado,
        repeticiones=10,
    )

    # ==========================================
    # REPORTE
    # ==========================================

    generar_reporte_interpretacion(
        metricas=metricas,
        errores=errores,
        importancia=importancia,
    )

    # ==========================================
    # GUARDAR RESULTADOS
    # ==========================================

    metricas.to_csv(
        carpeta_resultados
        / "metricas_train_test.csv",
        index=False,
        encoding="utf-8-sig",
    )

    errores.to_csv(
        carpeta_resultados
        / "analisis_errores_test.csv",
        index=False,
        encoding="utf-8-sig",
    )

    errores_ciudad.to_csv(
        carpeta_resultados
        / "errores_por_ciudad.csv",
        index=False,
        encoding="utf-8-sig",
    )

    errores_categoria.to_csv(
        carpeta_resultados
        / "errores_por_categoria.csv",
        index=False,
        encoding="utf-8-sig",
    )

    errores_marca.to_csv(
        carpeta_resultados
        / "errores_por_marca.csv",
        index=False,
        encoding="utf-8-sig",
    )

    importancia.to_csv(
        carpeta_resultados
        / "importancia_variables.csv",
        index=False,
        encoding="utf-8-sig",
    )

    print(
        "\nArchivos de interpretación guardados "
        "en la carpeta resultados."
    )


if __name__ == "__main__":
    main()