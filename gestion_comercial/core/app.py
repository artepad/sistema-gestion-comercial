import tkinter as tk
from gestion_comercial.config.settings import Settings
from gestion_comercial.config.theme import Theme
from gestion_comercial.core.navigation import Navigator

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Ocultar ventana temporalmente mientras se configura
        self.withdraw()

        self.title(Settings.APP_NAME)

        if not Settings.RESIZABLE:
            self.resizable(False, False)

        self.configure(bg=Theme.BACKGROUND)

        # Calcular posición centrada ANTES de mostrar la ventana
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - Settings.WINDOW_WIDTH) // 2
        y = (screen_height - Settings.WINDOW_HEIGHT) // 2

        # Establecer geometría con tamaño Y posición desde el inicio
        self.geometry(f"{Settings.WINDOW_WIDTH}x{Settings.WINDOW_HEIGHT}+{x}+{y}")

        # Main container for views
        self.container = tk.Frame(self, bg=Theme.BACKGROUND)
        self.container.pack(fill='both', expand=True)

        # Initialize Navigator
        self.navigator = Navigator(self.container)

        # Mostrar la ventana ya centrada
        self.deiconify()
