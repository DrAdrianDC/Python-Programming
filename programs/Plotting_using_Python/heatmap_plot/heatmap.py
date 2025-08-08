# Heatmap Plot in Python


import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

data = np.random.rand(10,12)
sns.heatmap(data, cmap='viridis') 


# Save the plot to a file
plt.savefig('heatmap.png', format='png')


plt.show()

