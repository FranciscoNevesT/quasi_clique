from VNS import *
import os
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

num_sample = 5
epsilon = 0.95
neighborhood_x = [2,3,4]
num_repetitions = 1000

data = []
for path in os.listdir("data"):
  print(path)
  if path == "vazio":
    continue

  graph = get_graph(path="data/{}".format(path))

  best_solution = None
  best_density = None
  for _ in range(num_sample):
    solution,density = vns(graph,epsilon=epsilon,num_repetitions=num_repetitions,neighborhood_x=neighborhood_x)

    if best_solution is None or len(solution) > len(best_solution):
      best_solution = solution
      best_density = density
    elif len(solution) == len(best_solution) and density > best_density:
      best_solution = solution
      best_density = density

  data.append([path,len(best_solution),best_density])

data = pd.DataFrame(data,columns=["example","num_nodes","density"])
data.to_csv("results/solution_{}.csv".format(epsilon),index=False)
print(data)