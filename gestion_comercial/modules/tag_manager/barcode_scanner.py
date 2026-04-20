"""
Ventana de escáner de código de barras.
Permite buscar productos en la base de datos y autocompletar información.
"""

import tkinter as tk
from tkinter import messagebox, filedialog
import shutil
import os
from gestion_comercial.config.theme import Theme
from gestion_comercial.modules.tag_manager.database import ProductDatabase


class BarcodeScannerWindow(tk.Toplevel):
    """Ventana emergente para escanear códigos de barras y buscar productos."""

    def __init__(self, parent, row_index, on_product_selected):
        """
        Inicializa la ventana de escáner.

        Args:
            parent: Ventana padre
            row_index (int): Índice de la fila (0-13)
            on_product_selected (callable): Callback que recibe (row_index, name, price)
        """
        super().__init__(parent)

        self.row_index = row_index
        self.on_product_selected = on_product_selected

        self.setup_window()
        self.setup_ui()

        # Foco en el campo de código
        self.barcode_entry.focus_set()

    def setup_window(self):
        """Configura las propiedades de la ventana."""
        self.title(f"Escáner de Código de Barras - Fila {self.row_index + 1:02d}")
        self.configure(bg=Theme.BACKGROUND)
        self.resizable(False, False)

        # Tamaño de la ventana
        window_width = 520
        window_height = 350

        # Centrar la ventana
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Hacer modal
        self.transient(self.master)
        self.grab_set()

    def setup_ui(self):
        """Configura la interfaz de usuario."""
        # Header
        self.create_header()

        # Contenido principal
        content_frame = tk.Frame(self, bg=Theme.BACKGROUND)
        content_frame.pack(fill='both', expand=True, padx=30, pady=20)

        # Sección de escáner (arriba)
        self.create_scanner_section(content_frame)

        # Sección de información de BD (abajo)
        self.create_db_info_section(content_frame)

    def create_header(self):
        """Crea el encabezado de la ventana."""
        header_frame = tk.Frame(self, bg=Theme.BILLS_FG, height=85)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        # Línea de acento verde
        tk.Frame(header_frame, bg='#27ae60', height=4).pack(fill='x')

        # Contenedor centrado
        content_container = tk.Frame(header_frame, bg=Theme.BILLS_FG)
        content_container.pack(expand=True)

        # Icono (más pequeño)
        tk.Label(
            content_container,
            text="🔍",
            font=(Theme.FONT_FAMILY, 24),
            bg=Theme.BILLS_FG,
            fg='white'
        ).pack(pady=(0, 3))

        # Título (más pequeño)
        tk.Label(
            content_container,
            text="Búsqueda de Producto",
            font=(Theme.FONT_FAMILY, 13, 'bold'),
            bg=Theme.BILLS_FG,
            fg='white'
        ).pack()

    def create_db_info_section(self, parent):
        """Crea la sección de información de la base de datos."""
        info_frame = tk.LabelFrame(
            parent,
            text="💾 Información de Base de Datos",
            font=(Theme.FONT_FAMILY, 10, 'bold'),
            bg='white',
            fg='#2c3e50',
            relief='solid',
            bd=1,
            padx=15,
            pady=12
        )
        info_frame.pack(fill='x', pady=(0, 15))

        # Obtener información de la BD
        db_info = ProductDatabase.get_database_info()

        if db_info['exists']:
            # Estado de conexión con fecha y enlace de eliminación en una sola línea
            status_container = tk.Frame(info_frame, bg='white')
            status_container.pack(fill='x', pady=(0, 8))

            tk.Label(
                status_container,
                text="Estado:",
                font=(Theme.FONT_FAMILY, 9),
                bg='white',
                fg='#495057'
            ).pack(side='left')

            tk.Label(
                status_container,
                text="Conectada",
                font=(Theme.FONT_FAMILY, 9, 'bold'),
                bg='white',
                fg='#28a745'
            ).pack(side='left', padx=(10, 0))

            # Separador
            tk.Label(
                status_container,
                text="—",
                font=(Theme.FONT_FAMILY, 9),
                bg='white',
                fg='#ced4da'
            ).pack(side='left', padx=(8, 8))

            # Fecha y hora de última actualización
            tk.Label(
                status_container,
                text=db_info['last_modified'],
                font=(Theme.FONT_FAMILY, 9, 'bold'),
                bg='white',
                fg='#2c3e50'
            ).pack(side='left')

            # Separador
            tk.Label(
                status_container,
                text="—",
                font=(Theme.FONT_FAMILY, 9),
                bg='white',
                fg='#ced4da'
            ).pack(side='left', padx=(8, 8))

            # Enlace para eliminar base de datos
            delete_link = tk.Label(
                status_container,
                text="🗑 Eliminar base de datos",
                font=(Theme.FONT_FAMILY, 8),
                bg='white',
                fg='#6c757d',
                cursor='hand2'
            )
            delete_link.pack(side='left')

            # Hover effect
            def on_delete_enter(e):
                delete_link.config(fg='#dc3545', font=(Theme.FONT_FAMILY, 8, 'underline'))

            def on_delete_leave(e):
                delete_link.config(fg='#6c757d', font=(Theme.FONT_FAMILY, 8))

            delete_link.bind('<Enter>', on_delete_enter)
            delete_link.bind('<Leave>', on_delete_leave)
            delete_link.bind('<Button-1>', lambda e: self.delete_database())
        else:
            # Mensaje de error
            error_container = tk.Frame(info_frame, bg='white')
            error_container.pack(fill='x', pady=(0, 8))

            tk.Label(
                error_container,
                text="Estado:",
                font=(Theme.FONT_FAMILY, 9),
                bg='white',
                fg='#495057'
            ).pack(side='left')

            tk.Label(
                error_container,
                text="✗ No disponible",
                font=(Theme.FONT_FAMILY, 9, 'bold'),
                bg='white',
                fg='#dc3545'
            ).pack(side='left', padx=(10, 0))

            # Instrucción
            tk.Label(
                info_frame,
                text="No se encontró ningún archivo de base de datos en la carpeta.",
                font=(Theme.FONT_FAMILY, 8),
                bg='white',
                fg='#6c757d',
                wraplength=450,
                justify='left'
            ).pack(fill='x', pady=(0, 10))

            # Botón para buscar base de datos
            search_button = tk.Button(
                info_frame,
                text="🔍 Buscar Base de Datos",
                font=(Theme.FONT_FAMILY, 9, 'bold'),
                bg='#3498db',
                fg='white',
                bd=0,
                padx=15,
                pady=6,
                cursor='hand2',
                command=self.search_database_file
            )
            search_button.pack()

            def on_search_enter(e):
                search_button.config(bg='#2980b9')

            def on_search_leave(e):
                search_button.config(bg='#3498db')

            search_button.bind('<Enter>', on_search_enter)
            search_button.bind('<Leave>', on_search_leave)

    def create_scanner_section(self, parent):
        """Crea la sección de escáner."""
        scanner_frame = tk.LabelFrame(
            parent,
            text="🔢 Código de Barras",
            font=(Theme.FONT_FAMILY, 10, 'bold'),
            bg='white',
            fg='#495057',
            padx=15,
            pady=15
        )
        scanner_frame.pack(fill='x', pady=(0, 15))

        # Instrucciones
        tk.Label(
            scanner_frame,
            text="Escanea o ingresa el código del producto:",
            font=(Theme.FONT_FAMILY, 9),
            bg='white',
            fg='#6c757d'
        ).pack(anchor='w', pady=(0, 8))

        # Campo de entrada
        self.barcode_entry = tk.Entry(
            scanner_frame,
            font=(Theme.FONT_FAMILY, 12),
            bg='#f8f9fa',
            relief='flat',
            bd=1,
            highlightthickness=2,
            highlightbackground='#ced4da',
            highlightcolor='#27ae60'
        )
        self.barcode_entry.pack(fill='x', ipady=6)

        # Bind para búsqueda automática
        self.barcode_entry.bind('<Return>', lambda e: self.auto_search())

    def update_db_info(self):
        """Actualiza la información de la base de datos reconstruyendo la interfaz."""
        # Destruir y recrear todo el contenido
        for widget in self.winfo_children():
            if not isinstance(widget, tk.Frame) or widget.winfo_class() != 'Frame':
                continue
            widget.destroy()

        # Recrear la interfaz completa
        self.setup_ui()

        # Restaurar el foco en el campo de entrada
        self.barcode_entry.focus_set()

    def delete_database(self):
        """Elimina la base de datos actual después de confirmar con el usuario."""
        # Confirmar con el usuario
        confirm = messagebox.askyesno(
            "Confirmar Eliminación",
            "¿Estás seguro de que deseas eliminar la base de datos?\n\n"
            "Esta acción no se puede deshacer.",
            parent=self,
            icon='warning'
        )

        if confirm:
            try:
                # Obtener información de la base de datos actual
                db_info = ProductDatabase.get_database_info()

                if db_info['exists'] and db_info['path']:
                    # Eliminar el archivo
                    if os.path.exists(db_info['path']):
                        os.remove(db_info['path'])

                        # Refrescar la interfaz
                        self.update_db_info()

                        messagebox.showinfo(
                            "Éxito",
                            "La base de datos ha sido eliminada correctamente.",
                            parent=self
                        )
                    else:
                        messagebox.showerror(
                            "Error",
                            "No se encontró el archivo de base de datos.",
                            parent=self
                        )
                else:
                    messagebox.showerror(
                        "Error",
                        "No hay ninguna base de datos para eliminar.",
                        parent=self
                    )
            except Exception as e:
                messagebox.showerror(
                    "Error",
                    f"No se pudo eliminar el archivo:\n{str(e)}",
                    parent=self
                )

    def auto_search(self):
        """Busca automáticamente el producto y transfiere los datos."""
        barcode = self.barcode_entry.get().strip()

        if not barcode:
            messagebox.showwarning("Código Vacío", "Por favor escanea un código de barras", parent=self)
            return

        # Buscar en la base de datos
        success, result = ProductDatabase.search_product(barcode)

        if success:
            # Producto encontrado - transferir datos inmediatamente
            self.on_product_selected(
                self.row_index,
                result['name'],
                result['price']
            )

            # Animación de éxito (verde)
            self.barcode_entry.config(highlightbackground='#28a745', highlightthickness=2, bg='#d4edda')

            # Cerrar ventana automáticamente después de 300ms
            self.after(300, self.destroy)
        else:
            # Producto no encontrado
            messagebox.showerror("Producto No Encontrado", result, parent=self)

            # Restaurar visibilidad y grab después del messagebox.
            # En Windows, al cerrarse el messagebox el grab del escáner no se
            # restaura automáticamente, lo que deja la app inaccesible si el
            # usuario cambia de ventana en ese momento.
            self.lift()
            self.grab_set()

            # Animación de error (rojo)
            self.barcode_entry.config(highlightbackground='#dc3545', highlightthickness=2, bg='#f8d7da')

            # Volver a color normal después de 500ms
            self.after(500, lambda: self.barcode_entry.config(
                highlightbackground='#ced4da',
                highlightthickness=2,
                bg='#f8f9fa'
            ))

            # Limpiar campo
            self.barcode_entry.delete(0, tk.END)
            self.barcode_entry.focus_set()

    def search_database_file(self):
        """Permite al usuario buscar y cargar un archivo de base de datos manualmente."""
        # Abrir diálogo para seleccionar archivo Excel
        file_path = filedialog.askopenfilename(
            title="Seleccionar Archivo de Base de Datos",
            filetypes=[("Archivos Excel", "*.xlsx"), ("Todos los archivos", "*.*")],
            parent=self
        )

        if file_path:
            try:
                # Asegurar que la carpeta bd existe
                if not os.path.exists(ProductDatabase.DB_FOLDER):
                    os.makedirs(ProductDatabase.DB_FOLDER)

                # Obtener nombre del archivo y copiar a la carpeta bd
                filename = os.path.basename(file_path)
                destination = os.path.join(ProductDatabase.DB_FOLDER, filename)

                shutil.copy2(file_path, destination)

                # Refrescar información de la base de datos
                self.update_db_info()

                messagebox.showinfo(
                    "Éxito",
                    f"Base de datos cargada correctamente:\n{filename}",
                    parent=self
                )
            except Exception as e:
                messagebox.showerror(
                    "Error",
                    f"No se pudo copiar el archivo:\n{str(e)}",
                    parent=self
                )


def show_barcode_scanner(parent, row_index, on_product_selected):
    """
    Muestra la ventana de escáner de código de barras.

    Args:
        parent: Ventana padre
        row_index (int): Índice de la fila
        on_product_selected (callable): Callback que recibe (row_index, name, price)
    """
    scanner_window = BarcodeScannerWindow(parent, row_index, on_product_selected)
    return scanner_window
