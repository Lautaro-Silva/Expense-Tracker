import csv
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from fuzzywuzzy import process
import logging

# Set up logging configuration
logging.basicConfig(filename='stock_control.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


# Helper function for reading stock from CSV
def read_stock_from_csv(filename):
    stock = []
    try:
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                stock.append(row)
    except FileNotFoundError:
        messagebox.showerror("Error", f"Stock file '{filename}' not found.")
    return stock


# Helper function for writing stock to CSV
def write_stock_to_csv(filename, stock_items):
    try:
        with open(filename, mode='w', newline='') as file:
            fieldnames = ['name', 'quantity', 'price', 'size', 'availability']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(stock_items)
    except IOError:
        messagebox.showerror("Error", f"Failed to write to file '{filename}'.")


# Helper function for centering a window
def center_window(window, width=400, height=300):
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')


class StockManager:
    FILENAME = "stock.csv"

    def __init__(self, main_menu_callback):
        """Initialize the StockManager class."""
        self.main_menu_callback = main_menu_callback
        self.root = tk.Tk()
        self.root.title("Stock Control - Add Stock")

        # Set window size and center it
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        center_window(self.root)

        # Read existing stock data
        self.stock_items = read_stock_from_csv(self.FILENAME)
        sizes = ["XS", "S", "M", "L", "XL"]

        # Entry for item name
        tk.Label(self.root, text="Item Name", font=("Arial", 12)).grid(row=0, column=0, padx=20, pady=10, sticky='e')
        self.name_var = tk.StringVar()
        tk.Entry(self.root, textvariable=self.name_var, font=("Arial", 12)).grid(row=0, column=1, padx=20, pady=10)

        # Dropdown to select size
        tk.Label(self.root, text="Select Size", font=("Arial", 12)).grid(row=1, column=0, padx=20, pady=10, sticky='e')
        self.size_dropdown = ttk.Combobox(self.root, values=sizes, font=("Arial", 12))
        self.size_dropdown.grid(row=1, column=1, padx=20, pady=10)

        # Entry for price
        tk.Label(self.root, text="Price", font=("Arial", 12)).grid(row=2, column=0, padx=20, pady=10, sticky='e')
        self.price_var = tk.StringVar()
        tk.Entry(self.root, textvariable=self.price_var, font=("Arial", 12)).grid(row=2, column=1, padx=20, pady=10)

        # Entry for quantity
        tk.Label(self.root, text="Quantity", font=("Arial", 12)).grid(row=3, column=0, padx=20, pady=10, sticky='e')
        self.quantity_var = tk.StringVar()
        tk.Entry(self.root, textvariable=self.quantity_var, font=("Arial", 12)).grid(row=3, column=1, padx=20, pady=10)

        # Button to add stock
        tk.Button(self.root, text="Add Stock", command=self.add_stock, font=("Arial", 12)).grid(row=4, column=0,
                                                                                                columnspan=2, pady=20)

        # Button to return to main menu
        tk.Button(self.root, text="Back to Main Menu", command=self.go_back, font=("Arial", 12)).grid(row=5, column=0,
                                                                                                      columnspan=2,
                                                                                                      pady=10)

    def validate_inputs(self):
        """Validate the input fields."""
        name = self.name_var.get().strip()
        size = self.size_dropdown.get()
        price = self.price_var.get().strip()
        quantity = self.quantity_var.get().strip()

        if not name:
            return False, "Item name cannot be empty."
        if not size:
            return False, "Size must be selected."
        if not price or not price.replace('.', '', 1).isdigit() or float(price) <= 0:
            return False, "Price must be a positive number."
        if not quantity.isdigit() or int(quantity) <= 0:
            return False, "Quantity must be a positive integer."

        return True, ""

    def item_exists(self, name, size):
        """Check if an item with the same name and size already exists."""
        return any(item['name'] == name and item['size'] == size for item in self.stock_items)

    def find_similar_item(self, name):
        """Find similar item names using fuzzy matching."""
        names = [item['name'] for item in self.stock_items]
        return process.extractOne(name, names, score_cutoff=85)

    def prompt_user(self, suggested_name, size):
        """Prompt the user to confirm if the suggested item is what they meant."""
        response = messagebox.askyesno(
            "Similar Item Found",
            f"An item with a similar name '{suggested_name}' and size '{size}' already exists. "
            "Did you mean this item? If yes, please go to 'Update Availability'. If no, you can add it anyway."
        )
        return response

    def add_stock(self):
        """Add a new stock item."""
        is_valid, message = self.validate_inputs()
        if not is_valid:
            messagebox.showerror("Error", message)
            return

        name = self.name_var.get().strip()
        size = self.size_dropdown.get()
        price = float(self.price_var.get().strip())
        quantity = int(self.quantity_var.get().strip())

        similar_item = self.find_similar_item(name)
        if similar_item:
            suggested_name = similar_item[0]
            if self.item_exists(suggested_name, size):
                if self.prompt_user(suggested_name, size):
                    # User chose "Yes", indicate to update availability
                    logging.info(f"User chose to update availability for similar item '{suggested_name}' ({size}).")
                    messagebox.showinfo("Information", "Please go to 'Update Availability' to modify this item.")
                    return
                else:
                    # User chose "No", continue to add the item anyway
                    pass  # Continue with adding the stock item

        # Add new stock item
        new_item = {'name': name, 'quantity': str(quantity), 'price': str(price), 'size': size,
                    'availability': "1" if quantity > 0 else "0"}
        self.stock_items.append(new_item)

        # Write updated stock data back to CSV
        write_stock_to_csv(self.FILENAME, self.stock_items)
        logging.info(f"Added new stock item: {name} ({size}) with quantity {quantity} and price ${price}.")
        messagebox.showinfo("Success", f"Added new stock item: {name} ({size}).")

    def go_back(self):
        """Close the current window and return to the main menu."""
        self.root.destroy()
        self.main_menu_callback()

    def run(self):
        """Run the StockManager."""
        self.root.mainloop()


class StockAvailabilityUpdater:
    FILENAME = "stock.csv"

    def __init__(self, main_menu_callback):
        """Initialize the StockAvailabilityUpdater class."""
        self.main_menu_callback = main_menu_callback
        self.root = tk.Tk()
        self.root.title("Stock Control - Update Quantity")

        # Set window size and center it
        center_window(self.root)

        # Read existing stock data
        self.stock_items = read_stock_from_csv(self.FILENAME)
        item_names = list(set(item['name'] for item in self.stock_items))  # Unique item names

        # Dropdown to select stock item
        tk.Label(self.root, text="Select Item", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.item_dropdown = ttk.Combobox(self.root, values=item_names, font=("Arial", 12))
        self.item_dropdown.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.item_dropdown.bind("<<ComboboxSelected>>", self.update_size_dropdown)

        # Dropdown to select size
        tk.Label(self.root, text="Select Size", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.size_dropdown = ttk.Combobox(self.root, values=[], font=("Arial", 12))
        self.size_dropdown.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Dropdown to select operation
        tk.Label(self.root, text="Operation", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.operation_var = tk.StringVar(value="Add Copies")
        self.operation_dropdown = ttk.Combobox(self.root, textvariable=self.operation_var,
                                               values=["Add Copies", "Sell Copies"], font=("Arial", 12))
        self.operation_dropdown.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Entry to set quantity
        tk.Label(self.root, text="Quantity", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.quantity_var = tk.StringVar()
        tk.Entry(self.root, textvariable=self.quantity_var, font=("Arial", 12)).grid(row=3, column=1, padx=10, pady=10,
                                                                                     sticky="w")

        # Button to update quantity
        tk.Button(self.root, text="Update Quantity", command=self.update_quantity, font=("Arial", 12), width=20).grid(
            row=4, column=0, columnspan=2, pady=20)

        # Button to return to main menu
        tk.Button(self.root, text="Back to Main Menu", command=self.go_back, font=("Arial", 12), width=20).grid(row=5,
                                                                                                                column=0,
                                                                                                                columnspan=2,
                                                                                                                pady=10)

    def update_size_dropdown(self, event):
        """Update the size dropdown based on the selected item."""
        selected_item = self.item_dropdown.get()
        sizes = [item['size'] for item in self.stock_items if item['name'] == selected_item]
        self.size_dropdown.config(values=sizes)
        self.size_dropdown.set("")  # Clear the selection

    def validate_inputs(self):
        """Validate the input fields."""
        item_name = self.item_dropdown.get()
        size = self.size_dropdown.get()
        quantity = self.quantity_var.get().strip()
        operation = self.operation_var.get()

        if not item_name:
            return False, "No item selected."
        if not size:
            return False, "No size selected."
        if not quantity.isdigit() or int(quantity) <= 0:
            return False, "Quantity must be a positive integer."
        if operation not in ["Add Copies", "Sell Copies"]:
            return False, "Invalid operation selected."

        return True, ""

    def update_quantity(self):
        """Update the quantity of the selected stock item."""
        is_valid, message = self.validate_inputs()
        if not is_valid:
            messagebox.showerror("Error", message)
            return

        item_name = self.item_dropdown.get()
        size = self.size_dropdown.get()
        quantity = int(self.quantity_var.get().strip())
        operation = self.operation_var.get()

        # Update quantity based on operation
        updated = False
        for row in self.stock_items:
            if row['name'] == item_name and row['size'] == size:
                current_quantity = int(row['quantity'])
                if operation == "Add Copies":
                    new_quantity = current_quantity + quantity
                    row['quantity'] = str(new_quantity)
                    # Set availability to 1 if quantity is greater than 0
                    if new_quantity > 0:
                        row['availability'] = "1"
                    logging.info(f"Added {quantity} copies to '{item_name}' ({size}). New quantity: {new_quantity}.")
                elif operation == "Sell Copies":
                    if quantity > current_quantity:
                        messagebox.showerror("Error", "Not enough copies available for this transaction.")
                        return
                    new_quantity = current_quantity - quantity
                    row['quantity'] = str(new_quantity)
                    # Set availability to 0 if quantity reaches 0
                    if new_quantity <= 0:
                        row['quantity'] = "0"
                        row['availability'] = "0"
                    logging.info(f"Sold {quantity} copies of '{item_name}' ({size}). New quantity: {new_quantity}.")
                updated = True
                break  # Exit loop after updating

        if updated:
            write_stock_to_csv(self.FILENAME, self.stock_items)
            messagebox.showinfo("Success", f"Updated quantity for {item_name} ({size}).")
        else:
            messagebox.showwarning("Warning", "Selected item and size not found or no updates made.")

    def go_back(self):
        """Close the current window and return to the main menu."""
        self.root.destroy()
        self.main_menu_callback()

    def run(self):
        """Run the StockAvailabilityUpdater."""
        self.root.mainloop()


class StockPriceUpdater:
    FILENAME = "stock.csv"

    def __init__(self, main_menu_callback):
        """Initialize the StockPriceUpdater class."""
        self.main_menu_callback = main_menu_callback
        self.root = tk.Tk()
        self.root.title("Stock Control - Update Price")

        # Set window size and center it
        center_window(self.root, width=400, height=250)
        self.root.resizable(False, False)

        # Read existing stock data
        self.stock_items = read_stock_from_csv(self.FILENAME)
        item_names = list(set(item['name'] for item in self.stock_items))  # Unique item names

        # Dropdown to select stock item
        tk.Label(self.root, text="Select Item", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.item_dropdown = ttk.Combobox(self.root, values=item_names, font=("Arial", 12))
        self.item_dropdown.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.item_dropdown.bind("<<ComboboxSelected>>", self.update_size_dropdown)

        # Dropdown to select size
        tk.Label(self.root, text="Select Size", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.size_dropdown = ttk.Combobox(self.root, values=[], font=("Arial", 12))
        self.size_dropdown.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Entry to set new price
        tk.Label(self.root, text="New Price", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.price_var = tk.StringVar()
        tk.Entry(self.root, textvariable=self.price_var, font=("Arial", 12)).grid(row=2, column=1, padx=10, pady=10,
                                                                                  sticky="w")

        # Button to update price
        tk.Button(self.root, text="Update Price", command=self.update_price, font=("Arial", 12), width=20).grid(row=3,
                                                                                                                column=0,
                                                                                                                columnspan=2,
                                                                                                                pady=20)

        # Button to return to main menu
        tk.Button(self.root, text="Back to Main Menu", command=self.go_back, font=("Arial", 12), width=20).grid(row=4,
                                                                                                                column=0,
                                                                                                                columnspan=2,
                                                                                                                pady=10)

    def update_size_dropdown(self, event):
        """Update the size dropdown based on the selected item."""
        selected_item = self.item_dropdown.get()
        sizes = [item['size'] for item in self.stock_items if item['name'] == selected_item]
        self.size_dropdown.config(values=sizes)
        self.size_dropdown.set("")  # Clear the selection

    def validate_inputs(self):
        """Validate the input fields."""
        item_name = self.item_dropdown.get()
        size = self.size_dropdown.get()
        price = self.price_var.get().strip()

        if not item_name:
            return False, "No item selected."
        if not size:
            return False, "No size selected."
        if not price or not price.replace('.', '', 1).isdigit() or float(price) <= 0:
            return False, "Price must be a positive number."

        return True, ""

    def update_price(self):
        """Update the price of the selected stock item."""
        is_valid, message = self.validate_inputs()
        if not is_valid:
            messagebox.showerror("Error", message)
            return

        item_name = self.item_dropdown.get()
        size = self.size_dropdown.get()
        new_price = float(self.price_var.get().strip())

        # Update price for the selected item and size
        updated = False
        for row in self.stock_items:
            if row['name'] == item_name and row['size'] == size:
                row['price'] = str(new_price)
                updated = True
                logging.info(f"Updated price for '{item_name}' ({size}) to ${new_price}.")
                break  # Exit loop after updating

        if updated:
            write_stock_to_csv(self.FILENAME, self.stock_items)
            messagebox.showinfo("Success", f"Updated price for {item_name} ({size}).")
        else:
            messagebox.showwarning("Warning", "Selected item and size not found or no updates made.")

    def go_back(self):
        """Close the current window and return to the main menu."""
        self.root.destroy()
        self.main_menu_callback()

    def run(self):
        """Run the StockPriceUpdater."""
        self.root.mainloop()


class StockViewer:
    FILENAME = "stock.csv"

    def __init__(self, main_menu_callback):
        """Initialize the StockViewer class."""
        self.main_menu_callback = main_menu_callback
        self.root = tk.Tk()
        self.root.title("Stock Control - View Available Items")

        # Frame for the main content
        content_frame = tk.Frame(self.root, padx=10, pady=10)
        content_frame.pack(expand=True, fill=tk.BOTH)

        # Header Label
        tk.Label(content_frame, text="Available Items", font=("Helvetica", 16, "bold")).pack(pady=5)

        # Search functionality
        search_frame = tk.Frame(content_frame)
        search_frame.pack(pady=10, fill=tk.X)
        tk.Label(search_frame, text="Search:", font=("Helvetica", 12)).pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=("Helvetica", 12))
        self.search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        tk.Button(search_frame, text="Search", command=self.search_stock, font=("Helvetica", 12)).pack(side=tk.RIGHT)

        # ScrolledText for displaying items
        self.text_area = scrolledtext.ScrolledText(content_frame, wrap=tk.WORD, width=80, height=20,
                                                   font=("Helvetica", 12))
        self.text_area.pack(expand=True, fill=tk.BOTH)

        # Undo functionality
        self.undo_button = tk.Button(content_frame, text="Undo", command=self.undo, font=("Helvetica", 12))
        self.undo_button.pack(pady=10)

        # Back to Main Menu Button
        tk.Button(content_frame, text="Back to Main Menu", command=self.go_back, font=("Helvetica", 12)).pack(pady=10)

        # Undo history
        self.undo_history = []

        # Load and display stock data
        self.display_stock()

    def read_stock(self):
        """Read stock from the CSV file."""
        stock_list = []
        try:
            with open(self.FILENAME, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    stock_list.append(row)
        except FileNotFoundError:
            messagebox.showerror("Error", "Stock file not found.")
        return stock_list

    def search_stock(self):
        """Filter and display stock items based on search query."""
        search_term = self.search_var.get().strip().lower()
        stock_items = self.read_stock()
        filtered_items = [item for item in stock_items if search_term in item['name'].lower()]

        if not filtered_items:
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, "No matching items found.\n")
            return

        self.text_area.delete(1.0, tk.END)
        for item in filtered_items:
            display_text = (f"Name: {item['name']}\nQuantity: {item['quantity']}\nPrice: ${item['price']}\n"
                            f"Size: {item['size']}\n")
            display_text += "-" * 40 + "\n"
            self.text_area.insert(tk.END, display_text)

    def display_stock(self):
        """Display available stock items in the text area."""
        available_items = [item for item in self.read_stock() if item['availability'] == "1"]

        if not available_items:
            self.text_area.insert(tk.END, "No available items in stock.\n")
            return

        self.text_area.delete(1.0, tk.END)
        for item in available_items:
            display_text = (f"Name: {item['name']}\nQuantity: {item['quantity']}\nPrice: ${item['price']}\n"
                            f"Size: {item['size']}\n")
            display_text += "-" * 40 + "\n"
            self.text_area.insert(tk.END, display_text)

    def undo(self):
        """Undo the last action."""
        if not self.undo_history:
            messagebox.showinfo("Info", "No actions to undo.")
            return

        last_action = self.undo_history.pop()
        # Here you should implement logic to revert the last action.
        # This depends on how you manage actions and state.

        messagebox.showinfo("Undo", f"Undone action: {last_action}")

    def go_back(self):
        """Close the current window and return to the main menu."""
        self.root.destroy()
        self.main_menu_callback()

    def run(self):
        """Run the StockViewer."""
        self.root.mainloop()


def main_menu():
    """Main program to choose between adding stock, updating stock, and viewing available items."""

    def open_add_stock():
        main_menu_window.destroy()
        manager = StockManager(main_menu)
        manager.run()

    def open_update_availability():
        main_menu_window.destroy()
        updater = StockAvailabilityUpdater(main_menu)
        updater.run()

    def open_update_price():
        main_menu_window.destroy()
        updater = StockPriceUpdater(main_menu)
        updater.run()

    def open_view_stock():
        main_menu_window.destroy()
        viewer = StockViewer(main_menu)
        viewer.run()

    # Create the main menu window
    global main_menu_window
    main_menu_window = tk.Tk()
    main_menu_window.title("Stock Control - Main Menu")

    # Set window size and center it
    main_menu_window.geometry("400x300")
    main_menu_window.resizable(False, False)
    center_window(main_menu_window)

    # Create and style the label
    tk.Label(main_menu_window, text="Choose an action:", font=("Arial", 14)).pack(pady=20)

    # Create and style buttons
    button_options = [
        ("Add Stock", open_add_stock),
        ("Update Availability", open_update_availability),
        ("Update Price", open_update_price),
        ("View Available Items", open_view_stock)
    ]

    for text, command in button_options:
        tk.Button(main_menu_window, text=text, command=command, font=("Arial", 12), width=25).pack(pady=10)

    main_menu_window.mainloop()


if __name__ == "__main__":
    main_menu()
