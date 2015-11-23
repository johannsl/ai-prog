import matplotlib.pyplot as plt

results = [89.44, 91.25, 92.41, 93.28, 94.07, 94.84, 95.32, 95.81, 96.18, 96.39]
results_y = [x for x in range(0, 101)]
results_x = [y for y in range(1, 11)]
plt.plot(results_x, results)
plt.xlabel("Epochs")
plt.ylabel("Correct %")
plt.show()
