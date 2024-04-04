# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 07:10:42 2024

@author: Berclay
"""
from Functions import create_connection, delete_item, close_connection, update_data_managers, create_table_managers, create_table_sales, insert_data_managers
import pytest

#test for creating managers table
def test_create_table_managers():
    db_name = ":memory:"
    conn, cursor = create_connection(db_name)
    create_table_managers(cursor)
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name = 'stocks';")
    results = cursor.fetchone()
    assert results is not None
    close_connection(conn)
    
#test for creating sales table
def test_create_table_sales():
    db_name = ":memory:"
    conn, cursor = create_connection(db_name)
    create_table_sales(cursor)
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name = 'sold';")
    results = cursor.fetchone()
    assert results is not None
    close_connection(conn)
    
#testing insert and update at the same time
def test_update_data_managers():
    db_name = ":memory:"
    conn, cursor = create_connection(db_name)
    create_table_managers(cursor)
    #insert data
    data = ('data', 13, 14)
    insert_data_managers(cursor, data)
    original_data = cursor.execute("SELECT ItemName, Quantity, ItemPrice FROM stocks")
    original_data.fetchone()
    new_data = ('new_data', 15,16, 1)#item is assumed to be first on the list
    update_data_managers(cursor, new_data)
    updated_data = cursor.execute("SELECT ItemName, Quantity, ItemPrice FROM stocks WHERE Id = 1")
    updated_data.fetchone()
    
    assert updated_data == ('new_data', 15,16, 1)
    assert original_data is not None
    close_connection(conn)
    
def test_delete_item():
    db_name = ":memory:"
    conn, cursor = create_connection(db_name)
    create_table_managers(cursor)
    #insert data
    data = ('data', 13, 14)
    insert_data_managers(cursor, data)
    original_data = cursor.execute("SELECT * FROM stocks")
    original_data.fetchall()
    delete_item(cursor, 1)#item is assumed to be first on the list
    updated_data = cursor.execute("SELECT * FROM stocks")
    updated_data.fetchall()
    assert len(updated_data) == 0#No Remaining Data Expected After Deletion
    assert original_data is not None
    close_connection(conn)
    
    