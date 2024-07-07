class Pharmacy:
    def __init__(self, pharmacy_name, initial_balance, initial_new_inventory, initial_old_inventory,
                  unit_cost = 10, unit_revenue = 20, holding_cost = 2, outdating_cost = 5):
        self.balance = initial_balance
        self.name = pharmacy_name
        self.inventory = {'new': initial_new_inventory, 'old': initial_old_inventory}
        self.revenue_per_unit = unit_revenue
        self.cost_per_unit = unit_cost
        self.holding_cost = holding_cost
        self.outdating_cost = outdating_cost
        self.sales_counter = 0
        self.lost_sales_counter = 0
    
    def replenish(self, amount):
        self.inventory['new'] += amount
        self.balance -= amount * self.cost_per_unit  # Assume each replenished item costs 10 unit of currency
    
    def process_day_end(self):
        # Apply holding cost for all items
        total_inventory = self.inventory['new'] + self.inventory['old']
        self.balance -= self.holding_cost * total_inventory
        
        # Apply outdating cost for old items that perish
        self.balance -= self.outdating_cost * self.inventory['old']
        # 'old' items perish at the end of the day
        self.inventory['old'] = 0
        # 'new' items become 'old' at the end of the day
        self.inventory['old'] = self.inventory['new']
        self.inventory['new'] = 0
    
    def fulfill_demand(self):
        if self.inventory['old'] > 0:
            self.inventory['old'] -= 1
            self.balance += self.revenue_per_unit
            self.sales_counter += 1
            return True
        elif self.inventory['new'] > 0:
            self.inventory['new'] -= 1
            self.balance += self.revenue_per_unit
            self.sales_counter += 1
            return True
        else:
            # Implicit lost sales cost (not explicit) = - (revenue - cost)
            lost_sales_cost = -(self.revenue_per_unit - self.cost_per_unit)
            self.balance += lost_sales_cost
            self.lost_sales_counter += 1
            print(self.get_name() + " has no inventory to fulfill demand")
            return False
           
    def get_inventory_level(self):
        return self.inventory['new'] + self.inventory['old']
    
    def get_shelf_life_value(self):
        return 2 * self.inventory['new'] + self.inventory['old']
    
    def get_name(self):
        return "Pharmacy " + self.name
    
    def __str__(self):
        return f"Balance: {self.balance}, Inventory: {self.inventory}"
    
    def __repr__(self):
        return self.get_name()