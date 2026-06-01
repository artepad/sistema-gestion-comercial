import os
import json


class Settings:
    # App Info
    APP_NAME = "Sistema de Gestión Comercial"

    # Window Configuration (defaults)
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 780
    RESIZABLE = False
    ALIGN_TOP = False
    COMPACT_MODE = False
    # True cuando el usuario cambió el modo manualmente desde Configuración.
    # False = la app puede auto-detectar según la resolución de pantalla.
    COMPACT_MODE_MANUAL = False

    # Available Resolutions
    AVAILABLE_RESOLUTIONS = [
        (800, 780),
        (520, 720),   # compacto — pantallas 1366×768
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
            cls.WINDOW_WIDTH       = data.get('window_width',        cls.WINDOW_WIDTH)
            cls.WINDOW_HEIGHT      = data.get('window_height',       cls.WINDOW_HEIGHT)
            cls.ALIGN_TOP          = data.get('align_top',           cls.ALIGN_TOP)
            cls.COMPACT_MODE_MANUAL = data.get('compact_mode_manual', cls.COMPACT_MODE_MANUAL)
            # Leer clave nueva; si no existe, intentar con la clave antigua (portrait_mode)
            cls.COMPACT_MODE = data.get('compact_mode', data.get('portrait_mode', cls.COMPACT_MODE))
        except Exception:
            pass

    @classmethod
    def save(cls):
        """Guarda la configuración actual en user_config.json"""
        data = {
            'window_width':        cls.WINDOW_WIDTH,
            'window_height':       cls.WINDOW_HEIGHT,
            'align_top':           cls.ALIGN_TOP,
            'compact_mode':        cls.COMPACT_MODE,
            'compact_mode_manual': cls.COMPACT_MODE_MANUAL,
        }
        try:
            os.makedirs(os.path.dirname(cls.CONFIG_FILE), exist_ok=True)
            with open(cls.CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass

    @classmethod
    def auto_detect_compact_mode(cls, screen_height: int):
        """
        Activa el modo compacto automáticamente si la pantalla lo requiere.
        Solo actúa si el usuario nunca configuró el modo manualmente.
        Umbral: pantallas con altura ≤ 800px (ej: 1366×768, 1280×800).
        """
        if cls.COMPACT_MODE_MANUAL:
            return  # Respetar la elección manual del usuario

        if screen_height <= 800:
            cls.COMPACT_MODE  = True
            cls.WINDOW_WIDTH  = 520
            cls.WINDOW_HEIGHT = 720
        else:
            cls.COMPACT_MODE  = False
            cls.WINDOW_WIDTH  = 800
            cls.WINDOW_HEIGHT = 780
