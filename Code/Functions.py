# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
@author: Phoenix
"""

import sqlite3
import tkinter as tk

def create_connection(db_name):
    """
    Function to create connection
    """
    conn = sqlite3.connect(db_name)
    print(conn.total_changes)
    cursor = conn.cursor()
    return conn, cursor

def close_connection(conn):
    """
    Function to close connection
    """
    conn.commit()
    conn.close()

#Managers operations
def create_table_managers(cursor):
    """
    Function to create the stocks table
    """
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stocks (
            Id INTEGER PRIMARY KEY,
            ItemName TEXT,
            Quantity INTEGER,
            ItemPrice INTEGER
        )
    ''')

def insert_data_managers(cursor, data):
    """
    Function to insert data into the stocks table
    """
    cursor.execute("INSERT INTO stocks (ItemName, Quantity, ItemPrice) VALUES (?, ?, ?)", data)
    
def get_items_managers(cursor):
    """
    Function to get all items from stocks table
    """
    cursor.execute("SELECT Id, ItemName, Quantity, ItemPrice FROM stocks")
    return cursor.fetchall()

def update_data_managers(cursor, data):
    """
    Function to update items in stocks table
    """
    cursor.execute("UPDATE stocks SET ItemName = ?, Quantity = ?, ItemPrice = ? WHERE Id = ?", data)

def clr_entries_managers(item, quantity, price):
    """
    Function to clear entries in the Tkinder management form
    """
    #clear entry fields
    item.delete(0, tk.END)
    quantity.delete(0, tk.END)
    price.delete(0, tk.END)

def count_unsold_items(cursor):
    """
    Function to count unsold items
    """
    cursor.execute("SELECT Quantity FROM stocks")
    return cursor.fetchall()

def count_total_sales(cursor):
    """
    Function to count total sales
    """
    cursor.execute("SELECT TotalPrice FROM sold")
    return cursor.fetchall()

def delete_item(cursor, Id):
    """
    Function to delete specific item from stocks table
    """
	# Delete From Database
    cursor.execute("DELETE from stocks WHERE Id=?", [Id])

def delete_all_stocks(cursor):
    """
    Function to Delete all items from stocks
    """
    cursor.execute("DROP TABLE stocks")
    create_table_managers(cursor)


#Sales Staff Operations
def search_item_sales(search, cursor):
    """
    Function to search for an item from stocks table
    """
    cursor.execute("SELECT Id FROM stocks WHERE ItemName=?", [search])
    srch_result = cursor.fetchone()
    return srch_result[0] if srch_result else None

def get_item_stocks(IdSold, cursor):
    """
    Function to get items from a specific row
    """
    cursor.execute("SELECT ItemName, Quantity, ItemPrice FROM stocks WHERE Id=?", [IdSold])
    return cursor.fetchall()

def create_table_sales(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sold (
            Id INTEGER PRIMARY KEY,
            IdSold INTEGER,
            ItemName TEXT,
            QuantitySold INTEGER,
            TotalPrice
        )
    ''')

def insert_data_sales(cursor, data):
    """
    Function to insert data into sold table
    """
    cursor.execute("INSERT INTO sold (IdSold, ItemName, QuantitySold, TotalPrice) VALUES (?, ?, ?, ?)", data)
    print("Item Sold In 'sold' Table")
    
def update_stock_table(cursor, data):
    """
    Function to quantity in stock table
    """
    cursor.execute("UPDATE stocks SET Quantity = ? WHERE Id = ?", data)

def get_items_sales(cursor):
    """
    Function to get all items from sold table
    """
    cursor.execute("SELECT Id, ItemName, QuantitySold, TotalPrice FROM sold")
    return cursor.fetchall()

def get_item_sales(Id, cursor):
    """
    Function to get specific items from sold table
    """
    cursor.execute("SELECT ItemName, QuantitySold, TotalPrice, IdSold FROM sold WHERE Id=?", [Id])
    return cursor.fetchall()

def display_all_sales(cursor):
    """
    Function to display items from sold table
    """
    data = get_items_sales(cursor)
    return data

def cancel_sale(cursor, data, Id):
    """
    Function to modify items from sold table and stocks table
    """
    # Return to stocks
    cursor.execute("UPDATE stocks SET Quantity = ? WHERE Id = ?", data)
	# Delete From Database
    cursor.execute("DELETE from sold WHERE Id=?", [Id])
    
def delete_all_sales(cursor):
    """
    Function to get delete all items in sold table
    """
    cursor.execute("DROP TABLE sold")
    create_table_sales(cursor)