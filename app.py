"""Punto de entrada para desplegar ModaPredict AI."""

from __future__ import annotations

import os

from app.gradio_app import APP


demo = APP


if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", "7860"))

    demo.launch(
        server_name="0.0.0.0",
        server_port=puerto,
        show_error=True,
    )