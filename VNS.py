import time

from auxiliar import get_graph
import numpy as np
import time

def add_node(solution, graph, density, epsilon,neighbors):
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

  if neighbors is None:
    neighbors = {}

    # Count the edges between solution nodes and their neighbors
    for node in solution:
      for neighbor in graph[node]:
        if neighbor not in solution:
          x = neighbors.setdefault(neighbor, 0)
          neighbors[neighbor] = x + 1

  solution_size = len(solution)
  num_edges = density * ((solution_size - 1) * solution_size) / 2

  if len(neighbors.values()) == 0:
    return solution, density, True, neighbors

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
    return solution, density, True, neighbors

  solution.add(max_node)

  neighbors.pop(max_node)

  for neighbor in graph[max_node]:
    if neighbor not in solution:
      x = neighbors.setdefault(neighbor, 0)
      neighbors[neighbor] = x + 1

  return solution, new_density, False, neighbors

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

def vns(graph,epsilon,num_repetitions, neighborhood_x = [2,3,4],solution = None):

  if solution is None:
    solution = set('1')
    density = 1
  else:
    density = calc_density(solution,graph)

  best_solution = set()
  best_density = 0

  repetitons = {}
  for i in neighborhood_x:
    repetitons[i] = num_repetitions

  while np.sum([i for i in repetitons.values()]):
    neighbors = None
    while True:
      # Update the solution, density, and check if the process should stop
      solution, density, end,neighbors = add_node(solution, graph, density=density, epsilon=epsilon, neighbors = neighbors)
      if end:
        break

    if len(solution) > len(best_solution):
      best_solution = solution.copy()
      best_density = density
      for i in neighborhood_x:
        repetitons[i] = num_repetitions
    elif len(solution) == len(best_solution) and best_density < density:
      best_solution = solution.copy()
      best_density = density
      for i in neighborhood_x:
        repetitons[i] = num_repetitions

    if len(solution) == len(graph.keys()):
      break

    for key,num_r in repetitons.items():
      change = False
      if num_r > 0:
        while repetitons[key] > 0:
          solution, density, change = neighborhood(solution,graph,base_density = density,neighborhood_number = 5,epsilon=epsilon)
          repetitons[key] = repetitons[key] -1
          if change:
            break
      if change:
        break

  density = calc_density(best_solution,graph)

  return best_solution,density