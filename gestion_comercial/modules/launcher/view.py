import os
import tkinter as tk
import shutil
from tkinter import filedialog, messagebox, ttk
from datetime import datetime
from gestion_comercial.config.theme import Theme
from gestion_comercial.config.settings import Settings
from gestion_comercial.modules.tag_manager.database import ProductDatabase

class LauncherView(tk.Frame):
    def __init__(self, parent, navigator):
        super().__init__(parent, bg=Theme.BACKGROUND)
        self.navigator = navigator
        
        self.setup_ui()
        self.update_clock()
        
    def setup_ui(self):
        # Header
        self.create_header()
        
        # Clock
        self.create_clock_section()
        
        # Apps Buttons
        self.create_apps_section()
        
        # Footer
        self.create_footer()
        
    def create_header(self):
        BIRTHDAYS = {
            (1, 19): {
                'title': 'Hoy es el cumpleaños de Miguel Ángel',
                'subtitles': [
                    'Alerta: hoy cumple años Miguel Ángel y espera ser felicitado con entusiasmo 🎂😄',
                    'Recuerda felicitarlo hoy, seguro que lo va a hacer muy feliz 🎉',
                    'Un día especial para alguien especial — ¡no olvides dedicarle un momento! 🌟',
                ]
            },
            (3, 21): {
                'title': 'Feliz Cumpleaños Rodrigo',
                'subtitles': [
                    'Que este día te traiga todo lo que mereces, hermano ✨',
                    'Gracias por estar siempre ahí, hermano — que lo disfrutes mucho 🎂',
                    'Un año más de risas, de proyectos y de crecer juntos, hermano 💪',
                ]
            },
            (4, 6): {
                'title': 'Feliz Cumpleaños Angélica',
                'subtitles': [
                    'Gracias por todo tu amor y dedicación, mamá 💖',
                    'Eres la fuerza de esta familia — que hoy sea un día tan hermoso como tú, mamá 🌸',
                    'Cada año que pasa, más agradecidos estamos de tenerte, mamá 🙏',
                ]
            },
            (9, 12): {
                'title': 'Feliz Cumpleaños Yamil',
                'subtitles': [
                    'Que sigas creciendo con alegría y éxito, hermano 🌟',
                    'Eres de los grandes, hermano — que este año sea increíble para ti 🚀',
                    'Orgullo de esta familia — feliz cumpleaños, hermano 🎊',
                ]
            },
            (12, 26): {
                'title': 'Feliz Cumpleaños Miguel',
                'subtitles': [
                    'Tu ejemplo nos guía cada día, papá 🙏',
                    'Gracias por construir la familia que somos, papá — que lo disfrutes mucho 💛',
                    'Con cada año que pasa, más te admiramos y queremos, papá ❤️',
                ]
            },
        }

        now = datetime.now()
        birthday = BIRTHDAYS.get((now.month, now.day))
        if birthday:
            title_text = birthday['title']
            subtitle_text = birthday['subtitles'][now.year % 3]
            accent_color = '#e74c3c'
        else:
            title_text = "Sistema de Gestión"
            subtitle_text = "Solución integral para tu negocio"
            accent_color = '#2ecc71'

        header_frame = tk.Frame(self, bg=Theme.TEXT_PRIMARY, height=120)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        # Accent line
        accent_container = tk.Frame(header_frame, bg=Theme.TEXT_PRIMARY, height=5)
        accent_container.pack(fill='x')
        tk.Frame(accent_container, bg=accent_color, height=5).pack(fill='x')

        tk.Label(
            header_frame,
            text=title_text,
            font=(Theme.FONT_FAMILY, 24, 'bold'),
            bg=Theme.TEXT_PRIMARY,
            fg='white'
        ).pack(expand=True, pady=(18, 5))

        tk.Label(
            header_frame,
            text=subtitle_text,
            font=(Theme.FONT_FAMILY, 13),
            bg=Theme.TEXT_PRIMARY,
            fg='#b4bcc4'
        ).pack(pady=(0, 18))

    def create_clock_section(self):
        clock_frame = tk.Frame(self, bg=Theme.BACKGROUND)
        clock_frame.pack(fill='x', pady=15)

        # Clock with improved font
        self.clock_label = tk.Label(
            clock_frame,
            text="00:00:00",
            font=(Theme.FONT_FAMILY, 52, 'bold'),
            bg=Theme.BACKGROUND,
            fg=Theme.TEXT_PRIMARY
        )
        self.clock_label.pack()

        # Date with better styling
        self.date_label = tk.Label(
            clock_frame,
            text="",
            font=(Theme.FONT_FAMILY, 15),
            bg=Theme.BACKGROUND,
            fg='#6c757d'
        )
        self.date_label.pack(pady=(8, 0))

    def create_apps_section(self):
        apps_container = tk.Frame(self, bg=Theme.BACKGROUND)
        apps_container.pack(fill='both', expand=True, padx=80, pady=(10, 20))

        # Container vertical centrado para botones
        buttons_container = tk.Frame(apps_container, bg=Theme.BACKGROUND)
        buttons_container.pack(expand=True)

        # Gestor de Etiquetas
        self.create_tag_manager_button(buttons_container)

        # Contador de Caja
        self.create_cash_counter_button(buttons_container)

        # Punto de Venta
        self.create_point_of_sale_button(buttons_container)

        # Comparador de Precios
        self.create_price_comparator_button(buttons_container)

    def create_tag_manager_button(self, parent):
        """Crea el botón de Gestor de Etiquetas."""
        color = '#3498db'   

        # Container principal con sombra
        button_container = tk.Frame(parent, bg=Theme.BACKGROUND)
        button_container.pack(pady=8)

        # Sombra
        shadow = tk.Frame(button_container, bg='#c8d0d8', bd=0)
        shadow.place(x=2, y=2, relwidth=1, relheight=1)

        # Botón principal rectangular
        button_frame = tk.Frame(
            button_container,
            bg='white',
            bd=0,
            highlightthickness=2,
            highlightbackground='#dde1e6',
            highlightcolor=color
        )
        button_frame.pack()

        # Frame interior con padding
        inner_frame = tk.Frame(button_frame, bg='white')
        inner_frame.pack(fill='both', expand=True, padx=25, pady=18)

        # Container para el icono (permite posicionamiento absoluto)
        icon_container = tk.Frame(inner_frame, bg='white')
        icon_container.pack(side='left', padx=(0, 15))

        # Icono del emoji
        icon_emoji = tk.Label(
            icon_container,
            text="🏷️",
            font=(Theme.FONT_FAMILY, 22),
            bg='white',
            fg=color
        )
        icon_emoji.pack()

        # Título
        title_label = tk.Label(
            inner_frame,
            text="Gestor de Etiquetas",
            font=(Theme.FONT_FAMILY, 14, 'bold'),
            bg='white',
            fg=Theme.TEXT_PRIMARY,
            anchor='w'
        )
        title_label.pack(side='left', fill='both', expand=True)

        # Tamaño fijo
        button_frame.config(width=420, height=77)
        button_frame.pack_propagate(False)

        # Hacer clickeable
        command = lambda: self.navigator.show_view('tag_manager')
        widgets = [button_container, shadow, button_frame, inner_frame,
                   icon_container, icon_emoji, title_label]
        for widget in widgets:
            widget.bind('<Button-1>', lambda e: command())
            widget.config(cursor='hand2')

        # Efectos hover
        def on_enter(e):
            button_frame.configure(highlightbackground=color, highlightthickness=3, bg='#f8f9fa')
            inner_frame.configure(bg='#f8f9fa')
            icon_container.configure(bg='#f8f9fa')
            icon_emoji.configure(bg='#f8f9fa')
            title_label.configure(bg='#f8f9fa')
            shadow.place(x=4, y=4, relwidth=1, relheight=1)

        def on_leave(e):
            button_frame.configure(highlightbackground='#dde1e6', highlightthickness=2, bg='white')
            inner_frame.configure(bg='white')
            icon_container.configure(bg='white')
            icon_emoji.configure(bg='white')
            title_label.configure(bg='white')
            shadow.place(x=2, y=2, relwidth=1, relheight=1)

        for widget in widgets:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)

    def create_cash_counter_button(self, parent):
        """Crea el botón de Contador de Caja."""
        color = '#e67e22'

        # Container principal con sombra
        button_container = tk.Frame(parent, bg=Theme.BACKGROUND)
        button_container.pack(pady=8)

        # Sombra
        shadow = tk.Frame(button_container, bg='#c8d0d8', bd=0)
        shadow.place(x=2, y=2, relwidth=1, relheight=1)

        # Botón principal rectangular
        button_frame = tk.Frame(
            button_container,
            bg='white',
            bd=0,
            highlightthickness=2,
            highlightbackground='#dde1e6',
            highlightcolor=color
        )
        button_frame.pack()

        # Frame interior con padding
        inner_frame = tk.Frame(button_frame, bg='white')
        inner_frame.pack(fill='both', expand=True, padx=25, pady=18)

        # Icono a la izquierda
        icon_label = tk.Label(
            inner_frame,
            text="💰",
            font=(Theme.FONT_FAMILY, 22),
            bg='white',
            fg=color,
            width=2
        )
        icon_label.pack(side='left', padx=(0, 62))

        # Título
        title_label = tk.Label(
            inner_frame,
            text="Contador de Caja",
            font=(Theme.FONT_FAMILY, 14, 'bold'),
            bg='white',
            fg=Theme.TEXT_PRIMARY,
            anchor='w'
        )
        title_label.pack(side='left', fill='both', expand=True)

        # Tamaño fijo
        button_frame.config(width=420, height=77)
        button_frame.pack_propagate(False)

        # Hacer clickeable
        command = lambda: self.navigator.show_view('cash_counter')
        widgets = [button_container, shadow, button_frame, inner_frame, icon_label, title_label]
        for widget in widgets:
            widget.bind('<Button-1>', lambda e: command())
            widget.config(cursor='hand2')

        # Efectos hover
        def on_enter(e):
            button_frame.configure(highlightbackground=color, highlightthickness=3, bg='#f8f9fa')
            inner_frame.configure(bg='#f8f9fa')
            icon_label.configure(bg='#f8f9fa')
            title_label.configure(bg='#f8f9fa')
            shadow.place(x=4, y=4, relwidth=1, relheight=1)

        def on_leave(e):
            button_frame.configure(highlightbackground='#dde1e6', highlightthickness=2, bg='white')
            inner_frame.configure(bg='white')
            icon_label.configure(bg='white')
            title_label.configure(bg='white')
            shadow.place(x=2, y=2, relwidth=1, relheight=1)

        for widget in widgets:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)

    def create_point_of_sale_button(self, parent):
        """Crea el botón de Punto de Venta."""
        color = '#27ae60'

        # Container principal con sombra
        button_container = tk.Frame(parent, bg=Theme.BACKGROUND)
        button_container.pack(pady=8)

        # Sombra
        shadow = tk.Frame(button_container, bg='#c8d0d8', bd=0)
        shadow.place(x=2, y=2, relwidth=1, relheight=1)

        # Botón principal rectangular
        button_frame = tk.Frame(
            button_container,
            bg='white',
            bd=0,
            highlightthickness=2,
            highlightbackground='#dde1e6',
            highlightcolor=color
        )
        button_frame.pack()

        # Frame interior con padding
        inner_frame = tk.Frame(button_frame, bg='white')
        inner_frame.pack(fill='both', expand=True, padx=25, pady=18)

        # Icono a la izquierda
        icon_label = tk.Label(
            inner_frame,
            text="🛒",
            font=(Theme.FONT_FAMILY, 22),
            bg='white',
            fg=color,
            width=2
        )
        icon_label.pack(side='left', padx=(0, 62))

        # Título
        title_label = tk.Label(
            inner_frame,
            text="Punto de Venta",
            font=(Theme.FONT_FAMILY, 14, 'bold'),
            bg='white',
            fg=Theme.TEXT_PRIMARY,
            anchor='w'
        )
        title_label.pack(side='left', fill='both', expand=True)

        # Tamaño fijo
        button_frame.config(width=420, height=77)
        button_frame.pack_propagate(False)

        # Hacer clickeable
        command = lambda: self.navigator.show_view('point_of_sale')
        widgets = [button_container, shadow, button_frame, inner_frame, icon_label, title_label]
        for widget in widgets:
            widget.bind('<Button-1>', lambda e: command())
            widget.config(cursor='hand2')

        # Efectos hover
        def on_enter(e):
            button_frame.configure(highlightbackground=color, highlightthickness=3, bg='#f8f9fa')
            inner_frame.configure(bg='#f8f9fa')
            icon_label.configure(bg='#f8f9fa')
            title_label.configure(bg='#f8f9fa')
            shadow.place(x=4, y=4, relwidth=1, relheight=1)

        def on_leave(e):
            button_frame.configure(highlightbackground='#dde1e6', highlightthickness=2, bg='white')
            inner_frame.configure(bg='white')
            icon_label.configure(bg='white')
            title_label.configure(bg='white')
            shadow.place(x=2, y=2, relwidth=1, relheight=1)

        for widget in widgets:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)

    def create_price_comparator_button(self, parent):
        """Crea el botón de Comparador de Precios."""
        color = '#9b59b6'

        # Container principal con sombra
        button_container = tk.Frame(parent, bg=Theme.BACKGROUND)
        button_container.pack(pady=8)

        # Sombra
        shadow = tk.Frame(button_container, bg='#c8d0d8', bd=0)
        shadow.place(x=2, y=2, relwidth=1, relheight=1)

        # Botón principal rectangular
        button_frame = tk.Frame(
            button_container,
            bg='white',
            bd=0,
            highlightthickness=2,
            highlightbackground='#dde1e6',
            highlightcolor=color
        )
        button_frame.pack()

        # Frame interior con padding
        inner_frame = tk.Frame(button_frame, bg='white')
        inner_frame.pack(fill='both', expand=True, padx=25, pady=18)

        # Icono a la izquierda
        icon_label = tk.Label(
            inner_frame,
            text="⚖️",
            font=(Theme.FONT_FAMILY, 22),
            bg='white',
            fg=color,
            width=2
        )
        icon_label.pack(side='left', padx=(0, 62))

        # Título
        title_label = tk.Label(
            inner_frame,
            text="Comparador de Precios",
            font=(Theme.FONT_FAMILY, 14, 'bold'),
            bg='white',
            fg=Theme.TEXT_PRIMARY,
            anchor='w'
        )
        title_label.pack(side='left', fill='both', expand=True)

        # Tamaño fijo
        button_frame.config(width=420, height=77)
        button_frame.pack_propagate(False)

        # Hacer clickeable
        command = lambda: self.navigator.show_view('price_comparator')
        widgets = [button_container, shadow, button_frame, inner_frame, icon_label, title_label]
        for widget in widgets:
            widget.bind('<Button-1>', lambda e: command())
            widget.config(cursor='hand2')

        # Efectos hover
        def on_enter(e):
            button_frame.configure(highlightbackground=color, highlightthickness=3, bg='#f8f9fa')
            inner_frame.configure(bg='#f8f9fa')
            icon_label.configure(bg='#f8f9fa')
            title_label.configure(bg='#f8f9fa')
            shadow.place(x=4, y=4, relwidth=1, relheight=1)

        def on_leave(e):
            button_frame.configure(highlightbackground='#dde1e6', highlightthickness=2, bg='white')
            inner_frame.configure(bg='white')
            icon_label.configure(bg='white')
            title_label.configure(bg='white')
            shadow.place(x=2, y=2, relwidth=1, relheight=1)

        for widget in widgets:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)

    def create_app_button(self, parent, title, icon, command, color):
        # Container principal con sombra
        button_container = tk.Frame(parent, bg=Theme.BACKGROUND)
        button_container.pack(pady=8)

        # Sombra
        shadow = tk.Frame(button_container, bg='#c8d0d8', bd=0)
        shadow.place(x=2, y=2, relwidth=1, relheight=1)

        # Botón principal rectangular
        button_frame = tk.Frame(
            button_container,
            bg='white',
            bd=0,
            highlightthickness=2,
            highlightbackground='#dde1e6',
            highlightcolor=color
        )
        button_frame.pack()

        # Frame interior con padding - layout horizontal
        inner_frame = tk.Frame(button_frame, bg='white')
        inner_frame.pack(fill='both', expand=True, padx=25, pady=18)

        # Icono a la izquierda
        icon_label = tk.Label(
            inner_frame,
            text=icon,
            font=(Theme.FONT_FAMILY, 32),
            bg='white',
            fg=color,
            width=2
        )
        icon_label.pack(side='left', padx=(0, 32))

        # Título
        title_label = tk.Label(
            inner_frame,
            text=title,
            font=(Theme.FONT_FAMILY, 14, 'bold'),
            bg='white',
            fg=Theme.TEXT_PRIMARY,
            anchor='w'
        )
        title_label.pack(side='left', fill='both', expand=True)

        # Tamaño fijo para uniformidad
        button_frame.config(width=450, height=65)
        button_frame.pack_propagate(False)

        # Hacer todos los elementos clickeables
        widgets = [button_container, shadow, button_frame, inner_frame,
                   icon_label, title_label]

        for widget in widgets:
            widget.bind('<Button-1>', lambda e: command())
            widget.config(cursor='hand2')

        # Efectos hover
        def on_enter(e):
            button_frame.configure(
                highlightbackground=color,
                highlightthickness=3,
                bg='#f8f9fa'
            )
            inner_frame.configure(bg='#f8f9fa')
            icon_label.configure(bg='#f8f9fa')
            title_label.configure(bg='#f8f9fa')
            shadow.place(x=4, y=4, relwidth=1, relheight=1)

        def on_leave(e):
            button_frame.configure(
                highlightbackground='#dde1e6',
                highlightthickness=2,
                bg='white'
            )
            inner_frame.configure(bg='white')
            icon_label.configure(bg='white')
            title_label.configure(bg='white')
            shadow.place(x=2, y=2, relwidth=1, relheight=1)

        for widget in widgets:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)

    def create_footer(self):
        footer_frame = tk.Frame(self, bg=Theme.BACKGROUND, height=65)
        footer_frame.pack(fill='x', side='bottom')
        footer_frame.pack_propagate(False)

        # Separator line with better color
        tk.Frame(footer_frame, bg='#dde1e6', height=2).pack(fill='x', pady=(10, 8))

        # Footer content container (fill width for left/right layout)
        footer_content = tk.Frame(footer_frame, bg=Theme.BACKGROUND)
        footer_content.pack(fill='x', expand=True, padx=15)

        # ☰ icon — right side (packed first so it anchors to the right)
        config_label = tk.Label(
            footer_content,
            text="☰",
            font=(Theme.FONT_FAMILY, 16),
            bg=Theme.BACKGROUND,
            fg='#8a939e',
            cursor='hand2'
        )
        config_label.pack(side='right')
        config_label.bind('<Button-1>', lambda e: self.show_settings())

        def on_config_enter(e):
            config_label.configure(fg=Theme.TOTAL_FG)

        def on_config_leave(e):
            config_label.configure(fg='#8a939e')

        config_label.bind("<Enter>", on_config_enter)
        config_label.bind("<Leave>", on_config_leave)

        # Center group: main text + help link
        center_frame = tk.Frame(footer_content, bg=Theme.BACKGROUND)
        center_frame.pack(side='left', expand=True)

        tk.Label(
            center_frame,
            text="Sistema de Gestión Comercial ",
            font=(Theme.FONT_FAMILY, 11, 'bold'),
            bg=Theme.BACKGROUND,
            fg='#8a939e'
        ).pack(side='left')

        # "¿Necesitas ayuda?" clickeable link
        link_label = tk.Label(
            center_frame,
            text="¿Necesitas ayuda?",
            font=(Theme.FONT_FAMILY, 11, 'bold'),
            bg=Theme.BACKGROUND,
            fg=Theme.TOTAL_FG,
            cursor='hand2'
        )
        link_label.pack(side='left')
        link_label.bind('<Button-1>', lambda e: self.show_contact_info())

        def on_enter(e):
            link_label.configure(fg='#1565c0', font=(Theme.FONT_FAMILY, 11, 'bold underline'))

        def on_leave(e):
            link_label.configure(fg=Theme.TOTAL_FG, font=(Theme.FONT_FAMILY, 11, 'bold'))

        link_label.bind("<Enter>", on_enter)
        link_label.bind("<Leave>", on_leave)

        config_label.bind("<Enter>", on_config_enter)
        config_label.bind("<Leave>", on_config_leave)

    def show_contact_info(self):
        """Muestra ventana emergente con información de contacto"""
        # Create popup window
        popup = tk.Toplevel(self)
        popup.title("Información de Contacto")
        popup.configure(bg=Theme.BACKGROUND)
        popup.resizable(False, False)

        # Set window size
        window_width = 480
        window_height = 320

        # Center popup over the main window
        root = self.winfo_toplevel()
        root_x = root.winfo_x()
        root_y = root.winfo_y()
        root_w = root.winfo_width()
        root_h = root.winfo_height()
        x = root_x + (root_w - window_width) // 2
        y = root_y + (root_h - window_height) // 2
        popup.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Make window modal
        popup.transient(self.master)
        popup.grab_set()

        # Header with gradient effect
        header_frame = tk.Frame(popup, bg=Theme.TEXT_PRIMARY, height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        # Accent line
        tk.Frame(header_frame, bg='#27ae60', height=4).pack(fill='x')

        # Title
        tk.Label(
            header_frame,
            text="Información de Contacto",
            font=(Theme.FONT_FAMILY, 16, 'bold'),
            bg=Theme.TEXT_PRIMARY,
            fg='white'
        ).pack(expand=True)

        # Content area with padding
        content_frame = tk.Frame(popup, bg=Theme.BACKGROUND)
        content_frame.pack(fill='both', expand=True, padx=40, pady=25)

        # Contact information with icons and styling
        contact_data = [
            ("👤", "Nombre:", "Miguel Ángel Saavedra"),
            ("📱", "Teléfono:", "+56 9 4877 7448"),
            ("📧", "Correo:", "misaavedraq1990@gmail.com")
        ]

        for icon, label_text, value_text in contact_data:
            # Container for each contact item
            item_frame = tk.Frame(content_frame, bg=Theme.BACKGROUND)
            item_frame.pack(fill='x', pady=8)

            # Icon
            tk.Label(
                item_frame,
                text=icon,
                font=(Theme.FONT_FAMILY, 20),
                bg=Theme.BACKGROUND,
                fg=Theme.TEXT_PRIMARY
            ).pack(side='left', padx=(0, 10))

            # Label and value container
            text_frame = tk.Frame(item_frame, bg=Theme.BACKGROUND)
            text_frame.pack(side='left', fill='x', expand=True)

            # Label
            tk.Label(
                text_frame,
                text=label_text,
                font=(Theme.FONT_FAMILY, 10),
                bg=Theme.BACKGROUND,
                fg='#6c757d',
                anchor='w'
            ).pack(fill='x')

            # Value
            value_label = tk.Label(
                text_frame,
                text=value_text,
                font=(Theme.FONT_FAMILY, 10, 'bold'),
                bg=Theme.BACKGROUND,
                fg=Theme.TEXT_PRIMARY,
                anchor='w',
                wraplength=360
            )
            value_label.pack(fill='x')

        # Close button with styling
        button_frame = tk.Frame(popup, bg=Theme.BACKGROUND)
        button_frame.pack(fill='x', padx=40, pady=(0, 25))

        close_button = tk.Button(
            button_frame,
            text="Cerrar",
            font=(Theme.FONT_FAMILY, 11, 'bold'),
            bg='#27ae60',
            fg='white',
            bd=0,
            padx=30,
            pady=10,
            cursor='hand2',
            command=popup.destroy
        )
        close_button.pack()

        # Hover effects for button
        def on_button_enter(e):
            close_button.configure(bg='#1e8449')

        def on_button_leave(e):
            close_button.configure(bg='#27ae60')

        close_button.bind("<Enter>", on_button_enter)
        close_button.bind("<Leave>", on_button_leave)

    def show_settings(self):
        """Muestra ventana emergente de configuración del sistema"""
        popup = tk.Toplevel(self)
        popup.title("Configuración del Sistema")
        popup.configure(bg=Theme.BACKGROUND)
        popup.resizable(False, False)

        window_width = 520
        window_height = 420
        root = self.winfo_toplevel()
        root_x = root.winfo_x()
        root_y = root.winfo_y()
        root_w = root.winfo_width()
        root_h = root.winfo_height()
        x = root_x + (root_w - window_width) // 2
        y = root_y + (root_h - window_height) // 2
        popup.geometry(f"{window_width}x{window_height}+{x}+{y}")

        popup.transient(self.master)
        popup.grab_set()

        # Header
        header_frame = tk.Frame(popup, bg=Theme.TEXT_PRIMARY, height=70)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        tk.Frame(header_frame, bg='#27ae60', height=4).pack(fill='x')
        tk.Label(
            header_frame,
            text="Configuración del Sistema",
            font=(Theme.FONT_FAMILY, 16, 'bold'),
            bg=Theme.TEXT_PRIMARY,
            fg='white'
        ).pack(expand=True)

        # Content area
        content_frame = tk.Frame(popup, bg=Theme.BACKGROUND)
        content_frame.pack(fill='both', expand=True, padx=25, pady=15)

        # === Database Section ===
        db_section = tk.LabelFrame(
            content_frame,
            text="  Base de Datos  ",
            font=(Theme.FONT_FAMILY, 11, 'bold'),
            bg=Theme.BACKGROUND,
            fg=Theme.TEXT_PRIMARY,
            bd=1,
            relief='solid',
            padx=15,
            pady=10
        )
        db_section.pack(fill='x', pady=(0, 12))

        # DB status info
        db_info = ProductDatabase.get_database_info()

        status_frame = tk.Frame(db_section, bg=Theme.BACKGROUND)
        status_frame.pack(fill='x', pady=(5, 10))

        if db_info['exists']:
            status_color = '#27ae60'
            status_text = f"Conectada  ({db_info['total_products']} productos)"
            date_text = f"Última actualización: {db_info['last_modified']}"
        else:
            status_color = '#e74c3c'
            status_text = "Sin base de datos"
            date_text = "Cargue un archivo .xlsx para comenzar"

        # Status indicator
        status_row = tk.Frame(status_frame, bg=Theme.BACKGROUND)
        status_row.pack(fill='x')

        tk.Label(
            status_row,
            text="Estado:",
            font=(Theme.FONT_FAMILY, 10),
            bg=Theme.BACKGROUND,
            fg='#6c757d'
        ).pack(side='left')

        tk.Label(
            status_row,
            text="  ●",
            font=(Theme.FONT_FAMILY, 12),
            bg=Theme.BACKGROUND,
            fg=status_color
        ).pack(side='left')

        self._db_status_label = tk.Label(
            status_row,
            text=f" {status_text}",
            font=(Theme.FONT_FAMILY, 10, 'bold'),
            bg=Theme.BACKGROUND,
            fg=Theme.TEXT_PRIMARY
        )
        self._db_status_label.pack(side='left')

        self._db_date_label = tk.Label(
            status_frame,
            text=date_text,
            font=(Theme.FONT_FAMILY, 9),
            bg=Theme.BACKGROUND,
            fg='#6c757d',
            anchor='w'
        )
        self._db_date_label.pack(fill='x', padx=(52, 0))

        # DB Buttons
        btn_frame = tk.Frame(db_section, bg=Theme.BACKGROUND)
        btn_frame.pack(fill='x', pady=(5, 0))

        load_btn = tk.Button(
            btn_frame,
            text="Cargar Base de Datos",
            font=(Theme.FONT_FAMILY, 10, 'bold'),
            bg='#3498db',
            fg='white',
            bd=0,
            padx=15,
            pady=8,
            cursor='hand2',
            command=lambda: self._load_database(popup)
        )
        load_btn.pack(side='left', padx=(0, 10))

        self._delete_btn = tk.Button(
            btn_frame,
            text="Eliminar BD",
            font=(Theme.FONT_FAMILY, 10, 'bold'),
            bg='#e74c3c' if db_info['exists'] else '#bdc3c7',
            fg='white',
            bd=0,
            padx=15,
            pady=8,
            cursor='hand2' if db_info['exists'] else 'arrow',
            state='normal' if db_info['exists'] else 'disabled',
            command=lambda: self._delete_database(popup)
        )
        self._delete_btn.pack(side='left')

        # Hover effects for buttons
        def on_load_enter(e):
            load_btn.configure(bg='#2980b9')
        def on_load_leave(e):
            load_btn.configure(bg='#3498db')
        load_btn.bind("<Enter>", on_load_enter)
        load_btn.bind("<Leave>", on_load_leave)

        def on_delete_enter(e):
            if self._delete_btn['state'] != 'disabled':
                self._delete_btn.configure(bg='#c0392b')
        def on_delete_leave(e):
            if self._delete_btn['state'] != 'disabled':
                self._delete_btn.configure(bg='#e74c3c')
        self._delete_btn.bind("<Enter>", on_delete_enter)
        self._delete_btn.bind("<Leave>", on_delete_leave)

        # === Screen Section ===
        screen_section = tk.LabelFrame(
            content_frame,
            text="  Pantalla  ",
            font=(Theme.FONT_FAMILY, 11, 'bold'),
            bg=Theme.BACKGROUND,
            fg=Theme.TEXT_PRIMARY,
            bd=1,
            relief='solid',
            padx=15,
            pady=10
        )
        screen_section.pack(fill='x', pady=(0, 10))

        # Resolution row
        res_row = tk.Frame(screen_section, bg=Theme.BACKGROUND)
        res_row.pack(fill='x', pady=(5, 5))

        tk.Label(
            res_row,
            text="Resolución:",
            font=(Theme.FONT_FAMILY, 10),
            bg=Theme.BACKGROUND,
            fg='#6c757d'
        ).pack(side='left', padx=(0, 10))

        res_options = [f"{w} x {h}" for w, h in Settings.AVAILABLE_RESOLUTIONS]
        current_res = f"{Settings.WINDOW_WIDTH} x {Settings.WINDOW_HEIGHT}"

        self._res_combo = ttk.Combobox(
            res_row,
            values=res_options,
            state='readonly',
            font=(Theme.FONT_FAMILY, 10),
            width=15
        )
        self._res_combo.set(current_res)
        self._res_combo.pack(side='left')
        self._res_combo.bind('<<ComboboxSelected>>', lambda e: self._on_resolution_change())

        self._res_note = tk.Label(
            screen_section,
            text="",
            font=(Theme.FONT_FAMILY, 9, 'italic'),
            bg=Theme.BACKGROUND,
            fg='#27ae60',
            anchor='w'
        )
        self._res_note.pack(fill='x')

        # Align top checkbox
        self._align_top_var = tk.BooleanVar(value=Settings.ALIGN_TOP)
        align_check = tk.Checkbutton(
            screen_section,
            text="Iniciar ventana alineada en la parte superior",
            variable=self._align_top_var,
            font=(Theme.FONT_FAMILY, 10),
            bg=Theme.BACKGROUND,
            fg=Theme.TEXT_PRIMARY,
            activebackground=Theme.BACKGROUND,
            selectcolor='white',
            cursor='hand2',
            command=self._on_align_top_change
        )
        align_check.pack(fill='x', pady=(5, 0), anchor='w')

        tk.Label(
            screen_section,
            text="Útil en equipos con alta resolución donde la ventana puede aparecer cortada",
            font=(Theme.FONT_FAMILY, 8, 'italic'),
            bg=Theme.BACKGROUND,
            fg='#95a5a6',
            anchor='w'
        ).pack(fill='x', padx=(22, 0))

        # Close button
        button_frame = tk.Frame(popup, bg=Theme.BACKGROUND)
        button_frame.pack(fill='x', padx=25, pady=(0, 20))

        close_button = tk.Button(
            button_frame,
            text="Cerrar",
            font=(Theme.FONT_FAMILY, 11, 'bold'),
            bg='#27ae60',
            fg='white',
            bd=0,
            padx=30,
            pady=10,
            cursor='hand2',
            command=popup.destroy
        )
        close_button.pack()

        def on_close_enter(e):
            close_button.configure(bg='#1e8449')
        def on_close_leave(e):
            close_button.configure(bg='#27ae60')
        close_button.bind("<Enter>", on_close_enter)
        close_button.bind("<Leave>", on_close_leave)

    def _refresh_db_status(self):
        """Actualiza los labels de estado de la BD en el popup de configuración"""
        db_info = ProductDatabase.get_database_info()

        if db_info['exists']:
            status_text = f" Conectada  ({db_info['total_products']} productos)"
            date_text = f"Última actualización: {db_info['last_modified']}"
            self._db_status_label.configure(text=status_text)
            self._db_date_label.configure(text=date_text)
            self._delete_btn.configure(
                bg='#e74c3c', state='normal', cursor='hand2'
            )
        else:
            self._db_status_label.configure(text=" Sin base de datos")
            self._db_date_label.configure(text="Cargue un archivo .xlsx para comenzar")
            self._delete_btn.configure(
                bg='#bdc3c7', state='disabled', cursor='arrow'
            )

    def _load_database(self, popup):
        """Permite al usuario seleccionar y cargar un archivo de base de datos"""
        file_path = filedialog.askopenfilename(
            parent=popup,
            title="Seleccionar Base de Datos",
            filetypes=[("Archivos Excel", "*.xlsx")],
            initialdir=os.path.expanduser("~")
        )

        if not file_path:
            return

        try:
            # Ensure bd directory exists
            bd_folder = ProductDatabase.DB_FOLDER
            os.makedirs(bd_folder, exist_ok=True)

            # Copy file to bd folder
            dest_path = os.path.join(bd_folder, os.path.basename(file_path))
            shutil.copy2(file_path, dest_path)

            self._refresh_db_status()
            messagebox.showinfo(
                "Base de Datos Cargada",
                f"Se cargó correctamente:\n{os.path.basename(file_path)}",
                parent=popup
            )
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"No se pudo cargar la base de datos:\n{str(e)}",
                parent=popup
            )

    def _delete_database(self, popup):
        """Elimina la base de datos actual previa confirmación"""
        confirm = messagebox.askyesno(
            "Confirmar Eliminación",
            "¿Está seguro que desea eliminar la base de datos?\n\nEsta acción no se puede deshacer.",
            parent=popup
        )

        if not confirm:
            return

        try:
            db_file = ProductDatabase.get_db_file()
            if db_file and os.path.exists(db_file):
                os.remove(db_file)
                self._refresh_db_status()
                messagebox.showinfo(
                    "Base de Datos Eliminada",
                    "La base de datos fue eliminada correctamente.",
                    parent=popup
                )
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"No se pudo eliminar la base de datos:\n{str(e)}",
                parent=popup
            )

    def _on_resolution_change(self):
        """Maneja el cambio de resolución en el combobox"""
        selected = self._res_combo.get()
        parts = selected.split(' x ')
        new_w, new_h = int(parts[0]), int(parts[1])

        # Update settings in memory and save
        Settings.WINDOW_WIDTH = new_w
        Settings.WINDOW_HEIGHT = new_h
        Settings.save()

        # Resize the main window immediately
        root = self.winfo_toplevel()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - new_w) // 2
        if Settings.ALIGN_TOP:
            y = 0
        else:
            y = (screen_height - new_h) // 2
        root.geometry(f"{new_w}x{new_h}+{x}+{y}")

        self._res_note.configure(text="✓ Configuración guardada")

    def _on_align_top_change(self):
        """Maneja el cambio del checkbox de alinear arriba"""
        Settings.ALIGN_TOP = self._align_top_var.get()
        Settings.save()

        # Apply immediately
        root = self.winfo_toplevel()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - Settings.WINDOW_WIDTH) // 2
        if Settings.ALIGN_TOP:
            y = 0
        else:
            y = (screen_height - Settings.WINDOW_HEIGHT) // 2
        root.geometry(f"{Settings.WINDOW_WIDTH}x{Settings.WINDOW_HEIGHT}+{x}+{y}")

        self._res_note.configure(text="✓ Configuración guardada")

    def update_clock(self):
        now = datetime.now()
        self.clock_label.config(text=now.strftime("%H:%M:%S"))
        
        # Simple date formatting for now, can add translation later if needed
        date_str = now.strftime("%A, %d de %B de %Y")
        # Quick translation map
        translations = {
            'Monday': 'Lunes', 'Tuesday': 'Martes', 'Wednesday': 'Miércoles',
            'Thursday': 'Jueves', 'Friday': 'Viernes', 'Saturday': 'Sábado',
            'Sunday': 'Domingo', 'January': 'Enero', 'February': 'Febrero',
            'March': 'Marzo', 'April': 'Abril', 'May': 'Mayo', 'June': 'Junio',
            'July': 'Julio', 'August': 'Agosto', 'September': 'Septiembre',
            'October': 'Octubre', 'November': 'Noviembre', 'December': 'Diciembre'
        }
        for eng, esp in translations.items():
            date_str = date_str.replace(eng, esp)
            
        self.date_label.config(text=date_str)
        self.after(1000, self.update_clock)
