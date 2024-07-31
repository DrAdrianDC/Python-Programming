## Root-Finding Algorithms 

This folder contains two Python programs that implement root-finding algorithms: Bisection Method and Newton-Raphson Method. These algorithms are used to find roots of a given function, which are points where the function evaluates to zero.

### Bisection Method

The Bisection Method is a straightforward iterative method to find the root of a function. It works by repeatedly bisecting an interval and selecting a subinterval in which a root must lie.
#### How it Works

    Start with an interval [a,b][a,b] where the function changes sign.
    Compute the midpoint c=a+b/2
    Determine the subinterval [a,c][a,c] or [c,b][c,b] where the function changes sign.
    Repeat the process until the interval is sufficiently small.

The algorithm is guaranteed to converge if the function is continuous on [a,b][a,b] and f(a)f(a) and f(b)f(b) have opposite signs.

### Newton-Raphson Method

The Newton-Raphson Method is an efficient and widely used iterative method to find roots of a real-valued function. It uses the function's derivative to converge to a root.
#### How it Works

    Start with an initial guess x0​.
    Compute the next approximation using the formula: xn+1=xn−f(xn)f′(xn)xn+1​=xn​−f′(xn​)f(xn​)​.
    Repeat the process until convergence is achieved.

This method typically converges faster than the Bisection Method but requires the function to be differentiable and the initial guess to be sufficiently close to the actual root.

## How to usage

Running Bisection Method

To run the Bisection Method, execute the bisection.py script:

python bisection.py


Running Newton-Raphson Method

To run the Newton-Raphson Method, execute the newton_raphson.py script:

python newton_raphson.py


## Requirements

    Python 3.8.3
    NumPy 

    

