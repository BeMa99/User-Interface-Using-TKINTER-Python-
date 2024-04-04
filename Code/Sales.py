# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 17:26:29 2024

@author: Phoenix
"""

import Functions
from tkinter import ttk, messagebox
import tkinter as tk

db_name = 'phoenix.db'
conn, cursor = Functions.create_connection(db_name)

Functions.create_table_sales(cursor)

#set up user interface
def search_stocks_btn():
    # Clear the Treeview
    for record in tree_stocks.get_children():
        tree_stocks.delete(record)
    ItemName = search_item.get()
    if ItemName:
        global ItemId
        ItemId = Functions.search_item_sales(ItemName, cursor)
        if ItemId is not None:
            search_data = Functions.get_item_stocks(ItemId, cursor)
            for row in search_data:
                print(f"Item Name: {row[0]}, Qty: {row[1]}, Price: {row[2]}")
                tree_stocks.insert("", tk.END, values=row)
                global item_data
                item_data = search_data
        else:
            print("Item {'ItemName'} You Have Searched Is Unavailable")


def get_selection_from_popup(passed_data):
    global ItemId
    for row in passed_data:
        print(f"Item Name: {row[0]}, Qty: {row[1]}, Price: {row[2]}")
        ItemName = row[0]
        tree_stocks.insert("", tk.END, values=row)
    ItemId = Functions.search_item_sales(ItemName, cursor)
    global item_data
    item_data = passed_data


def make_sale_btn():
    Quantity = 0
    try:
        Quantity = int(quantity.get())
        for row in item_data:
            ItemName = row[0]
            OriginalQty = row[1]
            ItemPrice = row[2]
        if OriginalQty < Quantity:
            print(f"Stocks Too Little For Sale!! Can sell only: {OriginalQty}!!")
            allert_center.config(text=f"Stocks Too Little For Sale!! Can sell only: {OriginalQty}!!")
        else:
            totalPrice = ItemPrice * int(Quantity)
            data = (ItemId, ItemName, Quantity, totalPrice)
            Functions.insert_data_sales(cursor, data)
            if OriginalQty == 0:
                print("Item Sold Out")
                allert_center.config(text="Item Sold Out!")
            else:
                RemainingQuantity = OriginalQty-int(Quantity)
                stock_data_update = (RemainingQuantity, ItemId)
                Functions.update_stock_table(cursor, stock_data_update)
        refresh_sales()
    except ValueError:
        allert_center.config(text="Please Enter A Number!!") 
        refresh_sales()
    
    
def refresh_sales():
    # Clear the Treeview
    for record in tree_sales.get_children():
        tree_sales.delete(record)
    new_sale = Functions.display_all_sales(cursor)
    for row in new_sale:
        print(f"Item Name: {row[0]}, Qty: {row[1]}, TotalPrice: {row[2]}")
        tree_sales.insert("", tk.END, values=row)
    
def select_sales(event):
    select = tree_sales.focus()
    select_values = tree_sales.item(select, 'values')
    global itemId
    itemId = select_values[0]
    print(f"ItemId: {itemId}")
    
def cancel_sale_btn():
    IdSold = 0
    Qty = 0
    OriginalQty = 0
    cancelItemId = itemId
    delItem = tree_sales.selection()[0]
    tree_sales.delete(delItem)
    new_data = Functions.get_item_sales(cancelItemId, cursor)
    # Get Item details from sales table
    for row in new_data:
        Qty = row[1]
        IdSold = row[3]
    search_data = Functions.get_item_stocks(IdSold, cursor)
        
    for row in search_data:
        OriginalQty = row[1]
        
    Qty = Qty + OriginalQty
   	# cancel function
    data = (Qty, IdSold)
    Functions.cancel_sale(cursor, data, cancelItemId)
  
def delete_all_btn():
    response = messagebox.askyesno("WAAAIT!!!!", "Sure You Want To Delete EVERYTHING?!")
    Functions.delete_all_sales(cursor)
    if response == 1:
        # Clear the Treeview
        for record in tree_sales.get_children():
            tree_sales.delete(record)
            
def select_stocks(event):
    select = tree.focus()
    select_values = tree.item(select, 'values')
    global itemId
    itemId = select_values[0]
    print(f"ItemId: {itemId}")
    
def select_and_close_btn():
    SelectItem = itemId
    # Get Item details from stocks table
    if SelectItem is not None:
        data = Functions.get_item_stocks(SelectItem, cursor)
        get_selection_from_popup(data)
        for row in data:
            print(f"Item Name: {row[0]}, Qty: {row[1]}, Price: {row[2]}")
        new.destroy()
    else:
        print("Selection Ist Kaputt!!")      
        

    
root = tk.Tk()

#function to open selection window
def select_from_list_btn():
    global new
    new = tk.Toplevel(root)
    new.geometry("750x250")
    new.title("All Stocks Data - For Sales")
    
    global tree
    tree = ttk.Treeview(new, column=("c1", "c2", "c3", "c4"), show='headings')

    data = Functions.get_items_managers(cursor)
    # Clear The Treeview Table
    tree.delete(*tree.get_children())
    for row in data:
        print(f"Item Name: {row[1]}, Qty: {row[2]}, Price: {row[3]}")
        tree.insert("", tk.END, values=row)
        
    select_and_close_button = ttk.Button(new, text="Select", command=select_and_close_btn)
    select_and_close_button.grid(row=0, column=0, padx=5, pady=5)

    close_button = ttk.Button(new, text="Cancel", command=new.destroy)
    close_button.grid(row=0, column=1, padx=5, pady=5)
    
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


root.title("Sales Data Retrieval - By Sales")
tree_stocks = ttk.Treeview(root, column=("c1", "c2", "c3"), show='headings')
tree_sales = ttk.Treeview(root, column=("c1", "c2", "c3", "c4"), show='headings')

search_lbl = ttk.Label(root, text="Search/Enter Item To Sell By Item Name:")
search_lbl.grid(row=0, column=0, padx=20, pady=5, sticky=tk.W)

search_item = ttk.Entry(root)
search_item.grid(row=1, column=0, padx=20, pady=5, sticky=tk.W)

# Button to add data
search_button = ttk.Button(root, text="Search", command=search_stocks_btn)
search_button.grid(row=1, column=1, pady=10)

# Button to open selection window
select_stocks_button = ttk.Button(root, text="Select From List", command=select_from_list_btn)
select_stocks_button.grid(row=1, column=2, pady=10)

#Display items in stock section

tree_stocks.column("#1", anchor=tk.CENTER)
tree_stocks.heading("#1", text="Item Name")
tree_stocks.column("#2", anchor=tk.CENTER)
tree_stocks.heading("#2", text="Quantity")
tree_stocks.column("#3", anchor=tk.CENTER)
tree_stocks.heading("#3", text="Item Price")
tree_stocks.grid(column=0, columnspan=4, pady=10)
    
    
qty_lbl = ttk.Label(root, text="Enter Quantity of Searched Item To Be Sold:")
qty_lbl.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)

allert_center = ttk.Label(root, text="")
allert_center.grid(row=4, column=0, padx=5, pady=5)

quantity = ttk.Entry(root)
quantity.grid(row=5, column=0, padx=10, pady=5)

# Button to make sale
add_button = ttk.Button(root, text="Make Sale", command=make_sale_btn)
add_button.grid(row=6, column=0, columnspan=2, pady=10)

#Display items in sales section
cancel_sale_button = ttk.Button(text="Cancel Sale", command=cancel_sale_btn)
cancel_sale_button.grid(row=6, column=1, padx=5, pady=5)

#Display Items In Stock
show_all_button = ttk.Button(text="Show All Stock", command=delete_all_btn)
show_all_button.grid(row=6, column=2, padx=5, pady=5)

remove_all_button = ttk.Button(text="Delete All Records", command=delete_all_btn)
remove_all_button.grid(row=6, column=3, padx=5, pady=5)
# Button to show/refresh sales
refresh_button = ttk.Button(root, text="Show/Refresh", command=refresh_sales)
refresh_button.grid(row=6, column=4, padx=5, pady=5)

tree_sales.column("#1", anchor=tk.CENTER)
tree_sales.heading("#1", text="Id")
tree_sales.column("#2", anchor=tk.CENTER)
tree_sales.heading("#2", text="Item Name")
tree_sales.column("#3", anchor=tk.CENTER)
tree_sales.heading("#3", text="Quantity")
tree_sales.column("#4", anchor=tk.CENTER)
tree_sales.heading("#4", text="Total Price")
tree_sales.grid(column=0, columnspan=5, pady=10)

# Bind the treeview
tree_sales.bind("<ButtonRelease-1>", select_sales)

# Run the GUI
root.mainloop()

Functions.close_connection(conn)