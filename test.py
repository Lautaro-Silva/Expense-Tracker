import csv
import tkinter as tk
from tkinter import messagebox

FILENAME = "test_stock.csv"

def read_stock():
    """Read stock from the CSV file."""
    with open(FILENAME, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        stock_list = list(reader)
    return stock_list

def add_stock():
    """Add a new stock item to the CSV file."""
    name = entry_name.get()
    quantity = entry_quantity.get()
    price = entry_price.get()
    size = entry_size.get()
    available = entry_available.get()

    try:
        with open(FILENAME, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, quantity, price, size, available])
        messagebox.showinfo("Success", "Stock added successfully!")
        entry_name.delete(0, tk.END)
        entry_quantity.delete(0, tk.END)
        entry_price.delete(0, tk.END)
        entry_size.delete(0, tk.END)
        entry_available.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the GUI
root = tk.Tk()
root.title("Stock Control - CSV Version")

# GUI elements
tk.Label(root, text="Name").grid(row=0, column=0)
tk.Label(root, text="Quantity").grid(row=1, column=0)
tk.Label(root, text="Price").grid(row=2, column=0)
tk.Label(root, text="Size").grid(row=3, column=0)
tk.Label(root, text="Available (1/0)").grid(row=4, column=0)

entry_name = tk.Entry(root)
entry_quantity = tk.Entry(root)
entry_price = tk.Entry(root)
entry_size = tk.Entry(root)
entry_available = tk.Entry(root)

entry_name.grid(row=0, column=1)
entry_quantity.grid(row=1, column=1)
entry_price.grid(row=2, column=1)
entry_size.grid(row=3, column=1)
entry_available.grid(row=4, column=1)

# Button to add stock
tk.Button(root, text="Add Stock", command=add_stock).grid(row=5, column=0, columnspan=2)

root.mainloop()
