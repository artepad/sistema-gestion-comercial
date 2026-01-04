import tkinter as tk
from tkinter import messagebox
import re
from gestion_comercial.config.theme import Theme
from gestion_comercial.modules.tag_manager.model import TagManagerModel
from gestion_comercial.modules.tag_manager.barcode_scanner import show_barcode_scanner

class TagManagerView(tk.Frame):
    def __init__(self, parent, navigator):
        super().__init__(parent, bg=Theme.BACKGROUND)
        self.navigator = navigator
        self.model = TagManagerModel()
        
        self.product_entries = []
        self.price_entries = []
        
        self.setup_ui()
        
    def setup_ui(self):
        # Top green accent strip
        self.create_top_accent()

        self.create_header()

        main_container = tk.Frame(self, bg=Theme.BACKGROUND, padx=40, pady=10)
        main_container.pack(fill='both', expand=True)

        self.create_product_form(main_container)
        self.create_button_panel(main_container)

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

    def create_product_form(self, parent):
        form_frame = tk.Frame(parent, bg='white', relief='flat', bd=0)
        form_frame.pack(fill='both', expand=True, pady=(0, 10))

        # Headers
        header_frame = tk.Frame(form_frame, bg=Theme.BACKGROUND, height=30)
        header_frame.pack(fill='x')

        # Header Row
        tk.Label(header_frame, text="Nombre del producto", font=Theme.FONTS['body'], bg=Theme.BACKGROUND, fg='#6b7280').pack(side='left', padx=(200, 0))
        tk.Label(header_frame, text="Precio", font=Theme.FONTS['body'], bg=Theme.BACKGROUND, fg='#6b7280').pack(side='right', padx=(0, 105))
        
        # Rows (1 to 14 in a single column)
        for row in range(14):
            self.create_product_row(form_frame, row)

    def create_product_row(self, parent, row_index):
        bg_color = 'white' if row_index % 2 == 0 else '#f8fafc'
        row_frame = tk.Frame(parent, bg=bg_color, pady=3)
        row_frame.pack(fill='x')

        self.create_product_field(row_frame, row_index, bg_color)

    def create_product_field(self, parent, index, bg_color):
        tk.Label(parent, text=f"{index+1:02d}", font=Theme.FONTS['body'], bg=bg_color, fg='#6b7280', width=3).pack(side='left', padx=(20, 0))

        p_entry = tk.Entry(parent, font=Theme.FONTS['body'], bg='white', relief='flat', bd=1, highlightthickness=1, highlightbackground='#e5e7eb')
        p_entry.pack(side='left', padx=(15, 15), ipady=4, fill='x', expand=True)
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

        tk.Label(price_container, text="$", font=Theme.FONTS['body'], bg=bg_color, fg='#6b7280').pack(side='left')

        pr_entry = tk.Entry(price_container, font=Theme.FONTS['body'], bg='white', relief='flat', bd=1, highlightthickness=1, highlightbackground='#e5e7eb', width=12)
        pr_entry.pack(side='left', padx=(2, 0), ipady=4)
        self.price_entries.append(pr_entry)

        pr_entry.bind('<KeyRelease>', lambda e, idx=index: self.validate_price(e, idx))

    def create_button_panel(self, parent):
        frame = tk.Frame(parent, bg=Theme.BACKGROUND)
        frame.pack(pady=10)

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
