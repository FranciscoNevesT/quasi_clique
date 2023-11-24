from VNS import *
import os
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

num_sample = 5
epsilon = 0.8
neighborhood_x = [2,3,4]
num_repetitions = 1000

data = []
for path in os.listdir("data"):
  if path == "vazio":
    continue

  graph = get_graph(path="data/{}".format(path))

  for _ in range(num_sample):
    best_solution,density = vns(graph,epsilon=epsilon,num_repetitions=num_repetitions,neighborhood_x=neighborhood_x)
    data.append([path,len(best_solution),density])

data = pd.DataFrame(data,columns=["example","num_nodes","density"])
sns.boxplot(data = data, x = "example", y = "num_nodes")
plt.show()

sns.boxplot(data = data, x = "example", y = "density")
plt.show()

print(data)