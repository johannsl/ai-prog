import matplotlib.pyplot as plt
from math import log10

results = [3.3030431013851259e-12, 3.4822975120068177e-06, 0.00017327911225070144, 9.1922308967964906e-06, 9.0512134754226715e-05, 9.1142347596850458e-06, 4.0212100360233579e-06, 1.7176906429217701e-06, 3.7151159086964058e-05, 3.7195992033241693e-10, 0.0038315756220902936, 3.2164630917894987e-06, 2.9632595531290804e-06, 3.849947793736722e-09, 2.0973277061885583e-09, 0.00014094152734067618, 0.00011492105417201478, 9.7764567946544351e-07, 0.031697430306401431, 9.3826721136490999e-08]
results_log = [-log10(x) for x in results]
results_x = [x for x in range(1, 21)]
plt.plot(results_x, results_log)
plt.xlabel("Runs")
plt.ylabel("-log10(p)")
plt.show()
