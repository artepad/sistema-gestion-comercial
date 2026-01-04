import os

class Settings:
    # App Info
    APP_NAME = "Sistema de Gestión Comercial"
    VERSION = "2.0.0"
    
    # Window Configuration
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 780
    RESIZABLE = False
    
    # Paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
