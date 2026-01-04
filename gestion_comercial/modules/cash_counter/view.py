import tkinter as tk
from gestion_comercial.config.theme import Theme
from gestion_comercial.modules.cash_counter.model import CashCounterModel

class CashCounterView(tk.Frame):
    def __init__(self, parent, navigator):
        super().__init__(parent, bg=Theme.BACKGROUND)
        self.navigator = navigator
        self.model = CashCounterModel()
        
        self.entries_bills = {}
        self.subtotals_bills = {}
        self.entries_coins_weight = {}
        self.entries_coins_qty = {}
        self.labels_coins_value = {}
        
        self.calculating = {}
        
        self.setup_ui()
        
    def setup_ui(self):
        # Top green accent strip
        self.create_top_accent()

        # Header with Back Button
        self.create_header()

        # Main Content
        content_frame = tk.Frame(self, bg=Theme.BACKGROUND)
        content_frame.pack(fill='both', expand=True, padx=30, pady=(10, 5))

        # Bills Section
        self.create_bills_section(content_frame)

        # Coins Section
        self.create_coins_section(content_frame)

        # Totals Section
        self.create_totals_section(content_frame)

        # Action Buttons
        self.create_action_buttons(content_frame)

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
            text="Contador de Caja Registradora",
            font=(Theme.FONT_FAMILY, 20, 'bold'),
            bg=Theme.TEXT_PRIMARY,
            fg='white'
        ).pack()
        
    def create_bills_section(self, parent):
        frame = tk.LabelFrame(
            parent,
            text="💵 BILLETES",
            font=Theme.FONTS['h3'],
            bg=Theme.BILLS_BG,
            fg=Theme.BILLS_FG,
            padx=10, pady=5
        )
        frame.pack(fill='x', pady=(0, 5))
        
        # Headers
        headers = [("Denominación", 0, 15), ("Cantidad", 1, 10), ("Subtotal", 2, 15)]
        for text, col, width in headers:
            tk.Label(frame, text=text, font=Theme.FONTS['body_bold'], bg=Theme.BILLS_BG, width=width).grid(row=0, column=col, padx=5, pady=2)
            
        # Rows
        for i, denom in enumerate(self.model.bills, 1):
            self.create_bill_row(frame, denom, i)
            
        # Total Bills
        self.create_total_row(frame, len(self.model.bills) + 1, "Total Billetes:", "total_bills")

    def create_bill_row(self, parent, denom, row):
        # Get bill color (para el texto)
        bill_colors = {
            20000: '#FF6B35',  # Orange
            10000: '#4A90E2',  # Blue
            5000: '#E63946',   # Red
            2000: '#9B59B6',   # Purple
            1000: '#2ECC71'    # Green
        }
        bill_color = bill_colors.get(denom, Theme.BILLS_FG)

        # Label con color de texto y fondo transparente
        lbl_denom = tk.Label(
            parent,
            text=f"${self.format_number(denom)}",
            font=(Theme.FONT_FAMILY, 11, 'bold'),
            bg=Theme.BILLS_BG,
            fg=bill_color,
            padx=10,
            pady=3,
            anchor='w',
            width=12
        )
        lbl_denom.grid(row=row, column=0, padx=5, pady=2, sticky='w')

        entry = tk.Entry(parent, width=10, font=Theme.FONTS['body'], justify='center', bg=Theme.ENTRY_BG)
        entry.grid(row=row, column=1, padx=5, pady=2)
        entry.insert(0, "0")
        entry.bind('<KeyRelease>', lambda e, d=denom: self.on_bill_change(d))
        entry.bind('<FocusIn>', self.on_focus_in)

        self.entries_bills[denom] = entry

        lbl_sub = tk.Label(parent, text="$0", font=Theme.FONTS['body'], bg=Theme.BILLS_BG, width=15)
        lbl_sub.grid(row=row, column=2)
        self.subtotals_bills[denom] = lbl_sub

    def create_coins_section(self, parent):
        frame = tk.LabelFrame(
            parent,
            text="🪙 MONEDAS",
            font=Theme.FONTS['h3'],
            bg=Theme.COINS_BG,
            fg=Theme.COINS_FG,
            padx=10, pady=5
        )
        frame.pack(fill='x', pady=(0, 5))
        
        # Headers
        headers = [("Denominación", 0, 12), ("Peso (g)", 1, 10), ("Cantidad", 2, 10), ("Valor", 3, 12)]
        for text, col, width in headers:
            tk.Label(frame, text=text, font=Theme.FONTS['body_bold'], bg=Theme.COINS_BG, width=width).grid(row=0, column=col, padx=5, pady=2)
            
        row = 1
        # 500 (Qty only)
        self.create_coin_qty_row(frame, 500, row)
        row += 1
        
        # Weighted coins
        for denom in sorted(self.model.coins_weight.keys(), reverse=True):
            self.create_coin_weight_row(frame, denom, row)
            row += 1
            
        # Total Coins
        self.create_total_row(frame, row, "Total Monedas:", "total_coins", col_offset=1)

    def create_coin_qty_row(self, parent, denom, row):
        # Label con texto negro y negrita (sin color de fondo)
        lbl_denom = tk.Label(
            parent,
            text=f"${denom}",
            font=(Theme.FONT_FAMILY, 11, 'bold'),
            bg=Theme.COINS_BG,
            fg='black',
            padx=10,
            pady=3,
            anchor='w',
            width=12
        )
        lbl_denom.grid(row=row, column=0, padx=5, pady=2, sticky='w')

        # Empty space for peso column (no weight for 500 peso coin)
        tk.Label(parent, text="", font=Theme.FONTS['body'], bg=Theme.COINS_BG).grid(row=row, column=1, pady=2)

        entry = tk.Entry(parent, width=10, font=Theme.FONTS['body'], justify='center', bg=Theme.ENTRY_BG)
        entry.grid(row=row, column=2, padx=5, pady=2)
        entry.insert(0, "0")
        entry.bind('<KeyRelease>', lambda e, d=denom: self.on_coin_qty_change(d))
        entry.bind('<FocusIn>', self.on_focus_in)
        
        self.entries_coins_qty[denom] = entry
        
        lbl_val = tk.Label(parent, text="$0", font=Theme.FONTS['body'], bg=Theme.COINS_BG)
        lbl_val.grid(row=row, column=3, pady=2)
        self.labels_coins_value[denom] = lbl_val

    def create_coin_weight_row(self, parent, denom, row):
        # Label con texto negro y negrita (sin color de fondo)
        lbl_denom = tk.Label(
            parent,
            text=f"${denom}",
            font=(Theme.FONT_FAMILY, 11, 'bold'),
            bg=Theme.COINS_BG,
            fg='black',
            padx=10,
            pady=3,
            anchor='w',
            width=12
        )
        lbl_denom.grid(row=row, column=0, padx=5, pady=2, sticky='w')

        entry_w = tk.Entry(parent, width=10, font=Theme.FONTS['body'], justify='center', bg=Theme.ENTRY_BG)
        entry_w.grid(row=row, column=1, padx=5, pady=2)
        entry_w.insert(0, "0")
        entry_w.bind('<KeyRelease>', lambda e, d=denom: self.on_coin_weight_change(d))
        entry_w.bind('<FocusIn>', self.on_focus_in)
        self.entries_coins_weight[denom] = entry_w

        entry_q = tk.Entry(parent, width=10, font=Theme.FONTS['body'], justify='center', bg=Theme.ENTRY_BG)
        entry_q.grid(row=row, column=2, padx=5, pady=2)
        entry_q.insert(0, "0")
        entry_q.bind('<KeyRelease>', lambda e, d=denom: self.on_coin_qty_change(d))
        entry_q.bind('<FocusIn>', self.on_focus_in)
        self.entries_coins_qty[denom] = entry_q
        
        lbl_val = tk.Label(parent, text="$0", font=Theme.FONTS['body'], bg=Theme.COINS_BG)
        lbl_val.grid(row=row, column=3, pady=2)
        self.labels_coins_value[denom] = lbl_val

    def create_total_row(self, parent, row, text, attr_name, col_offset=0):
        tk.Label(parent, text=text, font=Theme.FONTS['h3'], bg=parent['bg']).grid(row=row, column=1+col_offset, pady=3)
        lbl = tk.Label(parent, text="$0", font=Theme.FONTS['h3'], fg=parent['fg'], bg=parent['bg'])
        lbl.grid(row=row, column=2+col_offset, pady=3)
        setattr(self, attr_name, lbl)

    def create_totals_section(self, parent):
        frame = tk.LabelFrame(
            parent,
            text="💯 TOTAL GENERAL",
            font=Theme.FONTS['h2'],
            bg=Theme.TOTAL_BG,
            fg=Theme.TOTAL_FG,
            padx=10, pady=5
        )
        frame.pack(fill='x', pady=(0, 5))
        
        self.total_general = tk.Label(
            frame,
            text="$0",
            font=Theme.FONTS['total_large'],
            fg=Theme.TOTAL_TEXT,
            bg=Theme.TOTAL_BG
        )
        self.total_general.pack()

    def create_action_buttons(self, parent):
        frame = tk.Frame(parent, bg=Theme.BACKGROUND)
        frame.pack(pady=5)

        # Back Button (Blue theme)
        self.create_styled_button(
            frame,
            text="⬅ Volver",
            command=lambda: self.navigator.show_view('launcher'),
            bg_color=Theme.TOTAL_FG,
            hover_color='#0d47a1'
        )

        # Clear Button (Gray theme)
        self.create_styled_button(
            frame,
            text="🔄 Limpiar",
            command=self.clear_all,
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
            padx=25,
            pady=8,
            relief='flat',
            bd=0,
            cursor='hand2',
            activebackground=hover_color,
            activeforeground='white'
        )
        btn.pack(side='left', padx=20)

        # Hover effect
        def on_enter(e):
            btn.configure(bg=hover_color)

        def on_leave(e):
            btn.configure(bg=bg_color)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    # Logic Handlers
    def on_focus_in(self, event):
        if event.widget.get() == "0":
            event.widget.delete(0, tk.END)

    def on_bill_change(self, denom):
        try:
            qty = int(self.entries_bills[denom].get() or 0)
            subtotal = self.model.calculate_bill_subtotal(denom, qty)
            self.subtotals_bills[denom].config(text=f"${self.format_number(subtotal)}")
        except ValueError:
            self.subtotals_bills[denom].config(text="$0")
        self.calculate_totals()

    def on_coin_weight_change(self, denom):
        if self.calculating.get(denom): return
        
        try:
            weight = float(self.entries_coins_weight[denom].get() or 0)
            qty, val = self.model.calculate_coin_from_weight(denom, weight)
            
            self.calculating[denom] = True
            self.entries_coins_qty[denom].delete(0, tk.END)
            self.entries_coins_qty[denom].insert(0, str(qty))
            self.calculating[denom] = False
            
            self.labels_coins_value[denom].config(text=f"${self.format_number(val)}")
        except ValueError:
            pass
        self.calculate_totals()

    def on_coin_qty_change(self, denom):
        if self.calculating.get(denom): return
        
        try:
            qty = int(self.entries_coins_qty[denom].get() or 0)
            weight, val = self.model.calculate_coin_from_quantity(denom, qty)
            
            if denom in self.entries_coins_weight:
                self.calculating[denom] = True
                self.entries_coins_weight[denom].delete(0, tk.END)
                self.entries_coins_weight[denom].insert(0, f"{weight:.3f}")
                self.calculating[denom] = False
                
            self.labels_coins_value[denom].config(text=f"${self.format_number(val)}")
        except ValueError:
            pass
        self.calculate_totals()

    def calculate_totals(self):
        total_bills = 0
        for denom, entry in self.entries_bills.items():
            try:
                total_bills += int(entry.get() or 0) * denom
            except ValueError: pass
            
        total_coins = 0
        for denom, entry in self.entries_coins_qty.items():
            try:
                total_coins += int(entry.get() or 0) * denom
            except ValueError: pass
            
        self.total_bills.config(text=f"${self.format_number(total_bills)}")
        self.total_coins.config(text=f"${self.format_number(total_coins)}")
        self.total_general.config(text=f"${self.format_number(total_bills + total_coins)}")

    def clear_all(self):
        for e in self.entries_bills.values():
            e.delete(0, tk.END); e.insert(0, "0")
        for e in self.entries_coins_qty.values():
            e.delete(0, tk.END); e.insert(0, "0")
        for e in self.entries_coins_weight.values():
            e.delete(0, tk.END); e.insert(0, "0")
        for l in self.subtotals_bills.values(): l.config(text="$0")
        for l in self.labels_coins_value.values(): l.config(text="$0")
        self.calculate_totals()

    def format_number(self, num):
        return f"{int(num):,}".replace(",", ".")
