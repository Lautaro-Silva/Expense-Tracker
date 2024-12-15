import csv
import tkinter as tk
from tkinter import ttk, messagebox

FILENAME = "test_stock.csv"

def read_stock():
    """Read stock from the CSV file."""
    stock_list = []
    with open(FILENAME, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            stock_list.append(row)
    return stock_list

def update_stock(selected_item, new_availability):
    """Update the availability of the selected stock item."""
    stock = read_stock()

    # Find and update the selected item
    for row in stock:
        if row[0] == selected_item:  # Assuming the item name is unique
            row[4] = new_availability

    # Write the updated stock back to the CSV
    with open(FILENAME, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['name', 'quantity', 'price', 'size', 'available'])  # Write header
        writer.writerows(stock)

    messagebox.showinfo("Success", f"Availability of {selected_item} updated to {new_availability}")

def update_availability():
    """Handle the update availability button click."""
    selected_item = dropdown.get()
    new_availability = availability_var.get()
    update_stock(selected_item, new_availability)

# Create the GUI
root = tk.Tk()
root.title("Stock Control - Update Availability")

# Read stock and create a dropdown for items
stock_items = read_stock()
item_names = [item[0] for item in stock_items]  # Get names of items for dropdown

tk.Label(root, text="Select Item").grid(row=0, column=0)
dropdown = ttk.Combobox(root, values=item_names)
dropdown.grid(row=0, column=1)

# Dropdown for availability (1 or 0)
tk.Label(root, text="Set Availability").grid(row=1, column=0)
availability_var = tk.StringVar()
availability_dropdown = ttk.Combobox(root, textvariable=availability_var, values=["1", "0"])
availability_dropdown.grid(row=1, column=1)

# Button to update availability
update_button = tk.Button(root, text="Update Availability", command=update_availability)
update_button.grid(row=2, column=0, columnspan=2)

root.mainloop()

