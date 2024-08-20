# Differential Equation Solver in Python

This simple project demonstrates how to solve ordinary differential equations (ODEs) using Python. The project includes a Python script that solves a first-order differential equation using the `scipy` library and visualizes the solution with `matplotlib`.

## Problem Statement

We aim to solve the following first-order ODE:

\[ \frac{dy}{dt} = -2y + \sin(t) \]

with the initial condition:

\[ y(0) = 1 \]

## Features

- **Solving ODEs**: The project uses the `odeint` function from the `scipy.integrate` module to solve the differential equation.
- **Plotting Results**: The solution of the ODE is visualized using `matplotlib`, showing how the function \( y(t) \) evolves over time.
- **Expression Extraction**: The project includes functionality to print the differential equation's expression directly from the function definition.

## Installation

To run this project, you need to have Python installed along with the following libraries:

- `numpy`
- `matplotlib`
- `scipy`
- `inspect`

You can install the required libraries using `pip`:

```bash
pip install numpy matplotlib scipy

