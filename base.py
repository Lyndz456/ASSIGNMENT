from abc import ABC, abstractmethod

# Product class
class Product:
    def __init__(self, productID, productName, productPrice, quantity):
        self.__productID = productID
        self.__productName = productName
        self.__productPrice = productPrice
        self.__quantity = quantity

    def get_productID(self):
        return self.__productID

    def get_productName(self):
        return self.__productName

    def get_productPrice(self):
        return self.__productPrice

    def get_quantity(self):
        return self.__quantity

    def set_quantity(self, quantity):
        self.__quantity = quantity

    def get_details(self):
        return (f"Product ID: {self.__productID}, Name: {self.__productName}, "
                f"Price: {self.__productPrice}, Quantity: {self.__quantity}")


# Collection of Products
class ProductCollection:
    def __init__(self):
        self.items = []

    def add_product(self, product, quantity):
        for item in self.items:
            if item["product"].get_productID() == product.get_productID():
                item["quantity"] += quantity
                print(f"Updated {product.get_productName()} quantity to {item['quantity']}.")
                return
        self.items.append({"product": product, "quantity": quantity})
        print(f"Added {product.get_productName()} to the collection.")

    def remove_product(self, productID):
        for item in self.items:
            if item["product"].get_productID() == productID:
                self.items.remove(item)
                print(f"Removed {item['product'].get_productName()} from the collection.")
                return
        print(f"Product with ID {productID} not found in collection.")

    def view_products(self):
        if not self.items:
            print("The collection is empty.")
        else:
            for item in self.items:
                product = item["product"]
                quantity = item["quantity"]
                print(f"{product.get_details()}, Quantity in Collection: {quantity}")

    def calculate_total(self):
        return sum(item["product"].get_productPrice() * item["quantity"] for item in self.items)


# Order Class
class Order:
    def __init__(self, orderID, product_collection):
        self.__orderID = orderID
        self.product_collection = product_collection
        self.__status = "Pending"

    def get_order_details(self):
        print(f"Order ID: {self.__orderID}, Status: {self.__status}")
        self.product_collection.view_products()
        print(f"Total Price: {self.product_collection.calculate_total()}")

    def complete_order(self):
        if not self.product_collection.items:
            print("Cannot complete the order. The product collection is empty.")
        else:
            self.__status = "Completed"
            print(f"Order {self.__orderID} is now marked as Completed.")

    def cancel_order(self):
        self.__status = "Cancelled"
        print(f"Order {self.__orderID} has been cancelled.")

    def get_orderID(self):
        return self.__orderID

    def get_status(self):
        return self.__status


# Abstract User Class
class User(ABC):
    def __init__(self, userID, name, email):
        self.__userID = userID
        self.__name = name
        self.__email = email

    @abstractmethod
    def view_profile(self):
        pass

    def get_userID(self):
        return self.__userID

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def set_email(self, email):
        self.__email = email


# Customer Class
class Customer(User):
    def __init__(self, customerID, name, email):
        super().__init__(customerID, name, email)
        self.__orders = []

    def add_order(self, order):
        self.__orders.append(order)
        print(f"Order {order.get_orderID()} has been added for customer {self.get_name()}.")

    def view_orders(self):
        if not self.__orders:
            print(f"{self.get_name()} has no orders.")
            return []
        else:
            print(f"Orders for {self.get_name()}:")
            for order in self.__orders:
                order.get_order_details()
            return self.__orders

    def view_profile(self):
        print(f"Customer Profile - ID: {self.get_userID()}, Name: {self.get_name()}, Email: {self.get_email()}")

    def view_order_history(self):
        if not self.__orders:
            print(f"{self.get_name()} has no order history.")
        else:
            print(f"Order History for {self.get_name()}:")
            for order in self.__orders:
                order.get_order_details()


# Shopping System Class
class ShoppingSystem:
    def __init__(self):
        self.customers = {}
        self.products = {}

    def add_product(self, product):
        self.products[product.get_productID()] = product
        print(f"Product {product.get_productName()} added to the system.")

    def add_customer(self, customer):
        self.customers[customer.get_userID()] = customer
        print(f"Customer {customer.get_name()} added to the system.")

    def create_order(self, customerID, product_ids_quantities):
        if customerID not in self.customers:
            print("Customer not found.")
            return

        product_collection = ProductCollection()
        for productID, quantity in product_ids_quantities:
            if productID in self.products:
                product_collection.add_product(self.products[productID], quantity)
            else:
                print(f"Product ID {productID} not found in the system.")

        order = Order(len(self.customers[customerID].view_orders()) + 1, product_collection)
        self.customers[customerID].add_order(order)
        print(f"Order {order.get_orderID()} created for customer {customerID}.")

    def view_customer_orders(self, customerID):
        if customerID in self.customers:
            self.customers[customerID].view_orders()
        else:
            print("Customer not found.")

# Function to add products
def add_products(system):
    while True:
        try:
            productID = int(input("Enter Product ID: "))
            productName = input("Enter Product Name: ")
            productPrice = float(input("Enter Product Price: "))
            quantity = int(input("Enter Product Quantity: "))
            
            if productPrice < 0 or quantity < 0:
                print("Price and quantity must be non-negative values.")
                continue
            
            product = Product(productID, productName, productPrice, quantity)
            system.add_product(product)
        except ValueError:
            print("Invalid input. Please enter valid values.")
        
        another = input("Do you want to add another product? (yes/no): ").strip().lower()
        if another != 'yes':
            break

# Function to add customers
def add_customers(system):
    while True:
        customerID = input("Enter Customer ID: ")
        name = input("Enter Customer Name: ")
        email = input("Enter Customer Email: ")
        
        customer = Customer(customerID, name, email)
        system.add_customer(customer)

        another = input("Do you want to add another customer? (yes/no): ").strip().lower()
        if another != 'yes':
            break

# Function to create an order
def create_order(system):
    while True:
        customerID = input("Enter Customer ID for the order: ")
        product_ids_quantities = []
        
        while True:
            productID = input("Enter Product ID to add to the order: ")
            quantity = input("Enter Quantity: ")
            
            try:
                quantity = int(quantity)
                if quantity <= 0:
                    print("Quantity must be a positive integer.")
                    continue
                product_ids_quantities.append((productID, quantity))
            except ValueError:
                print("Invalid quantity. Please enter a positive integer.")
                continue

            another = input("Do you want to add another product to this order? (yes/no): ").strip().lower()
            if another != 'yes':
                break

        system.create_order(customerID, product_ids_quantities)

        another = input("Do you want to create another order? (yes/no): ").strip().lower()
        if another != 'yes':
            break

# Function to view a customer's orders
def view_orders(system):
    customerID = input("Enter Customer ID to view orders: ")
    system.view_customer_orders(customerID)

# Function to view order history
def view_order_history(system):
    customerID = input("Enter Customer ID to view order history: ")
    if customerID in system.customers:
        system.customers[customerID].view_order_history()
    else:
        print("Customer not found.")

# Main interactive loop for the shopping system
def main():
    system = ShoppingSystem()
    while True:
        print("\nShopping System")
        print("1. Add Product")
        print("2. Add Customer")
        print("3. Create Order")
        print("4. View Customer Orders")
        print("5. View Order History")
        print("6. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            add_products(system)
        elif choice == '2':
            add_customers(system)
        elif choice == '3':
            create_order(system)
        elif choice == '4':
            view_orders(system)
        elif choice == '5':
            view_order_history(system)
        elif choice == '6':
            print("Exiting the Shopping System.")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the main function to start the shopping system
if __name__ == "__main__":
    main()
