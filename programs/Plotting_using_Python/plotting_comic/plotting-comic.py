
# Matplotlib Comic Plot

import matplotlib.pyplot as plt
import numpy as np

plt.xkcd()
plt.plot(np.sin(np.linspace(0, 10)))
plt.title('Comic Plot')

# Save the plot to a file
plt.savefig('Comic-plot.png', format='png')


plt.show()
