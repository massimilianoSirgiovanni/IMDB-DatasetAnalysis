from graphConstruction import indexToMovie

# IMPLEMENTAZIONE SOVRASCRITTURA DEL GRAFO

def createActorGraphMovie(graph):
    max = (0, 0, 0)
    dictEdge = {}
    for movie in indexToMovie:
        tmp = linkActorsFromMovie(graph, movie, dictEdge)
        if max[2] < tmp[2]:
            max = tmp
    return (graph, max)


def linkActorsFromMovie(graph, movie, dictEdge):
    max = (0, 0, 0)
    actors = list(graph.neighbors(movie))
    graph.remove_node(movie)
    for i in range(0, len(actors)):
        for j in range(i + 1, len(actors)):
            tmp = 0
            if graph.has_edge(actors[i], actors[j]) == False:
                graph.add_edge(actors[i], actors[j])
                dictEdge[f"({actors[i]}, {actors[j]})"] = 1
            else:
                if f"({actors[i]}, {actors[j]})" in dictEdge:
                    tmp = dictEdge[f"({actors[i]}, {actors[j]})"]
                    dictEdge[f"({actors[i]}, {actors[j]})"] = tmp + 1
                else:
                    tmp = dictEdge[f"({actors[j]}, {actors[i]})"]
                    dictEdge[f"({actors[j]}, {actors[i]})"] = tmp + 1
            if max[2] < tmp + 1:
                max = (actors[i], actors[j], tmp + 1)
    return max