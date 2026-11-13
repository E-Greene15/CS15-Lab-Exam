class Inventory:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        if self.search(item.name):
            return False

        self.items.append(item)
        return True

    def search(self, name):
        for item in self.items:
            if item.name.lower() == name.lower():
                return item

        return None

    def update_quantity(self, name, qty):
        item = self.search(name)

        if item:
            return item.restock(qty)

        return False

    def display_all(self):
        if not self.items:
            print("Inventory is empty.")
            return

        for item in self.items:
            item.display()
            print("------------------------")

    def total_inventory_value(self):
        total = 0

        for item in self.items:
            total += item.total_value()

        return total