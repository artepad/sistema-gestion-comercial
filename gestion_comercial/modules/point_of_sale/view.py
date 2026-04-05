"""
Vista del Punto de Venta.
Incluye dos pestañas:
- Punto de Venta: sistema POS básico de respaldo
- Consulta de Precios: consultar precios mediante escáner de código de barras
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import winsound
import threading
import shutil
from datetime import datetime
from gestion_comercial.config.theme import Theme
from gestion_comercial.config.settings import Settings
from gestion_comercial.modules.tag_manager.database import ProductDatabase
from gestion_comercial.modules.point_of_sale.model import PointOfSaleModel


class PointOfSaleView(tk.Frame):
    def __init__(self, parent, navigator):
        super().__init__(parent, bg=Theme.BACKGROUND)
        self.navigator = navigator
        self.model = PointOfSaleModel()
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
        """Crea la interfaz en modo normal con pestañas."""
        # Top green accent strip
        self.create_top_accent()

        # Header
        self.create_header()

        # Container principal
        main_container = tk.Frame(self, bg=Theme.BACKGROUND, padx=40, pady=10)
        main_container.pack(fill='both', expand=True)

        # Crear sistema de pestañas
        self.create_notebook(main_container)

        # Bottom blue accent strip
        self.create_bottom_accent()

    # ─────────────────────────────────────────────────────────
    #  Estructura común (header, accents, notebook)
    # ─────────────────────────────────────────────────────────

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
            text="Punto de Venta",
            font=(Theme.FONT_FAMILY, 20, 'bold'),
            bg=Theme.TEXT_PRIMARY,
            fg='white'
        ).pack()

    def create_notebook(self, parent):
        """Crea el sistema de pestañas."""
        style = ttk.Style()
        style.theme_use('default')

        style.configure(
            'POS.TNotebook',
            background=Theme.BACKGROUND,
            borderwidth=0,
            tabmargins=[0, 0, 0, 0]
        )
        style.configure(
            'POS.TNotebook.Tab',
            background='#e5e7eb',
            foreground=Theme.TEXT_PRIMARY,
            padding=[12, 3],
            font=(Theme.FONT_FAMILY, 9, 'bold')
        )
        style.map(
            'POS.TNotebook.Tab',
            background=[('selected', '#3498db'), ('active', '#5dade2')],
            foreground=[('selected', 'white'), ('active', 'white')]
        )

        self.notebook = ttk.Notebook(parent, style='POS.TNotebook')
        self.notebook.pack(fill='both', expand=True)

        # Pestaña 1: Punto de Venta (principal)
        self.pos_tab = tk.Frame(self.notebook, bg=Theme.BACKGROUND)
        self.notebook.add(self.pos_tab, text='Punto de Venta')

        # Pestaña 2: Consulta de Precios
        self.lookup_tab = tk.Frame(self.notebook, bg=Theme.BACKGROUND)
        self.notebook.add(self.lookup_tab, text='Consulta de Precios')

        # Crear contenido de cada pestaña
        self.create_pos_content(self.pos_tab)
        self.create_price_lookup_content(self.lookup_tab)

    # ─────────────────────────────────────────────────────────
    #  PESTAÑA 1: Punto de Venta (POS)
    # ─────────────────────────────────────────────────────────

    def create_pos_content(self, parent):
        """Crea el contenido de la pestaña Punto de Venta."""
        main_container = tk.Frame(parent, bg=Theme.BACKGROUND)
        main_container.pack(fill='both', expand=True)

        # Botones al fondo (empaquetados primero con side='bottom')
        self._create_pos_buttons(main_container)

        # Contenido principal
        content_area = tk.Frame(main_container, bg=Theme.BACKGROUND)
        content_area.pack(fill='both', expand=True)

        # Sección de escaneo
        scan_section = tk.LabelFrame(
            content_area,
            text="  Escanear Producto  ",
            font=(Theme.FONT_FAMILY, 11, 'bold'),
            bg=Theme.BACKGROUND,
            fg=Theme.TEXT_PRIMARY,
            bd=1,
            relief='solid',
            padx=15,
            pady=10
        )
        scan_section.pack(fill='x', pady=(10, 8))

        scan_row = tk.Frame(scan_section, bg=Theme.BACKGROUND)
        scan_row.pack(fill='x', pady=5)

        # Entry de código de barras
        self.pos_barcode_entry = tk.Entry(
            scan_row,
            font=(Theme.FONT_FAMILY, 13),
            bg='white',
            fg=Theme.TEXT_PRIMARY,
            bd=0,
            relief='flat',
            highlightthickness=2,
            highlightcolor='#2ecc71',
            highlightbackground='#dde1e6'
        )
        self.pos_barcode_entry.pack(side='left', fill='x', expand=True, ipady=8, padx=(0, 10))
        self.pos_barcode_entry.bind('<Return>', self.pos_scan_product)
        self.pos_barcode_entry.focus_set()

        # Botón agregar manual
        manual_btn = tk.Button(
            scan_row,
            text="+ Manual",
            font=(Theme.FONT_FAMILY, 11, 'bold'),
            bg='#3498db',
            fg='white',
            bd=0,
            relief='flat',
            padx=20,
            pady=9,
            cursor='hand2',
            activebackground='#2980b9',
            activeforeground='white',
            command=self.show_manual_entry
        )
        manual_btn.pack(side='right')

        def on_manual_enter(e):
            manual_btn.configure(bg='#2980b9')

        def on_manual_leave(e):
            manual_btn.configure(bg='#3498db')

        manual_btn.bind("<Enter>", on_manual_enter)
        manual_btn.bind("<Leave>", on_manual_leave)

        # Sección de detalle de venta
        detail_section = tk.LabelFrame(
            content_area,
            text="  Detalle de Venta  ",
            font=(Theme.FONT_FAMILY, 11, 'bold'),
            bg=Theme.BACKGROUND,
            fg=Theme.TEXT_PRIMARY,
            bd=1,
            relief='solid',
            padx=10,
            pady=10
        )
        detail_section.pack(fill='both', expand=True, pady=(0, 8))

        # Treeview para la tabla de productos
        tree_frame = tk.Frame(detail_section, bg=Theme.BACKGROUND)
        tree_frame.pack(fill='both', expand=True)

        # Estilo del Treeview
        tree_style = ttk.Style()
        tree_style.configure(
            'POS.Treeview',
            font=(Theme.FONT_FAMILY, 10, 'bold'),
            rowheight=30,
            background='white',
            fieldbackground='white',
            foreground=Theme.TEXT_PRIMARY
        )
        tree_style.configure(
            'POS.Treeview.Heading',
            font=(Theme.FONT_FAMILY, 10, 'bold'),
            background=Theme.TEXT_PRIMARY,
            foreground='white',
            relief='flat',
            padding=6
        )
        tree_style.map(
            'POS.Treeview.Heading',
            background=[('active', '#34495e')]
        )
        tree_style.map(
            'POS.Treeview',
            background=[('selected', '#d4e6f1')],
            foreground=[('selected', Theme.TEXT_PRIMARY)]
        )

        columns = ('code', 'product', 'qty', 'unit_price', 'subtotal')
        self.cart_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            style='POS.Treeview',
            selectmode='browse'
        )

        self.cart_tree.heading('code', text='Código')
        self.cart_tree.heading('product', text='Producto')
        self.cart_tree.heading('qty', text='Cant.')
        self.cart_tree.heading('unit_price', text='P. Unitario')
        self.cart_tree.heading('subtotal', text='Subtotal')

        self.cart_tree.column('code', width=100, minwidth=80)
        self.cart_tree.column('product', width=250, minwidth=150)
        self.cart_tree.column('qty', width=55, minwidth=45, anchor='center')
        self.cart_tree.column('unit_price', width=95, minwidth=75, anchor='e')
        self.cart_tree.column('subtotal', width=95, minwidth=75, anchor='e')

        # Tags para filas alternadas (zebra)
        self.cart_tree.tag_configure('even', background='#f8f9fa')
        self.cart_tree.tag_configure('odd', background='white')

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.cart_tree.yview)
        self.cart_tree.configure(yscrollcommand=scrollbar.set)

        self.cart_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Doble click para editar cantidad
        self.cart_tree.bind('<Double-1>', self.edit_quantity)

        # Sección de total
        total_frame = tk.Frame(content_area, bg=Theme.TEXT_PRIMARY)
        total_frame.pack(fill='x', pady=(0, 0))

        self.total_label = tk.Label(
            total_frame,
            text="TOTAL: $0",
            font=(Theme.FONT_FAMILY, 24, 'bold'),
            bg=Theme.TEXT_PRIMARY,
            fg='white',
            pady=14
        )
        self.total_label.pack()

    def _create_pos_buttons(self, parent):
        """Crea los botones del POS al fondo, con el mismo estilo que Tag Manager."""
        frame = tk.Frame(parent, bg=Theme.BACKGROUND)
        frame.pack(side='bottom', fill='x', pady=(8, 5))

        btn_container = tk.Frame(frame, bg=Theme.BACKGROUND)
        btn_container.pack()

        self._create_styled_button(
            btn_container,
            text="⬅ Volver",
            command=lambda: self.navigator.show_view('launcher'),
            bg_color=Theme.TOTAL_FG,
            hover_color='#0d47a1'
        )
        self._create_styled_button(
            btn_container,
            text="Eliminar Producto",
            command=self.remove_selected_product,
            bg_color='#e74c3c',
            hover_color='#c0392b'
        )
        self._create_styled_button(
            btn_container,
            text="Nueva Venta",
            command=self.new_sale,
            bg_color='#27ae60',
            hover_color='#1e8449'
        )

    def _create_styled_button(self, parent, text, command, bg_color, hover_color):
        """Crea un botón con el mismo estilo que Tag Manager."""
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

        def on_enter(e):
            btn.configure(bg=hover_color)

        def on_leave(e):
            btn.configure(bg=bg_color)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    # ─── POS: Lógica ────────────────────────────────────────

    def _play_beep(self, success):
        """Reproduce un beep en un hilo separado para no bloquear la UI."""
        def beep():
            if success:
                winsound.Beep(1800, 80)
            else:
                winsound.Beep(400, 200)
        threading.Thread(target=beep, daemon=True).start()

    def pos_scan_product(self, event=None):
        """Escanea un producto y lo agrega al carrito."""
        barcode = self.pos_barcode_entry.get().strip()
        if not barcode:
            return

        success, result = ProductDatabase.search_product(barcode)

        if success:
            self._play_beep(True)
            self.model.add_item(barcode, result['name'], result['price'])
            self.refresh_cart_display()
        else:
            self._play_beep(False)
            messagebox.showwarning(
                "Producto no encontrado",
                f"No se encontró el código: {barcode}",
                parent=self
            )

        self.pos_barcode_entry.delete(0, tk.END)
        self.pos_barcode_entry.focus_set()

    def show_manual_entry(self):
        """Muestra popup para ingresar producto manualmente."""
        popup = tk.Toplevel(self)
        popup.title("Agregar Producto Manual")
        popup.configure(bg=Theme.BACKGROUND)
        popup.resizable(False, False)

        window_width = 420
        window_height = 320
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
        header_frame = tk.Frame(popup, bg=Theme.TEXT_PRIMARY, height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        tk.Frame(header_frame, bg='#3498db', height=4).pack(fill='x')
        tk.Label(
            header_frame,
            text="Agregar Producto Manual",
            font=(Theme.FONT_FAMILY, 14, 'bold'),
            bg=Theme.TEXT_PRIMARY,
            fg='white'
        ).pack(expand=True)

        # Contenido
        content = tk.Frame(popup, bg=Theme.BACKGROUND)
        content.pack(fill='both', expand=True, padx=30, pady=20)

        # Nombre
        tk.Label(
            content, text="Nombre del producto:",
            font=(Theme.FONT_FAMILY, 10, 'bold'),
            bg=Theme.BACKGROUND, fg=Theme.TEXT_PRIMARY
        ).pack(anchor='w', pady=(0, 3))

        name_entry = tk.Entry(
            content, font=(Theme.FONT_FAMILY, 11),
            bg='white', fg=Theme.TEXT_PRIMARY, bd=0,
            highlightthickness=2, highlightcolor='#3498db',
            highlightbackground='#dde1e6'
        )
        name_entry.pack(fill='x', ipady=6, pady=(0, 12))
        name_entry.focus_set()

        # Cantidad y Precio en la misma fila
        row_frame = tk.Frame(content, bg=Theme.BACKGROUND)
        row_frame.pack(fill='x', pady=(0, 15))

        # Cantidad
        qty_frame = tk.Frame(row_frame, bg=Theme.BACKGROUND)
        qty_frame.pack(side='left', fill='x', expand=True, padx=(0, 10))

        tk.Label(
            qty_frame, text="Cantidad:",
            font=(Theme.FONT_FAMILY, 10, 'bold'),
            bg=Theme.BACKGROUND, fg=Theme.TEXT_PRIMARY
        ).pack(anchor='w', pady=(0, 3))

        qty_entry = tk.Entry(
            qty_frame, font=(Theme.FONT_FAMILY, 11),
            bg='white', fg=Theme.TEXT_PRIMARY, bd=0,
            highlightthickness=2, highlightcolor='#3498db',
            highlightbackground='#dde1e6'
        )
        qty_entry.pack(fill='x', ipady=6)
        qty_entry.insert(0, "1")

        # Precio unitario
        price_frame = tk.Frame(row_frame, bg=Theme.BACKGROUND)
        price_frame.pack(side='left', fill='x', expand=True)

        tk.Label(
            price_frame, text="Precio unitario:",
            font=(Theme.FONT_FAMILY, 10, 'bold'),
            bg=Theme.BACKGROUND, fg=Theme.TEXT_PRIMARY
        ).pack(anchor='w', pady=(0, 3))

        price_entry = tk.Entry(
            price_frame, font=(Theme.FONT_FAMILY, 11),
            bg='white', fg=Theme.TEXT_PRIMARY, bd=0,
            highlightthickness=2, highlightcolor='#3498db',
            highlightbackground='#dde1e6'
        )
        price_entry.pack(fill='x', ipady=6)

        def confirm():
            name = name_entry.get().strip()
            qty_text = qty_entry.get().strip()
            price_text = price_entry.get().strip()

            if not name:
                messagebox.showwarning("Campo vacío", "Ingrese el nombre del producto.", parent=popup)
                return

            try:
                qty = int(qty_text)
                if qty <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showwarning("Cantidad inválida", "Ingrese una cantidad entera mayor a 0.", parent=popup)
                return

            try:
                price = float(price_text.replace(',', '.'))
                if price <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showwarning("Precio inválido", "Ingrese un precio válido mayor a 0.", parent=popup)
                return

            self.model.add_item("MANUAL", name, price, qty)
            self.refresh_cart_display()
            popup.destroy()
            self.pos_barcode_entry.focus_set()

        # Botones centrados
        btn_frame = tk.Frame(popup, bg=Theme.BACKGROUND)
        btn_frame.pack(pady=(0, 20))

        confirm_btn = tk.Button(
            btn_frame, text="Agregar",
            font=Theme.FONTS['button'],
            bg='#27ae60', fg='white', bd=0,
            relief='flat', padx=20, pady=10, cursor='hand2',
            activebackground='#1e8449', activeforeground='white',
            command=confirm
        )
        confirm_btn.pack(side='left', padx=10)

        def on_confirm_enter(e):
            confirm_btn.configure(bg='#1e8449')

        def on_confirm_leave(e):
            confirm_btn.configure(bg='#27ae60')

        confirm_btn.bind("<Enter>", on_confirm_enter)
        confirm_btn.bind("<Leave>", on_confirm_leave)

        cancel_btn = tk.Button(
            btn_frame, text="Cancelar",
            font=Theme.FONTS['button'],
            bg='#6c757d', fg='white', bd=0,
            relief='flat', padx=20, pady=10, cursor='hand2',
            activebackground='#5a6268', activeforeground='white',
            command=popup.destroy
        )
        cancel_btn.pack(side='left', padx=10)

        def on_cancel_enter(e):
            cancel_btn.configure(bg='#5a6268')

        def on_cancel_leave(e):
            cancel_btn.configure(bg='#6c757d')

        cancel_btn.bind("<Enter>", on_cancel_enter)
        cancel_btn.bind("<Leave>", on_cancel_leave)

        # Enter para confirmar
        popup.bind('<Return>', lambda e: confirm())

    def refresh_cart_display(self):
        """Actualiza la tabla y el total."""
        # Limpiar tabla
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)

        # Llenar con items del modelo (filas zebra)
        for i, item in enumerate(self.model.get_cart_items()):
            subtotal = item['price'] * item['qty']
            tag = 'even' if i % 2 == 0 else 'odd'
            self.cart_tree.insert('', 'end', values=(
                item['code'],
                item['name'],
                item['qty'],
                f"${self.format_price(item['price'])}",
                f"${self.format_price(subtotal)}"
            ), tags=(tag,))

        # Actualizar total
        total = self.model.get_total()
        self.total_label.configure(text=f"TOTAL: ${self.format_price(total)}")

    def remove_selected_product(self):
        """Elimina el producto seleccionado del carrito."""
        selected = self.cart_tree.selection()
        if not selected:
            messagebox.showinfo(
                "Seleccionar producto",
                "Seleccione un producto de la lista para eliminar.",
                parent=self
            )
            return

        # Obtener índice del item seleccionado
        index = self.cart_tree.index(selected[0])
        self.model.remove_item(index)
        self.refresh_cart_display()
        self.pos_barcode_entry.focus_set()

    def edit_quantity(self, event):
        """Permite editar la cantidad al hacer doble click."""
        selected = self.cart_tree.selection()
        if not selected:
            return

        # Verificar que se hizo click en la columna de cantidad
        column = self.cart_tree.identify_column(event.x)
        if column != '#3':  # Columna de cantidad
            return

        index = self.cart_tree.index(selected[0])
        item = self.model.get_cart_items()[index]

        popup = tk.Toplevel(self)
        popup.title("Modificar Cantidad")
        popup.configure(bg=Theme.BACKGROUND)
        popup.resizable(False, False)

        window_width = 300
        window_height = 150
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

        content = tk.Frame(popup, bg=Theme.BACKGROUND)
        content.pack(fill='both', expand=True, padx=20, pady=15)

        tk.Label(
            content,
            text=f"Cantidad para: {item['name'][:30]}",
            font=(Theme.FONT_FAMILY, 10, 'bold'),
            bg=Theme.BACKGROUND, fg=Theme.TEXT_PRIMARY
        ).pack(anchor='w', pady=(0, 8))

        qty_entry = tk.Entry(
            content, font=(Theme.FONT_FAMILY, 13),
            bg='white', fg=Theme.TEXT_PRIMARY, bd=0,
            highlightthickness=2, highlightcolor='#3498db',
            highlightbackground='#dde1e6', justify='center'
        )
        qty_entry.pack(fill='x', ipady=6)
        qty_entry.insert(0, str(item['qty']))
        qty_entry.select_range(0, tk.END)
        qty_entry.focus_set()

        def close_popup():
            popup.destroy()
            self.pos_barcode_entry.focus_set()

        popup.protocol("WM_DELETE_WINDOW", close_popup)

        def confirm():
            try:
                new_qty = int(qty_entry.get().strip())
                if new_qty <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showwarning("Cantidad inválida", "Ingrese un número entero mayor a 0.", parent=popup)
                return
            self.model.update_quantity(index, new_qty)
            self.refresh_cart_display()
            close_popup()

        btn_frame = tk.Frame(content, bg=Theme.BACKGROUND)
        btn_frame.pack(fill='x', pady=(10, 0))

        ok_btn = tk.Button(
            btn_frame, text="Aceptar",
            font=(Theme.FONT_FAMILY, 10, 'bold'),
            bg='#3498db', fg='white', bd=0,
            padx=20, pady=6, cursor='hand2',
            command=confirm
        )
        ok_btn.pack(side='left', padx=(0, 8))

        cancel_btn = tk.Button(
            btn_frame, text="Cancelar",
            font=(Theme.FONT_FAMILY, 10, 'bold'),
            bg='#95a5a6', fg='white', bd=0,
            padx=20, pady=6, cursor='hand2',
            command=close_popup
        )
        cancel_btn.pack(side='left')

        popup.bind('<Return>', lambda e: confirm())

    def new_sale(self):
        """Limpia el carrito para una nueva venta."""
        if self.model.get_cart_items():
            confirm = messagebox.askyesno(
                "Nueva Venta",
                "¿Desea limpiar la venta actual y comenzar una nueva?",
                parent=self
            )
            if not confirm:
                return

        self.model.clear_cart()
        self.refresh_cart_display()
        self.pos_barcode_entry.focus_set()

    # ─────────────────────────────────────────────────────────
    #  PESTAÑA 2: Consulta de Precios
    # ─────────────────────────────────────────────────────────

    def create_price_lookup_content(self, parent):
        """Crea el contenido de la pestaña Consulta de Precios."""
        content = tk.Frame(parent, bg=Theme.BACKGROUND)
        content.pack(fill='both', expand=True, pady=10)

        # Instrucciones
        tk.Label(
            content,
            text="Escanea el código de barras del producto para consultar su precio",
            font=(Theme.FONT_FAMILY, 12),
            bg=Theme.BACKGROUND,
            fg='#6c757d'
        ).pack(pady=(0, 20))

        # Campo de entrada
        input_frame = tk.Frame(content, bg=Theme.BACKGROUND)
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

        # Área de resultados
        self.result_frame = tk.LabelFrame(
            content,
            text="📊 Información del Producto",
            font=(Theme.FONT_FAMILY, 11, 'bold'),
            bg='#f8f9fa',
            fg='#495057',
            padx=25,
            pady=15
        )
        self.result_frame.pack(fill='both', expand=True, pady=(0, 15))

        self.result_content = tk.Frame(self.result_frame, bg='#f8f9fa')
        self.result_content.pack(fill='both', expand=True)

        self.show_initial_message()

        # Información de base de datos
        self.create_db_info_section(content)

        # Botones inferiores
        self.create_lookup_buttons(content)

    def create_lookup_buttons(self, parent):
        """Crea los botones de la pestaña de consulta."""
        button_container = tk.Frame(parent, bg=Theme.BACKGROUND)
        button_container.pack(fill='x', pady=(15, 0))

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

        db_info = ProductDatabase.get_database_info()

        if db_info['exists']:
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

            delete_link = tk.Label(
                status_container,
                text="🗑 Eliminar base de datos",
                font=(Theme.FONT_FAMILY, 9),
                bg='white',
                fg='#6c757d',
                cursor='hand2'
            )
            delete_link.pack(side='left', padx=(20, 0))

            def on_delete_enter(e):
                delete_link.config(fg='#dc3545', font=(Theme.FONT_FAMILY, 9, 'underline'))

            def on_delete_leave(e):
                delete_link.config(fg='#6c757d', font=(Theme.FONT_FAMILY, 9))

            delete_link.bind('<Enter>', on_delete_enter)
            delete_link.bind('<Leave>', on_delete_leave)
            delete_link.bind('<Button-1>', lambda e: self.delete_database())

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

            days_old = self.get_database_age_days()
            if days_old is not None:
                if days_old >= 30:
                    tk.Label(
                        update_container,
                        text="⚠ La base de datos lleva un mes desactualizada",
                        font=(Theme.FONT_FAMILY, 9, 'bold'),
                        bg='white',
                        fg='#dc3545'
                    ).pack(side='left', padx=(15, 0))
                elif days_old >= 15:
                    tk.Label(
                        update_container,
                        text="⚠ La BD tiene más de una semana desactualizada",
                        font=(Theme.FONT_FAMILY, 9, 'bold'),
                        bg='white',
                        fg='#f39c12'
                    ).pack(side='left', padx=(15, 0))

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

            tk.Label(
                info_frame,
                text="No se encontró ningún archivo de base de datos en la carpeta.",
                font=(Theme.FONT_FAMILY, 9),
                bg='white',
                fg='#6c757d',
                wraplength=600,
                justify='left'
            ).pack(fill='x', pady=(0, 10))

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

    # ─────────────────────────────────────────────────────────
    #  Consulta de precios: lógica
    # ─────────────────────────────────────────────────────────

    def show_initial_message(self):
        """Muestra el mensaje inicial en el área de resultados."""
        for widget in self.result_content.winfo_children():
            widget.destroy()

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
            if self.typing_timer:
                self.after_cancel(self.typing_timer)

            self.instruction_label.pack_forget()
            self.scanner_icon.pack_forget()
            self.error_label.pack_forget()
            self.barcode_entry.pack_forget()
            self.typing_label.pack_forget()

            self.product_name_label.config(text=product_data['name'])
            self.product_name_label.pack(pady=(0, 20))

            price_text = f"${self.format_price(product_data['price'])}"
            self.product_price_label.config(text=price_text)
            self.product_price_label.pack(pady=10)

            self.schedule_auto_clear()
        else:
            for widget in self.result_content.winfo_children():
                widget.destroy()

            tk.Label(
                self.result_content,
                text="✓ Producto Encontrado",
                font=(Theme.FONT_FAMILY, 12, 'bold'),
                bg='#f8f9fa',
                fg='#28a745'
            ).pack(pady=(8, 15))

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

    def show_error_message(self, error_msg):
        """Muestra un mensaje de error."""
        if self.fullscreen_mode:
            if self.typing_timer:
                self.after_cancel(self.typing_timer)

            self.instruction_label.pack_forget()
            self.scanner_icon.pack_forget()
            self.product_name_label.pack_forget()
            self.product_price_label.pack_forget()
            self.barcode_entry.pack_forget()
            self.typing_label.pack_forget()

            self.error_label.config(text=f"✗ {error_msg}")
            self.error_label.pack(pady=20)

            self.schedule_auto_clear()
        else:
            for widget in self.result_content.winfo_children():
                widget.destroy()

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

        success, result = ProductDatabase.search_product(barcode)

        if success:
            self.show_product_info(result)
        else:
            self.show_error_message(result)

        self.barcode_entry.delete(0, tk.END)
        self.barcode_entry.focus_set()

    # ─────────────────────────────────────────────────────────
    #  Modo pantalla completa
    # ─────────────────────────────────────────────────────────

    def create_fullscreen_ui(self):
        """Crea la interfaz en modo pantalla completa."""
        root = self.winfo_toplevel()
        root.attributes('-fullscreen', True)

        main_container = tk.Frame(self, bg='white')
        main_container.pack(fill='both', expand=True)

        center_frame = tk.Frame(main_container, bg='white')
        center_frame.place(relx=0.5, rely=0.5, anchor='center')

        self.instruction_label = tk.Label(
            center_frame,
            text="Escanea el código de barras del producto",
            font=(Theme.FONT_FAMILY, 28, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        self.instruction_label.pack(pady=(0, 50))

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

        self.typing_label = tk.Label(
            center_frame,
            text="",
            font=(Theme.FONT_FAMILY, 18),
            bg='white',
            fg='#7f8c8d'
        )
        self.typing_label.pack(pady=(20, 0))

        self.start_typing_effect()

        self.scanner_icon = tk.Label(
            center_frame,
            text="📊",
            font=(Theme.FONT_FAMILY, 70),
            bg='white'
        )
        self.scanner_icon.pack(pady=(40, 20))

        self.product_name_label = tk.Label(
            center_frame,
            text="",
            font=(Theme.FONT_FAMILY, 32, 'bold'),
            bg='white',
            fg='#2c3e50',
            wraplength=900
        )

        self.product_price_label = tk.Label(
            center_frame,
            text="",
            font=(Theme.FONT_FAMILY, 120, 'bold'),
            bg='white',
            fg='#27ae60'
        )

        self.error_label = tk.Label(
            center_frame,
            text="",
            font=(Theme.FONT_FAMILY, 28, 'bold'),
            bg='white',
            fg='#e74c3c',
            wraplength=800
        )

        mode_label = tk.Label(
            main_container,
            text="Modo pantalla completa (salir con Escape)",
            font=(Theme.FONT_FAMILY, 10),
            bg='white',
            fg='#95a5a6'
        )
        mode_label.place(relx=1.0, rely=0.0, anchor='ne', x=-20, y=20)

    def schedule_auto_clear(self):
        """Programa la limpieza automática de la pantalla."""
        if self.auto_clear_timer:
            self.after_cancel(self.auto_clear_timer)
        self.auto_clear_timer = self.after(5000, self.clear_fullscreen_display)

    def clear_fullscreen_display(self):
        """Limpia la pantalla en modo fullscreen."""
        if self.fullscreen_mode:
            self.product_name_label.pack_forget()
            self.product_price_label.pack_forget()
            self.error_label.pack_forget()

            self.instruction_label.pack(pady=(0, 50))
            self.barcode_entry.pack(ipady=15)
            self.typing_label.pack(pady=(20, 0))
            self.scanner_icon.pack(pady=(40, 20))

            self.start_typing_effect()
            self.barcode_entry.focus_set()

    def start_typing_effect(self, text=None):
        """Inicia el efecto de tipeo animado con ciclo de mensajes."""
        if not self.fullscreen_mode:
            return

        if self.typing_timer:
            self.after_cancel(self.typing_timer)

        if text is None:
            self.typing_text = self.typing_messages[self.current_message_index]
        else:
            self.typing_text = text

        self.typing_index = 0

        if hasattr(self, 'typing_label') and self.typing_label.winfo_exists():
            try:
                self.typing_label.config(text="")
            except:
                return

        self.type_next_character()

    def type_next_character(self):
        """Escribe el siguiente carácter del texto con efecto de tipeo."""
        if not self.fullscreen_mode:
            return

        if not hasattr(self, 'typing_label') or not self.typing_label.winfo_exists():
            return

        if self.typing_index < len(self.typing_text):
            current_text = self.typing_text[:self.typing_index + 1]
            try:
                self.typing_label.config(text=current_text)
            except:
                return

            self.typing_index += 1
            self.typing_timer = self.after(80, self.type_next_character)
        else:
            self.typing_timer = self.after(2000, self.start_erasing)

    def start_erasing(self):
        """Inicia el efecto de borrado del texto."""
        if not self.fullscreen_mode:
            return

        if hasattr(self, 'typing_label') and self.typing_label.winfo_exists():
            self.erase_next_character()

    def erase_next_character(self):
        """Borra el texto carácter por carácter."""
        if not self.fullscreen_mode:
            return

        if not hasattr(self, 'typing_label') or not self.typing_label.winfo_exists():
            return

        try:
            current_text = self.typing_label.cget('text')

            if len(current_text) > 0:
                self.typing_label.config(text=current_text[:-1])
                self.typing_timer = self.after(50, self.erase_next_character)
            else:
                self.advance_to_next_message()
        except:
            return

    def advance_to_next_message(self):
        """Avanza al siguiente mensaje en el ciclo y lo muestra."""
        if not self.fullscreen_mode:
            return

        self.current_message_index = (self.current_message_index + 1) % len(self.typing_messages)
        self.typing_timer = self.after(500, self.start_typing_effect)

    def enter_fullscreen(self, event=None):
        """Activa el modo pantalla completa."""
        if not self.fullscreen_mode:
            self.fullscreen_mode = True

            for widget in self.winfo_children():
                widget.destroy()

            self.setup_ui()

    def toggle_fullscreen(self, event=None):
        """Alterna entre modo normal y pantalla completa."""
        self.fullscreen_mode = not self.fullscreen_mode

        for widget in self.winfo_children():
            widget.destroy()

        self.setup_ui()

    def exit_fullscreen(self, event=None):
        """Sale del modo pantalla completa."""
        if self.fullscreen_mode:
            if self.typing_timer:
                self.after_cancel(self.typing_timer)
                self.typing_timer = None

            if self.auto_clear_timer:
                self.after_cancel(self.auto_clear_timer)
                self.auto_clear_timer = None

            self.fullscreen_mode = False

            root = self.winfo_toplevel()
            root.attributes('-fullscreen', False)

            for widget in self.winfo_children():
                widget.destroy()

            self.setup_ui()

    # ─────────────────────────────────────────────────────────
    #  Utilidades
    # ─────────────────────────────────────────────────────────

    def format_price(self, price):
        """Formatea el precio con separadores de miles."""
        return f"{int(price):,}".replace(',', '.')

    def get_database_age_days(self):
        """Calcula cuántos días han pasado desde la última actualización de la BD."""
        db_info = ProductDatabase.get_database_info()
        if not db_info['exists']:
            return None

        try:
            date_str = db_info['last_modified']
            if date_str == "Archivo no encontrado":
                return None

            last_update = datetime.strptime(date_str, "%d/%m/%Y %H:%M")
            today = datetime.now()
            delta = today - last_update
            return delta.days
        except Exception:
            return None

    def search_database_file(self):
        """Permite al usuario buscar y cargar un archivo de base de datos."""
        file_path = filedialog.askopenfilename(
            title="Seleccionar Archivo de Base de Datos",
            filetypes=[("Archivos Excel", "*.xlsx"), ("Todos los archivos", "*.*")],
            parent=self
        )

        if file_path:
            try:
                if not os.path.exists(ProductDatabase.DB_FOLDER):
                    os.makedirs(ProductDatabase.DB_FOLDER)

                filename = os.path.basename(file_path)
                destination = os.path.join(ProductDatabase.DB_FOLDER, filename)

                shutil.copy2(file_path, destination)

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
        """Elimina la base de datos actual después de confirmar."""
        confirm = messagebox.askyesno(
            "Confirmar Eliminación",
            "¿Estás seguro de que deseas eliminar la base de datos?\n\n"
            "Esta acción no se puede deshacer.",
            parent=self,
            icon='warning'
        )

        if confirm:
            try:
                db_info = ProductDatabase.get_database_info()

                if db_info['exists'] and db_info['path']:
                    if os.path.exists(db_info['path']):
                        os.remove(db_info['path'])

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
        for widget in self.winfo_children():
            widget.destroy()

        self.setup_ui()
