## Root-Finding Algorithms 

This folder contains two Python programs that implement root-finding algorithms: Bisection Method and Newton-Raphson Method. These algorithms are used to find roots of a given function, which are points where the function evaluates to zero.

### Bisection Method

The Bisection Method is a straightforward iterative method to find the root of a function. It works by repeatedly bisecting an interval and selecting a subinterval in which a root must lie.
How it Works

    Start with an interval [a,b][a,b] where the function changes sign.
    Compute the midpoint c=a+b/2
    Determine the subinterval [a,c][a,c] or [c,b][c,b] where the function changes sign.
    Repeat the process until the interval is sufficiently small.

The algorithm is guaranteed to converge if the function is continuous on [a,b][a,b] and f(a)f(a) and f(b)f(b) have opposite signs.
