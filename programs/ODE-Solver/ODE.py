#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 06:52:54 2024

@author: adriandominguezcastro
"""

print("*******************************************************************")
print("**                                                               **")
print("**    SOLVING Ordinary Differential Equations using Python       **")
print("**                                                               **")
print("*******************************************************************")

print("")
print("")
print("To solve differential equations in Python, you can use the scipy.integrate library, specifically the odeint function for ordinary differential equations (ODEs)")


# Import libraries
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

#import inspect

# Define the ODE function
def dydt(y, t):
    return -2 * y + np.sin(t)


print("")
print("")
print("Solving the differential equation: dy/dt = -2y + sin(t)")

# Print the actual function definition
#print("Function dydt:")
#print(inspect.getsource(dydt))

# Initial condition
y0 = 1

# Time points where solution is computed
t = np.linspace(0, 10, 100) # a time array t from 0 to 10, with 100 points in between, where we want to evaluate the solution.

# Solve ODE
# The odeint function takes the ODE function, initial condition, and time points as inputs and returns the solution y.
y = odeint(dydt, y0, t)



# Print summary of the solution
# Displays the minimum and maximum values of y(t) across the entire time range.
print("Summary:")
print(f"Minimum value of y: {np.min(y):.4f}")
print(f"Maximum value of y: {np.max(y):.4f}")


# Plot the results
plt.plot(t, y, label="y(t)")
plt.xlabel('Time t')
plt.ylabel('y(t)')
plt.title('Solution of the ODE dy/dt = -2y + sin(t)')
plt.legend()
plt.grid(True)

# Save the plot as a file
# plt.savefig('ode_solution.png')  # Save as PNG file
plt.savefig('ode_solution.png', dpi=300, transparent=True)

plt.show()


# Inform the user where the plot is saved
print("The plot of the solution has been saved as 'ode_solution.png' in the current directory.")
