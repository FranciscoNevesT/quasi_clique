def get_graph(path):
  graph = {}

  with open(path,"r") as file:
    text = file.read()

  text_ = []

  for t in text.split("\n"):
    tipo = t.split(" ")[0]
    if tipo == "e":
      text_.append(t)

  for p in text_:
    t,i,j = p.split(" ")

    nodes = graph.setdefault(i,[])
    nodes.append(j)

    nodes = graph.setdefault(j,[])
    nodes.append(i)

  return graph