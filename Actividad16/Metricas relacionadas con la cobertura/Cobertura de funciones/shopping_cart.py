# shopping_cart.py

class Item:
    def __init__(self, name, price, quantity=1):
        if not isinstance(name, str):
            raise TypeError("El nombre del artículo debe ser una cadena.")
        if not isinstance(price, (int, float)):
            raise TypeError("El precio debe ser un número.")
        if price < 0:
            raise ValueError("El precio no puede ser negativo.")
        if not isinstance(quantity, int):
            raise TypeError("La cantidad debe ser un entero.")
        if quantity <= 0:
            raise ValueError("La cantidad debe ser al menos 1.")
        self.name = name
        self.price = price
        self.quantity = quantity

    def total_price(self):
        return self.price * self.quantity


class ShoppingCart:
    def __init__(self):
        self.items = {}
        self.applied_discount = 0

    def add_item(self, item):
        if not isinstance(item, Item):
            raise TypeError("Solo se pueden agregar instancias de Item.")
        if item.name in self.items:
            self.items[item.name].quantity += item.quantity
        else:
            self.items[item.name] = item

    def remove_item(self, item_name, quantity=1):
        if item_name not in self.items:
            raise ValueError("El artículo no existe en el carrito.")
        if not isinstance(quantity, int):
            raise TypeError("La cantidad debe ser un entero.")
        if quantity <= 0:
            raise ValueError("La cantidad debe ser al menos 1.")
        if self.items[item_name].quantity < quantity:
            raise ValueError("Cantidad a remover excede la cantidad en el carrito.")
        self.items[item_name].quantity -= quantity
        if self.items[item_name].quantity == 0:
            del self.items[item_name]

    def apply_discount(self, discount):
        if not isinstance(discount, (int, float)):
            raise TypeError("El descuento debe ser un número.")
        if not (0 <= discount <= 100):
            raise ValueError("El descuento debe estar entre 0 y 100.")
        self.applied_discount = discount

    def calculate_total(self):
        total = sum(item.total_price() for item in self.items.values())
        if self.applied_discount > 0:
            total -= total * (self.applied_discount / 100)
        return round(total, 2)

    def list_items(self):
        return [{
            'name': item.name,
            'price': item.price,
            'quantity': item.quantity,
            'total_price': item.total_price()
        } for item in self.items.values()]

    def clear_cart(self):
        self.items = {}
        self.applied_discount = 0

    def is_empty(self):
        return len(self.items) == 0