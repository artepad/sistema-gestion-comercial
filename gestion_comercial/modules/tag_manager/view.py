import tkinter as tk
from tkinter import ttk, messagebox
import re
from gestion_comercial.config.theme import Theme
from gestion_comercial.modules.tag_manager.model import TagManagerModel
from gestion_comercial.modules.tag_manager.barcode_scanner import show_barcode_scanner

class TagManagerView(tk.Frame):
    def __init__(self, parent, navigator):
        super().__init__(parent, bg=Theme.BACKGROUND)
        self.navigator = navigator
        self.model = TagManagerModel()

        # Listas para pestaña de etiquetas normales
        self.product_entries = []
        self.price_entries = []

        # Sistema dinámico de ofertas
        self.offer_queue = []          # Lista de dicts (max 4), formato compatible con model
        self.current_offer_type = None
        self.form_frames = {}          # {'normal': Frame, ...}
        self.form_entries = {}         # {'normal': {'product': Entry, ...}, ...}
        self.type_buttons = {}         # {'normal': Button, ...}
        self.slot_cards = []           # 4 frames para visualizar la cola

        # Configuración de tipos de oferta
        self.offer_types = {
            'normal': {'label': 'Oferta Normal', 'color': '#e74c3c', 'icon': '🏷️'},
            'percentage': {'label': 'Oferta %', 'color': '#f39c12', 'icon': '💯'},
            'quantity': {'label': 'x Cantidad', 'color': '#9b59b6', 'icon': '📦'},
            'daily': {'label': 'Prod. del Día', 'color': '#3498db', 'icon': '⭐'},
        }

        self.setup_ui()
        
    def setup_ui(self):
        # Top green accent strip
        self.create_top_accent()

        self.create_header()

        # Contenedor principal con padding
        main_container = tk.Frame(self, bg=Theme.BACKGROUND, padx=40, pady=10)
        main_container.pack(fill='both', expand=True)

        # Crear sistema de pestañas
        self.create_notebook(main_container)

        # Bottom blue accent strip
        self.create_bottom_accent()
        
    def create_top_accent(self):
        """Creates the top green accent strip matching the launcher"""
        accent_frame = tk.Frame(self, bg='#2ecc71', height=5)
        accent_frame.pack(fill='x')
        accent_frame.pack_propagate(False)

    def create_bottom_accent(self):
        """Creates the bottom blue accent strip"""
        accent_frame = tk.Frame(self, bg=Theme.TOTAL_FG, height=5)
        accent_frame.pack(side='bottom', fill='x')
        accent_frame.pack_propagate(False)

    def create_header(self):
        header_frame = tk.Frame(self, bg=Theme.TEXT_PRIMARY, height=70)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        # Content container for centering
        content_container = tk.Frame(header_frame, bg=Theme.TEXT_PRIMARY)
        content_container.place(relx=0.5, rely=0.5, anchor='center')

        # Title only (sin subtítulo)
        tk.Label(
            content_container,
            text="Gestor de Etiquetas",
            font=(Theme.FONT_FAMILY, 20, 'bold'),
            bg=Theme.TEXT_PRIMARY,
            fg='white'
        ).pack()

    def create_notebook(self, parent):
        """Crea el sistema de pestañas para etiquetas normales y de oferta"""
        # Estilo personalizado para las pestañas
        style = ttk.Style()
        style.theme_use('default')

        # Configurar colores de las pestañas
        style.configure(
            'Custom.TNotebook',
            background=Theme.BACKGROUND,
            borderwidth=0,
            tabmargins=[0, 0, 0, 0]
        )
        style.configure(
            'Custom.TNotebook.Tab',
            background='#e5e7eb',
            foreground=Theme.TEXT_PRIMARY,
            padding=[12, 3],  # Reducido aún más: [12, 3]
            font=(Theme.FONT_FAMILY, 9, 'bold')  # Reducido a 9pt
        )
        style.map(
            'Custom.TNotebook.Tab',
            background=[('selected', '#3498db'), ('active', '#5dade2')],
            foreground=[('selected', 'white'), ('active', 'white')]
        )

        # Crear el notebook
        self.notebook = ttk.Notebook(parent, style='Custom.TNotebook')
        self.notebook.pack(fill='both', expand=True)

        # Pestaña 1: Etiquetas Normales
        self.normal_tab = tk.Frame(self.notebook, bg=Theme.BACKGROUND)
        self.notebook.add(self.normal_tab, text='Etiquetas Normales')

        # Pestaña 2: Etiquetas de Oferta
        self.offer_tab = tk.Frame(self.notebook, bg=Theme.BACKGROUND)
        self.notebook.add(self.offer_tab, text='Etiquetas de Oferta')

        # Crear contenido de cada pestaña
        self.create_normal_tags_content(self.normal_tab)
        self.create_offer_tags_content(self.offer_tab)

    def create_normal_tags_content(self, parent):
        """Crea el contenido de la pestaña de etiquetas normales"""
        # Contenedor para el formulario
        self.create_product_form(parent)
        self.create_button_panel(parent)

    def create_offer_tags_content(self, parent):
        """Crea el contenido dinámico de la pestaña de etiquetas de oferta"""
        main_container = tk.Frame(parent, bg=Theme.BACKGROUND)
        main_container.pack(expand=True, fill='both')

        # Botones al fondo (se empaquetan primero con side='bottom')
        self.create_offer_button_panel(main_container)

        # Contenido principal (se expande en el espacio restante)
        content_area = tk.Frame(main_container, bg=Theme.BACKGROUND)
        content_area.pack(expand=True, fill='both', pady=(5, 0))

        # === ZONA 1: Selector de tipo de oferta ===
        self.create_offer_type_selector(content_area)

        # === ZONA 2: Formulario dinámico ===
        self.create_dynamic_form_area(content_area)

        # === ZONA 3: Cola de ofertas ===
        self.create_offer_queue_display(content_area)

        # Seleccionar el primer tipo por defecto
        self.select_offer_type('normal')

    # --- ZONA 1: Selector de tipo ---

    def create_offer_type_selector(self, parent):
        """Crea la fila de botones para seleccionar el tipo de oferta"""
        selector_frame = tk.Frame(parent, bg=Theme.BACKGROUND)
        selector_frame.pack(fill='x', pady=(8, 12))

        # Título con estilo consistente
        tk.Label(
            selector_frame,
            text="Seleccione el tipo de oferta:",
            font=(Theme.FONT_FAMILY, 10),
            bg=Theme.BACKGROUND,
            fg='#6b7280'
        ).pack(anchor='w', pady=(0, 8))

        # Frame para los botones centrados
        buttons_frame = tk.Frame(selector_frame, bg=Theme.BACKGROUND)
        buttons_frame.pack(anchor='w')

        for type_key, config in self.offer_types.items():
            btn = tk.Button(
                buttons_frame,
                text=f"{config['icon']}  {config['label']}",
                font=(Theme.FONT_FAMILY, 10, 'bold'),
                bg='white',
                fg=config['color'],
                relief='flat',
                bd=0,
                padx=16,
                pady=8,
                cursor='hand2',
                highlightthickness=1,
                highlightbackground='#e5e7eb',
                activebackground=config['color'],
                activeforeground='white',
                command=lambda k=type_key: self.select_offer_type(k)
            )
            btn.pack(side='left', padx=(0, 10))
            self.type_buttons[type_key] = btn

            # Hover
            color = config['color']
            def on_enter(e, b=btn, c=color, k=type_key):
                if self.current_offer_type != k:
                    b.configure(bg=c, fg='white')
            def on_leave(e, b=btn, c=color, k=type_key):
                if self.current_offer_type != k:
                    b.configure(bg='white', fg=c)
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)

    def select_offer_type(self, type_key):
        """Selecciona un tipo de oferta y muestra su formulario"""
        self.current_offer_type = type_key

        # Actualizar botones
        for key, btn in self.type_buttons.items():
            config = self.offer_types[key]
            if key == type_key:
                btn.configure(bg=config['color'], fg='white',
                              highlightthickness=2, highlightbackground=config['color'])
            else:
                btn.configure(bg='white', fg=config['color'],
                              highlightthickness=1, highlightbackground='#e5e7eb')

        # Actualizar borde del formulario con el color del tipo
        color = self.offer_types[type_key]['color']
        self.form_outer.configure(highlightbackground=color, highlightthickness=2)

        # Mostrar formulario correspondiente
        self.form_frames[type_key].tkraise()

    # --- ZONA 2: Formulario dinámico ---

    def create_dynamic_form_area(self, parent):
        """Crea el contenedor con los 4 formularios apilados"""
        # Contenedor con borde coloreado
        self.form_outer = tk.Frame(
            parent,
            bg='white',
            highlightbackground='#e5e7eb',
            highlightthickness=2,
            padx=20,
            pady=12
        )
        self.form_outer.pack(fill='x', pady=(0, 15))

        # Contenedor interno para apilar formularios con grid
        self.form_container = tk.Frame(self.form_outer, bg='white')
        self.form_container.pack(fill='x')
        self.form_container.grid_rowconfigure(0, weight=1)
        self.form_container.grid_columnconfigure(0, weight=1)

        # Crear los 4 formularios apilados
        self.create_normal_offer_form()
        self.create_percent_offer_form()
        self.create_quantity_offer_form()
        self.create_daily_offer_form()

    def _styled_entry(self, parent, width=None, **kwargs):
        """Crea un Entry con estilo consistente (bordes suaves)"""
        config = {
            'font': (Theme.FONT_FAMILY, 10),
            'bg': 'white',
            'relief': 'flat',
            'bd': 1,
            'highlightthickness': 1,
            'highlightbackground': '#e5e7eb',
            'highlightcolor': '#3498db',
        }
        if width:
            config['width'] = width
        config.update(kwargs)
        entry = tk.Entry(parent, **config)
        return entry

    def create_normal_offer_form(self):
        """Formulario: Oferta Normal (Precio Antes/Ahora)"""
        frame = tk.Frame(self.form_container, bg='white')
        frame.grid(row=0, column=0, sticky='nsew')

        self._form_title(frame, "Oferta Normal", '#e74c3c',
                         "Muestra precio anterior tachado y precio actual")

        # Fila 1: Producto
        row1 = tk.Frame(frame, bg='white')
        row1.pack(fill='x', pady=(10, 8))
        tk.Label(row1, text="Producto:", font=(Theme.FONT_FAMILY, 10),
                 bg='white', fg='#495057', width=12, anchor='w').pack(side='left')
        product_entry = self._styled_entry(row1)
        product_entry.pack(side='left', fill='x', expand=True, ipady=4)

        # Fila 2: Precios
        row2 = tk.Frame(frame, bg='white')
        row2.pack(fill='x', pady=(0, 8))

        tk.Label(row2, text="Precio Antes:", font=(Theme.FONT_FAMILY, 10),
                 bg='white', fg='#e74c3c', width=12, anchor='w').pack(side='left')
        pf1 = tk.Frame(row2, bg='white')
        pf1.pack(side='left', padx=(0, 25))
        tk.Label(pf1, text="$", font=(Theme.FONT_FAMILY, 11, 'bold'),
                 bg='white', fg='#e74c3c').pack(side='left')
        price_before = self._styled_entry(pf1, width=12)
        price_before.pack(side='left', padx=(4, 0), ipady=4)

        tk.Label(row2, text="Precio Ahora:", font=(Theme.FONT_FAMILY, 10),
                 bg='white', fg='#27ae60', width=12, anchor='w').pack(side='left')
        pf2 = tk.Frame(row2, bg='white')
        pf2.pack(side='left')
        tk.Label(pf2, text="$", font=(Theme.FONT_FAMILY, 11, 'bold'),
                 bg='white', fg='#27ae60').pack(side='left')
        price_now = self._styled_entry(pf2, width=12)
        price_now.pack(side='left', padx=(4, 0), ipady=4)

        self._add_button(frame)

        self.form_frames['normal'] = frame
        self.form_entries['normal'] = {
            'product': product_entry,
            'price_before': price_before,
            'price_now': price_now
        }

    def create_percent_offer_form(self):
        """Formulario: Oferta con Porcentaje"""
        frame = tk.Frame(self.form_container, bg='white')
        frame.grid(row=0, column=0, sticky='nsew')

        self._form_title(frame, "Oferta con Porcentaje", '#f39c12',
                         "Muestra descuento porcentual y precios antes/ahora")

        # Fila 1: Producto y Descuento
        row1 = tk.Frame(frame, bg='white')
        row1.pack(fill='x', pady=(10, 8))
        tk.Label(row1, text="Producto:", font=(Theme.FONT_FAMILY, 10),
                 bg='white', fg='#495057', width=12, anchor='w').pack(side='left')
        product_entry = self._styled_entry(row1, width=28)
        product_entry.pack(side='left', padx=(0, 25), ipady=4)

        tk.Label(row1, text="Descuento:", font=(Theme.FONT_FAMILY, 10),
                 bg='white', fg='#f39c12').pack(side='left')
        combo = ttk.Combobox(
            row1,
            values=['5%', '10%', '15%', '20%', '30%', '40%', '50%'],
            state='readonly',
            font=(Theme.FONT_FAMILY, 10),
            width=8
        )
        combo.pack(side='left', padx=(5, 0))
        combo.set('10%')

        # Fila 2: Precios
        row2 = tk.Frame(frame, bg='white')
        row2.pack(fill='x', pady=(0, 8))

        tk.Label(row2, text="Precio Antes:", font=(Theme.FONT_FAMILY, 10),
                 bg='white', fg='#e74c3c', width=12, anchor='w').pack(side='left')
        pf1 = tk.Frame(row2, bg='white')
        pf1.pack(side='left', padx=(0, 25))
        tk.Label(pf1, text="$", font=(Theme.FONT_FAMILY, 11, 'bold'),
                 bg='white', fg='#e74c3c').pack(side='left')
        price_before = self._styled_entry(pf1, width=12)
        price_before.pack(side='left', padx=(4, 0), ipady=4)

        tk.Label(row2, text="Precio Ahora:", font=(Theme.FONT_FAMILY, 10),
                 bg='white', fg='#27ae60', width=12, anchor='w').pack(side='left')
        pf2 = tk.Frame(row2, bg='white')
        pf2.pack(side='left')
        tk.Label(pf2, text="$", font=(Theme.FONT_FAMILY, 11, 'bold'),
                 bg='white', fg='#27ae60').pack(side='left')
        price_now = self._styled_entry(pf2, width=12)
        price_now.pack(side='left', padx=(4, 0), ipady=4)

        self._add_button(frame)

        self.form_frames['percentage'] = frame
        self.form_entries['percentage'] = {
            'product': product_entry,
            'price_before': price_before,
            'price_now': price_now,
            'combo': combo
        }

    def create_quantity_offer_form(self):
        """Formulario: Oferta por Cantidad"""
        frame = tk.Frame(self.form_container, bg='white')
        frame.grid(row=0, column=0, sticky='nsew')

        self._form_title(frame, "Oferta por Cantidad", '#9b59b6',
                         "Formato: 3 x $1.000 (cantidad por precio total)")

        # Fila 1: Producto
        row1 = tk.Frame(frame, bg='white')
        row1.pack(fill='x', pady=(10, 8))
        tk.Label(row1, text="Producto:", font=(Theme.FONT_FAMILY, 10),
                 bg='white', fg='#495057', width=12, anchor='w').pack(side='left')
        product_entry = self._styled_entry(row1)
        product_entry.pack(side='left', fill='x', expand=True, ipady=4)

        # Fila 2: Cantidad y Precio
        row2 = tk.Frame(frame, bg='white')
        row2.pack(fill='x', pady=(0, 8))

        tk.Label(row2, text="Cantidad:", font=(Theme.FONT_FAMILY, 10),
                 bg='white', fg='#9b59b6', width=12, anchor='w').pack(side='left')
        quantity_entry = self._styled_entry(row2, width=10)
        quantity_entry.pack(side='left', padx=(0, 25), ipady=4)
        quantity_entry.insert(0, "3")

        tk.Label(row2, text="Precio Total:", font=(Theme.FONT_FAMILY, 10),
                 bg='white', fg='#9b59b6', width=12, anchor='w').pack(side='left')
        pf = tk.Frame(row2, bg='white')
        pf.pack(side='left')
        tk.Label(pf, text="$", font=(Theme.FONT_FAMILY, 11, 'bold'),
                 bg='white', fg='#9b59b6').pack(side='left')
        price_entry = self._styled_entry(pf, width=12)
        price_entry.pack(side='left', padx=(4, 0), ipady=4)

        self._add_button(frame)

        self.form_frames['quantity'] = frame
        self.form_entries['quantity'] = {
            'product': product_entry,
            'quantity': quantity_entry,
            'price': price_entry
        }

    def create_daily_offer_form(self):
        """Formulario: Producto del Día"""
        frame = tk.Frame(self.form_container, bg='white')
        frame.grid(row=0, column=0, sticky='nsew')

        self._form_title(frame, "Producto del Día", '#3498db',
                         "Destaca un producto especial del día con su precio")

        # Fila 1: Producto
        row1 = tk.Frame(frame, bg='white')
        row1.pack(fill='x', pady=(10, 8))
        tk.Label(row1, text="Producto:", font=(Theme.FONT_FAMILY, 10),
                 bg='white', fg='#495057', width=12, anchor='w').pack(side='left')
        product_entry = self._styled_entry(row1)
        product_entry.pack(side='left', fill='x', expand=True, ipady=4)

        # Fila 2: Precio
        row2 = tk.Frame(frame, bg='white')
        row2.pack(fill='x', pady=(0, 8))

        tk.Label(row2, text="Precio:", font=(Theme.FONT_FAMILY, 10),
                 bg='white', fg='#3498db', width=12, anchor='w').pack(side='left')
        pf = tk.Frame(row2, bg='white')
        pf.pack(side='left')
        tk.Label(pf, text="$", font=(Theme.FONT_FAMILY, 11, 'bold'),
                 bg='white', fg='#3498db').pack(side='left')
        price_entry = self._styled_entry(pf, width=12)
        price_entry.pack(side='left', padx=(4, 0), ipady=4)

        self._add_button(frame)

        self.form_frames['daily'] = frame
        self.form_entries['daily'] = {
            'product': product_entry,
            'price': price_entry
        }

    def _form_title(self, parent, title, color, description):
        """Crea título y descripción para un formulario de oferta"""
        # Separador visual superior
        sep = tk.Frame(parent, bg=color, height=3)
        sep.pack(fill='x', pady=(0, 8))

        title_frame = tk.Frame(parent, bg='white')
        title_frame.pack(fill='x', pady=(0, 2))
        tk.Label(
            title_frame, text=title,
            font=(Theme.FONT_FAMILY, 13, 'bold'),
            bg='white', fg=color
        ).pack(side='left')
        tk.Label(
            title_frame, text=f"  —  {description}",
            font=(Theme.FONT_FAMILY, 9),
            bg='white', fg='#adb5bd'
        ).pack(side='left')

    def _add_button(self, parent):
        """Crea el botón 'Agregar Oferta' dentro de un formulario"""
        # Separador sutil
        tk.Frame(parent, bg='#f0f0f0', height=1).pack(fill='x', pady=(8, 8))

        btn_frame = tk.Frame(parent, bg='white')
        btn_frame.pack(fill='x', pady=(0, 2))

        btn = tk.Button(
            btn_frame,
            text="+ Agregar Oferta",
            font=(Theme.FONT_FAMILY, 10, 'bold'),
            bg='#27ae60',
            fg='white',
            relief='flat',
            bd=0,
            padx=20,
            pady=7,
            cursor='hand2',
            activebackground='#1e8449',
            activeforeground='white',
            command=self.add_offer_to_queue
        )
        btn.pack(side='right')

        def on_enter(e):
            btn.configure(bg='#1e8449')
        def on_leave(e):
            btn.configure(bg='#27ae60')
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    # --- ZONA 3: Cola de ofertas ---

    def create_offer_queue_display(self, parent):
        """Crea la visualización de los 4 slots de la cola de ofertas"""
        # Contenedor con estilo LabelFrame
        queue_section = tk.LabelFrame(
            parent,
            text="  Ofertas en cola  ",
            font=(Theme.FONT_FAMILY, 10, 'bold'),
            bg=Theme.BACKGROUND,
            fg=Theme.TEXT_PRIMARY,
            relief='solid',
            bd=1,
            padx=15,
            pady=10
        )
        queue_section.pack(fill='x', pady=(0, 0))

        # Contador
        self.queue_counter_label = tk.Label(
            queue_section,
            text="0 de 4 espacios utilizados",
            font=(Theme.FONT_FAMILY, 9),
            bg=Theme.BACKGROUND,
            fg='#6b7280'
        )
        self.queue_counter_label.pack(anchor='w', pady=(0, 8))

        # Frame para los 4 slot cards
        self.cards_frame = tk.Frame(queue_section, bg=Theme.BACKGROUND)
        self.cards_frame.pack(fill='x')

        self.slot_cards = []
        for i in range(4):
            card = tk.Frame(
                self.cards_frame,
                bg='#f8f9fa',
                highlightbackground='#dee2e6',
                highlightthickness=1,
                width=155,
                height=80
            )
            card.pack(side='left', padx=(0, 10), expand=True)
            card.pack_propagate(False)
            self.slot_cards.append(card)

        self.refresh_queue_display()

    def refresh_queue_display(self):
        """Actualiza la visualización de los 4 slots"""
        count = len(self.offer_queue)
        self.queue_counter_label.configure(
            text=f"{count} de 4 espacios utilizados",
            fg='#27ae60' if count > 0 else '#6b7280'
        )

        for i, card in enumerate(self.slot_cards):
            # Limpiar contenido del card
            for widget in card.winfo_children():
                widget.destroy()

            if i < len(self.offer_queue):
                offer = self.offer_queue[i]
                config = self.offer_types[offer['type']]
                color = config['color']

                card.configure(bg='white', highlightbackground=color, highlightthickness=2)

                # Barra superior de color
                color_bar = tk.Frame(card, bg=color, height=4)
                color_bar.pack(fill='x')

                # Contenido
                content = tk.Frame(card, bg='white')
                content.pack(fill='both', expand=True, padx=6, pady=3)

                # Tipo + botón eliminar
                top_row = tk.Frame(content, bg='white')
                top_row.pack(fill='x')
                tk.Label(
                    top_row,
                    text=f"{config['icon']} {config['label']}",
                    font=(Theme.FONT_FAMILY, 8, 'bold'),
                    bg='white', fg=color
                ).pack(side='left')

                remove_btn = tk.Label(
                    top_row,
                    text="✕",
                    font=(Theme.FONT_FAMILY, 10, 'bold'),
                    bg='white', fg='#adb5bd',
                    cursor='hand2'
                )
                remove_btn.pack(side='right')
                # Hover en el botón eliminar
                remove_btn.bind("<Enter>", lambda e, b=remove_btn: b.configure(fg='#e74c3c'))
                remove_btn.bind("<Leave>", lambda e, b=remove_btn: b.configure(fg='#adb5bd'))
                remove_btn.bind("<Button-1>", lambda e, idx=i: self.remove_offer_from_queue(idx))

                # Nombre del producto (truncado)
                product_name = offer['product']
                if len(product_name) > 18:
                    product_name = product_name[:16] + "..."
                tk.Label(
                    content,
                    text=product_name,
                    font=(Theme.FONT_FAMILY, 8),
                    bg='white', fg=Theme.TEXT_PRIMARY,
                    anchor='w'
                ).pack(fill='x')

                # Detalle de precio
                price_text = self._get_offer_price_text(offer)
                tk.Label(
                    content,
                    text=price_text,
                    font=(Theme.FONT_FAMILY, 9, 'bold'),
                    bg='white', fg='#27ae60',
                    anchor='w'
                ).pack(fill='x')

            else:
                # Slot vacío
                card.configure(bg='#f8f9fa', highlightbackground='#dee2e6', highlightthickness=1)
                empty_frame = tk.Frame(card, bg='#f8f9fa')
                empty_frame.place(relx=0.5, rely=0.5, anchor='center')
                tk.Label(
                    empty_frame,
                    text=f"{i + 1}",
                    font=(Theme.FONT_FAMILY, 14, 'bold'),
                    bg='#f8f9fa', fg='#dee2e6'
                ).pack()
                tk.Label(
                    empty_frame,
                    text="Disponible",
                    font=(Theme.FONT_FAMILY, 8),
                    bg='#f8f9fa', fg='#bdc3c7'
                ).pack()

    def _get_offer_price_text(self, offer):
        """Retorna texto resumen del precio de una oferta"""
        t = offer['type']
        if t == 'normal':
            return f"${int(offer['price_before'])} → ${int(offer['price_now'])}"
        elif t == 'percentage':
            return f"{offer['percentage']} - ${int(offer['price_now'])}"
        elif t == 'quantity':
            return f"{offer['quantity']} x ${int(offer['price'])}"
        elif t == 'daily':
            return f"${int(offer['price'])}"
        return ""

    # --- Lógica de la cola ---

    def add_offer_to_queue(self):
        """Valida el formulario actual y agrega la oferta a la cola"""
        if len(self.offer_queue) >= 4:
            messagebox.showwarning("Cola llena", "Ya tiene 4 ofertas. Elimine una para agregar otra.")
            return

        offer = self._validate_current_form()
        if offer:
            self.offer_queue.append(offer)
            self._clear_current_form()
            self.refresh_queue_display()

    def remove_offer_from_queue(self, index):
        """Elimina una oferta de la cola por índice"""
        if 0 <= index < len(self.offer_queue):
            self.offer_queue.pop(index)
            self.refresh_queue_display()

    def _validate_current_form(self):
        """Valida y retorna dict de oferta del formulario actual, o None si inválido"""
        type_key = self.current_offer_type
        entries = self.form_entries[type_key]

        if type_key == 'normal':
            product = entries['product'].get().strip()
            pb = entries['price_before'].get().strip()
            pn = entries['price_now'].get().strip()
            if not product or not pb or not pn:
                messagebox.showerror("Error", "Complete todos los campos de Oferta Normal")
                return None
            try:
                return {
                    'type': 'normal',
                    'product': product,
                    'price_before': float(pb),
                    'price_now': float(pn)
                }
            except ValueError:
                messagebox.showerror("Error", "Los precios deben ser números válidos")
                return None

        elif type_key == 'percentage':
            product = entries['product'].get().strip()
            pb = entries['price_before'].get().strip()
            pn = entries['price_now'].get().strip()
            percentage = entries['combo'].get()
            if not product or not pb or not pn or not percentage:
                messagebox.showerror("Error", "Complete todos los campos de Oferta con Porcentaje")
                return None
            try:
                return {
                    'type': 'percentage',
                    'product': product,
                    'price_before': float(pb),
                    'price_now': float(pn),
                    'percentage': percentage
                }
            except ValueError:
                messagebox.showerror("Error", "Los precios deben ser números válidos")
                return None

        elif type_key == 'quantity':
            product = entries['product'].get().strip()
            quantity = entries['quantity'].get().strip()
            price = entries['price'].get().strip()
            if not product or not quantity or not price:
                messagebox.showerror("Error", "Complete todos los campos de Oferta por Cantidad")
                return None
            try:
                return {
                    'type': 'quantity',
                    'product': product,
                    'quantity': quantity,
                    'price': float(price)
                }
            except ValueError:
                messagebox.showerror("Error", "El precio debe ser un número válido")
                return None

        elif type_key == 'daily':
            product = entries['product'].get().strip()
            price = entries['price'].get().strip()
            if not product or not price:
                messagebox.showerror("Error", "Complete todos los campos de Producto del Día")
                return None
            try:
                return {
                    'type': 'daily',
                    'product': product,
                    'price': float(price)
                }
            except ValueError:
                messagebox.showerror("Error", "El precio debe ser un número válido")
                return None

        return None

    def _clear_current_form(self):
        """Limpia los campos del formulario actual"""
        entries = self.form_entries[self.current_offer_type]
        for key, widget in entries.items():
            if key == 'combo':
                widget.set('10%')
            elif key == 'quantity':
                widget.delete(0, tk.END)
                widget.insert(0, "3")
            else:
                widget.delete(0, tk.END)

    # --- Botones y acciones ---

    def create_offer_button_panel(self, parent):
        """Crea el panel de botones al fondo de la pestaña de oferta"""
        frame = tk.Frame(parent, bg=Theme.BACKGROUND)
        frame.pack(side='bottom', fill='x', pady=(10, 5))

        # Centrar los botones
        btn_container = tk.Frame(frame, bg=Theme.BACKGROUND)
        btn_container.pack()

        self.create_styled_button(
            btn_container,
            text="⬅ Volver",
            command=lambda: self.navigator.show_view('launcher'),
            bg_color=Theme.TOTAL_FG,
            hover_color='#0d47a1'
        )
        self.create_styled_button(
            btn_container,
            text="Generar Ofertas",
            command=self.generate_offers,
            bg_color='#27ae60',
            hover_color='#1e8449'
        )
        self.create_styled_button(
            btn_container,
            text="Limpiar",
            command=self.clear_offer_form,
            bg_color='#6c757d',
            hover_color='#5a6268'
        )

    def generate_offers(self):
        """Genera las etiquetas de oferta desde la cola"""
        if not self.offer_queue:
            messagebox.showwarning("Advertencia", "Agregue al menos una oferta a la cola")
            return

        # Completar con slots vacíos hasta 4
        offers = list(self.offer_queue)
        while len(offers) < 4:
            offers.append({'type': 'empty'})

        success, message = self.model.print_offers(offers)
        if success:
            messagebox.showinfo("Éxito", "Etiquetas de ofertas generadas correctamente")
        else:
            messagebox.showerror("Error", f"Error al generar etiquetas: {message}")

    def clear_offer_form(self):
        """Limpia la cola y todos los formularios"""
        if not self.offer_queue:
            return
        if messagebox.askyesno("Confirmar", "¿Limpiar todas las ofertas de la cola?"):
            self.offer_queue.clear()
            self.refresh_queue_display()
            for type_key, entries in self.form_entries.items():
                for key, widget in entries.items():
                    if key == 'combo':
                        widget.set('10%')
                    elif key == 'quantity':
                        widget.delete(0, tk.END)
                        widget.insert(0, "3")
                    else:
                        widget.delete(0, tk.END)

    def create_product_form(self, parent):
        form_frame = tk.Frame(parent, bg='white', relief='flat', bd=0)
        form_frame.pack(fill='both', expand=True, pady=(0, 5))

        # Headers - Más compacto
        header_frame = tk.Frame(form_frame, bg=Theme.BACKGROUND, height=25)
        header_frame.pack(fill='x')

        # Header Row
        tk.Label(header_frame, text="Nombre del producto", font=(Theme.FONT_FAMILY, 9), bg=Theme.BACKGROUND, fg='#6b7280').pack(side='left', padx=(200, 0))
        tk.Label(header_frame, text="Precio", font=(Theme.FONT_FAMILY, 9), bg=Theme.BACKGROUND, fg='#6b7280').pack(side='right', padx=(0, 105))
        
        # Rows (1 to 14 in a single column)
        for row in range(14):
            self.create_product_row(form_frame, row)

    def create_product_row(self, parent, row_index):
        bg_color = 'white' if row_index % 2 == 0 else '#f8fafc'
        row_frame = tk.Frame(parent, bg=bg_color, pady=2)  # Reducido de 3 a 2
        row_frame.pack(fill='x')

        self.create_product_field(row_frame, row_index, bg_color)

    def create_product_field(self, parent, index, bg_color):
        tk.Label(parent, text=f"{index+1:02d}", font=(Theme.FONT_FAMILY, 9), bg=bg_color, fg='#6b7280', width=3).pack(side='left', padx=(20, 0))

        p_entry = tk.Entry(parent, font=(Theme.FONT_FAMILY, 9), bg='white', relief='flat', bd=1, highlightthickness=1, highlightbackground='#e5e7eb')
        p_entry.pack(side='left', padx=(15, 15), ipady=3, fill='x', expand=True)  # ipady reducido de 4 a 3
        self.product_entries.append(p_entry)

        # Botón de escáner (a la derecha)
        scanner_btn = tk.Button(
            parent,
            text="🔍",
            font=(Theme.FONT_FAMILY, 12),
            bg=Theme.BILLS_FG,
            fg='white',
            bd=0,
            padx=8,
            pady=2,
            cursor='hand2',
            command=lambda idx=index: self.open_barcode_scanner(idx)
        )
        scanner_btn.pack(side='right', padx=(0, 20))

        # Hover effects para el botón
        def on_enter(e):
            scanner_btn.configure(bg='#7b68ee')

        def on_leave(e):
            scanner_btn.configure(bg=Theme.BILLS_FG)

        scanner_btn.bind("<Enter>", on_enter)
        scanner_btn.bind("<Leave>", on_leave)

        price_container = tk.Frame(parent, bg=bg_color)
        price_container.pack(side='right', padx=(0, 10))

        tk.Label(price_container, text="$", font=(Theme.FONT_FAMILY, 9), bg=bg_color, fg='#6b7280').pack(side='left')

        pr_entry = tk.Entry(price_container, font=(Theme.FONT_FAMILY, 9), bg='white', relief='flat', bd=1, highlightthickness=1, highlightbackground='#e5e7eb', width=12)
        pr_entry.pack(side='left', padx=(2, 0), ipady=3)  # ipady reducido de 4 a 3
        self.price_entries.append(pr_entry)

        pr_entry.bind('<KeyRelease>', lambda e, idx=index: self.validate_price(e, idx))

    def create_button_panel(self, parent):
        frame = tk.Frame(parent, bg=Theme.BACKGROUND)
        frame.pack(pady=5)  # Reducido de 10 a 5

        # Back Button (Blue theme)
        self.create_styled_button(
            frame,
            text="⬅ Volver",
            command=lambda: self.navigator.show_view('launcher'),
            bg_color=Theme.TOTAL_FG,
            hover_color='#0d47a1'
        )

        # Generate Button (Green theme - primary action)
        self.create_styled_button(
            frame,
            text="Generar Etiquetas",
            command=self.generate,
            bg_color='#27ae60',
            hover_color='#1e8449'
        )

        # Clear Button (Gray theme)
        self.create_styled_button(
            frame,
            text="Limpiar",
            command=self.clear_form,
            bg_color='#6c757d',
            hover_color='#5a6268'
        )

    def create_styled_button(self, parent, text, command, bg_color, hover_color):
        """Creates a button with hover animation"""
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=Theme.FONTS['button'],
            bg=bg_color,
            fg='white',
            padx=20,
            pady=10,
            relief='flat',
            bd=0,
            cursor='hand2',
            activebackground=hover_color,
            activeforeground='white'
        )
        btn.pack(side='left', padx=10)

        # Hover effect
        def on_enter(e):
            btn.configure(bg=hover_color)

        def on_leave(e):
            btn.configure(bg=bg_color)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    def validate_price(self, event, index):
        value = self.price_entries[index].get()
        if value and not re.match(r'^\d*\.?\d*$', value):
            self.price_entries[index].delete(len(value)-1)

    def get_products_data(self):
        products = []
        for i in range(14):
            name = self.product_entries[i].get().strip()
            price = self.price_entries[i].get().strip()
            
            if name and price:
                try:
                    price_float = float(price)
                    if price_float > 0:
                        products.append({'name': name, 'price': price_float})
                except ValueError: pass
        return products

    def generate(self):
        products = self.get_products_data()
        if not products:
            messagebox.showwarning("Sin Productos", "Ingresa al menos un producto válido.")
            return
            
        success, result = self.model.print_tags(products)
        if success:
            self.after(300000, lambda: self.model.cleanup_temp_file(result))
        else:
            messagebox.showerror("Error", result)

    def clear_form(self):
        if messagebox.askyesno("Confirmar", "¿Limpiar todo?"):
            for e in self.product_entries: e.delete(0, tk.END)
            for e in self.price_entries: e.delete(0, tk.END)

    def open_barcode_scanner(self, row_index):
        """
        Abre la ventana de escáner de código de barras para una fila específica.

        Args:
            row_index (int): Índice de la fila (0-13)
        """
        show_barcode_scanner(self, row_index, self.on_product_selected)

    def on_product_selected(self, row_index, product_name, product_price):
        """
        Callback ejecutado cuando se selecciona un producto desde el escáner.

        Args:
            row_index (int): Índice de la fila
            product_name (str): Nombre del producto
            product_price (float): Precio del producto
        """
        # Limpiar los campos
        self.product_entries[row_index].delete(0, tk.END)
        self.price_entries[row_index].delete(0, tk.END)

        # Insertar los nuevos valores
        self.product_entries[row_index].insert(0, product_name)
        self.price_entries[row_index].insert(0, str(int(product_price)))

        # Animación visual de confirmación
        self.product_entries[row_index].config(highlightbackground='#27ae60', highlightthickness=2)
        self.price_entries[row_index].config(highlightbackground='#27ae60', highlightthickness=2)

        # Volver al color normal después de 800ms
        self.after(800, lambda: self.product_entries[row_index].config(highlightbackground='#e5e7eb', highlightthickness=1))
        self.after(800, lambda: self.price_entries[row_index].config(highlightbackground='#e5e7eb', highlightthickness=1))
