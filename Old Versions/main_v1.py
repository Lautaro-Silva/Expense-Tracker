import csv
import tkinter as tk
from tkinter import ttk, messagebox


class StockManager:
    FILENAME = "test_stock.csv"

    def __init__(self, main_menu_callback):
        """Initialize the StockManager class."""
        self.main_menu_callback = main_menu_callback
        self.root = tk.Tk()
        self.root.title("Stock Control - Add Stock")

        # GUI elements for adding stock
        tk.Label(self.root, text="Name").grid(row=0, column=0)
        tk.Label(self.root, text="Quantity").grid(row=1, column=0)
        tk.Label(self.root, text="Price").grid(row=2, column=0)
        tk.Label(self.root, text="Size").grid(row=3, column=0)
        tk.Label(self.root, text="Available (1/0)").grid(row=4, column=0)

        self.entry_name = tk.Entry(self.root)
        self.entry_quantity = tk.Entry(self.root)
        self.entry_price = tk.Entry(self.root)
        self.entry_size = tk.Entry(self.root)
        self.entry_available = tk.Entry(self.root)

        self.entry_name.grid(row=0, column=1)
        self.entry_quantity.grid(row=1, column=1)
        self.entry_price.grid(row=2, column=1)
        self.entry_size.grid(row=3, column=1)
        self.entry_available.grid(row=4, column=1)

        tk.Button(self.root, text="Add Stock", command=self.add_stock).grid(row=5, column=0, columnspan=2)
        tk.Button(self.root, text="Back to Main Menu", command=self.go_back).grid(row=6, column=0, columnspan=2)

    def add_stock(self):
        """Add a new stock item to the CSV file."""
        name = self.entry_name.get()
        quantity = self.entry_quantity.get()
        price = self.entry_price.get()
        size = self.entry_size.get()
        available = self.entry_available.get()

        try:
            with open(self.FILENAME, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([name, quantity, price, size, available])
            messagebox.showinfo("Success", "Stock added successfully!")
            self.clear_entries()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_entries(self):
        """Clear the input fields."""
        self.entry_name.delete(0, tk.END)
        self.entry_quantity.delete(0, tk.END)
        self.entry_price.delete(0, tk.END)
        self.entry_size.delete(0, tk.END)
        self.entry_available.delete(0, tk.END)

    def go_back(self):
        """Close the current window and return to the main menu."""
        self.root.destroy()
        self.main_menu_callback()

    def run(self):
        """Run the StockManager."""
        self.root.mainloop()


class StockViewer:
    FILENAME = "test_stock.csv"

    def __init__(self, main_menu_callback):
        """Initialize the StockViewer class."""
        self.main_menu_callback = main_menu_callback
        self.root = tk.Tk()
        self.root.title("Stock Control - Update Availability")

        # Read stock data
        self.stock_items = self.read_stock()
        item_names = [item[0] for item in self.stock_items]  # Get names of items for dropdown

        # Dropdown to select stock item
        tk.Label(self.root, text="Select Item").grid(row=0, column=0)
        self.dropdown = ttk.Combobox(self.root, values=item_names)
        self.dropdown.grid(row=0, column=1)

        # Dropdown to select availability
        tk.Label(self.root, text="Set Availability").grid(row=1, column=0)
        self.availability_var = tk.StringVar()
        self.availability_dropdown = ttk.Combobox(self.root, textvariable=self.availability_var, values=["1", "0"])
        self.availability_dropdown.grid(row=1, column=1)

        # Button to update availability
        tk.Button(self.root, text="Update Availability", command=self.update_availability).grid(row=2, column=0, columnspan=2)
        tk.Button(self.root, text="Back to Main Menu", command=self.go_back).grid(row=3, column=0, columnspan=2)

    def read_stock(self):
        """Read stock from the CSV file."""
        stock_list = []
        with open(self.FILENAME, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                stock_list.append(row)
        return stock_list

    def update_stock(self, selected_item, new_availability):
        """Update the availability of the selected stock item."""
        stock = self.read_stock()

        # Find and update the selected item
        for row in stock:
            if row[0] == selected_item:  # Assuming the item name is unique
                row[4] = new_availability

        # Write the updated stock back to the CSV
        with open(self.FILENAME, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['name', 'quantity', 'price', 'size', 'available'])  # Write header
            writer.writerows(stock)

        messagebox.showinfo("Success", f"Availability of {selected_item} updated to {new_availability}")

    def update_availability(self):
        """Handle the update availability button click."""
        selected_item = self.dropdown.get()
        new_availability = self.availability_var.get()
        self.update_stock(selected_item, new_availability)

    def go_back(self):
        """Close the current window and return to the main menu."""
        self.root.destroy()
        self.main_menu_callback()

    def run(self):
        """Run the StockViewer."""
        self.root.mainloop()


def main_menu():
    """Main program to choose between adding stock and updating availability."""
    def open_add_stock():
        main_menu_window.destroy()
        manager = StockManager(main_menu)
        manager.run()

    def open_view_stock():
        main_menu_window.destroy()
        viewer = StockViewer(main_menu)
        viewer.run()

    # Create the main menu window
    global main_menu_window
    main_menu_window = tk.Tk()
    main_menu_window.title("Stock Control - Main Menu")

    tk.Label(main_menu_window, text="Choose an action:").grid(row=0, column=0, columnspan=2)

    tk.Button(main_menu_window, text="Add Stock", command=open_add_stock).grid(row=1, column=0)
    tk.Button(main_menu_window, text="Update Availability", command=open_view_stock).grid(row=1, column=1)

    main_menu_window.mainloop()


if __name__ == "__main__":
    main_menu()
