import os

from dotenv import load_dotenv


load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

if not RAPIDAPI_KEY:
    raise ValueError("No se encontró RAPIDAPI_KEY en el archivo .env")


ASOS_HEADERS = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": "asos2.p.rapidapi.com",
}

HM_HEADERS = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": "apidojo-hm-hennes-mauritz-v1.p.rapidapi.com",
}