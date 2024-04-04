# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 17:06:37 2024

@author: Phoenix
"""

import Functions
from tkinter import ttk, messagebox
import tkinter as tk

db_name = 'phoenix.db'
conn, cursor = Functions.create_connection(db_name)

Functions.create_table_managers(cursor)


#setup User Interface
def add_stocks_btn():
    Quantity = 0
    ItemPrice = 0
    ItemName = item.get() 
    try:
        Quantity = int(quantity.get())
        try:
            ItemPrice  = float(price.get())
            if ItemName and Quantity and ItemPrice:
                data = (ItemName, Quantity, ItemPrice)
                Functions.insert_data_managers(cursor, data)
                Functions.clr_entries_managers(item, quantity, price)
                display_all_stocks_btn()
                print("New Stock Item Added.")
        except ValueError:
            allert_center2.config(text="Please Enter A Number!!") 
    except ValueError:
        allert_center1.config(text="Please Enter A Number!!") 
        
        
def display_all_stocks_btn():
    show_calculations()
    data = Functions.get_items_managers(cursor)
    # Clear The Treeview Table
    tree.delete(*tree.get_children())
    for row in data:
        print(f"Item Name: {row[1]}, Qty: {row[2]}, Price: {row[3]}")
        tree.insert("", tk.END, values=row)

def show_calculations():
    unsold = Functions.count_unsold_items(cursor)
    total_sales = Functions.count_total_sales(cursor)
    total_sold = 0
    total_unsold = 0
    
    for row in total_sales:
        total_sold = total_sold + row[0]
        
    for row in unsold:
        total_unsold = total_unsold + row[0]
        
    to_touring = (25/100) * total_sold
    total_sales_lbl.config(text=f"Total Sales: {total_sold}")
    touring_band_return_lbl.config(text=f"Return to Touring Band: {to_touring}")
    total_unsold_lbl.config(text=f"Total Items Unsold: {total_unsold}")

def select_stocks(event):
    Functions.clr_entries_managers(item, quantity, price)
    select = tree.focus()
    select_values = tree.item(select, 'values')
    global itemId
    itemId = select_values[0]
    print(f"ItemId: {itemId}")
    #place selection in entry box
    item.insert(0, select_values[1])
    quantity.insert(0, select_values[2])
    price.insert(0, select_values[3])
    
def delete_stock_item():
    delItem = tree.selection()[0]
    tree.delete(delItem)
    Id = itemId
    Functions.delete_item(cursor, Id)
    Functions.clr_entries_managers(item, quantity, price)
    
def update_stocks():
    select = tree.focus()
	# Update record
    tree.item(select, text="", values=(item.get(), quantity.get(), price.get()))
    data = (item.get(), quantity.get(), price.get(), itemId)
    Functions.update_data_managers(cursor, data)
    Functions.clr_entries_managers(item, quantity, price)
    display_all_stocks_btn()
    print("Stock Item Updated.")

def delete_all_btn():
    response = messagebox.askyesno("WAAAIT!!!!", "Sure You Want To Delete EVERYTHING?!")
    if response == 1:
        Functions.delete_all_stocks(cursor)
        # Clear the Treeview
        for record in tree.get_children():
            tree.delete(record)
    display_all_stocks_btn()


root = tk.Tk()
root.title("Stocks Data Entry - By Manager")
tree = ttk.Treeview(root, column=("c1", "c2", "c3", "c4"), show='headings')

item_lbl = ttk.Label(root, text="Item Name:")
item_lbl.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

item = ttk.Entry(root)
item.grid(row=0, column=1, padx=10, pady=5)

qty_lbl = ttk.Label(root, text="Quantity:")
qty_lbl.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

quantity = ttk.Entry(root)
quantity.grid(row=1, column=1, padx=10, pady=5)

allert_center1 = ttk.Label(root, text="")
allert_center1.grid(row=2, column=0, padx=5, pady=5)

price_lbl = ttk.Label(root, text="Price per Item:")
price_lbl.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)

price = ttk.Entry(root)
price.grid(row=3, column=1, padx=10, pady=5)

allert_center2 = ttk.Label(root, text="")
allert_center2.grid(row=4, column=0, padx=5, pady=5)

# Button to add data
add_button = ttk.Button(root, text="Add To Stock", command=add_stocks_btn)
add_button.grid(row=5, column=0, padx=5, pady=5)

#All items in stocks table
update_button = ttk.Button(text="Update Record", command=update_stocks)
update_button.grid(row=5, column=1, padx=5, pady=5)

remove_select_button = ttk.Button(text="Delete Selected", command=delete_stock_item)
remove_select_button.grid(row=5, column=2, padx=5, pady=5)

remove_all_button = ttk.Button(text="Delete All Records", command=delete_all_btn)
remove_all_button.grid(row=5, column=3, padx=5, pady=5)

#Button to get all data
refresh_button = ttk.Button(root, text="Show/Refresh", command=display_all_stocks_btn)
refresh_button.grid(row=5, column=4, padx=5, pady=5)

total_sales_lbl = ttk.Label(root, text="")
total_sales_lbl.grid(row=6, column=0, padx=5, pady=5)

total_unsold_lbl = ttk.Label(root, text="")
total_unsold_lbl.grid(row=7, column=0, padx=5, pady=5)

touring_band_return_lbl = ttk.Label(root, text="")
touring_band_return_lbl.grid(row=8, column=0, padx=5, pady=5)

tree.column("#1", anchor=tk.CENTER)
tree.heading("#1", text="Id")
tree.column("#2", anchor=tk.CENTER)
tree.heading("#2", text="Item Name")
tree.column("#3", anchor=tk.CENTER)
tree.heading("#3", text="Quantity")
tree.column("#4", anchor=tk.CENTER)
tree.heading("#4", text="Item Price")
tree.grid(column=0, columnspan=5, pady=10)

# Bind the treeview
tree.bind("<ButtonRelease-1>", select_stocks)

# Run the GUI
root.mainloop()

Functions.close_connection(conn)