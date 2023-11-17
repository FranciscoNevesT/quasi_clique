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

def calc_density(solution: set, graph: dict) -> float:
  """
  Calculate the density of a given solution in a graph.

  Parameters:
  - solution (set): Set of nodes representing the solution.
  - graph (dict): Graph representation where keys are nodes and values are lists of neighbors.

  Returns:
  - float: Density of the solution in the graph.
  """
  if len(solution) == 1:
    return 1

  solution_size = len(solution)
  num_edges = 0
  num_max_edges = (solution_size * (solution_size - 1)) / 2


  # Count the edges between nodes in the solution
  for node in solution:
    for node_neighbor in graph[node]:
      if node_neighbor in solution:
        num_edges += 1

  num_edges = num_edges / 2

  return num_edges / num_max_edges


def neighborhood(solution: set, graph, base_density: float, neighborhood_number: int, epsilon: float):
  """
  Generate a neighborhood of a solution in a graph.

  Parameters:
  - solution (set): Current solution nodes.
  - graph (dict): Graph representation where keys are nodes and values are lists of neighbors.
  - base_density (float): Density of the current solution.
  - neighborhood_number (int): Number of nodes to add/remove in the neighborhood.
  - epsilon (float): Threshold for density, if the new density is greater than or equal to this value, the process stops.

  Returns:
  - solution_in (set): Updated solution after generating the neighborhood.
  - density (float): Density of the updated solution.
  - end (bool): True if the change ocorreu, False otherwise.
  """
  num_out_node = np.random.randint(1, min(len(solution) - 1, neighborhood_number) + 1)
  num_in_node = neighborhood_number - num_out_node

  neighbors = set()

  # Find neighbors of nodes in the current solution
  for node in solution:
    for neighbor in graph[node]:
      if neighbor not in solution:
        neighbors.add(neighbor)

  solution_in = solution.copy()
  solution = solution.copy()

  # Randomly remove nodes from the solution
  nodes_out = np.random.choice(list(solution_in), num_out_node, replace=False)
  for node in nodes_out:
    solution_in = solution_in - {node}

  # Randomly add nodes from the neighbors
  nodes_in = np.random.choice(list(neighbors), num_in_node, replace=False)
  for node in nodes_in:
    solution_in.add(node)

  density = calc_density(solution_in, graph)

  # Check if the new density is greater than or equal to the threshold
  if density >= epsilon:
    return solution_in, density, True
  else:
    return solution, base_density, False

# Get the graph from the specified path
graph = get_graph(path="data/johnson8-2-4.mtx")

# Initialize the solution with node '1', density, and epsilon
solution = set('1')
density = 1

best_solution = set()

c = 1000
for _ in range(100):
  while True:
    # Update the solution, density, and check if the process should stop
    solution, density, end = add_node(solution, graph, density=density, epsilon=0.9)

    if end:
      break

  if len(solution) > len(best_solution):
    best_solution = solution.copy()

  print(solution)
  change = False
  c = 1000
  while change == False and c > 0:
    solution, density, change = neighborhood(solution,graph,base_density = density,neighborhood_number = 2,epsilon=0.9)
    c -= 1

density = calc_density(best_solution,graph)
# Print the final solution, density, and end status
print("Final Solution:", best_solution)
print("Final Density:", density)
