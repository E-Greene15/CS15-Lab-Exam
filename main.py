
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from item import Item, PerishableItem, ElectronicItem
from inventory import Inventory


inventory = Inventory()


class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory System")
        self.root.geometry("950x600")
        self.root.minsize(750, 500)
        self.root.configure(bg="#F7F8FA")

        self.setup_style()
        self.create_header()
        self.create_summary()
        self.create_table()
        self.create_buttons()

        self.refresh_table()

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background="white",
            foreground="#333333",
            fieldbackground="white",
            rowheight=35,
            font=("Arial", 10),
            borderwidth=0
        )

        style.configure(
            "Treeview.Heading",
            background="#F0F1F3",
            foreground="#333333",
            font=("Arial", 10, "bold"),
            padding=10
        )

        style.map(
            "Treeview",
            background=[("selected", "#DCE8F8")],
            foreground=[("selected", "#222222")]
        )

    def create_header(self):
        header = tk.Frame(self.root, bg="#FFFFFF")
        header.pack(fill="x")

        tk.Label(
            header,
            text="Inventory System",
            font=("Arial", 21, "bold"),
            bg="white",
            fg="#222222"
        ).pack(anchor="w", padx=30, pady=(20, 3))

        tk.Label(
            header,
            text="Manage your items and stock in one place.",
            font=("Arial", 10),
            bg="white",
            fg="#777777"
        ).pack(anchor="w", padx=30, pady=(0, 20))

    def create_summary(self):
        summary = tk.Frame(self.root, bg="#F7F8FA")
        summary.pack(fill="x", padx=30, pady=20)

        self.item_count = self.create_summary_card(
            summary, "Total Items", "0"
        )

        self.stock_count = self.create_summary_card(
            summary, "Total Stock", "0"
        )

        self.total_value = self.create_summary_card(
            summary, "Total Value", "PHP 0.00"
        )

    def create_summary_card(self, parent, title, value):
        card = tk.Frame(
            parent,
            bg="white",
            highlightbackground="#E5E7EB",
            highlightthickness=1
        )
        card.pack(side="left", fill="both", expand=True, padx=5)

        tk.Label(
            card,
            text=title,
            font=("Arial", 10),
            bg="white",
            fg="#777777"
        ).pack(anchor="w", padx=15, pady=(12, 5))

        value_label = tk.Label(
            card,
            text=value,
            font=("Arial", 17, "bold"),
            bg="white",
            fg="#222222"
        )
        value_label.pack(anchor="w", padx=15, pady=(0, 12))

        return value_label

    def create_table(self):
        container = tk.Frame(self.root, bg="#F7F8FA")
        container.pack(fill="both", expand=True, padx=30)

        tk.Label(
            container,
            text="Inventory List",
            font=("Arial", 13, "bold"),
            bg="#F7F8FA",
            fg="#222222"
        ).pack(anchor="w", pady=(0, 10))

        columns = (
            "name", "type", "quantity",
            "price", "value", "details"
        )

        self.table = ttk.Treeview(
            container,
            columns=columns,
            show="headings"
        )

        headings = {
            "name": "Item Name",
            "type": "Type",
            "quantity": "Quantity",
            "price": "Price",
            "value": "Total Value",
            "details": "Details"
        }

        for column in columns:
            self.table.heading(
                column, text=headings[column]
            )

        self.table.column("name", width=150)
        self.table.column("type", width=110)
        self.table.column("quantity", width=80, anchor="center")
        self.table.column("price", width=110, anchor="center")
        self.table.column("value", width=120, anchor="center")
        self.table.column("details", width=150, anchor="center")

        scrollbar = ttk.Scrollbar(
            container,
            orient="vertical",
            command=self.table.yview
        )

        self.table.configure(
            yscrollcommand=scrollbar.set
        )

        self.table.pack(
            side="left", fill="both", expand=True
        )

        scrollbar.pack(side="right", fill="y")

    def create_buttons(self):
        button_area = tk.Frame(self.root, bg="#F7F8FA")
        button_area.pack(fill="x", padx=30, pady=20)

        buttons = [
            ("Add Item", self.add_item),
            ("Restock", self.restock_item),
            ("Sell", self.sell_item),
            ("Search", self.search_item),
            ("Display All", self.display_all),
            ("Total Value", self.show_total),
            ("Exit", self.exit_app)
        ]

        for text, command in buttons:
            tk.Button(
                button_area,
                text=text,
                command=command,
                font=("Arial", 9, "bold"),
                bg="#FFFFFF",
                fg="#333333",
                activebackground="#E8EDF5",
                relief="solid",
                bd=1,
                padx=10,
                pady=9,
                cursor="hand2"
            ).pack(side="left", padx=3, expand=True)

    def refresh_table(self):
        for row in self.table.get_children():
            self.table.delete(row)

        total_stock = 0

        for item in inventory.items:
            total_stock += item.get_quantity()

            if isinstance(item, PerishableItem):
                item_type = "Perishable"
                details = f"{item.days_until_expiry} days left"

            elif isinstance(item, ElectronicItem):
                item_type = "Electronic"
                details = f"{item.warranty_months} months warranty"

            else:
                item_type = "Regular"
                details = "-"

            self.table.insert(
                "",
                "end",
                values=(
                    item.name,
                    item_type,
                    item.get_quantity(),
                    f"PHP {item.get_price():.2f}",
                    f"PHP {item.total_value():.2f}",
                    details
                )
            )

        self.item_count.config(text=str(len(inventory.items)))
        self.stock_count.config(text=str(total_stock))

        self.total_value.config(
            text=f"PHP {inventory.total_inventory_value():,.2f}"
        )

    def create_popup(self, title, size):
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry(size)
        window.resizable(False, False)
        window.configure(bg="white")
        window.transient(self.root)
        window.grab_set()

        tk.Label(
            window,
            text=title,
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#222222"
        ).pack(anchor="w", padx=25, pady=(20, 15))

        return window

    def create_entry(self, parent, label):
        tk.Label(
            parent,
            text=label,
            font=("Arial", 10),
            bg="white",
            fg="#555555"
        ).pack(anchor="w", padx=25, pady=(5, 3))

        entry = tk.Entry(
            parent,
            font=("Arial", 11),
            relief="solid",
            bd=1
        )
        entry.pack(fill="x", padx=25, ipady=6)

        return entry

    def add_item(self):
        window = self.create_popup("Add Item", "360x470")

        name_entry = self.create_entry(window, "Item Name")

        tk.Label(
            window,
            text="Item Type",
            bg="white",
            fg="#555555",
            font=("Arial", 10)
        ).pack(anchor="w", padx=25, pady=(10, 3))

        item_type = ttk.Combobox(
            window,
            values=["Regular", "Perishable", "Electronic"],
            state="readonly"
        )
        item_type.set("Regular")
        item_type.pack(fill="x", padx=25, ipady=4)

        quantity_entry = self.create_entry(window, "Quantity")
        price_entry = self.create_entry(window, "Price (PHP)")

        extra_label = tk.Label(
            window,
            text="Additional Information",
            bg="white",
            fg="#555555",
            font=("Arial", 10)
        )
        extra_label.pack(anchor="w", padx=25, pady=(8, 3))

        extra_entry = tk.Entry(
            window,
            font=("Arial", 11),
            relief="solid",
            bd=1
        )
        extra_entry.pack(fill="x", padx=25, ipady=6)

        def change_extra_label(event=None):
            selected = item_type.get()

            if selected == "Perishable":
                extra_label.config(text="Days Until Expiry")
            elif selected == "Electronic":
                extra_label.config(text="Warranty (Months)")
            else:
                extra_label.config(text="Not Required")
                extra_entry.delete(0, tk.END)

        item_type.bind(
            "<<ComboboxSelected>>", change_extra_label
        )
        change_extra_label()

        def save_item():
            try:
                name = name_entry.get().strip()

                if not name:
                    raise ValueError("Please enter an item name.")

                if inventory.search(name):
                    raise ValueError("This item already exists.")

                quantity = int(quantity_entry.get())
                price = float(price_entry.get())

                if quantity < 0 or price < 0:
                    raise ValueError(
                        "Quantity and price cannot be negative."
                    )

                selected = item_type.get()

                if selected == "Perishable":
                    days = int(extra_entry.get())
                    item = PerishableItem(
                        name, quantity, price, days
                    )

                elif selected == "Electronic":
                    warranty = int(extra_entry.get())
                    item = ElectronicItem(
                        name, quantity, price, warranty
                    )

                else:
                    item = Item(name, quantity, price)

                if inventory.add_item(item):
                    self.refresh_table()
                    messagebox.showinfo(
                        "Success",
                        "Item added successfully.",
                        parent=window
                    )
                    window.destroy()

            except ValueError as error:
                messagebox.showerror(
                    "Invalid Input", str(error), parent=window
                )

        tk.Button(
            window,
            text="Save Item",
            command=save_item,
            bg="#333333",
            fg="white",
            relief="flat",
            font=("Arial", 10, "bold"),
            pady=9,
            cursor="hand2"
        ).pack(fill="x", padx=25, pady=18)

    def get_item(self, title):
        name = tk.simpledialog.askstring(
            title, "Enter item name:", parent=self.root
        )

        if name is None:
            return None

        if not name.strip():
            messagebox.showwarning(
                "Invalid Input", "Item name cannot be empty."
            )
            return None

        item = inventory.search(name.strip())

        if item is None:
            messagebox.showerror(
                "Not Found", "Item does not exist."
            )

        return item

    def get_quantity(self, title):
        from tkinter import simpledialog

        return simpledialog.askinteger(
            title,
            "Enter quantity:",
            parent=self.root,
            minvalue=1
        )

    def restock_item(self):
        item = self.get_item("Restock Item")

        if item is None:
            return

        qty = self.get_quantity("Restock Item")

        if qty is not None:
            item.restock(qty)
            self.refresh_table()

            messagebox.showinfo(
                "Success", "Stock updated successfully."
            )

    def sell_item(self):
        item = self.get_item("Sell Item")

        if item is None:
            return

        qty = self.get_quantity("Sell Item")

        if qty is None:
            return

        if item.sell(qty):
            self.refresh_table()
            messagebox.showinfo(
                "Success", "Item sold successfully."
            )
        else:
            messagebox.showerror(
                "Sale Failed", "Not enough stock available."
            )

    def search_item(self):
        item = self.get_item("Search Item")

        if item is None:
            return

        item.display()

        details = (
            f"Item: {item.name}\n"
            f"Quantity: {item.get_quantity()}\n"
            f"Price: PHP {item.get_price():.2f}\n"
            f"Total Value: PHP {item.total_value():.2f}"
        )

        if isinstance(item, PerishableItem):
            details += (
                f"\nDays Until Expiry: {item.days_until_expiry}"
            )

        elif isinstance(item, ElectronicItem):
            details += (
                f"\nWarranty: {item.warranty_months} months"
            )

        messagebox.showinfo("Item Found", details)

    def display_all(self):
        self.refresh_table()

        if not inventory.items:
            messagebox.showinfo(
                "Inventory", "There are no items yet."
            )

    def show_total(self):
        total = inventory.total_inventory_value()

        messagebox.showinfo(
            "Total Inventory Value",
            f"PHP {total:,.2f}"
        )

    def exit_app(self):
        answer = messagebox.askyesno(
            "Exit",
            "Do you want to close the application?"
        )

        if answer:
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()