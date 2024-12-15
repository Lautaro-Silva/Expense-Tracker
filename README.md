# Stock Control Manager
A simple desktop app to manage inventory, track prices, and explore stock data.
This is a personal coding project I worked on because I enjoy building small tools, and a couple of friends suggested I create something like this. It’s still a work in progress, but I thought it was worth sharing.

# Features (so far)
- Add Stock: Enter new items into the inventory with details like name, size, price, and quantity.
- Update Stock:
  - Adjust availability of existing items.
  - Change prices dynamically through a simple interface.
- Search Stock: Filter and view stock details quickly.
- Undo Functionality: Roll back recent actions (still under development).
- View Available Items: A detailed list of currently available stock items with a basic text-based UI.
- Logging function: To view past changes of stock

# Planned Features
- Add low-stock alerts.
- Add visual data (like bar charts) to see trends or stock composition.
- Implement role-based access for admins and viewers.
- A more polished interface.

# What's inside the code
This project is written in Python and uses the following libraries:
- ````tkinter````: For the graphical user interface.
- ````csv````: To handle inventory data storage.
- ````logging````: For basic debugging and tracking actions.
- ````scrolledtext````: For the stock viewer's text area.

The main features are organized into classes, such as:
- ````StockManager````: Handles adding new items to stock.
- ````StockPriceUpdater````: Allows updating prices for existing items.
- ````StockViewer````: Lets you browse and search for available stock.

There are also many safety checks baked inside the code so that the functions are polished and not prone to errors.

# Why I made this
I’ve always enjoyed coding small projects to make repetitive tasks easier. A couple of friends needed a way to manage and track their stock, so I thought, "Why not make something for them?" It was a fun challenge to design a functional, interactive app with Python.
I learned a lot while working on this, and there's still more I want to add as I refine it.

This project is far from finished! Some parts need improvement, and some features are half-baked. But hey, that's part of the journey. If you have suggestions or feedback, feel free to share them. :)

# What's next?
Here’s what I plan to work on in future updates:

- Add role-based user management (Admin vs. Viewer access).
- Save and load inventory from more robust formats (e.g., SQLite or JSON).
- Add data visualization for stock trends.
- Implement better undo/redo logic.

# Contributing
This is more of a personal project than a professional one, but if you want to play around with the code or suggest improvements, feel free to fork the repo and submit a pull request.
