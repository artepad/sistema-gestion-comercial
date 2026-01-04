"""
Vista del lector de precios.
Permite consultar precios mediante escáner de código de barras con dos modos:
- Modo normal: interfaz completa con controles
- Modo pantalla completa: solo muestra precio y nombre (uso público)
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil
from datetime import datetime
from gestion_comercial.config.theme import Theme
from gestion_comercial.modules.tag_manager.database import ProductDatabase


class PriceReaderView(tk.Frame):
    def __init__(self, parent, navigator):
        super().__init__(parent, bg=Theme.BACKGROUND)
        self.navigator = navigator
        self.fullscreen_mode = False
        self.auto_clear_timer = None
        self.typing_timer = None
        self.typing_text = ""
        self.typing_index = 0
        self.current_message_index = 0

        # Lista de mensajes que se mostrarán en ciclo
        self.typing_messages = [
            "Esperando escaneo...",
            "Sistema listo para operar...",
            "Acerca el código de barras...",
            "Consulta de precios activa...",
            "Listo para atender..."
        ]

        # Binding global para F5 (activar pantalla completa) y Escape (salir)
        self.bind_all('<F5>', self.enter_fullscreen)
        self.bind_all('<Escape>', self.exit_fullscreen)

        self.setup_ui()

    def setup_ui(self):
        """Configura la interfaz según el modo actual."""
        if self.fullscreen_mode:
            self.create_fullscreen_ui()
        else:
            self.create_normal_ui()

    def create_normal_ui(self):
        """Crea la interfaz en modo normal."""
        # Top green accent strip
        self.create_top_accent()

        # Header
        self.create_header()

        # Container principal
        main_container = tk.Frame(self, bg=Theme.BACKGROUND)
        main_container.pack(fill='both', expand=True, padx=40, pady=20)

        # Instrucciones
        tk.Label(
            main_container,
            text="Escanea el código de barras del producto para consultar su precio",
            font=(Theme.FONT_FAMILY, 12),
            bg=Theme.BACKGROUND,
            fg='#6c757d'
        ).pack(pady=(0, 20))

        # Campo de entrada
        input_frame = tk.Frame(main_container, bg=Theme.BACKGROUND)
        input_frame.pack(fill='x', pady=(0, 25))

        tk.Label(
            input_frame,
            text="Código de barras:",
            font=(Theme.FONT_FAMILY, 11, 'bold'),
            bg=Theme.BACKGROUND,
            fg=Theme.TEXT_PRIMARY
        ).pack(anchor='w', pady=(0, 5))

        self.barcode_entry = tk.Entry(
            input_frame,
            font=(Theme.FONT_FAMILY, 13),
            bg='white',
            fg=Theme.TEXT_PRIMARY,
            bd=0,
            relief='flat',
            highlightthickness=2,
            highlightcolor='#2ecc71',
            highlightbackground='#2ecc71'
        )
        self.barcode_entry.pack(fill='x', ipady=8)
        self.barcode_entry.bind('<Return>', self.search_product)
        self.barcode_entry.focus_set()

        # Área de resultados
        self.result_frame = tk.LabelFrame(
            main_container,
            text="📊 Información del Producto",
            font=(Theme.FONT_FAMILY, 11, 'bold'),
            bg='#f8f9fa',
            fg='#495057',
            padx=25,
            pady=15
        )
        self.result_frame.pack(fill='both', expand=True, pady=(0, 15))

        # Mensaje inicial
        self.result_content = tk.Frame(self.result_frame, bg='#f8f9fa')
        self.result_content.pack(fill='both', expand=True)

        self.show_initial_message()

        # Información de base de datos
        self.create_db_info_section(main_container)

        # Botones inferiores
        self.create_bottom_buttons(main_container)

        # Bottom blue accent strip
        self.create_bottom_accent()

    def create_fullscreen_ui(self):
        """Crea la interfaz en modo pantalla completa."""
        # Configurar ventana principal en pantalla completa
        root = self.winfo_toplevel()
        root.attributes('-fullscreen', True)

        # Container principal centrado con fondo blanco limpio
        main_container = tk.Frame(self, bg='white')
        main_container.pack(fill='both', expand=True)

        # Frame centrado verticalmente y horizontalmente
        center_frame = tk.Frame(main_container, bg='white')
        center_frame.place(relx=0.5, rely=0.5, anchor='center')

        # Instrucciones iniciales
        self.instruction_label = tk.Label(
            center_frame,
            text="Escanea el código de barras del producto",
            font=(Theme.FONT_FAMILY, 28, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        self.instruction_label.pack(pady=(0, 50))

        # Campo de entrada minimalista sin bordes visibles
        self.barcode_entry = tk.Entry(
            center_frame,
            font=(Theme.FONT_FAMILY, 36),
            bg='white',
            fg='#2c3e50',
            bd=0,
            highlightthickness=0,
            insertwidth=3,
            insertbackground='#000000',
            justify='center',
            width=20
        )
        self.barcode_entry.pack(ipady=15)
        self.barcode_entry.bind('<Return>', self.search_product)
        self.barcode_entry.focus_set()

        # Label con efecto de tipeo debajo del campo de entrada
        self.typing_label = tk.Label(
            center_frame,
            text="",
            font=(Theme.FONT_FAMILY, 18),
            bg='white',
            fg='#7f8c8d'
        )
        self.typing_label.pack(pady=(20, 0))

        # Iniciar efecto de tipeo cíclico (sin parámetros para usar el ciclo)
        self.start_typing_effect()

        # Icono de escáner debajo
        self.scanner_icon = tk.Label(
            center_frame,
            text="📊",
            font=(Theme.FONT_FAMILY, 70),
            bg='white'
        )
        self.scanner_icon.pack(pady=(40, 20))

        # Nombre del producto (oculto inicialmente)
        self.product_name_label = tk.Label(
            center_frame,
            text="",
            font=(Theme.FONT_FAMILY, 32, 'bold'),
            bg='white',
            fg='#2c3e50',
            wraplength=900
        )

        # Precio del producto (oculto inicialmente)
        self.product_price_label = tk.Label(
            center_frame,
            text="",
            font=(Theme.FONT_FAMILY, 120, 'bold'),
            bg='white',
            fg='#27ae60'
        )

        # Mensaje de error (oculto inicialmente)
        self.error_label = tk.Label(
            center_frame,
            text="",
            font=(Theme.FONT_FAMILY, 28, 'bold'),
            bg='white',
            fg='#e74c3c',
            wraplength=800
        )

        # Indicador de modo (esquina superior derecha)
        mode_label = tk.Label(
            main_container,
            text="Modo pantalla completa (salir con Escape)",
            font=(Theme.FONT_FAMILY, 10),
            bg='white',
            fg='#95a5a6'
        )
        mode_label.place(relx=1.0, rely=0.0, anchor='ne', x=-20, y=20)

    def create_top_accent(self):
        """Crea la franja verde superior."""
        accent_frame = tk.Frame(self, bg='#2ecc71', height=5)
        accent_frame.pack(fill='x')
        accent_frame.pack_propagate(False)

    def create_bottom_accent(self):
        """Crea la franja azul inferior."""
        accent_frame = tk.Frame(self, bg=Theme.TOTAL_FG, height=5)
        accent_frame.pack(side='bottom', fill='x')
        accent_frame.pack_propagate(False)

    def create_header(self):
        """Crea el header en modo normal."""
        header_frame = tk.Frame(self, bg=Theme.TEXT_PRIMARY, height=70)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        content_container = tk.Frame(header_frame, bg=Theme.TEXT_PRIMARY)
        content_container.place(relx=0.5, rely=0.5, anchor='center')

        tk.Label(
            content_container,
            text="Lector de Precios",
            font=(Theme.FONT_FAMILY, 20, 'bold'),
            bg=Theme.TEXT_PRIMARY,
            fg='white'
        ).pack()

    def create_bottom_buttons(self, parent):
        """Crea los botones en la parte inferior."""
        button_container = tk.Frame(parent, bg=Theme.BACKGROUND)
        button_container.pack(fill='x', pady=(15, 0))

        # Container centrado para los botones
        buttons_center = tk.Frame(button_container, bg=Theme.BACKGROUND)
        buttons_center.pack(anchor='center')

        # Botón Volver
        back_button = tk.Button(
            buttons_center,
            text="⬅ Volver",
            font=(Theme.FONT_FAMILY, 11, 'bold'),
            bg=Theme.TOTAL_FG,
            fg='white',
            bd=0,
            padx=25,
            pady=10,
            cursor='hand2',
            command=lambda: self.navigator.show_view('launcher')
        )
        back_button.pack(side='left', padx=(0, 10))

        def on_back_enter(e):
            back_button.config(bg='#1565c0')

        def on_back_leave(e):
            back_button.config(bg=Theme.TOTAL_FG)

        back_button.bind('<Enter>', on_back_enter)
        back_button.bind('<Leave>', on_back_leave)

        # Botón Pantalla Completa
        fullscreen_button = tk.Button(
            buttons_center,
            text="Modo pantalla completa",
            font=(Theme.FONT_FAMILY, 11, 'bold'),
            bg=Theme.BILLS_FG,
            fg='white',
            bd=0,
            padx=25,
            pady=10,
            cursor='hand2',
            command=self.toggle_fullscreen
        )
        fullscreen_button.pack(side='left', padx=(10, 0))

        def on_full_enter(e):
            fullscreen_button.config(bg='#1e7e34')

        def on_full_leave(e):
            fullscreen_button.config(bg=Theme.BILLS_FG)

        fullscreen_button.bind('<Enter>', on_full_enter)
        fullscreen_button.bind('<Leave>', on_full_leave)

    def create_db_info_section(self, parent):
        """Crea la sección de información de la base de datos."""
        info_frame = tk.LabelFrame(
            parent,
            text="💾 Información de Base de Datos",
            font=(Theme.FONT_FAMILY, 11, 'bold'),
            bg='white',
            fg='#2c3e50',
            relief='solid',
            bd=1,
            padx=20,
            pady=15
        )
        info_frame.pack(fill='x', pady=(15, 0))

        # Obtener información de la BD
        db_info = ProductDatabase.get_database_info()

        if db_info['exists']:
            # Estado de conexión
            status_container = tk.Frame(info_frame, bg='white')
            status_container.pack(fill='x', pady=(0, 10))

            tk.Label(
                status_container,
                text="Estado:",
                font=(Theme.FONT_FAMILY, 10),
                bg='white',
                fg='#495057'
            ).pack(side='left')

            tk.Label(
                status_container,
                text="Conectada",
                font=(Theme.FONT_FAMILY, 10, 'bold'),
                bg='white',
                fg='#28a745'
            ).pack(side='left', padx=(10, 0))

            # Enlace para eliminar base de datos (al lado de Estado)
            delete_link = tk.Label(
                status_container,
                text="🗑 Eliminar base de datos",
                font=(Theme.FONT_FAMILY, 9),
                bg='white',
                fg='#6c757d',
                cursor='hand2'
            )
            delete_link.pack(side='left', padx=(20, 0))

            # Hover effect
            def on_delete_enter(e):
                delete_link.config(fg='#dc3545', font=(Theme.FONT_FAMILY, 9, 'underline'))

            def on_delete_leave(e):
                delete_link.config(fg='#6c757d', font=(Theme.FONT_FAMILY, 9))

            delete_link.bind('<Enter>', on_delete_enter)
            delete_link.bind('<Leave>', on_delete_leave)
            delete_link.bind('<Button-1>', lambda e: self.delete_database())

            # Última actualización
            update_container = tk.Frame(info_frame, bg='white')
            update_container.pack(fill='x', pady=(0, 10))

            tk.Label(
                update_container,
                text="Última actualización:",
                font=(Theme.FONT_FAMILY, 10),
                bg='white',
                fg='#495057'
            ).pack(side='left')

            tk.Label(
                update_container,
                text=db_info['last_modified'],
                font=(Theme.FONT_FAMILY, 10, 'bold'),
                bg='white',
                fg='#2c3e50'
            ).pack(side='left', padx=(10, 0))

            # Verificar antigüedad de la base de datos y mostrar advertencias
            days_old = self.get_database_age_days()
            if days_old is not None:
                if days_old >= 30:
                    # Advertencia roja para más de 30 días
                    tk.Label(
                        update_container,
                        text="⚠ La base de datos lleva un mes desactualizada",
                        font=(Theme.FONT_FAMILY, 9, 'bold'),
                        bg='white',
                        fg='#dc3545'  # Rojo
                    ).pack(side='left', padx=(15, 0))
                elif days_old >= 15:
                    # Advertencia amarilla para más de 15 días
                    tk.Label(
                        update_container,
                        text="⚠ La BD tiene más de una semana desactualizada",
                        font=(Theme.FONT_FAMILY, 9, 'bold'),
                        bg='white',
                        fg='#f39c12'  # Amarillo/Naranja
                    ).pack(side='left', padx=(15, 0))

            # Productos disponibles
            products_container = tk.Frame(info_frame, bg='white')
            products_container.pack(fill='x')

            tk.Label(
                products_container,
                text="Productos disponibles:",
                font=(Theme.FONT_FAMILY, 10),
                bg='white',
                fg='#495057'
            ).pack(side='left')

            tk.Label(
                products_container,
                text=str(db_info['total_products']),
                font=(Theme.FONT_FAMILY, 10, 'bold'),
                bg='white',
                fg='#2c3e50'
            ).pack(side='left', padx=(10, 0))
        else:
            # Mensaje de error
            error_container = tk.Frame(info_frame, bg='white')
            error_container.pack(fill='x', pady=(0, 8))

            tk.Label(
                error_container,
                text="Estado:",
                font=(Theme.FONT_FAMILY, 10),
                bg='white',
                fg='#495057'
            ).pack(side='left')

            tk.Label(
                error_container,
                text="✗ No disponible",
                font=(Theme.FONT_FAMILY, 10, 'bold'),
                bg='white',
                fg='#dc3545'
            ).pack(side='left', padx=(10, 0))

            # Instrucción
            tk.Label(
                info_frame,
                text="No se encontró ningún archivo de base de datos en la carpeta.",
                font=(Theme.FONT_FAMILY, 9),
                bg='white',
                fg='#6c757d',
                wraplength=600,
                justify='left'
            ).pack(fill='x', pady=(0, 10))

            # Botón para buscar base de datos
            search_button = tk.Button(
                info_frame,
                text="🔍 Buscar Base de Datos",
                font=(Theme.FONT_FAMILY, 10, 'bold'),
                bg='#3498db',
                fg='white',
                bd=0,
                padx=20,
                pady=8,
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

    def show_initial_message(self):
        """Muestra el mensaje inicial en el área de resultados."""
        # Limpiar contenido anterior
        for widget in self.result_content.winfo_children():
            widget.destroy()

        # Mensaje de espera
        tk.Label(
            self.result_content,
            text="🔍",
            font=(Theme.FONT_FAMILY, 50),
            bg='#f8f9fa',
            fg='#6c757d'
        ).pack(pady=(20, 10))

        tk.Label(
            self.result_content,
            text="Esperando escaneo...",
            font=(Theme.FONT_FAMILY, 13),
            bg='#f8f9fa',
            fg='#6c757d'
        ).pack()

    def show_product_info(self, product_data):
        """Muestra la información del producto encontrado."""
        if self.fullscreen_mode:
            # Detener animación de tipeo
            if self.typing_timer:
                self.after_cancel(self.typing_timer)

            # Ocultar elementos iniciales
            self.instruction_label.pack_forget()
            self.scanner_icon.pack_forget()
            self.error_label.pack_forget()
            self.barcode_entry.pack_forget()
            self.typing_label.pack_forget()

            # Mostrar nombre y precio
            self.product_name_label.config(text=product_data['name'])
            self.product_name_label.pack(pady=(0, 20))

            price_text = f"${self.format_price(product_data['price'])}"
            self.product_price_label.config(text=price_text)
            self.product_price_label.pack(pady=10)

            # Auto-limpiar después de 5 segundos
            self.schedule_auto_clear()
        else:
            # Limpiar contenido anterior
            for widget in self.result_content.winfo_children():
                widget.destroy()

            # Mostrar información del producto
            tk.Label(
                self.result_content,
                text="✓ Producto Encontrado",
                font=(Theme.FONT_FAMILY, 12, 'bold'),
                bg='#f8f9fa',
                fg='#28a745'
            ).pack(pady=(8, 15))

            # Nombre del producto
            tk.Label(
                self.result_content,
                text="Producto:",
                font=(Theme.FONT_FAMILY, 9, 'bold'),
                bg='#f8f9fa',
                fg='#495057',
                anchor='w'
            ).pack(fill='x', pady=(0, 3))

            tk.Label(
                self.result_content,
                text=product_data['name'],
                font=(Theme.FONT_FAMILY, 12),
                bg='#f8f9fa',
                fg=Theme.TEXT_PRIMARY,
                anchor='w',
                wraplength=650
            ).pack(fill='x', pady=(0, 12))

            # Precio
            tk.Label(
                self.result_content,
                text="Precio:",
                font=(Theme.FONT_FAMILY, 9, 'bold'),
                bg='#f8f9fa',
                fg='#495057',
                anchor='w'
            ).pack(fill='x', pady=(0, 3))

            price_text = f"${self.format_price(product_data['price'])}"
            tk.Label(
                self.result_content,
                text=price_text,
                font=(Theme.FONT_FAMILY, 32, 'bold'),
                bg='#f8f9fa',
                fg='#27ae60',
                anchor='w'
            ).pack(fill='x', pady=(0, 8))

    def get_database_age_days(self):
        """Calcula cuántos días han pasado desde la última actualización de la BD.

        Returns:
            int: Número de días desde la última actualización, o None si hay error
        """
        db_info = ProductDatabase.get_database_info()
        if not db_info['exists']:
            return None

        try:
            # Parse date string (format: "DD/MM/YYYY HH:MM")
            date_str = db_info['last_modified']
            if date_str == "Archivo no encontrado":
                return None

            last_update = datetime.strptime(date_str, "%d/%m/%Y %H:%M")
            today = datetime.now()
            delta = today - last_update
            return delta.days
        except Exception:
            return None

    def show_error_message(self, error_msg):
        """Muestra un mensaje de error."""
        if self.fullscreen_mode:
            # Detener animación de tipeo
            if self.typing_timer:
                self.after_cancel(self.typing_timer)

            # Ocultar elementos
            self.instruction_label.pack_forget()
            self.scanner_icon.pack_forget()
            self.product_name_label.pack_forget()
            self.product_price_label.pack_forget()
            self.barcode_entry.pack_forget()
            self.typing_label.pack_forget()

            # Mostrar error
            self.error_label.config(text=f"✗ {error_msg}")
            self.error_label.pack(pady=20)

            # Auto-limpiar después de 5 segundos
            self.schedule_auto_clear()
        else:
            # Limpiar contenido anterior
            for widget in self.result_content.winfo_children():
                widget.destroy()

            # Mostrar error
            tk.Label(
                self.result_content,
                text="✗",
                font=(Theme.FONT_FAMILY, 50),
                bg='#f8f9fa',
                fg='#dc3545'
            ).pack(pady=(20, 10))

            tk.Label(
                self.result_content,
                text=error_msg,
                font=(Theme.FONT_FAMILY, 13),
                bg='#f8f9fa',
                fg='#dc3545',
                wraplength=600
            ).pack(pady=(0, 20))

    def search_product(self, event=None):
        """Busca el producto en la base de datos."""
        barcode = self.barcode_entry.get().strip()

        if not barcode:
            return

        # Buscar en la base de datos
        success, result = ProductDatabase.search_product(barcode)

        if success:
            self.show_product_info(result)
        else:
            self.show_error_message(result)

        # Limpiar campo de entrada
        self.barcode_entry.delete(0, tk.END)
        self.barcode_entry.focus_set()

    def schedule_auto_clear(self):
        """Programa la limpieza automática de la pantalla."""
        # Cancelar timer anterior si existe
        if self.auto_clear_timer:
            self.after_cancel(self.auto_clear_timer)

        # Programar nueva limpieza en 5 segundos
        self.auto_clear_timer = self.after(5000, self.clear_fullscreen_display)

    def clear_fullscreen_display(self):
        """Limpia la pantalla en modo fullscreen."""
        if self.fullscreen_mode:
            # Ocultar todo
            self.product_name_label.pack_forget()
            self.product_price_label.pack_forget()
            self.error_label.pack_forget()

            # Mostrar estado inicial
            self.instruction_label.pack(pady=(0, 50))

            # Mostrar campo de entrada nuevamente
            self.barcode_entry.pack(ipady=15)

            # Mostrar label de tipeo nuevamente
            self.typing_label.pack(pady=(20, 0))

            # Mostrar icono
            self.scanner_icon.pack(pady=(40, 20))

            # Reiniciar efecto de tipeo cíclico (continúa con el ciclo)
            self.start_typing_effect()

            # Mantener focus en entrada
            self.barcode_entry.focus_set()

    def start_typing_effect(self, text=None):
        """Inicia el efecto de tipeo animado con ciclo de mensajes."""
        # Solo continuar si estamos en modo pantalla completa
        if not self.fullscreen_mode:
            return

        # Cancelar timer anterior si existe
        if self.typing_timer:
            self.after_cancel(self.typing_timer)

        # Si no se proporciona texto, usar el mensaje actual del ciclo
        if text is None:
            self.typing_text = self.typing_messages[self.current_message_index]
        else:
            self.typing_text = text

        # Reiniciar índice
        self.typing_index = 0

        # Limpiar label si existe
        if hasattr(self, 'typing_label') and self.typing_label.winfo_exists():
            try:
                self.typing_label.config(text="")
            except:
                return

        # Iniciar animación de escritura
        self.type_next_character()

    def type_next_character(self):
        """Escribe el siguiente carácter del texto con efecto de tipeo."""
        # Verificar que seguimos en modo pantalla completa y el widget existe
        if not self.fullscreen_mode:
            return

        if not hasattr(self, 'typing_label') or not self.typing_label.winfo_exists():
            return

        if self.typing_index < len(self.typing_text):
            # Agregar siguiente carácter
            current_text = self.typing_text[:self.typing_index + 1]
            try:
                self.typing_label.config(text=current_text)
            except:
                return

            # Incrementar índice
            self.typing_index += 1

            # Programar siguiente carácter (80ms para efecto de tipeo natural)
            self.typing_timer = self.after(80, self.type_next_character)
        else:
            # Texto completo - esperar 2 segundos y luego borrar
            self.typing_timer = self.after(2000, self.start_erasing)

    def start_erasing(self):
        """Inicia el efecto de borrado del texto."""
        if not self.fullscreen_mode:
            return

        if hasattr(self, 'typing_label') and self.typing_label.winfo_exists():
            self.erase_next_character()

    def erase_next_character(self):
        """Borra el texto carácter por carácter."""
        # Verificar que seguimos en modo pantalla completa y el widget existe
        if not self.fullscreen_mode:
            return

        if not hasattr(self, 'typing_label') or not self.typing_label.winfo_exists():
            return

        try:
            current_text = self.typing_label.cget('text')

            if len(current_text) > 0:
                # Borrar último carácter
                self.typing_label.config(text=current_text[:-1])

                # Programar siguiente borrado (50ms para efecto más rápido)
                self.typing_timer = self.after(50, self.erase_next_character)
            else:
                # Texto completamente borrado - avanzar al siguiente mensaje
                self.advance_to_next_message()
        except:
            return

    def advance_to_next_message(self):
        """Avanza al siguiente mensaje en el ciclo y lo muestra."""
        if not self.fullscreen_mode:
            return

        # Avanzar al siguiente mensaje (ciclo)
        self.current_message_index = (self.current_message_index + 1) % len(self.typing_messages)

        # Esperar 500ms antes de escribir el siguiente mensaje
        self.typing_timer = self.after(500, self.start_typing_effect)

    def enter_fullscreen(self, event=None):
        """Activa el modo pantalla completa (solo si no está activo)."""
        if not self.fullscreen_mode:
            self.fullscreen_mode = True

            # Limpiar interfaz actual
            for widget in self.winfo_children():
                widget.destroy()

            # Recrear interfaz en modo pantalla completa
            self.setup_ui()

    def toggle_fullscreen(self, event=None):
        """Alterna entre modo normal y pantalla completa."""
        self.fullscreen_mode = not self.fullscreen_mode

        # Limpiar interfaz actual
        for widget in self.winfo_children():
            widget.destroy()

        # Recrear interfaz
        self.setup_ui()

    def exit_fullscreen(self, event=None):
        """Sale del modo pantalla completa."""
        if self.fullscreen_mode:
            # Cancelar todos los timers activos
            if self.typing_timer:
                self.after_cancel(self.typing_timer)
                self.typing_timer = None

            if self.auto_clear_timer:
                self.after_cancel(self.auto_clear_timer)
                self.auto_clear_timer = None

            # Cambiar modo
            self.fullscreen_mode = False

            # Restaurar ventana normal
            root = self.winfo_toplevel()
            root.attributes('-fullscreen', False)

            # Limpiar y recrear interfaz
            for widget in self.winfo_children():
                widget.destroy()

            self.setup_ui()

    def format_price(self, price):
        """Formatea el precio con separadores de miles."""
        return f"{int(price):,}".replace(',', '.')

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

    def update_db_info(self):
        """Actualiza la información de la base de datos en la interfaz."""
        # Limpiar y recrear la interfaz para reflejar los cambios
        for widget in self.winfo_children():
            widget.destroy()

        self.setup_ui()
