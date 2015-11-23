import matplotlib.pyplot as plt

results = [94.3, 96.64, 97.34, 97.51, 97.84, 97.84, 97.88, 98.03, 98.08, 98.11]
results_y = [x for x in range(0, 101)]
results_x = [y for y in range(1, 11)]
plt.plot(results_x, results)
plt.xlabel("Epochs")
plt.ylabel("Correct %")
plt.show()
