import matplotlib.pyplot as plt

results = [43.54, 55.32, 58.84, 62.88, 66.93, 70.14, 71.8, 73.38, 75.14, 76.99]
results_y = [x for x in range(0, 101)]
results_x = [y for y in range(1, 11)]
plt.plot(results_x, results)
plt.xlabel("Epochs")
plt.ylabel("Correct %")
plt.show()
