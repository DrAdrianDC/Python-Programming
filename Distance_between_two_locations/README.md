# Distance between two locations

## Overview

This project demonstrates how to calculate the distance between two geographic locations on Earth using the Haversine Formula. The formula is widely used in navigation and mapping applications to determine the shortest distance between two points on a sphere, given their latitude and longitude coordinates. It accounts for the curvature of the Earth, making it more accurate than using simple Euclidean geometry.


### Haversine Formula

The Haversine formula calculates the great-circle distance between two points on a sphere given their longitudes and latitudes:

$$
a = \sin^2\left(\frac{\Delta \phi}{2}\right) + \cos(\phi_1) \cdot \cos(\phi_2) \cdot \sin^2\left(\frac{\Delta \lambda}{2}\right)
$$

$$
c = 2 \cdot \text{atan2}\left(\sqrt{a}, \sqrt{1 - a}\right)
$$

$$
d = R \cdot c
$$

Where:
- $\phi_1$ and $\phi_2$ are the latitudes of the two locations in radians.
- \( \Delta \phi \) is the difference between the latitudes: \( \phi_2 - \phi_1 \),
- \( \Delta \lambda \) is the difference between the longitudes: \( \lambda_2 - \lambda_1 \),
- \( R \) is the Earth's radius (mean radius = 6,371 km),
- \( d \) is the distance between the two points along the surface of the sphere (in kilometers).
