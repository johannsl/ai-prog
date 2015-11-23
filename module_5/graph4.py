import matplotlib.pyplot as plt

results = [94.63, 95.44, 95.91, 96.09, 96.6, 96.48, 96.59, 96.61, 96.74, 96.69]
results_y = [x for x in range(0, 101)]
results_x = [y for y in range(1, 11)]
plt.plot(results_x, results)
plt.xlabel("Epochs")
plt.ylabel("Correct %")
plt.show()
