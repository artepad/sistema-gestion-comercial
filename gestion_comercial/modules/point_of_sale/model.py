"""
Modelo del módulo Punto de Venta.
Gestiona la lógica del carrito de ventas (POS de respaldo).
"""


class PointOfSaleModel:
    def __init__(self):
        self.cart = []  # Lista de dicts: {code, name, price, qty}

    def add_item(self, code, name, price, qty=1):
        """Agrega item al carrito. Acumula cantidad solo si es escaneado (mismo código)."""
        # Solo acumular si el código NO es manual
        if code != "MANUAL":
            for item in self.cart:
                if item['code'] == code:
                    item['qty'] += qty
                    return
        self.cart.append({
            'code': code,
            'name': name,
            'price': price,
            'qty': qty
        })

    def remove_item(self, index):
        """Elimina un item del carrito por índice."""
        if 0 <= index < len(self.cart):
            self.cart.pop(index)

    def update_quantity(self, index, new_qty):
        """Actualiza la cantidad de un item."""
        if 0 <= index < len(self.cart) and new_qty > 0:
            self.cart[index]['qty'] = new_qty

    def get_total(self):
        """Calcula el total de la venta."""
        return sum(item['price'] * item['qty'] for item in self.cart)

    def get_item_subtotal(self, index):
        """Calcula el subtotal de un item."""
        if 0 <= index < len(self.cart):
            item = self.cart[index]
            return item['price'] * item['qty']
        return 0

    def clear_cart(self):
        """Limpia el carrito completo."""
        self.cart.clear()

    def get_cart_items(self):
        """Retorna la lista de items del carrito."""
        return self.cart

    def get_item_count(self):
        """Retorna la cantidad total de items (sumando cantidades)."""
        return sum(item['qty'] for item in self.cart)
