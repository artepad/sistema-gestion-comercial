import os
import json


class Settings:
    # App Info
    APP_NAME = "Sistema de Gestión Comercial"
    VERSION = "2.0.0"

    # Window Configuration (defaults)
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 780
    RESIZABLE = False
    ALIGN_TOP = False

    # Available Resolutions
    AVAILABLE_RESOLUTIONS = [
        (800, 780),
        (900, 850),
        (1024, 900),
        (1280, 1024),
    ]

    # Paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
    CONFIG_FILE = os.path.join(BASE_DIR, 'config', 'user_config.json')

    @classmethod
    def load(cls):
        """Carga la configuración guardada desde user_config.json"""
        if not os.path.exists(cls.CONFIG_FILE):
            return
        try:
            with open(cls.CONFIG_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            cls.WINDOW_WIDTH = data.get('window_width', cls.WINDOW_WIDTH)
            cls.WINDOW_HEIGHT = data.get('window_height', cls.WINDOW_HEIGHT)
            cls.ALIGN_TOP = data.get('align_top', cls.ALIGN_TOP)
        except Exception:
            pass

    @classmethod
    def save(cls):
        """Guarda la configuración actual en user_config.json"""
        data = {
            'window_width': cls.WINDOW_WIDTH,
            'window_height': cls.WINDOW_HEIGHT,
            'align_top': cls.ALIGN_TOP,
        }
        try:
            os.makedirs(os.path.dirname(cls.CONFIG_FILE), exist_ok=True)
            with open(cls.CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass
