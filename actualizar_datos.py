from src.api.asos import (
    descargar_productos,
    guardar_productos_csv,
    transformar_productos,
)
from src.api.hm import (
    descargar_productos_hm,
    guardar_productos_hm_csv,
    transformar_productos_hm,
)


def actualizar_asos():
    print("\n========== ACTUALIZANDO ASOS ==========\n")

    datos_asos = descargar_productos(numero_paginas=10)
    productos_asos = transformar_productos(datos_asos)
    guardar_productos_csv(productos_asos)

    print(f"Productos ASOS guardados: {len(productos_asos)}")


def actualizar_hm():
    print("\n========== ACTUALIZANDO H&M ==========\n")

    datos_hm = descargar_productos_hm(numero_paginas=10)
    productos_hm = transformar_productos_hm(datos_hm)
    guardar_productos_hm_csv(productos_hm)

    print(f"Productos H&M guardados: {len(productos_hm)}")


def main():
    actualizar_asos()
    actualizar_hm()

    print("\nActualización de datos terminada correctamente.")


if __name__ == "__main__":
    main()