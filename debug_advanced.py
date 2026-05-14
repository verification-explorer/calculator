"""Advanced Debug Console learning."""


class ShoppingCart:
    def __init__(self):
        self.items = []
        self._discount = 0.1  # private attribute

    def add_item(self, name, price, quantity=1):
        item = {"name": name, "price": price, "qty": quantity}
        self.items.append(item)
        return item

    def get_total(self):
        subtotal = sum(item["price"] * item["qty"] for item in self.items)
        return subtotal * (1 - self._discount)

    def __repr__(self):
        return f"ShoppingCart({len(self.items)} items)"


def process_order(cart, customer):
    """Process an order - set breakpoint on line 25."""
    total = cart.get_total()

    order = {
        "customer": customer,
        "items": cart.items,
        "total": total,
        "status": "pending"
    }

    print(f"Order for {customer}: ${total:.2f}")
    return order


def main():
    # Create cart with items
    cart = ShoppingCart()
    cart.add_item("Laptop", 999.99)
    cart.add_item("Mouse", 29.99, quantity=2)
    cart.add_item("Keyboard", 79.99)

    customer_name = "Alice"
    customer_email = "alice@example.com"

    # SET BREAKPOINT HERE (line 46)
    order = process_order(cart, customer_name)

    print(f"Order complete: {order['status']}")


if __name__ == "__main__":
    main()
