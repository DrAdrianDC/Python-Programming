#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 02:19:35 2024

@author: adriandominguezcastro
"""

# Grocery List Management


print("*********************************************************")
print("**                                                     **") 
print("**             GROCERY LIST MANAGEMENT                 **") 
print("**                                                     **") 
print("*********************************************************")



def show_menu():
    print("\nGrocery List:")
    print("1. Add an item")
    print("2. Remove an item")
    print("3. View grocery list")
    print("4. Mark an item as purchased")
    print("5. Exit")
    return input("Select an option: ")

def add_item(grocery_list):
    name = input("Enter the name of the item: ")
    quantity = input("Enter the quantity: ")
    item = {"name": name, "quantity": quantity, "purchased": False}
    grocery_list.append(item)
    print(f"{quantity} {name}(s) added to the list.")

def remove_item(grocery_list):
    name = input("Enter the name of the item to remove: ")
    for item in grocery_list:
        if item["name"].lower() == name.lower():
            grocery_list.remove(item)
            print(f"{name} removed from the list.")
            return
    print(f"{name} not found in the list.")

def view_list(grocery_list):
    if not grocery_list:
        print("The list is empty.")
        return
    print("\nGrocery List:")
    for i, item in enumerate(grocery_list, 1):
        status = "Purchased" if item["purchased"] else "Not purchased"
        print(f"{i}. {item['name']} ({item['quantity']}) - {status}")

def mark_as_purchased(grocery_list):
    name = input("Enter the name of the item to mark as purchased: ")
    for item in grocery_list:
        if item["name"].lower() == name.lower():
            item["purchased"] = True
            print(f"{name} marked as purchased.")
            return
    print(f"{name} not found in the list.")

def main():
    grocery_list = []
    while True:
        option = show_menu()
        if option == "1":
            add_item(grocery_list)
        elif option == "2":
            remove_item(grocery_list)
        elif option == "3":
            view_list(grocery_list)
        elif option == "4":
            mark_as_purchased(grocery_list)
        elif option == "5":
            print("Exiting the program...")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
