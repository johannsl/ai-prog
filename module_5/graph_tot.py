import matplotlib.pyplot as plt
import numpy as np

x = np.arange(1, 11)

result1 = [94.3, 96.64, 97.34, 97.51, 97.84, 97.84, 97.88, 98.03, 98.08, 98.11]
result2 = [94.58, 96.65, 97.07, 97.58, 97.63, 97.94, 98.09, 97.98, 98.12, 98.21]
result3 = [89.44, 91.25, 92.41, 93.28, 94.07, 94.84, 95.32, 95.81, 96.18, 96.39]
result4 = [94.63, 95.44, 95.91, 96.09, 96.6, 96.48, 96.59, 96.61, 96.74, 96.69]
result5 = [43.54, 55.32, 58.84, 62.88, 66.93, 70.14, 71.8, 73.38, 75.14, 76.99]

plt.plot(x, result1)
plt.plot(x, result2)
plt.plot(x, result3)
plt.plot(x, result4)
plt.plot(x, result5)

plt.legend(['hidden layer number', 'hidden layer size', 'activation function', 'learning rate', 'back-propagation'], loc='lower right')

plt.xlabel("Epochs")
plt.ylabel("Correct %")
plt.show()
