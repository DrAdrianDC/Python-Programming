#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 17:24:46 2024

@author: adriandominguezcastro
"""

# File Reader Program

# The program demonstrates basic error handling using `try` and `except` blocks to manage common issues such as missing files, permission errors, and unexpected exceptions.


print("*********************************************************")
print("**                                                     **") 
print("**             FILE READER                             **") 
print("**                                                     **") 
print("*********************************************************")



def read_file():
    try:
        # Ask the user to enter the name of the file
        file_name = input("Enter the name of the file you want to read: ")
        
        # Try to open and read the file
        with open(file_name, 'r') as file:
            content = file.read()
            print("\nFile content:\n")
            print(content)
    
    except FileNotFoundError:
        # Handle the case where the file does not exist
        print(f"Error: The file '{file_name}' does not exist.")
    
    except PermissionError:
        # Handle the case where the user does not have permission to read the file
        print(f"Error: You do not have permission to access the file '{file_name}'.")
    
    except Exception as e:
        # Handle any other type of exception that may occur
        print(f"An unexpected error occurred: {e}")
    
    finally:
        # This block always executes, regardless of whether an exception occurred or not
        print("File reading operation completed.")

# Call the function to execute the file reading
read_file()

