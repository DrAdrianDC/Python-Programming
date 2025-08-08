
# Scatter Plot using poorly in Python

# pip install plotly


import plotly.express as px

data = px.data.iris()


# Plotting
fig = px.scatter(data, x='sepal_width', y='sepal_length' ,
                            color='species' ,
                            title="Interactive  Iris Dataset Scatter Plot")


# Display the figure
fig.show()

# Save the figure as a PNG
fig.write_image("iris_scatter_plot.png")

