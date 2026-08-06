from pathlib import Path

import pandas as pd
import requests

from src.config.settings import HM_HEADERS


import time


def descargar_productos_hm(numero_paginas=10):
    url = (
        "https://apidojo-hm-hennes-mauritz-v1.p.rapidapi.com/"
        "products/v2/list"
    )

    todos_los_productos = []

    for pagina in range(1, numero_paginas + 1):
        parametros = {
            "country": "us",
            "lang": "en",
            "page": str(pagina),
            "pageSize": "30",
            "sortBy": "RELEVANCE",
            "categoryId": "ladies_all",
        }

        print(
            f"Descargando página H&M {pagina} "
            f"de {numero_paginas}..."
        )

        respuesta = requests.get(
            url,
            headers=HM_HEADERS,
            params=parametros,
            timeout=30,
        )

        print(f"Status H&M: {respuesta.status_code}")
        respuesta.raise_for_status()

        datos_pagina = respuesta.json()

        productos_pagina = (
            datos_pagina.get("plpList", {})
            .get("productList", [])
        )

        print(
            "Productos encontrados en esta página: "
            f"{len(productos_pagina)}"
        )

        if not productos_pagina:
            print("No se encontraron más productos de H&M.")
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
        "\nTotal de productos H&M descargados: "
        f"{len(todos_los_productos)}"
    )
    print(
        "Total después de eliminar duplicados: "
        f"{len(lista_productos_unicos)}"
    )

    return {
        "plpList": {
            "productList": lista_productos_unicos
        }
    }


def transformar_productos_hm(datos):
    productos = (
        datos.get("plpList", {})
        .get("productList", [])
    )

    registros = []

    for producto in productos:
        precios = producto.get("prices", [])
        precio_principal = precios[0] if precios else {}

        disponibilidad = producto.get("availability", {})
        tallas = producto.get("sizes", [])

        tallas_disponibles = [
            talla.get("label")
            for talla in tallas
            if talla.get("stock", 0) > 0
        ]

        stock_total = sum(
            talla.get("stock", 0)
            for talla in tallas
        )

        url_relativa = producto.get("url")
        url_completa = (
            f"https://www2.hm.com{url_relativa}"
            if url_relativa
            else None
        )

        registros.append(
            {
                "id_producto": producto.get("id"),
                "nombre": producto.get("productName"),
                "marca": producto.get("brandName"),
                "color": producto.get("colorName"),
                "precio_actual": precio_principal.get("price"),
                "precio_minimo": precio_principal.get("minPrice"),
                "precio_maximo": precio_principal.get("maxPrice"),
                "moneda": "USD",
                "disponibilidad": disponibilidad.get("stockState"),
                "proximamente": disponibilidad.get("comingSoon"),
                "es_nuevo": producto.get("newArrival"),
                "en_linea": producto.get("isOnline"),
                "categoria": producto.get("mainCatCode"),
                "tallas_disponibles": ", ".join(
                    talla for talla in tallas_disponibles if talla
                ),
                "cantidad_tallas": len(tallas_disponibles),
                "stock_total_api": stock_total,
                "url_producto": url_completa,
                "url_imagen": producto.get("productImage"),
                "fuente": "H&M",
            }
        )

    return pd.DataFrame(registros)


def guardar_productos_hm_csv(dataframe):
    ruta_proyecto = Path(_file_).resolve().parents[2]
    carpeta_datos = ruta_proyecto / "datos"
    carpeta_datos.mkdir(exist_ok=True)

    ruta_archivo = carpeta_datos / "productos_hm.csv"

    dataframe.to_csv(
        ruta_archivo,
        index=False,
        encoding="utf-8-sig",
    )

    print(f"CSV de H&M guardado correctamente en: {ruta_archivo}")