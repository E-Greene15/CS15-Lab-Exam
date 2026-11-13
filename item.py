class Item:
    def __init__(self, name, quantity, price):
        if quantity < 0 or price < 0:
            raise ValueError("Quantity and price cannot be negative.")

        self.name = name
        self.__quantity = quantity
        self.__price = price

    def restock(self, qty):
        if qty <= 0:
            print("Please enter a positive quantity.")
            return False

        self.__quantity += qty
        return True

    def sell(self, qty):
        if qty <= 0:
            print("Please enter a positive quantity.")
            return False

        if qty > self.__quantity:
            return False

        self.__quantity -= qty
        return True

    def get_quantity(self):
        return self.__quantity

    def get_price(self):
        return self.__price

    def total_value(self):
        return self.__quantity * self.__price

    def display(self):
        print(f"Item: {self.name}")
        print(f"Quantity: {self.__quantity}")
        print(f"Price: PHP {self.__price:.2f}")
        print(f"Total Value: PHP {self.total_value():.2f}")


class PerishableItem(Item):
    def __init__(self, name, quantity, price, days_until_expiry):
        super().__init__(name, quantity, price)

        if days_until_expiry < 0:
            raise ValueError("Expiry days cannot be negative.")

        self.days_until_expiry = days_until_expiry

    def is_expiring_soon(self):
        return self.days_until_expiry <= 3

    def total_value(self):
        value = super().total_value()

        if self.is_expiring_soon():
            return value * 0.50

        return value

    def display(self):
        super().display()
        print(f"Days until expiry: {self.days_until_expiry}")


class ElectronicItem(Item):
    def __init__(self, name, quantity, price, warranty_months):
        super().__init__(name, quantity, price)

        if warranty_months < 0:
            raise ValueError("Warranty cannot be negative.")

        self.warranty_months = warranty_months

    def display(self):
        super().display()
        print(f"Warranty: {self.warranty_months} months")