## Root-Finding Algorithms 

This folder contains two Python programs that implement root-finding algorithms: Bisection Method and Newton-Raphson Method. These algorithms are used to find roots of a given function, which are points where the function evaluates to zero.

### Bisection Method

The Bisection Method is a straightforward iterative method to find the root of a function. It works by repeatedly bisecting an interval and selecting a subinterval in which a root must lie.
#### How it Works

1. Start with an interval `[a, b]` where the function changes sign, i.e., `f(a) * f(b) < 0`.
2. Compute the midpoint `c = (a + b) / 2`.
3. Determine the subinterval `[a, c]` or `[c, b]` where the function changes sign:
   - If `f(a) * f(c) < 0`, then the root is in the interval `[a, c]`.
   - Otherwise, the root is in the interval `[c, b]`.
4. Update the interval to the subinterval identified in the previous step.
5. Repeat the process until the interval `[a, b]` is sufficiently small.

This method is guaranteed to converge to a root if the function is continuous on `[a, b]` and `f(a)` and `f(b)` have opposite signs.

### Newton-Raphson Method

The Newton-Raphson Method is an efficient and widely used iterative method to find roots of a real-valued function. It uses the function's derivative to converge to a root.
#### How it Works

### How it Works

1. Start with an initial guess `x_0`.
2. Compute the next approximation using the formula:

   `x_(n+1) = x_n - f(x_n) / f'(x_n)`

3. Repeat the process until convergence is achieved.

This method typically converges faster than the Bisection Method but requires the function to be differentiable and the initial guess to be sufficiently close to the actual root.


## How to usage

 **Run the Program**
```bash
./python bisection.py
```
or

```bash
python bisection.py
```

Running Newton-Raphson Method

To run the Newton-Raphson Method, execute the newton_raphson.py script:

```bash
./python newton_raphson.py
```
or

```bash
python newton_raphson.py
```


## Requirements

    Python 3.8.3
    NumPy 

    

