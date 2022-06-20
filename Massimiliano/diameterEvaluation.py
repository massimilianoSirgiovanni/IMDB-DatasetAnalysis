import networkx as nx


def nodeGradeMax(graph):
    maxN = -1  # Variable to store the id of the current
    sumMax = 0
    giant = max(nx.connected_components(graph), key=len)

    for i in giant:
        neighbors = list(graph.neighbors(i))
        sumN = len(neighbors)
        if sumN > sumMax:
            sumMax = sumN
            maxN = i
    if maxN == -1:
        print("ERROR: NO NODE FOUND IN THE GRAPH")
        return -1
    else:
        return maxN


visitNodes = {}


def bfs(graph, startNode):

    nodeDistance = {startNode: 0}

    nodeToVisit = [startNode]
    index = 0
    max = 0

    while index < len(nodeToVisit):
        currentVert = nodeToVisit[index]
        neighbors = list(graph.neighbors(currentVert))

        for nbr in neighbors:
            if nbr not in nodeDistance:
                nodeToVisit.append(nbr)
                nodeDistance[nbr] = nodeDistance[currentVert] + 1
                if nodeDistance[nbr] > max:
                    max = nodeDistance[nbr]
        index = index + 1

    return max


# Calcolo dell'eccentricità
def eccentricity(graph, startNode):
    max = bfs(graph, startNode)

def dinameter(graph, startNode):
    i = eccentricity(graph, startNode)
    
    return max