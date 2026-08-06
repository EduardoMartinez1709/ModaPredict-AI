from pathlib import Path

import pandas as pd
import requests


CIUDADES = [
    "Toluca",
    "Ciudad de México",
    "Guadalajara",
    "Monterrey",
    "Cancún",
]


def obtener_coordenadas(ciudad: str) -> dict:
    """Busca las coordenadas de una ciudad."""

    url = "https://geocoding-api.open-meteo.com/v1/search"

    parametros = {
        "name": ciudad,
        "count": 1,
        "language": "es",
        "format": "json",
        "countryCode": "MX",
    }

    respuesta = requests.get(
        url,
        params=parametros,
        timeout=30,
    )

    respuesta.raise_for_status()
    datos = respuesta.json()

    resultados = datos.get("results", [])

    if not resultados:
        raise ValueError(
            f"No se encontraron coordenadas para {ciudad}."
        )

    ubicacion = resultados[0]

    return {
        "ciudad": ciudad,
        "nombre_encontrado": ubicacion.get("name"),
        "estado": ubicacion.get("admin1"),
        "latitud": ubicacion.get("latitude"),
        "longitud": ubicacion.get("longitude"),
        "zona_horaria": ubicacion.get("timezone"),
    }


def obtener_pronostico(ubicacion: dict) -> pd.DataFrame:
    """Obtiene el pronóstico diario de una ubicación."""

    url = "https://api.open-meteo.com/v1/forecast"

    parametros = {
        "latitude": ubicacion["latitud"],
        "longitude": ubicacion["longitud"],
        "daily": ",".join(
            [
                "weather_code",
                "temperature_2m_max",
                "temperature_2m_min",
                "precipitation_sum",
                "rain_sum",
                "wind_speed_10m_max",
            ]
        ),
        "timezone": "auto",
        "forecast_days": 16,
    }

    respuesta = requests.get(
        url,
        params=parametros,
        timeout=30,
    )

    respuesta.raise_for_status()
    datos = respuesta.json()

    diarios = datos.get("daily", {})

    if not diarios:
        raise ValueError(
            f"No se obtuvo pronóstico para {ubicacion['ciudad']}."
        )

    dataframe = pd.DataFrame(diarios)

    dataframe = dataframe.rename(
        columns={
            "time": "fecha",
            "weather_code": "codigo_clima",
            "temperature_2m_max": "temperatura_max",
            "temperature_2m_min": "temperatura_min",
            "precipitation_sum": "precipitacion_mm",
            "rain_sum": "lluvia_mm",
            "wind_speed_10m_max": "viento_max_kmh",
        }
    )

    dataframe["ciudad"] = ubicacion["ciudad"]
    dataframe["estado"] = ubicacion["estado"]
    dataframe["latitud"] = ubicacion["latitud"]
    dataframe["longitud"] = ubicacion["longitud"]

    return dataframe


def guardar_clima(dataframe: pd.DataFrame) -> Path:
    """Guarda todos los pronósticos en un CSV."""

    ruta_proyecto = Path(__file__).resolve().parent

    carpeta = (
        ruta_proyecto
        / "datos"
        / "externos"
        / "clima"
    )

    carpeta.mkdir(
        parents=True,
        exist_ok=True,
    )

    ruta_archivo = carpeta / "pronostico_ciudades.csv"

    dataframe.to_csv(
        ruta_archivo,
        index=False,
        encoding="utf-8-sig",
    )

    return ruta_archivo


def main() -> None:
    print("\n========== CLIMA MODAPREDICT AI ==========\n")

    pronosticos = []

    for ciudad in CIUDADES:
        print(f"Consultando clima de {ciudad}...")

        ubicacion = obtener_coordenadas(ciudad)
        pronostico = obtener_pronostico(ubicacion)

        pronosticos.append(pronostico)

        print(
            f"Registros obtenidos para {ciudad}: "
            f"{len(pronostico)}"
        )

    clima_completo = pd.concat(
        pronosticos,
        ignore_index=True,
    )

    ruta = guardar_clima(clima_completo)

    print("\nVista previa:")
    print(clima_completo.head())

    print(
        f"\nTotal de registros: "
        f"{len(clima_completo)}"
    )

    print(f"Archivo guardado en:\n{ruta}")


if __name__ == "__main__":
    main()