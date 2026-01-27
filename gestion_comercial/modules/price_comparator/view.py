"""
Vista del módulo de comparación de precios
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
from gestion_comercial.config.theme import Theme
from .model import PriceComparator


class PriceComparatorView(tk.Frame):
    """Vista principal del comparador de precios"""

    def __init__(self, parent, navigator):
        super().__init__(parent, bg=Theme.BACKGROUND)
        self.navigator = navigator
        self.comparator = PriceComparator()
        self.main_file_path = None
        self.comparison_file_path = None
        self.differences = []
        self.fullscreen_mode = False

        # Binding para F11 (pantalla completa)
        self.bind_all('<F11>', self.toggle_fullscreen)

        self.setup_ui()

    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Top green accent strip
        self.create_top_accent()

        # Header compacto
        self.create_header()

        # Container principal
        main_container = tk.Frame(self, bg=Theme.BACKGROUND)
        main_container.pack(fill='both', expand=True, padx=40, pady=20)

        # Sección de carga de archivos (compacta)
        self.create_file_selection_section(main_container)

        # Sección de estadísticas (inicialmente oculta)
        self.create_statistics_section(main_container)

        # Sección de resultados (inicialmente oculta)
        self.create_results_section(main_container)

        # Botones inferiores
        self.create_bottom_buttons(main_container)

        # Bottom blue accent strip
        self.create_bottom_accent()

    def create_top_accent(self):
        """Crea la franja de acento superior"""
        tk.Frame(self, bg='#2ecc71', height=4).pack(fill='x')

    def create_bottom_accent(self):
        """Crea la franja de acento inferior"""
        tk.Frame(self, bg='#3498db', height=4).pack(side='bottom', fill='x')

    def create_header(self):
        """Crea el encabezado con fondo azul"""
        header_frame = tk.Frame(self, bg=Theme.TEXT_PRIMARY, height=70)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        # Content container para centrar
        content_container = tk.Frame(header_frame, bg=Theme.TEXT_PRIMARY)
        content_container.place(relx=0.5, rely=0.5, anchor='center')

        # Título centrado
        tk.Label(
            content_container,
            text='Comparador de Precios',
            font=(Theme.FONT_FAMILY, 18, 'bold'),
            bg=Theme.TEXT_PRIMARY,
            fg='white'
        ).pack()

    def create_file_selection_section(self, parent):
        """Crea la sección compacta de selección de archivos"""
        # Frame con estilo similar a "Información de base de datos"
        files_frame = tk.LabelFrame(
            parent,
            text="📁 Selección de Bases de Datos",
            font=(Theme.FONT_FAMILY, 11, 'bold'),
            bg='#f8f9fa',
            fg='#495057',
            padx=20,
            pady=15
        )
        files_frame.pack(fill='x', pady=(0, 15))

        # Contenido interno
        content_frame = tk.Frame(files_frame, bg='#f8f9fa')
        content_frame.pack(fill='x')

        # Archivo principal (compacto)
        main_row = tk.Frame(content_frame, bg='#f8f9fa')
        main_row.pack(fill='x', pady=(0, 10))

        tk.Label(
            main_row,
            text='Base Principal:',
            font=(Theme.FONT_FAMILY, 10, 'bold'),
            bg='#f8f9fa',
            fg=Theme.TEXT_PRIMARY,
            width=15,
            anchor='w'
        ).pack(side='left', padx=(0, 10))

        self.main_file_label = tk.Label(
            main_row,
            text='Ningún archivo seleccionado',
            font=(Theme.FONT_FAMILY, 9),
            bg='#f8f9fa',
            fg='#6c757d',
            anchor='w'
        )
        self.main_file_label.pack(side='left', fill='x', expand=True, padx=(0, 10))

        tk.Button(
            main_row,
            text='Seleccionar',
            font=(Theme.FONT_FAMILY, 9),
            bg='#3498db',
            fg='white',
            bd=0,
            padx=12,
            pady=5,
            cursor='hand2',
            command=self.select_main_file
        ).pack(side='left')

        # Archivo de comparación (compacto)
        comp_row = tk.Frame(content_frame, bg='#f8f9fa')
        comp_row.pack(fill='x', pady=(0, 15))

        tk.Label(
            comp_row,
            text='Base a Comparar:',
            font=(Theme.FONT_FAMILY, 10, 'bold'),
            bg='#f8f9fa',
            fg=Theme.TEXT_PRIMARY,
            width=15,
            anchor='w'
        ).pack(side='left', padx=(0, 10))

        self.comparison_file_label = tk.Label(
            comp_row,
            text='Ningún archivo seleccionado',
            font=(Theme.FONT_FAMILY, 9),
            bg='#f8f9fa',
            fg='#6c757d',
            anchor='w'
        )
        self.comparison_file_label.pack(side='left', fill='x', expand=True, padx=(0, 10))

        tk.Button(
            comp_row,
            text='Seleccionar',
            font=(Theme.FONT_FAMILY, 9),
            bg='#3498db',
            fg='white',
            bd=0,
            padx=12,
            pady=5,
            cursor='hand2',
            command=self.select_comparison_file
        ).pack(side='left')

        # Botón comparar centrado
        button_row = tk.Frame(content_frame, bg='#f8f9fa')
        button_row.pack(fill='x')

        self.compare_btn = tk.Button(
            button_row,
            text='⚖️ Comparar Bases de Datos',
            font=(Theme.FONT_FAMILY, 11, 'bold'),
            bg='#27ae60',
            fg='white',
            bd=0,
            padx=25,
            pady=10,
            cursor='hand2',
            state='disabled',
            command=self.compare_databases
        )
        self.compare_btn.pack()

    def create_statistics_section(self, parent):
        """Crea la sección compacta de estadísticas"""
        self.stats_frame = tk.LabelFrame(
            parent,
            text="📊 Resumen de Comparación",
            font=(Theme.FONT_FAMILY, 11, 'bold'),
            bg='#f8f9fa',
            fg='#495057',
            padx=20,
            pady=12
        )
        # Inicialmente oculto

        # Contenedor horizontal para las 3 estadísticas
        stats_container = tk.Frame(self.stats_frame, bg='#f8f9fa')
        stats_container.pack(fill='x')

        # Estadística Total
        total_frame = tk.Frame(stats_container, bg='#f8f9fa')
        total_frame.pack(side='left', fill='x', expand=True, padx=5)

        tk.Label(
            total_frame,
            text='Total de Diferencias',
            font=(Theme.FONT_FAMILY, 9),
            bg='#f8f9fa',
            fg='#6c757d'
        ).pack()

        self.total_diff_label = tk.Label(
            total_frame,
            text='0',
            font=(Theme.FONT_FAMILY, 24, 'bold'),
            bg='#f8f9fa',
            fg='#e74c3c'
        )
        self.total_diff_label.pack()

        # Separador 1
        tk.Frame(stats_container, bg='#dde1e6', width=2).pack(side='left', fill='y', padx=10)

        # Estadística Diferencias de Precio
        price_frame = tk.Frame(stats_container, bg='#f8f9fa')
        price_frame.pack(side='left', fill='x', expand=True, padx=5)

        tk.Label(
            price_frame,
            text='Diferencias de Precio',
            font=(Theme.FONT_FAMILY, 9),
            bg='#f8f9fa',
            fg='#6c757d'
        ).pack()

        self.price_diff_label = tk.Label(
            price_frame,
            text='0',
            font=(Theme.FONT_FAMILY, 24, 'bold'),
            bg='#f8f9fa',
            fg='#f39c12'
        )
        self.price_diff_label.pack()

        # Separador 2
        tk.Frame(stats_container, bg='#dde1e6', width=2).pack(side='left', fill='y', padx=10)

        # Estadística Productos Faltantes
        missing_frame = tk.Frame(stats_container, bg='#f8f9fa')
        missing_frame.pack(side='left', fill='x', expand=True, padx=5)

        tk.Label(
            missing_frame,
            text='Productos Faltantes',
            font=(Theme.FONT_FAMILY, 9),
            bg='#f8f9fa',
            fg='#6c757d'
        ).pack()

        self.missing_label = tk.Label(
            missing_frame,
            text='0',
            font=(Theme.FONT_FAMILY, 24, 'bold'),
            bg='#f8f9fa',
            fg='#3498db'
        )
        self.missing_label.pack()

    def create_results_section(self, parent):
        """Crea la sección de resultados con tabla"""
        self.results_container = tk.Frame(parent, bg=Theme.BACKGROUND)
        # Inicialmente oculto

        # Frame con scrollbar
        table_frame = tk.Frame(self.results_container, bg=Theme.BACKGROUND)
        table_frame.pack(fill='both', expand=True)

        # Scrollbar vertical
        scrollbar_y = ttk.Scrollbar(table_frame, orient='vertical')
        scrollbar_y.pack(side='right', fill='y')

        # Scrollbar horizontal
        scrollbar_x = ttk.Scrollbar(table_frame, orient='horizontal')
        scrollbar_x.pack(side='bottom', fill='x')

        # Crear Treeview
        columns = ('barcode', 'name', 'main_price', 'comp_price', 'difference', 'status')
        self.results_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set,
            height=12
        )

        # Configurar scrollbars
        scrollbar_y.config(command=self.results_tree.yview)
        scrollbar_x.config(command=self.results_tree.xview)

        # Configurar columnas
        self.results_tree.heading('barcode', text='Código')
        self.results_tree.heading('name', text='Producto')
        self.results_tree.heading('main_price', text='Precio Principal')
        self.results_tree.heading('comp_price', text='Precio Comparación')
        self.results_tree.heading('difference', text='Diferencia')
        self.results_tree.heading('status', text='Estado')

        self.results_tree.column('barcode', width=100, anchor='center')
        self.results_tree.column('name', width=220, anchor='w')
        self.results_tree.column('main_price', width=110, anchor='center')
        self.results_tree.column('comp_price', width=110, anchor='center')
        self.results_tree.column('difference', width=90, anchor='center')
        self.results_tree.column('status', width=90, anchor='center')

        self.results_tree.pack(fill='both', expand=True)

        # Configurar tags para colores
        self.results_tree.tag_configure('price_diff', background='#fff3cd')
        self.results_tree.tag_configure('missing', background='#cfe2ff')

        # Bind doble click
        self.results_tree.bind('<Double-1>', self.on_row_double_click)

        # Ayuda compacta
        tk.Label(
            self.results_container,
            text='💡 Doble click para editar',
            font=(Theme.FONT_FAMILY, 9, 'italic'),
            bg=Theme.BACKGROUND,
            fg='#6c757d'
        ).pack(pady=(5, 0))

    def create_bottom_buttons(self, parent):
        """Crea los botones inferiores centrados con estilo de tag_manager"""
        button_frame = tk.Frame(parent, bg=Theme.BACKGROUND)
        button_frame.pack(side='bottom', fill='x', pady=(15, 0))

        # Container centrado para los botones
        buttons_container = tk.Frame(button_frame, bg=Theme.BACKGROUND)
        buttons_container.pack(anchor='center')

        # Botón Volver - Blue like tag_manager
        self.create_styled_button(
            buttons_container,
            text="⬅ Volver",
            command=lambda: self.navigator.show_view('launcher'),
            bg_color=Theme.TOTAL_FG,  # #1565c0
            hover_color='#0d47a1'
        )

        # Botón Comparar - Green like tag_manager "Generar"
        self.create_styled_button(
            buttons_container,
            text="Comparar",
            command=self.generate_comparison_report,
            bg_color='#27ae60',
            hover_color='#1e8449'
        )

        # Botón Ampliar Vista - Gray like tag_manager "Limpiar"
        self.fullscreen_btn = self.create_styled_button(
            buttons_container,
            text="Ampliar Vista (F11)",
            command=lambda: self.toggle_fullscreen(None),
            bg_color='#6c757d',
            hover_color='#5a6268'
        )

    def create_styled_button(self, parent, text, command, bg_color, hover_color):
        """Creates a button with hover animation (same style as tag_manager)"""
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

        return btn

    def select_main_file(self):
        """Abre diálogo para seleccionar archivo principal"""
        file_path = filedialog.askopenfilename(
            title='Seleccionar base de datos principal',
            filetypes=[('Excel files', '*.xlsx'), ('All files', '*.*')]
        )

        if file_path:
            try:
                self.comparator.set_main_database(file_path)
                self.main_file_path = file_path
                filename = file_path.split('/')[-1]
                self.main_file_label.config(
                    text=filename,
                    fg='#27ae60'
                )
                self.check_enable_compare_button()
            except Exception as e:
                messagebox.showerror('Error', f'Error al cargar archivo:\n{str(e)}')

    def select_comparison_file(self):
        """Abre diálogo para seleccionar archivo de comparación"""
        file_path = filedialog.askopenfilename(
            title='Seleccionar base de datos a comparar',
            filetypes=[('Excel files', '*.xlsx'), ('All files', '*.*')]
        )

        if file_path:
            try:
                self.comparator.set_comparison_database(file_path)
                self.comparison_file_path = file_path
                filename = file_path.split('/')[-1]
                self.comparison_file_label.config(
                    text=filename,
                    fg='#27ae60'
                )
                self.check_enable_compare_button()
            except Exception as e:
                messagebox.showerror('Error', f'Error al cargar archivo:\n{str(e)}')

    def check_enable_compare_button(self):
        """Habilita el botón comparar si ambos archivos están cargados"""
        if self.main_file_path and self.comparison_file_path:
            self.compare_btn.config(state='normal')

    def compare_databases(self):
        """Ejecuta la comparación de bases de datos"""
        try:
            # Realizar comparación
            self.differences = self.comparator.compare_databases()

            # Actualizar estadísticas
            stats = self.comparator.get_statistics()
            self.update_statistics(stats)

            # Mostrar resultados
            self.display_results()

            # Mostrar secciones
            self.stats_frame.pack(fill='x', pady=(0, 10))
            self.results_container.pack(fill='both', expand=True, pady=(0, 10))

            if len(self.differences) == 0:
                messagebox.showinfo(
                    'Comparación Completa',
                    'No se encontraron diferencias entre las bases de datos.'
                )

        except Exception as e:
            messagebox.showerror('Error', f'Error al comparar:\n{str(e)}')

    def update_statistics(self, stats):
        """Actualiza las tarjetas de estadísticas"""
        self.total_diff_label.config(text=str(stats['total_differences']))
        self.price_diff_label.config(text=str(stats['price_differences']))
        self.missing_label.config(text=str(stats['missing_products']))

    def display_results(self):
        """Muestra los resultados en la tabla"""
        # Limpiar tabla
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)

        # Agregar diferencias
        for diff in self.differences:
            barcode = diff['barcode']
            name = diff['name']
            main_price = f"${diff['main_price']:,.0f}"
            comp_price = f"${diff['comparison_price']:,.0f}" if diff['comparison_price'] else 'N/A'
            difference = f"${diff['difference']:,.0f}" if diff['difference'] else 'N/A'
            status = 'Diferencia' if diff['status'] == 'price_diff' else 'Faltante'

            self.results_tree.insert(
                '',
                'end',
                values=(barcode, name, main_price, comp_price, difference, status),
                tags=(diff['status'],)
            )

    def on_row_double_click(self, event):
        """Maneja el doble click en una fila"""
        selection = self.results_tree.selection()
        if not selection:
            return

        item = selection[0]
        values = self.results_tree.item(item, 'values')
        barcode = values[0]
        status = values[5]

        diff = next((d for d in self.differences if d['barcode'] == barcode), None)
        if not diff:
            return

        if status == 'Diferencia':
            self.show_modify_price_dialog(diff)
        elif status == 'Faltante':
            self.show_add_product_dialog(diff)

    def show_modify_price_dialog(self, diff):
        """Muestra diálogo para modificar precio"""
        dialog = tk.Toplevel(self)
        dialog.title('Modificar Precio')
        dialog.geometry('380x220')
        dialog.resizable(False, False)
        dialog.configure(bg=Theme.BACKGROUND)
        dialog.transient(self)
        dialog.grab_set()

        # Centrar
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (380 // 2)
        y = (dialog.winfo_screenheight() // 2) - (220 // 2)
        dialog.geometry(f'+{x}+{y}')

        # Título
        tk.Label(
            dialog,
            text='Modificar Precio',
            font=(Theme.FONT_FAMILY, 12, 'bold'),
            bg=Theme.BACKGROUND,
            fg=Theme.TEXT_PRIMARY
        ).pack(pady=(15, 10))

        # Info
        info_frame = tk.Frame(dialog, bg=Theme.BACKGROUND)
        info_frame.pack(pady=8, padx=20, fill='x')

        tk.Label(
            info_frame,
            text=f"Producto: {diff['name'][:40]}...",
            font=(Theme.FONT_FAMILY, 9),
            bg=Theme.BACKGROUND,
            fg=Theme.TEXT_PRIMARY
        ).pack(anchor='w')

        tk.Label(
            info_frame,
            text=f"Actual: ${diff['comparison_price']:,.0f} → Nuevo: ${diff['main_price']:,.0f}",
            font=(Theme.FONT_FAMILY, 9),
            bg=Theme.BACKGROUND,
            fg='#27ae60'
        ).pack(anchor='w')

        # Entry
        tk.Label(
            dialog,
            text='Precio a aplicar:',
            font=(Theme.FONT_FAMILY, 10),
            bg=Theme.BACKGROUND,
            fg=Theme.TEXT_PRIMARY
        ).pack(anchor='w', padx=20)

        price_entry = tk.Entry(
            dialog,
            font=(Theme.FONT_FAMILY, 11),
            bd=1,
            relief='solid'
        )
        price_entry.pack(pady=5, padx=20, fill='x')
        price_entry.insert(0, str(int(diff['main_price'])))
        price_entry.focus()

        # Botones
        btn_frame = tk.Frame(dialog, bg=Theme.BACKGROUND)
        btn_frame.pack(pady=15)

        def save_price():
            try:
                new_price = float(price_entry.get())
                if new_price <= 0:
                    messagebox.showerror('Error', 'El precio debe ser mayor a 0')
                    return

                if self.comparator.update_price(diff['barcode'], new_price):
                    messagebox.showinfo('Éxito', 'Precio actualizado')
                    dialog.destroy()
                    self.compare_databases()
                else:
                    messagebox.showerror('Error', 'No se pudo actualizar')
            except ValueError:
                messagebox.showerror('Error', 'Precio inválido')

        tk.Button(
            btn_frame,
            text='Guardar',
            font=(Theme.FONT_FAMILY, 10),
            bg='#27ae60',
            fg='white',
            bd=0,
            padx=18,
            pady=7,
            cursor='hand2',
            command=save_price
        ).pack(side='left', padx=5)

        tk.Button(
            btn_frame,
            text='Cancelar',
            font=(Theme.FONT_FAMILY, 10),
            bg='#95a5a6',
            fg='white',
            bd=0,
            padx=18,
            pady=7,
            cursor='hand2',
            command=dialog.destroy
        ).pack(side='left', padx=5)

    def show_add_product_dialog(self, diff):
        """Muestra diálogo para agregar producto"""
        result = messagebox.askyesno(
            'Agregar Producto',
            f"¿Agregar '{diff['name'][:50]}...' a la base de comparación?\n\n"
            f"Código: {diff['barcode']}\n"
            f"Precio: ${diff['main_price']:,.0f}"
        )

        if result:
            try:
                if self.comparator.add_product(diff['barcode']):
                    messagebox.showinfo('Éxito', 'Producto agregado')
                    self.compare_databases()
                else:
                    messagebox.showerror('Error', 'No se pudo agregar')
            except Exception as e:
                messagebox.showerror('Error', f'Error:\n{str(e)}')

    def generate_comparison_report(self):
        """Genera y guarda el reporte de comparación en formato texto"""
        # Verificar que hay datos para comparar
        if not self.main_file_path or not self.comparison_file_path:
            messagebox.showwarning(
                'Advertencia',
                'Debes cargar ambas bases de datos primero.'
            )
            return

        # Verificar que se haya ejecutado la comparación
        if not self.differences:
            messagebox.showwarning(
                'Advertencia',
                'No hay datos de comparación. Presiona "Comparar" primero.'
            )
            return

        try:
            # Generar el reporte
            report_content = self.comparator.generate_report()

            # Generar nombre de archivo con fecha actual
            today = datetime.now().strftime('%Y%m%d')
            default_filename = f'actualizacion_precios_{today}.txt'

            # Abrir diálogo para guardar archivo
            file_path = filedialog.asksaveasfilename(
                title='Guardar reporte de comparación',
                defaultextension='.txt',
                initialfile=default_filename,
                filetypes=[
                    ('Archivos de texto', '*.txt'),
                    ('Todos los archivos', '*.*')
                ]
            )

            # Si el usuario cancela, no hacer nada
            if not file_path:
                return

            # Guardar el archivo
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(report_content)

            # Mostrar mensaje de éxito
            messagebox.showinfo(
                'Reporte Generado',
                f'El reporte se ha guardado exitosamente en:\n{file_path}'
            )

        except Exception as e:
            messagebox.showerror(
                'Error',
                f'Error al generar el reporte:\n{str(e)}'
            )

    def toggle_fullscreen(self, event):
        """Alterna el modo pantalla completa"""
        root = self.winfo_toplevel()
        self.fullscreen_mode = not self.fullscreen_mode
        root.attributes('-fullscreen', self.fullscreen_mode)

        # Actualizar texto del botón
        if self.fullscreen_mode:
            self.fullscreen_btn.config(text='Restaurar Vista (F11)')
        else:
            self.fullscreen_btn.config(text='Ampliar Vista (F11)')
