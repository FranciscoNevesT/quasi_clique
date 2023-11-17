from auxiliar import get_graph
import numpy as np

def add_node(solution, graph, density, epsilon):
  """
  Add a node to the solution based on the graph, density, and epsilon.

  Parameters:
  - solution (set): Current solution nodes.
  - graph (dict): Graph representation where keys are nodes and values are lists of neighbors.
  - density (float): Current density of the solution.
  - epsilon (float): Threshold for density, if the new density falls below this value, the process stops.

  Returns:
  - solution (set): Updated solution after adding a node.
  - density (float): Updated density after adding a node.
  - end (bool): True if the process should stop, False otherwise.
  """

  neighbors = {}
  solution_size = len(solution)

  num_edges = density * ((solution_size - 1) * solution_size) / 2

  # Count the edges between solution nodes and their neighbors
  for node in solution:
    for neighbor in graph[node]:
      if neighbor not in solution:
        x = neighbors.setdefault(neighbor, 0)
        neighbors[neighbor] = x + 1

  if len(neighbors.values()) == 0:
    return solution, density, True

  max_node = None
  max_add_edges = 0

  # Find the node with the maximum number of additional edges to the solution
  for node, add_edges in neighbors.items():
    if add_edges > max_add_edges:
      max_add_edges = add_edges
      max_node = node

  max_edges_possible = ((solution_size + 1) * solution_size) / 2

  new_density = (num_edges + max_add_edges) / max_edges_possible

  # Check if the new density falls below the threshold
  if new_density < epsilon:
    return solution, density, True

  solution.add(max_node)

  return solution, new_density, False

# Get the graph from the specified path
graph = get_graph(path="data/johnson8-2-4.mtx")

# Initialize the solution with node '1', density, and epsilon
solution = set('1')
density = 1

while True:
  # Update the solution, density, and check if the process should stop
  solution, density, end = add_node(solution, graph, density=density, epsilon=0.9)

  if end:
    break

# Print the final solution, density, and end status
print("Final Solution:", solution)
print("Final Density:", density)
print("Process Ended:", end)
