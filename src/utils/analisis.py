import pandas as pd


def generar_reporte(df):

    print("\n========== MODAPREDICT AI ==========\n")

    print(f"Productos analizados: {len(df)}")

    print("\nTop 10 marcas")
    print(df["marca"].value_counts().head(10))

    print("\nTop 10 colores")
    print(df["color"].value_counts().head(10))

    print("\nPrecio promedio")
    print(f"${df['precio_actual'].mean():.2f} USD")

    print("\nPrecio mínimo")
    print(f"${df['precio_actual'].min()} USD")

    print("\nPrecio máximo")
    print(f"${df['precio_actual'].max()} USD")

    print("\nProductos en descuento")
    print(df["en_descuento"].sum())

    print("\nProductos nuevos")
    print(df["es_nuevo"].sum())

    print("\nProductos en promoción")
    print(df["promocion"].sum())

    print("\n==============================")