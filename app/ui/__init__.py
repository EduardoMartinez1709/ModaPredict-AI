"""
Componentes modulares de la interfaz de ModaPredict AI.
"""

from app.ui.analitica_modelo import (
    construir_tab_analitica_modelo,
)
from app.ui.chat import (
    construir_tab_chat,
)
from app.ui.dashboard_emprendedor import (
    construir_tab_dashboard_emprendedor,
)
from app.ui.dashboard_empresa import (
    construir_tab_dashboard_empresa,
)
from app.ui.inicio import (
    construir_tab_inicio,
)
from app.ui.recomendador import (
    construir_tab_recomendador,
)

__all__ = [
    "construir_tab_inicio",
    "construir_tab_recomendador",
    "construir_tab_chat",
    "construir_tab_dashboard_emprendedor",
    "construir_tab_dashboard_empresa",
    "construir_tab_analitica_modelo",
]