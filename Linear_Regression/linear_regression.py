# Linear Regression using Python

from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Sample data
x = [[1], [2], [3], [4], [5]]
y = [2, 4, 6, 8, 10]

# Train the model
model = LinearRegression()
model.fit(x, y)

# Print model parameters
print(f"Slope: {model.coef_[0]}")
print(f"Intercept: {model.intercept_}")

# Make a prediction
prediction = model.predict([[6]])
print(f"Prediction for x=6: {prediction[0]}")

# Visualization
plt.scatter([i[0] for i in x], y, color='blue', label='Data')
plt.plot([i[0] for i in x] + [6], model.predict(x + [[6]]), color='red', label='Regression line')
plt.scatter(6, prediction, color='green', label='Prediction for x=6')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.title('Linear Regression Example')
plt.grid(True)
plt.show()