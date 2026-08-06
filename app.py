"""Punto de entrada para desplegar ModaPredict AI."""

from app.gradio_app import APP


demo = APP


if __name__ == "__main__":
    demo.launch()