from pathlib import Path

import pandas as pd
import requests

from src.config.settings import ASOS_HEADERS


import time

import requests

from src.config.settings import ASOS_HEADERS


def descargar_productos(numero_paginas=10):
    url = "https://asos2.p.rapidapi.com/products/v2/list"

    todos_los_productos = []

    for pagina in range(numero_paginas):
        offset = pagina * 48

        parametros = {
            "store": "US",
            "offset": str(offset),
            "categoryId": "4209",
            "country": "US",
            "sort": "freshness",
            "currency": "USD",
            "sizeSchema": "US",
            "limit": "48",
            "lang": "en-US",
        }

        print(
            f"Descargando página {pagina + 1} "
            f"de {numero_paginas}..."
        )

        respuesta = requests.get(
            url,
            headers=ASOS_HEADERS,
            params=parametros,
            timeout=30,
        )

        print(f"Status ASOS: {respuesta.status_code}")
        respuesta.raise_for_status()

        datos_pagina = respuesta.json()
        productos_pagina = datos_pagina.get("products", [])

        print(
            f"Productos encontrados en esta página: "
            f"{len(productos_pagina)}"
        )

        if not productos_pagina:
            print("No se encontraron más productos.")
            break

        todos_los_productos.extend(productos_pagina)

        time.sleep(0.5)

    productos_unicos = {
        producto.get("id"): producto
        for producto in todos_los_productos
        if producto.get("id") is not None
    }

    lista_productos_unicos = list(productos_unicos.values())

    print(
        f"\nTotal de productos ASOS descargados: "
        f"{len(todos_los_productos)}"
    )
    print(
        f"Total después de eliminar duplicados: "
        f"{len(lista_productos_unicos)}"
    )

    return {
        "products": lista_productos_unicos
    }


def transformar_productos(datos):
    productos = datos.get("products", [])
    registros = []

    for producto in productos:
        precio = producto.get("price", {})
        precio_actual = precio.get("current", {})
        precio_anterior = precio.get("previous", {})

        registros.append(
            {
                "id_producto": producto.get("id"),
                "nombre": producto.get("name"),
                "marca": producto.get("brandName"),
                "color": producto.get("colour"),
                "precio_actual": precio_actual.get("value"),
                "precio_anterior": precio_anterior.get("value"),
                "moneda": precio.get("currency"),
                "en_descuento": precio.get("isMarkedDown"),
                "es_nuevo": producto.get("isNew"),
                "venta_rapida": producto.get("isSellingFast"),
                "promocion": producto.get("isPromotion"),
                "url_producto": producto.get("url"),
                "url_imagen": producto.get("imageUrl"),
            }
        )

    dataframe = pd.DataFrame(registros)

    return dataframe


def guardar_productos_csv(dataframe):
    ruta_proyecto = Path(_file_).resolve().parents[2]
    carpeta_datos = ruta_proyecto / "datos"
    carpeta_datos.mkdir(exist_ok=True)

    ruta_archivo = carpeta_datos / "productos_asos.csv"

    dataframe.to_csv(
        ruta_archivo,
        index=False,
        encoding="utf-8-sig",
    )

    print(f"CSV guardado correctamente en: {ruta_archivo}")