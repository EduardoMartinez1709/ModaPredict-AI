from app.gradio_app import APP


def main() -> None:
    print(
        "\n========== MODAPREDICT AI ==========\n"
    )

    print(
        "Iniciando aplicación..."
    )

    print(
        "Cuando aparezca el enlace, ábrelo "
        "en tu navegador."
    )

    APP.queue().launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        show_error=True,
        inbrowser=True,
    )


if __name__ == "__main__":
    main()