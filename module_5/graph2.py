import matplotlib.pyplot as plt

results = [94.58, 96.65, 97.07, 97.58, 97.63, 97.94, 98.09, 97.98, 98.12, 98.21]
results_y = [x for x in range(0, 101)]
results_x = [y for y in range(1, 11)]
plt.plot(results_x, results)
plt.xlabel("Epochs")
plt.ylabel("Correct %")
plt.show()
