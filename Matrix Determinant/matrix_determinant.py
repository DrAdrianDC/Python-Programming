#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 06:32:30 2024

@author: adriandominguezcastro
"""

# The matrix determinant

# Import libraries
import numpy as np

# Ask the user for the size of the square matrix
n = int(input("Enter the size of the matrix (n x n): "))

# Create a list to store the rows of the matrix
matrix_rows = []

# Ask the user to enter each row
print("Enter each row of the matrix, with elements separated by spaces:")
for i in range(n):
    while True:  # Loop until valid input is received
        try:
            row = input(f"Row {i + 1}: ").split()
            # Convert to float and check if the row has the correct number of elements
            row = list(map(float, row))
            if len(row) != n:
                print("Error: the row must have the same number of elements as the matrix size.")
                continue
            matrix_rows.append(row)
            break  # Break out of the loop if input is valid
        except ValueError:
            print("Error: Please enter numeric values only.")


# Convert the list of lists to a NumPy array
x = np.array(matrix_rows)
# Printing the matrix with two decimal places
print("The entered matrix is:")
for row in x:
    print(' '.join(['%.2f' % value for value in row]))


# Check if the matrix is square and calculate the determinant
if x.shape[0] == x.shape[1]:
    matrix_det = np.linalg.det(x)
    # Round the determinant to avoid floating-point precision issues
    matrix_det = round(matrix_det, 2)  # You can adjust the number of decimals as needed
    print("Determinant of the matrix:", matrix_det)
else:
    print("The matrix is not square. Check the data.")
