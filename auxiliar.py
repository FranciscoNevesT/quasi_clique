def get_graph(path):
  graph = {}

  with open(path,"r") as file:
    text = file.read()

  text = text.split("\n")[2:-1]

  for p in text:
    i,j = p.split(" ")

    nodes = graph.setdefault(i,[])
    nodes.append(j)

    nodes = graph.setdefault(j,[])
    nodes.append(i)

  return graph