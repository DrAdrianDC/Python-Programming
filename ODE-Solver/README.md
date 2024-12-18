# Ordinary Differential Equation Solver in Python

This simple project demonstrates how to solve ordinary differential equations (ODEs) using Python. The project includes a Python script that solves a first-order differential equation using the `scipy` library and visualizes the solution with `matplotlib`.

## Problem Statement

We aim to solve the following first-order ODE:

$$
\frac{dy}{dt} = -2y + \sin(t)
$$

with the initial condition:

$$
y(0) = 1
$$
## Features

- **Solving ODEs**: The project uses the `odeint` function from the `scipy.integrate` module to solve the differential equation.
- **Plotting Results**: The solution of the ODE is visualized using `matplotlib`, showing how the function \( y(t) \) evolves over time.


## Requirements

* Python 3.8.3
  
To run this project, you need to have Python installed along with the following libraries:

- `numpy`
- `matplotlib`
- `scipy`


## How to use

**1. Clone the Repository:**
```bash
git clone https://github.com/DrAdrianDC/Python-Programming.git
cd Python-Programming/ODE-Solver/

```
**2. Run the Script:**
Execute the Python script to solve the ODE and display the plot:
```bash
python ODE.py
```
**3. Output:**

    The script will print the differential equation being solved.
    The solution y(t)y(t) will be plotted and displayed.
    The plot will be saved as ode_solution.png in the current directory. 

## Customization

You can modify the differential equation by editing the dydt function in the script. For example, to solve a different ODE, simply change the expression inside the dydt function.
