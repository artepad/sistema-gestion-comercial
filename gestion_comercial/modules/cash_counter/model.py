class CashCounterModel:
    def __init__(self):
        # Denominations
        self.bills = [20000, 10000, 5000, 2000, 1000]
        
        self.coins_weight = {
            100: 7.57/1000,  # 7.57g
            50: 7.0/1000,    # 7.0g
            10: 3.5/1000     # 3.5g
        }
        
        self.coins_qty = [500]
        
    def calculate_bill_subtotal(self, denomination, quantity):
        return denomination * quantity
        
    def calculate_coin_from_weight(self, denomination, weight):
        if denomination not in self.coins_weight:
            return 0, 0
            
        unit_weight = self.coins_weight[denomination]
        if unit_weight <= 0:
            return 0, 0
            
        quantity = round(weight / unit_weight)
        total_value = quantity * denomination
        return quantity, total_value
        
    def calculate_coin_from_quantity(self, denomination, quantity):
        total_value = quantity * denomination
        
        weight = 0
        if denomination in self.coins_weight:
            weight = quantity * self.coins_weight[denomination]
            
        return weight, total_value
