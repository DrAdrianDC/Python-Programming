# Execution time of a Python code

# This is important for Performance Optimization, Cost Efficiency, Scalability, and Debugging and Development, etc

import time

# Record start time
start = time.time()

# Code to measure

result = sum(range(1, 1000001))

# Record end time
end = time.time()

execution_time = end - start

print(f"The execution time is: {execution_time:.5f} seconds")


