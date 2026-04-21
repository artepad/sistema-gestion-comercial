import tkinter as tk
from gestion_comercial.config.settings import Settings
from gestion_comercial.config.theme import Theme
from gestion_comercial.core.navigation import Navigator

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Cargar configuración guardada
        Settings.load()

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
        if Settings.ALIGN_TOP:
            y = 0
        else:
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

        # --- Manejo de popups modales frente a Win+D y minimización ---
        # Win+D oculta ventanas con SWP_HIDEWINDOW (distinto al minimize normal).
        # Con grab_set() activo en un popup, la app queda inaccesible al restaurar.
        # Solución: liberar el grab al ocultarse y restaurarlo al volver.
        self._popup_with_grab = None
        self.bind('<Unmap>', self._on_root_hidden)
        self.bind('<Map>',   self._on_root_shown)
        self.bind('<FocusIn>', self._on_root_focus)

    # ------------------------------------------------------------------
    #  Handlers para minimización / Win+D
    # ------------------------------------------------------------------

    def _on_root_hidden(self, event):
        """
        La ventana raíz fue ocultada (minimize clásico o Win+D).
        Liberar el grab activo para que el OS pueda manejar la restauración.
        """
        if event.widget is not self:
            return
        grab = self.grab_current()
        if grab and grab is not self and grab.winfo_exists():
            self._popup_with_grab = grab
            grab.grab_release()

    def _on_root_shown(self, event):
        """
        La ventana raíz fue restaurada (botón de barra de tareas o Win+D).
        Recuperar el popup y re-aplicar el grab con una pequeña demora.
        """
        if event.widget is not self:
            return
        self.after(150, self._restore_popup)

    def _on_root_focus(self, event):
        """
        La ventana raíz recuperó el foco del OS.
        Alternativa a <Map> para el caso Win+D, donde <Map> puede no dispararse.
        Solo actúa si hay un popup guardado pendiente de restaurar.
        """
        if event.widget is not self or not self._popup_with_grab:
            return
        self.after(100, self._restore_popup)

    def _restore_popup(self):
        """Restaura el popup guardado: lo muestra, lo trae al frente y re-aplica grab."""
        popup = self._popup_with_grab
        if popup and popup.winfo_exists():
            self._popup_with_grab = None
            popup.deiconify()   # Necesario para Win+D (ventanas ocultas con SWP_HIDEWINDOW)
            popup.lift()
            popup.grab_set()
            popup.focus_force()
