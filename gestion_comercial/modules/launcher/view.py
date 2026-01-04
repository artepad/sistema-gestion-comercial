import tkinter as tk
from datetime import datetime
from gestion_comercial.config.theme import Theme

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
        header_frame = tk.Frame(self, bg=Theme.TEXT_PRIMARY, height=120)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        # Accent line with gradient effect (simulated with multiple lines)
        accent_container = tk.Frame(header_frame, bg=Theme.TEXT_PRIMARY, height=5)
        accent_container.pack(fill='x')
        tk.Frame(accent_container, bg='#2ecc71', height=5).pack(fill='x')

        # Title with better spacing
        tk.Label(
            header_frame,
            text="Sistema de Gestión",
            font=(Theme.FONT_FAMILY, 24, 'bold'),
            bg=Theme.TEXT_PRIMARY,
            fg='white'
        ).pack(expand=True, pady=(18, 5))

        # Subtitle with improved color
        tk.Label(
            header_frame,
            text="Solución integral para tu negocio",
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

        tk.Label(
            apps_container,
            text="Selecciona una aplicación",
            font=Theme.FONTS['h2'],
            bg=Theme.BACKGROUND,
            fg=Theme.TEXT_PRIMARY
        ).pack(pady=(0, 20))

        # Container vertical centrado para botones
        buttons_container = tk.Frame(apps_container, bg=Theme.BACKGROUND)
        buttons_container.pack(expand=True)

        # Gestor de Etiquetas
        self.create_tag_manager_button(buttons_container)

        # Contador de Caja
        self.create_cash_counter_button(buttons_container)

        # Lector de Precios
        self.create_price_reader_button(buttons_container)

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

    def create_price_reader_button(self, parent):
        """Crea el botón de Lector de Precios."""
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
            text="💲",
            font=(Theme.FONT_FAMILY, 22),
            bg='white',
            fg=color,
            width=2
        )
        icon_label.pack(side='left', padx=(0, 62))

        # Título
        title_label = tk.Label(
            inner_frame,
            text="Lector de Precios",
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
        command = lambda: self.navigator.show_view('price_reader')
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

        # Footer content container
        footer_content = tk.Frame(footer_frame, bg=Theme.BACKGROUND)
        footer_content.pack(expand=True)

        # Main text
        tk.Label(
            footer_content,
            text="Sistema de Gestión Comercial ",
            font=(Theme.FONT_FAMILY, 11, 'bold'),
            bg=Theme.BACKGROUND,
            fg='#8a939e'
        ).pack(side='left')

        # "¿Necesitas ayuda?" clickeable link
        link_label = tk.Label(
            footer_content,
            text="¿Necesitas ayuda?",
            font=(Theme.FONT_FAMILY, 11, 'bold'),
            bg=Theme.BACKGROUND,
            fg=Theme.TOTAL_FG,
            cursor='hand2'
        )
        link_label.pack(side='left')
        link_label.bind('<Button-1>', lambda e: self.show_contact_info())

        # Hover effects for the link
        def on_enter(e):
            link_label.configure(fg='#1565c0', font=(Theme.FONT_FAMILY, 11, 'bold underline'))

        def on_leave(e):
            link_label.configure(fg=Theme.TOTAL_FG, font=(Theme.FONT_FAMILY, 11, 'bold'))

        link_label.bind("<Enter>", on_enter)
        link_label.bind("<Leave>", on_leave)

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

        # Center the window
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
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
