#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 23:11:23 2024

@author: adriandominguezcastro
"""


print("*************************************") 
print("**                                 **") 
print("**                                 **") 
print("**        CALCULATOR               **")
print("**                                 **") 
print("**                                 **") 
print("*************************************") 


# Function to add two numbers
def add(a, b):
    return a + b

# Function to subtract two numbers
def subtract(a, b):
    return a - b

# Function to multiply two numbers
def multiply(a, b):
    return a * b

# Function to divide two numbers
def divide(a, b):
    if b != 0:
        return a / b
    else:
        return "Cannot divide by zero"
    

print("Enter two numbers:")
print("First number and press Enter, and Second number and press Enter")
num1 = float(input())
num2 = float(input())

print("Which operation do you want to perform?")
print("1. Add")
print("2. Subtract")
print("3. Multiply")
print("4. Divide")
operation = input()

if operation == "1":
    print(num1, "+", num2, "=", add(num1, num2))

elif operation == "2":
    print(num1, "-", num2, "=", subtract(num1, num2))

elif operation == "3":
    print(num1, "*", num2, "=", multiply(num1, num2))

elif operation == "4":
    print(num1, "/", num2, "=", divide(num1, num2))

else:
    print("Invalid operation")


