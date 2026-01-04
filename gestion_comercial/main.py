"""
Sistema de Gestión Comercial
Punto de entrada principal de la aplicación
"""

import sys
import os

# Add the current directory to sys.path to ensure imports work correctly
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from gestion_comercial.core.app import MainApp
from gestion_comercial.modules.launcher.view import LauncherView
from gestion_comercial.modules.cash_counter.view import CashCounterView
from gestion_comercial.modules.tag_manager.view import TagManagerView
from gestion_comercial.modules.price_reader.view import PriceReaderView


def main():
    """Función principal de la aplicación."""
    # Crear aplicación principal
    app = MainApp()

    # Registrar vistas
    app.navigator.register_view('launcher', LauncherView)
    app.navigator.register_view('cash_counter', CashCounterView)
    app.navigator.register_view('tag_manager', TagManagerView)
    app.navigator.register_view('price_reader', PriceReaderView)

    # Iniciar con el launcher
    app.navigator.show_view('launcher')

    # Ejecutar aplicación
    app.mainloop()


if __name__ == "__main__":
    main()
