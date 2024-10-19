from datetime import datetime

class MenuItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.is_available = True
    def mark_as_available(self):
        self.is_available = True
    def mark_as_unavailable(self):
        self.is_available = False
    def __repr__(self):
        return f"The {self.name} dish costs ${self.price}"
    
class Order:
    def __init__(self, order_number, items, total_amount):
        self.order_number = order_number
        self.items = []
        self.total_amount = 0
    def add_item(self, menu_item):
        self.items.append(menu_item)
        self.calculate_total()
    def remove_item(self, menu_item):
        for i in self.items:
            if menu_item == i:
                self.items.remove(i)
                self.calculate_total()
        raise Exception(f"Item {menu_item.name} not found in the order.")
    def calculate_total(self):
       self.total_amount = sum(item.price for item in self.items)
    def __repr__(self):
        return f"Order #{self.order_number}, Total Amount: {self.total_amount}, Items: {[item.name for item in self.items]}"
    
class Table:
    def __init__(self, table_number, seats):
        self.table_number = table_number
        self.seats = seats
        self.is_reserved = True
    def reserve(self):
        self.is_reserved = False
        return f"This {self.table_number} with {self.seats} is Reserved."
    def free(self):
        self.is_reserved = True
        return f"This {self.table_number} with {self.seats} is free!."
    def __repr__(self):
        status = "Reserved" if self.is_reserved else "Available"
        return f"Table {self.table_number} : {self.seats} seats, status : {status}."
    
class Reservation:
    def __init__(self, customer_name, table, reservation_time = None):
        self.customer_name = customer_name
        self.table = table
        self.reservation_time = reservation_time or datetime.now()
    def __repr__(self):
        return (f"Reservation for {self.customer_name} at Table {self.table.table_number} "
                f"with {self.table.seats} seats on {self.reservation_time.strftime('%Y-%m-%d %H:%M:%S')}.")
    
class Restaurant:
    def __init__(self):
        self.menu = []
        self.orders = []
        self.tables = []
        self.reservation = []
    def add_menu_item(self, menu_item):
        self.menu.append(menu_item)
    def remove_menu_item(self, item_name):
        for item in self.menu:
            if item.name == item_name:
                self.menu.remove(item)
                return f"{item_name} has been removed from the menu"
        raise Exception(f"Menu item is not found")
    def take_order(self, order):
        self.orders.append(order)
    def list_orders(self):
        if not self.orders:
            return "No current orders."
        return [f"Order #{order.order_number}: {len(order.items)} items, Total: {order.total_amount}" for order in self.orders]
    def reserve_table(self, customer_name, table_number, reservation_time):
        for table in self.tables:
            if table.table_number == table_number:
                raise Exception(f"Table {table_number} is already reserved.")
            reservation = Reservation(customer_name, table, reservation_time)
            table.reserve()
            self.reservations.append(reservation)
            return "Reservation for {customer_name} at Table {table_number} is confirmed."
        raise Exception(f"Table {table_number} not found.")
    def list_reservations(self):
        if not self.reservations:
            return "No current reservations."
        return [str(reservation) for reservation in self.reservations]

    def add_table(self, table):
        self.tables.append(table)
        return f"Table {table.table_number} with {table.seats} seats has been added."

def main():
    restaurant = Restaurant()

    # Pre-populate some tables and menu items for demo purposes
    restaurant.add_table(Table(1, 4))
    restaurant.add_table(Table(2, 2))
    restaurant.add_menu_item(MenuItem("Burger", 10.99))
    restaurant.add_menu_item(MenuItem("Pasta", 12.99))

    while True:
        print("\nWelcome to the Restaurant Management System!")
        print("1. Add Menu Item")
        print("2. Remove Menu Item")
        print("3. Take Order")
        print("4. List Orders")
        print("5. Reserve Table")
        print("6. List Reservations")
        print("7. Exit")

        choice = input("Please choose an option (1-7): ")

        if choice == '1':
            name = input("Enter the name of the dish: ")
            price = float(input(f"Enter the price for {name}: "))
            menu_item = MenuItem(name, price)
            restaurant.add_menu_item(menu_item)
            print(f"{name} has been added to the menu.\n")

        elif choice == '2':
            name = input("Enter the name of the dish to remove: ")
            try:
                restaurant.remove_menu_item(name)
                print(f"{name} has been removed from the menu.\n")
            except Exception as e:
                print(f"Error: {e}\n")

        elif choice == '3':
            order_number = input("Enter the order number: ")
            order = Order(order_number, [], 0)
            while True:
                item_name = input("Enter the name of the item to add to the order (or type 'done' to finish): ")
                if item_name.lower() == 'done':
                    break
                # Find the item from the menu
                menu_item = next((item for item in restaurant.menu if item.name == item_name), None)
                if menu_item:
                    order.add_item(menu_item)
                    print(f"{item_name} has been added to the order.")
                else:
                    print(f"{item_name} is not available in the menu.")
            restaurant.take_order(order)
            print(f"Order #{order_number} has been placed.\n")

        elif choice == '4':
            orders = restaurant.list_orders()
            if orders:
                print("Current Orders:")
                for order in orders:
                    print(order)
            else:
                print("No orders have been placed yet.\n")

        elif choice == '5':
            customer_name = input("Enter the customer name: ")
            table_number = int(input("Enter the table number: "))
            reservation_time = input("Enter reservation time (YYYY-MM-DD HH:MM:SS) or leave blank for now: ")
            if reservation_time:
                reservation_time = datetime.strptime(reservation_time, "%Y-%m-%d %H:%M:%S")
            else:
                reservation_time = None

            try:
                restaurant.reserve_table(customer_name, table_number, reservation_time)
                print(f"Reservation for {customer_name} at Table {table_number} has been confirmed.\n")
            except Exception as e:
                print(f"Error: {e}\n")

        elif choice == '6':
            reservations = restaurant.list_reservations()
            if reservations:
                print("Current Reservations:")
                for reservation in reservations:
                    print(reservation)
            else:
                print("No reservations have been made yet.\n")

        elif choice == '7':
            print("Thank you for using the Restaurant Management System!")
            break

        else:
            print("Invalid option. Please choose a valid number (1-7).\n")


if __name__ == "__main__":
    main()
