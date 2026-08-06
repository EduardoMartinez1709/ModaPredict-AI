import pandas as pd


def revisar_calidad_productos(df: pd.DataFrame) -> None:
    """Muestra un diagnóstico básico de calidad del catálogo."""

    print("\n========== CALIDAD DE DATOS ==========\n")

    print(f"Filas: {df.shape[0]}")
    print(f"Columnas: {df.shape[1]}")

    duplicados_id = df["id_producto"].duplicated().sum()
    duplicados_completos = df.duplicated().sum()

    print(f"\nIDs duplicados: {duplicados_id}")
    print(f"Filas completamente duplicadas: {duplicados_completos}")

    print("\nValores nulos por columna:")
    nulos = df.isna().sum()
    print(nulos[nulos > 0] if nulos.sum() > 0 else "No hay valores nulos.")

    precios_invalidos = (
        df["precio_actual"].isna()
        | (df["precio_actual"] <= 0)
    ).sum()

    print(f"\nPrecios vacíos, negativos o iguales a cero: {precios_invalidos}")

    print("\nVariaciones detectadas en colores:")
    print(sorted(df["color"].dropna().unique()))

    marcas_propias = df[
        df["marca"].str.contains(
            "ASOS",
            case=False,
            na=False,
        )
    ]

    print(f"\nProductos de marca propia ASOS: {len(marcas_propias)}")

    print("\nPorcentaje de marca propia ASOS:")
    porcentaje = (
        len(marcas_propias) / len(df) * 100
        if len(df) > 0
        else 0
    )
    print(f"{porcentaje:.2f}%")

    print("\n======================================")