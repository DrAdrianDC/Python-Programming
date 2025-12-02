# Distance between two locations

## Overview

This project demonstrates how to calculate the distance between two geographic locations on Earth using the Haversine Formula. The formula is widely used in navigation and mapping applications to determine the shortest distance between two points on a sphere, given their latitude and longitude coordinates. It accounts for the curvature of the Earth, making it more accurate than using simple Euclidean geometry.


### Haversine Formula

The Haversine formula calculates the great-circle distance between two points on a sphere given their longitudes and latitudes:

$$
d = 2 \cdot R \cdot \arcsin (\sqrt{\sin^2\left(\frac{\Delta \phi}{2}\right) + \cos(\phi_1) \cdot \cos(\phi_2) \cdot \sin^2\left(\frac{\Delta \lambda}{2}\right)})
$$


Where:
- $\phi_1$ and $\phi_2$ are the latitudes of the two locations in radians.
- ( $\Delta \phi $) is the difference between the latitudes: ($\phi_2 - \phi_1$),
- ( $\Delta \lambda $) is the difference between the longitudes: ($\lambda_2 - \lambda_1$),
- \( R \) is the Earth's radius (mean radius = 6,371 km),
- \( d \) is the distance between the two points along the surface of the sphere (in kilometers).


## Requirements

- **Python 3.8.3**
  
To run this code, you'll need the following Python packages:

- `numpy`

You can install the required packages using pip:

```bash
pip install numpy
```


## How to Use
1- Clone or download the script.

2- Run the script and the input data about.
```bash
python haversine.py
```
3- Enter by keyboard the requiered input data . 
